# Phase 3 Pilot Candidate Review v0.1

**Project:** SocialCue-BN  
**Review date:** 2026-08-30  
**Reviewer ID:** R01  
**Status:** APPROVED FOR CONTEXT CONSTRUCTION  
**Raw candidate source:** `docs/pilot/AI_CANDIDATES_RAW_v0.1.md`

## 1. Review purpose

This document records the human review of the 30 AI-generated pilot
candidates and the selection of 15 message families for controlled-context
construction.

The raw AI-output file remains unchanged. The selected messages and all
language revisions are recorded in this separate human-reviewed document.

These messages are approved only for context construction. They are not
gold-labelled or validated benchmark instances yet.

## 2. Human-review confirmation

The student researcher completed the following checks:

- [x] Read all 30 raw candidates.
- [x] Read the 15 selected messages aloud.
- [x] Checked the messages for understandable Romanized Bangla.
- [x] Checked that each selected message has a clear intention.
- [x] Checked that the messages contain no private or identifiable information.
- [x] Checked that each message can remain unchanged across three contexts.
- [x] Checked that no selected message directly uses TUI, TUMI, or APNI.
- [x] Reviewed the proposed selection and rejection decisions.
- [x] Accepted all 15 recommended candidates and reviewed messages.
- [x] Preserved the original raw AI-output file without modification.

## 3. Selected message families

| Family ID | Source candidate | Domain | Human-reviewed Romanized Bangla message | A-B planned cue | A-C planned cue |
|---|---|---|---|---|---|
| F001 | C001 | Academic | Kal project niye ekta meeting kora jabe? | authority | relative_age |
| F002 | C002 | Academic | Assignment er deadline niye ektu kotha chilo. | familiarity | setting |
| F003 | C003 | Academic | Report ta niye ektu motamot dorkar chilo. | authority | setting |
| F004 | C006 | Professional | Client er file ta ajker moddhe dorkar. | authority | familiarity |
| F005 | C007 | Professional | Agamikaler shift er shomoy ta confirm kora dorkar. | relative_age | setting |
| F006 | C008 | Professional | Ei prostab ta onumodon kora dorkar. | authority | relative_age |
| F007 | C011 | Family | Bari pouchhanor por ekbar janale bhalo hoy. | relative_age | familiarity |
| F008 | C012 | Family | Ghorer kaj e ektu shahajjo dorkar. | authority | familiarity |
| F009 | C013 | Family | Oshudh ta rate khete hobe. | relative_age | setting |
| F010 | C016 | Friendship | Kal campus e dekha kora jabe? | familiarity | setting |
| F011 | C017 | Friendship | Ekta chhoto shahajjo dorkar chilo. | authority | relative_age |
| F012 | C021 | Service/public interaction | Ei thikanay jawar rasta ta jante chachchilam. | authority | setting |
| F013 | C023 | Service/public interaction | Appointment er shomoy ta confirm kora dorkar. | relative_age | familiarity |
| F014 | C026 | Online community | Group e post korar niyom ta ektu clear kora jabe? | authority | familiarity |
| F015 | C027 | Online community | Ei tothyer source ta share kora jabe? | relative_age | setting |

## 4. Domain coverage

| Domain | Selected families | Count |
|---|---|---:|
| Academic | F001, F002, F003 | 3 |
| Professional | F004, F005, F006 | 3 |
| Family | F007, F008, F009 | 3 |
| Friendship | F010, F011 | 2 |
| Service/public interaction | F012, F013 | 2 |
| Online community | F014, F015 | 2 |
| **Total** | **F001-F015** | **15** |

## 5. Planned cue coverage

Every selected family will later produce two controlled comparisons:

- A-B will change one cue.
- A-C will change one different cue.
- B-C will not automatically be treated as controlled.

| Planned changed cue | Number of comparisons |
|---|---:|
| authority | 8 |
| relative_age | 8 |
| familiarity | 7 |
| setting | 7 |
| **Total** | **30** |

The actual context values have not yet been constructed.

## 6. Human-reviewed language revisions

| Candidate | Raw AI-generated message | Accepted reviewed message | Reason |
|---|---|---|---|
| C003 | Report ta niye ektu feedback dorkar. | Report ta niye ektu motamot dorkar chilo. | Reduced unnecessary English mixing and made the request softer. |
| C011 | Bari pouchhanor por ekta message korle bhalo hoy. | Bari pouchhanor por ekbar janale bhalo hoy. | Improved naturalness and reduced English mixing. |
| C016 | Kal campus e dekha korar plan ache? | Kal campus e dekha kora jabe? | Made the meeting request clearer and more direct. |
| C021 | Ei address e jawar rasta ta jante chai. | Ei thikanay jawar rasta ta jante chachchilam. | Improved naturalness and replaced an English lexical item. |

## 7. Rejected candidates

| Candidate | Decision reason |
|---|---|
| C004 | Overlaps with other scheduling and confirmation messages. |
| C005 | Overlaps with the selected file and assistance requests. |
| C009 | “Ager request” depends on unspecified previous information. |
| C010 | Overlaps with selected meeting and shift-confirmation messages. |
| C014 | Primarily a statement and does not clearly address a recipient. |
| C015 | Has weaker cue coverage than the selected family requests. |
| C018 | Overlaps with academic file and note requests. |
| C019 | “Ager bishoy” depends on hidden previous information. |
| C020 | Overlaps with the selected friendship-planning message. |
| C022 | Simple price inquiry may have weak sensitivity to multiple cues. |
| C024 | Overlaps with the selected public-information request. |
| C025 | The driver context restricts meaningful counterfactual variation. |
| C028 | The intended recipient and communication purpose are underspecified. |
| C029 | The answer may depend on whether the recipient knows why the post was removed. |
| C030 | Procedural request with weaker age and familiarity sensitivity. |

## 8. Review decision

**Human decision:** All 15 recommended candidates and reviewed messages were accepted.

**Approved next action:** Construct baseline context A for families F001-F015.

**Not yet permitted:**

- assigning gold TUI, TUMI, or APNI labels;
- creating contexts B and C;
- conducting annotation;
- running model experiments;
- treating these messages as the final benchmark.