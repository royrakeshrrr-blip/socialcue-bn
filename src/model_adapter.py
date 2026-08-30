from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any


ALLOWED_LABELS = {"TUI", "TUMI", "APNI"}


@dataclass(frozen=True, slots=True)
class ModelRequest:
    """One request sent to a model adapter."""

    request_id: str
    prompt: str
    temperature: float
    max_output_tokens: int
    seed: int | None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError(
                "request_id must not be empty"
            )

        if not self.prompt.strip():
            raise ValueError(
                "prompt must not be empty"
            )

        if self.temperature < 0:
            raise ValueError(
                "temperature cannot be negative"
            )

        if self.max_output_tokens < 1:
            raise ValueError(
                "max_output_tokens must be positive"
            )


@dataclass(frozen=True, slots=True)
class ModelResponse:
    """Raw response and metadata returned by an adapter."""

    request_id: str
    provider: str
    model_name: str
    model_version: str
    raw_text: str
    finish_reason: str
    input_token_estimate: int
    output_token_estimate: int
    latency_ms: float
    cost_usd: float
    attempt_count: int
    uses_api: bool
    is_dummy: bool

    def to_dict(self) -> dict[str, Any]:
        """Convert the response into a JSON-ready dictionary."""

        return asdict(self)


class ModelAdapter(ABC):
    """Common interface for dummy and future API models."""

    @abstractmethod
    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Generate one model response."""

        raise NotImplementedError


class DummyModelAdapter(ModelAdapter):
    """Return a deterministic label without using an API."""

    def __init__(
        self,
        fixed_label: str = "TUMI",
    ) -> None:
        if fixed_label not in ALLOWED_LABELS:
            raise ValueError(
                "fixed_label must be TUI, TUMI, or APNI"
            )

        self.fixed_label = fixed_label
        self.provider = "dummy"
        self.model_name = "fixed-label-dummy"
        self.model_version = "1.0"

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Return a fixed response with zero financial cost."""

        raw_text = json.dumps(
            {
                "label": self.fixed_label,
                "reason": "DUMMY_RESPONSE_NO_API",
            },
            ensure_ascii=False,
            sort_keys=True,
        )

        return ModelResponse(
            request_id=request.request_id,
            provider=self.provider,
            model_name=self.model_name,
            model_version=self.model_version,
            raw_text=raw_text,
            finish_reason="stop",
            input_token_estimate=max(
                1,
                len(request.prompt.split()),
            ),
            output_token_estimate=max(
                1,
                len(raw_text.split()),
            ),
            latency_ms=0.0,
            cost_usd=0.0,
            attempt_count=1,
            uses_api=False,
            is_dummy=True,
        )


def run_smoke_test() -> None:
    """Confirm that the dummy adapter behaves safely."""

    request = ModelRequest(
        request_id="phase2-smoke-001",
        prompt=(
            "Choose one register label: "
            "TUI, TUMI, or APNI."
        ),
        temperature=0.0,
        max_output_tokens=128,
        seed=42,
    )

    adapter = DummyModelAdapter(
        fixed_label="TUMI"
    )

    response = adapter.generate(request)

    parsed_response = json.loads(
        response.raw_text
    )

    if parsed_response.get("label") != "TUMI":
        raise RuntimeError(
            "Dummy adapter returned the wrong label."
        )

    if response.uses_api:
        raise RuntimeError(
            "Dummy adapter must not use an API."
        )

    if response.cost_usd != 0.0:
        raise RuntimeError(
            "Dummy adapter cost must remain zero."
        )

    print(
        "SUCCESS: Dummy model adapter passed."
    )
    print(
        f"Request ID: {response.request_id}"
    )
    print(
        f"Provider: {response.provider}"
    )
    print(
        f"Model: {response.model_name}"
    )
    print(
        f"Raw response: {response.raw_text}"
    )
    print(
        f"Uses API: {response.uses_api}"
    )
    print(
        f"Cost: USD {response.cost_usd:.2f}"
    )


if __name__ == "__main__":
    run_smoke_test()