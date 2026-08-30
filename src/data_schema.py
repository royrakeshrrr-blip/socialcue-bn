from __future__ import annotations

import re
from typing import Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


Variant = Literal["A", "B", "C"]
Register = Literal["TUI", "TUMI", "APNI"]
SourceRegister = Literal["TUI", "TUMI", "APNI", "MIXED", "UNCLEAR"]

Domain = Literal[
    "ACADEMIC",
    "PROFESSIONAL",
    "FAMILY",
    "FRIENDSHIP",
    "SERVICE_PUBLIC",
    "ONLINE",
]

Intent = Literal[
    "REQUEST",
    "QUESTION",
    "REMINDER",
    "APOLOGY",
    "INVITATION",
    "FOLLOW_UP",
    "CONFIRMATION",
    "INFORMATION",
    "FEEDBACK",
    "OTHER",
]

Authority = Literal["LOWER", "EQUAL", "HIGHER", "UNKNOWN"]
RelativeAge = Literal["YOUNGER", "SIMILAR", "OLDER", "UNKNOWN"]
Familiarity = Literal["LOW", "MEDIUM", "HIGH"]
Setting = Literal["INFORMAL", "SEMI_FORMAL", "FORMAL"]

ChangedCue = Literal[
    "NONE",
    "AUTHORITY",
    "AGE",
    "FAMILIARITY",
    "SETTING",
]

Answerability = Literal[
    "ANSWERABLE",
    "UNDERSPECIFIED",
    "CONTRADICTORY",
    "CONTENTIOUS",
]

Confidence = Literal["HIGH", "MEDIUM", "LOW"]

ReasonCode = Literal[
    "AUTHORITY",
    "AGE",
    "FAMILIARITY",
    "SETTING",
    "KINSHIP",
    "EMOTIONAL_STANCE",
    "OTHER",
]

MixLevel = Literal["NONE", "LIGHT", "MODERATE"]

AuthoringSource = Literal[
    "AI_CANDIDATE_REVISED",
    "HUMAN_DRAFT",
    "OTHER_DOCUMENTED",
]

RevisionStatus = Literal["REVIEWED", "REWRITTEN", "REJECTED"]
Split = Literal["DEVELOPMENT", "TEST"]


class DatasetRow(BaseModel):
    """Validated representation of one SocialCue-BN CSV row."""

    model_config = ConfigDict(extra="forbid")

    instance_id: str
    message_family_id: str
    variant: Variant
    romanized_message: str
    source_register: SourceRegister
    domain: Domain
    intent: Intent
    speaker_role: str
    recipient_role: str
    authority_relation: Authority
    relative_age: RelativeAge
    familiarity: Familiarity
    setting: Setting
    changed_cue_from_A: ChangedCue
    comparison_ids: list[str]
    primary_register: Register | None
    secondary_register: Register | None
    acceptable_registers: list[Register]
    answerability: Answerability
    gold_confidence: Confidence | None
    reason_codes: list[ReasonCode]
    english_token_ratio: float = Field(ge=0.0, le=0.30)
    code_mix_level: MixLevel
    spelling_noise_level: MixLevel
    authoring_source: AuthoringSource
    human_revision_status: RevisionStatus
    split: Split
    dataset_version: str

    @field_validator(
        "primary_register",
        "secondary_register",
        "gold_confidence",
        mode="before",
    )
    @classmethod
    def convert_blank_to_none(cls, value: object) -> object:
        if value is None or str(value).strip() == "":
            return None
        return value

    @field_validator(
        "comparison_ids",
        "acceptable_registers",
        "reason_codes",
        mode="before",
    )
    @classmethod
    def parse_pipe_separated_values(
        cls,
        value: object,
    ) -> list[str]:
        if value is None or str(value).strip() == "":
            return []

        if isinstance(value, list):
            return value

        return [
            part.strip()
            for part in str(value).split("|")
            if part.strip()
        ]

    @field_validator("instance_id")
    @classmethod
    def validate_instance_id(cls, value: str) -> str:
        if re.fullmatch(r"F\d{3}-[ABC]", value) is None:
            raise ValueError("must follow the format F001-A")

        return value

    @field_validator("message_family_id")
    @classmethod
    def validate_family_id(cls, value: str) -> str:
        if re.fullmatch(r"F\d{3}", value) is None:
            raise ValueError("must follow the format F001")

        return value

    @field_validator(
        "romanized_message",
        "speaker_role",
        "recipient_role",
        "dataset_version",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty")

        if value != value.strip():
            raise ValueError(
                "must not start or end with whitespace"
            )

        if "\n" in value or "\r" in value:
            raise ValueError("must remain on one line")

        return value

    @model_validator(mode="after")
    def validate_linked_fields(self) -> Self:
        expected_id = (
            f"{self.message_family_id}-{self.variant}"
        )

        if self.instance_id != expected_id:
            raise ValueError(
                f"instance_id must be {expected_id}"
            )

        if len(self.comparison_ids) != len(
            set(self.comparison_ids)
        ):
            raise ValueError(
                "comparison_ids contains duplicate IDs"
            )

        if self.instance_id in self.comparison_ids:
            raise ValueError(
                "an instance cannot compare with itself"
            )

        if self.variant == "A":
            expected_comparisons = {
                f"{self.message_family_id}-B",
                f"{self.message_family_id}-C",
            }

            if self.changed_cue_from_A != "NONE":
                raise ValueError(
                    "variant A must use "
                    "changed_cue_from_A=NONE"
                )

            if set(self.comparison_ids) != (
                expected_comparisons
            ):
                raise ValueError(
                    "variant A must compare with "
                    "its B and C rows"
                )
        else:
            if self.changed_cue_from_A == "NONE":
                raise ValueError(
                    "variants B and C must declare "
                    "a changed cue"
                )

            if self.comparison_ids != [
                f"{self.message_family_id}-A"
            ]:
                raise ValueError(
                    "variants B and C must compare only with A"
                )

        if self.english_token_ratio == 0.0:
            expected_mix_level = "NONE"
        elif self.english_token_ratio <= 0.15:
            expected_mix_level = "LIGHT"
        else:
            expected_mix_level = "MODERATE"

        if self.code_mix_level != expected_mix_level:
            raise ValueError(
                "code_mix_level does not match "
                "english_token_ratio; "
                f"expected {expected_mix_level}"
            )

        if self.primary_register is None:
            if (
                self.secondary_register is not None
                or self.acceptable_registers
            ):
                raise ValueError(
                    "secondary/acceptable registers "
                    "require a primary register"
                )
        else:
            if not self.acceptable_registers:
                raise ValueError(
                    "acceptable_registers must not be empty"
                )

            if (
                self.acceptable_registers[0]
                != self.primary_register
            ):
                raise ValueError(
                    "acceptable_registers must begin "
                    "with primary_register"
                )

            if len(self.acceptable_registers) != len(
                set(self.acceptable_registers)
            ):
                raise ValueError(
                    "acceptable_registers contains duplicates"
                )

            if len(self.acceptable_registers) > 2:
                raise ValueError(
                    "only one secondary register is allowed"
                )

            expected_registers = {
                self.primary_register
            }

            if self.secondary_register is not None:
                if (
                    self.secondary_register
                    == self.primary_register
                ):
                    raise ValueError(
                        "secondary_register must differ "
                        "from primary_register"
                    )

                expected_registers.add(
                    self.secondary_register
                )

            if set(self.acceptable_registers) != (
                expected_registers
            ):
                raise ValueError(
                    "acceptable_registers must equal "
                    "primary plus secondary"
                )

        return self