from __future__ import annotations

import csv
from pathlib import Path


OUTPUT_PATH = Path(
    "annotations/templates/"
    "annotation_response_template_v0.1.csv"
)

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


def main() -> int:
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
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

    print(
        "PASS: Created the header-only annotation "
        f"template with {len(FIELDNAMES)} columns."
    )

    print(
        "PASS: Family IDs, variants, changed cues, "
        "private predictions, and gold labels "
        "are excluded."
    )

    print(f"File: {OUTPUT_PATH.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())