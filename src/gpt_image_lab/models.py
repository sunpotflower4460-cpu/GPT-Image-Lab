from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


VISUAL_SCORE_KEYS = (
    "composition",
    "lighting",
    "color_design",
    "materials_texture",
    "depth_spatial_coherence",
    "instruction_adherence",
    "artifact_control",
    "originality_concept_clarity",
    "professional_finish",
    "social_stopping_power",
)

FATAL_FAILURE_KEYS = (
    "anatomy_failure",
    "text_failure",
    "identity_character_inconsistency",
    "broken_object_geometry",
    "impossible_reflection_lighting_failure",
    "obvious_generation_artifact",
    "wrong_aspect_layout",
    "copyright_brand_risk",
    "safety_policy_concern",
    "unusable_crop",
)


class HypothesisResult(str, Enum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    NOT_SUPPORTED = "not_supported"
    INCONCLUSIVE = "inconclusive"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class Reflection:
    worked: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    uncertain: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ResearchNote:
    learned: list[str] = field(default_factory=list)
    relevance: str = ""
    uncertainty: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GenerationMetadata:
    model: str = ""
    generated_at: str = ""
    prompt_version: str = "v1"
    width: int | None = None
    height: int | None = None
    quality: str = ""
    reference_images: list[str] = field(default_factory=list)
    seed: str | None = None
    cost: float | None = None

    def ensure_timestamp(self) -> None:
        if not self.generated_at:
            self.generated_at = datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Critique:
    visual_scores: dict[str, float] = field(default_factory=dict)
    evidence: dict[str, str] = field(default_factory=dict)
    fatal_failures: dict[str, bool] = field(default_factory=dict)
    hypothesis_metric_name: str = ""
    hypothesis_metric_score: float | None = None
    hypothesis_metric_evidence: str = ""
    viewpoints: dict[str, list[str]] = field(default_factory=dict)

    @property
    def visual_average(self) -> float | None:
        values = [self.visual_scores[key] for key in VISUAL_SCORE_KEYS if key in self.visual_scores]
        if len(values) != len(VISUAL_SCORE_KEYS):
            return None
        return round(sum(values) / len(values), 2)


@dataclass(slots=True)
class ExperimentRecord:
    experiment_id: str
    bootstrap_experiment: bool = False
    subject: str = ""
    investigation: str = ""
    why_it_matters: str = ""
    relevant_prior_findings: list[str] = field(default_factory=list)
    unresolved_question: str = ""
    reflection: Reflection = field(default_factory=Reflection)
    research: ResearchNote = field(default_factory=ResearchNote)
    hypothesis: str = ""
    primary_variables: list[str] = field(default_factory=list)
    held_stable: list[str] = field(default_factory=list)
    expected_benefit: str = ""
    possible_downside: str = ""
    prompt: str = ""
    prompt_rationale: str = ""
    output_reference: str = ""
    generation: GenerationMetadata = field(default_factory=GenerationMetadata)
    critique: Critique = field(default_factory=Critique)
    hypothesis_result: str = ""
    hypothesis_result_reason: str = ""
    confounds: list[str] = field(default_factory=list)
    candidate_learning: str = ""
    confidence: str = ""
    learning_scope: str = ""
    learning_limits: str = ""
    promote_to_playbook: bool = False
    next_hypothesis: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finalized_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["visual_average"] = self.critique.visual_average
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExperimentRecord":
        data = dict(data)
        data.pop("visual_average", None)
        data["reflection"] = Reflection(**data.get("reflection", {}))
        data["research"] = ResearchNote(**data.get("research", {}))
        data["generation"] = GenerationMetadata(**data.get("generation", {}))
        data["critique"] = Critique(**data.get("critique", {}))
        return cls(**data)

    def validate(self) -> list[str]:
        errors: list[str] = []

        required_text = {
            "subject": self.subject,
            "investigation": self.investigation,
            "why_it_matters": self.why_it_matters,
            "hypothesis": self.hypothesis,
            "prompt": self.prompt,
            "prompt_rationale": self.prompt_rationale,
            "output_reference": self.output_reference,
            "hypothesis_result": self.hypothesis_result,
            "hypothesis_result_reason": self.hypothesis_result_reason,
            "candidate_learning": self.candidate_learning,
            "confidence": self.confidence,
            "next_hypothesis": self.next_hypothesis,
        }
        for name, value in required_text.items():
            if not str(value).strip():
                errors.append(f"missing required field: {name}")

        if self.bootstrap_experiment:
            if self.experiment_id != "0001":
                errors.append("bootstrap_experiment is only allowed for Experiment 0001")
        else:
            if not self.reflection.worked:
                errors.append("reflection.worked must contain at least one observation")
            if not self.reflection.failed:
                errors.append("reflection.failed must contain at least one observation")
            if not self.reflection.uncertain:
                errors.append("reflection.uncertain must contain at least one observation")

        if not self.research.learned and not self.research.relevance.strip():
            errors.append("research must contain learned items or an explicit relevance/no-new-research note")

        if not 1 <= len(self.primary_variables) <= 2:
            errors.append("primary_variables must contain 1 or 2 variables")

        if self.hypothesis_result not in {item.value for item in HypothesisResult}:
            errors.append("hypothesis_result must be supported, partially_supported, not_supported, or inconclusive")

        if self.confidence not in {item.value for item in Confidence}:
            errors.append("confidence must be low, medium, or high")

        missing_scores = [key for key in VISUAL_SCORE_KEYS if key not in self.critique.visual_scores]
        if missing_scores:
            errors.append("missing visual scores: " + ", ".join(missing_scores))
        for key, score in self.critique.visual_scores.items():
            if key in VISUAL_SCORE_KEYS and not 1 <= float(score) <= 10:
                errors.append(f"visual score {key} must be between 1 and 10")

        missing_evidence = [key for key in VISUAL_SCORE_KEYS if not self.critique.evidence.get(key, "").strip()]
        if missing_evidence:
            errors.append("missing score evidence: " + ", ".join(missing_evidence))

        if not self.critique.hypothesis_metric_name.strip():
            errors.append("critique.hypothesis_metric_name is required")
        if self.critique.hypothesis_metric_score is None:
            errors.append("critique.hypothesis_metric_score is required")
        elif not 1 <= float(self.critique.hypothesis_metric_score) <= 10:
            errors.append("critique.hypothesis_metric_score must be between 1 and 10")
        if not self.critique.hypothesis_metric_evidence.strip():
            errors.append("critique.hypothesis_metric_evidence is required")

        expected_viewpoints = {"visual_craft", "prompt_adherence", "commercial_social_usability"}
        missing_viewpoints = [key for key in expected_viewpoints if not self.critique.viewpoints.get(key)]
        if missing_viewpoints:
            errors.append("missing critique viewpoints: " + ", ".join(sorted(missing_viewpoints)))

        for key in FATAL_FAILURE_KEYS:
            self.critique.fatal_failures.setdefault(key, False)

        return errors
