from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class GenerationResult:
    raw_text: str
    raw_provider_response: dict[str, Any] | None
    finish_reason: str | None
    usage: dict[str, Any]
    latency_ms: float
    attempts: list[dict[str, Any]]
    provider_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ModelAdapter(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        ...

