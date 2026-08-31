# Experiments

Every experiment gets its own immutable folder.

## Naming

Use:

```text
NNNN-short-descriptive-slug
```

Examples:

```text
0001-functional-rim-light
0002-glass-material-language
0003-premium-typography-layout
```

Never reuse an experiment ID.

## Minimum contents

During the early manual phase, one Markdown file based on `templates/EXPERIMENT_TEMPLATE.md` is enough, plus the generated image or a durable reference to it.

Suggested mature structure:

```text
experiments/0001-example/
├── experiment.md
├── result.png
├── result-metadata.json
└── references.md
```

Split the Markdown into separate `research.md`, `prompt.md`, `critique.md`, etc. only when automation or scale makes that genuinely useful.

## Immutability rule

Do not rewrite old experiment outcomes to match later beliefs.

If an interpretation changes later, add a dated correction / follow-up reference instead. Raw experimental history should remain auditable.

## Failed runs

Generation errors, API failures, broken outputs, and aborted runs may be recorded, but distinguish:

- **technical failure** — no valid image/evidence produced
- **visual failure** — valid image produced but quality/hypothesis failed
- **research failure** — experiment was too confounded or vague to teach much

Technical failures must never become prompt-learning evidence.

## Replications

A replication gets a new experiment ID and links back to the original.

Do not overwrite the original result.

## First milestone

The first goal is not 24 experiments per day.

The first goal is **10 consecutive useful experiments** that demonstrate genuine accumulated learning.
