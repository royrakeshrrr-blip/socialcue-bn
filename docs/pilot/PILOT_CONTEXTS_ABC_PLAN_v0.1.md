# Phase 3 Pilot Contexts A/B/C Plan v0.1

**Project:** SocialCue-BN  
**Date:** 2026-08-30  
**Preparation method:** AI-assisted controlled-context construction  
**Technical verification:** PASSED  
**Human-language review:** Deferred to the final pilot quality gate  
**Status:** AI-PRE-SCREENED A/B/C PLAN  
**Baseline input:** `docs/pilot/PILOT_BASELINE_CONTEXT_A_v0.1.md`  
**Message input:** `docs/pilot/PILOT_CANDIDATE_REVIEW_v0.1.md`

## 1. Purpose

This document defines controlled contexts A, B, and C for the 15 pilot
message families.

Each family contains:

- A: baseline context;
- B: changes exactly one designated cue from A;
- C: returns to A and changes one different designated cue.

A-B and A-C are controlled comparisons. B-C is not automatically treated
as a controlled comparison.

No TUI, TUMI, or APNI gold labels are assigned in this document.

## 2. Controlled-construction rules

1. The Romanized message must remain identical across A, B, and C.
2. Domain, intent, speaker role, recipient role, and source register remain fixed.
3. B changes exactly one of the four social cues.
4. C restores the B-changed cue to its A value.
5. C changes a different cue from A.
6. `changed_cue_from_A` is `NONE` for A.
7. B and C identify their single changed cue.
8. Only A-B and A-C are designated controlled comparisons.

## 3. Fixed family metadata

The metadata below applies identically to all three variants in each family.

| Family | Romanized message | Domain | Intent | Speaker role | Recipient role | Source register |
|---|---|---|---|---|---|---|
| F001 | Kal project niye ekta meeting kora jabe? | academic | request | university_project_member | university_project_member | UNCLEAR |
| F002 | Assignment er deadline niye ektu kotha chilo. | academic | request | student | academic_contact | UNCLEAR |
| F003 | Report ta niye ektu motamot dorkar chilo. | academic | request | student_writer | academic_reviewer | UNCLEAR |
| F004 | Client er file ta ajker moddhe dorkar. | professional | request | work_team_member | work_team_member | UNCLEAR |
| F005 | Agamikaler shift er shomoy ta confirm kora dorkar. | professional | question | staff_member | staff_member | UNCLEAR |
| F006 | Ei prostab ta onumodon kora dorkar. | professional | request | proposal_author | proposal_reviewer | UNCLEAR |
| F007 | Bari pouchhanor por ekbar janale bhalo hoy. | family | reminder | family_member | family_member | UNCLEAR |
| F008 | Ghorer kaj e ektu shahajjo dorkar. | family | request | family_member | family_member | UNCLEAR |
| F009 | Oshudh ta rate khete hobe. | family | reminder | family_member | family_member | UNCLEAR |
| F010 | Kal campus e dekha kora jabe? | friendship | invitation | university_peer | university_peer | UNCLEAR |
| F011 | Ekta chhoto shahajjo dorkar chilo. | friendship | request | friend | friend | UNCLEAR |
| F012 | Ei thikanay jawar rasta ta jante chachchilam. | service/public | question | person_seeking_directions | public_contact | UNCLEAR |
| F013 | Appointment er shomoy ta confirm kora dorkar. | service/public | follow-up | service_user | service_contact | UNCLEAR |
| F014 | Group e post korar niyom ta ektu clear kora jabe? | online community | question | online_group_member | online_group_member | UNCLEAR |
| F015 | Ei tothyer source ta share kora jabe? | online community | request | online_community_member | online_community_member | UNCLEAR |

## 4. Context cue matrix

All relational values describe the recipient relative to the speaker.

| Instance ID | Family | Variant | Authority | Relative age | Familiarity | Setting | Changed cue from A | Controlled comparison |
|---|---|---|---|---|---|---|---|---|
| F001-A | F001 | A | equal | similar | medium | semi-formal | NONE | BASELINE |
| F001-B | F001 | B | higher | similar | medium | semi-formal | AUTHORITY | A-B |
| F001-C | F001 | C | equal | older | medium | semi-formal | AGE | A-C |
| F002-A | F002 | A | equal | similar | high | informal | NONE | BASELINE |
| F002-B | F002 | B | equal | similar | low | informal | FAMILIARITY | A-B |
| F002-C | F002 | C | equal | similar | high | formal | SETTING | A-C |
| F003-A | F003 | A | equal | similar | medium | informal | NONE | BASELINE |
| F003-B | F003 | B | higher | similar | medium | informal | AUTHORITY | A-B |
| F003-C | F003 | C | equal | similar | medium | formal | SETTING | A-C |
| F004-A | F004 | A | equal | similar | high | semi-formal | NONE | BASELINE |
| F004-B | F004 | B | higher | similar | high | semi-formal | AUTHORITY | A-B |
| F004-C | F004 | C | equal | similar | low | semi-formal | FAMILIARITY | A-C |
| F005-A | F005 | A | equal | similar | medium | informal | NONE | BASELINE |
| F005-B | F005 | B | equal | older | medium | informal | AGE | A-B |
| F005-C | F005 | C | equal | similar | medium | formal | SETTING | A-C |
| F006-A | F006 | A | equal | similar | medium | semi-formal | NONE | BASELINE |
| F006-B | F006 | B | higher | similar | medium | semi-formal | AUTHORITY | A-B |
| F006-C | F006 | C | equal | older | medium | semi-formal | AGE | A-C |
| F007-A | F007 | A | equal | similar | high | informal | NONE | BASELINE |
| F007-B | F007 | B | equal | older | high | informal | AGE | A-B |
| F007-C | F007 | C | equal | similar | low | informal | FAMILIARITY | A-C |
| F008-A | F008 | A | equal | similar | high | informal | NONE | BASELINE |
| F008-B | F008 | B | higher | similar | high | informal | AUTHORITY | A-B |
| F008-C | F008 | C | equal | similar | low | informal | FAMILIARITY | A-C |
| F009-A | F009 | A | equal | similar | high | informal | NONE | BASELINE |
| F009-B | F009 | B | equal | older | high | informal | AGE | A-B |
| F009-C | F009 | C | equal | similar | high | formal | SETTING | A-C |
| F010-A | F010 | A | equal | similar | high | informal | NONE | BASELINE |
| F010-B | F010 | B | equal | similar | low | informal | FAMILIARITY | A-B |
| F010-C | F010 | C | equal | similar | high | formal | SETTING | A-C |
| F011-A | F011 | A | equal | similar | high | informal | NONE | BASELINE |
| F011-B | F011 | B | higher | similar | high | informal | AUTHORITY | A-B |
| F011-C | F011 | C | equal | older | high | informal | AGE | A-C |
| F012-A | F012 | A | equal | similar | low | informal | NONE | BASELINE |
| F012-B | F012 | B | higher | similar | low | informal | AUTHORITY | A-B |
| F012-C | F012 | C | equal | similar | low | formal | SETTING | A-C |
| F013-A | F013 | A | equal | similar | high | semi-formal | NONE | BASELINE |
| F013-B | F013 | B | equal | older | high | semi-formal | AGE | A-B |
| F013-C | F013 | C | equal | similar | low | semi-formal | FAMILIARITY | A-C |
| F014-A | F014 | A | equal | similar | high | informal | NONE | BASELINE |
| F014-B | F014 | B | higher | similar | high | informal | AUTHORITY | A-B |
| F014-C | F014 | C | equal | similar | low | informal | FAMILIARITY | A-C |
| F015-A | F015 | A | equal | similar | medium | informal | NONE | BASELINE |
| F015-B | F015 | B | equal | older | medium | informal | AGE | A-B |
| F015-C | F015 | C | equal | similar | medium | formal | SETTING | A-C |

## 5. Changed-cue coverage

| Changed cue | B/C comparisons |
|---|---:|
| AUTHORITY | 8 |
| AGE | 8 |
| FAMILIARITY | 7 |
| SETTING | 7 |
| **Total** | **30** |

The 15 A rows are baselines and therefore use `NONE`.

## 6. Technical verification result

The cue matrix was checked programmatically before being provided.

- [x] Exactly 15 families are present.
- [x] Exactly 45 contexts are present.
- [x] Every family contains A, B, and C.
- [x] Every A row is marked `NONE`.
- [x] Every B row changes exactly one cue from A.
- [x] Every C row restores the B cue to its A value.
- [x] Every C row changes one different cue from A.
- [x] There are 30 controlled comparisons.
- [x] Authority appears in 8 controlled comparisons.
- [x] Age appears in 8 controlled comparisons.
- [x] Familiarity appears in 7 controlled comparisons.
- [x] Setting appears in 7 controlled comparisons.
- [x] No B-C comparison is designated as controlled.
- [x] No gold register labels are assigned.
- [ ] Consolidated native-Bangla naturalness review completed at the final pilot quality gate.

## 7. Current status and next action

**AI technical verification:** PASSED  
**Human-language review:** DEFERRED TO FINAL PILOT QUALITY GATE  
**Current artifact type:** Controlled-context authoring plan  
**Next action:** Convert this plan into the frozen 28-column pilot CSV structure

This document is not yet the final dataset. Gold-label fields, code-mixing
measurements, spelling-noise tags, split assignment, and dataset-version
fields must be completed or appropriately marked before the pilot CSV is
validated and frozen.