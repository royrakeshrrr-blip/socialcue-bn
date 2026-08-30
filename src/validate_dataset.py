from __future__ import annotations

import argparse
import csv
from pathlib import Path

from pydantic import ValidationError

from src.data_schema import DatasetRow


def validate_rows(csv_path: Path) -> int:
    """Validate every CSV row."""

    if not csv_path.is_file():
        print(f"FAIL: File not found: {csv_path}")
        return 1

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
            print(
                "FAIL: CSV columns do not match "
                "the frozen schema."
            )

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
                print(
                    "Missing columns:",
                    ", ".join(missing),
                )

            if unexpected:
                print(
                    "Unexpected columns:",
                    ", ".join(unexpected),
                )

            if not missing and not unexpected:
                print(
                    "The columns are present but "
                    "are in the wrong order."
                )

            return 1

        rows = list(reader)

    if not rows:
        print("FAIL: The CSV contains no data rows.")
        return 1

    errors: list[str] = []

    for line_number, row in enumerate(
        rows,
        start=2,
    ):
        if None in row:
            errors.append(
                f"Line {line_number}: extra CSV values "
                "found; a field containing a comma may "
                "need quotation marks"
            )
            continue

        try:
            DatasetRow.model_validate(row)

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

    if errors:
        print(
            f"FAIL: Found {len(errors)} "
            "row-level validation error(s)."
        )

        for error in errors:
            print(f"- {error}")

        return 1

    print(
        f"PASS: All {len(rows)} rows satisfy "
        "the row-level schema."
    )
    print(f"File: {csv_path.as_posix()}")
    print(
        "Family-level counterfactual checks "
        "have not run yet."
    )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate SocialCue-BN CSV rows."
        )
    )

    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to a dataset CSV",
    )

    arguments = parser.parse_args()
    return validate_rows(arguments.csv_path)


if __name__ == "__main__":
    raise SystemExit(main())