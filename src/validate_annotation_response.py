from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path


FIELDNAMES = (
    "annotation_id",
    "annotator_code",
    "packet_order",
    "romanized_message",
    "domain",
    "intent",
    "speaker_role",
    "recipient_role",
    "authority_relation",
    "relative_age",
    "familiarity",
    "setting",
    "answerability",
    "primary_register",
    "secondary_register",
    "confidence",
    "reason_codes",
    "annotation_note",
    "annotation_timestamp",
    "guide_version",
)

PREFILLED_FIELDS = (
    "annotation_id",
    "annotator_code",
    "packet_order",
    "romanized_message",
    "domain",
    "intent",
    "speaker_role",
    "recipient_role",
    "authority_relation",
    "relative_age",
    "familiarity",
    "setting",
    "guide_version",
)

RESPONSE_FIELDS = (
    "answerability",
    "primary_register",
    "secondary_register",
    "confidence",
    "reason_codes",
    "annotation_note",
    "annotation_timestamp",
)

AUTHORITY_VALUES = {
    "LOWER",
    "EQUAL",
    "HIGHER",
    "UNKNOWN",
}

AGE_VALUES = {
    "YOUNGER",
    "SIMILAR",
    "OLDER",
    "UNKNOWN",
}

FAMILIARITY_VALUES = {
    "LOW",
    "MEDIUM",
    "HIGH",
}

SETTING_VALUES = {
    "INFORMAL",
    "SEMI_FORMAL",
    "FORMAL",
}

ANSWERABILITY_VALUES = {
    "ANSWERABLE",
    "UNDERSPECIFIED",
    "CONTRADICTORY",
    "CONTENTIOUS",
}

REGISTER_VALUES = {
    "TUI",
    "TUMI",
    "APNI",
}

CONFIDENCE_VALUES = {
    "HIGH",
    "MEDIUM",
    "LOW",
}

REASON_CODE_VALUES = {
    "AUTHORITY",
    "AGE",
    "FAMILIARITY",
    "SETTING",
    "KINSHIP",
    "EMOTIONAL_STANCE",
    "OTHER",
}

ANNOTATION_ID_PATTERN = re.compile(
    r"^[A-Z][0-9]{3}$"
)

ANNOTATOR_CODE_PATTERN = re.compile(
    r"^A[1-9][0-9]*$"
)

POSITIVE_INTEGER_PATTERN = re.compile(
    r"^[1-9][0-9]*$"
)


def timestamp_is_valid(value: str) -> bool:
    normalized = value.replace(
        "Z",
        "+00:00",
    )

    try:
        parsed = datetime.fromisoformat(
            normalized
        )
    except ValueError:
        return False

    return parsed.utcoffset() is not None


def validate_file(
    path: Path,
    mode: str,
) -> tuple[list[str], int]:
    errors: list[str] = []

    if not path.is_file():
        return [
            f"File does not exist: {path.as_posix()}"
        ], 0

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)
            actual_fields = tuple(
                reader.fieldnames or ()
            )
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as error:
        return [
            f"Could not read CSV: {error}"
        ], 0

    if actual_fields != FIELDNAMES:
        errors.append(
            "The CSV header does not exactly match "
            "the required 20-column schema."
        )

        return errors, len(rows)

    if mode == "template":
        if rows:
            errors.append(
                "Template mode requires a header-only "
                "CSV with no data rows."
            )

        return errors, len(rows)

    if not rows:
        errors.append(
            f"{mode.capitalize()} mode requires "
            "at least one data row."
        )

        return errors, 0

    annotation_ids: list[str] = []
    packet_orders: list[int] = []
    annotator_codes: set[str] = set()
    guide_versions: set[str] = set()

    for row_number, row in enumerate(
        rows,
        start=2,
    ):
        values = {
            field: row.get(field, "") or ""
            for field in FIELDNAMES
        }

        for field in PREFILLED_FIELDS:
            if not values[field].strip():
                errors.append(
                    f"Row {row_number}: "
                    f"{field} is required."
                )

        annotation_id = values[
            "annotation_id"
        ]

        if annotation_id:
            annotation_ids.append(
                annotation_id
            )

            if not ANNOTATION_ID_PATTERN.fullmatch(
                annotation_id
            ):
                errors.append(
                    f"Row {row_number}: annotation_id "
                    "must contain one capital letter "
                    "followed by three digits."
                )

        annotator_code = values[
            "annotator_code"
        ]

        if annotator_code:
            annotator_codes.add(
                annotator_code
            )

            if not ANNOTATOR_CODE_PATTERN.fullmatch(
                annotator_code
            ):
                errors.append(
                    f"Row {row_number}: annotator_code "
                    "must use a value such as A1 or A2."
                )

        order_text = values["packet_order"]

        if POSITIVE_INTEGER_PATTERN.fullmatch(
            order_text
        ):
            packet_orders.append(
                int(order_text)
            )
        elif order_text:
            errors.append(
                f"Row {row_number}: packet_order "
                "must be a positive integer."
            )

        guide_version = values[
            "guide_version"
        ]

        if guide_version:
            guide_versions.add(
                guide_version
            )

        categorical_checks = (
            (
                "authority_relation",
                AUTHORITY_VALUES,
            ),
            (
                "relative_age",
                AGE_VALUES,
            ),
            (
                "familiarity",
                FAMILIARITY_VALUES,
            ),
            (
                "setting",
                SETTING_VALUES,
            ),
        )

        for field, allowed_values in (
            categorical_checks
        ):
            value = values[field]

            if value and value not in allowed_values:
                errors.append(
                    f"Row {row_number}: illegal "
                    f"{field} value {value!r}."
                )

        for field in RESPONSE_FIELDS:
            value = values[field]

            if value != value.strip():
                errors.append(
                    f"Row {row_number}: {field} "
                    "contains leading or trailing "
                    "whitespace."
                )

        if mode == "packet":
            populated_fields = [
                field
                for field in RESPONSE_FIELDS
                if values[field]
            ]

            if populated_fields:
                errors.append(
                    f"Row {row_number}: blank packet "
                    "contains response values in "
                    + ", ".join(populated_fields)
                    + "."
                )

            continue

        answerability = values[
            "answerability"
        ]
        primary = values[
            "primary_register"
        ]
        secondary = values[
            "secondary_register"
        ]
        confidence = values["confidence"]
        reasons = values["reason_codes"]
        note = values["annotation_note"]
        timestamp = values[
            "annotation_timestamp"
        ]

        if answerability not in (
            ANSWERABILITY_VALUES
        ):
            errors.append(
                f"Row {row_number}: illegal or blank "
                "answerability value."
            )

        if confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"Row {row_number}: illegal or blank "
                "confidence value."
            )

        reason_parts: list[str] = []

        if not reasons:
            errors.append(
                f"Row {row_number}: at least one "
                "reason code is required."
            )
        else:
            reason_parts = reasons.split("|")
            unknown_reasons = sorted(
                set(reason_parts)
                - REASON_CODE_VALUES
            )

            if unknown_reasons:
                errors.append(
                    f"Row {row_number}: illegal reason "
                    "codes: "
                    + ", ".join(unknown_reasons)
                    + "."
                )

            if len(reason_parts) != len(
                set(reason_parts)
            ):
                errors.append(
                    f"Row {row_number}: duplicate "
                    "reason codes are not allowed."
                )

        if "\n" in note or "\r" in note:
            errors.append(
                f"Row {row_number}: annotation_note "
                "must remain on one line."
            )

        if "OTHER" in reason_parts and not note:
            errors.append(
                f"Row {row_number}: annotation_note "
                "is required when OTHER is selected."
            )

        if not timestamp:
            errors.append(
                f"Row {row_number}: "
                "annotation_timestamp is required."
            )
        elif not timestamp_is_valid(timestamp):
            errors.append(
                f"Row {row_number}: "
                "annotation_timestamp must be a "
                "timezone-aware ISO 8601 value."
            )

        if answerability == "ANSWERABLE":
            if primary not in REGISTER_VALUES:
                errors.append(
                    f"Row {row_number}: an answerable "
                    "item requires a legal primary "
                    "register."
                )

            if (
                secondary
                and secondary not in REGISTER_VALUES
            ):
                errors.append(
                    f"Row {row_number}: illegal "
                    "secondary register."
                )

            if (
                primary
                and secondary
                and primary == secondary
            ):
                errors.append(
                    f"Row {row_number}: primary and "
                    "secondary registers must differ."
                )

        elif answerability in {
            "UNDERSPECIFIED",
            "CONTRADICTORY",
            "CONTENTIOUS",
        }:
            if primary or secondary:
                errors.append(
                    f"Row {row_number}: non-answerable "
                    "items must have blank register "
                    "fields."
                )

            if confidence != "LOW":
                errors.append(
                    f"Row {row_number}: non-answerable "
                    "items require LOW confidence."
                )

            if not note:
                errors.append(
                    f"Row {row_number}: non-answerable "
                    "items require an annotation note."
                )

    if len(annotation_ids) != len(
        set(annotation_ids)
    ):
        errors.append(
            "annotation_id values must be unique "
            "within one packet."
        )

    if (
        len(packet_orders) == len(rows)
        and sorted(packet_orders)
        != list(range(1, len(rows) + 1))
    ):
        errors.append(
            "packet_order values must be unique and "
            "consecutive from 1 through the row count."
        )

    if len(annotator_codes) != 1:
        errors.append(
            "Each packet must contain exactly one "
            "annotator_code."
        )

    if len(guide_versions) != 1:
        errors.append(
            "Each packet must contain exactly one "
            "guide_version."
        )

    return errors, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a SocialCue-BN annotation "
            "template, blank packet, or completed "
            "response file."
        )
    )

    parser.add_argument(
        "csv_path",
        type=Path,
    )

    parser.add_argument(
        "--mode",
        required=True,
        choices=(
            "template",
            "packet",
            "completed",
        ),
    )

    arguments = parser.parse_args()

    errors, row_count = validate_file(
        arguments.csv_path,
        arguments.mode,
    )

    if errors:
        print(
            "FAIL: Annotation-response validation "
            "failed."
        )

        for error in errors:
            print(f"- {error}")

        return 1

    print(
        "PASS: Exact 20-column annotation "
        "schema found."
    )

    if arguments.mode == "template":
        print(
            "PASS: Template contains no data rows."
        )
    elif arguments.mode == "packet":
        print(
            f"PASS: Blank packet contains "
            f"{row_count} valid prefilled rows."
        )
    else:
        print(
            f"PASS: Completed response contains "
            f"{row_count} valid annotation rows."
        )

    print(
        "PASS: Annotation-response validation "
        "completed successfully."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())