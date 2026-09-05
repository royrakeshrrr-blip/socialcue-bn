from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any


REGISTERS = {"TUI", "TUMI", "APNI"}
CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
REASON_CODES = {
    "AUTHORITY",
    "AGE",
    "FAMILIARITY",
    "SETTING",
    "KINSHIP",
    "EMOTIONAL_STANCE",
    "OTHER",
}


@dataclass(frozen=True, slots=True)
class ParsedResponse:
    register: str | None
    confidence: str | None
    reason_codes: list[str]
    parse_status: str
    parse_error: str | None
    recovered_format: bool
    parsed_object: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _json_candidates(raw_text: str) -> list[tuple[str, bool]]:
    candidates = [(raw_text.strip(), False)]
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", raw_text.strip(), flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        candidates.append((fenced.group(1).strip(), True))
    object_match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
    if object_match and object_match.group(0).strip() != raw_text.strip():
        candidates.append((object_match.group(0).strip(), True))
    seen: set[str] = set()
    return [(value, recovered) for value, recovered in candidates if value and not (value in seen or seen.add(value))]


def parse_response(raw_text: str) -> ParsedResponse:
    if not raw_text or not raw_text.strip():
        return ParsedResponse(None, None, [], "empty", "Response is empty.", False, None)

    parsed: dict[str, Any] | None = None
    recovered = False
    last_error: str | None = None
    for candidate, candidate_recovered in _json_candidates(raw_text):
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError as error:
            last_error = str(error)
            continue
        if isinstance(value, dict):
            parsed = value
            recovered = candidate_recovered
            break
        last_error = "Top-level JSON value is not an object."

    if parsed is None:
        return ParsedResponse(None, None, [], "invalid_json", last_error, recovered, None)

    register_value = parsed.get("register", parsed.get("label"))
    register = str(register_value).strip().upper() if register_value is not None else ""
    if register not in REGISTERS:
        return ParsedResponse(None, None, [], "invalid_label", f"Illegal register: {register_value!r}", recovered, parsed)

    confidence_value = parsed.get("confidence")
    confidence = str(confidence_value).strip().upper() if confidence_value is not None else None
    if confidence not in CONFIDENCE:
        confidence = None

    raw_reasons = parsed.get("reason_codes", [])
    if isinstance(raw_reasons, str):
        raw_reasons = re.split(r"[|,]", raw_reasons)
    if not isinstance(raw_reasons, list):
        raw_reasons = []
    reason_codes = []
    for reason in raw_reasons:
        normalized = str(reason).strip().upper()
        if normalized in REASON_CODES and normalized not in reason_codes:
            reason_codes.append(normalized)

    if confidence is None or not reason_codes:
        status = "recoverable_missing_metadata"
        error = "Register is valid, but confidence or reason_codes is missing/invalid."
    elif recovered:
        status = "recoverable_format"
        error = "Valid JSON object was recovered from surrounding formatting."
    else:
        status = "valid"
        error = None

    return ParsedResponse(register, confidence, reason_codes, status, error, recovered, parsed)

