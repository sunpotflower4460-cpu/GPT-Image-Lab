from pathlib import Path

import pytest

from gpt_image_lab.models import Critique, ExperimentRecord, Reflection, ResearchNote, VISUAL_SCORE_KEYS
from gpt_image_lab.storage import RepositoryMemory


def complete_record(experiment_id: str = "0001") -> ExperimentRecord:
    scores = {key: 8.0 for key in VISUAL_SCORE_KEYS}
    evidence = {key: f"Evidence for {key}." for key in VISUAL_SCORE_KEYS}
    return ExperimentRecord(
        experiment_id=experiment_id,
        subject="Premium glass product photograph",
        investigation="Whether functional light-role language improves subject separation.",
        why_it_matters="Lighting language is common in commercial prompts and should be tested rather than assumed.",
        relevant_prior_findings=["Generic cinematic-lighting language is hard to diagnose."],
        unresolved_question="Does explicit key/fill/rim role language improve separation without halos?",
        reflection=Reflection(
            worked=["The previous composition had a clear focal point."],
            failed=["The edge light looked synthetic."],
            uncertain=["It is unclear whether the artifact came from light-role wording or material wording."],
        ),
        research=ResearchNote(
            learned=["Lighting roles describe function rather than only mood."],
            relevance="This gives the experiment a controlled language change to inspect.",
            uncertainty=["Prompt language may not map consistently to physical ratios."],
            sources=["internal research note"],
        ),
        hypothesis="Specifying key, fill, and rim light by function will improve subject separation without increasing halos.",
        primary_variables=["functional lighting-role language"],
        held_stable=["subject", "composition", "palette"],
        expected_benefit="Cleaner separation and more deliberate commercial lighting.",
        possible_downside="The model may exaggerate the rim light.",
        prompt="A controlled premium product photograph with explicit key, fill, and rim light roles.",
        prompt_rationale="Only the lighting description is the main experimental change.",
        output_reference="assets/result.png",
        critique=Critique(
            visual_scores=scores,
            evidence=evidence,
            fatal_failures={},
            hypothesis_metric_name="subject/background separation",
            hypothesis_metric_score=8.0,
            hypothesis_metric_evidence="The subject edge remains readable without a strong visible halo.",
            viewpoints={
                "visual_craft": ["Lighting hierarchy is coherent."],
                "prompt_adherence": ["The requested light roles are visibly differentiated."],
                "commercial_social_usability": ["The image is usable as a premium-ad study."],
            },
        ),
        hypothesis_result="partially_supported",
        hypothesis_result_reason="Separation improved, but a second controlled repeat is needed.",
        confounds=["Single generated sample."],
        candidate_learning="Functional lighting-role language may improve controllability more than a generic cinematic-lighting adjective.",
        confidence="medium",
        learning_scope="Studio-style product imagery.",
        learning_limits="Not yet tested on portraits or wide scenes.",
        promote_to_playbook=False,
        next_hypothesis="Repeat the same lighting-role experiment on a portrait while holding the palette and framing stable.",
    )


def test_ids_increment_and_latest_is_loaded(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    assert memory.next_experiment_id() == "0001"

    first = ExperimentRecord(experiment_id="0001", subject="first")
    memory.create_draft(first)
    assert memory.next_experiment_id() == "0002"
    assert memory.latest().experiment_id == "0001"


def test_incomplete_experiment_fails_validation() -> None:
    record = ExperimentRecord(experiment_id="0001")
    errors = record.validate()
    assert errors
    assert any("hypothesis" in error for error in errors)
    assert any("visual scores" in error for error in errors)


def test_finalize_writes_report_and_candidate_learning(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = complete_record()
    memory.create_draft(record)

    experiment_path = memory.finalize(record)

    assert (experiment_path / "REPORT.md").exists()
    reloaded = memory.load("0001")
    assert reloaded.finalized_at
    assert reloaded.critique.visual_average == 8.0

    learnings = (tmp_path / "knowledge" / "LEARNINGS.md").read_text(encoding="utf-8")
    assert "Experiment 0001" in learnings
    assert record.candidate_learning in learnings


def test_finalize_never_auto_promotes_playbook(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    playbook = tmp_path / "knowledge" / "PROMPT_PLAYBOOK.md"
    playbook.parent.mkdir(parents=True, exist_ok=True)
    playbook.write_text("# Durable Playbook\n", encoding="utf-8")

    record = complete_record()
    record.promote_to_playbook = True
    memory.create_draft(record)
    memory.finalize(record)

    assert playbook.read_text(encoding="utf-8") == "# Durable Playbook\n"


def test_primary_variables_are_limited_to_two() -> None:
    record = complete_record()
    record.primary_variables = ["a", "b", "c"]
    errors = record.validate()
    assert any("1 or 2 variables" in error for error in errors)
