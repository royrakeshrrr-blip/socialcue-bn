from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models.dummy import DummyAdapter
from .models.openai_compatible import OpenAICompatibleAdapter
from .parser import parse_response
from .prompts import render_prompt, sha256_text
from .schema import DatasetRow, load_dataset


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PACKAGE_ROOT / "config" / "experiment.json"
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{1,80}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def select_model(config: dict[str, Any], key: str) -> dict[str, Any]:
    matches = [model for model in config["models"] if model["key"] == key]
    if len(matches) != 1:
        raise ValueError(f"Unknown or duplicate model key: {key}")
    return matches[0]


def build_adapter(model: dict[str, Any], config: dict[str, Any]):
    if model["provider"] == "dummy":
        return DummyAdapter()
    api_key_env = model["api_key_env"]
    api_key = os.environ.get(api_key_env, "").strip()
    if not api_key:
        raise ValueError(f"Missing API key. Set the {api_key_env} environment variable first.")
    return OpenAICompatibleAdapter(
        endpoint=model["endpoint"],
        api_key=api_key,
        model_id=model["model_id"],
        temperature=float(config["temperature"]),
        max_output_tokens=int(config["max_output_tokens"]),
        retry_count=int(config["retry_count"]),
        timeout_seconds=int(config["request_timeout_seconds"]),
        provider_parameters=model.get("provider_parameters") or {},
        include_temperature=bool(model.get("include_temperature", True)),
    )


def input_snapshot(row: DatasetRow) -> dict[str, str]:
    return {
        "instance_id": row.instance_id,
        "message_family_id": row.message_family_id,
        "variant": row.variant,
        "romanized_message": row.romanized_message,
        "domain": row.domain,
        "intent": row.intent,
        "speaker_role": row.speaker_role,
        "recipient_role": row.recipient_role,
        "authority_relation": row.authority_relation,
        "relative_age": row.relative_age,
        "familiarity": row.familiarity,
        "setting": row.setting,
        "changed_cue_from_A": row.changed_cue_from_A,
        "split": row.split,
    }


def existing_request_ids(output_path: Path) -> set[str]:
    if not output_path.exists():
        return set()
    ids: set[str] = set()
    with output_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Malformed existing JSONL line {line_number}: {error}") from error
            request_id = record.get("request_id")
            if request_id in ids:
                raise ValueError(f"Duplicate request_id in existing output: {request_id}")
            ids.add(request_id)
    return ids


def record_provider_failure(
    *,
    output_path: Path,
    request_id: str,
    experiment_id: str,
    model: dict[str, Any],
    condition: str,
    row: DatasetRow,
    result: Any,
) -> Path:
    """Keep transient API failures separate so a resumed run retries them."""
    error_path = output_path.with_name(output_path.stem + ".errors.jsonl")
    failure = {
        "error_schema": "SOCIALCUE-CORE-PROVIDER-ERROR-V1.0",
        "request_id": request_id,
        "experiment_id": experiment_id,
        "timestamp_utc": utc_now(),
        "model_key": model["key"],
        "provider": model["provider"],
        "model_id": model["model_id"],
        "prompt_condition": condition,
        "input": input_snapshot(row),
        "generation": result.to_dict(),
    }
    with error_path.open("a", encoding="utf-8", newline="\n") as error_file:
        error_file.write(json.dumps(failure, ensure_ascii=False, sort_keys=True) + "\n")
    return error_path


def run_experiment(
    *,
    dataset_path: Path,
    config_path: Path,
    model_key: str,
    condition_value: str,
    split_value: str,
    run_id: str,
    ids_file: Path | None,
    limit: int | None,
    output_path: Path,
    allow_test: bool,
) -> Path:
    if not SAFE_ID.fullmatch(run_id):
        raise ValueError("run_id must contain only letters, numbers, dots, underscores, and hyphens.")
    split_value = split_value.upper()
    if split_value == "TEST" and not allow_test:
        raise ValueError("TEST is locked. Re-run with --allow-test only after prompts and models are frozen.")

    config = load_config(config_path)
    model = select_model(config, model_key)
    conditions = config["conditions"] if condition_value == "ALL" else [condition_value]
    unknown = sorted(set(conditions) - set(config["conditions"]))
    if unknown:
        raise ValueError("Unknown prompt condition(s): " + ", ".join(unknown))

    rows = [row for row in load_dataset(dataset_path) if row.split == split_value]
    rows.sort(key=lambda row: row.instance_id)
    if not rows:
        raise ValueError(f"Dataset contains no {split_value} rows.")
    if ids_file is not None:
        requested_ids = [
            line.strip()
            for line in ids_file.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        if len(requested_ids) != len(set(requested_ids)):
            raise ValueError(f"Duplicate IDs found in {ids_file}.")
        row_by_id = {row.instance_id: row for row in rows}
        unknown_ids = [instance_id for instance_id in requested_ids if instance_id not in row_by_id]
        if unknown_ids:
            raise ValueError(
                f"IDs are absent from the selected {split_value} split: " + ", ".join(unknown_ids)
            )
        rows = [row_by_id[instance_id] for instance_id in requested_ids]
        if not rows:
            raise ValueError(f"ID file is empty: {ids_file}")
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be positive.")
        rows = rows[:limit]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed = existing_request_ids(output_path)
    adapter = build_adapter(model, config)
    delay_seconds = float(model.get("request_delay_seconds", config["request_delay_seconds"]))
    dataset_hash = sha256_file(dataset_path)
    config_hash = sha256_file(config_path)
    experiment_id = f"{config['protocol_version']}::{model_key}::{condition_value}::{split_value}::{run_id}"
    planned = len(rows) * len(conditions)
    remaining = 0
    for row in rows:
        for condition in conditions:
            request_id = f"{run_id}::{model_key}::{condition}::{row.instance_id}"
            if request_id not in completed:
                remaining += 1

    print(f"Experiment: {experiment_id}")
    print(f"Instances: {len(rows)} | Conditions: {len(conditions)} | Planned records: {planned}")
    print(f"Already complete: {planned - remaining} | Remaining: {remaining}")
    print(f"Output: {output_path}")
    if remaining == 0:
        print("PASS: Nothing to do; every planned request is already recorded.")
        return output_path

    written = 0
    with output_path.open("a", encoding="utf-8", newline="\n") as output_file:
        for row in rows:
            for condition in conditions:
                request_id = f"{run_id}::{model_key}::{condition}::{row.instance_id}"
                if request_id in completed:
                    continue
                system_prompt, user_prompt = render_prompt(row, condition)
                request_timestamp = utc_now()
                result = adapter.generate(system_prompt, user_prompt)
                response_timestamp = utc_now()
                if result.provider_status != "success":
                    error_path = record_provider_failure(
                        output_path=output_path,
                        request_id=request_id,
                        experiment_id=experiment_id,
                        model=model,
                        condition=condition,
                        row=row,
                        result=result,
                    )
                    raise RuntimeError(
                        "Provider request failed after retries. "
                        f"The batch stopped safely; details are in {error_path}. "
                        "Run the same command later to resume from this request."
                    )
                parsed = parse_response(result.raw_text)
                parsed_payload = parsed.to_dict()
                record = {
                    "raw_result_schema": "SOCIALCUE-CORE-RAW-V1.0",
                    "request_id": request_id,
                    "experiment_id": experiment_id,
                    "run_id": run_id,
                    "request_timestamp_utc": request_timestamp,
                    "response_timestamp_utc": response_timestamp,
                    "dataset_path": str(dataset_path),
                    "dataset_sha256": dataset_hash,
                    "selection_ids_file": None if ids_file is None else str(ids_file),
                    "selection_ids_sha256": None if ids_file is None else sha256_file(ids_file),
                    "dataset_version": config["dataset_version"],
                    "config_sha256": config_hash,
                    "model_key": model_key,
                    "provider": model["provider"],
                    "model_id": model["model_id"],
                    "prompt_condition": condition,
                    "prompt_version": config["prompt_version"],
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "prompt_sha256": sha256_text(system_prompt + "\n\n" + user_prompt),
                    "request_parameters": {
                        "temperature": (
                            config["temperature"]
                            if model.get("include_temperature", True)
                            else None
                        ),
                        "temperature_source": (
                            "explicit"
                            if model.get("include_temperature", True)
                            else "provider_default"
                        ),
                        "max_output_tokens": config["max_output_tokens"],
                        "retry_count": config["retry_count"],
                        "request_delay_seconds": delay_seconds,
                        "provider_parameters": model.get("provider_parameters") or {},
                    },
                    "input": input_snapshot(row),
                    "generation": result.to_dict(),
                    "parsed": parsed_payload,
                }
                output_file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                output_file.flush()
                written += 1
                if written % 25 == 0 or written == remaining:
                    print(f"Recorded {written}/{remaining} new responses.")
                if model["provider"] != "dummy" and delay_seconds > 0:
                    time.sleep(delay_seconds)

    print(f"PASS: Wrote {written} new immutable raw records.")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a resumable SocialCue-BN core experiment batch.")
    parser.add_argument("--dataset", type=Path, default=PACKAGE_ROOT / "data" / "socialcue_bn_gold_v1.0.csv")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", required=True, help="Model key from config/experiment.json")
    parser.add_argument("--condition", default="ALL", help="P0..., P1..., P2..., or ALL")
    parser.add_argument("--split", default="DEVELOPMENT", choices=["DEVELOPMENT", "TEST"])
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--ids-file", type=Path, help="Optional ordered list of instance IDs to run")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-test", action="store_true")
    args = parser.parse_args()
    output = args.output or PACKAGE_ROOT / "results" / "raw" / f"{args.run_id}.jsonl"
    try:
        run_experiment(
            dataset_path=args.dataset,
            config_path=args.config,
            model_key=args.model,
            condition_value=args.condition,
            split_value=args.split,
            run_id=args.run_id,
            ids_file=args.ids_file,
            limit=args.limit,
            output_path=output,
            allow_test=args.allow_test,
        )
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
