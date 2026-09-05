from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.parser import parse_response


class ParserTests(unittest.TestCase):
    def test_valid_exact_json(self) -> None:
        parsed = parse_response(
            '{"register":"APNI","confidence":"HIGH","reason_codes":["AUTHORITY","AGE"]}'
        )
        self.assertEqual(parsed.parse_status, "valid")
        self.assertEqual(parsed.register, "APNI")
        self.assertEqual(parsed.reason_codes, ["AUTHORITY", "AGE"])

    def test_normalizes_lowercase_values(self) -> None:
        parsed = parse_response(
            '{"register":"tumi","confidence":"medium","reason_codes":"familiarity|setting"}'
        )
        self.assertEqual(parsed.parse_status, "valid")
        self.assertEqual(parsed.register, "TUMI")
        self.assertEqual(parsed.confidence, "MEDIUM")

    def test_recovers_fenced_json(self) -> None:
        parsed = parse_response(
            '```json\n{"register":"TUI","confidence":"LOW","reason_codes":["KINSHIP"]}\n```'
        )
        self.assertEqual(parsed.parse_status, "recoverable_format")
        self.assertTrue(parsed.recovered_format)

    def test_recovers_json_from_extra_prose(self) -> None:
        parsed = parse_response(
            'Answer: {"register":"APNI","confidence":"HIGH","reason_codes":["SETTING"]}'
        )
        self.assertEqual(parsed.parse_status, "recoverable_format")

    def test_keeps_valid_label_when_metadata_missing(self) -> None:
        parsed = parse_response('{"register":"TUMI"}')
        self.assertEqual(parsed.parse_status, "recoverable_missing_metadata")
        self.assertEqual(parsed.register, "TUMI")

    def test_rejects_illegal_label(self) -> None:
        parsed = parse_response(
            '{"register":"AMI","confidence":"HIGH","reason_codes":["OTHER"]}'
        )
        self.assertEqual(parsed.parse_status, "invalid_label")
        self.assertIsNone(parsed.register)

    def test_rejects_empty_response(self) -> None:
        parsed = parse_response("   ")
        self.assertEqual(parsed.parse_status, "empty")


if __name__ == "__main__":
    unittest.main()
