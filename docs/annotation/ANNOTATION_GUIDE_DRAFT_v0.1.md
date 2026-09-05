# SocialCue-BN Annotation Guide

**Version:** Draft v0.1  
**Date:** 2026-08-30  
**Status:** DRAFT — NOT AUTHORIZED FOR MAIN ANNOTATION  
**Dataset:** SocialCue-BN Romanized Bangla Pilot  
**Pilot size:** 45 instances from 15 message families

## 1. Purpose

This guide explains how independent annotators should identify the
socially appropriate Bangla address register for a Romanized Bangla
message and its accompanying social context.

The three possible register labels are:

- TUI
- TUMI
- APNI

The task is not merely to identify a pronoun already visible in the
message. The task is to decide which address register would be most
socially appropriate for addressing the recipient in the described
context.

## 2. Annotation Unit

Each annotation item contains:

- one Romanized Bangla message;
- the communication domain;
- the speaker's role;
- the recipient's role;
- the authority relation;
- the relative-age relation;
- the familiarity level;
- the communication setting.

Annotators must evaluate each item independently.

Annotators will not be shown:

- the message-family ID;
- whether the item is variant A, B, or C;
- which social cue changed;
- comparison IDs;
- private designer expectations;
- another annotator's answers;
- model predictions.

## 3. Register Definitions

### 3.1 TUI

TUI represents the highly intimate or strongly non-honorific
second-person register associated with forms such as `tui`.

It may be natural when:

- the people have a very close relationship;
- the recipient is considerably younger;
- the recipient has lower social authority;
- the setting is highly informal;
- close friendship or kinship licenses this form.

TUI must not be selected merely because the conversation is
informal.

Depending on the relationship and community, TUI can express:

- affection;
- intimacy;
- seniority;
- disrespect;
- anger or aggression.

Because of this variation, TUI should be selected carefully.

### 3.2 TUMI

TUMI represents the familiar or neutral non-honorific register
associated with forms such as `tumi`.

It may be natural when:

- the participants are friends or peers;
- their ages are similar;
- familiarity is medium or high;
- the setting is informal or semi-formal;
- no strong respect cue requires APNI;
- the relationship is not intimate enough to strongly license TUI.

TUMI is often the neutral middle option, but it must not be selected
automatically without considering the context.

### 3.3 APNI

APNI represents the respectful or honorific register associated with
forms such as `apni`.

It may be natural when:

- the recipient has higher authority;
- the recipient is older;
- familiarity is low;
- the setting is formal;
- the interaction is professional, academic, public, or service
  oriented;
- respectful distance is expected.

APNI must not be selected solely because it is the safest or most
polite option. It should be socially natural for the described
relationship.

## 4. Context Fields

### 4.1 Authority Relation

Authority describes the recipient's social or institutional position
relative to the speaker.

Possible values are:

- `HIGHER`: the recipient has higher authority;
- `EQUAL`: neither participant has clearly higher authority;
- `LOWER`: the recipient has lower authority;
- `UNKNOWN`: the authority relation cannot be determined.

Authority is important, but it does not automatically override every
other social cue.

### 4.2 Relative Age

Relative age describes the recipient's age relative to the speaker.

Possible values are:

- `OLDER`;
- `SIMILAR`;
- `YOUNGER`;
- `UNKNOWN`.

Older age may favor APNI, while younger age may allow TUMI or TUI.
However, age must be considered together with familiarity, authority,
and setting.

### 4.3 Familiarity

Familiarity describes how well the participants know each other.

Possible values are:

- `LOW`;
- `MEDIUM`;
- `HIGH`.

Low familiarity may favor APNI. High familiarity may favor TUMI or
sometimes TUI. High familiarity alone does not always make TUI
appropriate.

### 4.4 Setting

The setting describes the level of formality of the interaction.

Possible values are:

- `INFORMAL`;
- `SEMI_FORMAL`;
- `FORMAL`.

Formal settings often favor APNI. Informal settings may allow TUMI
or TUI, depending on the relationship.

## 5. General Decision Principle

No single social cue should be treated as an absolute rule.

Annotators must consider the combined effect of:

1. authority;
2. age;
3. familiarity;
4. setting;
5. speaker and recipient roles;
6. relevant kinship or emotional information.

For example, a recipient may be older but also a highly familiar
family member in an informal setting. In such a case, more than one
register may be naturally acceptable.

## 6. Annotation Fields

### 6.1 Answerability

First, decide whether the item can be annotated reliably.

Choose one value:

#### ANSWERABLE

Use this when the message and context provide enough information to
make a defensible register decision.

#### UNDERSPECIFIED

Use this when essential information is missing or the message cannot
be interpreted reliably enough to make a defensible decision.

Ordinary uncertainty between two plausible registers does not
automatically make an item underspecified.

#### CONTRADICTORY

Use this only when the supplied information is logically
inconsistent.

Mixed social cues are not automatically contradictory. Real
relationships may contain competing age, authority, familiarity, and
setting cues.

#### CONTENTIOUS

Use this when the register decision depends so strongly on community,
regional, family, or individual variation that no stable acceptable
set of one or two registers can be given.

### 6.2 Primary Register

If the item is `ANSWERABLE`, choose exactly one primary register:

- `TUI`
- `TUMI`
- `APNI`

The primary register is the register the annotator considers most
socially natural for the described context.

Do not select a primary register merely because it is grammatically
possible.

### 6.3 Secondary Register

A secondary register is optional.

Select a secondary register only when it would also sound naturally
acceptable in the same context without changing the intended
relationship.

A secondary register must:

- differ from the primary register;
- be genuinely acceptable, not merely imaginable;
- not be added only because the annotator feels uncertain.

Only one secondary register is allowed.

If one register is clearly preferred, leave the secondary field
blank.

### 6.4 Acceptable Register Set

The acceptable-register set consists of:

- the primary register; and
- the optional secondary register.

The primary register must appear first.

Examples:

- `APNI`
- `TUMI`
- `TUMI|TUI`
- `APNI|TUMI`

The acceptable set may contain no more than two registers.

### 6.5 Confidence

Choose one confidence value:

#### HIGH

Use when the primary register is clear and broad agreement is
expected.

#### MEDIUM

Use when the primary register is defensible but another register or
community-specific variation is plausible.

#### LOW

Use when substantial uncertainty remains.

Low confidence does not excuse random selection. If no defensible
primary register exists, use the appropriate non-answerable category.

### 6.6 Reason Codes

Select one or more reason codes that genuinely influenced the
decision:

- `AUTHORITY`
- `AGE`
- `FAMILIARITY`
- `SETTING`
- `KINSHIP`
- `EMOTIONAL_STANCE`
- `OTHER`

Do not select every reason code automatically.

If `OTHER` is selected, explain it briefly in the note field.

### 6.7 Annotation Timestamp

Each completed response must contain an annotation timestamp.

Use ISO 8601 format with a timezone, for example:

`2026-08-31T15:30:00+06:00`

The example must not be copied as the real timestamp. The timestamp
should record when the response row was finalized. It may be entered by
the annotator or added automatically by the authorized collection tool.

## 7. Required Annotation Sequence

For every item, follow this sequence:

1. Read the Romanized Bangla message.
2. Read the speaker and recipient roles.
3. Read all four context cues.
4. Decide whether the item is answerable.
5. Identify the strongest relevant social cues.
6. Select the primary register.
7. Decide whether one secondary register is genuinely acceptable.
8. Select confidence.
9. Select the relevant reason codes.
10. Add a short note only when clarification is necessary.
11. Submit the answer before moving to the next item.

Annotators should not return to earlier items merely to force similar
answers across apparently related cases.

## 8. Existing Register Markers in a Message

A message may contain a pronoun, address term, or verb form that
suggests an existing register.

Do not copy that register automatically.

Instead, determine whether that register is socially appropriate for
the supplied context.

If the visible marker conflicts with the context, annotate the
register that should naturally be used for the context and mention
the conflict in the note field.

## 9. Romanization, Spelling and Code-Mixing

Romanized Bangla has no single universally accepted spelling system.

Do not reject an item merely because another spelling would also be
possible.

Minor spelling variation should not affect the register label.

English words mixed into the message should not affect the decision
unless they change:

- the meaning;
- the communication setting;
- the emotional stance; or
- the perceived relationship.

Do not silently rewrite or correct the supplied message.

If the message is genuinely impossible to interpret, use
`UNDERSPECIFIED` and explain the problem briefly.

## 10. Training-Only Examples

The examples in this section are not part of the 45-instance pilot.

### Example 1: Formal Academic Interaction

Context:

- speaker: student;
- recipient: unfamiliar senior teacher;
- authority: higher;
- age: older;
- familiarity: low;
- setting: formal.

Recommended annotation:

- answerability: `ANSWERABLE`;
- primary: `APNI`;
- secondary: blank;
- confidence: `HIGH`;
- reasons: `AUTHORITY|AGE|FAMILIARITY|SETTING`.

### Example 2: Close Same-Age Friends

Context:

- speaker: friend;
- recipient: close same-age friend;
- authority: equal;
- age: similar;
- familiarity: high;
- setting: informal.

Recommended annotation:

- answerability: `ANSWERABLE`;
- primary: `TUMI`;
- secondary: `TUI`;
- confidence: `MEDIUM`;
- reasons: `FAMILIARITY|SETTING`.

TUI is included only as a plausible secondary form because not every
close friendship naturally uses TUI.

### Example 3: Younger Close Sibling

Context:

- speaker: older sibling;
- recipient: much younger sibling;
- authority: lower;
- age: younger;
- familiarity: high;
- setting: informal.

Recommended annotation:

- answerability: `ANSWERABLE`;
- primary: `TUI`;
- secondary: `TUMI`;
- confidence: `MEDIUM`;
- reasons: `AGE|FAMILIARITY|KINSHIP|SETTING`.

### Example 4: Semi-Formal Peer

Context:

- speaker: colleague;
- recipient: similarly aged colleague;
- authority: equal;
- age: similar;
- familiarity: medium;
- setting: semi-formal.

Recommended annotation:

- answerability: `ANSWERABLE`;
- primary: `TUMI`;
- secondary: `APNI`;
- confidence: `MEDIUM`;
- reasons: `FAMILIARITY|SETTING`.

### 10.1 Positive, Boundary, and Exclusion Examples

These examples are for training only. They must not be copied into the
pilot or final benchmark.

| Target label | Example type | Context | Annotation guidance |
|---|---|---|---|
| `TUI` | Positive | An older sibling addresses a much younger sibling at home. Authority is lower, age is younger, familiarity is high, and the setting is informal. | `TUI` is the expected primary register because strong intimacy and downward age jointly license it. |
| `TUI` | Boundary | Two very close same-age childhood friends speak informally. | `TUMI` and `TUI` may both be natural. Select the community-natural primary form and add the other only if genuinely acceptable. |
| `TUI` | Exclusion | A speaker addresses an unfamiliar younger service employee. | Do not select `TUI` only because the recipient is younger or has lower authority. Low familiarity and the service setting may require `TUMI` or `APNI`. |
| `TUMI` | Positive | A student addresses a similarly aged, familiar classmate in an informal setting. | `TUMI` is the expected primary register. |
| `TUMI` | Boundary | A person addresses a familiar, similarly aged colleague in a semi-formal workplace. | `TUMI` or `APNI` may be acceptable depending on workplace practice. |
| `TUMI` | Exclusion | A student addresses an unfamiliar senior professor in a formal academic interaction. | Do not select `TUMI` merely because the message sounds friendly. `APNI` is expected. |
| `APNI` | Positive | A student addresses an unfamiliar, older, senior teacher in a formal setting. | `APNI` is the expected primary register. |
| `APNI` | Boundary | A speaker addresses an older but very close relative at home. | Family convention may license `APNI` or `TUMI`. Use a secondary register only when both are naturally acceptable. |
| `APNI` | Exclusion | A parent addresses a very young child at home. | Do not select `APNI` merely because it is the most polite form. `TUI` or `TUMI` will normally be more socially natural. |

### 10.2 Special-Case Rules

#### Group Recipients

When a message addresses a group, determine which register would be
natural for addressing the group as a whole.

If the group includes a clearly senior or higher-authority person,
`APNI` may be the most appropriate common register.

If the intended recipient within the group cannot be identified and
that information is essential, select `UNDERSPECIFIED`.

#### Plural Address

The task concerns social register, not grammatical number.

Do not change the label merely because the message addresses multiple
people. Select the register level that best represents the social
relationship between the speaker and the intended recipients.

#### Joking

Joking does not automatically license `TUI`.

First consider the normal relationship, age, familiarity, authority, and
setting. Use `EMOTIONAL_STANCE` only when the joking tone materially
affects the register decision.

#### Sarcasm

A respectful form may sometimes be used sarcastically, and a familiar
form may sometimes be used aggressively.

Annotate the socially intended address register, not politeness inferred
from the surface wording alone.

If sarcasm makes the intended register genuinely impossible to
determine, use the most appropriate non-answerable category and explain
the problem in `annotation_note`.

#### Anger or Conflict

Anger does not automatically change the appropriate register to `TUI`.

Consider whether the relationship normally licenses `TUI`. If an
aggressive form conflicts with the socially expected register, select
the context-appropriate register and record the conflict in
`annotation_note`.

Use `EMOTIONAL_STANCE` as a reason code when anger materially influences
the decision.

#### Mixed Professional and Personal Relationships

Two people may be friends or relatives while also having a professional
relationship.

Give particular attention to:

- the role active during the current interaction;
- the immediate communication setting;
- whether other people are present;
- institutional expectations; and
- the participants' established form of address.

For example, two friends may use `TUMI` privately but prefer `APNI`
during a formal public meeting.

If two registers are genuinely natural in the supplied context, choose
the more natural one as primary and record the other as secondary.

## 11. Independence Rules

Annotators must complete their work independently.

Before submitting their responses, annotators must not:

- discuss individual items with another annotator;
- inspect another annotator's responses;
- inspect the private designer expectations;
- use ChatGPT or another AI system to select labels;
- search online for answers to individual items;
- ask another person to choose labels;
- try to identify A/B/C counterfactual families.

Annotators may ask the researcher to clarify the written procedure,
but the researcher must not recommend a label for a specific pilot
item.

## 12. Privacy and Storage

Annotators will be identified only by codes such as:

- `A1`
- `A2`

Personal names, phone numbers, email addresses, signatures, and other
identifiable information must not be placed in the public dataset.

Raw annotation responses will initially be stored under a private
location such as:

`data/private/annotations/`

Only anonymized and approved results may later be transferred into a
public research artifact.

## 13. Annotator Qualification

Two native or near-native Bangla speakers who are comfortable reading
Romanized Bangla will be used for the pilot.

Before receiving the 45 pilot items, each candidate annotator must
complete a separate qualification exercise.

The qualification materials will contain:

- 12 clear control items;
- additional boundary examples for training and discussion;
- no item copied from the 45-instance pilot or future benchmark.

The correct reference label for every qualification control must be
established before the controls are given to the annotators.

Each annotator must complete the 12 controls independently and correctly
label at least 10 of the 12 controls.

The researcher must also verify that the annotator:

- does not systematically confuse any register-label pair;
- understands primary versus secondary registers;
- understands the answerability categories;
- understands the independence rules; and
- confirms that AI will not be used to label individual items.

Cohen's kappa is not used as the Phase 4 qualification threshold.

Cohen's kappa will instead be calculated from the two annotators'
independent annotations of the real 45-item pilot during Phase 5. If the
pilot kappa is below `0.60`, the instructions, label distribution,
missing context, and possible label confusion must be investigated.

If an annotator does not pass the qualification:

1. review the annotation rules with that annotator;
2. discuss only training and qualification examples;
3. provide different practice examples;
4. allow one new qualification attempt; and
5. replace the annotator if the second attempt fails.

The real pilot items must never be discussed before both independent
pilot annotation files have been submitted.

## 14. Version Control

This document is Draft v0.1.

It may be revised only during training and qualification.

After both annotators qualify, the guide may be approved as the guide
used for the Phase 5 pilot.

During Phase 5:

1. both annotators will independently annotate the 45 pilot items;
2. agreement and disagreements will be analyzed;
3. unclear rules and examples may be revised;
4. both annotators will review the final changes; and
5. the guide will then be frozen as `ANNOTATION_GUIDE_v1.0`.

Version 1.0 must be frozen before construction and annotation of the
full 450-instance benchmark.

## 15. Current Authorization

This draft is authorized for:

- preparing the response template;
- creating training examples;
- creating qualification questions;
- explaining the task to candidate annotators.

This draft is not yet authorized for the main 45-item annotation.