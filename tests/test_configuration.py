from __future__ import annotations

import yaml

from src.config_loader import (
    PROJECT_ROOT,
    load_config,
)


def test_experiment_safety_settings() -> None:
    config, key_available = load_config()

    assert config["runtime"]["mode"] == "dummy"
    assert config["runtime"]["remote_api_only"] is True
    assert config["runtime"]["local_llm_allowed"] is False

    assert (
        config["safety"]["hard_budget_usd"]
        == 0.0
    )
    assert (
        config["safety"]["paid_fallback_allowed"]
        is False
    )
    assert (
        config["safety"]["log_api_keys"]
        is False
    )

    assert (
        config["dataset"][
            "projected_core_responses"
        ]
        == 4050
    )

    assert isinstance(key_available, bool)


def test_free_quota_policy() -> None:
    quota_path = (
        PROJECT_ROOT
        / "config"
        / "free_quota.yaml"
    )

    with quota_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        quota = yaml.safe_load(file)

    policy = quota["policy"]

    assert policy["access_mode"] == "FREE_ONLY"
    assert policy["hard_budget_usd"] == 0.0
    assert (
        policy["paid_fallback_allowed"]
        is False
    )
    assert policy["reserve_fraction"] == 0.25
    assert policy["dry_run_instances"] == 10
    assert isinstance(
        quota["free_models"],
        list,
    )