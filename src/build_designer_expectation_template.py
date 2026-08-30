from __future__ import annotations

import csv
from pathlib import Path

from src.validate_dataset import (
    load_and_validate_rows,
    validate_families,
)


SOURCE_PATH = Path(
    "data/pilot/pilot_authoring_v0.1.csv"
)

OUTPUT_PATH = Path(
    "data/private/"
    "pilot_designer_expectation_template_v0.1.csv"
)

FIELDNAMES = (
    "instance_id",
    "message_family_id",
    "variant",
    "romanized_message",
    "source_register",
    "domain",
    "intent",
    "speaker_role",
    "recipient_role",
    "authority_relation",
    "relative_age",
    "familiarity",
    "setting",
    "changed_cue_from_A",
    "comparison_ids",
    "authoring_answerability",
    "provisional_primary_register",
    "provisional_secondary_register",
    "provisional_acceptable_registers",
    "provisional_answerability",
    "provisional_confidence",
    "provisional_reason_codes",
    "designer_notes",
    "expectation_source",
    "expectation_version",
)


def main() -> int:
    rows, row_errors = load_and_validate_rows(
        SOURCE_PATH
    )

    if row_errors:
        print(
            "FAIL: The pilot authoring dataset "
            "did not pass row validation."
        )

        for error in row_errors:
            print(f"- {error}")

        return 1

    family_errors = validate_families(rows)

    if family_errors:
        print(
            "FAIL: The pilot authoring dataset "
            "did not pass family validation."
        )

        for error in family_errors:
            print(f"- {error}")

        return 1

    populated_gold_rows = [
        row.instance_id
        for row in rows
        if (
            row.primary_register is not None
            or row.secondary_register is not None
            or row.acceptable_registers
            or row.gold_confidence is not None
            or row.reason_codes
        )
    ]

    if populated_gold_rows:
        print(
            "FAIL: Gold-label fields are already "
            "populated in the authoring dataset."
        )

        print(
            "Affected rows: "
            + ", ".join(populated_gold_rows)
        )

        return 1

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sorted_rows = sorted(
        rows,
        key=lambda row: (
            row.message_family_id,
            row.variant,
        ),
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()

        for row in sorted_rows:
            writer.writerow(
                {
                    "instance_id": row.instance_id,
                    "message_family_id": (
                        row.message_family_id
                    ),
                    "variant": row.variant,
                    "romanized_message": (
                        row.romanized_message
                    ),
                    "source_register": (
                        row.source_register
                    ),
                    "domain": row.domain,
                    "intent": row.intent,
                    "speaker_role": row.speaker_role,
                    "recipient_role": (
                        row.recipient_role
                    ),
                    "authority_relation": (
                        row.authority_relation
                    ),
                    "relative_age": row.relative_age,
                    "familiarity": row.familiarity,
                    "setting": row.setting,
                    "changed_cue_from_A": (
                        row.changed_cue_from_A
                    ),
                    "comparison_ids": "|".join(
                        row.comparison_ids
                    ),
                    "authoring_answerability": (
                        row.answerability
                    ),
                    "provisional_primary_register": "",
                    "provisional_secondary_register": "",
                    "provisional_acceptable_registers": "",
                    "provisional_answerability": "",
                    "provisional_confidence": "",
                    "provisional_reason_codes": "",
                    "designer_notes": "",
                    "expectation_source": "PENDING",
                    "expectation_version": (
                        "DESIGNER-EXPECTATION-DRAFT-v0.1"
                    ),
                }
            )

    print(
        "PASS: Created private designer-expectation "
        f"template for {len(sorted_rows)} rows."
    )

    print(
        "PASS: Source gold-label fields remain blank."
    )

    print(
        "IMPORTANT: Keep this file private and "
        "do not give it to annotators."
    )

    print(f"File: {OUTPUT_PATH.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())