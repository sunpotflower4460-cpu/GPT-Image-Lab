# Phase 1 GitHub Experiment Workflow

This workflow exists to make the first ten evidence-gathering experiments easy to run without enabling autonomous hourly research too early.

## What it does

The manual GitHub Actions workflow `.github/workflows/phase1-experiment.yml` runs one already-planned experiment.

It performs:

1. validate the four-digit experiment ID
2. verify an `OPENAI_API_KEY` repository secret is available
3. check out `main`
4. install GPT-Image-Lab
5. run the no-cost Phase 1 preflight
6. create a unique review branch
7. generate the image
8. critique the image with the configured GPT-5.6 critic
9. validate the research record
10. write `REVIEW.md`
11. commit the experiment evidence to the review branch
12. open a pull request for human review

It intentionally does **not** call `finalize`.

## One-time credential requirement

Configure a GitHub Actions repository secret named:

```text
OPENAI_API_KEY
```

Never commit an API key to `.env`, workflow YAML, experiment JSON, README, issue, pull request, or any other repository file.

The repository `.gitignore` excludes `.env` and `.env.*`, but GitHub Actions should use the encrypted repository secret rather than an env file.

## Run Experiment 0001

In GitHub:

1. open **Actions**
2. choose **Phase 1 Experiment**
3. choose **Run workflow**
4. keep `experiment_id` as `0001`
5. keep the default critic model unless deliberately testing a critic change
6. run the workflow

A successful workflow creates a branch similar to:

```text
experiment/0001-run-<workflow-run-id>
```

and opens a pull request against `main`.

## Human review gate

Before merging the generated experiment pull request, inspect:

```text
experiments/0001/assets/result.png
experiments/0001/REVIEW.md
experiments/0001/experiment.json
experiments/0001/result-metadata.json
experiments/0001/critique-metadata.json
```

Check that:

- the image is a valid generation rather than a technical failure
- the automated visual critique is grounded in what is actually visible
- the hypothesis result is not stronger than the evidence supports
- confounds are acknowledged
- the candidate learning is specific rather than universal
- the next hypothesis is useful and changes no more than two primary variables

Merging the review PR means the generated evidence is accepted into the repository, but it still does not promote the candidate learning into the durable playbook.

## Why finalization is separate

During Phase 1, a generated result and an AI critique should not automatically become research memory merely because the API calls succeeded.

The human-review boundary gives us a chance to reject:

- broken generations
- hallucinated critique claims
- overconfident causal conclusions
- low-information experiments
- accidental prompt drift

After the review PR is accepted, finalization can append the candidate learning to `knowledge/LEARNINGS.md` and produce the immutable experiment report.

## Failure behavior

The workflow stops before a paid generation if:

- the experiment ID is malformed
- the API secret is missing
- the experiment planning record is incomplete

The runner is resumable at the repository level, but every GitHub workflow run starts from `main`. Do not launch multiple competing review runs for the same experiment unless an intentional retry is desired.

## Phase boundary

This workflow is **manual only** during Phase 1.

Do not add an hourly `schedule:` trigger until Experiments 0001–0010 demonstrate that the system consistently turns prior evidence into better follow-up questions.
