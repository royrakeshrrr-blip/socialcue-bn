from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.schema import load_dataset


class DatasetSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.full = load_dataset(ROOT / "data" / "socialcue_bn_gold_v1.0.csv")
        cls.development = load_dataset(ROOT / "data" / "development.csv")
        cls.test = load_dataset(ROOT / "data" / "test.csv")

    def test_expected_sizes_and_gold_distribution(self) -> None:
        self.assertEqual(len(self.full), 450)
        self.assertEqual(len(self.development), 90)
        self.assertEqual(len(self.test), 360)
        self.assertEqual(
            Counter(row.primary_register for row in self.full),
            Counter({"APNI": 221, "TUMI": 210, "TUI": 19}),
        )

    def test_split_is_family_safe(self) -> None:
        development_families = {row.message_family_id for row in self.development}
        test_families = {row.message_family_id for row in self.test}
        self.assertEqual(len(development_families), 30)
        self.assertEqual(len(test_families), 120)
        self.assertFalse(development_families & test_families)

    def test_every_family_has_identical_message_and_abc(self) -> None:
        families: dict[str, list] = {}
        for row in self.full:
            families.setdefault(row.message_family_id, []).append(row)
        self.assertEqual(len(families), 150)
        for rows in families.values():
            self.assertEqual({row.variant for row in rows}, {"A", "B", "C"})
            self.assertEqual(len({row.romanized_message for row in rows}), 1)

    def test_demos_are_development_only_and_cover_labels(self) -> None:
        by_id = {row.instance_id: row for row in self.full}
        demo_ids = ["F017-A", "F007-A", "F002-C"]
        self.assertEqual({by_id[value].split for value in demo_ids}, {"DEVELOPMENT"})
        self.assertEqual(
            {by_id[value].primary_register for value in demo_ids},
            {"TUI", "TUMI", "APNI"},
        )


if __name__ == "__main__":
    unittest.main()
