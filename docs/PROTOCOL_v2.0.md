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