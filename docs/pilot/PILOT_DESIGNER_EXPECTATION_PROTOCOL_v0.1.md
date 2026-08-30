# Pilot Designer-Expectation Protocol v0.1

**Project:** SocialCue-BN  
**Date:** 2026-08-30  
**Status:** FROZEN PRIVATE PRIOR — NOT GOLD DATA

## 1. Purpose

The private designer expectations record the anticipated register
labels for the 45 pilot instances before independent annotation.

Their purpose is to support later error analysis by showing where
independent annotators agree or disagree with the original dataset
design assumptions.

The designer expectations are not human annotations and are not part
of the gold dataset.

## 2. Input and Private Output

Public source dataset:

`data/pilot/pilot_authoring_v0.1.csv`

Private expectation dataset:

`data/private/pilot_designer_expectations_v0.1.csv`

The private file contains 45 rows covering 15 complete A/B/C message
families.

The private file is excluded from Git through the `data/private/`
ignore rule.

## 3. Expectation Method

The provisional expectations were generated using a transparent,
AI-assisted context-rule prior.

The rules use the following social-context fields:

- authority relation;
- relative age;
- familiarity;
- communication setting.

The broad decision rules were:

1. Formal settings generally favor APNI.
2. Higher recipient authority generally favors APNI.
3. Older recipient age generally favors APNI unless strong
   familiarity and informality weaken that preference.
4. Low familiarity generally favors APNI.
5. TUI is predicted only when lower authority, younger age, high
   familiarity, and an informal setting occur together.
6. Close informal relationships generally favor TUMI, while TUI may
   be listed as a secondary possibility.
7. Semi-formal contexts generally favor TUMI while allowing APNI as
   a secondary possibility.
8. TUMI is the neutral expectation when no stronger social cue
   requires APNI or strongly licenses TUI.

The private expectations may contain:

- a provisional primary register;
- an optional provisional secondary register;
- a provisional acceptable-register set;
- provisional confidence;
- provisional reason codes;
- a short explanatory note.

## 4. Scientific Separation

The private expectations must remain separate from:

- the public pilot authoring dataset;
- annotator instructions;
- annotator response sheets;
- adjudication materials shown before independent decisions;
- final gold labels.

The following authoring-dataset fields remain blank:

- `primary_register`
- `secondary_register`
- `acceptable_registers`
- `gold_confidence`
- `reason_codes`

No AI-assisted expectation may be represented as a human annotation.

## 5. Annotator Blinding

Annotators must not receive or inspect the private expectation file.

The private expectations must not be used to persuade annotators or
resolve disagreements during annotation.

Gold labels will be determined from independent annotation and
documented adjudication. If human judgments disagree with the private
expectations, the private expectations do not automatically take
priority.

## 6. Frozen-File Commitment

A SHA-256 fingerprint of the private expectation file is stored in:

`docs/pilot/PILOT_DESIGNER_EXPECTATION_HASH_v0.1.txt`

The fingerprint commits to the exact private file without publishing
its contents.

Any later modification to the private CSV will produce a different
SHA-256 fingerprint and must be recorded through formal change
control.

## 7. Remaining Quality Gate

A consolidated native-Bangla naturalness review remains pending and
will be completed before the pilot dataset is finally frozen.

Independent annotation and adjudication are also still required.

## 8. Decision

The private designer prior is approved only as a frozen research
planning and comparison artifact.

It is not approved as:

- human annotation;
- adjudicated annotation;
- gold data; or
- evidence of model performance.