from __future__ import annotations

import csv
import random
from pathlib import Path

from src.build_annotation_template import FIELDNAMES


SOURCE_PATH = Path(
    "data/pilot/pilot_authoring_v0.1.csv"
)

OUTPUT_DIR = Path(
    "data/private/annotations/pilot"
)

VISIBLE_FIELDS = (
    "romanized_message",
    "domain",
    "intent",
    "speaker_role",
    "recipient_role",
    "authority_relation",
    "relative_age",
    "familiarity",
    "setting",
)

RESPONSE_FIELDS = (
    "answerability",
    "primary_register",
    "secondary_register",
    "confidence",
    "reason_codes",
    "annotation_note",
)

PACKET_PATHS = {
    "A1": OUTPUT_DIR / "pilot_packet_A1_v0.1.csv",
    "A2": OUTPUT_DIR / "pilot_packet_A2_v0.1.csv",
}

ID_MAP_PATH = (
    OUTPUT_DIR / "pilot_annotation_id_map_v0.1.csv"
)

PACKET_SEEDS = {
    "A1": 20260901,
    "A2": 20260902,
}

ID_SEED = 20260903


def read_source() -> list[dict[str, str]]:
    with SOURCE_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        fieldnames = set(reader.fieldnames or [])
        rows = list(reader)

    required = {
        "instance_id",
        "message_family_id",
        "variant",
        *VISIBLE_FIELDS,
    }

    missing = sorted(required - fieldnames)

    if missing:
        raise ValueError(
            "Pilot dataset is missing fields: "
            + ", ".join(missing)
        )

    if len(rows) != 45:
        raise ValueError(
            f"Expected 45 pilot rows, found {len(rows)}."
        )

    instance_ids = [
        row["instance_id"] for row in rows
    ]

    if len(instance_ids) != len(set(instance_ids)):
        raise ValueError("Duplicate instance IDs found.")

    return rows


def validate_template() -> None:
    required = {
        "annotation_id",
        "annotator_code",
        "packet_order",
        *VISIBLE_FIELDS,
        *RESPONSE_FIELDS,
    }

    missing = sorted(required - set(FIELDNAMES))

    if missing:
        raise ValueError(
            "Annotation template is missing fields: "
            + ", ".join(missing)
        )

    forbidden = {
        "instance_id",
        "message_family_id",
        "variant",
        "changed_cue_from_A",
        "comparison_ids",
        "source_register",
        "provisional_primary_register",
        "primary_register_gold",
        "gold_confidence",
    }

    exposed = sorted(forbidden & set(FIELDNAMES))

    if exposed:
        raise ValueError(
            "Template exposes blinded fields: "
            + ", ".join(exposed)
        )


def create_annotation_ids(
    rows: list[dict[str, str]],
) -> dict[str, str]:
    shuffled = list(rows)
    random.Random(ID_SEED).shuffle(shuffled)

    return {
        row["instance_id"]: f"P{number:03d}"
        for number, row in enumerate(
            shuffled,
            start=1,
        )
    }


def create_packet(
    rows: list[dict[str, str]],
    annotation_ids: dict[str, str],
    annotator_code: str,
) -> list[dict[str, str]]:
    shuffled = list(rows)

    random.Random(
        PACKET_SEEDS[annotator_code]
    ).shuffle(shuffled)

    packet_rows: list[dict[str, str]] = []

    for order, source_row in enumerate(
        shuffled,
        start=1,
    ):
        packet_row = {
            field: ""
            for field in FIELDNAMES
        }

        packet_row.update(
            {
                "annotation_id": annotation_ids[
                    source_row["instance_id"]
                ],
                "annotator_code": annotator_code,
                "packet_order": str(order),
            }
        )

        for field in VISIBLE_FIELDS:
            packet_row[field] = source_row[field]

        if "guide_version" in packet_row:
            packet_row["guide_version"] = (
                "DRAFT_v0.1"
            )

        packet_rows.append(packet_row)

    return packet_rows


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = read_source()
    validate_template()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    annotation_ids = create_annotation_ids(rows)

    packets = {
        annotator_code: create_packet(
            rows,
            annotation_ids,
            annotator_code,
        )
        for annotator_code in ("A1", "A2")
    }

    a1_order = [
        row["annotation_id"]
        for row in packets["A1"]
    ]

    a2_order = [
        row["annotation_id"]
        for row in packets["A2"]
    ]

    if a1_order == a2_order:
        raise ValueError(
            "A1 and A2 packet orders are identical."
        )

    for annotator_code, path in PACKET_PATHS.items():
        write_csv(
            path,
            packets[annotator_code],
        )

    map_rows = []

    for row in rows:
        map_rows.append(
            {
                "annotation_id": annotation_ids[
                    row["instance_id"]
                ],
                "instance_id": row["instance_id"],
                "message_family_id": row[
                    "message_family_id"
                ],
                "variant": row["variant"],
            }
        )

    map_rows.sort(
        key=lambda row: row["annotation_id"]
    )

    with ID_MAP_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=(
                "annotation_id",
                "instance_id",
                "message_family_id",
                "variant",
            ),
        )

        writer.writeheader()
        writer.writerows(map_rows)

    print(
        "PASS: Created two independently randomized "
        "45-item pilot packets."
    )

    print(
        "PASS: Family IDs, variants, comparison "
        "fields, and label keys are hidden."
    )

    print(f"A1: {PACKET_PATHS['A1'].as_posix()}")
    print(f"A2: {PACKET_PATHS['A2'].as_posix()}")
    print(
        "Private map: "
        f"{ID_MAP_PATH.as_posix()}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())