# GPT-Image-Lab

GPT-Image-Lab is an experimental research system for continuously improving GPT-based image generation through repeated observation, hypothesis, prompt design, generation, critique, and learning.

The goal is not to collect prompts. The goal is to build a **living image-generation methodology** that becomes better after every experiment.

## Core loop

Each experiment follows the same cycle:

1. **Research** — collect current visual trends, techniques, references, and prior findings.
2. **Observe & Reflect** — inspect the previous result and identify strengths, failures, and uncertainty.
3. **Form a Hypothesis** — decide what 1–2 variables to test next.
4. **Design the Prompt** — build a professional prompt with explicit visual intent.
5. **Generate** — create the image.
6. **Critique** — evaluate both visual quality and instruction adherence.
7. **Record Learning** — write candidate findings back into the repository.
8. **Prepare Distribution** — later, pass selected outputs to SNSAI and prepare a daily note draft.
9. **Learn from Response** — later, feed social performance back into the research loop without confusing popularity with image quality.

## Principle

**Change the subject freely; change only 1–2 experimental variables at a time.**

This keeps public output visually diverse while preserving the ability to learn from experiments.

## Runnable research core

The repository includes a Python core that manages experiment IDs, research records, validation, reports, candidate-learning memory, next-hypothesis handoff, and controlled OpenAI image generation.

### Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

### Start an experiment

```bash
gpt-image-lab new \
  --subject "premium glass product photograph" \
  --investigation "test functional key/fill/rim light language" \
  --why "improve lighting controllability" \
  --hypothesis "functional light-role language will improve subject separation" \
  --variable "functional lighting-role language"
```

This creates `experiments/0001/experiment.json` plus an `assets/` directory. From Experiment 0002 onward, `new` automatically carries the latest candidate learning and next hypothesis into the new draft.

### Inspect the generation request without spending anything

```bash
gpt-image-lab generate 0001 --dry-run
```

Dry run validates model, prompt, size, quality, and output location but makes no API request.

### Generate the image

The OpenAI Image API is used for the actual render. Configure `OPENAI_API_KEY` in the execution environment, then run:

```bash
gpt-image-lab generate 0001
```

Generation writes:

```text
experiments/0001/assets/result.png
experiments/0001/result-metadata.json
```

The sidecar metadata records provider, model, timestamp, prompt version, dimensions, quality, byte count, and SHA-256. The experiment JSON is updated with the generation timestamp only after a successful render.

Safety rules:

- finalized experiments cannot be regenerated
- an existing result is never overwritten by default
- `--overwrite` is allowed only as an explicit pre-finalize retry
- output paths cannot escape the experiment directory
- generated results are stored as PNG

### Complete the record

After generation, fill in `experiment.json` with:

- previous-result observations: worked / failed / uncertain (not required for the bootstrap experiment)
- research and source notes
- one explicit hypothesis
- 1–2 primary variables
- final prompt and rationale
- ten visual scores with evidence
- a hypothesis-specific metric
- three critique viewpoints
- hypothesis result and confounds
- candidate learning, confidence, scope, limits
- next hypothesis

### Validate before accepting the experiment

```bash
gpt-image-lab validate 0001
```

An experiment cannot pass if required research evidence is missing.

### Finalize

```bash
gpt-image-lab finalize 0001
```

Finalization:

1. validates the research-loop completion gate
2. writes `experiments/0001/REPORT.md`
3. appends the finding to `knowledge/LEARNINGS.md`
4. preserves the next hypothesis for the next run

It **never automatically promotes a single result into `PROMPT_PLAYBOOK.md`**, even if the experiment requests promotion. Durable rules require repeated or unusually strong evidence.

### Check lab status

```bash
gpt-image-lab status
```

## Repository structure

```text
GPT-Image-Lab/
├── AGENTS.md
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── src/gpt_image_lab/
│   ├── __init__.py
│   ├── cli.py
│   ├── generation.py
│   ├── models.py
│   └── storage.py
├── tests/
│   ├── test_core.py
│   └── test_generation.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RESEARCH_LOOP.md
│   ├── EVALUATION_RUBRIC.md
│   ├── SNSAI_INTEGRATION.md
│   └── NOTE_WORKFLOW.md
├── templates/
│   ├── EXPERIMENT_TEMPLATE.md
│   └── DAILY_REPORT_TEMPLATE.md
├── knowledge/
│   ├── PROMPT_PLAYBOOK.md
│   └── LEARNINGS.md
└── experiments/
    ├── README.md
    └── 0001/
        ├── experiment.json
        └── assets/
```

## Two separate score systems

A central rule of this project is:

> **Image quality is not the same thing as social performance.**

A visually excellent image can underperform because of topic, timing, copy, or audience fit. A mediocre image can spread because the topic is unusually strong.

The lab therefore keeps visual evaluation separate from future SNSAI performance metrics.

## Research quality gates

The code enforces several rules from `docs/RESEARCH_LOOP.md`:

- at least one worked, failed, and uncertain observation for standard experiments
- research evidence or an explicit reason new research was unnecessary
- exactly 1–2 primary variables
- all ten visual-rubric scores, each with evidence
- one hypothesis-specific metric
- critique from visual craft, prompt adherence/model behavior, and commercial/social usability viewpoints
- explicit hypothesis result
- candidate learning and confidence
- concrete next hypothesis

## Model reproducibility

Research experiments should prefer a pinned GPT Image snapshot when a snapshot is available. This prevents a moving model alias from silently changing during controlled comparisons. A later GPT Image snapshot should be treated as a new model epoch and compared deliberately before durable prompt rules are transferred.

## Intended evolution

1. **Phase 0 — Foundation:** protocol, rubric, templates, repository rules.
2. **Phase 1 — Ten useful experiments:** prove that the memory loop produces better questions. Manual API-backed rendering is allowed; autonomous hourly planning is not.
3. **Phase 2 — Research automation:** automate research → hypothesis → prompt → generation → critique → learning after Phase 1 evidence exists.
4. **Phase 3 — Hourly research:** schedule the proven loop with cost, retry, and failure guards.
5. **Phase 4 — SNSAI:** publish selected experiments and collect distribution data.
6. **Phase 5 — Closed feedback:** feed SNS results back without treating popularity as image quality.
7. **Phase 6 — note daily draft:** generate one coherent daily research article for human final publish.
8. **Phase 7 — Knowledge compression:** convert repeated findings into durable playbooks.
9. **Phase 8 — Productization:** package the validated methodology as a Prompt OS / image-generation system.

## Current milestone

Before connecting SNSAI or hourly scheduling, GPT-Image-Lab should complete **10 useful experiments in a row** where each experiment clearly reuses earlier learning and produces a concrete next hypothesis.

## Definition of a successful experiment

An experiment is successful even if the image is worse, provided that it produces a defensible learning:

- what changed
- what improved
- what degraded
- what remains uncertain
- what should be tested next

Failures without recorded learning are waste. Failures with precise learning are research.
