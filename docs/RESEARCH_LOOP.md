# Research Loop Protocol

This document defines the minimum protocol for every GPT-Image-Lab experiment.

## Rule 0 — An experiment must teach something

Do not generate an image only because an hour has passed.

A run should begin only when it can state:

- what is being investigated
- why it matters
- what is being changed
- what evidence would count as improvement or failure

If these cannot be stated, the run should become a research/planning run instead of a generation run.

## Step 1 — Read memory

Before deciding what to generate:

1. Read the most recent experiment.
2. Read the most relevant durable knowledge in `knowledge/`.
3. Check recent subject/theme history to avoid accidental repetition.
4. Check unresolved hypotheses from prior experiments.

Output:

- relevant prior findings
- unresolved question
- candidate direction

## Step 2 — Observe and reflect

Inspect the previous output and record at least three observations.

Required categories:

1. **What worked**
2. **What did not work**
3. **What remains uncertain**

Avoid vague statements such as “make it more professional.”

Prefer statements such as:

- subject separation improved, but rim light created an unnatural halo on the left edge
- texture detail increased, but the surface now looks over-sharpened
- typography is legible, but letter spacing looks generic and weakens the premium impression

## Step 3 — Gather information

Gather new information only when it helps the current question.

Possible sources:

- current social / visual trends
- photography and cinematography techniques
- graphic-design principles
- advertising references
- art direction
- prior GPT-Image-Lab experiments
- model-specific prompting behavior

Record:

- what was learned
- why it is relevant
- any uncertainty or conflicting guidance

Do not paste research without turning it into a usable hypothesis.

## Step 4 — Choose the subject

The subject may vary widely to keep the public output interesting.

Examples:

- product advertising
- portraits
- landscapes
- anime / illustration
- album covers
- posters
- food
- architecture
- fantasy
- editorial photography
- infographics

Subject diversity is encouraged.

However, the experimental variables must remain controlled.

## Step 5 — Define the hypothesis

Every experiment must name 1–2 primary variables.

Example:

> Hypothesis: specifying key, fill, and rim light by function rather than saying “cinematic lighting” will improve subject separation and perceived commercial quality without increasing visible lighting artifacts.

Record:

- hypothesis
- primary variable(s)
- variables intentionally held stable
- expected benefit
- possible downside

## Step 6 — Design the prompt

Build the prompt intentionally.

Recommended structure:

1. Subject
2. Concept / narrative intent
3. Composition
4. Camera / lens language
5. Lighting
6. Color palette
7. Material / texture
8. Environment
9. Depth / atmosphere
10. Emotional direction
11. Art direction
12. Typography if relevant
13. Micro-details
14. Output purpose / format
15. Constraints
16. Avoid / failure controls

Not every section must be long. Remove sections that do not help the image.

Record both:

- final prompt
- short rationale for the experimental changes

## Step 7 — Generate

Store generation metadata whenever available:

- experiment ID
- model
- timestamp
- prompt version
- image dimensions / aspect ratio
- quality setting
- reference images used
- seed or equivalent if available
- estimated or actual cost if available

## Step 8 — Critique

Evaluate the result using `docs/EVALUATION_RUBRIC.md`.

Critique from at least three viewpoints:

- visual craft / art direction
- prompt adherence / model behavior
- commercial or social usability

Record evidence, not only scores.

## Step 9 — Compare to hypothesis

Choose one result:

- supported
- partially supported
- not supported
- inconclusive

Explain why.

Also record confounds: anything that changed or occurred that makes the result difficult to interpret.

## Step 10 — Extract learning

Write:

- strongest observed learning
- confidence: low / medium / high
- scope: where the learning likely applies
- where it may not apply
- whether it deserves promotion into a durable playbook yet

A single experiment normally creates a **candidate learning**, not a universal rule.

## Step 11 — Define the next hypothesis

Every generation should leave a useful next question.

The next experiment should either:

- validate the finding
- test its boundary
- isolate a confounding factor
- apply the principle to a new subject
- investigate the next largest weakness

## Step 12 — Distribution handoff (future)

If the output is publishable, prepare structured metadata for SNSAI:

- experiment ID
- image path / asset reference
- one-sentence finding
- visual category
- novelty angle
- recommended audience promise
- known weaknesses
- whether this is suitable for public comparison / before-after presentation

SNSAI owns copy and distribution decisions.

## Step 13 — Social feedback (future)

When performance data returns, do not say “high impressions = better image.”

Analyze possible drivers separately:

- visual strength
- topic demand
- hook / copy
- posting time
- audience fit
- novelty
- controversy / curiosity
- platform effects

Social data generates a new hypothesis. It does not overwrite visual critique.

## Minimum completion checklist

An experiment is complete only when it contains:

- [ ] previous-result observations
- [ ] relevant research or explicit reason no new research was needed
- [ ] hypothesis
- [ ] 1–2 experimental variables
- [ ] final prompt
- [ ] generated output reference
- [ ] rubric scores and qualitative critique
- [ ] hypothesis result
- [ ] candidate learning
- [ ] confidence / confounds
- [ ] next hypothesis
