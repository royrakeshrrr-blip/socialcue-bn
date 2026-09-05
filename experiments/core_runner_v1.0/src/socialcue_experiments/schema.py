from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


REGISTERS = ("TUI", "TUMI", "APNI")
SPLITS = ("DEVELOPMENT", "TEST")
VARIANTS = ("A", "B", "C")

REQUIRED_HEADERS = {
    "instance_id",
    "message_family_id",
    "variant",
    "romanized_message",
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
    "primary_register",
    "secondary_register",
    "acceptable_registers",
    "answerability",
    "gold_confidence",
    "reason_codes",
    "split",
    "dataset_version",
}


@dataclass(frozen=True, slots=True)
class DatasetRow:
    instance_id: str
    message_family_id: str
    variant: str
    romanized_message: str
    domain: str
    intent: str
    speaker_role: str
    recipient_role: str
    authority_relation: str
    relative_age: str
    familiarity: str
    setting: str
    changed_cue_from_A: str
    comparison_ids: str
    primary_register: str
    secondary_register: str
    acceptable_registers: str
    answerability: str
    gold_confidence: str
    reason_codes: str
    split: str
    dataset_version: str

    @classmethod
    def from_mapping(cls, row: dict[str, str]) -> "DatasetRow":
        return cls(**{field: (row.get(field) or "").strip() for field in cls.__dataclass_fields__})

    @property
    def acceptable_set(self) -> set[str]:
        return {value for value in self.acceptable_registers.split("|") if value}

    @property
    def comparison_id_list(self) -> list[str]:
        return [value for value in self.comparison_ids.split("|") if value]


def validate_rows(rows: list[DatasetRow]) -> list[str]:
    errors: list[str] = []
    ids = [row.instance_id for row in rows]
    id_set = set(ids)
    if len(ids) != len(id_set):
        errors.append("Duplicate instance_id values found.")

    for row in rows:
        prefix = row.instance_id or "<blank-id>"
        if row.variant not in VARIANTS:
            errors.append(f"{prefix}: invalid variant {row.variant!r}.")
        if row.primary_register not in REGISTERS:
            errors.append(f"{prefix}: invalid primary_register {row.primary_register!r}.")
        if row.secondary_register and row.secondary_register not in REGISTERS:
            errors.append(f"{prefix}: invalid secondary_register {row.secondary_register!r}.")
        if row.secondary_register == row.primary_register:
            errors.append(f"{prefix}: primary and secondary registers are identical.")
        if not row.acceptable_set or row.primary_register not in row.acceptable_set:
            errors.append(f"{prefix}: acceptable_registers does not contain the primary label.")
        if len(row.acceptable_set) > 2:
            errors.append(f"{prefix}: acceptable_registers contains more than two labels.")
        if row.answerability != "ANSWERABLE":
            errors.append(f"{prefix}: expected ANSWERABLE.")
        if row.gold_confidence not in {"HIGH", "MEDIUM", "LOW"}:
            errors.append(f"{prefix}: invalid gold_confidence {row.gold_confidence!r}.")
        if row.split not in SPLITS:
            errors.append(f"{prefix}: invalid split {row.split!r}.")
        if not row.reason_codes:
            errors.append(f"{prefix}: reason_codes is blank.")
        for comparison_id in row.comparison_id_list:
            if comparison_id not in id_set:
                errors.append(f"{prefix}: missing comparison ID {comparison_id}.")
            elif comparison_id.split("-")[0] != row.message_family_id:
                errors.append(f"{prefix}: comparison ID {comparison_id} crosses families.")

    families: dict[str, list[DatasetRow]] = {}
    for row in rows:
        families.setdefault(row.message_family_id, []).append(row)

    for family_id, family_rows in sorted(families.items()):
        variants = {row.variant for row in family_rows}
        if len(family_rows) != 3 or variants != set(VARIANTS):
            errors.append(f"{family_id}: expected exactly A/B/C.")
        if len({row.split for row in family_rows}) != 1:
            errors.append(f"{family_id}: family crosses splits.")
        if len({row.romanized_message for row in family_rows}) != 1:
            errors.append(f"{family_id}: message text changes within the family.")

    message_splits: dict[str, set[str]] = {}
    for row in rows:
        message_splits.setdefault(row.romanized_message.casefold(), set()).add(row.split)
    for message, splits in message_splits.items():
        if len(splits) > 1:
            errors.append(f"Exact message appears across splits: {message!r}.")

    return errors


def load_dataset(path: Path) -> list[DatasetRow]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        headers = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_HEADERS - headers)
        if missing:
            raise ValueError("Dataset is missing columns: " + ", ".join(missing))
        rows = [DatasetRow.from_mapping(row) for row in reader]

    if not rows:
        raise ValueError("Dataset contains no rows.")
    errors = validate_rows(rows)
    if errors:
        raise ValueError("Dataset validation failed: " + " | ".join(errors[:20]))
    return rows

