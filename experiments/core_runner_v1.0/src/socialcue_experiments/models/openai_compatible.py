from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from .base import GenerationResult


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _extract_content(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    content = (choices[0].get("message") or {}).get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(str(item.get("text", "")) if isinstance(item, dict) else str(item) for item in content)
    return str(content or "")


class OpenAICompatibleAdapter:
    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str,
        model_id: str,
        temperature: float,
        max_output_tokens: int,
        retry_count: int,
        timeout_seconds: int,
        provider_parameters: dict[str, Any] | None = None,
        include_temperature: bool = True,
    ) -> None:
        self.endpoint = endpoint
        self.api_key = api_key
        self.model_id = model_id
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.retry_count = retry_count
        self.timeout_seconds = timeout_seconds
        self.provider_parameters = dict(provider_parameters or {})
        self.include_temperature = include_temperature

    def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        body = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": self.max_output_tokens,
        }
        if self.include_temperature:
            body["temperature"] = self.temperature
        reserved = {"model", "messages", "temperature", "max_tokens"}
        overlap = reserved.intersection(self.provider_parameters)
        if overlap:
            raise ValueError(
                "Provider parameters cannot override core fields: " + ", ".join(sorted(overlap))
            )
        body.update(self.provider_parameters)
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        attempts: list[dict[str, Any]] = []
        total_start = time.perf_counter()

        for attempt_number in range(1, self.retry_count + 2):
            request_time = utc_now()
            request = urllib.request.Request(
                self.endpoint,
                data=encoded,
                method="POST",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "SocialCue-BN/1.0",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    response_bytes = response.read()
                    response_json = json.loads(response_bytes.decode("utf-8"))
                    attempts.append(
                        {
                            "attempt": attempt_number,
                            "request_timestamp_utc": request_time,
                            "response_timestamp_utc": utc_now(),
                            "http_status": response.status,
                        }
                    )
                    choice = (response_json.get("choices") or [{}])[0]
                    return GenerationResult(
                        raw_text=_extract_content(response_json),
                        raw_provider_response=response_json,
                        finish_reason=choice.get("finish_reason"),
                        usage=response_json.get("usage") or {},
                        latency_ms=(time.perf_counter() - total_start) * 1000,
                        attempts=attempts,
                        provider_status="success",
                    )
            except urllib.error.HTTPError as error:
                body_text = error.read().decode("utf-8", errors="replace")
                attempts.append(
                    {
                        "attempt": attempt_number,
                        "request_timestamp_utc": request_time,
                        "response_timestamp_utc": utc_now(),
                        "http_status": error.code,
                        "error": body_text,
                    }
                )
                retryable = error.code == 429 or error.code >= 500
                if retryable and attempt_number <= self.retry_count:
                    retry_after = error.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after and retry_after.replace(".", "", 1).isdigit() else min(2**attempt_number, 8)
                    time.sleep(delay)
                    continue
                break
            except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError) as error:
                attempts.append(
                    {
                        "attempt": attempt_number,
                        "request_timestamp_utc": request_time,
                        "response_timestamp_utc": utc_now(),
                        "http_status": None,
                        "error": repr(error),
                    }
                )
                if attempt_number <= self.retry_count:
                    time.sleep(min(2**attempt_number, 8))
                    continue
                break

        return GenerationResult(
            raw_text="",
            raw_provider_response=None,
            finish_reason=None,
            usage={},
            latency_ms=(time.perf_counter() - total_start) * 1000,
            attempts=attempts,
            provider_status="provider_error",
        )
