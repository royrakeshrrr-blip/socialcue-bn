# SocialCue-BN Research Protocol v2.0

**Working title:** SocialCue-BN: A Counterfactual Benchmark and Lightweight
Agentic Framework for Tui–Tumi–Apni Selection and Register-Aware Rewriting
in Romanized Bangla

**Protocol version:** 2.0  
**Status:** DRAFT  
**Researcher:** Rakesh Roy Plabon  
**Supervisor:** Prof. Rokan Uddin Faruqui
**Date created:** 8/30/26 
**Approval date:** Pending  
**Dataset size:** 150 message families / 450 instances  
**Core experiment:** 3 models × 3 prompt conditions  
**Agent extension:** 90 test cases / 3 systems  
## 1. Study Scope

### 1.1 Main problem

Romanized Bangla messages do not always clearly indicate whether the speaker
should use Tui, Tumi or Apni. The appropriate choice depends on social
information such as the recipient's authority, age, familiarity with the
speaker and the communication setting.

This thesis will investigate whether existing large language models can use
this social information correctly and consistently.

### 1.2 Core benchmark

The core contribution will be a controlled Romanized Bangla benchmark.

The benchmark will contain:

- 150 message families.
- Three context variants for every message family.
- 450 total context-conditioned instances.
- Tui, Tumi and Apni as the target register labels.
- Authority, relative age, familiarity and setting as the controlled social cues.

The Romanized message will remain exactly the same within one message family.
Only one selected social-context variable will change in each controlled
comparison.

### 1.3 Core model evaluation

The core evaluation will use:

- Three remotely hosted API models.
- Three prompt conditions.
- Message-only prompting.
- Narrative-context prompting.
- Structured-context prompting.

The complete core experiment will contain:

450 instances × 3 models × 3 prompt conditions = 4,050 model responses.

The specific API models will be selected later according to availability,
reliability, reproducibility and cost.

### 1.4 BanglaMate agent extension

After the core benchmark evaluation is completed and frozen, a controlled
BanglaMate extension will be evaluated.

The extension will use:

- 90 frozen test cases.
- One remotely hosted API model.
- A direct-rewrite baseline.
- A complete four-agent BanglaMate pipeline.
- A no-Critic version of BanglaMate.
- A maximum of one Critic-requested revision.

The four BanglaMate agents will be:

1. Context/Linguist Agent
2. Translator Agent
3. Diplomat Agent
4. Critic Agent

The agent extension cannot change the core dataset, labels, prompts or results.

### 1.5 Work outside the scope

This thesis will not:

- Train a new foundation model.
- Fine-tune an existing language model.
- Run a large language model locally.
- Build a knowledge graph.
- Build an unrestricted agent loop.
- Build a production mobile or web application.
- Claim to represent every Bangla dialect or social relationship.
- Use private messages without consent.

### 1.6 Order of execution

The work will be completed in this order:

1. Freeze the research protocol.
2. Create and validate the benchmark.
3. Complete human annotation.
4. Freeze development and test splits.
5. Develop prompts using only development data.
6. Run and analyze the core experiments.
7. Record CORE_RESULTS_FROZEN.
8. Implement and evaluate the BanglaMate extension.
9. Record EXTENSION_RESULTS_FROZEN.
10. Write, audit and submit the thesis.

## 2. Dataset Units and Counterfactual Design

### 2.1 Message family

A message family is a group containing one Romanized Bangla message and
three different social-context variants.

Every message family will have a unique identifier such as:

- F001
- F002
- F003

The same Romanized message must be used in all three variants of a family.

Example message:

`kalke report ta niye kotha bola jabe?`

A message family does not need to contain one Tui, one Tumi and one Apni
instance. The appropriate labels will be determined later through human
annotation rather than being forced during dataset construction.

### 2.2 Instance

An instance is one complete research record containing:

- One Romanized Bangla message.
- One social-context record.
- One unique instance identifier.
- One message-family identifier.
- All required social-context fields.
- Human annotation fields, which will be completed later.

Every message family will contain three instances:

- Variant A
- Variant B
- Variant C

Example identifiers:

- F001-A
- F001-B
- F001-C

Therefore:

150 message families × 3 instances per family = 450 total instances.

The instance is the basic unit that will be sent to a model during the
experiment.

### 2.3 Baseline context A

Variant A is the baseline context for a message family.

It contains the original combination of:

- Authority relation
- Relative age
- Familiarity
- Setting

The `changed_cue_from_A` value for Variant A will be `NONE`.

### 2.4 Counterfactual context B

Variant B will be created by copying Variant A and changing exactly one
approved social cue.

Every other field must remain unchanged.

The `changed_cue_from_A` field must record which cue changed.

Example:

- Variant A authority: EQUAL
- Variant B authority: HIGHER
- All other context fields remain unchanged
- `changed_cue_from_A`: AUTHORITY

### 2.5 Counterfactual context C

Variant C will also be created from Variant A.

It will return to all of Variant A's original values and change one different
approved social cue.

Example:

- Variant A familiarity: MEDIUM
- Variant C familiarity: HIGH
- All other context fields remain unchanged
- `changed_cue_from_A`: FAMILIARITY

### 2.6 Controlled comparison

A controlled comparison contains two instances where:

1. The Romanized message is exactly identical.
2. Exactly one approved social cue changes.
3. Every other experimental field remains unchanged.
4. The changed cue is recorded explicitly.

The primary controlled comparisons in each family are:

- A compared with B
- A compared with C

B compared with C is not automatically a controlled comparison because B
and C may differ in two social cues.

### 2.7 Structural example

| Field | F001-A | F001-B | F001-C |
|---|---|---|---|
| `message_family_id` | F001 | F001 | F001 |
| `instance_id` | F001-A | F001-B | F001-C |
| `romanized_message` | kalke report ta niye kotha bola jabe? | kalke report ta niye kotha bola jabe? | kalke report ta niye kotha bola jabe? |
| `authority_relation` | EQUAL | HIGHER | EQUAL |
| `relative_age` | SIMILAR | SIMILAR | SIMILAR |
| `familiarity` | MEDIUM | MEDIUM | HIGH |
| `setting` | SEMI_FORMAL | SEMI_FORMAL | SEMI_FORMAL |
| `changed_cue_from_A` | NONE | AUTHORITY | FAMILIARITY |

In this example:

- F001-A compared with F001-B changes authority only.
- F001-A compared with F001-C changes familiarity only.
- F001-B compared with F001-C changes both authority and familiarity.
- Therefore, F001-B compared with F001-C is not used as a primary controlled comparison.

This table is a structural example only. It does not assign final Tui, Tumi
or Apni labels. Human annotators will determine the labels later.

### 2.8 Message identity rule

Within one message family, the value of `romanized_message` must be exactly
identical across A, B and C.

The following differences are not permitted within the same family:

- Spelling changes
- Capitalization changes
- Punctuation changes
- Added or removed words
- Whitespace differences
- Changed verb forms
- Changed pronouns

If the message needs correction, it must be corrected in all three instances
before annotation begins.

### 2.9 Validity conditions

A message family is structurally valid only when:

- It has exactly three instances.
- Its instance IDs are unique.
- All three instances use the same `message_family_id`.
- The Romanized message is identical in A, B and C.
- B changes exactly one social cue from A.
- C changes exactly one different social cue from A.
- The changed cues use approved categorical values.
- `changed_cue_from_A` correctly describes the change.
- No required context field is missing.

If any of these conditions fail, the family must be corrected or excluded
before annotation.

## 3. Context Variables and Allowed Values

### 3.1 General rule

Every dataset instance must use the exact field names and allowed categorical
values defined in this section.

Different spellings or alternative descriptions must not be used for fields
that will be analyzed statistically.

For example, the authority value must be recorded as `HIGHER`, not as:

- High
- Senior
- Boss
- More powerful
- Higher authority person

The four controlled social cues are:

1. Authority relation
2. Relative age
3. Familiarity
4. Setting

All four social cues must have valid values in every dataset instance.
Blank and unknown values are not allowed for the primary benchmark.

If a cue cannot be determined from the scenario, the instance must be
rewritten or excluded.

### 3.2 Identification fields

| Field | Type | Allowed values or format | Purpose |
|---|---|---|---|
| `message_family_id` | Text ID | F001 to F150 | Identifies the message family |
| `instance_id` | Text ID | F001-A, F001-B, F001-C, etc. | Identifies one instance |
| `variant` | Category | A, B, C | Identifies the context variant |
| `romanized_message` | Text | Romanized Bangla message | Message shown to models |
| `changed_cue_from_A` | Category | NONE, AUTHORITY, AGE, FAMILIARITY, SETTING | Records the cue changed from A |

Variant A must always use:

`changed_cue_from_A = NONE`

Variant B and Variant C must each use one of:

- AUTHORITY
- AGE
- FAMILIARITY
- SETTING

Variant B and Variant C must change different cues from Variant A.

### 3.3 Authority relation

Field name:

`authority_relation`

Allowed values:

| Value | Meaning |
|---|---|
| `LOWER` | Recipient has lower authority than the speaker |
| `EQUAL` | Recipient and speaker have approximately equal authority |
| `HIGHER` | Recipient has higher authority than the speaker |

Authority is always recorded from the recipient's position relative to the
speaker.

Example:

- A student speaking to a teacher: `HIGHER`
- A teacher speaking to a student: `LOWER`
- One classmate speaking to another classmate: `EQUAL`

Authority does not automatically determine the final Tui, Tumi or Apni label.
Human annotators will consider all available social information.

### 3.4 Relative age

Field name:

`relative_age`

Allowed values:

| Value | Meaning |
|---|---|
| `YOUNGER` | Recipient is meaningfully younger than the speaker |
| `SIMILAR` | Recipient and speaker are approximately similar in age |
| `OLDER` | Recipient is meaningfully older than the speaker |

Age is always recorded from the recipient's position relative to the speaker.

Example:

- A 20-year-old speaking to a 45-year-old: `OLDER`
- A 45-year-old speaking to a 20-year-old: `YOUNGER`
- Two university classmates of similar age: `SIMILAR`

Exact numerical ages do not need to be included unless they are necessary
to understand the scenario.

### 3.5 Familiarity

Field name:

`familiarity`

Allowed values:

| Value | Meaning |
|---|---|
| `LOW` | Stranger, first meeting or very limited personal familiarity |
| `MEDIUM` | Acquaintance, regular contact or moderately familiar relationship |
| `HIGH` | Close friend, close relative or strongly familiar relationship |

Familiarity describes the personal relationship between the speaker and the
recipient.

Examples:

- Speaking to an unknown shopkeeper: `LOW`
- Speaking to a regularly contacted classmate: `MEDIUM`
- Speaking to a very close childhood friend: `HIGH`

Familiarity must not be determined only from the amount of time two people
have known each other. The closeness of the relationship must also be
considered.

### 3.6 Setting

Field name:

`setting`

Allowed values:

| Value | Meaning |
|---|---|
| `INFORMAL` | Casual, personal or relaxed communication |
| `SEMI_FORMAL` | Moderately structured communication without strict formality |
| `FORMAL` | Official, professional, institutional or ceremonially respectful communication |

Examples:

- Casual conversation at home: `INFORMAL`
- Ordinary class-group communication: `SEMI_FORMAL`
- Formal communication with a department head: `FORMAL`

Setting describes the communication situation. It does not describe the
physical location alone.

For example, communication inside an office is not automatically `FORMAL`.
Two close colleagues may communicate informally while physically present
in an office.

### 3.7 Domain

Field name:

`domain`

Allowed values:

| Value | Meaning |
|---|---|
| `ACADEMIC` | University, school, teaching, supervision or coursework |
| `PROFESSIONAL` | Workplace, employment, office or organizational communication |
| `FAMILY` | Communication between family members or relatives |
| `FRIENDSHIP` | Communication between friends or socially close peers |
| `SERVICE_PUBLIC` | Shops, transportation, healthcare, customer service or public offices |
| `ONLINE_COMMUNITY` | Online groups, forums, social communities or moderated spaces |

Domain is used to measure dataset coverage. It is not one of the four
controlled social cues.

All three instances in one message family must use the same domain.

### 3.8 Communicative intention

Field name:

`intent`

Allowed values:

| Value | Meaning |
|---|---|
| `REQUEST` | Asking someone to do something |
| `QUESTION` | Requesting information |
| `REMINDER` | Reminding someone about a task or event |
| `APOLOGY` | Expressing regret |
| `INVITATION` | Inviting someone to an event or activity |
| `FOLLOW_UP` | Checking the status of earlier communication |
| `INFORMATION` | Providing information |
| `FEEDBACK` | Giving or requesting feedback |
| `CONFIRMATION` | Confirming a plan, decision or event |
| `OTHER_DOCUMENTED` | A justified intention not covered by the main categories |

If `OTHER_DOCUMENTED` is used, a short explanation must be recorded.

All three instances in one message family must have the same communicative
intention.

### 3.9 Speaker and recipient roles

Field names:

- `speaker_role`
- `recipient_role`

Recommended role values include:

- STUDENT
- TEACHER
- SUPERVISOR
- COLLEAGUE
- EMPLOYEE
- MANAGER
- FRIEND
- SIBLING
- PARENT
- RELATIVE
- CUSTOMER
- SERVICE_WORKER
- DRIVER
- SHOPKEEPER
- DOCTOR
- PATIENT
- OFFICIAL
- MODERATOR
- COMMUNITY_MEMBER
- OTHER_DOCUMENTED

If `OTHER_DOCUMENTED` is used, the role must be explained in a separate note.

Speaker and recipient roles provide context but are not treated as separate
experimental social cues.

The roles should normally remain unchanged across A, B and C. If changing a
role also changes authority, age, familiarity or setting, the family must be
reviewed carefully to ensure that only the designated experimental cue has
changed.

### 3.10 Source register

Field name:

`source_register`

Allowed values:

| Value | Meaning |
|---|---|
| `TUI` | Original message already contains clear Tui-form language |
| `TUMI` | Original message already contains clear Tumi-form language |
| `APNI` | Original message already contains clear Apni-form language |
| `MIXED` | Original message contains more than one register form |
| `UNCLEAR` | Original message does not clearly reveal a register |

`source_register` describes the language already present in the Romanized
message. It is not the final human gold label.

The field will later help measure whether a model genuinely uses social
context or simply copies the register already present in the message.

Because the Romanized message is identical within a family, `source_register`
must also remain identical across A, B and C.

### 3.11 Fields that must remain unchanged within a family

The following fields must remain unchanged across A, B and C:

- `message_family_id`
- `romanized_message`
- `domain`
- `intent`
- `source_register`
- Normally `speaker_role`
- Normally `recipient_role`

For each controlled comparison, all non-target social cues must also remain
unchanged.

Only the cue named in `changed_cue_from_A` may differ from Variant A.

### 3.12 Invalid field examples

The following entries are invalid:

| Field | Invalid entry | Correct form |
|---|---|---|
| `authority_relation` | Boss | HIGHER |
| `authority_relation` | Same level | EQUAL |
| `relative_age` | 45 years | OLDER, YOUNGER or SIMILAR |
| `familiarity` | Known for two years | LOW, MEDIUM or HIGH |
| `setting` | Office | INFORMAL, SEMI_FORMAL or FORMAL |
| `domain` | University teacher | ACADEMIC |
| `changed_cue_from_A` | Authority changed | AUTHORITY |

The descriptive details may appear in contextual notes, but the analytical
fields must use the approved categorical values.

### 3.13 Context-variable validation rules

An instance passes context-variable validation only when:

- Every required field exists.
- No required value is blank.
- Every categorical value belongs to the approved list.
- Authority and age are recorded from the recipient's position.
- Domain and intent remain unchanged within a family.
- Source register remains unchanged within a family.
- Variant A uses `changed_cue_from_A = NONE`.
- Variants B and C record valid and different changed cues.
- Each controlled comparison changes exactly one social cue.

### 4.9 Acceptable register set

The acceptable register set will be created automatically from the annotation.

Example 1:

```text
primary_register = APNI
secondary_register = NONE
acceptable_registers = [APNI]
```

Example 2:

```text
primary_register = TUMI
secondary_register = APNI
acceptable_registers = [TUMI, APNI]
```

A model prediction will count as acceptable-set correct if it belongs to the
approved acceptable-register set.

Primary-label accuracy and acceptable-set accuracy will be reported
separately.

### 4.10 Confidence

Field name:

`confidence`

Allowed values:

| Value | Meaning |
|---|---|
| `HIGH` | The annotator is confident that the decision is appropriate |
| `MEDIUM` | The decision is reasonable, but some social variation is possible |
| `LOW` | Important uncertainty remains and the instance should be reviewed |

Confidence does not replace the primary register.

For example, the following is invalid:

```text
primary_register = UNSURE
```

The correct approach is:

```text
primary_register = TUMI
confidence = LOW
```

If the scenario cannot reasonably be answered, the annotator should use the
appropriate answerability status instead of forcing a register label.

### 4.11 Answerability status

Field name:

`answerability_status`

Allowed values:

| Value | Meaning |
|---|---|
| `ANSWERABLE` | Enough consistent context exists to choose a register |
| `UNDERSPECIFIED` | Important information is missing |
| `CONTRADICTORY` | Context fields conflict with one another |
| `CULTURALLY_CONTENTIOUS` | Genuine cultural or social disagreement is likely |
| `EXCLUDE` | The instance is unsuitable for the benchmark |

Rules:

- `ANSWERABLE` instances must have a primary register.
- Non-answerable instances may leave the primary register blank temporarily.
- Non-answerable instances must contain a short explanatory note.
- Every non-answerable instance must be reviewed before dataset freeze.
- An instance must not enter the final test set without a resolved decision.
- Structurally weak instances should be rewritten or excluded rather than
  receiving an artificial gold label.

### 4.12 Reason codes

Field name:

`reason_codes`

One or more of the following values may be selected:

| Code | Meaning |
|---|---|
| `AUTHORITY` | Authority difference influenced the decision |
| `AGE` | Relative age influenced the decision |
| `FAMILIARITY` | Personal familiarity influenced the decision |
| `SETTING` | Communication setting influenced the decision |
| `KINSHIP` | Family or kinship relationship influenced the decision |
| `ROLE` | Speaker or recipient role influenced the decision |
| `EMOTIONAL_STANCE` | Affection, anger, distance or another emotional factor influenced the decision |
| `MESSAGE_FORM` | Existing wording of the message influenced the interpretation |
| `MISSING_CONTEXT` | Necessary contextual information is absent |
| `CONTRADICTION` | Context fields conflict |
| `CULTURAL_VARIATION` | Multiple interpretations may reflect genuine cultural variation |
| `OTHER` | Another documented reason influenced the decision |

If `OTHER` is selected, a short note is required.

Reason codes provide short, auditable evidence. Annotators should not normally
write long free-text explanations.

### 4.13 Short annotation note

Field name:

`annotation_note`

A short note is optional for ordinary high-confidence answerable cases.

A note is required when:

- Confidence is `LOW`.
- Answerability is not `ANSWERABLE`.
- `OTHER` is selected as a reason code.
- The annotator identifies a possible error.
- The context contains an unusual relationship.
- The secondary register needs clarification.

The note should explain the uncertainty briefly without including private or
personally identifying information.

### 4.14 Source register versus annotated register

The following fields have different meanings:

| Field | Meaning |
|---|---|
| `source_register` | Register form already present in the original Romanized message |
| `primary_register` | Register judged most appropriate for the described social context |
| `secondary_register` | Another register that is also acceptable |

These fields may differ.

Example:

```text
source_register = APNI
primary_register = TUMI
secondary_register = NONE
```

This means that the original message uses an Apni-style form, but the human
annotator believes Tumi is more appropriate for the supplied context.

This difference is important because the study will measure whether models
use social context or merely copy the message's existing register.

### 4.15 Required annotation fields

Every annotation record must contain:

| Field | Required? |
|---|---|
| `instance_id` | Yes |
| `annotator_id` | Yes |
| `primary_register` | Yes when answerable |
| `secondary_register` | Yes; use NONE when absent |
| `confidence` | Yes |
| `answerability_status` | Yes |
| `reason_codes` | Yes |
| `annotation_note` | Required for flagged cases |
| `annotation_guide_version` | Yes |
| `annotation_timestamp` | Yes |

Annotator identities will use non-identifying codes such as:

- `ANN_A`
- `ANN_B`
- `ADJUDICATOR`

Personal names should not be placed in the public or shareable dataset.

### 4.16 Example annotation record

Example context:

- Speaker is a university student.
- Recipient has higher authority.
- Recipient is older.
- Familiarity is low.
- Setting is formal.

Example annotation:

```text
instance_id = F025-B
annotator_id = ANN_A
primary_register = APNI
secondary_register = NONE
confidence = HIGH
answerability_status = ANSWERABLE
reason_codes = [AUTHORITY, AGE, SETTING]
annotation_note =
annotation_guide_version = 1.0
annotation_timestamp = YYYY-MM-DD HH:MM
```

This is an illustrative example only. It will not be used as a benchmark
instance or model demonstration.

### 4.17 Annotation validation rules

An annotation passes basic validation only when:

- `annotator_id` exists.
- The answerability value belongs to the approved list.
- Every answerable instance has one primary register.
- The primary register is TUI, TUMI or APNI.
- The secondary register is valid or NONE.
- Primary and secondary registers are different.
- A maximum of one secondary register is selected.
- Confidence is HIGH, MEDIUM or LOW.
- At least one reason code is present.
- A note exists whenever the protocol requires one.
- The annotation guide version is recorded.
- The timestamp is recorded.

## 5. Instance Review, Revision, and Exclusion Rules

### 5.1 Purpose

Every candidate dataset instance must be reviewed before it enters the frozen
benchmark.

An instance must not be retained merely because it supports the researcher's
expected Tui, Tumi or Apni label.

If the supplied context does not support a reliable decision, the instance
must be revised, adjudicated or excluded.

### 5.2 Answerability status versus review action

The following fields serve different purposes:

| Field | Meaning |
|---|---|
| `answerability_status` | Annotator's judgment about whether the instance can be answered |
| `review_action` | Researcher's documented decision about what to do with the instance |

Allowed `review_action` values are:

| Value | Meaning |
|---|---|
| `KEEP` | Instance is valid and may remain in the dataset |
| `REVISE` | Instance requires correction and revalidation |
| `ADJUDICATE` | Instance requires another qualified review |
| `EXCLUDE` | Instance will not enter the final benchmark |

`ADJUDICATE` is a temporary action. After adjudication, the final action must
be `KEEP`, `REVISE` or `EXCLUDE`.

### 5.3 Structural problems

An instance or message family must be revised when:

- The family does not contain exactly three instances.
- An instance ID is missing or duplicated.
- A message-family ID is missing or duplicated.
- A, B and C do not use exactly the same Romanized message.
- Variant B changes more than one cue from A.
- Variant C changes more than one cue from A.
- B and C change the same cue from A.
- `changed_cue_from_A` does not match the actual changed field.
- A categorical value does not belong to the approved list.
- A required field is blank.
- Comparison IDs refer to nonexistent instances.

If a structural error cannot be corrected without redesigning the family,
the complete family must be excluded.

### 5.4 Underspecified context

Use:

`answerability_status = UNDERSPECIFIED`

when important information required for the register decision is missing.

Examples include:

- The relationship between speaker and recipient is unclear.
- Authority information is missing.
- Familiarity is not described sufficiently.
- The setting cannot be determined.
- A family relationship is mentioned without enough information about closeness.
- The decision depends on information that exists only in the researcher's mind.

Recommended action:

1. Identify the missing information.
2. Add only the minimum necessary contextual information.
3. Confirm that the correction does not change an unintended cue.
4. Revalidate all three instances in the family.
5. Send the revised instance for fresh annotation.

Do not use a secondary acceptable label merely to hide missing context.

### 5.5 Contradictory context

Use:

`answerability_status = CONTRADICTORY`

when two or more parts of the context conflict.

Examples include:

- The recipient is described as both younger and older.
- The recipient is described as a stranger but familiarity is `HIGH`.
- The setting is described as an official hearing but marked `INFORMAL`.
- The narrative says the recipient is the speaker's supervisor while
  `authority_relation = LOWER`.
- The changed-cue field says `AGE`, but authority is the field that changed.

Recommended action:

1. Identify the conflicting fields.
2. Determine whether the contradiction is a data-entry error.
3. Correct the error only when the intended context is clear.
4. Record the original and corrected values.
5. Revalidate the complete family.
6. Exclude the family if the intended context cannot be recovered.

### 5.6 Culturally contentious cases

Use:

`answerability_status = CULTURALLY_CONTENTIOUS`

when the context is complete and consistent but qualified native speakers
may reasonably disagree because of genuine social or cultural variation.

Examples may include:

- Tui versus Tumi between close siblings.
- Tumi versus Apni between familiar colleagues of different ages.
- Register choice involving regional or family-specific norms.
- Relationships where affection and hierarchy provide conflicting signals.

Recommended action:

1. Request independent review from another qualified native Bangla speaker.
2. Record the competing interpretations.
3. Determine whether one register is preferable and another is acceptable.
4. Use the optional secondary register when both are genuinely acceptable.
5. Keep the case only when its ambiguity can be represented transparently.
6. Exclude it from the primary analysis if no defensible interpretation can
   be established.
7. Optionally archive it as an exploratory example.

Cultural disagreement must not automatically be treated as annotation failure.

### 5.7 Linguistic naturalness

A candidate must be revised or excluded when:

- The Romanized Bangla is not understandable.
- The wording appears machine-translated.
- The message uses an unrealistic sentence structure.
- The wording is unnecessarily long or artificial.
- It contains an unnatural mixture of formal and intimate forms.
- It requires hidden background information.
- It contains obvious placeholder text.
- It does not resemble a plausible digital message.

Minor natural Romanized spelling variation is permitted.

The researcher must not silently convert every message into standardized
Bangla spelling. Natural variation may be preserved when the meaning remains
clear.

A native Bangla speaker who did not draft the candidate messages should
review a sample for naturalness.

### 5.8 Code-mixing rules

The message must remain primarily Romanized Bangla.

Use the following code-mixing levels:

| English lexical-token proportion | `code_mix_level` |
|---|---|
| 0%–5% | `NONE` |
| Above 5%–15% | `LIGHT` |
| Above 15%–30% | `MODERATE` |
| Above 30% | `REVIEW_OR_EXCLUDE` |

Rules:

- A complete English clause should normally be revised or excluded.
- Common technical terms may remain when they are natural in the domain.
- Any exception above the 30% limit must be documented before annotation.
- The same message must have the same English-token ratio in A, B and C.
- Code-mixing must not be silently corrected after annotation.
- Code-mixing level must be recorded for later analysis.

Example of a potentially acceptable technical term:

```text
assignment ta submit kora hoyeche?
```

Example requiring review:

```text
Could you please submit the assignment before tomorrow?
```

The second example is primarily English rather than Romanized Bangla.

### 5.9 Privacy and ethical exclusion

A candidate must be revised or excluded when it contains:

- A real private person's full name.
- A private phone number.
- A private email address.
- A private home address.
- A student ID, employee ID or account number.
- A copied private conversation without consent.
- Confidential academic, medical or workplace information.
- Information that could identify an annotator.
- Harmful personal allegations.
- Unnecessary sensitive personal information.

Use role-based or fictional descriptions instead.

Examples:

| Unsafe content | Safer replacement |
|---|---|
| Real teacher's full name | `TEACHER` or a fictional name |
| Real phone number | Remove the number |
| Exact private workplace issue | Use a fictional professional scenario |
| Annotator's real name | `ANN_A` or `ANN_B` |

A private GitHub repository does not remove the responsibility to protect
personal information.

### 5.10 Duplicate and template-like content

A candidate must be reviewed when:

- Its message is identical to another family's message.
- Its context is nearly identical to another family.
- Only one or two words distinguish many candidate messages.
- AI-generated candidates repeatedly use the same sentence structure.
- One domain or communicative intention appears too frequently.
- Multiple examples test effectively the same social contrast.

Use exact-text and approximate-duplicate checking before dataset freeze.

When duplicates are detected:

1. Keep the clearer and more natural family.
2. Rewrite the weaker family into a genuinely different scenario.
3. Exclude it if a meaningful distinction cannot be created.

### 5.11 Stereotype and label-obviousness review

A candidate must be revised or excluded when:

- It relies on gender, class, occupation, age or regional stereotypes.
- It suggests that every older person must receive Apni.
- It suggests that every younger person must receive Tui.
- It makes the expected label obvious through an artificial description.
- It is designed only to force the researcher's preferred result.
- It portrays a social group unnecessarily negatively.
- Its expected answer depends on offensive or harmful assumptions.

The context should provide relevant social information without directly
telling the annotator which register to select.

Invalid example:

```text
The recipient is very respected, so the speaker must use Apni.
```

Better approach:

```text
The recipient has higher institutional authority, familiarity is low,
and the communication occurs in a formal setting.
```

The second version supplies context without directly revealing the label.

### 5.12 Revision record

Every material revision must be documented.

The revision record should contain:

| Field | Meaning |
|---|---|
| `issue_id` | Unique issue identifier |
| `message_family_id` | Affected family |
| `instance_id` | Affected instance or ALL |
| `issue_type` | Structural, linguistic, privacy, ambiguity, duplicate, etc. |
| `detected_by` | Validator, researcher, annotator or reviewer |
| `original_value` | Value before revision |
| `revised_value` | Value after revision |
| `revision_reason` | Why the change was necessary |
| `review_action` | KEEP, REVISE, ADJUDICATE or EXCLUDE |
| `reviewer_id` | Person who approved the action |
| `review_timestamp` | Date and time |
| `requires_reannotation` | YES or NO |

No material revision may be performed without a record.

### 5.13 Family-level revision rule

The message family is the main counterfactual unit.

Therefore, when any instance in a family changes:

1. Recheck all three instance IDs.
2. Recheck message identity across A, B and C.
3. Recalculate which fields differ.
4. Revalidate A-B.
5. Revalidate A-C.
6. Recalculate code-mixing information if the message changed.
7. Review the source-register value.
8. Determine whether previous annotations are still valid.
9. Reannotate the complete affected family when the message or social
   interpretation changes.

Do not repair only one row and assume the remaining family is still valid.

### 5.14 Timing of revisions

Before annotation freeze:

- Structural and linguistic problems may be corrected.
- Corrections must be logged.
- Materially changed cases must be reannotated.

After dataset freeze:

- The frozen dataset must not be silently changed.
- A correction requires a new dataset version.
- The reason and affected results must be documented.
- Checksums and split files must be regenerated.
- The supervisor must approve major changes.

After inspecting test results:

- Do not revise cases merely because a model performed poorly.
- Do not remove difficult cases merely to improve accuracy.
- A genuine data error may be corrected only through a documented amendment.
- The affected analysis must be labelled appropriately.

### 5.15 Example review decisions

| Situation | Answerability | Review action |
|---|---|---|
| One required context field is missing | UNDERSPECIFIED | REVISE |
| Narrative and structured fields conflict | CONTRADICTORY | REVISE |
| Two registers are genuinely acceptable | ANSWERABLE or CULTURALLY_CONTENTIOUS | ADJUDICATE |
| Message contains a real phone number | EXCLUDE temporarily | REVISE or EXCLUDE |
| Message differs between A, B and C | Not applicable | REVISE |
| More than one cue changes from A | Not applicable | REVISE |
| Primarily English message | EXCLUDE | REVISE or EXCLUDE |
| Serious unresolved cultural disagreement | CULTURALLY_CONTENTIOUS | EXCLUDE from primary analysis |
| Natural minor Romanized spelling variation | ANSWERABLE | KEEP |
| Model gives an incorrect answer | Not a dataset problem | KEEP |

A model error is not automatically evidence that the dataset instance is
incorrect.

### 5.16 Final instance acceptance checklist

An instance may enter the final benchmark only when:

- It passes structural validation.
- Its context is sufficiently specified.
- Its fields do not contradict one another.
- Its Romanized Bangla is understandable and natural.
- It follows the code-mixing rule.
- It contains no private information.
- It is not an unjustified duplicate.
- It does not rely on harmful stereotypes.
- Its family retains one-cue counterfactual control.
- Required revisions are documented.
- Required reannotation is complete.
- Its final review action is `KEEP`.

## 6. Human Annotation Design

### 6.1 Annotation design summary

The benchmark will use two native Bangla annotators.

The annotation design is:

| Activity | Annotator A | Annotator B |
|---|---:|---:|
| Qualification controls | 12 | 12 |
| Pilot annotation | 45 instances | 45 instances |
| Final benchmark annotation | All 450 instances | Frozen 150-instance subset |
| Additional flagged cases | When required | When required |
| Extension-output rating | Defined separately | Defined separately |

Annotator B's primary reliability subset will contain 50 complete message
families:

50 families × 3 instances = 150 instances.

This design reduces annotation workload while preserving an independently
annotated subset for agreement analysis.

It is less rigorous than having both annotators label all 450 instances.
This limitation must be disclosed in the thesis and approved by the
supervisor.

### 6.2 Annotator eligibility

An annotator should:

- Be an adult native or highly proficient Bangla speaker.
- Understand ordinary Bangladeshi social relationships.
- Be comfortable reading Romanized Bangla.
- Understand the difference between Tui, Tumi and Apni.
- Be able to work independently.
- Provide informed consent.
- Agree not to share the dataset before its release.
- Have no financial or personal interest in producing a particular result.

An annotator does not need to be:

- A machine-learning expert.
- A programmer.
- A linguistics researcher.
- Familiar with the evaluated language models.

An AI system cannot serve as an official human annotator.

### 6.3 Researcher participation

Whenever possible, the two annotators should not be the same person who
created most of the dataset.

If the researcher must act as Annotator A because of limited resources:

- This must be approved by the supervisor.
- The researcher role must be disclosed in the thesis.
- Annotator B must remain independent.
- The frozen 150-instance subset must be selected before Annotator B sees it.
- Annotator B must not see the researcher's labels.
- Disagreements must be recorded transparently.
- Stronger independent review should be used for low-confidence cases.

The researcher must not change an instance merely because Annotator B
disagrees with the researcher's expected label.

### 6.4 Annotator identifiers

Real names will not appear in the research dataset.

Use:

- `ANN_A`
- `ANN_B`
- `ADJUDICATOR`

A separate private consent record may connect these codes to real identities.

The identity file must be stored outside the shareable dataset in:

`data/private/`

The private identity file must not be pushed to GitHub because the
`data/private/` directory is excluded by `.gitignore`.

### 6.5 Annotator information and consent

Before annotation, each annotator must receive a short information sheet
explaining:

- The purpose of the research.
- What they will be asked to do.
- Approximate time required.
- That participation is voluntary.
- Whether compensation will be provided.
- How their identity will be protected.
- That they may stop participating.
- That the messages are synthetic, fictional or safely documented.
- How their anonymized annotations may be used in the thesis.

Consent must be collected before qualification or annotation begins.

The consent procedure must follow university and supervisor requirements.

### 6.6 Qualification controls

Each annotator must independently complete 12 clear qualification items.

Qualification items must:

- Be separate from the pilot and final dataset.
- Never appear in development or test data.
- Contain enough context for a clear decision.
- Include examples of Tui, Tumi and Apni.
- Include examples from more than one domain.
- Have reference answers established before annotator recruitment.
- Test whether the annotator understands primary and secondary labels.
- Test whether the annotator can identify missing or contradictory context.

Passing requirement:

- At least 10 correct primary labels out of 12.
- No systematic confusion between one label pair.
- Correct understanding of the annotation instructions.

If an annotator fails:

1. Explain the misunderstood rules.
2. Provide separate practice examples.
3. Do not reveal answers to future qualification items.
4. Give one new qualification attempt using different examples.
5. Replace the annotator if the second attempt also fails.

Qualification responses must not be included in benchmark agreement
statistics.

### 6.7 Pilot annotation

The pilot will contain:

15 message families × 3 instances = 45 instances.

Both Annotator A and Annotator B will independently annotate all 45 pilot
instances.

Pilot procedure:

1. Give both annotators the same frozen pilot file.
2. Give both annotators the same annotation-guide version.
3. Randomize item order separately for each annotator.
4. Do not show family adjacency when practical.
5. Do not show one annotator's answers to the other.
6. Do not show model predictions.
7. Do not show researcher-expected labels.
8. Allow questions about the procedure, but do not coach individual answers.
9. Save each annotator's raw responses separately.
10. Validate that every required annotation field is present.
11. Calculate agreement before adjudication.
12. Categorize disagreements.
13. Revise the annotation guide when necessary.
14. Run another small pilot if serious misunderstanding remains.

Pilot annotations are used to improve the annotation guide. They do not
automatically become final gold annotations.

If a pilot family is later included in the full benchmark, it must pass all
final validation rules and be annotated under the frozen final annotation
guide.

### 6.8 Annotator A full-dataset assignment

Annotator A will independently annotate all:

150 families × 3 instances = 450 instances.

Annotator A must:

- Use the frozen annotation guide.
- Receive instances in randomized order.
- Annotate without seeing model outputs.
- Annotate without seeing dataset-designer predictions.
- Complete all required fields.
- Work in several manageable sessions.
- Save progress after every session.
- Avoid discussing individual answers with Annotator B.
- Mark uncertain or problematic cases rather than guessing.

Recommended session size:

- Approximately 50–75 instances per session.
- Take a break between sessions.
- Avoid completing all 450 instances in one sitting.

### 6.9 Annotator B frozen subset

Annotator B will independently annotate 50 complete message families:

50 families × 3 instances = 150 instances.

The subset-selection process must:

1. Start from the structurally valid full dataset.
2. Select complete families, not individual rows.
3. Use a recorded random seed.
4. Include every domain.
5. Represent all four changed-cue types.
6. Avoid selecting according to model results.
7. Avoid selecting only easy or obvious cases.
8. Occur before Annotator B sees any full-dataset labels.
9. Produce a saved list of selected family IDs.
10. Produce a checksum or frozen version identifier.

The selected IDs will later be saved in a file such as:

`data/annotations/annotator_b_family_ids.txt`

The file will contain 50 family IDs, for example:

```text
F003
F009
F012
F017
...
```

The actual family IDs will be generated later after the full dataset exists.
They are not selected during Phase 1.

### 6.10 Stratification of Annotator B's subset

Annotator B's subset should be approximately balanced across the six domains.

A suitable target is:

| Domain | Approximate families |
|---|---:|
| Academic | 8–10 |
| Professional | 7–9 |
| Family | 7–9 |
| Friendship | 7–9 |
| Service/Public | 7–9 |
| Online Community | 7–9 |
| Total | 50 |

The exact allocation may follow the final dataset distribution.

The selection report must state:

- Random seed.
- Number of families from each domain.
- Number of comparisons for each cue type.
- Number of instances.
- Date of selection.
- Dataset version used.

Do not use model accuracy or model error categories when selecting the
annotation subset.

### 6.11 Independence rules

During independent annotation:

- Annotator A must not see Annotator B's labels.
- Annotator B must not see Annotator A's labels.
- Neither annotator may see model predictions.
- Neither annotator may see BanglaMate outputs.
- Neither annotator may see hidden researcher-expected labels.
- Annotators must not discuss individual cases before submitting their files.
- Each annotator must receive independently randomized item order.
- Raw annotation files must be stored separately.

Questions about file access, field meanings or the annotation interface are
allowed.

Questions such as the following must not be answered during independent
annotation:

> Should this particular example be Apni?

That question would influence the annotation decision.

### 6.12 Raw annotation files

Raw annotation files will be stored separately.

Recommended paths:

```text
data/annotations/raw/ANN_A.csv
data/annotations/raw/ANN_B.csv
```

Raw annotation files must:

- Preserve the original submitted answers.
- Never be silently overwritten.
- Include the annotation-guide version.
- Include timestamps.
- Include all confidence and answerability fields.
- Be backed up after every completed session.
- Remain separate from adjudicated gold labels.

Corrections to accidental data-entry mistakes must be recorded separately.

### 6.13 Agreement calculation

Agreement will be calculated using only cases independently annotated by both
Annotator A and Annotator B.

Agreement measures will include:

- Exact primary-label agreement.
- Cohen's kappa for primary labels.
- Acceptable-register-set overlap.
- Agreement by Tui, Tumi and Apni.
- Agreement by changed-cue type.
- Agreement by domain.
- Number and percentage of low-confidence cases.

Agreement must be calculated before adjudication.

Do not calculate agreement using the final adjudicated labels because
adjudication would artificially increase agreement.

A pilot Cohen's kappa below 0.60 will trigger a review of:

- Annotation instructions.
- Label prevalence.
- Missing context.
- Contradictory fields.
- Systematic label confusion.
- Genuine cultural variation.

The value 0.60 is a review trigger, not an automatic publication threshold
and not permission to remove difficult cases.

### 6.14 Acceptable-set overlap

Primary-label agreement alone may underestimate agreement when both
annotators consider more than one register acceptable.

Example:

Annotator A:

```text
primary_register = TUMI
secondary_register = APNI
```

Annotator B:

```text
primary_register = APNI
secondary_register = TUMI
```

Their primary labels differ, but their acceptable sets are identical:

```text
[TUMI, APNI]
```

Therefore, acceptable-set overlap will be reported separately from Cohen's
kappa.

### 6.15 Disagreement categories

Every shared-subset disagreement should be assigned one category:

- `PRIMARY_PREFERENCE_DIFFERENCE`
- `SECONDARY_LABEL_DIFFERENCE`
- `MISSING_CONTEXT`
- `CONTRADICTORY_CONTEXT`
- `CULTURAL_VARIATION`
- `INSTRUCTION_MISUNDERSTANDING`
- `DATA_ENTRY_ERROR`
- `UNNATURAL_MESSAGE`
- `OTHER_DOCUMENTED`

The category should be assigned before determining the final gold label when
possible.

### 6.16 Adjudication procedure

Adjudication occurs only after independent annotations are saved and agreement
is calculated.

Procedure:

1. Create a list of disagreements.
2. Hide unnecessary personal annotator information.
3. Review the message and all context fields.
4. Review both annotations and reason codes.
5. Determine whether the disagreement results from missing information,
   misunderstanding or genuine variation.
6. Preserve both original raw annotations.
7. Assign a final primary register when justified.
8. Add a secondary acceptable register when genuinely appropriate.
9. Revise or exclude structurally weak cases.
10. Record the adjudicator's decision and reason.
11. Reannotate materially revised cases.
12. Save adjudicated labels in a new file.

Recommended adjudication path:

`data/annotations/adjudication.csv`

Recommended gold-data path:

`data/final/gold_v1.0.csv`

The adjudicator must not delete or replace the original raw annotation files.

### 6.17 Cases annotated only by Annotator A

Approximately 300 final benchmark instances will initially have only
Annotator A's annotation.

For those instances:

- Annotator A's label may become the provisional gold label.
- Every low-confidence case must receive additional review.
- Every non-answerable case must receive additional review.
- Every case flagged by a validator must receive additional review.
- Cases containing a secondary label may be sampled for review.
- The researcher should inspect a random quality-control sample.
- Materially revised instances must be reannotated.

The thesis and data card must state clearly that only the frozen 150-instance
subset received two complete independent annotations.

### 6.18 Annotation quality-control files

The annotation process should eventually produce:

```text
docs/ANNOTATION_GUIDE_v1.0.md
data/annotations/qualification/ANN_A.csv
data/annotations/qualification/ANN_B.csv
data/annotations/pilot/ANN_A.csv
data/annotations/pilot/ANN_B.csv
data/annotations/raw/ANN_A.csv
data/annotations/raw/ANN_B.csv
data/annotations/annotator_b_family_ids.txt
data/annotations/adjudication.csv
data/annotations/agreement_report.csv
```

These files will be created in later phases.

Phase 1 only freezes the rules and expected paths.

### 6.19 Estimated annotation workload

Approximate annotation effort is:

| Activity | Annotator A | Annotator B |
|---|---:|---:|
| Qualification | 15–30 minutes | 15–30 minutes |
| Pilot | 45–75 minutes | 45–75 minutes |
| Full annotation | 4–8 hours | 1.5–3 hours |
| Additional review | 1–2 hours | 1–2 hours |

These are planning estimates, not required completion speeds.

Annotators should prioritize accuracy over speed.

### 6.20 Annotation freeze conditions

Human annotation is considered complete only when:

- Qualification results are saved.
- Pilot results and agreement are reported.
- The annotation guide is frozen.
- Annotator A completes all required final instances.
- Annotator B completes the frozen 150-instance subset.
- Raw files are preserved separately.
- Agreement is calculated before adjudication.
- Disagreements are categorized.
- Required adjudication is complete.
- Flagged cases are resolved.
- Gold labels are stored separately from raw labels.
- Annotation limitations are documented.

## 7. Development/Test Split and Data-Leakage Prevention

### 7.1 Purpose of the split

The final benchmark will be divided into:

- A development set used for prompt and configuration development.
- A test set used only for the final frozen evaluation.

The development set is comparable to practice material.

The test set is comparable to an unseen final examination.

Model prompts, demonstrations, parameters and parsing rules may be improved
using development data only.

They must not be improved after observing test-set performance.

### 7.2 Split size

The split will contain:

| Split | Message families | Instances | Percentage |
|---|---:|---:|---:|
| Development | 30 | 90 | 20% |
| Test | 120 | 360 | 80% |
| Total | 150 | 450 | 100% |

Calculation:

```text
Development: 30 families × 3 instances = 90 instances
Test: 120 families × 3 instances = 360 instances
Total: 150 families × 3 instances = 450 instances
```

### 7.3 Family-level splitting

The split must be performed using `message_family_id`.

All three instances of one family must belong to the same split.

Valid example:

```text
F001-A → Development
F001-B → Development
F001-C → Development
```

Invalid example:

```text
F001-A → Development
F001-B → Test
F001-C → Test
```

The invalid example causes data leakage because the same underlying message
appears in both development and test data.

Individual instances must never be randomly split without considering their
message family.

### 7.4 Split timing

The actual split will be created only after:

1. All 150 message families exist.
2. All 450 instances pass structural validation.
3. Human annotation is complete.
4. Required adjudication is complete.
5. The gold dataset version is frozen.
6. No unresolved family-level errors remain.

The split must be created before:

- Prompt demonstrations are selected.
- Models are compared.
- Prompt wording is optimized.
- Final model parameters are selected.
- Core API experiments begin.

### 7.5 Fixed random seed

The split process will use the fixed random seed:

`20260830`

The seed is frozen before the completed dataset and model results are
available.

The researcher must not repeatedly change the random seed to obtain:

- Higher model accuracy.
- Easier test examples.
- More favorable label distributions.
- Better-looking results.
- Fewer difficult cases.

If the selected split has a serious predefined balance failure, limited
family-level swaps may be performed before model experiments.

Every swap must:

- Preserve the 30/120 family counts.
- Preserve family integrity.
- Be performed without model results.
- Be justified only by dataset balance.
- Be recorded in the split report.

### 7.6 Domain allocation

The development set should contain approximately 20% of the families from
every domain.

If the final dataset follows the recommended domain allocation, the target
development counts are:

| Domain | Total families | Development families | Test families |
|---|---:|---:|---:|
| Academic | 30 | 6 | 24 |
| Professional | 25 | 5 | 20 |
| Family | 25 | 5 | 20 |
| Friendship | 25 | 5 | 20 |
| Service/Public | 25 | 5 | 20 |
| Online Community | 20 | 4 | 16 |
| Total | 150 | 30 | 120 |

If final domain counts differ, approximately 20% of each domain should be
allocated to development while maintaining exactly 30 development families.

### 7.7 Additional balance checks

After splitting, compare development and test distributions for:

- Primary register.
- Secondary acceptable register.
- Changed-cue type.
- Source register.
- Domain.
- Communicative intention.
- Code-mixing level.
- Answerability status.
- Confidence level.

Perfectly identical distributions are not required.

However, the development set must contain:

- Examples of Tui, Tumi and Apni.
- Examples involving all four changed-cue types.
- Examples from all six domains.
- More than one source-register category.
- Enough variation for prompt development.

Do not remove naturally difficult cases solely to make the distributions
appear cleaner.

### 7.8 Duplicate and near-duplicate leakage

Before freezing the split, check for:

- Identical messages across different families.
- Near-identical messages across different families.
- Repeated templates with only one replaced word.
- Duplicated contexts.
- Pilot or qualification examples copied into the benchmark.
- Prompt demonstrations that closely reproduce test messages.

If near-duplicate families appear in different splits:

1. Review whether they represent the same underlying communicative example.
2. Move related families into the same split when justified.
3. Replace or exclude an unjustified duplicate.
4. Record the decision.
5. Recalculate the split checks.

### 7.9 Development-set permissions

The development set may be used for:

- Selecting prompt wording.
- Selecting demonstrations.
- Testing output schemas.
- Improving the response parser.
- Comparing deterministic parameter settings.
- Testing model availability.
- Identifying malformed-output problems.
- Estimating token usage, latency and cost.
- Running small stability checks.
- Selecting one model for the later BanglaMate extension.

Development-set results must still be logged.

The researcher must not repeatedly tune prompts only to solve individual
development examples without recording the changes.

### 7.10 Test-set restrictions

Before final test execution, the test set must not be used for:

- Selecting prompt wording.
- Selecting demonstrations.
- Selecting models.
- Selecting temperature.
- Selecting maximum output tokens.
- Adding special-case instructions.
- Changing the parser because of a test answer.
- Selecting a favorable random seed.
- Removing cases where a model performs poorly.
- Estimating expected test accuracy.

Test messages, labels and examples must never be included in prompt
demonstrations.

### 7.11 Prompt-demonstration rules

All few-shot demonstrations must come from development families.

For every demonstration, record:

- Demonstration ID.
- Source development family ID.
- Prompt condition using it.
- Prompt version.
- Date selected.
- Reason for selection.

Demonstrations should represent multiple labels and cue types.

A demonstration must not be selected because it resembles a known test
instance.

The final list of demonstration IDs must be frozen before test execution.

### 7.12 Test-access rule

Before prompt and model freeze, test-set access should be limited to:

- Automated structural validation.
- Automated checksum generation.
- Automated duplicate detection.
- Split-balance summaries.
- File-integrity checks.

The researcher must not inspect test model performance during prompt
development.

If the test data must be opened to investigate a genuine technical or data
problem, record:

- Date and time.
- Person accessing it.
- Reason for access.
- Files accessed.
- Whether labels or model outputs were visible.
- Action taken.
- Whether a protocol amendment is required.

Recommended record:

`docs/TEST_ACCESS_LOG.md`

### 7.13 Core test execution rule

Before test execution, freeze:

- Dataset version.
- Development and test family IDs.
- Model names and versions.
- Prompt text.
- Demonstration IDs.
- Model parameters.
- Output schema.
- Parser version.
- Retry rules.
- Analysis plan.
- Cost limit.

During test execution:

- Monitor technical failures only.
- Do not modify prompts based on apparent answer quality.
- Do not stop a batch because the accuracy appears low.
- Preserve all raw responses.
- Record every permitted retry.
- Complete and reconcile the planned test inventory.

After test execution begins, any changed configuration must receive a new
experiment name and must be reported as exploratory unless the protocol
explicitly permits the change.

### 7.14 BanglaMate extension separation

The 90-case BanglaMate extension sample will be drawn from the frozen test set
only after core results are frozen.

The extension sample must not be used to:

- Modify the core prompts.
- Modify core gold labels.
- Remove difficult core cases.
- Recalculate the core split.
- Replace core test results.
- Select a model using extension performance.

The extension will use the model selected through a predeclared
development-only selection rule.

The extension sample must be frozen before rewrite outputs are generated.

### 7.15 Dataset-publication rule

The complete benchmark should not be publicly released before the frozen model
evaluation is finished.

Before evaluation:

- Keep the GitHub repository private.
- Do not upload the test set to public websites.
- Do not place test examples in public prompts or discussions.
- Share files only with authorized annotators, the supervisor and approved
  reviewers.

A documented dataset release may be prepared after the primary experiments
are complete.

### 7.16 Split files

The split process will eventually produce:

```text
data/final/dev_family_ids.txt
data/final/test_family_ids.txt
data/final/dev_ids.txt
data/final/test_ids.txt
data/final/split_manifest.csv
data/final/split_report.md
data/final/split_checksums.txt
docs/TEST_ACCESS_LOG.md
```

These files will be created in a later phase.

Phase 1 only defines the required rules and file paths.

### 7.17 Split-manifest fields

The split manifest should contain:

| Field | Meaning |
|---|---|
| `message_family_id` | Family identifier |
| `instance_id` | Instance identifier |
| `split` | DEVELOPMENT or TEST |
| `domain` | Scenario domain |
| `primary_register` | Frozen gold primary label |
| `changed_cue_from_A` | Controlled cue change |
| `source_register` | Register present in the original message |
| `dataset_version` | Frozen dataset version |
| `split_seed` | Random seed used |
| `split_timestamp` | Date and time of split |

### 7.18 Automated split checks

The split validator must confirm:

- Development contains exactly 30 families.
- Development contains exactly 90 instances.
- Test contains exactly 120 families.
- Test contains exactly 360 instances.
- The complete dataset contains 150 families.
- The complete dataset contains 450 instances.
- Every family has exactly three instances.
- No family appears in both splits.
- No instance appears in both splits.
- Development and test family intersections are empty.
- Development and test family unions contain all 150 families.
- Development and test instance unions contain all 450 instances.
- Every domain appears in development.
- Every controlled cue appears in development.
- Tui, Tumi and Apni appear in development.
- Demonstration IDs belong only to development.
- Split files have recorded checksums.

### 7.19 Split freeze conditions

The split is considered frozen only when:

- Gold dataset version is frozen.
- Random seed is recorded.
- Family-level splitting is complete.
- Development and test counts are correct.
- Distribution reports are generated.
- Duplicate checks are complete.
- Any family swaps are documented.
- Automated split validation passes.
- Split files are saved.
- Checksums are recorded.
- Prompt demonstrations have not yet used test data.

After split freeze, family membership must not be changed without a documented
protocol amendment.

## 8. Core Models, Prompt Conditions, and Output Format

### 8.1 Core experiment objective

The core experiment will determine whether language models select Tui, Tumi
and Apni more accurately and consistently when they receive explicit social
context.

Every eligible model will be evaluated under the same three conditions:

- `P0_MESSAGE_ONLY`
- `P1_NARRATIVE_CONTEXT`
- `P2_STRUCTURED_CONTEXT`

The same frozen dataset instances will be used for every model and prompt
condition.

### 8.2 Core experiment matrix

The complete primary experiment contains:

```text
450 instances × 3 models × 3 prompt conditions = 4,050 responses
```

Breakdown:

```text
Development:
90 instances × 3 models × 3 conditions = 810 responses

Test:
360 instances × 3 models × 3 conditions = 3,240 responses
```

Prompt-development trials, technical dry runs and permitted retries will be
recorded separately and will not be confused with the final response
inventory.

### 8.3 Model count

The primary experiment will use exactly three remotely hosted API models.

All three models must:

- Be accessible through a programmatic API.
- Be available throughout the planned experiment period.
- Accept the required Romanized Bangla prompt.
- Support sufficient context length.
- Return text or structured output that can be saved.
- Have an identifiable model name or version.
- Be affordable under the approved API budget.
- Complete a development dry run.
- Be used under all three prompt conditions.

Manual ChatGPT, Gemini, Claude or other website conversations must not be
used as primary experimental records.

The experiment runner must call the models programmatically and save every
request and response.

### 8.4 Model-selection criteria

The exact model names will be selected in a later phase using development
data and the following predeclared criteria:

| Criterion | Requirement |
|---|---|
| API availability | Reliable programmatic access |
| Version identification | Exact model identifier can be recorded |
| Structured output | Can follow the required JSON schema |
| Romanized Bangla capability | Can process the task without systematic technical failure |
| Cost | Fits the approved budget |
| Latency | Can complete the experiment within the schedule |
| Provider diversity | Prefer models from more than one provider when feasible |
| Reproducibility | Parameters, prompts and raw outputs can be saved |

Models must not be selected using test-set accuracy.

A model may be rejected during development when:

- It cannot reliably access the API.
- Its responses repeatedly fail the output schema.
- Its projected cost exceeds the budget.
- The selected model version will not remain available.
- It produces systematic empty or blocked outputs.
- It cannot complete a controlled dry run.

Model rejection reasons must be documented.

### 8.5 Model diversity rule

When feasible, the three selected models should represent more than one:

- API provider.
- Model family.
- Price level.
- System design.

A suitable selection may include:

- One strong general-purpose commercial model.
- One model from a different commercial provider.
- One affordable or remotely hosted open-weight model.

This is a selection principle, not a requirement to run a model locally.

Local LLM inference is outside the required thesis scope.

### 8.6 Model manifest

The final selected models will later be recorded in:

`config/MODEL_MANIFEST.csv`

The model manifest should contain:

| Field | Meaning |
|---|---|
| `model_code` | Internal identifier such as M1, M2 or M3 |
| `provider` | API provider |
| `model_id` | Exact API model identifier |
| `model_version` | Recorded version or snapshot |
| `access_date` | Date availability was checked |
| `temperature` | Frozen generation temperature |
| `max_output_tokens` | Frozen output limit |
| `seed` | Seed if the provider supports one |
| `response_format` | JSON or text mode |
| `price_reference_date` | Date used for cost projection |
| `selection_reason` | Why the model was included |
| `status` | SELECTED, REJECTED or REPLACED |

Actual model names will not be inserted until the model-selection phase.

### 8.7 Common instruction across conditions

Every prompt condition must use the same:

- Task definition.
- Tui, Tumi and Apni definitions.
- Required JSON output schema.
- Confidence options.
- Reason-code options.
- Model parameters where supported.
- Language describing the required decision.

The conditions should differ only in the social-context representation visible
to the model.

The model will answer:

> Which Tui, Tumi or Apni register would be most socially appropriate for the
> supplied Romanized Bangla message and the information available in this
> prompt?

The model must not receive hidden chain-of-thought instructions.

### 8.8 P0: Message-only condition

Condition name:

`P0_MESSAGE_ONLY`

The model receives:

- The Romanized Bangla message.
- Short definitions of Tui, Tumi and Apni.
- The required output schema.

The model does not receive:

- Speaker role.
- Recipient role.
- Authority.
- Relative age.
- Familiarity.
- Setting.
- Domain.
- Communicative intention.
- Gold labels.

Example input structure:

```text
Task: Select the most socially appropriate second-person register.

Labels:
TUI = intimate or strongly downward register
TUMI = familiar or neutral-personal register
APNI = respectful or formal register

Message:
kalke report ta niye kotha bola jabe?

Return only the required JSON object.
```

Purpose:

The message-only condition measures model behavior when recipient context is
not explicitly available.

### 8.9 P1: Narrative-context condition

Condition name:

`P1_NARRATIVE_CONTEXT`

The model receives:

- Everything provided in P0.
- A short natural-language description of the social context.

The narrative must be generated deterministically from the structured context
fields.

It must not add information that is absent from the structured record.

Example narrative:

```text
The speaker is a student addressing a teacher. The recipient has higher
authority than the speaker, is older, and has low familiarity with the
speaker. The communication occurs in a formal academic setting.
```

The narrative generator must use a fixed template.

It must not use another language model to invent or enrich context during the
final experiment.

Purpose:

The narrative condition tests whether ordinary natural-language context helps
the model select an appropriate register.

### 8.10 P2: Structured-context condition

Condition name:

`P2_STRUCTURED_CONTEXT`

The model receives:

- Everything provided in P0.
- The same social information used in P1.
- Social information represented through fixed field names and values.

Example structured context:

```json
{
  "domain": "ACADEMIC",
  "intent": "REQUEST",
  "speaker_role": "STUDENT",
  "recipient_role": "TEACHER",
  "authority_relation": "HIGHER",
  "relative_age": "OLDER",
  "familiarity": "LOW",
  "setting": "FORMAL"
}
```

Purpose:

The structured condition tests whether a fixed and explicit representation of
social context improves register selection and cue sensitivity.

P1 and P2 must contain the same underlying social information. Only the
presentation format may differ.

### 8.11 Demonstration-control rule

If few-shot demonstrations are used, all three prompt conditions must use the
same number of demonstrations and the same development-family IDs.

Recommended design:

- Three demonstrations.
- One example with primary gold Tui.
- One example with primary gold Tumi.
- One example with primary gold Apni.
- All demonstrations selected from development families.
- No demonstration selected from test families.

The demonstration content will be adapted to each condition:

- P0 receives message-only versions.
- P1 receives narrative-context versions.
- P2 receives structured-context versions.

This prevents the structured condition from receiving more examples than the
other conditions.

If the supervisor requires demonstrations only in P2, the condition must be
described as a combined structured-context-plus-demonstration intervention.
The thesis must not claim that any improvement was caused by structure alone.

The final zero-shot or parallel few-shot decision must be made using
development data and frozen before test execution.

### 8.12 Information prohibited from model input

The following fields must never be shown to the model during the primary
register-selection task:

- `primary_register`
- `secondary_register`
- `acceptable_registers`
- `answerability_status`
- Annotator labels
- Adjudication decisions
- Researcher-expected labels
- Model scores
- Error categories
- `changed_cue_from_A`
- Comparison direction
- Test-set performance
- Another evaluated model's prediction

The model does not need to see:

- `instance_id`
- `message_family_id`
- Split assignment
- Annotator identifiers
- Dataset version
- Review actions

These fields may be retained in experiment metadata outside the rendered
prompt.

### 8.13 Required model output

Every model must return one JSON object with this schema:

```json
{
  "register": "TUI",
  "confidence": "high",
  "reason_codes": ["AUTHORITY", "SETTING"]
}
```

Allowed `register` values:

- `TUI`
- `TUMI`
- `APNI`

Allowed `confidence` values:

- `low`
- `medium`
- `high`

Allowed `reason_codes`:

- `AUTHORITY`
- `AGE`
- `FAMILIARITY`
- `SETTING`
- `KINSHIP`
- `ROLE`
- `EMOTIONAL_STANCE`
- `MESSAGE_FORM`
- `OTHER`

The model must return only the JSON object.

It must not return:

- A Markdown explanation.
- An essay.
- Multiple predictions.
- An acceptable-register set.
- Hidden chain-of-thought.
- A rewritten message during the core selection task.
- Additional keys not defined by the schema.

### 8.14 Parser rules

The response parser may:

- Remove a surrounding Markdown JSON code fence.
- Ignore harmless leading or trailing whitespace.
- Normalize allowed label capitalization.
- Validate the required keys.
- Validate allowed categorical values.
- Record whether a harmless formatting correction occurred.

The parser must not:

- Infer a register from unrelated prose.
- Change one valid register into another.
- Select the first label mentioned in an explanation.
- Replace a missing prediction with a default label.
- Use the gold label to repair an output.
- Silently discard invalid responses.

Every parsed response must receive one status:

- `VALID`
- `RECOVERABLE_FORMAT`
- `INVALID_JSON`
- `INVALID_REGISTER`
- `MISSING_FIELD`
- `EXTRA_UNAPPROVED_FIELD`
- `EMPTY_RESPONSE`
- `PROVIDER_ERROR`
- `BLOCKED`

Raw responses must be preserved before parsing.

### 8.15 Prompt-development rules

Prompt development may use only development data.

The researcher may modify prompts to address general problems such as:

- Unclear task wording.
- Repeated invalid JSON.
- Misunderstood label definitions.
- Missing required fields.
- Excessively long outputs.
- Inconsistent formatting.

The researcher must not add special instructions designed only to solve one
individual test instance.

Every prompt revision must record:

- Prompt condition.
- Previous version.
- New version.
- Reason for change.
- Development evidence.
- Date.
- Researcher.
- Whether test results had been observed.

### 8.16 Prompt files

The final prompts will later be stored in:

```text
prompts/core/P0_message_only_v1.txt
prompts/core/P1_narrative_context_v1.txt
prompts/core/P2_structured_context_v1.txt
prompts/core/system_message_v1.txt
prompts/PROMPT_MANIFEST.csv
```

Phase 1 defines the required conditions.

The actual prompt files will be written and tested in a later phase.

### 8.17 Prompt manifest

The prompt manifest should contain:

| Field | Meaning |
|---|---|
| `prompt_code` | P0, P1 or P2 |
| `prompt_version` | Frozen prompt version |
| `prompt_path` | File containing the prompt |
| `system_prompt_path` | Common system instruction |
| `demonstration_ids` | Development-only example IDs |
| `demonstration_count` | Number of demonstrations |
| `template_checksum` | Prompt-file checksum |
| `freeze_date` | Date prompt was frozen |
| `approved_by` | Supervisor or researcher according to protocol |
| `status` | DEVELOPMENT or FROZEN |

### 8.18 Generation-parameter rules

Use deterministic settings where the provider supports them.

Recommended starting settings:

```text
temperature = 0
max_output_tokens = 100
number_of_outputs = 1
```

If a provider does not support temperature zero, use its closest deterministic
setting.

Exact provider-specific values will be tested using development data and
recorded in the model manifest.

The final test experiment must not give one model:

- More output tokens without justification.
- More demonstrations.
- More context.
- Different label definitions.
- Additional retry opportunities.

Provider-specific technical differences must be documented.

### 8.19 Stability check

Because API models may not be completely deterministic, a small repeated-run
stability check may be performed on development data.

Recommended stability sample:

- Ten development instances.
- All three labels represented when possible.
- Each selected model.
- Each prompt condition.
- Two additional repeated runs.

The stability check must:

- Use development data only.
- Be reported separately from the primary experiment.
- Not replace the one-response-per-condition primary test design.
- Record exact parameters and dates.

### 8.20 Model replacement rule

If a selected model becomes unavailable before test execution:

1. Record the unavailable model and date.
2. Select a replacement using the original eligibility criteria.
3. Rerun required development validation.
4. Update the model manifest.
5. Update the cost projection.
6. Freeze the replacement before test execution.

If a model becomes unavailable during test execution:

1. Stop the affected model configuration.
2. Do not silently mix model versions.
3. Preserve completed raw outputs.
4. Record the incident.
5. Consult the frozen fallback rule.
6. If a replacement is approved, run the replacement across the complete
   required condition rather than only missing cases.
7. Report the replacement transparently.

### 8.21 Prompt and model freeze conditions

The core prompt and model configuration is frozen only when:

- Three eligible API models are selected.
- Every model passes the development dry run.
- P0, P1 and P2 prompts exist.
- Label definitions are identical across conditions.
- P1 and P2 contain the same underlying context information.
- Demonstration rules are satisfied.
- Demonstration IDs come only from development.
- Output schema is frozen.
- Parser tests pass.
- Model parameters are recorded.
- Prompt and model checksums are recorded.
- Cost projection passes the approved budget.
- Test data has not been used for prompt development.

After this freeze, prompt or model changes require a new experiment name and
documented change classification.