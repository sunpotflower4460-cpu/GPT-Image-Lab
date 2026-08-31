# GPT-Image-Lab Agent Operating Rules

This file defines how AI agents should work inside this repository.

## Mission

Continuously improve GPT-based image generation through evidence-driven experiments while preserving a clear record of what was tried, what happened, and what should happen next.

The system is not rewarded for generating more images. It is rewarded for producing **useful learning**.

## Mandatory behavior before every generation

Before generating an image, the agent must perform at least these three reasoning activities and record their outputs:

1. **Previous observation and reflection**
   - what worked
   - what failed
   - what remains uncertain
2. **Prompt-improvement analysis**
   - what part of the prompt architecture should change and why
3. **Research and hypothesis formation**
   - relevant prior knowledge and/or fresh information
   - one explicit testable hypothesis

The agent may perform additional analyses when useful.

## Experimental discipline

- Subjects may change each run.
- Change only 1–2 primary experimental variables at a time whenever possible.
- Do not claim causality from uncontrolled comparisons.
- Do not promote one lucky result into a universal rule.
- Record confounding factors.
- Failed images are valid research when they produce specific learning.
- Repeating an experiment is allowed when it validates or challenges a finding.
- Repeating a theme merely because it is easy is discouraged.

## Memory discipline

Before inventing a new technique:

1. check relevant files in `knowledge/`
2. check recent experiments
3. reuse validated findings where appropriate
4. identify whether the new experiment is exploration, validation, boundary testing, or application

Do not append every observation to durable knowledge.

A new finding should first be treated as a **candidate learning**.

Promote it to `knowledge/PROMPT_PLAYBOOK.md` only when:

- repeated evidence supports it, or
- a controlled comparison provides unusually clear evidence, and
- its scope and limitations can be stated.

## Prompt discipline

Prompt length is not a goal.

Every instruction should serve an intended visual effect.

Prefer explicit art direction over stacks of generic quality adjectives.

When useful, consider:

- subject
- concept
- composition
- camera / lens language
- lighting roles
- color system
- materials
- spatial depth
- emotional direction
- typography
- output context
- constraints
- known failure controls

Do not blindly copy old prompts. Reuse principles, not accidental wording.

## Critique discipline

Use `docs/EVALUATION_RUBRIC.md`.

Scores without evidence are insufficient.

Always distinguish:

- visual craft
- prompt adherence
- model artifacts
- concept strength
- professional usability
- social stopping power

When SNS data exists, keep it separate from visual-quality scoring.

## SNS discipline

SNSAI is a distribution partner, not the authority on image quality.

Social performance may inform:

- topic demand
- packaging
- hooks
- presentation format
- audience fit
- future exploration priorities

It must not silently redefine visual truth.

## note discipline

Do not create one note article for every hourly run.

The daily note draft should select the day's most educational or compelling finding and turn it into one coherent story.

A good note draft should include:

- the question
- why it mattered
- what was tried
- the visual result
- what changed
- what was learned
- what remains uncertain
- what will be tested next
- a useful partial principle for the reader
- an appropriate CTA

## Automation discipline

Do not enable hourly autonomous generation until the manual/semi-manual research loop has demonstrated at least 10 useful consecutive experiments.

When hourly automation is added:

- every run needs a unique experiment ID
- no existing experiment may be overwritten
- failed runs must be logged
- generation/API failures must not become false learnings
- cost/quota guards should exist
- duplicated hypotheses should be detected
- low-information runs should be allowed to stop before generation

## Truthfulness

Never write that an experiment proved something when the evidence is weak.

Use calibrated language:

- observed
- suggests
- partially supported
- needs replication
- inconclusive
- contradicted by this run

## North star

Over time, raw experiment count matters less than the quality of the compressed knowledge.

The desired end state is a reliable **Prompt OS / image-generation methodology** that can diagnose a visual goal, select relevant principles, construct a prompt, evaluate the output, and improve itself from evidence.
