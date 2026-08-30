# Phase 3 Exit Gate

**Project:** SocialCue-BN  
**Phase:** 3 — Pilot Dataset Authoring  
**Gate date:** 2026-08-30  
**Gate status:** PASS — PHASE CLOSED  
**Next phase:** Phase 4 — Annotation Guide and Annotator Qualification

## 1. Phase Objective

The objective of Phase 3 was to author and technically validate a
small controlled pilot dataset before preparing the annotation
process.

The required pilot size was:

- 15 message families;
- three variants per family;
- 45 total instances.

## 2. Exit Decision

Phase 3 has passed its exit gate.

The 45-row pilot authoring dataset is structurally valid and ready
for annotation-guide development.

The dataset is not yet a gold-labelled dataset.

## 3. Primary Evidence

| Evidence | Location | Status |
|---|---|---|
| Pilot authoring dataset | `data/pilot/pilot_authoring_v0.1.csv` | PASS |
| Pilot-generation script | `src/build_pilot_authoring.py` | PASS |
| Candidate-review record | `docs/pilot/PILOT_CANDIDATE_REVIEW_v0.1.md` | PASS |
| Baseline-context record | `docs/pilot/PILOT_BASELINE_CONTEXT_A_v0.1.md` | PASS |
| A/B/C context plan | `docs/pilot/PILOT_CONTEXTS_ABC_PLAN_v0.1.md` | PASS |
| Authoring validation report | `docs/pilot/PILOT_AUTHORING_VALIDATION_REPORT_v0.1.md` | PASS |
| Designer-expectation protocol | `docs/pilot/PILOT_DESIGNER_EXPECTATION_PROTOCOL_v0.1.md` | PASS |
| Private-prior SHA-256 commitment | `docs/pilot/PILOT_DESIGNER_EXPECTATION_HASH_v0.1.txt` | PASS |
| AI-use audit record | `AI_USE_LOG.csv` | PASS |

## 4. Dataset Completion Checks

- [x] The dataset contains exactly 15 message families.
- [x] The dataset contains exactly 45 rows.
- [x] Every family contains variants A, B, and C.
- [x] Variant A is the family baseline.
- [x] Every B row changes exactly one context cue from A.
- [x] Every C row changes exactly one context cue from A.
- [x] B and C change different context cues.
- [x] All comparison IDs point to valid family members.
- [x] All rows satisfy the frozen schema.
- [x] All English-token ratios are at most 0.30.
- [x] Code-mixing levels match their English-token ratios.
- [x] Automated tests pass.
- [x] Final gold-register fields remain blank.

## 5. Gold-Label Protection

The following fields remain blank in the public authoring dataset:

- `primary_register`
- `secondary_register`
- `acceptable_registers`
- `gold_confidence`
- `reason_codes`

These fields will not be populated using AI-assisted designer
expectations.

They may be populated only after independent annotation and
documented adjudication.

## 6. Private Designer Prior

A private AI-assisted designer prior was created for later comparison
and diagnostic analysis.

It is stored locally under:

`data/private/pilot_designer_expectations_v0.1.csv`

The private prior:

- is excluded from Git;
- is not given to annotators;
- is not treated as human annotation;
- is not treated as gold data;
- is protected by a public SHA-256 commitment.

## 7. Deferred Work

The following tasks are intentionally deferred and do not block the
Phase 3 exit:

- writing the annotation guide;
- qualifying annotators;
- conducting the consolidated native-Bangla naturalness review;
- running independent pilot annotation;
- measuring agreement;
- adjudicating disagreements;
- producing the final gold-labelled pilot.

These activities belong to Phase 4, Phase 5, or the later final pilot
quality gate.

## 8. Scope-Control Decision

No model evaluation, API experiment, full-dataset expansion, agentic
system, knowledge graph, or rewriting demonstration will begin at
this gate.

The next authorized activity is Phase 4 annotation-guide development
and annotator qualification.

## 9. Final Gate Statement

Phase 3 is formally closed.

The approved Phase 3 output is a technically validated,
non-gold-labelled 45-instance pilot authoring dataset with controlled
A/B/C social-context variants.