from __future__ import annotations

import json
from pathlib import Path

import pytest

from gpt_image_lab.critique import CritiqueError, CritiqueResult, critique_experiment
from gpt_image_lab.models import (
    ExperimentRecord,
    FATAL_FAILURE_KEYS,
    GenerationMetadata,
    VISUAL_SCORE_KEYS,
)
from gpt_image_lab.storage import RepositoryMemory


class FakeCritic:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.calls = 0

    def critique(self, record: ExperimentRecord, image_path: Path) -> CritiqueResult:
        self.calls += 1
        assert image_path.exists()
        return CritiqueResult(
            payload=self.payload,
            model="fake-critic",
            provider="fake",
            response_id="resp_test",
        )


def payload() -> dict:
    return {
        "visual_scores": {key: 8 for key in VISUAL_SCORE_KEYS},
        "evidence": {key: f"Evidence for {key}." for key in VISUAL_SCORE_KEYS},
        "fatal_failures": {key: False for key in FATAL_FAILURE_KEYS},
        "hypothesis_metric_score": 8,
        "hypothesis_metric_evidence": "Lighting roles are visible without a strong halo.",
        "viewpoints": {
            "visual_craft": ["The light hierarchy is legible."],
            "prompt_adherence": ["The requested studio setup is substantially followed."],
            "commercial_social_usability": ["The image is usable as a product-study asset."],
        },
        "hypothesis_result": "partially_supported",
        "hypothesis_result_reason": "The baseline is strong but a single sample cannot isolate causality.",
        "confounds": ["Single generated sample."],
        "candidate_learning": "Functional lighting-role language appears usable for controlled glass-product prompting.",
        "confidence": "medium",
        "learning_scope": "Studio product imagery with reflective materials.",
        "learning_limits": "Not yet compared against a generic-lighting control.",
        "next_hypothesis": "Compare the same subject with generic cinematic-lighting language while holding all other prompt dimensions stable.",
    }


def generated_record() -> ExperimentRecord:
    record = ExperimentRecord(
        experiment_id="0001",
        bootstrap_experiment=True,
        subject="Clear glass bottle",
        investigation="Test functional light roles.",
        why_it_matters="Establish a measured lighting baseline.",
        hypothesis="Functional key/fill/rim roles create coherent product lighting.",
        primary_variables=["functional lighting-role language"],
        held_stable=["subject", "composition"],
        expected_benefit="Coherent separation.",
        possible_downside="Rim halo.",
        prompt="Create a premium clear-glass product photograph with functional key, fill and rim lights.",
        prompt_rationale="Lighting language is the controlled variable.",
        output_reference="assets/result.png",
        generation=GenerationMetadata(
            model="gpt-image-2-2026-04-21",
            generated_at="2026-08-31T00:00:00+00:00",
            width=1024,
            height=1536,
            quality="high",
        ),
    )
    record.critique.hypothesis_metric_name = "lighting coherence and subject separation"
    return record


def test_critique_experiment_applies_payload_and_writes_metadata(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = generated_record()
    memory.create_draft(record)
    image = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    image.write_bytes(b"fake-image")
    critic = FakeCritic(payload())

    metadata_path = critique_experiment(memory, "0001", critic)

    assert critic.calls == 1
    saved = memory.load("0001")
    assert saved.critique.visual_average == 8.0
    assert saved.hypothesis_result == "partially_supported"
    assert saved.confidence == "medium"
    assert "generic cinematic-lighting" in saved.next_hypothesis

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["provider"] == "fake"
    assert metadata["model"] == "fake-critic"
    assert metadata["response_id"] == "resp_test"
    assert metadata["visual_average"] == 8.0


def test_existing_critique_is_not_overwritten_by_default(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = generated_record()
    record.critique.visual_scores = {key: 7 for key in VISUAL_SCORE_KEYS}
    memory.create_draft(record)
    image = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    image.write_bytes(b"fake-image")

    with pytest.raises(CritiqueError, match="Critique already exists"):
        critique_experiment(memory, "0001", FakeCritic(payload()))


def test_explicit_critique_overwrite_is_allowed_before_finalize(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = generated_record()
    record.critique.visual_scores = {key: 7 for key in VISUAL_SCORE_KEYS}
    memory.create_draft(record)
    image = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    image.write_bytes(b"fake-image")

    critique_experiment(memory, "0001", FakeCritic(payload()), overwrite=True)
    assert memory.load("0001").critique.visual_average == 8.0


def test_critique_requires_successful_generation_timestamp(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = generated_record()
    record.generation.generated_at = ""
    memory.create_draft(record)
    image = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    image.write_bytes(b"fake-image")

    with pytest.raises(CritiqueError, match="no successful generation timestamp"):
        critique_experiment(memory, "0001", FakeCritic(payload()))


def test_finalized_experiment_cannot_be_recritiqued(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = generated_record()
    record.finalized_at = "2026-08-31T00:00:00+00:00"
    memory.create_draft(record)
    image = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    image.write_bytes(b"fake-image")

    with pytest.raises(CritiqueError, match="finalized"):
        critique_experiment(memory, "0001", FakeCritic(payload()))
