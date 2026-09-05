from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from socialcue_experiments.metrics import PARSEABLE, load_raw_records, score_records
from socialcue_experiments.schema import load_dataset


MODELS = (
    ("gemini_3_5_flash_lite", "Gemini 3.5 Flash-Lite"),
    ("groq_gpt_oss_120b", "GPT-OSS 120B"),
    ("groq_qwen_3_8_27b", "Qwen 3.8 27B"),
)

CONDITIONS = (
    ("P0_MESSAGE_ONLY", "P0 Message Only"),
    ("P1_NARRATIVE_CONTEXT", "P1 Narrative Context"),
    ("P2_STRUCTURED_CONTEXT", "P2 Structured Context"),
)

MODEL_NAMES = dict(MODELS)
CONDITION_NAMES = dict(CONDITIONS)
REGISTERS = ("TUI", "TUMI", "APNI")
COLORS = {
    "gemini_3_5_flash_lite": "#2563eb",
    "groq_gpt_oss_120b": "#ea580c",
    "groq_qwen_3_8_27b": "#16a34a",
}
SAFE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{1,80}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def numeric(value: Any) -> float:
    return float(value) if isinstance(value, (int, float)) else 0.0


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def select_rows(
    dataset_rows: list[Any],
    split: str,
    instances: int,
    ids_file: Path | None,
) -> list[Any]:
    rows = sorted(
        (row for row in dataset_rows if row.split == split),
        key=lambda row: row.instance_id,
    )
    if not rows:
        raise ValueError(f"The dataset contains no {split} rows.")

    row_by_id = {row.instance_id: row for row in rows}
    if ids_file is None:
        selected = rows[:instances]
    else:
        requested = [
            line.strip()
            for line in ids_file.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        if len(requested) != len(set(requested)):
            raise ValueError(f"Duplicate IDs found in {ids_file}.")
        missing = [instance_id for instance_id in requested if instance_id not in row_by_id]
        if missing:
            raise ValueError("IDs missing from the selected split: " + ", ".join(missing))
        selected = [row_by_id[instance_id] for instance_id in requested]

    if len(selected) != instances:
        raise ValueError(
            f"Expected {instances} selected instances but found {len(selected)}."
        )

    if split == "TEST":
        families: dict[str, set[str]] = defaultdict(set)
        for row in selected:
            families[row.message_family_id].add(row.variant)
        incomplete = {
            family_id: sorted(variants)
            for family_id, variants in families.items()
            if variants != {"A", "B", "C"}
        }
        if incomplete:
            raise ValueError(
                "The selected TEST range cuts an A/B/C family. "
                "Use an instance count divisible by three."
            )
    return selected


def validate_and_select_records(
    path: Path,
    expected_model: str,
    split: str,
    selected_ids: set[str],
    dataset_hash: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    records = load_raw_records(path)
    warnings: list[str] = []
    chosen = [
        record
        for record in records
        if (record.get("input") or {}).get("split") == split
        and (record.get("input") or {}).get("instance_id") in selected_ids
    ]

    wrong_model = sorted({record.get("model_key") for record in chosen} - {expected_model})
    if wrong_model:
        raise ValueError(f"{path.name} contains unexpected model keys: {wrong_model}")

    seen: set[tuple[str, str]] = set()
    coverage: dict[str, set[str]] = defaultdict(set)
    for record in chosen:
        condition = record.get("prompt_condition")
        instance_id = (record.get("input") or {}).get("instance_id")
        key = (condition, instance_id)
        if key in seen:
            raise ValueError(
                f"Duplicate model-condition-instance record in {path.name}: {key}"
            )
        seen.add(key)
        coverage[condition].add(instance_id)
        provider_status = (record.get("generation") or {}).get("provider_status")
        if provider_status != "success":
            raise ValueError(
                f"Non-success provider record in {path.name}: {record.get('request_id')}"
            )

    for condition, _ in CONDITIONS:
        missing = selected_ids - coverage.get(condition, set())
        extra = coverage.get(condition, set()) - selected_ids
        if missing or extra:
            raise ValueError(
                f"Coverage failure for {expected_model}/{condition}: "
                f"missing={len(missing)}, extra={len(extra)}"
            )

    expected_count = len(selected_ids) * len(CONDITIONS)
    if len(chosen) != expected_count:
        raise ValueError(
            f"Expected {expected_count} selected records in {path.name}, found {len(chosen)}."
        )

    hashes = sorted({record.get("dataset_sha256") for record in chosen})
    if hashes != [dataset_hash]:
        raise ValueError(
            f"Dataset SHA-256 mismatch in {path.name}. Expected {dataset_hash}; found {hashes}."
        )

    config_hashes = sorted({record.get("config_sha256") for record in chosen})
    if len(config_hashes) != 1:
        warnings.append(
            f"{path.name} contains {len(config_hashes)} config hashes: "
            + ", ".join(str(value) for value in config_hashes)
        )
    return chosen, warnings


def metric_rows(
    scores: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records_by_group: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        records_by_group[(record["model_key"], record["prompt_condition"])].append(record)

    output: list[dict[str, Any]] = []
    for model_key, _ in MODELS:
        for condition, _ in CONDITIONS:
            score = scores[f"{model_key}::{condition}"]
            group = records_by_group[(model_key, condition)]
            prompt_tokens = sum(
                numeric((record.get("generation") or {}).get("usage", {}).get("prompt_tokens"))
                for record in group
            )
            completion_tokens = sum(
                numeric((record.get("generation") or {}).get("usage", {}).get("completion_tokens"))
                for record in group
            )
            total_tokens = sum(
                numeric((record.get("generation") or {}).get("usage", {}).get("total_tokens"))
                for record in group
            )
            output.append(
                {
                    "model_key": model_key,
                    "model_name": MODEL_NAMES[model_key],
                    "prompt_condition": condition,
                    "prompt_name": CONDITION_NAMES[condition],
                    "records": score["records"],
                    "parseable_rate": score["parseable_rate"],
                    "exact_schema_rate": score["exact_schema_rate"],
                    "primary_accuracy": score["primary_accuracy"],
                    "acceptable_set_accuracy": score["acceptable_set_accuracy"],
                    "macro_f1_primary": score["macro_f1_primary"],
                    "over_polite_errors": score["over_polite_errors"],
                    "under_polite_errors": score["under_polite_errors"],
                    "mean_latency_ms": score["mean_latency_ms"],
                    "counterfactual_direction_accuracy": score["counterfactual"][
                        "direction_accuracy"
                    ],
                    "counterfactual_matched_pairs": score["counterfactual"]["matched_pairs"],
                    "counterfactual_evaluable_pairs": score["counterfactual"][
                        "evaluable_pairs"
                    ],
                    "prompt_tokens": int(prompt_tokens),
                    "completion_tokens": int(completion_tokens),
                    "total_tokens": int(total_tokens),
                }
            )
    return output


def prediction_rows(
    dataset_rows: list[Any], records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    row_by_id = {row.instance_id: row for row in dataset_rows}
    output: list[dict[str, Any]] = []
    for record in sorted(
        records,
        key=lambda value: (
            value["model_key"],
            value["prompt_condition"],
            value["input"]["instance_id"],
        ),
    ):
        instance_id = record["input"]["instance_id"]
        gold = row_by_id[instance_id]
        parsed = record.get("parsed") or {}
        status = parsed.get("parse_status", "missing")
        prediction = parsed.get("register") if status in PARSEABLE else None
        usage = (record.get("generation") or {}).get("usage") or {}
        reasons = parsed.get("reason_codes") or []
        output.append(
            {
                "instance_id": instance_id,
                "message_family_id": gold.message_family_id,
                "variant": gold.variant,
                "model_key": record["model_key"],
                "prompt_condition": record["prompt_condition"],
                "gold_primary": gold.primary_register,
                "gold_acceptable": "|".join(gold.acceptable_set),
                "predicted_register": prediction or "",
                "primary_correct": prediction == gold.primary_register,
                "acceptable_correct": prediction in gold.acceptable_set if prediction else False,
                "parse_status": status,
                "predicted_confidence": parsed.get("confidence") or "",
                "predicted_reason_codes": "|".join(reasons),
                "latency_ms": (record.get("generation") or {}).get("latency_ms"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "request_id": record.get("request_id"),
            }
        )
    return output


def confusion_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str, str, str]] = Counter()
    for row in predictions:
        predicted = row["predicted_register"] or "UNPARSEABLE"
        counts[
            (
                row["model_key"],
                row["prompt_condition"],
                row["gold_primary"],
                predicted,
            )
        ] += 1
    output: list[dict[str, Any]] = []
    for model_key, _ in MODELS:
        for condition, _ in CONDITIONS:
            for gold in REGISTERS:
                for predicted in (*REGISTERS, "UNPARSEABLE"):
                    output.append(
                        {
                            "model_key": model_key,
                            "prompt_condition": condition,
                            "gold_register": gold,
                            "predicted_register": predicted,
                            "count": counts[(model_key, condition, gold, predicted)],
                        }
                    )
    return output


def svg_bar_chart(
    path: Path,
    rows: list[dict[str, Any]],
    metric: str,
    title: str,
    percent: bool,
) -> None:
    width, height = 1080, 640
    left, right, top, bottom = 90, 35, 90, 115
    plot_width = width - left - right
    plot_height = height - top - bottom
    values = [numeric(row.get(metric)) for row in rows]
    maximum = 1.0 if percent else max(values + [1.0]) * 1.10
    group_width = plot_width / len(CONDITIONS)
    bar_width = min(72.0, group_width / 5.0)
    gap = 12.0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111827}.title{font-size:25px;font-weight:700}.axis{font-size:14px}.label{font-size:13px}.legend{font-size:14px}</style>',
        f'<text x="{width/2}" y="42" text-anchor="middle" class="title">{html.escape(title)}</text>',
    ]

    for index in range(6):
        ratio = index / 5
        y = top + plot_height - ratio * plot_height
        value = ratio * maximum
        label = f"{value * 100:.0f}%" if percent else f"{value:.0f}"
        parts.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" stroke="#e5e7eb" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left-12}" y="{y+5:.2f}" text-anchor="end" class="axis">{label}</text>'
        )

    indexed = {(row["model_key"], row["prompt_condition"]): row for row in rows}
    for group_index, (condition, condition_name) in enumerate(CONDITIONS):
        center = left + group_width * (group_index + 0.5)
        total_bars = len(MODELS) * bar_width + (len(MODELS) - 1) * gap
        start = center - total_bars / 2
        for model_index, (model_key, _) in enumerate(MODELS):
            row = indexed[(model_key, condition)]
            value = numeric(row.get(metric))
            bar_height = 0.0 if maximum == 0 else value / maximum * plot_height
            x = start + model_index * (bar_width + gap)
            y = top + plot_height - bar_height
            value_label = f"{value * 100:.1f}%" if percent else f"{value:.0f}"
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" rx="3" fill="{COLORS[model_key]}"/>'
            )
            parts.append(
                f'<text x="{x + bar_width/2:.2f}" y="{max(top+13, y-7):.2f}" text-anchor="middle" class="label">{value_label}</text>'
            )
        parts.append(
            f'<text x="{center:.2f}" y="{top+plot_height+30}" text-anchor="middle" class="axis">{html.escape(condition_name)}</text>'
        )

    legend_y = height - 35
    legend_start = 150
    legend_spacing = 275
    for index, (model_key, model_name) in enumerate(MODELS):
        x = legend_start + index * legend_spacing
        parts.append(
            f'<rect x="{x}" y="{legend_y-14}" width="18" height="18" rx="2" fill="{COLORS[model_key]}"/>'
        )
        parts.append(
            f'<text x="{x+27}" y="{legend_y}" class="legend">{html.escape(model_name)}</text>'
        )

    parts.append(
        f'<line x1="{left}" y1="{top+plot_height}" x2="{width-right}" y2="{top+plot_height}" stroke="#111827" stroke-width="1.5"/>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Model | Prompt | Primary accuracy | Acceptable-set accuracy | Macro-F1 | Counterfactual accuracy | Parseable | Mean latency (ms) | Total tokens |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        counterfactual = row["counterfactual_direction_accuracy"]
        counterfactual_text = (
            "N/A" if counterfactual is None else f"{counterfactual * 100:.1f}%"
        )
        lines.append(
            "| {model} | {prompt} | {primary:.1f}% | {acceptable:.1f}% | "
            "{macro:.3f} | {counterfactual} | {parseable:.1f}% | {latency:.1f} | {tokens} |".format(
                model=row["model_name"],
                prompt=row["prompt_name"],
                primary=row["primary_accuracy"] * 100,
                acceptable=row["acceptable_set_accuracy"] * 100,
                macro=row["macro_f1_primary"],
                counterfactual=counterfactual_text,
                parseable=row["parseable_rate"] * 100,
                latency=numeric(row["mean_latency_ms"]),
                tokens=row["total_tokens"],
            )
        )
    return "\n".join(lines)


def html_table(rows: list[dict[str, Any]]) -> str:
    body: list[str] = []
    for row in rows:
        cf = row["counterfactual_direction_accuracy"]
        body.append(
            "<tr>"
            f"<td>{html.escape(row['model_name'])}</td>"
            f"<td>{html.escape(row['prompt_name'])}</td>"
            f"<td>{row['primary_accuracy']*100:.1f}%</td>"
            f"<td>{row['acceptable_set_accuracy']*100:.1f}%</td>"
            f"<td>{row['macro_f1_primary']:.3f}</td>"
            f"<td>{'N/A' if cf is None else f'{cf*100:.1f}%'}</td>"
            f"<td>{row['parseable_rate']*100:.1f}%</td>"
            f"<td>{numeric(row['mean_latency_ms']):.1f}</td>"
            f"<td>{row['total_tokens']}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Model</th><th>Prompt</th><th>Primary accuracy</th>"
        "<th>Acceptable-set accuracy</th><th>Macro-F1</th><th>Counterfactual accuracy</th>"
        "<th>Parseable</th><th>Mean latency (ms)</th><th>Total tokens</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table>"
    )


def build_reports(
    output_dir: Path,
    label: str,
    split: str,
    instances: int,
    generated_at: str,
    metrics: list[dict[str, Any]],
    warnings: list[str],
) -> None:
    preliminary = "PRELIMINARY" in label.upper()
    status = "PRELIMINARY — NOT FINAL THESIS RESULTS" if preliminary else "FINAL"
    table_md = markdown_table(metrics)
    warning_lines = [f"- {warning}" for warning in warnings] or ["- None"]
    report_md = f"""# SocialCue-BN Core Experiment Report — {label}

**Status:** {status}  
**Split:** {split}  
**Unique instances per model:** {instances}  
**Prompt conditions:** 3  
**Models:** 3  
**Total evaluated records:** {instances * 3 * 3}  
**Generated at:** {generated_at}

## Interpretation Rule

This report was generated automatically from immutable JSONL outputs and the frozen gold benchmark. {'Do not present these values as final thesis results.' if preliminary else 'These values represent the complete requested evaluation scope.'}

## Combined Performance Table

{table_md}

## Figures

![Primary accuracy](figure_primary_accuracy.svg)

![Acceptable-set accuracy](figure_acceptable_set_accuracy.svg)

![Macro-F1](figure_macro_f1.svg)

![Counterfactual direction accuracy](figure_counterfactual_accuracy.svg)

## Validation Warnings

{chr(10).join(warning_lines)}

## Generated Files

- `combined_metrics.csv`
- `combined_metrics.json`
- `predictions_long.csv`
- `error_cases.csv`
- `confusion_matrices.csv`
- `run_manifest.json`
- four SVG figures
- this Markdown report and `report.html`
"""
    (output_dir / "report.md").write_text(report_md, encoding="utf-8")

    warning_html = "".join(f"<li>{html.escape(item)}</li>" for item in warnings) or "<li>None</li>"
    badge_class = "preliminary" if preliminary else "final"
    report_html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SocialCue-BN — {html.escape(label)}</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f3f4f6;color:#111827}}
main{{max-width:1180px;margin:32px auto;background:white;padding:36px;border-radius:14px;box-shadow:0 3px 18px #0001}}
h1{{margin-top:0}} .badge{{display:inline-block;padding:7px 11px;border-radius:999px;font-weight:700}}
.preliminary{{background:#fef3c7;color:#92400e}} .final{{background:#dcfce7;color:#166534}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:22px 0}}
.card{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:9px;padding:13px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{border:1px solid #d1d5db;padding:9px;text-align:right}}
th{{background:#111827;color:white}} td:first-child,td:nth-child(2),th:first-child,th:nth-child(2){{text-align:left}}
img{{width:100%;max-width:1080px;border:1px solid #e5e7eb;margin:18px 0}}
.note{{border-left:5px solid #2563eb;background:#eff6ff;padding:14px}}
</style></head><body><main>
<h1>SocialCue-BN Core Experiment Report</h1><h2>{html.escape(label)}</h2>
<span class="badge {badge_class}">{html.escape(status)}</span>
<div class="meta"><div class="card"><b>Split</b><br>{split}</div><div class="card"><b>Instances per model</b><br>{instances}</div>
<div class="card"><b>Total evaluated records</b><br>{instances*9}</div><div class="card"><b>Generated</b><br>{html.escape(generated_at)}</div></div>
<p class="note">This report was generated automatically from immutable JSONL outputs and the frozen gold benchmark. {'Do not present these values as final thesis results.' if preliminary else 'This is the complete requested evaluation report.'}</p>
<h2>Combined performance</h2>{html_table(metrics)}
<h2>Figures</h2>
<img src="figure_primary_accuracy.svg" alt="Primary accuracy"><img src="figure_acceptable_set_accuracy.svg" alt="Acceptable-set accuracy">
<img src="figure_macro_f1.svg" alt="Macro-F1"><img src="figure_counterfactual_accuracy.svg" alt="Counterfactual direction accuracy">
<h2>Validation warnings</h2><ul>{warning_html}</ul>
</main></body></html>"""
    (output_dir / "report.html").write_text(report_html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate reproducible SocialCue-BN tables, figures, and reports."
    )
    parser.add_argument("--instances", type=int, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--split", choices=["DEVELOPMENT", "TEST"], default="TEST")
    parser.add_argument("--ids-file", type=Path)
    parser.add_argument(
        "--dataset", type=Path, default=ROOT / "data" / "socialcue_bn_gold_v1.0.csv"
    )
    parser.add_argument(
        "--gemini",
        type=Path,
        default=ROOT / "results" / "raw" / "test_gemini_3_5_flash_lite.jsonl",
    )
    parser.add_argument(
        "--gpt-oss",
        type=Path,
        default=ROOT / "results" / "raw" / "test_groq_gpt_oss_120b.jsonl",
    )
    parser.add_argument(
        "--qwen",
        type=Path,
        default=ROOT / "results" / "raw" / "test_groq_qwen_3_8_27b.jsonl",
    )
    parser.add_argument(
        "--output-root", type=Path, default=ROOT / "results" / "reports"
    )
    args = parser.parse_args()

    if args.instances < 1:
        print("FAIL: --instances must be positive.")
        return 1
    if not SAFE_LABEL.fullmatch(args.label):
        print("FAIL: --label may contain only letters, numbers, dots, underscores and hyphens.")
        return 1

    try:
        dataset_rows = load_dataset(args.dataset)
        selected_rows = select_rows(
            dataset_rows, args.split, args.instances, args.ids_file
        )
        selected_ids = {row.instance_id for row in selected_rows}
        dataset_hash = sha256_file(args.dataset)
        input_paths = {
            "gemini_3_5_flash_lite": args.gemini,
            "groq_gpt_oss_120b": args.gpt_oss,
            "groq_qwen_3_8_27b": args.qwen,
        }
        all_records: list[dict[str, Any]] = []
        warnings: list[str] = []
        for model_key, _ in MODELS:
            chosen, model_warnings = validate_and_select_records(
                input_paths[model_key], model_key, args.split, selected_ids, dataset_hash
            )
            all_records.extend(chosen)
            warnings.extend(model_warnings)

        scores = score_records(selected_rows, all_records)
        metrics = metric_rows(scores, all_records)
        predictions = prediction_rows(selected_rows, all_records)
        errors = [row for row in predictions if not row["primary_correct"]]
        confusions = confusion_rows(predictions)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1

    output_dir = args.output_root / args.label
    output_dir.mkdir(parents=True, exist_ok=True)

    metric_fields = list(metrics[0])
    write_csv(output_dir / "combined_metrics.csv", metric_fields, metrics)
    (output_dir / "combined_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    prediction_fields = list(predictions[0])
    write_csv(output_dir / "predictions_long.csv", prediction_fields, predictions)
    write_csv(output_dir / "error_cases.csv", prediction_fields, errors)
    write_csv(
        output_dir / "confusion_matrices.csv",
        ["model_key", "prompt_condition", "gold_register", "predicted_register", "count"],
        confusions,
    )

    svg_bar_chart(
        output_dir / "figure_primary_accuracy.svg",
        metrics,
        "primary_accuracy",
        "Primary-register accuracy by model and prompt",
        True,
    )
    svg_bar_chart(
        output_dir / "figure_acceptable_set_accuracy.svg",
        metrics,
        "acceptable_set_accuracy",
        "Acceptable-set accuracy by model and prompt",
        True,
    )
    svg_bar_chart(
        output_dir / "figure_macro_f1.svg",
        metrics,
        "macro_f1_primary",
        "Macro-F1 by model and prompt",
        True,
    )
    svg_bar_chart(
        output_dir / "figure_counterfactual_accuracy.svg",
        metrics,
        "counterfactual_direction_accuracy",
        "Counterfactual direction accuracy by model and prompt",
        True,
    )

    generated_at = utc_now()
    config_hashes = sorted({record.get("config_sha256") for record in all_records})
    prompt_versions = sorted({record.get("prompt_version") for record in all_records})
    parse_statuses = dict(
        sorted(Counter((record.get("parsed") or {}).get("parse_status", "missing") for record in all_records).items())
    )
    manifest = {
        "report_schema": "SOCIALCUE-CORE-REPORT-V1.0",
        "label": args.label,
        "status": "PRELIMINARY" if "PRELIMINARY" in args.label.upper() else "FINAL",
        "generated_at_utc": generated_at,
        "split": args.split,
        "instances_per_model": args.instances,
        "conditions": [condition for condition, _ in CONDITIONS],
        "models": [model_key for model_key, _ in MODELS],
        "total_records": len(all_records),
        "selected_instance_ids_sha256": sha256_text("\n".join(sorted(selected_ids)) + "\n"),
        "dataset_path": str(args.dataset),
        "dataset_sha256": dataset_hash,
        "input_files": {
            model_key: {
                "path": str(path),
                "sha256": sha256_file(path),
            }
            for model_key, path in input_paths.items()
        },
        "config_sha256_values": config_hashes,
        "prompt_versions": prompt_versions,
        "parse_status_counts": parse_statuses,
        "validation_warnings": warnings,
    }
    (output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    build_reports(
        output_dir,
        args.label,
        args.split,
        args.instances,
        generated_at,
        metrics,
        warnings,
    )

    print(
        f"PASS: Generated {args.label} from {args.instances} {args.split} instances "
        f"for 3 prompts and 3 models ({len(all_records)} records)."
    )
    print(f"PASS: Parse statuses: {parse_statuses}")
    print(f"Report: {output_dir / 'report.html'}")
    print(f"Table: {output_dir / 'combined_metrics.csv'}")
    print(f"Figures: {output_dir / 'figure_primary_accuracy.svg'} and 3 more")
    if warnings:
        print(f"WARNING: {len(warnings)} provenance warning(s) recorded in the report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())