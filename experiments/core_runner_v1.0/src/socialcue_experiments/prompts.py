from __future__ import annotations

import hashlib
from pathlib import Path

from .schema import DatasetRow


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = PACKAGE_ROOT / "prompts"

CONDITION_FILES = {
    "P0_MESSAGE_ONLY": "P0_MESSAGE_ONLY_v1.0.txt",
    "P1_NARRATIVE_CONTEXT": "P1_NARRATIVE_CONTEXT_v1.0.txt",
    "P2_STRUCTURED_CONTEXT": "P2_STRUCTURED_CONTEXT_v1.0.txt",
}


def load_system_prompt() -> str:
    return (PROMPT_DIR / "SYSTEM_v1.0.txt").read_text(encoding="utf-8").strip()


def narrative_context(row: DatasetRow) -> str:
    authority = {
        "HIGHER": "higher authority than the speaker",
        "EQUAL": "equal authority to the speaker",
        "LOWER": "lower authority than the speaker",
        "UNKNOWN": "unknown relative authority",
    }.get(row.authority_relation, row.authority_relation.lower())
    age = {
        "OLDER": "older than the speaker",
        "SIMILAR": "similar in age to the speaker",
        "YOUNGER": "younger than the speaker",
        "UNKNOWN": "of unknown relative age",
    }.get(row.relative_age, row.relative_age.lower())
    return (
        f"A {row.speaker_role.lower().replace('_', ' ')} is addressing a "
        f"{row.recipient_role.lower().replace('_', ' ')}. The recipient has {authority}, "
        f"is {age}, the familiarity level is {row.familiarity.lower()}, and the setting is "
        f"{row.setting.lower().replace('_', ' ')}."
    )


def render_prompt(row: DatasetRow, condition: str) -> tuple[str, str]:
    if condition not in CONDITION_FILES:
        raise ValueError(f"Unknown prompt condition: {condition}")
    template = (PROMPT_DIR / CONDITION_FILES[condition]).read_text(encoding="utf-8")
    replacements = {
        "romanized_message": row.romanized_message,
        "narrative_context": narrative_context(row),
        "speaker_role": row.speaker_role,
        "recipient_role": row.recipient_role,
        "authority_relation": row.authority_relation,
        "relative_age": row.relative_age,
        "familiarity": row.familiarity,
        "setting": row.setting,
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(f"[[{key}]]", value)
    if "[[" in rendered or "]]" in rendered:
        raise ValueError(f"Unresolved placeholder in {condition} for {row.instance_id}")
    return load_system_prompt(), rendered.strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

