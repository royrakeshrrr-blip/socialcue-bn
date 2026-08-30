# Pilot Authoring Dataset Validation Report v0.1

**Project:** SocialCue-BN  
**Date:** 2026-08-30  
**Dataset:** `data/pilot/pilot_authoring_v0.1.csv`  
**Dataset version:** `PILOT-AUTHORING-V0.1`  
**Status:** TECHNICALLY VALIDATED — NOT YET GOLD-LABELLED

## 1. Purpose

This report records the technical validation of the SocialCue-BN
pilot authoring dataset.

The dataset currently contains the Romanized Bangla messages and
their controlled social-context variants. It does not yet contain
final gold register labels.

## 2. Validation Commands

The following commands were executed from the repository root while
the Python virtual environment was active:

```powershell
python -m src.build_pilot_authoring
python -m src.validate_dataset data/pilot/pilot_authoring_v0.1.csv
python -m pytest
```

## 3. Validation Results

| Validation check | Result |
|---|---|
| Dataset generation completed | PASS |
| Row-level schema validation | PASS |
| Counterfactual family validation | PASS |
| Automated test suite | PASS |
| Gold-label fields remain blank | PASS |
| English-token ratio is at most 0.30 | PASS |

## 4. Dataset Size

| Item | Count |
|---|---:|
| Message families | 15 |
| Variant A rows | 15 |
| Variant B rows | 15 |
| Variant C rows | 15 |
| Total dataset rows | 45 |
| Counterfactual comparison rows | 30 |

Each family contains exactly three rows: A, B, and C.

Variant A is the baseline context. Variants B and C each change
exactly one social-context cue relative to A.

## 5. Changed-Cue Distribution

| Changed social cue | Number of B/C rows |
|---|---:|
| Authority | 8 |
| Relative age | 8 |
| Familiarity | 7 |
| Setting | 7 |
| **Total** | **30** |

The changed-cue distribution is sufficiently balanced for the
15-family pilot.

## 6. Code-Mixing Distribution

| Code-mixing level | Families | Rows |
|---|---:|---:|
| NONE | 6 | 18 |
| LIGHT | 1 | 3 |
| MODERATE | 8 | 24 |
| **Total** | **15** | **45** |

The highest English-token ratio is `0.300`, found in family `F014`.
This is equal to the permitted maximum and therefore passes the
frozen schema rule.

Two selected messages were revised before dataset generation:

1. `F005` was revised to reduce excessive English-token use.
2. `F006` was revised by replacing unnecessary English lexical items
   with natural Romanized Bangla alternatives.

The immutable raw AI-candidate file was not edited.

## 7. Gold-Label Safeguard

The following fields remain blank in the authoring dataset:

- `primary_register`
- `secondary_register`
- `acceptable_registers`
- `gold_confidence`
- `reason_codes`

They are intentionally blank because the authoring dataset must not
be treated as a gold-labelled dataset before annotation and
adjudication.

No AI-generated prediction has been inserted as a human gold label.

## 8. Current Review Status

Completed:

- AI-assisted candidate generation
- Candidate selection and revision
- Baseline-context design
- Controlled A/B/C context construction
- Schema validation
- Counterfactual validation
- Code-mixing validation
- Automated testing

Still required before freezing the pilot:

- Consolidated native-Bangla naturalness review
- Annotation preparation
- Independent annotation
- Adjudication of disagreements
- Final pilot dataset validation and freeze

## 9. Technical Decision

The pilot authoring dataset is technically approved for the next
quality-control and annotation-preparation steps.

It must not yet be described as:

- a gold-labelled dataset;
- an independently human-validated dataset; or
- the final frozen pilot dataset.