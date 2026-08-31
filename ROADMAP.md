# Roadmap

## Phase 0 — Foundation

Goal: define how GPT-Image-Lab learns before adding automation.

- [x] Define project mission and core loop
- [x] Separate image-quality signals from social-performance signals
- [x] Finalize research-loop protocol
- [x] Finalize evaluation rubric
- [x] Finalize experiment template
- [x] Implement experiment validation / storage core
- [x] Implement candidate-learning memory with no automatic playbook promotion
- [x] Implement CLI for new / status / validate / finalize / show
- [ ] Run Experiment 0001 manually

## Phase 1 — Ten useful experiments

Exit condition: 10 consecutive experiments each reuse prior knowledge and produce a concrete next hypothesis.

Supporting tooling is implemented; the evidence-gathering sequence itself remains intentionally manual/semi-manual until the exit condition is met.

- [ ] Experiment 0001
- [ ] Experiment 0002
- [ ] Experiment 0003
- [ ] Experiment 0004
- [ ] Experiment 0005
- [ ] Experiment 0006
- [ ] Experiment 0007
- [ ] Experiment 0008
- [ ] Experiment 0009
- [ ] Experiment 0010

Do not automate hourly execution before this exit condition is met.

## Phase 2 — Research automation

Build one command/job that can:

1. read recent experiments and durable knowledge
2. gather fresh research when useful
3. choose a topic and a small experimental variable set
4. write hypothesis and prompt plan
5. call image generation
6. critique the output
7. write experiment artifacts
8. update durable learnings only when evidence is strong enough

Add safeguards for duplicated themes, repeated hypotheses, low-information experiments, and accidental overwriting of prior knowledge.

## Phase 3 — Hourly research

After the loop is reliable:

- schedule at most once per hour
- persist every run with an experiment ID
- allow failed generations to be recorded without poisoning the knowledge base
- add cost / quota guards
- add retry and failure logging
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
