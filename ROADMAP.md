# Roadmap

## Phase 0 — Foundation

Goal: define how GPT-Image-Lab learns before adding autonomous research.

- [x] Define project mission and core loop
- [x] Separate image-quality signals from social-performance signals
- [x] Finalize research-loop protocol
- [x] Finalize evaluation rubric
- [x] Finalize experiment template
- [x] Implement experiment validation / storage core
- [x] Implement candidate-learning memory with no automatic playbook promotion
- [x] Implement CLI for new / status / validate / finalize / show
- [x] Implement safe GPT-Image-2 generation adapter
- [x] Implement structured GPT-5.6 visual critique
- [x] Implement resumable Phase 1 runner and human-review gate
- [x] Prepare Experiment 0001 research / hypothesis / prompt
- [x] Add CI readiness checks for Experiment 0001
- [ ] Execute and finalize Experiment 0001 with a live API credential

## Phase 1 — Ten useful experiments

Exit condition: 10 consecutive experiments each reuse prior knowledge and produce a concrete next hypothesis.

Supporting execution tooling is implemented. Topic selection, fresh research, hypothesis formation, and prompt design remain deliberate during this phase; generation and critique may be executed through the resumable runner.

Normal prepared-experiment flow:

```text
research + planning
      ↓
gpt-image-lab run NNNN
      ↓
REVIEW.md + image
      ↓
human review
      ↓
gpt-image-lab finalize NNNN
      ↓
candidate learning + next hypothesis
```

- [ ] Experiment 0001 — functional key/fill/rim lighting baseline on clear glass
- [ ] Experiment 0002
- [ ] Experiment 0003
- [ ] Experiment 0004
- [ ] Experiment 0005
- [ ] Experiment 0006
- [ ] Experiment 0007
- [ ] Experiment 0008
- [ ] Experiment 0009
- [ ] Experiment 0010

Do not enable autonomous hourly research before this exit condition is met.

## Phase 2 — Research automation

Build one research-planning job that can:

1. read recent experiments and durable knowledge
2. gather fresh research when useful
3. choose a topic and a small experimental variable set
4. write hypothesis and prompt plan
5. hand the prepared experiment to the existing runner
6. interpret critique and recent evidence
7. propose knowledge promotion only when evidence is strong enough

Add safeguards for duplicated themes, repeated hypotheses, low-information experiments, overfitting to one subject, and accidental overwriting of prior knowledge.

## Phase 3 — Hourly research

After the loop is reliable:

- schedule at most once per hour
- persist every run with an experiment ID
- allow technical and visual failures to be recorded without poisoning the knowledge base
- add cost / quota guards
- add bounded retry and failure logging
- prevent simultaneous runs from claiming the same experiment ID
- generate a daily summary from that day's runs

## Phase 4 — SNS account + SNSAI

Create and prepare the dedicated social account when the research loop is stable enough to show publicly.

Start with a small number of human-reviewed posts, then connect SNSAI.

SNSAI responsibilities:

- choose publishable experiments
- write platform-native hooks and copy
- decide presentation format
- schedule / publish where permitted
- collect performance metrics
- distinguish topic, copy, timing, and image effects

## Phase 5 — Closed feedback loop

Feed SNS results back to GPT-Image-Lab.

Never use raw popularity as a direct replacement for visual-quality evaluation.

Maintain two models:

- **Visual model:** what makes the image better?
- **Distribution model:** what makes people stop, react, save, click, or follow?

Use both when choosing future experiments.

## Phase 6 — note daily draft

Once per day:

1. rank the day's experiments by educational value, not only engagement
2. select the strongest story / finding
3. prepare title, body, images, partial prompt, finding, next hypothesis, CTA, and tags
4. place the content into a draft workflow where feasible
5. human performs final review and Publish

Target human workload: one short review session per day.

## Phase 7 — Knowledge compression

Periodically consolidate repeated findings into playbooks:

- lighting
- composition
- realism
- materials
- typography
- character consistency
- advertising
- cinematic imagery
- social stopping power
- prompt architecture

A finding should become a rule only after repeated evidence or a sufficiently strong controlled comparison.

## Phase 8 — Productization

Potential product direction:

**GPT Image Prompt OS / Image Generation Methodology**

Package validated principles, diagnostic logic, prompt architecture, correction patterns, and reusable workflows.

The moat should be accumulated experimental learning, not a static prompt dump.
