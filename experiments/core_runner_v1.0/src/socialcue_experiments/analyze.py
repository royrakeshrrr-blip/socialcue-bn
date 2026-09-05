from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .metrics import load_raw_records, score_records
from .schema import load_dataset


PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze one SocialCue-BN raw JSONL result file.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, default=PACKAGE_ROOT / "data" / "socialcue_bn_gold_v1.0.csv")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = load_dataset(args.dataset)
        records = load_raw_records(args.input)
        results = score_records(rows, records)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    csv_path = args.output.with_suffix(".csv")
    fields = [
        "model_key",
        "prompt_condition",
        "records",
        "parseable_rate",
        "exact_schema_rate",
        "primary_accuracy",
        "acceptable_set_accuracy",
        "macro_f1_primary",
        "over_polite_errors",
        "under_polite_errors",
        "mean_latency_ms",
        "counterfactual_direction_accuracy",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for result in results.values():
            writer.writerow(
                {
                    **{field: result.get(field) for field in fields},
                    "counterfactual_direction_accuracy": result["counterfactual"]["direction_accuracy"],
                }
            )
    print(f"PASS: analyzed {len(records)} raw records across {len(results)} model-condition groups.")
    print(f"JSON: {args.output}")
    print(f"CSV: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

