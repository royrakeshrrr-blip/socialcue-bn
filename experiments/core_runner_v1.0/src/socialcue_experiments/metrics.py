from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .schema import DatasetRow, REGISTERS


ORDER = {"TUI": 0, "TUMI": 1, "APNI": 2}
PARSEABLE = {"valid", "recoverable_format", "recoverable_missing_metadata"}


def load_raw_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            request_id = record.get("request_id")
            if not request_id:
                raise ValueError(f"Line {line_number} has no request_id.")
            if request_id in seen:
                raise ValueError(f"Duplicate request_id: {request_id}")
            seen.add(request_id)
            records.append(record)
    return records


def _macro_f1(gold: list[str], predicted: list[str | None]) -> float:
    scores: list[float] = []
    for label in REGISTERS:
        true_positive = sum(g == label and p == label for g, p in zip(gold, predicted))
        false_positive = sum(g != label and p == label for g, p in zip(gold, predicted))
        false_negative = sum(g == label and p != label for g, p in zip(gold, predicted))
        denominator = 2 * true_positive + false_positive + false_negative
        scores.append(0.0 if denominator == 0 else (2 * true_positive) / denominator)
    return mean(scores)


def _counterfactual_score(rows: list[DatasetRow], predictions: dict[str, str | None]) -> dict[str, Any]:
    families: dict[str, dict[str, DatasetRow]] = defaultdict(dict)
    for row in rows:
        families[row.message_family_id][row.variant] = row
    matched = 0
    evaluable = 0
    missing = 0
    for family in families.values():
        if set(family) != {"A", "B", "C"}:
            continue
        for target in ("B", "C"):
            a = family["A"]
            other = family[target]
            prediction_a = predictions.get(a.instance_id)
            prediction_other = predictions.get(other.instance_id)
            if prediction_a is None or prediction_other is None:
                missing += 1
                continue
            expected_change = a.primary_register != other.primary_register
            observed_change = prediction_a != prediction_other
            evaluable += 1
            matched += expected_change == observed_change
    return {
        "matched_pairs": matched,
        "evaluable_pairs": evaluable,
        "missing_pairs": missing,
        "direction_accuracy": None if evaluable == 0 else matched / evaluable,
    }


def score_group(rows: list[DatasetRow], records: list[dict[str, Any]]) -> dict[str, Any]:
    row_by_id = {row.instance_id: row for row in rows}
    predictions: dict[str, str | None] = {}
    parse_status_counts: dict[str, int] = defaultdict(int)
    confusion = {gold: {prediction: 0 for prediction in REGISTERS} for gold in REGISTERS}
    gold_labels: list[str] = []
    predicted_labels: list[str | None] = []
    primary_correct = 0
    acceptable_correct = 0
    over_polite = 0
    under_polite = 0
    latencies: list[float] = []

    for record in records:
        instance_id = record["input"]["instance_id"]
        row = row_by_id.get(instance_id)
        if row is None:
            raise ValueError(f"Raw result references unknown instance: {instance_id}")
        parsed = record.get("parsed") or {}
        status = parsed.get("parse_status", "missing")
        parse_status_counts[status] += 1
        prediction = parsed.get("register") if status in PARSEABLE else None
        predictions[instance_id] = prediction
        gold_labels.append(row.primary_register)
        predicted_labels.append(prediction)
        if prediction is not None:
            confusion[row.primary_register][prediction] += 1
            primary_correct += prediction == row.primary_register
            acceptable_correct += prediction in row.acceptable_set
            acceptable_orders = [ORDER[label] for label in row.acceptable_set]
            if ORDER[prediction] > max(acceptable_orders):
                over_polite += 1
            elif ORDER[prediction] < min(acceptable_orders):
                under_polite += 1
        latency = (record.get("generation") or {}).get("latency_ms")
        if isinstance(latency, (int, float)):
            latencies.append(float(latency))

    total = len(records)
    parseable = sum(prediction is not None for prediction in predicted_labels)
    exact_schema = parse_status_counts.get("valid", 0)
    observed_ids = set(predictions)
    observed_rows = [row for row in rows if row.instance_id in observed_ids]
    return {
        "records": total,
        "parseable_records": parseable,
        "parseable_rate": 0.0 if total == 0 else parseable / total,
        "exact_schema_rate": 0.0 if total == 0 else exact_schema / total,
        "primary_accuracy": 0.0 if total == 0 else primary_correct / total,
        "acceptable_set_accuracy": 0.0 if total == 0 else acceptable_correct / total,
        "macro_f1_primary": _macro_f1(gold_labels, predicted_labels),
        "over_polite_errors": over_polite,
        "under_polite_errors": under_polite,
        "mean_latency_ms": None if not latencies else mean(latencies),
        "parse_status_counts": dict(sorted(parse_status_counts.items())),
        "confusion_matrix": confusion,
        "counterfactual": _counterfactual_score(observed_rows, predictions),
    }


def score_records(rows: list[DatasetRow], records: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    seen_predictions: set[tuple[str, str, str]] = set()
    for record in records:
        group_key = (record["model_key"], record["prompt_condition"])
        prediction_key = (*group_key, record["input"]["instance_id"])
        if prediction_key in seen_predictions:
            raise ValueError(
                "Duplicate model-condition-instance result: " + "::".join(prediction_key)
            )
        seen_predictions.add(prediction_key)
        groups[group_key].append(record)
    output: dict[str, Any] = {}
    for (model_key, condition), group_records in sorted(groups.items()):
        output[f"{model_key}::{condition}"] = {
            "model_key": model_key,
            "prompt_condition": condition,
            **score_group(rows, group_records),
        }
    return output
