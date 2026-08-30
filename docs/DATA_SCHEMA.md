# SocialCue-BN Dataset Schema

Schema version: v0.1-DRAFT  
Protocol version: 2.0-APPROVED

## Purpose

This schema defines the structure of every SocialCue-BN dataset row.

One message family contains exactly three instances: A, B, and C. The
Romanized Bangla message must be identical in all three instances.

A is the baseline. B changes exactly one social cue from A. C returns to
the A context and changes one different cue from A. B and C are not
automatically treated as a controlled pair.

## Storage format

The primary tabular storage format is UTF-8 CSV.

Fields containing multiple values use the pipe character as the
separator. Example:

TUMI|APNI

Do not insert spaces before or after the pipe character.

## Dataset fields

| Field | Type | Definition |
|---|---|---|
| instance_id | string | Unique instance ID, such as F001-A. |
| message_family_id | string | Shared identifier for all three instances in one family. |
| variant | enum | A, B, or C. |
| romanized_message | string | Romanized Bangla message; byte-identical within a family. |
| source_register | enum | Register already expressed by the message. |
| domain | enum | Communication domain. |
| intent | enum | Main communicative intention. |
| speaker_role | string | Generic role of the speaker; never use identifiable real names. |
| recipient_role | string | Generic role of the recipient; never use identifiable real names. |
| authority_relation | enum | Recipient's authority relative to the speaker. |
| relative_age | enum | Recipient's age relative to the speaker. |
| familiarity | enum | Familiarity between speaker and recipient. |
| setting | enum | Informality or formality of the interaction. |
| changed_cue_from_A | enum | Cue changed from baseline A. |
| comparison_ids | pipe-separated list | IDs forming valid controlled comparisons. |
| primary_register | nullable enum | Adjudicated primary TUI, TUMI, or APNI label. |
| secondary_register | nullable enum | One optional additional acceptable label. |
| acceptable_registers | pipe-separated list | Primary register plus any approved secondary register. |
| answerability | enum | Whether the presented context is sufficient and consistent. |
| gold_confidence | nullable enum | Confidence after annotation and adjudication. |
| reason_codes | pipe-separated list | Contextual reasons supporting the register decision. |
| english_token_ratio | float | English lexical tokens divided by all lexical tokens. |
| code_mix_level | enum | Code-mixing category derived from the English-token ratio. |
| spelling_noise_level | enum | Amount of preserved Romanized spelling variation. |
| authoring_source | enum | Documented origin of the candidate message. |
| human_revision_status | enum | Human-review status of the candidate. |
| split | enum | DEVELOPMENT or TEST; assigned by complete family. |
| dataset_version | string | Dataset version or draft identifier. |

## Allowed categorical values

### variant

- A
- B
- C

### source_register

- TUI
- TUMI
- APNI
- MIXED
- UNCLEAR

### domain

- ACADEMIC
- PROFESSIONAL
- FAMILY
- FRIENDSHIP
- SERVICE_PUBLIC
- ONLINE

### intent

- REQUEST
- QUESTION
- REMINDER
- APOLOGY
- INVITATION
- FOLLOW_UP
- CONFIRMATION
- INFORMATION
- FEEDBACK
- OTHER

### authority_relation

The value describes the recipient relative to the speaker.

- LOWER
- EQUAL
- HIGHER
- UNKNOWN

### relative_age

The value describes the recipient relative to the speaker.

- YOUNGER
- SIMILAR
- OLDER
- UNKNOWN

### familiarity

- LOW
- MEDIUM
- HIGH

### setting

- INFORMAL
- SEMI_FORMAL
- FORMAL

### changed_cue_from_A

- NONE
- AUTHORITY
- AGE
- FAMILIARITY
- SETTING

### Register labels

- TUI
- TUMI
- APNI

### answerability

- ANSWERABLE
- UNDERSPECIFIED
- CONTRADICTORY
- CONTENTIOUS

### gold_confidence

- HIGH
- MEDIUM
- LOW

### reason_codes

- AUTHORITY
- AGE
- FAMILIARITY
- SETTING
- KINSHIP
- EMOTIONAL_STANCE
- OTHER

### code_mix_level

- NONE: english_token_ratio is exactly 0.000.
- LIGHT: english_token_ratio is greater than 0.000 and no more than 0.150.
- MODERATE: english_token_ratio is greater than 0.150 and no more than 0.300.

A ratio above 0.300 is invalid for the primary benchmark. Full English
clauses are excluded even when the numerical ratio is no more than 0.300.

### spelling_noise_level

- NONE
- LIGHT
- MODERATE

### authoring_source

- AI_CANDIDATE_REVISED
- HUMAN_DRAFT
- OTHER_DOCUMENTED

Unedited AI output cannot enter the research dataset.

### human_revision_status

- REVIEWED
- REWRITTEN
- REJECTED

Rows marked REJECTED cannot enter the final dataset.

### split

- DEVELOPMENT
- TEST

## Counterfactual family rules

1. Every message_family_id must have exactly three rows.
2. The three variants must be A, B, and C.
3. The romanized_message must be exactly identical across A, B, and C.
4. Variant A must use changed_cue_from_A = NONE.
5. Variant B must change exactly one of the four controlled cues from A.
6. Variant C must change exactly one different controlled cue from A.
7. All non-designated context fields must remain unchanged.
8. A comparison is valid only when exactly one controlled cue changes.
9. B and C must not automatically be treated as a controlled comparison.
10. A complete family must remain entirely inside one dataset split.

## Annotation-field rule

During early authoring, primary_register, secondary_register,
acceptable_registers, gold_confidence, and reason_codes may temporarily
be blank.

Before the final dataset is frozen:

- primary_register is required;
- acceptable_registers must contain the primary register;
- secondary_register must differ from the primary register;
- gold_confidence is required;
- reason_codes are required;
- answerability must be resolved according to the annotation protocol.

Designer predictions must never be shown to annotators as gold labels.

## Privacy rule

Do not include real names, phone numbers, email addresses, private
institutional information, or copied private conversations. Use generic
roles or clearly fictional placeholders.