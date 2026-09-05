# SocialCue-BN

Undergraduate Computer Science thesis on controlled evaluation of
Tui–Tumi–Apni selection and register-aware rewriting in Romanized Bangla.


## Core study

- 150 message families
- 450 context-conditioned instances
- Three API models
- Three prompt conditions
- 4,050 planned core responses

## Controlled extension

- 90 frozen test cases
- Direct rewrite baseline
- Full four-agent BanglaMate
- No-Critic ablation
- Maximum one Critic-triggered revision

## Important rule

Do not start the pilot dataset until the supervisor approves
docs/SCOPE_CONFIRMATION.md.

## Environment and Hardware

### Development Environment

* Operating system: Windows 10, 64-bit
* Python implementation: Standard CPython with GIL enabled
* Python version: 3.14.5
* Virtual environment directory: `.venv`
* Primary editor: Visual Studio Code
* Version control: Git and GitHub Desktop

### Hardware Constraint

* Processor: 11th Generation Intel Core i3
* Memory: 8 GB RAM
* Local execution: CPU-only
* Local LLM inference: Not included in the required workflow
* Model inference: Remote free-tier APIs only
* Financial API limit: USD 0

The local computer will be used for:

* dataset validation;
* API-request orchestration;
* response parsing;
* statistical analysis;
* tables and figures;
* thesis writing.

The local computer will not be used for:

* LLM training;
* LLM fine-tuning;
* large-model inference;
* knowledge-graph training;
* GPU-dependent experimentation.

### Reproducibility Rule

All project dependencies must be installed inside the local `.venv` virtual environment. Package versions will be locked in `requirements.txt` after the environment has been tested.

API keys must never be stored in this README, source code, notebooks, screenshots, or GitHub.
