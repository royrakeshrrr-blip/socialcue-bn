# Justification for the SocialCue-BN Thesis Scope

## Previous Direction

The earlier BanglaMate proposal focused on a comparatively broad multi-agent communication system, potentially involving several specialized agents and knowledge-guided reasoning.

Although that direction is interesting, implementing and scientifically validating the complete system would require several difficult components simultaneously:

* defining socially appropriate Romanized Bangla behavior;
* designing several interacting agents;
* evaluating whether each agent contributes meaningfully;
* controlling errors passed between agents;
* developing a sufficiently reliable evaluation dataset;
* managing model access and hardware constraints;
* separating genuine research improvement from additional prompt calls;
* preventing the engineering system from becoming larger than the research contribution.

Without a controlled benchmark, it would be difficult to determine whether BanglaMate failed because of an agent design, an incorrect social assumption, an unsuitable model, an ambiguous message, or an unreliable evaluation procedure.

## Revised Core Direction

The revised thesis places SocialCue-BN at the center of the research.

The thesis will create a controlled Romanized Bangla benchmark in which message families contain related contextual versions. Between the controlled A–B and A–C comparisons, only one planned social cue changes.

The controlled cues are:

* authority;
* relative age;
* familiarity;
* setting.

This design makes it possible to measure whether language models respond consistently and appropriately when a specific social relationship changes.

The final dataset will contain:

* 150 message families;
* three contextualized instances per family;
* 450 instances;
* TUI, TUMI, and APNI register labels;
* primary and acceptable-register annotations;
* family-safe development and test splits.

The core experiment will compare:

* three fixed free-tier API models;
* three prompt conditions;
* 4,050 total model responses;
* instance-level and controlled counterfactual behavior.

## Why the Revision Is Scientifically Stronger

The revised direction produces a clearer and more defensible scientific contribution.

Instead of claiming that a large communication system works, the thesis first establishes:

* what social-context problem is being measured;
* how individual cues are isolated;
* what counts as an acceptable answer;
* how model behavior changes across controlled pairs;
* whether structured context improves predictions;
* where existing models fail.

This approach improves:

* reproducibility;
* interpretability;
* experimental control;
* feasibility;
* error analysis;
* defensibility during examination.

The dataset does not need to be physically large in gigabytes. Its value comes from controlled design, culturally relevant annotation, and precise comparisons.

## Relationship to BanglaMate

BanglaMate has not been completely abandoned.

It has been repositioned as a small secondary extension that can run only after the core results are complete and frozen.

The extension will use:

* one fixed free-tier model;
* four role-based agents;
* 90 frozen test cases;
* direct, pre-Critic, and post-Critic comparisons;
* maximum one Critic-triggered revision;
* maximum 540 final test API calls;
* limited blinded human evaluation.

This structure allows the thesis to retain an agentic component without allowing it to endanger the core research.

The controlled benchmark logically comes first: a socially aware agent system cannot be evaluated convincingly until there is a controlled method for measuring whether it handles social cues correctly.

## Feasibility

The project is designed for an undergraduate thesis with limited hardware and financial resources.

The implementation will:

* use remote free-tier APIs;
* require no payment card;
* avoid local LLM inference;
* avoid fine-tuning;
* avoid knowledge-graph engineering;
* reuse one experiment runner across models;
* limit agent revision to one cycle;
* preserve all raw outputs for reproducibility.

Free-tier quotas may increase calendar waiting time, but they do not materially increase personal active-work time.

## Expected Contribution

The expected contribution is not a new foundational language model.

The expected contribution is:

1. a controlled Romanized Bangla social-register dataset;
2. a reproducible evaluation pipeline;
3. evidence about the effect of social-context prompting;
4. counterfactual consistency analysis;
5. culturally grounded error analysis;
6. a limited agentic demonstration built on top of the benchmark.

## Supervisor Decision Requested

Approval is requested for:

* SocialCue-BN as the primary thesis contribution;
* the controlled 150-family dataset;
* the three-model and three-prompt experiment;
* the reduced two-annotator coverage plan;
* legitimate zero-cost API use;
* BanglaMate as a strictly secondary gated extension.

This revision preserves the original interest in socially intelligent and agentic AI while establishing a more reliable experimental foundation within the graduation timeline.
