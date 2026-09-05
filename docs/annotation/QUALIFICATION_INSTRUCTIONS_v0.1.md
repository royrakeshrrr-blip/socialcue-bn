# SocialCue-BN Qualification Instructions

**Version:** v0.1  
**Guide version:** Draft v0.1  
**Qualification size:** 12 controls  
**Passing requirement:** At least 10 correct primary-register labels

## 1. Purpose

This qualification exercise checks whether a candidate understands how
to identify socially appropriate TUI, TUMI, and APNI address registers
from Romanized Bangla messages and their social contexts.

The qualification controls are separate from the 45-item pilot and will
never be included in the research benchmark.

## 2. Materials

Each candidate receives:

- the SocialCue-BN annotation guide;
- this qualification-instruction document;
- one assigned 12-row qualification CSV; and
- the approved participant information and consent material.

Candidates must open only the packet assigned to their annotator code.

## 3. Required Procedure

For every row:

1. Read the Romanized Bangla message.
2. Read the speaker and recipient roles.
3. Read authority, relative age, familiarity, and setting.
4. Select the appropriate answerability category.
5. Select exactly one primary register for an answerable item.
6. Add one secondary register only when it is genuinely acceptable.
7. Select confidence.
8. Select the relevant reason codes.
9. Add a short note when the annotation guide requires it.
10. Enter a real timezone-aware ISO 8601 timestamp.
11. Complete the items in the supplied packet order.

## 4. Editable Columns

Only these seven response columns may be completed:

- `answerability`
- `primary_register`
- `secondary_register`
- `confidence`
- `reason_codes`
- `annotation_note`
- `annotation_timestamp`

Do not edit:

- `annotation_id`
- `annotator_code`
- `packet_order`
- the message or context fields;
- `guide_version`; or
- the CSV header.

## 5. Independence Requirements

Candidates must not:

- discuss individual qualification items with another person;
- inspect another candidate's packet or answers;
- use ChatGPT or another AI system to choose labels;
- search online for answers to individual items;
- inspect the private reference key;
- inspect designer expectations; or
- ask the researcher which label to select.

Candidates may ask procedural questions about the written instructions.
The researcher must not recommend a label for a specific item.

## 6. Scoring

Qualification is based on the primary register.

A candidate must correctly label at least 10 of the 12 controls.

The researcher will also check whether the candidate:

- systematically confuses any label pair;
- understands primary versus secondary registers;
- understands the answerability categories; and
- followed the independence requirements.

Cohen's kappa is not used as the qualification passing threshold.

If the first attempt fails, the candidate may receive clarification and
different practice examples before one new qualification attempt. The
same failed controls must not simply be repeated as a coached test.

## 7. Saving and Submission

Save the completed file as CSV UTF-8 without changing its filename.

Return only the assigned completed qualification packet.

Do not send another candidate's file, the annotation guide, or a renamed
copy of the packet.