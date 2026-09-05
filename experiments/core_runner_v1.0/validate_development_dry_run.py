from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.metrics import load_raw_records


MODELS = (
    "gemini_3_5_flash_lite",
    "groq_gpt_oss_120b",
    "groq_qwen_3_8_27b",
)
CONDITIONS = {
    "P0_MESSAGE_ONLY",
    "P1_NARRATIVE_CONTEXT",
    "P2_STRUCTURED_CONTEXT",
}


def main() -> int:
    expected_ids = {
        line.strip()
        for line in (ROOT / "data" / "development_dry_run_ids.txt")
        .read_text(encoding="utf-8-sig")
        .splitlines()
        if line.strip()
    }
    failures: list[str] = []
    total_records = 0

    for model_key in MODELS:
        path = ROOT / "results" / "raw" / f"development_{model_key}.jsonl"
        try:
            records = load_raw_records(path)
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
            failures.append(f"{model_key}: {error}")
            continue

        total_records += len(records)
        observed_pairs = {
            (record["input"]["instance_id"], record["prompt_condition"])
            for record in records
        }
        expected_pairs = {
            (instance_id, condition)
            for instance_id in expected_ids
            for condition in CONDITIONS
        }
        if len(records) != 30 or observed_pairs != expected_pairs:
            failures.append(f"{model_key}: expected exactly 30 dry-run records.")
            continue
        if any(record["model_key"] != model_key for record in records):
            failures.append(f"{model_key}: model key mismatch in raw results.")
            continue
        if any(record["generation"]["provider_status"] != "success" for record in records):
            failures.append(f"{model_key}: provider failure found in raw results.")
            continue
        forbidden = {
            "primary_register",
            "secondary_register",
            "acceptable_registers",
            "gold_confidence",
            "reason_codes",
        }
        if any(forbidden.intersection(record["input"]) for record in records):
            failures.append(f"{model_key}: a gold field leaked into a model input.")
            continue
        statuses = Counter(record["parsed"]["parse_status"] for record in records)
        print(f"PASS: {model_key}: 30 records; parse statuses {dict(statuses)}")

    if failures:
        print("\nFAIL: Development dry-run validation failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    if total_records != 90:
        print(f"FAIL: expected 90 total records but found {total_records}.")
        return 1
    print("PASS: All 90 DEVELOPMENT dry-run records are complete and safe for analysis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
