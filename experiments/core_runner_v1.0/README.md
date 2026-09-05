# SocialCue-BN — Step 2 Experiment Runner v1.0

This standalone folder contains the frozen Step 1 benchmark/prompts and the complete Step 2 experiment runner. Do not merge it manually with the earlier Step 1 folder.

## Included

- Adjudicated benchmark: 450 instances in 150 A/B/C families.
- Family-safe split: 90 DEVELOPMENT and 360 locked TEST instances.
- Frozen P0, P1, and P2 prompts.
- Three free-tier model candidates:
  - Google `gemini-3.5-flash-lite`
  - Groq `openai/gpt-oss-120b`
  - Groq `qwen/qwen3.8-27b`
- Resumable API runner, parser, tests, metrics, and dummy results.

The model candidates will be frozen only after the 90-call DEVELOPMENT dry run succeeds. TEST remains locked.

## Action 1 — Validate locally

Open this folder in VS Code, select **Terminal → New Terminal**, and run:

```powershell
python validate_package.py
```

Then run:

```powershell
python -m unittest discover -s tests -v
```

The first command must show four `PASS` lines. The tests must end with `OK`.

## Action 2 — Create and set free API keys

Create one key from each provider:

- Google AI Studio: <https://aistudio.google.com/apikey>
- GroqCloud: <https://console.groq.com/keys>

Free-tier availability and exact quotas can vary by account and region. You do not need to enable a paid plan for the dry run when the free tier is available.

In the same VS Code PowerShell terminal, enter:

```powershell
$env:GEMINI_API_KEY="PASTE_YOUR_GOOGLE_KEY_HERE"
$env:GROQ_API_KEY="PASTE_YOUR_GROQ_KEY_HERE"
```

Replace only the text inside the quotation marks. Never send either key to another person or paste it into ChatGPT, a source file, Git, or a screenshot.

Check all three endpoints with three total calls:

```powershell
python check_api_access.py
```

Continue only if the final line says:

```text
PASS: All three model endpoints are accessible. Three total test calls completed.
```

## Action 3 — Run and validate the 90-call dry run

Run:

```powershell
python run_development_dry_run.py
```

The access check already completed one request per model. This command resumes those files and completes `10 instances × 3 prompts × 3 models = 90` total records without repeating successful calls.

When it finishes, run:

```powershell
python validate_development_dry_run.py
```

The last line must say:

```text
PASS: All 90 DEVELOPMENT dry-run records are complete and safe for analysis.
```

Upload these three files for the next analysis step:

```text
results/raw/development_gemini_3_5_flash_lite.jsonl
results/raw/development_groq_gpt_oss_120b.jsonl
results/raw/development_groq_qwen_3_8_27b.jsonl
```

Do not upload `.env` or API keys. Do not run TEST yet.

## If a command stops

- Keep the terminal output.
- Do not delete any JSONL result file.
- Run the same command again after fixing the reported key or rate-limit problem.
- Successful calls are detected and skipped automatically.

Transient provider failures are stored separately in `*.errors.jsonl`; they are not counted as completed benchmark responses.

## Frozen request settings

- Temperature: `0.0`
- Maximum completion tokens: `256`
- Gemini 3.5 Flash-Lite reasoning: minimal; temperature: provider default
- GPT-OSS 120B reasoning: low, reasoning text excluded
- Qwen 3.8 27B reasoning: disabled
- Output request: one JSON object containing `register`, `confidence`, and `reason_codes`

These settings must not be changed after the DEVELOPMENT dry run is approved.

## Official references

- Gemini pricing: <https://ai.google.dev/gemini-api/docs/pricing>
- Gemini OpenAI compatibility: <https://ai.google.dev/gemini-api/docs/openai>
- Groq models: <https://console.groq.com/docs/models>
- Groq reasoning controls: <https://console.groq.com/docs/reasoning>
- Groq free-plan rate limits: <https://console.groq.com/docs/rate-limits>
