from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from pydantic import ValidationError

from src.data_schema import DatasetRow


CONTEXT_FIELDS = (
    "authority_relation",
    "relative_age",
    "familiarity",
    "setting",
)

CUE_TO_FIELD = {
    "AUTHORITY": "authority_relation",
    "AGE": "relative_age",
    "FAMILIARITY": "familiarity",
    "SETTING": "setting",
}

FAMILY_CONSTANT_FIELDS = (
    "romanized_message",
    "source_register",
    "domain",
    "intent",
    "speaker_role",
    "recipient_role",
    "english_token_ratio",
    "code_mix_level",
    "spelling_noise_level",
    "authoring_source",
    "split",
    "dataset_version",
)


def load_and_validate_rows(
    csv_path: Path,
) -> tuple[list[DatasetRow], list[str]]:
    """Load the CSV and return validated rows and errors."""

    if not csv_path.is_file():
        return [], [f"File not found: {csv_path}"]

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        expected_columns = list(
            DatasetRow.model_fields
        )
        actual_columns = reader.fieldnames or []

        if actual_columns != expected_columns:
            errors = [
                "CSV columns do not match "
                "the frozen schema."
            ]

            missing = [
                column
                for column in expected_columns
                if column not in actual_columns
            ]

            unexpected = [
                column
                for column in actual_columns
                if column not in expected_columns
            ]

            if missing:
                errors.append(
                    "Missing columns: "
                    + ", ".join(missing)
                )

            if unexpected:
                errors.append(
                    "Unexpected columns: "
                    + ", ".join(unexpected)
                )

            if not missing and not unexpected:
                errors.append(
                    "The columns are present but "
                    "are in the wrong order."
                )

            return [], errors

        raw_rows = list(reader)

    if not raw_rows:
        return [], [
            "The CSV contains no data rows."
        ]

    validated_rows: list[DatasetRow] = []
    errors: list[str] = []

    for line_number, raw_row in enumerate(
        raw_rows,
        start=2,
    ):
        if None in raw_row:
            errors.append(
                f"Line {line_number}: extra CSV "
                "values found; a field containing "
                "a comma may need quotation marks"
            )
            continue

        try:
            validated_rows.append(
                DatasetRow.model_validate(raw_row)
            )

        except ValidationError as error:
            for item in error.errors(
                include_url=False
            ):
                location = ".".join(
                    str(part)
                    for part in item["loc"]
                )

                errors.append(
                    f"Line {line_number}, "
                    f"{location}: {item['msg']}"
                )

    return validated_rows, errors


def validate_families(
    rows: list[DatasetRow],
) -> list[str]:
    """Validate families and controlled comparisons."""

    errors: list[str] = []

    id_counts = Counter(
        row.instance_id for row in rows
    )

    for instance_id, count in sorted(
        id_counts.items()
    ):
        if count > 1:
            errors.append(
                f"Duplicate instance_id "
                f"{instance_id} appears "
                f"{count} times."
            )

    known_ids = set(id_counts)

    for row in rows:
        for comparison_id in row.comparison_ids:
            if comparison_id not in known_ids:
                errors.append(
                    f"{row.instance_id} references "
                    f"missing comparison "
                    f"{comparison_id}."
                )

    families: dict[
        str,
        list[DatasetRow],
    ] = defaultdict(list)

    for row in rows:
        families[row.message_family_id].append(
            row
        )

    for family_id, family_rows in sorted(
        families.items()
    ):
        if len(family_rows) != 3:
            errors.append(
                f"{family_id} must contain "
                f"exactly 3 rows; found "
                f"{len(family_rows)}."
            )
            continue

        variant_counts = Counter(
            row.variant for row in family_rows
        )

        expected_variants = {"A", "B", "C"}

        if set(variant_counts) != expected_variants:
            found = ", ".join(
                sorted(variant_counts)
            )

            errors.append(
                f"{family_id} must contain "
                f"variants A, B, and C; "
                f"found: {found}."
            )
            continue

        duplicate_variants = [
            variant
            for variant, count
            in variant_counts.items()
            if count > 1
        ]

        if duplicate_variants:
            errors.append(
                f"{family_id} contains duplicate "
                "variant(s): "
                + ", ".join(
                    sorted(duplicate_variants)
                )
            )
            continue

        by_variant = {
            row.variant: row
            for row in family_rows
        }

        baseline = by_variant["A"]

        for field_name in FAMILY_CONSTANT_FIELDS:
            values = {
                getattr(row, field_name)
                for row in family_rows
            }

            if len(values) != 1:
                errors.append(
                    f"{family_id}: {field_name} "
                    "must be identical across "
                    "A, B, and C."
                )

        for variant in ("B", "C"):
            comparison = by_variant[variant]

            changed_fields = [
                field_name
                for field_name in CONTEXT_FIELDS
                if getattr(
                    baseline,
                    field_name,
                )
                != getattr(
                    comparison,
                    field_name,
                )
            ]

            declared_cue = (
                comparison.changed_cue_from_A
            )

            expected_field = CUE_TO_FIELD.get(
                declared_cue
            )

            if changed_fields != [expected_field]:
                if changed_fields:
                    changed_text = ", ".join(
                        changed_fields
                    )
                else:
                    changed_text = "NONE"

                errors.append(
                    f"{comparison.instance_id}: "
                    f"declares {declared_cue}, "
                    "but actual changed field(s): "
                    f"{changed_text}."
                )

        if (
            by_variant["B"].changed_cue_from_A
            == by_variant["C"].changed_cue_from_A
        ):
            errors.append(
                f"{family_id}: B and C must "
                "change two different cues from A."
            )

    return errors


def validate_dataset(
    csv_path: Path,
) -> int:
    """Run row-level and family-level validation."""

    rows, row_errors = (
        load_and_validate_rows(csv_path)
    )

    if row_errors:
        print(
            f"FAIL: Found {len(row_errors)} "
            "row-level validation error(s)."
        )

        for error in row_errors:
            print(f"- {error}")

        return 1

    print(
        f"PASS: All {len(rows)} rows satisfy "
        "the row-level schema."
    )

    family_errors = validate_families(rows)

    if family_errors:
        print(
            f"FAIL: Found {len(family_errors)} "
            "family-level validation error(s)."
        )

        for error in family_errors:
            print(f"- {error}")

        return 1

    family_count = len({
        row.message_family_id
        for row in rows
    })

    family_word = (
        "family"
        if family_count == 1
        else "families"
    )

    print(
        "PASS: Counterfactual validation "
        f"passed for {family_count} "
        f"{family_word}."
    )

    print(f"File: {csv_path.as_posix()}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate SocialCue-BN rows and "
            "counterfactual families."
        )
    )

    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to a dataset CSV",
    )

    arguments = parser.parse_args()

    return validate_dataset(
        arguments.csv_path
    )


if __name__ == "__main__":
    raise SystemExit(main())