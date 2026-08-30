# SocialCue-BN Protocol Change Log

This file is append-only. Previous change entries must not be deleted or rewritten to conceal earlier decisions.

## Status Values

* `PROPOSED`
* `APPROVED`
* `REJECTED`
* `IMPLEMENTED`
* `SUPERSEDED`

## Change C001

* Date: 2026-08-30
* Protocol version: v2.0-DRAFT
* Category: Scientific/material
* Requested by: Student
* Affected area: Overall thesis scope
* Old rule: Broad BanglaMate multi-agent communication system as the main contribution.
* New rule: SocialCue-BN controlled counterfactual benchmark as the main contribution, with BanglaMate retained as a secondary extension.
* Reason: Improve experimental control, reproducibility, feasibility, and defensibility.
* Development results viewed: No
* Test results viewed: No
* Supervisor decision: Pending
* Required rerun: None
* Status: PROPOSED
* Git commit: To be added

## Change C002

* Date: 2026-08-30
* Protocol version: v2.0-DRAFT
* Category: Scientific/material
* Requested by: Student
* Affected area: Dataset
* Old rule: Dataset design not sufficiently frozen.
* New rule: 150 families, three instances per family, 450 instances, and two controlled pairs per family.
* Reason: Create a manageable but scientifically controlled benchmark.
* Development results viewed: No
* Test results viewed: No
* Supervisor decision: Pending
* Required rerun: None
* Status: PROPOSED
* Git commit: To be added

## Change C003

* Date: 2026-08-30
* Protocol version: v2.0-DRAFT
* Category: Scientific/material
* Requested by: Student
* Affected area: Annotation coverage
* Old rule: Complete annotation coverage by multiple annotators was considered.
* New rule: ANN_A annotates all 450 instances; ANN_B independently annotates a frozen 150-instance overlap and flagged cases receive additional review.
* Reason: Reduce time while retaining measurable independent agreement.
* Development results viewed: No
* Test results viewed: No
* Supervisor decision: Pending
* Required rerun: None
* Status: PROPOSED
* Git commit: To be added

## Change C004

* Date: 2026-08-30
* Protocol version: v2.0-DRAFT
* Category: Scientific/material
* Requested by: Student
* Affected area: BanglaMate extension
* Old rule: Four-agent system either excluded or insufficiently bounded.
* New rule: Secondary 90-case extension using one model, E0/E1/E2, cached E2, and maximum one Critic-triggered revision.
* Reason: Retain the supervisor’s agentic-AI interest without endangering the core experiment.
* Development results viewed: No
* Test results viewed: No
* Supervisor decision: Pending
* Required rerun: None
* Status: PROPOSED
* Git commit: To be added

## Change C005

* Date: 2026-08-30
* Protocol version: v2.0-DRAFT
* Category: Scientific/material and operational
* Requested by: Student
* Affected area: API access and experiment execution
* Old rule: Paid API access was permitted under a monetary safety cap.
* New rule: Only legitimate free-tier APIs requiring no payment card may be used. Core financial cap is USD 0.
* Reason: The student does not have a payment card and must complete the experiment without financial API charges.
* Development results viewed: No
* Test results viewed: No
* Supervisor decision: Pending
* Required rerun: None
* Status: PROPOSED
* Git commit: To be added

## New Change Template

Copy this template when a future change is required.

* Change ID:
* Date:
* Protocol version:
* Category:
* Requested by:
* Affected area:
* Old rule:
* New rule:
* Reason:
* Development results viewed:
* Test results viewed:
* Supervisor decision:
* Required rerun:
* Status:
* Git commit:
