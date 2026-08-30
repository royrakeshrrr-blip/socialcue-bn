from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.config_loader import PROJECT_ROOT
from src.data_schema import DatasetRow
from src.validate_dataset import (
    load_and_validate_rows,
    validate_families,
)


SAMPLE_PATH = (
    PROJECT_ROOT
    / "data"
    / "pilot"
    / "schema_example.csv"
)


def load_sample_rows() -> list[DatasetRow]:
    rows, errors = load_and_validate_rows(
        SAMPLE_PATH
    )

    assert errors == []

    return rows


def test_schema_example_passes_row_validation() -> None:
    rows = load_sample_rows()

    assert len(rows) == 3


def test_schema_example_passes_family_validation() -> None:
    rows = load_sample_rows()

    assert validate_families(rows) == []


def test_code_mix_mismatch_is_rejected() -> None:
    row = load_sample_rows()[0]

    invalid_data = row.model_dump(
        mode="json"
    )

    invalid_data["english_token_ratio"] = 0.20
    invalid_data["code_mix_level"] = "LIGHT"

    with pytest.raises(
        ValidationError,
        match=(
            "code_mix_level does not match "
            "english_token_ratio"
        ),
    ):
        DatasetRow.model_validate(
            invalid_data
        )


def test_ratio_above_limit_is_rejected() -> None:
    row = load_sample_rows()[0]

    invalid_data = row.model_dump(
        mode="json"
    )

    invalid_data["english_token_ratio"] = 0.31
    invalid_data["code_mix_level"] = "MODERATE"

    with pytest.raises(ValidationError):
        DatasetRow.model_validate(
            invalid_data
        )


def test_multiple_cue_changes_are_rejected() -> None:
    rows = load_sample_rows()

    by_variant = {
        row.variant: row
        for row in rows
    }

    invalid_c = by_variant["C"].model_copy(
        update={
            "authority_relation": "LOWER",
        }
    )

    invalid_family = [
        by_variant["A"],
        by_variant["B"],
        invalid_c,
    ]

    errors = validate_families(
        invalid_family
    )

    assert any(
        "F000-C" in error
        and "actual changed field(s)" in error
        for error in errors
    )