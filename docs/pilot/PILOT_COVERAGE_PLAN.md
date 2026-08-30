# Phase 3 Pilot Coverage Plan

**Project:** SocialCue-BN  
**Document version:** 0.1  
**Status:** DRAFT — planning document only  
**Target:** 15 message families and 45 total instances

## 1. Purpose

The pilot dataset will test whether the dataset structure, social-context
fields, counterfactual design, annotation instructions, and validation
scripts work correctly before constructing the full 450-instance benchmark.

The pilot is not intended to produce the final thesis results.

## 2. Pilot size

- Number of message families: 15
- Contexts per family: 3
- Total instances: 45
- Controlled comparisons per family: 2
- Total controlled comparisons: 30

For every family:

- Context A is the baseline.
- Context B differs from A in exactly one social cue.
- Context C returns to the A baseline and differs from A in one different cue.
- A–B is a controlled comparison.
- A–C is a controlled comparison.
- B–C must not automatically be treated as a controlled comparison.

## 3. Non-negotiable construction rules

1. The Romanized Bangla message must be identical in contexts A, B, and C.
2. Only the social context may change between the three instances.
3. Context B must change exactly one cue relative to A.
4. Context C must change exactly one different cue relative to A.
5. All other context fields must remain unchanged in each controlled comparison.
6. Every message must be understandable using the supplied context.
7. Messages must be short, realistic, and natural when read aloud.
8. Do not use real names, phone numbers, exact institutions, or copied private conversations.
9. Do not assign annotator gold labels during candidate generation.
10. Any designer-predicted label must remain private and must not be shown to annotators.
11. Awkward, stereotyped, unsafe, or culturally implausible AI suggestions must be rewritten or rejected.
12. All AI assistance must be recorded in `docs/AI_USE_LOG.csv`.

## 4. Domain allocation

| Domain | Number of families | Number of instances |
|---|---:|---:|
| Academic | 3 | 9 |
| Professional | 3 | 9 |
| Family | 3 | 9 |
| Friendship | 2 | 6 |
| Service/public interaction | 2 | 6 |
| Online community | 2 | 6 |
| **Total** | **15** | **45** |

## 5. Planned family allocation

The intention descriptions below are planning targets. They are not final
messages and may be replaced when the candidate messages are reviewed.

| Family ID | Domain | Candidate intention | A–B changed cue | A–C changed cue |
|---|---|---|---|---|
| F001 | Academic | Requesting a meeting | authority | relative_age |
| F002 | Academic | Requesting a deadline extension | familiarity | setting |
| F003 | Academic | Requesting feedback or class information | authority | setting |
| F004 | Professional | Requesting a file or document | authority | familiarity |
| F005 | Professional | Confirming a shift or schedule | relative_age | setting |
| F006 | Professional | Asking for approval | authority | relative_age |
| F007 | Family | Checking someone's location | relative_age | familiarity |
| F008 | Family | Asking for household help | authority | familiarity |
| F009 | Family | Giving a reminder | relative_age | setting |
| F010 | Friendship | Making plans or inviting someone | familiarity | setting |
| F011 | Friendship | Requesting notes or asking a favor | authority | relative_age |
| F012 | Service/public interaction | Asking for directions or assistance | authority | setting |
| F013 | Service/public interaction | Making a request to a service provider | relative_age | familiarity |
| F014 | Online community | Replying to a moderator or senior member | authority | familiarity |
| F015 | Online community | Asking a question in an online group | relative_age | setting |

## 6. Social-cue balance

Each family contributes two controlled comparisons, producing 30 planned
cue changes.

| Changed cue | Planned comparisons |
|---|---:|
| authority | 8 |
| relative_age | 8 |
| familiarity | 7 |
| setting | 7 |
| **Total** | **30** |

Small differences in these counts are acceptable because 30 cannot be
divided equally among four cue types. However, every cue must appear in
multiple domains.

## 7. Message-selection requirements

A candidate may be selected only if:

- it is written in understandable Romanized Bangla;
- it represents a realistic communication intention;
- it can remain exactly the same across three contexts;
- its suitable address register could reasonably depend on social context;
- it does not require hidden information;
- it does not contain identifiable or private information;
- it does not depend entirely on sarcasm, joking, or an unusual relationship;
- the two planned cue changes can be made independently;
- it does not require changing the message wording to make the contexts believable.

## 8. Pilot completion checklist

The pilot will not be considered complete until:

- [ ] 25–30 candidate families have been generated and logged.
- [ ] 15 natural and diverse families have been manually selected.
- [ ] All six domains are represented.
- [ ] Every family contains contexts A, B, and C.
- [ ] Every A–B comparison changes exactly one cue.
- [ ] Every A–C comparison changes exactly one different cue.
- [ ] The message is identical within every family.
- [ ] All four social cues are represented.
- [ ] English lexical-token proportion has been checked.
- [ ] Code mixing has been classified using the frozen rule.
- [ ] All 45 instances have been read aloud.
- [ ] A native Bangla speaker who did not write the items has reviewed a sample.
- [ ] Structurally invalid or unnatural instances have been corrected or removed.
- [ ] The validator accepts all 45 instances.
- [ ] The accepted pilot has been saved as an immutable version.