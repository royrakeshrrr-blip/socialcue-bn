from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.runner import run_experiment


class RunnerIntegrationTests(unittest.TestCase):
    def test_dummy_runs_all_conditions_and_resumes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "dummy.jsonl"
            arguments = {
                "dataset_path": ROOT / "data" / "socialcue_bn_gold_v1.0.csv",
                "config_path": ROOT / "config" / "experiment.json",
                "model_key": "dummy",
                "condition_value": "ALL",
                "split_value": "DEVELOPMENT",
                "run_id": "unit_dummy",
                "ids_file": None,
                "limit": 1,
                "output_path": output,
                "allow_test": False,
            }
            run_experiment(**arguments)
            run_experiment(**arguments)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(len(records), 3)
        self.assertEqual(
            {record["prompt_condition"] for record in records},
            {"P0_MESSAGE_ONLY", "P1_NARRATIVE_CONTEXT", "P2_STRUCTURED_CONTEXT"},
        )
        self.assertEqual(len({record["request_id"] for record in records}), 3)
        for record in records:
            self.assertNotIn("primary_register", record["input"])
            self.assertNotIn("acceptable_registers", record["input"])
            self.assertEqual(record["parsed"]["parse_status"], "valid")

    def test_test_split_is_locked_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "TEST is locked"):
                run_experiment(
                    dataset_path=ROOT / "data" / "socialcue_bn_gold_v1.0.csv",
                    config_path=ROOT / "config" / "experiment.json",
                    model_key="dummy",
                    condition_value="P0_MESSAGE_ONLY",
                    split_value="TEST",
                    run_id="unit_lock",
                    ids_file=None,
                    limit=1,
                    output_path=Path(directory) / "locked.jsonl",
                    allow_test=False,
                )


if __name__ == "__main__":
    unittest.main()
