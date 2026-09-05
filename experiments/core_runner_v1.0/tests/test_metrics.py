from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.metrics import score_group
from socialcue_experiments.schema import load_dataset


def make_record(instance_id: str, register: str) -> dict:
    return {
        "input": {"instance_id": instance_id},
        "parsed": {"parse_status": "valid", "register": register},
        "generation": {"latency_ms": 5.0},
    }


class MetricTests(unittest.TestCase):
    def test_primary_and_acceptable_accuracy(self) -> None:
        rows = load_dataset(ROOT / "data" / "development.csv")[:3]
        records = [make_record(row.instance_id, row.primary_register) for row in rows]
        result = score_group(rows, records)
        self.assertEqual(result["primary_accuracy"], 1.0)
        self.assertEqual(result["acceptable_set_accuracy"], 1.0)
        self.assertEqual(result["macro_f1_primary"], 2 / 3)
        self.assertEqual(result["counterfactual"]["evaluable_pairs"], 2)

    def test_secondary_prediction_counts_as_acceptable_not_primary(self) -> None:
        row = load_dataset(ROOT / "data" / "development.csv")[0]
        self.assertTrue(row.secondary_register)
        result = score_group([row], [make_record(row.instance_id, row.secondary_register)])
        self.assertEqual(result["primary_accuracy"], 0.0)
        self.assertEqual(result["acceptable_set_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
