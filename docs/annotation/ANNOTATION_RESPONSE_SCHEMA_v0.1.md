# SocialCue-BN Annotation Response Schema

**Version:** v0.1  
**Date:** 2026-08-31  
**Status:** DRAFT  
**Related guide:** `ANNOTATION_GUIDE_DRAFT_v0.1.md`

## 1. Purpose

This document defines the raw response format used by independent
annotators during SocialCue-BN annotation.

Each CSV row represents one independent judgment of one blinded
dataset instance.

The raw annotation file must contain only information required to
make and record the judgment.

## 2. Blinding Requirements

Annotators may see:

- an opaque annotation ID;
- the Romanized Bangla message;
- domain and intent;
- speaker and recipient roles;
- authority relation;
- relative age;
- familiarity;
- setting.

Annotators must not see:

- `instance_id`;
- `message_family_id`;
- A/B/C variant labels;
- `changed_cue_from_A`;
- `comparison_ids`;
- `source_register`;
- private designer expectations;
- another annotator's responses;
- model predictions;
- gold labels.

The annotation ID must use an opaque format such as `P001`. It must
not reveal the original family or variant.

## 3. Column Definitions

| Column | Filled by | Required | Allowed content |
|---|---|---|---|
| `annotation_id` | Packet generator | Yes | Opaque identifier such as `P001` |
| `annotator_code` | Packet generator | Yes | Anonymous code such as `A1` or `A2` |
| `packet_order` | Packet generator | Yes | Integer from 1 to the packet size |
| `romanized_message` | Packet generator | Yes | Unmodified Romanized Bangla message |
| `domain` | Packet generator | Yes | Frozen dataset domain |
| `intent` | Packet generator | Yes | Frozen dataset intent |
| `speaker_role` | Packet generator | Yes | Speaker's role |
| `recipient_role` | Packet generator | Yes | Recipient's role |
| `authority_relation` | Packet generator | Yes | `LOWER`, `EQUAL`, `HIGHER`, or `UNKNOWN` |
| `relative_age` | Packet generator | Yes | `YOUNGER`, `SIMILAR`, `OLDER`, or `UNKNOWN` |
| `familiarity` | Packet generator | Yes | `LOW`, `MEDIUM`, or `HIGH` |
| `setting` | Packet generator | Yes | `INFORMAL`, `SEMI_FORMAL`, or `FORMAL` |
| `answerability` | Annotator | Yes | `ANSWERABLE`, `UNDERSPECIFIED`, `CONTRADICTORY`, or `CONTENTIOUS` |
| `primary_register` | Annotator | Conditional | `TUI`, `TUMI`, `APNI`, or blank |
| `secondary_register` | Annotator | No | `TUI`, `TUMI`, `APNI`, or blank |
| `confidence` | Annotator | Yes | `HIGH`, `MEDIUM`, or `LOW` |
| `reason_codes` | Annotator | Yes | One or more permitted codes separated by `|` |
| `annotation_note` | Annotator | Conditional | Short one-line explanation |
| `annotation_timestamp` | Annotator or collection tool | Yes | Timezone-aware ISO 8601 timestamp |
| `guide_version` | Packet generator | Yes | Annotation-guide version used |

## 4. Prefilled Columns

Annotators must not edit the following columns:

- `annotation_id`
- `annotator_code`
- `packet_order`
- `romanized_message`
- `domain`
- `intent`
- `speaker_role`
- `recipient_role`
- `authority_relation`
- `relative_age`
- `familiarity`
- `setting`
- `guide_version`

Only the seven response columns may be edited or populated during collection:

- `answerability`
- `primary_register`
- `secondary_register`
- `confidence`
- `reason_codes`
- `annotation_note`
- `annotation_timestamp`

## 5. Rules for Answerable Items

When `answerability=ANSWERABLE`:

- `primary_register` is required;
- `secondary_register` is optional;
- primary and secondary must be different;
- `confidence` is required;
- at least one `reason_codes` value is required;
- `annotation_note` is optional.

The primary register must be one of:

- `TUI`
- `TUMI`
- `APNI`

## 6. Rules for Non-Answerable Items

When answerability is:

- `UNDERSPECIFIED`;
- `CONTRADICTORY`; or
- `CONTENTIOUS`;

then:

- `primary_register` must remain blank;
- `secondary_register` must remain blank;
- `confidence` must be `LOW`;
- at least one reason code is required;
- `annotation_note` is required.

## 7. Reason-Code Format

Allowed reason codes are:

- `AUTHORITY`
- `AGE`
- `FAMILIARITY`
- `SETTING`
- `KINSHIP`
- `EMOTIONAL_STANCE`
- `OTHER`

Multiple codes must be separated using the pipe character.

Example:

`AUTHORITY|SETTING`

Do not use commas to separate reason codes.

If `OTHER` is selected, the annotation note is required.

## 8. Blank-Value Rules

Do not type any of the following to represent a blank value:

- `N/A`
- `NA`
- `NONE`
- `NULL`
- `-`

Leave the CSV field genuinely empty when a blank is permitted.
### 8.1 Annotation-Timestamp Rule

The `annotation_timestamp` field must remain blank in:

- the header-only response template; and
- a blank annotation packet that has not yet been completed.

The field becomes required when an annotator completes a response.

The timestamp must use timezone-aware ISO 8601 format.

Example for Bangladesh time:

`2026-08-31T15:30:00+06:00`

The example is provided only to demonstrate the format. Annotators must
not copy it as their actual timestamp.

Invalid examples include:

- `2026-08-31`
- `15:30`
- `2026-08-31 15:30`
- `N/A`
- `NONE`

A completed response with a blank timestamp or a timestamp without a
timezone must fail validation.

## 9. Acceptable-Register Set

Annotators will not manually enter an `acceptable_registers` field.

After collection, the processing script will derive it as:

- primary only, when secondary is blank;
- `PRIMARY|SECONDARY`, when secondary is present.

This prevents inconsistencies between primary, secondary, and
acceptable-register fields.

## 10. Raw and Processed Data Separation

The annotator CSV is raw research data.

It must not be manually corrected after submission.

If a response is invalid:

1. preserve the original submitted file;
2. record the validation problem;
3. request a correction from the same annotator;
4. save the correction as a new version.

Derived acceptable sets, agreement measures, and adjudicated labels
will be stored in separate processed files.

## 11. Storage

Raw response files will be stored privately under:

`data/private/annotations/`

Annotators will be identified only through codes such as `A1` and
`A2`.

Personal names and contact information must not appear in public
research files.

## 12. Current Authorization

This schema is authorized for template and validator development.

It is not yet authorized for distribution of the 45 pilot items.