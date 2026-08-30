from __future__ import annotations

import json

import pytest

from src.config_loader import PROJECT_ROOT
from src.model_adapter import (
    DummyModelAdapter,
    ModelRequest,
)
from src.run_dummy_experiment import (
    CORE_CONDITIONS,
    build_prompt,
)
from src.validate_dataset import (
    load_and_validate_rows,
)


SAMPLE_PATH = (
    PROJECT_ROOT
    / "data"
    / "pilot"
    / "schema_example.csv"
)

RAW_OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "raw"
    / "core"
    / "phase2-dummy-smoke-test.jsonl"
)


def test_dummy_adapter_is_zero_cost() -> None:
    request = ModelRequest(
        request_id="pytest-dummy-001",
        prompt="Choose TUI, TUMI, or APNI.",
        temperature=0.0,
        max_output_tokens=128,
        seed=42,
    )

    adapter = DummyModelAdapter(
        fixed_label="TUMI"
    )

    response = adapter.generate(request)
    parsed = json.loads(response.raw_text)

    assert parsed["label"] == "TUMI"
    assert response.uses_api is False
    assert response.is_dummy is True
    assert response.cost_usd == 0.0


def test_invalid_dummy_label_is_rejected() -> None:
    with pytest.raises(ValueError):
        DummyModelAdapter(
            fixed_label="INVALID"
        )


def test_prompts_exclude_gold_field_names() -> None:
    rows, errors = load_and_validate_rows(
        SAMPLE_PATH
    )

    assert errors == []

    row = rows[0]

    forbidden_names = {
        "primary_register",
        "secondary_register",
        "acceptable_registers",
        "gold_confidence",
        "reason_codes",
    }

    for condition in CORE_CONDITIONS:
        prompt = build_prompt(
            row,
            condition,
        )

        for forbidden_name in forbidden_names:
            assert forbidden_name not in prompt

    message_only_prompt = build_prompt(
        row,
        "P0_MESSAGE_ONLY",
    )

    assert "authority_relation:" not in (
        message_only_prompt
    )
    assert row.speaker_role not in (
        message_only_prompt
    )

    structured_prompt = build_prompt(
        row,
        "P2_STRUCTURED_CONTEXT",
    )

    assert "authority_relation:" in (
        structured_prompt
    )
    assert "relative_age:" in (
        structured_prompt
    )


def test_saved_dummy_run_is_complete_and_safe() -> None:
    assert RAW_OUTPUT_PATH.is_file()

    records = [
        json.loads(line)
        for line in RAW_OUTPUT_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert len(records) == 9

    observed_conditions = {
        record["prompt_condition"]
        for record in records
    }

    assert observed_conditions == set(
        CORE_CONDITIONS
    )

    request_ids = [
        record["response"]["request_id"]
        for record in records
    ]

    assert len(request_ids) == len(
        set(request_ids)
    )

    forbidden_input_fields = {
        "primary_register",
        "secondary_register",
        "acceptable_registers",
        "gold_confidence",
        "reason_codes",
    }

    for record in records:
        response = record["response"]
        input_record = record["input"]

        assert response["uses_api"] is False
        assert response["is_dummy"] is True
        assert response["cost_usd"] == 0.0

        assert forbidden_input_fields.isdisjoint(
            input_record
        )