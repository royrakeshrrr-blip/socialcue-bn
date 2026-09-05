from __future__ import annotations

import json

from .base import GenerationResult


class DummyAdapter:
    def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        raw_text = json.dumps(
            {
                "register": "TUMI",
                "confidence": "MEDIUM",
                "reason_codes": ["OTHER"],
            },
            separators=(",", ":"),
        )
        return GenerationResult(
            raw_text=raw_text,
            raw_provider_response={"dummy": True, "content": raw_text},
            finish_reason="stop",
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            latency_ms=0.0,
            attempts=[{"attempt": 1, "http_status": 200, "dummy": True}],
            provider_status="success",
        )

