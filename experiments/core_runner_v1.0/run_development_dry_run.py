from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.runner import run_experiment


MODELS = (
    "gemini_3_5_flash_lite",
    "groq_gpt_oss_120b",
    "groq_qwen_3_8_27b",
)


def main() -> int:
    failures: list[tuple[str, str]] = []
    for model_key in MODELS:
        run_id = f"development_{model_key}"
        print(f"\nRunning 10-item × 3-condition batch for {model_key}...")
        try:
            run_experiment(
                dataset_path=ROOT / "data" / "socialcue_bn_gold_v1.0.csv",
                config_path=ROOT / "config" / "experiment.json",
                model_key=model_key,
                condition_value="ALL",
                split_value="DEVELOPMENT",
                run_id=run_id,
                ids_file=ROOT / "data" / "development_dry_run_ids.txt",
                limit=None,
                output_path=ROOT / "results" / "raw" / f"{run_id}.jsonl",
                allow_test=False,
            )
        except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
            failures.append((model_key, str(error)))
            print(f"FAIL: {model_key}: {error}")

    print()
    if failures:
        print("One or more batches stopped safely.")
        for model_key, error in failures:
            print(f"- {model_key}: {error}")
        print("Run this same command later; completed requests will not be repeated.")
        return 1

    print("PASS: The 90-call DEVELOPMENT dry run is complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
