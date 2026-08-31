# Evaluation Rubric

Use this rubric to evaluate generated images consistently across experiments.

Scores are useful only when accompanied by evidence.

## Visual quality score

Score each category from 1–10.

### 1. Composition

Questions:

- Is visual hierarchy clear?
- Is attention guided intentionally?
- Does framing feel deliberate rather than accidental?
- Are balance, negative space, and subject placement appropriate?

### 2. Lighting

Questions:

- Is the light physically and visually coherent?
- Does it support the subject?
- Are highlights, shadows, reflections, and edge light believable?
- Does the lighting create the intended mood?

### 3. Color design

Questions:

- Is the palette coherent?
- Is contrast controlled?
- Does color support hierarchy and emotion?
- Are there muddy or unintentionally oversaturated regions?

### 4. Materials and texture

Questions:

- Do surfaces look materially distinct?
- Are skin, glass, metal, fabric, wood, water, etc. rendered plausibly?
- Are textures too smooth, noisy, plastic, or over-sharpened?

### 5. Depth and spatial coherence

Questions:

- Is foreground / subject / background separation convincing?
- Is perspective coherent?
- Does depth of field make visual sense?
- Are scale relationships believable?

### 6. Instruction adherence

Questions:

- Did the model follow the requested subject, pose, layout, text, aspect, mood, and constraints?
- Were important requested details omitted or altered?

### 7. Artifact control

Questions:

- Are there anatomical, typographic, geometric, texture, or reflection artifacts?
- Do edges break unnaturally?
- Are there hidden AI-generation tells?

A high score means fewer meaningful artifacts.

### 8. Originality / concept clarity

Questions:

- Does the image have a distinctive idea?
- Does it avoid feeling like generic AI imagery?
- Is the concept understandable without explanation?

### 9. Professional finish

Questions:

- Could this plausibly be used in a commercial campaign, editorial, album cover, poster, or professional portfolio?
- Does it feel art-directed?
- Is there an obvious unfinished region?

### 10. Social stopping power

This is still a visual score, not a performance metric.

Questions:

- Would the image interrupt passive scrolling?
- Is there a strong first-read focal point?
- Is there enough novelty or emotional clarity to earn attention?

## Suggested visual total

Average the 10 visual categories for a 1–10 visual score.

Do not optimize blindly for the average. A single fatal failure may matter more than a small change in total score.

## Fatal-failure flags

Record separately as true/false:

- anatomy failure
- text failure
- identity / character inconsistency
- broken object geometry
- impossible reflection / lighting failure
- obvious generation artifact
- wrong aspect / layout
- copyright / brand-risk concern
- safety / policy concern
- unusable crop

## Hypothesis-specific metric

Every experiment must define at least one metric tied directly to the hypothesis.

Examples:

- edge-light naturalness
- typography legibility
- glass realism
- face consistency
- subject/background separation
- material differentiation
- premium-ad impression

Score 1–10 and explain what changed.

## Confidence

After critique, assign confidence:

- **Low** — result is noisy, subjective, or confounded
- **Medium** — evidence is meaningful but needs repetition
- **High** — repeated controlled results support the finding

High confidence should normally require more than one experiment.

# Social performance rubric

Use only after SNSAI is connected.

Do not merge these metrics into the visual-quality score.

## Raw metrics

Record where available:

- impressions / views
- likes
- replies
- reposts / shares
- bookmarks / saves
- profile visits
- link clicks
- follows
- watch time when relevant

## Derived metrics

Where data allows:

- engagement rate
- save rate
- follow conversion rate
- click-through rate
- repost/share rate

## Distribution analysis

After each sufficiently mature post, estimate each factor separately from 1–10:

- image strength
- topic demand
- hook strength
- copy clarity
- curiosity gap
- audience fit
- timing / distribution context

These are hypotheses, not ground truth.

## Interpretation rule

Never conclude:

> This image is visually better because it received more impressions.

Prefer:

> This post outperformed. Candidate explanations are stronger topic demand and a clearer hook; the visual rubric improved only slightly. Run a controlled follow-up before attributing the gain to image quality.
