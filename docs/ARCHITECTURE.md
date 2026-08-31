# Architecture

## Purpose

GPT-Image-Lab is designed as a learning system, not merely an image generator.

The system should improve by converting every generation into structured evidence that can influence later generations.

## High-level architecture

```text
Fresh research / trends
        │
        ▼
Research Planner
        │
        ├── reads recent experiments
        ├── reads durable knowledge
        └── chooses one focused hypothesis
        │
        ▼
Prompt Designer
        │
        ▼
Image Generator
        │
        ▼
Visual Critic
        │
        ├── image-quality score
        ├── instruction-adherence score
        └── qualitative observations
        │
        ▼
Learning Writer
        │
        ├── experiment record
        ├── candidate learning
        └── next hypothesis
        │
        ▼
Repository Memory
        │
        ├───────────────┐
        ▼               ▼
Future experiments    SNSAI
                        │
                        ▼
                  Social platforms
                        │
                        ▼
                Performance metrics
                        │
                        ▼
                Distribution analysis
                        │
                        └──────────────► Repository Memory
```

## Core components

### 1. Research Planner

Responsibilities:

- inspect the previous experiment
- inspect recent experiment history
- search durable playbooks before reinventing knowledge
- gather new external information when useful
- avoid repeating the same subject too frequently
- choose a visually interesting subject
- choose only 1–2 meaningful variables to test
- state a falsifiable or at least inspectable hypothesis

### 2. Prompt Designer

Build prompts from explicit dimensions such as:

- subject
- concept
- composition
- camera / lens language
- lighting
- color design
- materials / texture
- environment
- depth
- emotion
- art direction
- typography
- micro-details
- output purpose
- constraints
- avoid / failure controls

Prompt detail should be purposeful. More words are not automatically better.

### 3. Image Generator

The generator should store enough metadata to reconstruct the experiment later, including model, prompt, dimensions, quality settings, reference inputs when applicable, and generation timestamp.

### 4. Visual Critic

The critic must not judge only whether the image is attractive.

It should distinguish:

- objective instruction failures
- visible artifacts
- visual craft
- subject / concept strength
- professional usability
- uncertainty

### 5. Learning Writer

The Learning Writer converts one experiment into:

- observed evidence
- candidate principle
- confidence level
- possible confounds
- next experiment

It must avoid turning one lucky result into a universal rule.

### 6. Repository Memory

Memory has two layers:

#### Raw experimental memory

Every experiment remains available as evidence.

#### Compressed durable memory

Repeated or strongly supported findings move into `knowledge/` playbooks.

The system should prefer compressed knowledge during normal runs, then inspect raw experiments only when needed.

## SNSAI boundary

GPT-Image-Lab and SNSAI should remain separate systems.

GPT-Image-Lab answers:

> How do we make stronger images and learn from image-generation experiments?

SNSAI answers:

> Which output should we publish, how should we package it, and how did the audience respond?

They exchange structured data but should not collapse into one undifferentiated score.

## note boundary

The note workflow is editorial, not the core research engine.

Once per day, an editorial step should select the most useful experiment(s) and turn them into one coherent article draft.

The daily article should tell a research story rather than dump all hourly outputs.

## Future implementation suggestion

When code is introduced, prefer modular components rather than one giant prompt/script. A possible layout:

```text
src/
├── planner/
├── research/
├── prompt_engine/
├── generation/
├── critique/
├── learning/
├── social_bridge/
├── note_draft/
└── storage/
```

This makes it easier to replace models, social connectors, or evaluation strategies without rewriting the full loop.
