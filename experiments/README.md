# Experiments

Every experiment gets its own immutable folder.

## Naming

The implemented storage format uses a four-digit experiment ID as the directory name:

```text
0001
0002
0003
```

Never reuse an experiment ID. Human-readable subject and investigation names live inside `experiment.json` and `REPORT.md` rather than in the directory name, which keeps machine parsing and handoff stable.

## Phase 1 structure

```text
experiments/0001/
├── experiment.json
├── REPORT.md          # created only after successful finalization
└── assets/
    ├── README.md
    └── result.png     # or another durable output reference
```

`experiment.json` is the source record for the experiment. `REPORT.md` is a human-readable rendering of the finalized evidence.

## Lifecycle

Create the next draft:

```bash
gpt-image-lab new --subject "..." --investigation "..." --variable "..."
```

Validate it:

```bash
gpt-image-lab validate 0001
```

Finalize only when the research-loop gate passes:

```bash
gpt-image-lab finalize 0001
```

The next experiment receives the prior candidate learning and unresolved next hypothesis as starting memory.

## Immutability rule

Do not rewrite finalized experiment outcomes to match later beliefs.

The CLI/storage layer rejects finalizing the same experiment twice. If an interpretation changes later, create a new experiment and link the new evidence back to the original in its notes. Raw experimental history should remain auditable.

## Candidate versus durable knowledge

Finalization appends the result to `knowledge/LEARNINGS.md` as candidate evidence.

It does **not** automatically modify `knowledge/PROMPT_PLAYBOOK.md`. A durable rule requires replication, a strong controlled comparison, or another explicit evidence review.

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
