from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .critique import ImageCritic, critique_experiment
from .generation import ImageGenerator, generate_experiment
from .storage import RepositoryMemory


class RunnerError(RuntimeError):
    """Raised when a prepared Phase 1 experiment cannot reach human review."""


@dataclass(slots=True, frozen=True)
class RunResult:
    experiment_id: str
    generated: bool
    critiqued: bool
    review_path: Path


def _existing_output(memory: RepositoryMemory, experiment_id: str) -> Path:
    record = memory.load(experiment_id)
    experiment_dir = memory.experiment_path(experiment_id).resolve()
    path = (experiment_dir / record.output_reference).resolve()
    try:
        path.relative_to(experiment_dir)
    except ValueError as exc:
        raise RunnerError("output_reference must stay inside the experiment directory.") from exc
    return path


def inspect_prepared_experiment(memory: RepositoryMemory, experiment_id: str) -> list[str]:
    """Return pre-generation planning problems without requiring critique fields yet."""
    record = memory.load(experiment_id)
    problems: list[str] = []

    if record.finalized_at:
        problems.append("experiment is already finalized")

    required_text = {
        "subject": record.subject,
        "investigation": record.investigation,
        "why_it_matters": record.why_it_matters,
        "hypothesis": record.hypothesis,
        "expected_benefit": record.expected_benefit,
        "possible_downside": record.possible_downside,
        "prompt": record.prompt,
        "prompt_rationale": record.prompt_rationale,
        "output_reference": record.output_reference,
        "hypothesis_metric_name": record.critique.hypothesis_metric_name,
        "generation.model": record.generation.model,
        "generation.quality": record.generation.quality,
    }
    for name, value in required_text.items():
        if not str(value).strip():
            problems.append(f"missing prepared field: {name}")

    if not 1 <= len(record.primary_variables) <= 2:
        problems.append("primary_variables must contain 1 or 2 variables")
    if not record.held_stable:
        problems.append("held_stable should identify controlled conditions")
    if not record.research.learned and not record.research.relevance.strip():
        problems.append("research evidence or a no-new-research rationale is required")
    if not record.generation.width or not record.generation.height:
        problems.append("generation width and height are required")

    if not record.bootstrap_experiment:
        if not record.reflection.worked:
            problems.append("reflection.worked is required for a standard experiment")
        if not record.reflection.failed:
            problems.append("reflection.failed is required for a standard experiment")
        if not record.reflection.uncertain:
            problems.append("reflection.uncertain is required for a standard experiment")

    return problems


def run_prepared_experiment(
    memory: RepositoryMemory,
    experiment_id: str,
    generator: ImageGenerator,
    critic: ImageCritic,
) -> RunResult:
    """Advance a planned Phase 1 experiment to the human-review gate.

    This deliberately does not finalize the experiment or append durable learning.
    It is resumable: successful generation and critique stages are skipped when
    their artifacts already exist.
    """
    problems = inspect_prepared_experiment(memory, experiment_id)
    if problems:
        raise RunnerError("Experiment is not ready to run:\n- " + "\n- ".join(problems))

    record = memory.load(experiment_id)
    output_path = _existing_output(memory, experiment_id)

    generated_now = False
    if record.generation.generated_at:
        if not output_path.exists():
            raise RunnerError(
                "generation timestamp exists but the result image is missing; repair the experiment before continuing"
            )
    else:
        generate_experiment(memory, experiment_id, generator)
        generated_now = True

    record = memory.load(experiment_id)
    critiqued_now = False
    if not record.critique.visual_scores:
        critique_experiment(memory, experiment_id, critic)
        critiqued_now = True

    record = memory.load(experiment_id)
    validation_errors = record.validate()
    if validation_errors:
        raise RunnerError(
            "Experiment reached critique but does not pass the completion gate:\n- "
            + "\n- ".join(validation_errors)
        )

    review_path = memory.experiment_path(experiment_id) / "REVIEW.md"
    review_path.write_text(
        "# Pre-finalization human review\n\n"
        "This packet is generated after image generation, structured AI critique, and validation.\n"
        "Review the image and evidence before running `gpt-image-lab finalize "
        f"{experiment_id}`.\n\n"
        + memory.render_report(record),
        encoding="utf-8",
    )

    return RunResult(
        experiment_id=experiment_id,
        generated=generated_now,
        critiqued=critiqued_now,
        review_path=review_path,
    )
