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
7. **Record Learning** — write durable findings back into the repository.
8. **Prepare Distribution** — later, pass selected outputs to SNSAI and prepare a daily note draft.
9. **Learn from Response** — later, feed social performance back into the research loop without confusing popularity with image quality.

## Principle

**Change the subject freely; change only 1–2 experimental variables at a time.**

This keeps the feed visually diverse while preserving the ability to learn causally from experiments.

## Research dimensions

- composition and visual hierarchy
- lighting and shadow structure
- lens / camera language
- depth and atmosphere
- color design
- material and texture rendering
- realism and artifact reduction
- typography and text accuracy
- character consistency
- product and advertising imagery
- cinematic imagery
- illustration styles
- social-feed stopping power
- emotional clarity
- prompt structure and instruction ordering

## Repository structure

```text
GPT-Image-Lab/
├── README.md
├── ROADMAP.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RESEARCH_LOOP.md
│   ├── EVALUATION_RUBRIC.md
│   └── SNSAI_INTEGRATION.md
├── templates/
│   ├── EXPERIMENT_TEMPLATE.md
│   └── DAILY_REPORT_TEMPLATE.md
├── knowledge/
│   ├── PROMPT_PLAYBOOK.md
│   └── LEARNINGS.md
└── experiments/
    └── (one folder per experiment)
```

A future experiment may look like:

```text
experiments/0001-rim-light-product-photo/
├── research.md
├── hypothesis.md
├── prompt.md
├── critique.md
├── result-metadata.json
└── result.png
```

## Two separate score systems

A central rule of this project is:

> **Image quality is not the same thing as social performance.**

A visually excellent image can underperform because of topic, timing, copy, or audience fit. A mediocre image can spread because the topic is unusually strong.

Therefore the system keeps separate measurements for image quality and distribution performance.

### Image quality
- composition
- lighting
- color
- texture/material quality
- instruction adherence
- realism / artifact control
- originality
- professional finish

### Distribution performance
- impressions
- engagement rate
- likes
- saves / bookmarks when available
- replies
- clicks
- follows attributable to the post when available
- hook / copy quality
- topic demand
- posting context

## Intended evolution

### Phase 1 — Research foundation
Run experiments manually and make sure each cycle produces useful learning.

### Phase 2 — Automated research loop
Automate research → hypothesis → prompt → generation → critique → repository update.

### Phase 3 — SNSAI connection
Create/prepare the social account, let SNSAI select outputs and create posts, and collect response data.

### Phase 4 — Feedback learning
Feed social data back into GPT-Image-Lab while keeping visual-quality and popularity signals separate.

### Phase 5 — Daily note draft
Automatically select the most educational experiments of the day and prepare one polished daily note draft. Human reviews and presses Publish.

### Phase 6 — Knowledge compression
Periodically convert raw experiments into durable playbooks such as lighting, realism, typography, characters, advertising, and social visuals.

### Phase 7 — Productization
Turn validated findings into a Prompt OS / image-generation methodology rather than selling a static prompt list.

## Current milestone

Before connecting SNSAI or hourly scheduling, GPT-Image-Lab should complete **at least 10 useful experiments in a row** where each experiment clearly uses earlier learning and produces a concrete next hypothesis.

## Definition of a successful experiment

An experiment is successful even if the image is worse, provided that it produces a defensible learning:

- what changed
- what improved
- what degraded
- what remains uncertain
- what should be tested next

Failures without recorded learning are waste. Failures with precise learning are research.

## Status

Initial research foundation. SNS automation and note drafting should be added only after the research loop itself is reliable.
