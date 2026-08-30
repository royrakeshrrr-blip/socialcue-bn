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