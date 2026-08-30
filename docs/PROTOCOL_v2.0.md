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