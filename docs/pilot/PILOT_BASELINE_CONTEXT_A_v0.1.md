# Phase 3 Pilot Baseline Context A Plan v0.1

**Project:** SocialCue-BN  
**Date:** 2026-08-30  
**Preparation method:** AI-assisted drafting  
**Technical review:** Approved by AI assistant  
**Human-language review:** Deferred to the final pilot quality gate  
**Status:** AI-PRE-SCREENED BASELINE A  
**Input:** `docs/pilot/PILOT_CANDIDATE_REVIEW_v0.1.md`

## 1. Purpose

This document defines baseline context A for the 15 selected pilot
message families.

It is an authoring plan, not the final pilot dataset. Contexts B and C,
gold labels, English-token calculations, and final structural validation
have not yet been completed.

The baseline contexts have passed an AI-assisted technical consistency
check. A consolidated native-Bangla naturalness review will be performed
before the complete pilot dataset is frozen.

## 2. Field interpretation

All relational fields describe the recipient relative to the speaker.

- `authority_relation`: lower, equal, higher, or unknown
- `relative_age`: younger, similar, older, or unknown
- `familiarity`: low, medium, or high
- `setting`: informal, semi-formal, or formal
- `source_register`: register already encoded in the message

The value `UNCLEAR` is used for source register because the selected
messages intentionally avoid direct TUI, TUMI, or APNI forms.

Generic roles are used so that authority, age, familiarity, or setting
can later change without changing the speaker-role or recipient-role
fields.

## 3. Baseline context A definitions

| Family | Message | Domain | Intent | Speaker role | Recipient role | Authority | Relative age | Familiarity | Setting | Source register | Planned B cue | Planned C cue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F001 | Kal project niye ekta meeting kora jabe? | academic | request | university_project_member | university_project_member | equal | similar | medium | semi-formal | UNCLEAR | authority | relative_age |
| F002 | Assignment er deadline niye ektu kotha chilo. | academic | request | student | academic_contact | equal | similar | high | informal | UNCLEAR | familiarity | setting |
| F003 | Report ta niye ektu motamot dorkar chilo. | academic | request | student_writer | academic_reviewer | equal | similar | medium | informal | UNCLEAR | authority | setting |
| F004 | Client er file ta ajker moddhe dorkar. | professional | request | work_team_member | work_team_member | equal | similar | high | semi-formal | UNCLEAR | authority | familiarity |
| F005 | Agamikaler shift er shomoy ta confirm kora dorkar. | professional | question | staff_member | staff_member | equal | similar | medium | informal | UNCLEAR | relative_age | setting |
| F006 | Ei prostab ta onumodon kora dorkar. | professional | request | proposal_author | proposal_reviewer | equal | similar | medium | semi-formal | UNCLEAR | authority | relative_age |
| F007 | Bari pouchhanor por ekbar janale bhalo hoy. | family | reminder | family_member | family_member | equal | similar | high | informal | UNCLEAR | relative_age | familiarity |
| F008 | Ghorer kaj e ektu shahajjo dorkar. | family | request | family_member | family_member | equal | similar | high | informal | UNCLEAR | authority | familiarity |
| F009 | Oshudh ta rate khete hobe. | family | reminder | family_member | family_member | equal | similar | high | informal | UNCLEAR | relative_age | setting |
| F010 | Kal campus e dekha kora jabe? | friendship | invitation | university_peer | university_peer | equal | similar | high | informal | UNCLEAR | familiarity | setting |
| F011 | Ekta chhoto shahajjo dorkar chilo. | friendship | request | friend | friend | equal | similar | high | informal | UNCLEAR | authority | relative_age |
| F012 | Ei thikanay jawar rasta ta jante chachchilam. | service/public | question | person_seeking_directions | public_contact | equal | similar | low | informal | UNCLEAR | authority | setting |
| F013 | Appointment er shomoy ta confirm kora dorkar. | service/public | follow-up | service_user | service_contact | equal | similar | high | semi-formal | UNCLEAR | relative_age | familiarity |
| F014 | Group e post korar niyom ta ektu clear kora jabe? | online community | question | online_group_member | online_group_member | equal | similar | high | informal | UNCLEAR | authority | familiarity |
| F015 | Ei tothyer source ta share kora jabe? | online community | request | online_community_member | online_community_member | equal | similar | medium | informal | UNCLEAR | relative_age | setting |

## 4. Baseline design rationale

Most baseline-A contexts use neutral or familiar relationships:

- equal authority;
- similar age;
- medium or high familiarity;
- informal or semi-formal settings.

This provides a controlled starting point. Context B can introduce a
stronger authority, age, familiarity, or setting contrast. Context C will
return to baseline A and change a different cue.

The generic roles intentionally avoid role names such as teacher, manager,
parent, or moderator because those names could independently reveal
authority or age. The explicit context fields carry that information.

## 5. AI technical pre-screen

- [x] There are exactly 15 baseline families.
- [x] Family IDs run from F001 through F015.
- [x] Every message matches the approved candidate-review file.
- [x] Each family has one baseline-A definition.
- [x] Every authority value belongs to the planned value set.
- [x] Every relative-age value belongs to the planned value set.
- [x] Every familiarity value belongs to the planned value set.
- [x] Every setting value belongs to the planned value set.
- [x] Roles do not unnecessarily reveal the cue that will change.
- [x] No primary or secondary register label has been assigned.
- [x] No context B or C has been created in this document.
- [x] This document is not presented as the final pilot dataset.
- [ ] Consolidated native-Bangla naturalness review completed at the final pilot quality gate.

## 6. Review decision

**AI technical pre-screen:** APPROVED  
**Human-language review:** DEFERRED TO FINAL PILOT QUALITY GATE  
**Approved next action:** Construct controlled contexts B and C

## 7. Current limitations

This approval covers structural and methodological consistency only.

It does not claim that:

- the messages have received independent native-speaker validation;
- TUI, TUMI, or APNI gold labels have been determined;
- the complete counterfactual families have passed programmatic validation;
- the English-token ratio or code-mixing level has been calculated;
- the pilot dataset is ready for annotation or model evaluation.

These checks will be completed at the appropriate later Phase 3 gates.