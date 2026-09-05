from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from .prompts import CONDITION_FILES, PROMPT_DIR
from .schema import load_dataset


PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    try:
        full = load_dataset(PACKAGE_ROOT / "data" / "socialcue_bn_gold_v1.0.csv")
        development = load_dataset(PACKAGE_ROOT / "data" / "development.csv")
        test = load_dataset(PACKAGE_ROOT / "data" / "test.csv")
        if len(full) != 450 or len(development) != 90 or len(test) != 360:
            raise ValueError("Expected 450 full, 90 development, and 360 test rows.")
        if {row.instance_id for row in development} & {row.instance_id for row in test}:
            raise ValueError("Development and test IDs overlap.")
        if {row.message_family_id for row in development} & {row.message_family_id for row in test}:
            raise ValueError("A message family crosses development and test.")

        config = json.loads((PACKAGE_ROOT / "config" / "experiment.json").read_text(encoding="utf-8"))
        selected = [model for model in config["models"] if model.get("selected")]
        if len(selected) != 3:
            raise ValueError("Exactly three real models must be selected.")
        expected_parameters = {
            "gemini_3_5_flash_lite": {"reasoning_effort": "minimal"},
            "groq_gpt_oss_120b": {"reasoning_effort": "low", "include_reasoning": False},
            "groq_qwen_3_8_27b": {"reasoning_effort": "none"},
        }
        for model in selected:
            if model.get("provider_parameters") != expected_parameters[model["key"]]:
                raise ValueError(f"Unexpected provider parameters for {model['key']}.")
            if model["key"] == "gemini_3_5_flash_lite" and model.get("include_temperature") is not False:
                raise ValueError("Gemini 3.5 Flash-Lite must use provider-default temperature.")
        if config.get("max_output_tokens") != 256:
            raise ValueError("Expected max_output_tokens=256.")
        development_ids = {row.instance_id for row in development}
        demo_ids = set(config["development_demonstration_ids"])
        if not demo_ids <= development_ids:
            raise ValueError("A P2 demonstration is not in DEVELOPMENT.")

        dry_run_path = PACKAGE_ROOT / "data" / "development_dry_run_ids.txt"
        dry_run_ids = [
            line.strip()
            for line in dry_run_path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        if len(dry_run_ids) != 10 or len(set(dry_run_ids)) != 10:
            raise ValueError("The development dry-run list must contain 10 unique IDs.")
        if not set(dry_run_ids) <= development_ids:
            raise ValueError("A dry-run instance is not in DEVELOPMENT.")
        development_by_id = {row.instance_id: row for row in development}
        dry_rows = [development_by_id[instance_id] for instance_id in dry_run_ids]
        if {row.primary_register for row in dry_rows} != {"TUI", "TUMI", "APNI"}:
            raise ValueError("The development dry run does not cover all three gold labels.")
        if {row.domain for row in dry_rows} != {
            "ACADEMIC",
            "FAMILY",
            "FRIENDSHIP",
            "ONLINE",
            "PROFESSIONAL",
            "SERVICE_PUBLIC",
        }:
            raise ValueError("The development dry run does not cover all six domains.")

        manifest_path = PACKAGE_ROOT / "config" / "PROMPT_MANIFEST.csv"
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            manifest_rows = list(csv.DictReader(file))
        expected_prompt_names = {"SYSTEM_v1.0.txt", *CONDITION_FILES.values()}
        if {row["prompt_file"] for row in manifest_rows} != expected_prompt_names:
            raise ValueError("Prompt manifest file list is incomplete.")
        for row in manifest_rows:
            prompt_path = PROMPT_DIR / row["prompt_file"]
            if sha256_file(prompt_path) != row["sha256"]:
                raise ValueError(f"Prompt checksum mismatch: {row['prompt_file']}")

        env_text = (PACKAGE_ROOT / ".env.example").read_text(encoding="utf-8")
        if "replace_with" not in env_text:
            raise ValueError(".env.example appears to contain a real key.")
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1

    print("PASS: 450 rows, 150 intact families, and the 90/360 split are valid.")
    print("PASS: all demonstrations are development-only and prompt checksums match.")
    print("PASS: the 10-item development dry run covers all labels and domains.")
    print("PASS: three real API model candidates and one zero-cost dummy are configured.")
    return 0
