from __future__ import annotations

from pathlib import Path

import pytest

from gpt_image_lab.critique import CritiqueResult
from gpt_image_lab.generation import GenerationRequest, GenerationResult
from gpt_image_lab.models import (
    ExperimentRecord,
    FATAL_FAILURE_KEYS,
    GenerationMetadata,
    ResearchNote,
    VISUAL_SCORE_KEYS,
)
from gpt_image_lab.runner import RunnerError, inspect_prepared_experiment, run_prepared_experiment
from gpt_image_lab.storage import RepositoryMemory


class FakeGenerator:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.calls += 1
        return GenerationResult(image_bytes=b"image", provider="fake")


class FakeCritic:
    def __init__(self) -> None:
        self.calls = 0

    def critique(self, record: ExperimentRecord, image_path: Path) -> CritiqueResult:
        self.calls += 1
        payload = {
            "visual_scores": {key: 8 for key in VISUAL_SCORE_KEYS},
            "evidence": {key: f"Evidence for {key}." for key in VISUAL_SCORE_KEYS},
            "fatal_failures": {key: False for key in FATAL_FAILURE_KEYS},
            "hypothesis_metric_score": 8,
            "hypothesis_metric_evidence": "The intended lighting structure is visible.",
            "viewpoints": {
                "visual_craft": ["The composition and light hierarchy are controlled."],
                "prompt_adherence": ["The requested subject and lighting roles are visible."],
                "commercial_social_usability": ["The image is usable for a product-study post."],
            },
            "hypothesis_result": "partially_supported",
            "hypothesis_result_reason": "The output meets the baseline but there is no control comparison yet.",
            "confounds": ["Single sample."],
            "candidate_learning": "Functional lighting-role language is a viable baseline for this subject.",
            "confidence": "medium",
            "learning_scope": "Controlled studio product imagery.",
            "learning_limits": "No generic-lighting control has been tested yet.",
            "next_hypothesis": "Compare the same subject with generic cinematic-lighting wording while holding everything else stable.",
        }
        return CritiqueResult(payload=payload, model="fake-critic", provider="fake")


def prepared_record() -> ExperimentRecord:
    record = ExperimentRecord(
        experiment_id="0001",
        bootstrap_experiment=True,
        subject="Clear glass fragrance bottle",
        investigation="Test functional lighting roles.",
        why_it_matters="Create the first measured professional-lighting baseline.",
        relevant_prior_findings=["Bootstrap baseline; no prior experiment exists."],
        unresolved_question="Can role-based lighting create a coherent baseline?",
        research=ResearchNote(
            learned=["Three-point lighting assigns different functions to key, fill, and rim lights."],
            relevance="The roles can be inspected visually.",
            uncertainty=["Language does not guarantee physical ratios."],
            sources=["research source"],
        ),
        hypothesis="Functional key/fill/rim descriptions will create coherent product lighting.",
        primary_variables=["functional lighting-role language"],
        held_stable=["subject", "composition", "palette"],
        expected_benefit="Clear subject separation.",
        possible_downside="Artificial rim halo.",
        prompt="A premium clear-glass product photograph with explicit key, fill and rim roles.",
        prompt_rationale="Lighting wording is the only main variable.",
        output_reference="assets/result.png",
        generation=GenerationMetadata(
            model="gpt-image-2-2026-04-21",
            width=1024,
            height=1536,
            quality="high",
        ),
    )
    record.critique.hypothesis_metric_name = "lighting coherence and subject separation"
    return record


def test_runner_advances_to_review_without_finalizing(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    memory.create_draft(prepared_record())
    generator = FakeGenerator()
    critic = FakeCritic()

    result = run_prepared_experiment(memory, "0001", generator, critic)

    assert generator.calls == 1
    assert critic.calls == 1
    assert result.generated is True
    assert result.critiqued is True
    assert result.review_path.exists()
    saved = memory.load("0001")
    assert saved.finalized_at == ""
    assert saved.critique.visual_average == 8.0
    assert saved.next_hypothesis
    assert not (tmp_path / "knowledge" / "LEARNINGS.md").exists()


def test_runner_is_resumable_after_generation_and_critique(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    memory.create_draft(prepared_record())
    generator = FakeGenerator()
    critic = FakeCritic()

    run_prepared_experiment(memory, "0001", generator, critic)
    second_generator = FakeGenerator()
    second_critic = FakeCritic()
    result = run_prepared_experiment(memory, "0001", second_generator, second_critic)

    assert second_generator.calls == 0
    assert second_critic.calls == 0
    assert result.generated is False
    assert result.critiqued is False
    assert result.review_path.exists()


def test_runner_refuses_timestamp_without_image(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = prepared_record()
    record.generation.generated_at = "2026-08-31T00:00:00+00:00"
    memory.create_draft(record)

    with pytest.raises(RunnerError, match="result image is missing"):
        run_prepared_experiment(memory, "0001", FakeGenerator(), FakeCritic())


def test_inspect_prepared_experiment_catches_missing_hypothesis(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = prepared_record()
    record.hypothesis = ""
    memory.create_draft(record)

    problems = inspect_prepared_experiment(memory, "0001")
    assert any("hypothesis" in item for item in problems)


def test_runner_refuses_to_start_when_planning_is_incomplete(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = prepared_record()
    record.held_stable = []
    memory.create_draft(record)

    with pytest.raises(RunnerError, match="held_stable"):
        run_prepared_experiment(memory, "0001", FakeGenerator(), FakeCritic())
