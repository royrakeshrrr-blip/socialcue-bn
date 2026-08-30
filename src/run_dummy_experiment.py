from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config_loader import (
    CONFIG_PATH,
    PROJECT_ROOT,
    load_config,
)
from src.data_schema import DatasetRow
from src.model_adapter import (
    DummyModelAdapter,
    ModelRequest,
)
from src.validate_dataset import (
    load_and_validate_rows,
    validate_families,
)


CORE_CONDITIONS = (
    "P0_MESSAGE_ONLY",
    "P1_NATURAL_CONTEXT",
    "P2_STRUCTURED_CONTEXT",
)

RUN_ID_PATTERN = re.compile(
    r"[a-z0-9][a-z0-9_-]{2,63}"
)


def resolve_project_path(
    path_value: str | Path,
) -> Path:
    path = Path(path_value)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(65536),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def build_prompt(
    row: DatasetRow,
    condition: str,
) -> str:
    """Build a draft smoke-test prompt without gold labels."""

    output_rule = (
        'Return JSON only: '
        '{"label": "TUI or TUMI or APNI"}.'
    )

    if condition == "P0_MESSAGE_ONLY":
        return "\n".join(
            [
                (
                    "Select the socially appropriate "
                    "Bangla address register."
                ),
                (
                    f"Message: "
                    f"{row.romanized_message}"
                ),
                output_rule,
            ]
        )

    if condition == "P1_NATURAL_CONTEXT":
        context_sentence = (
            f"The speaker role is "
            f"{row.speaker_role.lower()} and the "
            f"recipient role is "
            f"{row.recipient_role.lower()}. "
            f"The recipient's authority is "
            f"{row.authority_relation.lower()} "
            f"relative to the speaker, the "
            f"recipient's age is "
            f"{row.relative_age.lower()}, "
            f"familiarity is "
            f"{row.familiarity.lower()}, and "
            f"the setting is "
            f"{row.setting.lower().replace('_', ' ')}."
        )

        return "\n".join(
            [
                (
                    "Select the socially appropriate "
                    "Bangla address register."
                ),
                context_sentence,
                (
                    f"Message: "
                    f"{row.romanized_message}"
                ),
                output_rule,
            ]
        )

    if condition == "P2_STRUCTURED_CONTEXT":
        return "\n".join(
            [
                (
                    "TASK: Select the socially "
                    "appropriate Bangla address register."
                ),
                (
                    f"MESSAGE: "
                    f"{row.romanized_message}"
                ),
                "CONTEXT:",
                (
                    f"speaker_role: "
                    f"{row.speaker_role}"
                ),
                (
                    f"recipient_role: "
                    f"{row.recipient_role}"
                ),
                (
                    f"authority_relation: "
                    f"{row.authority_relation}"
                ),
                (
                    f"relative_age: "
                    f"{row.relative_age}"
                ),
                (
                    f"familiarity: "
                    f"{row.familiarity}"
                ),
                f"setting: {row.setting}",
                output_rule,
            ]
        )

    raise ValueError(
        f"Unknown prompt condition: {condition}"
    )


def input_snapshot(
    row: DatasetRow,
) -> dict[str, Any]:
    """Save input fields without including gold labels."""

    return {
        "instance_id": row.instance_id,
        "message_family_id": (
            row.message_family_id
        ),
        "variant": row.variant,
        "romanized_message": (
            row.romanized_message
        ),
        "domain": row.domain,
        "intent": row.intent,
        "speaker_role": row.speaker_role,
        "recipient_role": row.recipient_role,
        "authority_relation": (
            row.authority_relation
        ),
        "relative_age": row.relative_age,
        "familiarity": row.familiarity,
        "setting": row.setting,
        "changed_cue_from_A": (
            row.changed_cue_from_A
        ),
    }


def run_dummy_experiment(
    dataset_value: Path,
    run_id: str,
) -> Path:
    """Run all three conditions using the dummy adapter."""

    if RUN_ID_PATTERN.fullmatch(run_id) is None:
        raise ValueError(
            "run_id must use 3-64 lowercase "
            "letters, numbers, hyphens, "
            "or underscores"
        )

    config, _ = load_config()

    if config["runtime"]["mode"] != "dummy":
        raise ValueError(
            "runtime.mode must be dummy "
            "for this smoke test"
        )

    if config["model"]["adapter"] != "dummy":
        raise ValueError(
            "model.adapter must be dummy "
            "for this smoke test"
        )

    if (
        float(
            config["safety"]["hard_budget_usd"]
        )
        != 0.0
    ):
        raise ValueError(
            "hard_budget_usd must remain 0"
        )

    conditions = tuple(
        config["prompts"].get(
            "core_conditions",
            [],
        )
    )

    if conditions != CORE_CONDITIONS:
        raise ValueError(
            "core_conditions do not match "
            "the expected three conditions"
        )

    dataset_path = resolve_project_path(
        dataset_value
    )

    rows, row_errors = load_and_validate_rows(
        dataset_path
    )

    if row_errors:
        raise ValueError(
            "Dataset row validation failed: "
            + " | ".join(row_errors)
        )

    family_errors = validate_families(rows)

    if family_errors:
        raise ValueError(
            "Dataset family validation failed: "
            + " | ".join(family_errors)
        )

    output_directory = resolve_project_path(
        config["paths"]["core_raw_results"]
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory / f"{run_id}.jsonl"
    )

    if output_path.exists():
        raise FileExistsError(
            "Raw output already exists and "
            "will not be overwritten: "
            f"{output_path}"
        )

    adapter = DummyModelAdapter(
        fixed_label="TUMI"
    )

    run_timestamp = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    dataset_hash = sha256_file(dataset_path)
    config_hash = sha256_file(CONFIG_PATH)

    records: list[dict[str, Any]] = []

    for row in rows:
        for condition in conditions:
            prompt = build_prompt(
                row,
                condition,
            )

            request_id = (
                f"{run_id}::{row.instance_id}"
                f"::{condition}"
            )

            request = ModelRequest(
                request_id=request_id,
                prompt=prompt,
                temperature=float(
                    config["generation"][
                        "temperature"
                    ]
                ),
                max_output_tokens=int(
                    config["generation"][
                        "max_output_tokens"
                    ]
                ),
                seed=int(
                    config["generation"]["seed"]
                ),
            )

            response = adapter.generate(request)

            if (
                response.uses_api
                or response.cost_usd != 0.0
            ):
                raise RuntimeError(
                    "Dummy response violated "
                    "the zero-cost safety rule"
                )

            record = {
                "raw_result_schema": "0.1-DRAFT",
                "run_id": run_id,
                "record_index": len(records) + 1,
                "timestamp_utc": run_timestamp,
                "dataset_path": (
                    dataset_path
                    .relative_to(PROJECT_ROOT)
                    .as_posix()
                ),
                "dataset_sha256": dataset_hash,
                "config_sha256": config_hash,
                "prompt_condition": condition,
                "prompt_version": (
                    config["prompts"][
                        "core_version"
                    ]
                ),
                "prompt_text": prompt,
                "prompt_sha256": (
                    sha256_text(prompt)
                ),
                "input": input_snapshot(row),
                "request_parameters": {
                    "temperature": (
                        request.temperature
                    ),
                    "max_output_tokens": (
                        request.max_output_tokens
                    ),
                    "seed": request.seed,
                    "retry_count": int(
                        config["generation"][
                            "retry_count"
                        ]
                    ),
                },
                "response": response.to_dict(),
            }

            records.append(record)

    expected_count = (
        len(rows) * len(conditions)
    )

    if len(records) != expected_count:
        raise RuntimeError(
            "Generated record count is incorrect"
        )

    total_cost = sum(
        float(
            record["response"]["cost_usd"]
        )
        for record in records
    )

    if total_cost > float(
        config["safety"]["hard_budget_usd"]
    ):
        raise RuntimeError(
            "Run exceeded the hard budget"
        )

    with output_path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            file.write("\n")

    api_calls = sum(
        1
        for record in records
        if record["response"]["uses_api"]
    )

    print(
        "SUCCESS: Dummy experiment completed."
    )
    print(f"Dataset rows: {len(rows)}")
    print(
        f"Prompt conditions: {len(conditions)}"
    )
    print(f"Raw records: {len(records)}")
    print(f"API calls: {api_calls}")
    print(f"Total cost: USD {total_cost:.2f}")
    print(
        "Output: "
        + output_path
        .relative_to(PROJECT_ROOT)
        .as_posix()
    )

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the zero-cost dummy "
            "core experiment."
        )
    )

    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--run-id",
        required=True,
    )

    arguments = parser.parse_args()

    try:
        run_dummy_experiment(
            arguments.dataset,
            arguments.run_id,
        )

    except (
        FileExistsError,
        FileNotFoundError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"FAIL: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())