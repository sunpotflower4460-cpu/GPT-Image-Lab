# SNSAI Integration Contract

This document defines how GPT-Image-Lab should connect to SNSAI later without mixing research quality with distribution performance.

## When to connect SNSAI

Do not connect SNSAI at the beginning.

Recommended entry condition:

- at least 10 useful GPT-Image-Lab experiments completed
- research loop is stable
- prompt and critique records are reproducible
- at least a few outputs are clearly publishable
- there is enough data to distinguish experiment quality from random variation

At that point, create/prepare the dedicated social account and begin with a small number of human-reviewed posts before enabling broader automation.

## GPT-Image-Lab → SNSAI handoff

Each publishable experiment should expose a structured payload similar to:

```json
{
  "experiment_id": "0001",
  "asset": "experiments/0001/.../result.png",
  "category": "premium-product-photo",
  "finding": "Functional key/fill/rim descriptions improved subject separation.",
  "hypothesis": "...",
  "visual_score": 8.4,
  "fatal_flags": [],
  "novelty_angle": "AI studies lighting like a photographer",
  "known_weaknesses": ["background is slightly synthetic"],
  "before_after_available": true,
  "publication_status": "candidate"
}
```

Exact implementation may change, but keep the semantic separation.

## SNSAI responsibilities

SNSAI should decide:

- whether to publish
- which platform(s) to use
- hook / first line
- body copy
- CTA
- tags / metadata where useful
- posting time
- whether the post should be single-image, comparison, carousel, thread, etc.

SNSAI may use experiment findings as story material, but should not rewrite the underlying research record.

## Suggested public content pillars

A healthy mix can include:

1. **Result-first** — striking image first, short insight second
2. **Before / after** — show a controlled improvement
3. **Experiment log** — “Experiment #042: what changed?”
4. **Failure analysis** — visually interesting failure + lesson
5. **Prompt principle** — reveal one useful principle, not necessarily the full prompt
6. **Trend experiment** — test a currently popular visual format
7. **Challenge** — deliberately difficult image-generation task

This prevents the account from becoming a repetitive prompt dump.

## SNSAI → GPT-Image-Lab feedback

Return structured performance data after an appropriate observation window.

Example:

```json
{
  "experiment_id": "0001",
  "platform": "x",
  "post_id": "...",
  "published_at": "...",
  "metrics": {
    "impressions": null,
    "likes": null,
    "replies": null,
    "reposts": null,
    "bookmarks": null,
    "profile_visits": null,
    "follows": null,
    "clicks": null
  },
  "distribution_analysis": {
    "topic_demand": null,
    "hook_strength": null,
    "copy_clarity": null,
    "audience_fit": null,
    "timing_context": null
  }
}
```

## Feedback rule

Social feedback may influence future subject selection and presentation experiments, but it must not silently alter visual-quality rules.

Example:

Good conclusion:

> Surreal food images repeatedly earn higher save rates. Test whether the demand persists with different composition styles.

Bad conclusion:

> Surreal food is objectively better image generation.

## Exploration vs exploitation

Once enough data exists, SNSAI should balance:

- **Exploitation:** use themes / formats already shown to perform well
- **Exploration:** test new subjects, visual ideas, and hooks so the system does not become trapped in a local optimum

A future scheduler can reserve a portion of posts for explicit exploration.

## Data windows

Do not compare posts measured at wildly different ages without normalization.

Prefer checkpoints such as:

- early response
- 24-hour response
- 7-day response when relevant

Exact windows should adapt to the platform.

## Safety / quality gate

SNSAI should never auto-publish an asset with a fatal visual flag, unresolved policy concern, accidental private information, misleading real-person depiction risk, or clearly broken typography / anatomy when those elements are central to the post.

## note relationship

SNSAI optimizes ongoing social distribution.

The daily note workflow optimizes depth, education, trust, and product funnel.

They can use the same experiments but should package them differently.
