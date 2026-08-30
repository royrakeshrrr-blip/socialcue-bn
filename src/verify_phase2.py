from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.config_loader import (
    PROJECT_ROOT,
    load_config,
)
from src.validate_dataset import (
    load_and_validate_rows,
    validate_families,
)


REQUIRED_ARTIFACTS = (
    "README.md",
    "requirements.txt",
    "requirements-lock.txt",
    ".gitignore",
    ".env.example",
    "config/experiment.yaml",
    "config/free_quota.yaml",
    "data/pilot/schema_example.csv",
    "docs/DATA_SCHEMA.md",
    "docs/milestones/PHASE2_QUOTA_SMOKE_TEST.md",
    "src/config_loader.py",
    "src/data_schema.py",
    "src/validate_dataset.py",
    "src/validate_extension_sample.py",
    "src/model_adapter.py",
    "src/run_dummy_experiment.py",
    "src/estimate_cost.py",
    "tests/test_configuration.py",
    "tests/test_dataset_validation.py",
    "tests/test_dummy_pipeline.py",
    (
        "results/raw/core/"
        "phase2-dummy-smoke-test.jsonl"
    ),
)

SAMPLE_PATH = (
    PROJECT_ROOT
    / "data"
    / "pilot"
    / "schema_example.csv"
)

RAW_OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "raw"
    / "core"
    / "phase2-dummy-smoke-test.jsonl"
)

QUOTA_REPORT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "milestones"
    / "PHASE2_QUOTA_SMOKE_TEST.md"
)

EXIT_REPORT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "milestones"
    / "PHASE2_EXIT_GATE.md"
)


def run_command(
    command: list[str],
) -> tuple[bool, str]:
    """Run one local verification command."""

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=300,
            check=False,
        )

    except subprocess.TimeoutExpired:
        return False, "Command exceeded 300 seconds"

    combined_output = "\n".join(
        part.strip()
        for part in (
            result.stdout,
            result.stderr,
        )
        if part.strip()
    )

    output_lines = [
        line.strip()
        for line in combined_output.splitlines()
        if line.strip()
    ]

    if output_lines:
        detail = output_lines[-1]
    else:
        detail = (
            f"Command returned code "
            f"{result.returncode}"
        )

    return result.returncode == 0, detail


def add_check(
    checks: list[tuple[str, bool, str]],
    name: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        (name, passed, detail)
    )


def verify_phase2(
    write_report: bool,
) -> int:
    checks: list[
        tuple[str, bool, str]
    ] = []

    missing_artifacts = [
        relative_path
        for relative_path in REQUIRED_ARTIFACTS
        if not (
            PROJECT_ROOT / relative_path
        ).is_file()
    ]

    add_check(
        checks,
        "Required artifacts",
        not missing_artifacts,
        (
            "All required files exist"
            if not missing_artifacts
            else "Missing: "
            + ", ".join(missing_artifacts)
        ),
    )

    try:
        readme_text = (
            PROJECT_ROOT / "README.md"
        ).read_text(encoding="utf-8")

        readme_passed = all(
            required_text in readme_text
            for required_text in (
                "requirements-lock.txt",
                "python -m src.verify_phase2",
                "USD 0",
            )
        )

        add_check(
            checks,
            "README reproduction commands",
            readme_passed,
            (
                "Reproduction commands documented"
                if readme_passed
                else "Required README commands missing"
            ),
        )

    except OSError as error:
        add_check(
            checks,
            "README reproduction commands",
            False,
            str(error),
        )

    try:
        gitignore_text = (
            PROJECT_ROOT / ".gitignore"
        ).read_text(encoding="utf-8")

        required_patterns = (
            ".venv/",
            ".env",
            "!.env.example",
            "data/annotations/identifiable/",
        )

        missing_patterns = [
            pattern
            for pattern in required_patterns
            if pattern not in gitignore_text
        ]

        add_check(
            checks,
            "Secret and cache exclusions",
            not missing_patterns,
            (
                "Required ignore rules present"
                if not missing_patterns
                else "Missing patterns: "
                + ", ".join(missing_patterns)
            ),
        )

    except OSError as error:
        add_check(
            checks,
            "Secret and cache exclusions",
            False,
            str(error),
        )

    try:
        example_text = (
            PROJECT_ROOT / ".env.example"
        ).read_text(encoding="utf-8")

        key_lines = [
            line.strip()
            for line in example_text.splitlines()
            if line.strip().startswith(
                "SOCIALCUE_API_KEY="
            )
        ]

        safe_template = (
            len(key_lines) == 1
            and key_lines[0]
            .partition("=")[2]
            .strip()
            == ""
        )

        add_check(
            checks,
            "Safe environment template",
            safe_template,
            (
                "API-key placeholder is blank"
                if safe_template
                else (
                    "The example API-key value "
                    "must remain blank"
                )
            ),
        )

    except OSError as error:
        add_check(
            checks,
            "Safe environment template",
            False,
            str(error),
        )

    try:
        lock_text = (
            PROJECT_ROOT
            / "requirements-lock.txt"
        ).read_text(encoding="utf-8-sig")

        locked_lines = [
            line.strip()
            for line in lock_text.splitlines()
            if line.strip()
            and not line.lstrip().startswith("#")
        ]

        lock_passed = (
            len(locked_lines) >= 10
            and all(
                "==" in line or " @ " in line
                for line in locked_lines
            )
        )

        add_check(
            checks,
            "Locked dependencies",
            lock_passed,
            (
                f"{len(locked_lines)} pinned entries"
                if lock_passed
                else (
                    "Lock file is empty or contains "
                    "unpinned entries"
                )
            ),
        )

    except OSError as error:
        add_check(
            checks,
            "Locked dependencies",
            False,
            str(error),
        )

    try:
        config, key_available = load_config()

        conditions = tuple(
            config["prompts"][
                "core_conditions"
            ]
        )

        config_passed = (
            config["runtime"]["mode"] == "dummy"
            and config["runtime"][
                "remote_api_only"
            ]
            is True
            and config["runtime"][
                "local_llm_allowed"
            ]
            is False
            and config["safety"][
                "hard_budget_usd"
            ]
            == 0.0
            and config["safety"][
                "paid_fallback_allowed"
            ]
            is False
            and conditions
            == (
                "P0_MESSAGE_ONLY",
                "P1_NATURAL_CONTEXT",
                "P2_STRUCTURED_CONTEXT",
            )
        )

        add_check(
            checks,
            "Experiment configuration",
            config_passed,
            (
                "Dummy mode, API-only, USD 0; "
                f"API key available={key_available}"
            ),
        )

    except (
        KeyError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        add_check(
            checks,
            "Experiment configuration",
            False,
            str(error),
        )

    rows, row_errors = (
        load_and_validate_rows(SAMPLE_PATH)
    )

    family_errors = (
        validate_families(rows)
        if not row_errors
        else []
    )

    dataset_passed = (
        len(rows) == 3
        and not row_errors
        and not family_errors
    )

    add_check(
        checks,
        "Dataset and counterfactual validation",
        dataset_passed,
        (
            "Three valid rows and one valid family"
            if dataset_passed
            else " | ".join(
                row_errors + family_errors
            )
        ),
    )

    try:
        records = [
            json.loads(line)
            for line in (
                RAW_OUTPUT_PATH.read_text(
                    encoding="utf-8"
                ).splitlines()
            )
            if line.strip()
        ]

        observed_conditions = {
            record["prompt_condition"]
            for record in records
        }

        raw_output_passed = (
            len(records) == 9
            and observed_conditions
            == {
                "P0_MESSAGE_ONLY",
                "P1_NATURAL_CONTEXT",
                "P2_STRUCTURED_CONTEXT",
            }
            and all(
                record["response"][
                    "uses_api"
                ]
                is False
                and record["response"][
                    "is_dummy"
                ]
                is True
                and record["response"][
                    "cost_usd"
                ]
                == 0.0
                for record in records
            )
        )

        add_check(
            checks,
            "Immutable dummy output",
            raw_output_passed,
            (
                "Nine zero-cost dummy records"
                if raw_output_passed
                else "Dummy output is incomplete or unsafe"
            ),
        )

    except (
        KeyError,
        json.JSONDecodeError,
        OSError,
    ) as error:
        add_check(
            checks,
            "Immutable dummy output",
            False,
            str(error),
        )

    try:
        quota_report = (
            QUOTA_REPORT_PATH.read_text(
                encoding="utf-8"
            )
        )

        quota_passed = (
            "Budget gate: `PASS`"
            in quota_report
            and (
                "BLOCKED_PENDING_"
                "FREE_QUOTA_VERIFICATION"
            )
            in quota_report
            and "5663" in quota_report
        )

        add_check(
            checks,
            "Zero-dollar quota gate",
            quota_passed,
            (
                "Budget passes; real API remains blocked"
                if quota_passed
                else "Quota report is incomplete"
            ),
        )

    except OSError as error:
        add_check(
            checks,
            "Zero-dollar quota gate",
            False,
            str(error),
        )

    pip_check_passed, pip_check_detail = (
        run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "check",
            ]
        )
    )

    add_check(
        checks,
        "Installed dependency health",
        pip_check_passed,
        pip_check_detail,
    )

    dry_install_passed, dry_install_detail = (
        run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--dry-run",
                "-r",
                "requirements-lock.txt",
            ]
        )
    )

    add_check(
        checks,
        "Locked-install dry run",
        dry_install_passed,
        dry_install_detail,
    )

    pytest_passed, pytest_detail = (
        run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
            ]
        )
    )

    add_check(
        checks,
        "Automated test suite",
        pytest_passed,
        pytest_detail,
    )

    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"

        print(
            f"[{status}] {name}: {detail}"
        )

    passed_count = sum(
        1
        for _, passed, _ in checks
        if passed
    )

    print()
    print(
        f"Summary: {passed_count}/"
        f"{len(checks)} checks passed."
    )

    all_passed = (
        passed_count == len(checks)
    )

    if not all_passed:
        print(
            "FAIL: Phase 2 exit gate "
            "has not passed."
        )
        return 1

    if write_report:
        generated = (
            datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

        report_lines = [
            "# Phase 2 Exit Gate",
            "",
            f"Generated UTC: {generated}",
            "",
            "Status: PASS",
            "",
            "## Verification results",
            "",
            "| Check | Status | Detail |",
            "|---|---|---|",
        ]

        for name, passed, detail in checks:
            safe_detail = (
                detail
                .replace("|", "\\|")
                .replace("\n", " ")
            )

            report_lines.append(
                f"| {name} | "
                f"{'PASS' if passed else 'FAIL'} | "
                f"{safe_detail} |"
            )

        report_lines.extend(
            [
                "",
                "## Gate decision",
                "",
                (
                    "The repository environment, "
                    "configuration, schema validation, "
                    "counterfactual checks, dummy runner, "
                    "zero-dollar quota protection, and "
                    "automated tests passed the Phase 2 "
                    "exit gate."
                ),
                "",
                (
                    "This does not authorize real API "
                    "execution. Real execution remains "
                    "blocked until three free models and "
                    "their current official quotas are "
                    "verified."
                ),
                "",
            ]
        )

        EXIT_REPORT_PATH.write_text(
            "\n".join(report_lines),
            encoding="utf-8",
        )

        print(
            "Report: "
            + EXIT_REPORT_PATH
            .relative_to(PROJECT_ROOT)
            .as_posix()
        )

    print(
        "SUCCESS: Phase 2 exit gate passed."
    )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the complete Phase 2 exit gate."
        )
    )

    parser.add_argument(
        "--write-report",
        action="store_true",
        help=(
            "Write the Phase 2 milestone report"
        ),
    )

    arguments = parser.parse_args()

    return verify_phase2(
        write_report=arguments.write_report
    )


if __name__ == "__main__":
    raise SystemExit(main())