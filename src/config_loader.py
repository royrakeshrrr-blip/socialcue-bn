from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "experiment.yaml"
ENV_PATH = PROJECT_ROOT / ".env"

REQUIRED_SECTIONS = {
    "project",
    "runtime",
    "safety",
    "generation",
    "prompts",
    "model",
    "dataset",
    "extension",
    "paths",
}


def load_config(
    config_path: Path = CONFIG_PATH,
) -> tuple[dict[str, Any], bool]:
    """Load and validate the experiment configuration safely."""

    load_dotenv(dotenv_path=ENV_PATH, override=False)

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("The configuration must contain a YAML mapping.")

    missing_sections = REQUIRED_SECTIONS - set(config)
    if missing_sections:
        missing = ", ".join(sorted(missing_sections))
        raise ValueError(f"Missing configuration sections: {missing}")

    if float(config["safety"]["hard_budget_usd"]) != 0.0:
        raise ValueError("The hard API budget must remain USD 0.")

    if config["safety"]["paid_fallback_allowed"]:
        raise ValueError("Paid API fallback must remain disabled.")

    if config["runtime"]["local_llm_allowed"]:
        raise ValueError("Local LLM inference must remain disabled.")

    if not config["runtime"]["remote_api_only"]:
        raise ValueError("The required LLM workflow must remain API-only.")

    dataset = config["dataset"]

    calculated_instances = (
        int(dataset["total_families"])
        * int(dataset["contexts_per_family"])
    )

    if calculated_instances != int(dataset["total_instances"]):
        raise ValueError("The configured dataset instance count is incorrect.")

    calculated_responses = (
        int(dataset["total_instances"])
        * int(dataset["core_model_count"])
        * int(dataset["core_prompt_count"])
    )

    if calculated_responses != int(dataset["projected_core_responses"]):
        raise ValueError("The projected core response count is incorrect.")

    split_families = (
        int(dataset["development_families"])
        + int(dataset["test_families"])
    )

    if split_families != int(dataset["total_families"]):
        raise ValueError("Development and test family counts do not add up.")

    key_variable = str(config["model"]["api_key_env"])
    api_key_available = bool(os.getenv(key_variable, "").strip())

    return config, api_key_available


def main() -> None:
    """Load the configuration and print only non-secret information."""

    config, api_key_available = load_config()

    print("SUCCESS: Configuration loaded and validated.")
    print(f"Project: {config['project']['name']}")
    print(f"Protocol: {config['project']['protocol_version']}")
    print(f"Run mode: {config['runtime']['mode']}")
    print(f"Model: {config['model']['name']}")
    print(
        "Projected core responses:",
        config["dataset"]["projected_core_responses"],
    )
    print(
        "Hard budget: USD",
        f"{float(config['safety']['hard_budget_usd']):.2f}",
    )
    print(f"API key available: {api_key_available}")
    print("The API-key value was not printed.")


if __name__ == "__main__":
    main()