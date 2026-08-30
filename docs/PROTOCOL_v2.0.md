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