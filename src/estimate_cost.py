from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean
from typing import Any

import yaml

from src.config_loader import (
    PROJECT_ROOT,
    load_config,
)


DEFAULT_QUOTA_CONFIG = (
    PROJECT_ROOT
    / "config"
    / "free_quota.yaml"
)


def resolve_project_path(
    path_value: str | Path,
) -> Path:
    path = Path(path_value)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


def load_yaml(
    path: Path,
) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Configuration not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        content = yaml.safe_load(file)

    if not isinstance(content, dict):
        raise ValueError(
            "YAML file must contain "
            f"a mapping: {path}"
        )

    return content


def load_jsonl(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Dry-run file not found: {path}"
        )

    records: list[dict[str, Any]] = []

    with path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        for line_number, line in enumerate(
            file,
            start=1,
        ):
            if not line.strip():
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as error:
                raise ValueError(
                    "Invalid JSON on line "
                    f"{line_number}: {error.msg}"
                ) from error

            if (
                not isinstance(record, dict)
                or not isinstance(
                    record.get("response"),
                    dict,
                )
            ):
                raise ValueError(
                    f"Line {line_number} lacks "
                    "a response object"
                )

            records.append(record)

    if not records:
        raise ValueError(
            "Dry-run file contains no records"
        )

    return records


def approved_free_models(
    free_models: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[str],
]:
    approved: list[dict[str, Any]] = []
    problems: list[str] = []

    required_fields = (
        "model_id",
        "provider",
        "model_name",
        "verification_date",
        "evidence_file",
        "requests_per_minute",
        "requests_per_day",
    )

    for index, model in enumerate(
        free_models,
        start=1,
    ):
        label = str(
            model.get("model_id")
            or f"entry-{index}"
        )

        if (
            model.get("authorization_status")
            != "APPROVED"
        ):
            problems.append(
                f"{label}: authorization_status "
                "is not APPROVED"
            )
            continue

        missing_fields = [
            field
            for field in required_fields
            if model.get(field) in (None, "")
        ]

        if missing_fields:
            problems.append(
                f"{label}: missing "
                + ", ".join(missing_fields)
            )
            continue

        try:
            requests_per_minute = int(
                model["requests_per_minute"]
            )
            requests_per_day = int(
                model["requests_per_day"]
            )

        except (TypeError, ValueError):
            problems.append(
                f"{label}: quota limits "
                "must be integers"
            )
            continue

        if (
            requests_per_minute <= 0
            or requests_per_day <= 0
        ):
            problems.append(
                f"{label}: quota limits "
                "must be positive"
            )
            continue

        evidence_path = resolve_project_path(
            model["evidence_file"]
        )

        if not evidence_path.is_file():
            problems.append(
                f"{label}: evidence file "
                "does not exist"
            )
            continue

        approved.append(model)

    return approved, problems


def create_projection(
    dry_run_path: Path,
    quota_config_path: Path,
    report_path: Path,
) -> None:
    experiment, _ = load_config()
    quota = load_yaml(quota_config_path)
    records = load_jsonl(dry_run_path)

    policy = quota.get("policy")
    free_models = quota.get("free_models")

    if not isinstance(policy, dict):
        raise ValueError(
            "free_quota.yaml is missing "
            "the policy mapping"
        )

    if not isinstance(free_models, list):
        raise ValueError(
            "free_models must be a YAML list"
        )

    if policy.get("access_mode") != "FREE_ONLY":
        raise ValueError(
            "access_mode must remain FREE_ONLY"
        )

    hard_budget = float(
        policy["hard_budget_usd"]
    )
    reserve_fraction = float(
        policy["reserve_fraction"]
    )
    dry_run_instances = int(
        policy["dry_run_instances"]
    )
    paid_fallback = bool(
        policy["paid_fallback_allowed"]
    )

    if hard_budget != 0.0:
        raise ValueError(
            "The hard budget must remain USD 0"
        )

    if paid_fallback:
        raise ValueError(
            "Paid fallback must remain disabled"
        )

    if reserve_fraction != 0.25:
        raise ValueError(
            "The frozen core reserve "
            "fraction must be 0.25"
        )

    dataset = experiment["dataset"]

    model_count = int(
        dataset["core_model_count"]
    )
    prompt_count = int(
        dataset["core_prompt_count"]
    )
    development_instances = int(
        dataset["development_instances"]
    )
    test_instances = int(
        dataset["test_instances"]
    )
    total_instances = int(
        dataset["total_instances"]
    )

    dry_run_calls = (
        dry_run_instances
        * model_count
        * prompt_count
    )

    development_calls = (
        development_instances
        * model_count
        * prompt_count
    )

    test_calls = (
        test_instances
        * model_count
        * prompt_count
    )

    core_calls = (
        total_instances
        * model_count
        * prompt_count
    )

    configured_core_calls = int(
        dataset["projected_core_responses"]
    )

    if core_calls != configured_core_calls:
        raise ValueError(
            "Core-call calculation disagrees "
            "with experiment.yaml"
        )

    reserve_calls = math.ceil(
        core_calls * reserve_fraction
    )

    core_ceiling = (
        core_calls + reserve_calls
    )

    extension_cap = int(
        experiment["extension"][
            "maximum_total_calls"
        ]
    )

    overall_ceiling = (
        core_ceiling + extension_cap
    )

    calls_per_model = (
        total_instances * prompt_count
    )

    reserve_per_model = math.ceil(
        calls_per_model * reserve_fraction
    )

    ceiling_per_model = (
        calls_per_model + reserve_per_model
    )

    input_values: list[float] = []
    output_values: list[float] = []

    observed_cost = 0.0
    all_dummy = True

    for index, record in enumerate(
        records,
        start=1,
    ):
        response = record["response"]

        try:
            input_values.append(
                float(
                    response[
                        "input_token_estimate"
                    ]
                )
            )

            output_values.append(
                float(
                    response[
                        "output_token_estimate"
                    ]
                )
            )

            observed_cost += float(
                response["cost_usd"]
            )

            all_dummy = (
                all_dummy
                and bool(response["is_dummy"])
            )

        except (
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            raise ValueError(
                f"Record {index} has incomplete "
                "token/cost metadata"
            ) from error

    average_input = fmean(input_values)
    average_output = fmean(output_values)

    projected_input_tokens = math.ceil(
        average_input * core_ceiling
    )

    projected_output_tokens = math.ceil(
        average_output * core_ceiling
    )

    approved, model_problems = (
        approved_free_models(free_models)
    )

    quota_ready = (
        len(approved) == model_count
    )

    budget_pass = (
        observed_cost <= hard_budget
        and not paid_fallback
    )

    if quota_ready and budget_pass:
        execution_gate = "PASS"
    else:
        execution_gate = (
            "BLOCKED_PENDING_"
            "FREE_QUOTA_VERIFICATION"
        )

    if report_path.exists():
        raise FileExistsError(
            "Projection report already exists "
            "and will not be overwritten: "
            f"{report_path}"
        )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    dry_run_display = (
        dry_run_path
        .relative_to(PROJECT_ROOT)
        .as_posix()
    )

    lines = [
        "# Phase 2 Free-Quota Projection Smoke Test",
        "",
        f"Generated UTC: {generated}",
        f"Source dry run: `{dry_run_display}`",
        (
            "Source is dummy data: "
            f"`{'YES' if all_dummy else 'NO'}`"
        ),
        "",
        "## Call projection",
        "",
        "| Segment | Required calls |",
        "|---|---:|",
        (
            f"| Ten-instance dry run | "
            f"{dry_run_calls} |"
        ),
        (
            f"| Development inventory | "
            f"{development_calls} |"
        ),
        (
            f"| Test inventory | "
            f"{test_calls} |"
        ),
        (
            f"| Frozen core matrix | "
            f"{core_calls} |"
        ),
        (
            f"| Core reserve "
            f"({reserve_fraction:.0%}) | "
            f"{reserve_calls} |"
        ),
        (
            f"| Core authorization ceiling | "
            f"{core_ceiling} |"
        ),
        (
            f"| Extension fixed cap | "
            f"{extension_cap} |"
        ),
        (
            "| Overall planned experiment "
            f"ceiling | {overall_ceiling} |"
        ),
        "",
        (
            "The ten-instance dry run uses "
            "development cases and is not added "
            "again to the frozen core matrix when "
            "its valid outputs are retained."
        ),
        "",
        "## Token projection",
        "",
        f"- Observed records: {len(records)}",
        (
            "- Average input-token estimate: "
            f"{average_input:.2f}"
        ),
        (
            "- Average output-token estimate: "
            f"{average_output:.2f}"
        ),
        (
            "- Projected input tokens at the "
            f"core ceiling: {projected_input_tokens}"
        ),
        (
            "- Projected output tokens at the "
            f"core ceiling: {projected_output_tokens}"
        ),
        "",
        (
            "Dummy whitespace-token estimates are "
            "infrastructure checks only. Replace "
            "this report after the real 90-call "
            "development dry run."
        ),
        "",
        "## Free-access gate",
        "",
        (
            "- Required approved free models: "
            f"{model_count}"
        ),
        (
            "- Approved free models recorded: "
            f"{len(approved)}"
        ),
        (
            "- Calls per model including reserve: "
            f"{ceiling_per_model}"
        ),
        (
            "- Maximum paid expenditure allowed: "
            f"USD {hard_budget:.2f}"
        ),
        (
            "- Observed expenditure: "
            f"USD {observed_cost:.2f}"
        ),
        (
            "- Budget gate: "
            f"`{'PASS' if budget_pass else 'FAIL'}`"
        ),
        (
            f"- Execution gate: "
            f"`{execution_gate}`"
        ),
        "",
    ]

    if approved:
        lines.extend(
            [
                (
                    "| Model ID | Provider | Model | "
                    "Requests/day | Minimum days |"
                ),
                "|---|---|---|---:|---:|",
            ]
        )

        for model in approved:
            daily_limit = int(
                model["requests_per_day"]
            )

            minimum_days = math.ceil(
                ceiling_per_model
                / daily_limit
            )

            lines.append(
                f"| {model['model_id']} | "
                f"{model['provider']} | "
                f"{model['model_name']} | "
                f"{daily_limit} | "
                f"{minimum_days} |"
            )

        lines.append("")

    if model_problems:
        lines.append(
            "Recorded model-entry problems:"
        )
        lines.append("")

        lines.extend(
            f"- {problem}"
            for problem in model_problems
        )

        lines.append("")

    lines.extend(
        [
            "## Authorization decision",
            "",
            (
                "This Phase 2 smoke test does not "
                "authorize real API execution. Real "
                "execution remains blocked until "
                "three model entries are verified "
                "against current official free-tier "
                "documentation, evidence files are "
                "committed, all tests pass, and the "
                "90-call real dry run is reviewed."
            ),
            "",
        ]
    )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "SUCCESS: Free-quota projection "
        "report created."
    )
    print(
        f"Observed dry-run records: "
        f"{len(records)}"
    )
    print(
        f"Required future dry-run calls: "
        f"{dry_run_calls}"
    )
    print(f"Frozen core calls: {core_calls}")
    print(
        "Core reserve calls (25%): "
        f"{reserve_calls}"
    )
    print(
        f"Core authorization ceiling: "
        f"{core_ceiling}"
    )
    print(f"Extension cap: {extension_cap}")
    print(
        "Overall planned experiment ceiling: "
        f"{overall_ceiling}"
    )
    print(
        f"Hard paid budget: "
        f"USD {hard_budget:.2f}"
    )
    print(
        "Budget gate: "
        f"{'PASS' if budget_pass else 'FAIL'}"
    )
    print(
        f"Execution gate: {execution_gate}"
    )
    print(
        "Report: "
        + report_path
        .relative_to(PROJECT_ROOT)
        .as_posix()
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Project zero-cost API calls "
            "and free-tier quota needs."
        )
    )

    parser.add_argument(
        "--dry-run",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--quota-config",
        type=Path,
        default=Path(
            "config/free_quota.yaml"
        ),
    )

    parser.add_argument(
        "--report",
        type=Path,
        required=True,
    )

    arguments = parser.parse_args()

    try:
        create_projection(
            resolve_project_path(
                arguments.dry_run
            ),
            resolve_project_path(
                arguments.quota_config
            ),
            resolve_project_path(
                arguments.report
            ),
        )

    except (
        FileExistsError,
        FileNotFoundError,
        KeyError,
        ValueError,
    ) as error:
        print(f"FAIL: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())