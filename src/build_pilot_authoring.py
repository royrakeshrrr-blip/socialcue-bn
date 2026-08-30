from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

from pydantic import ValidationError

from src.data_schema import DatasetRow
from src.validate_dataset import validate_families


OUTPUT_PATH = Path(
    "data/pilot/pilot_authoring_v0.1.csv"
)

DATASET_VERSION = "PILOT-AUTHORING-V0.1"

CUE_CHANGE = {
    "AUTHORITY": (
        "authority_relation",
        "HIGHER",
    ),
    "AGE": (
        "relative_age",
        "OLDER",
    ),
    "FAMILIARITY": (
        "familiarity",
        "LOW",
    ),
    "SETTING": (
        "setting",
        "FORMAL",
    ),
}

EXPECTED_CUE_COUNTS = Counter({
    "AUTHORITY": 8,
    "AGE": 8,
    "FAMILIARITY": 7,
    "SETTING": 7,
})


def family(
    *,
    message: str,
    domain: str,
    intent: str,
    speaker_role: str,
    recipient_role: str,
    familiarity: str,
    setting: str,
    b_cue: str,
    c_cue: str,
    english_words: tuple[str, ...] = (),
    revision_status: str = "REVIEWED",
) -> dict[str, object]:
    return {
        "message": message,
        "domain": domain,
        "intent": intent,
        "speaker_role": speaker_role,
        "recipient_role": recipient_role,
        "source_register": "UNCLEAR",
        "english_words": english_words,
        "revision_status": revision_status,
        "base": {
            "authority_relation": "EQUAL",
            "relative_age": "SIMILAR",
            "familiarity": familiarity,
            "setting": setting,
        },
        "b_cue": b_cue,
        "c_cue": c_cue,
    }


FAMILIES = {
    "F001": family(
        message=(
            "Kal project niye ekta meeting "
            "kora jabe?"
        ),
        domain="ACADEMIC",
        intent="REQUEST",
        speaker_role="UNIVERSITY_PROJECT_MEMBER",
        recipient_role="UNIVERSITY_PROJECT_MEMBER",
        familiarity="MEDIUM",
        setting="SEMI_FORMAL",
        b_cue="AUTHORITY",
        c_cue="AGE",
        english_words=("project", "meeting"),
    ),
    "F002": family(
        message=(
            "Assignment er deadline niye "
            "ektu kotha chilo."
        ),
        domain="ACADEMIC",
        intent="REQUEST",
        speaker_role="STUDENT",
        recipient_role="ACADEMIC_CONTACT",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="FAMILIARITY",
        c_cue="SETTING",
        english_words=("assignment", "deadline"),
    ),
    "F003": family(
        message=(
            "Report ta niye ektu motamot "
            "dorkar chilo."
        ),
        domain="ACADEMIC",
        intent="REQUEST",
        speaker_role="STUDENT_WRITER",
        recipient_role="ACADEMIC_REVIEWER",
        familiarity="MEDIUM",
        setting="INFORMAL",
        b_cue="AUTHORITY",
        c_cue="SETTING",
        english_words=("report",),
        revision_status="REWRITTEN",
    ),
    "F004": family(
        message=(
            "Client er file ta ajker "
            "moddhe dorkar."
        ),
        domain="PROFESSIONAL",
        intent="REQUEST",
        speaker_role="WORK_TEAM_MEMBER",
        recipient_role="WORK_TEAM_MEMBER",
        familiarity="HIGH",
        setting="SEMI_FORMAL",
        b_cue="AUTHORITY",
        c_cue="FAMILIARITY",
        english_words=("client", "file"),
    ),
    "F005": family(
        message=(
            "Agamikaler shift er shomoy ta "
            "confirm kora dorkar."
        ),
        domain="PROFESSIONAL",
        intent="QUESTION",
        speaker_role="STAFF_MEMBER",
        recipient_role="STAFF_MEMBER",
        familiarity="MEDIUM",
        setting="INFORMAL",
        b_cue="AGE",
        c_cue="SETTING",
        english_words=("shift", "confirm"),
        revision_status="REWRITTEN",
    ),
    "F006": family(
        message=(
            "Ei prostab ta onumodon "
            "kora dorkar."
        ),
        domain="PROFESSIONAL",
        intent="REQUEST",
        speaker_role="PROPOSAL_AUTHOR",
        recipient_role="PROPOSAL_REVIEWER",
        familiarity="MEDIUM",
        setting="SEMI_FORMAL",
        b_cue="AUTHORITY",
        c_cue="AGE",
        revision_status="REWRITTEN",
    ),
    "F007": family(
        message=(
            "Bari pouchhanor por ekbar "
            "janale bhalo hoy."
        ),
        domain="FAMILY",
        intent="REMINDER",
        speaker_role="FAMILY_MEMBER",
        recipient_role="FAMILY_MEMBER",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="AGE",
        c_cue="FAMILIARITY",
        revision_status="REWRITTEN",
    ),
    "F008": family(
        message=(
            "Ghorer kaj e ektu shahajjo "
            "dorkar."
        ),
        domain="FAMILY",
        intent="REQUEST",
        speaker_role="FAMILY_MEMBER",
        recipient_role="FAMILY_MEMBER",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="AUTHORITY",
        c_cue="FAMILIARITY",
    ),
    "F009": family(
        message="Oshudh ta rate khete hobe.",
        domain="FAMILY",
        intent="REMINDER",
        speaker_role="FAMILY_MEMBER",
        recipient_role="FAMILY_MEMBER",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="AGE",
        c_cue="SETTING",
    ),
    "F010": family(
        message=(
            "Kal campus e dekha kora jabe?"
        ),
        domain="FRIENDSHIP",
        intent="INVITATION",
        speaker_role="UNIVERSITY_PEER",
        recipient_role="UNIVERSITY_PEER",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="FAMILIARITY",
        c_cue="SETTING",
        english_words=("campus",),
        revision_status="REWRITTEN",
    ),
    "F011": family(
        message=(
            "Ekta chhoto shahajjo dorkar "
            "chilo."
        ),
        domain="FRIENDSHIP",
        intent="REQUEST",
        speaker_role="FRIEND",
        recipient_role="FRIEND",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="AUTHORITY",
        c_cue="AGE",
    ),
    "F012": family(
        message=(
            "Ei thikanay jawar rasta ta "
            "jante chachchilam."
        ),
        domain="SERVICE_PUBLIC",
        intent="QUESTION",
        speaker_role="PERSON_SEEKING_DIRECTIONS",
        recipient_role="PUBLIC_CONTACT",
        familiarity="LOW",
        setting="INFORMAL",
        b_cue="AUTHORITY",
        c_cue="SETTING",
        revision_status="REWRITTEN",
    ),
    "F013": family(
        message=(
            "Appointment er shomoy ta "
            "confirm kora dorkar."
        ),
        domain="SERVICE_PUBLIC",
        intent="FOLLOW_UP",
        speaker_role="SERVICE_USER",
        recipient_role="SERVICE_CONTACT",
        familiarity="HIGH",
        setting="SEMI_FORMAL",
        b_cue="AGE",
        c_cue="FAMILIARITY",
        english_words=("appointment", "confirm"),
    ),
    "F014": family(
        message=(
            "Group e post korar niyom ta "
            "ektu clear kora jabe?"
        ),
        domain="ONLINE",
        intent="QUESTION",
        speaker_role="ONLINE_GROUP_MEMBER",
        recipient_role="ONLINE_GROUP_MEMBER",
        familiarity="HIGH",
        setting="INFORMAL",
        b_cue="AUTHORITY",
        c_cue="FAMILIARITY",
        english_words=("group", "post", "clear"),
    ),
    "F015": family(
        message=(
            "Ei tothyer source ta share "
            "kora jabe?"
        ),
        domain="ONLINE",
        intent="REQUEST",
        speaker_role="ONLINE_COMMUNITY_MEMBER",
        recipient_role="ONLINE_COMMUNITY_MEMBER",
        familiarity="MEDIUM",
        setting="INFORMAL",
        b_cue="AGE",
        c_cue="SETTING",
        english_words=("source", "share"),
    ),
}


def calculate_code_mix(
    message: str,
    english_words: tuple[str, ...],
) -> tuple[float, str]:
    tokens = [
        token.casefold()
        for token in re.findall(
            r"[A-Za-z]+",
            message,
        )
    ]

    if not tokens:
        raise ValueError(
            "Message contains no countable tokens."
        )

    english_set = {
        word.casefold()
        for word in english_words
    }

    missing_words = (
        english_set - set(tokens)
    )

    if missing_words:
        raise ValueError(
            "English-token list contains words "
            "that are not in the message: "
            + ", ".join(sorted(missing_words))
        )

    english_count = sum(
        token in english_set
        for token in tokens
    )

    ratio = round(
        english_count / len(tokens),
        3,
    )

    if ratio > 0.30:
        raise ValueError(
            f"English-token ratio {ratio:.3f} "
            "exceeds the 0.30 limit."
        )

    if ratio == 0.0:
        level = "NONE"
    elif ratio <= 0.15:
        level = "LIGHT"
    else:
        level = "MODERATE"

    return ratio, level


def apply_cue_change(
    baseline: dict[str, str],
    cue: str,
) -> dict[str, str]:
    field_name, new_value = CUE_CHANGE[cue]

    changed = baseline.copy()
    changed[field_name] = new_value

    return changed


def build_rows() -> tuple[
    list[dict[str, str]],
    list[DatasetRow],
]:
    raw_rows: list[dict[str, str]] = []
    validated_rows: list[DatasetRow] = []

    for family_id, metadata in FAMILIES.items():
        message = str(metadata["message"])

        ratio, mix_level = calculate_code_mix(
            message,
            tuple(metadata["english_words"]),
        )

        baseline = dict(metadata["base"])
        b_cue = str(metadata["b_cue"])
        c_cue = str(metadata["c_cue"])

        if b_cue == c_cue:
            raise ValueError(
                f"{family_id}: B and C cues "
                "must be different."
            )

        variant_specs = [
            (
                "A",
                "NONE",
                baseline,
            ),
            (
                "B",
                b_cue,
                apply_cue_change(
                    baseline,
                    b_cue,
                ),
            ),
            (
                "C",
                c_cue,
                apply_cue_change(
                    baseline,
                    c_cue,
                ),
            ),
        ]

        for variant, changed_cue, context in (
            variant_specs
        ):
            instance_id = (
                f"{family_id}-{variant}"
            )

            if variant == "A":
                comparison_ids = (
                    f"{family_id}-B|"
                    f"{family_id}-C"
                )
            else:
                comparison_ids = (
                    f"{family_id}-A"
                )

            row = {
                "instance_id": instance_id,
                "message_family_id": family_id,
                "variant": variant,
                "romanized_message": message,
                "source_register": str(
                    metadata["source_register"]
                ),
                "domain": str(metadata["domain"]),
                "intent": str(metadata["intent"]),
                "speaker_role": str(
                    metadata["speaker_role"]
                ),
                "recipient_role": str(
                    metadata["recipient_role"]
                ),
                "authority_relation": str(
                    context["authority_relation"]
                ),
                "relative_age": str(
                    context["relative_age"]
                ),
                "familiarity": str(
                    context["familiarity"]
                ),
                "setting": str(
                    context["setting"]
                ),
                "changed_cue_from_A": (
                    changed_cue
                ),
                "comparison_ids": comparison_ids,
                "primary_register": "",
                "secondary_register": "",
                "acceptable_registers": "",
                "answerability": "ANSWERABLE",
                "gold_confidence": "",
                "reason_codes": "",
                "english_token_ratio": (
                    f"{ratio:.3f}"
                ),
                "code_mix_level": mix_level,
                "spelling_noise_level": "NONE",
                "authoring_source": (
                    "AI_CANDIDATE_REVISED"
                ),
                "human_revision_status": str(
                    metadata["revision_status"]
                ),
                "split": "DEVELOPMENT",
                "dataset_version": (
                    DATASET_VERSION
                ),
            }

            try:
                validated = (
                    DatasetRow.model_validate(row)
                )
            except ValidationError as error:
                print(
                    f"FAIL: {instance_id} did "
                    "not satisfy the schema."
                )
                print(error)
                raise

            raw_rows.append(row)
            validated_rows.append(validated)

    return raw_rows, validated_rows


def main() -> int:
    if len(FAMILIES) != 15:
        print(
            "FAIL: Expected 15 families, "
            f"found {len(FAMILIES)}."
        )
        return 1

    try:
        raw_rows, validated_rows = build_rows()
    except (
        KeyError,
        ValueError,
        ValidationError,
    ) as error:
        print(f"FAIL: {error}")
        return 1

    if len(raw_rows) != 45:
        print(
            "FAIL: Expected 45 rows, "
            f"found {len(raw_rows)}."
        )
        return 1

    family_errors = validate_families(
        validated_rows
    )

    if family_errors:
        print(
            "FAIL: Generated rows failed "
            "family validation."
        )

        for error in family_errors:
            print(f"- {error}")

        return 1

    cue_counts = Counter(
        row.changed_cue_from_A
        for row in validated_rows
        if row.changed_cue_from_A != "NONE"
    )

    if cue_counts != EXPECTED_CUE_COUNTS:
        print(
            "FAIL: Changed-cue counts "
            "do not match the plan."
        )
        print(dict(cue_counts))
        return 1

    if any(
        row.primary_register is not None
        or row.secondary_register is not None
        or row.acceptable_registers
        or row.gold_confidence is not None
        or row.reason_codes
        for row in validated_rows
    ):
        print(
            "FAIL: Gold fields must remain "
            "blank during authoring."
        )
        return 1

    fieldnames = list(
        DatasetRow.model_fields
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = OUTPUT_PATH.with_suffix(
        ".csv.tmp"
    )

    with temporary_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(raw_rows)

    temporary_path.replace(OUTPUT_PATH)

    print(
        "PASS: Generated 45 authoring rows "
        "across 15 complete families."
    )
    print(
        "PASS: Every B/C row changes exactly "
        "one declared cue from A."
    )
    print(
        "PASS: Gold-label fields remain blank."
    )
    print(
        "Changed-cue counts: "
        + ", ".join(
            f"{cue}={cue_counts[cue]}"
            for cue in (
                "AUTHORITY",
                "AGE",
                "FAMILIARITY",
                "SETTING",
            )
        )
    )
    print(
        f"File: {OUTPUT_PATH.as_posix()}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())