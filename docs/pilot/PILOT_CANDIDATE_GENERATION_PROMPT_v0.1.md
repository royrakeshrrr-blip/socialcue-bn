# Pilot Candidate Generation Prompt v0.1

**Project:** SocialCue-BN  
**Phase:** Phase 3  
**Date:** 2026-08-30  
**Purpose:** Generate a preliminary pool of Romanized Bangla messages for manual review.

## Prompt

You are assisting with candidate generation for an undergraduate research
benchmark called SocialCue-BN.

Generate exactly 30 original candidate message families written in natural
Romanized Bangla used in Bangladesh.

Use exactly six domains with five candidates in each domain:

1. Academic
2. Professional
3. Family
4. Friendship
5. Service/public interaction
6. Online community

Each candidate must contain:

- candidate ID;
- domain;
- communication intention;
- one short Romanized Bangla message;
- two or more social cues that could plausibly affect the appropriate
  TUI, TUMI, or APNI address register.

The allowed social cues are:

- authority;
- relative_age;
- familiarity;
- setting.

Construction requirements:

1. Keep every message short and understandable.
2. Make the situations realistic in Bangladeshi communication.
3. Do not use real names, phone numbers, exact institutions, addresses,
   or copied private conversations.
4. Avoid offensive, stereotyped, romantic, sexual, political, medical-emergency,
   or legally sensitive scenarios.
5. Prefer messages that can remain lexically identical when the social context changes.
6. Avoid directly using tui, tumi, apni, tor, tomar, apnar, or similar
   address terms in the message.
7. Whenever possible, avoid verb endings that already force a particular
   address register.
8. Do not assign TUI, TUMI, or APNI labels.
9. Do not construct contexts A, B, and C.
10. Do not claim that any candidate is validated research data.
11. Use candidate IDs C001 through C030.
12. Present the result as a Markdown table.

The output is only a candidate pool. A human will later review, rewrite,
select, validate, and assign controlled contexts.