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
        print(f"\nChecking {model_key}...")
        try:
            run_experiment(
                dataset_path=ROOT / "data" / "socialcue_bn_gold_v1.0.csv",
                config_path=ROOT / "config" / "experiment.json",
                model_key=model_key,
                condition_value="P0_MESSAGE_ONLY",
                split_value="DEVELOPMENT",
                run_id=run_id,
                ids_file=ROOT / "data" / "development_dry_run_ids.txt",
                limit=1,
                output_path=ROOT / "results" / "raw" / f"{run_id}.jsonl",
                allow_test=False,
            )
        except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
            failures.append((model_key, str(error)))
            print(f"FAIL: {model_key}: {error}")
        else:
            print(f"PASS: {model_key} API access works.")

    print()
    if failures:
        print("API access is not ready for every model.")
        for model_key, error in failures:
            print(f"- {model_key}: {error}")
        print("Fix only the reported key/provider problem, then run this command again.")
        return 1

    print("PASS: All three model endpoints are accessible. Three total test calls completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
