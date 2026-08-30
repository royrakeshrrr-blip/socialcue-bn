from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from src.validate_dataset import (
    load_and_validate_rows,
    validate_families,
)


REQUIRED_ROW_COUNT = 90
REQUIRED_FAMILY_COUNT = 30

REQUIRED_LABEL_COUNTS = {
    "TUI": 30,
    "TUMI": 30,
    "APNI": 30,
}

REQUIRED_DOMAINS = {
    "ACADEMIC",
    "PROFESSIONAL",
    "FAMILY",
    "FRIENDSHIP",
    "SERVICE_PUBLIC",
    "ONLINE",
}

REQUIRED_CHANGED_CUES = {
    "AUTHORITY",
    "AGE",
    "FAMILIARITY",
    "SETTING",
}


def validate_extension_sample(
    csv_path: Path,
) -> int:
    """Check whether a sample is eligible for the extension."""

    rows, row_errors = load_and_validate_rows(
        csv_path
    )

    if row_errors:
        print(
            "FAIL: Extension sample has "
            "row-level errors."
        )

        for error in row_errors:
            print(f"- {error}")

        return 1

    family_errors = validate_families(rows)

    if family_errors:
        print(
            "FAIL: Extension sample has "
            "family-level errors."
        )

        for error in family_errors:
            print(f"- {error}")

        return 1

    errors: list[str] = []

    family_ids = {
        row.message_family_id
        for row in rows
    }

    if len(rows) != REQUIRED_ROW_COUNT:
        errors.append(
            f"Expected {REQUIRED_ROW_COUNT} rows; "
            f"found {len(rows)}."
        )

    if len(family_ids) != REQUIRED_FAMILY_COUNT:
        errors.append(
            f"Expected {REQUIRED_FAMILY_COUNT} "
            "complete families; "
            f"found {len(family_ids)}."
        )

    non_test_ids = [
        row.instance_id
        for row in rows
        if row.split != "TEST"
    ]

    if non_test_ids:
        errors.append(
            "Every extension instance must "
            "come from the TEST split."
        )

    missing_primary_ids = [
        row.instance_id
        for row in rows
        if row.primary_register is None
    ]

    if missing_primary_ids:
        errors.append(
            "Every extension instance must "
            "have a primary register."
        )

    label_counts = Counter(
        row.primary_register
        for row in rows
        if row.primary_register is not None
    )

    for label, required_count in (
        REQUIRED_LABEL_COUNTS.items()
    ):
        observed_count = label_counts.get(
            label,
            0,
        )

        if observed_count != required_count:
            errors.append(
                f"Expected {required_count} "
                f"{label} instances; "
                f"found {observed_count}."
            )

    if any(
        row.answerability != "ANSWERABLE"
        for row in rows
    ):
        errors.append(
            "All extension instances must "
            "be marked ANSWERABLE."
        )

    if any(
        row.human_revision_status == "REJECTED"
        for row in rows
    ):
        errors.append(
            "REJECTED rows cannot enter "
            "the extension sample."
        )

    observed_domains = {
        row.domain for row in rows
    }

    missing_domains = sorted(
        REQUIRED_DOMAINS - observed_domains
    )

    if missing_domains:
        errors.append(
            "Missing domain coverage: "
            + ", ".join(missing_domains)
        )

    observed_cues = {
        row.changed_cue_from_A
        for row in rows
        if row.variant in {"B", "C"}
    }

    missing_cues = sorted(
        REQUIRED_CHANGED_CUES - observed_cues
    )

    if missing_cues:
        errors.append(
            "Missing changed-cue coverage: "
            + ", ".join(missing_cues)
        )

    dataset_versions = {
        row.dataset_version for row in rows
    }

    if len(dataset_versions) != 1:
        errors.append(
            "All extension rows must use "
            "one frozen dataset version."
        )

    if "SCHEMA-EXAMPLE" in dataset_versions:
        errors.append(
            "The schema example cannot enter "
            "the extension sample."
        )

    if "F000" in family_ids:
        errors.append(
            "Reserved example family F000 "
            "cannot enter the extension sample."
        )

    print(
        f"Observed rows: {len(rows)} / "
        f"{REQUIRED_ROW_COUNT}"
    )

    print(
        f"Observed families: {len(family_ids)} / "
        f"{REQUIRED_FAMILY_COUNT}"
    )

    print(
        "Observed labels: "
        f"TUI={label_counts.get('TUI', 0)}, "
        f"TUMI={label_counts.get('TUMI', 0)}, "
        f"APNI={label_counts.get('APNI', 0)}"
    )

    if errors:
        print(
            f"FAIL: Found {len(errors)} "
            "extension-selection error(s)."
        )

        for error in errors:
            print(f"- {error}")

        return 1

    print(
        "PASS: Extension sample satisfies "
        "all frozen selection rules."
    )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the frozen 90-instance "
            "BanglaMate extension sample."
        )
    )

    parser.add_argument(
        "csv_path",
        type=Path,
        help=(
            "Path to the proposed "
            "extension-sample CSV"
        ),
    )

    arguments = parser.parse_args()

    return validate_extension_sample(
        arguments.csv_path
    )


if __name__ == "__main__":
    raise SystemExit(main())