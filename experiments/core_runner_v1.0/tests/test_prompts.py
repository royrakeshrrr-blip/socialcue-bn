from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.prompts import render_prompt
from socialcue_experiments.schema import load_dataset


class PromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.row = load_dataset(ROOT / "data" / "development.csv")[0]

    def test_p0_contains_message_but_no_context_fields(self) -> None:
        _, prompt = render_prompt(self.row, "P0_MESSAGE_ONLY")
        self.assertIn(self.row.romanized_message, prompt)
        self.assertNotIn(self.row.recipient_role, prompt)
        self.assertNotIn("authority_relation:", prompt)

    def test_p1_contains_narrative_context(self) -> None:
        _, prompt = render_prompt(self.row, "P1_NARRATIVE_CONTEXT")
        self.assertIn(self.row.romanized_message, prompt)
        self.assertIn("equal authority", prompt)
        self.assertIn("semi formal", prompt)

    def test_p2_contains_structured_context_and_three_demos(self) -> None:
        _, prompt = render_prompt(self.row, "P2_STRUCTURED_CONTEXT")
        self.assertIn(f"recipient_role: {self.row.recipient_role}", prompt)
        self.assertIn(f"authority_relation: {self.row.authority_relation}", prompt)
        self.assertEqual(prompt.count("DEMONSTRATION "), 3)
        self.assertIn('"register":"TUI"', prompt)
        self.assertIn('"register":"TUMI"', prompt)
        self.assertIn('"register":"APNI"', prompt)

    def test_no_condition_leaves_placeholders(self) -> None:
        for condition in (
            "P0_MESSAGE_ONLY",
            "P1_NARRATIVE_CONTEXT",
            "P2_STRUCTURED_CONTEXT",
        ):
            _, prompt = render_prompt(self.row, condition)
            self.assertNotIn("[[", prompt)
            self.assertNotIn("]]", prompt)


if __name__ == "__main__":
    unittest.main()
