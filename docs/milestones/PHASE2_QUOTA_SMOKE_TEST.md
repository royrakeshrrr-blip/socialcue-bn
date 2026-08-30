# Phase 2 Free-Quota Projection Smoke Test

Generated UTC: 2026-08-30T11:05:22.596416Z
Source dry run: `results/raw/core/phase2-dummy-smoke-test.jsonl`
Source is dummy data: `YES`

## Call projection

| Segment | Required calls |
|---|---:|
| Ten-instance dry run | 90 |
| Development inventory | 810 |
| Test inventory | 3240 |
| Frozen core matrix | 4050 |
| Core reserve (25%) | 1013 |
| Core authorization ceiling | 5063 |
| Extension fixed cap | 600 |
| Overall planned experiment ceiling | 5663 |

The ten-instance dry run uses development cases and is not added again to the frozen core matrix when its valid outputs are retained.

## Token projection

- Observed records: 9
- Average input-token estimate: 37.67
- Average output-token estimate: 4.00
- Projected input tokens at the core ceiling: 190707
- Projected output tokens at the core ceiling: 20252

Dummy whitespace-token estimates are infrastructure checks only. Replace this report after the real 90-call development dry run.

## Free-access gate

- Required approved free models: 3
- Approved free models recorded: 0
- Calls per model including reserve: 1688
- Maximum paid expenditure allowed: USD 0.00
- Observed expenditure: USD 0.00
- Budget gate: `PASS`
- Execution gate: `BLOCKED_PENDING_FREE_QUOTA_VERIFICATION`

## Authorization decision

This Phase 2 smoke test does not authorize real API execution. Real execution remains blocked until three model entries are verified against current official free-tier documentation, evidence files are committed, all tests pass, and the 90-call real dry run is reviewed.
