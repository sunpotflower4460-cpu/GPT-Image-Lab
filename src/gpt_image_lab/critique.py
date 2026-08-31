from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from .models import (
    Confidence,
    Critique,
    ExperimentRecord,
    FATAL_FAILURE_KEYS,
    HypothesisResult,
    VISUAL_SCORE_KEYS,
)
from .storage import RepositoryMemory


DEFAULT_CRITIC_MODEL = "gpt-5.6-sol"


class CritiqueError(RuntimeError):
    """Raised when automated image critique cannot be completed safely."""


@dataclass(slots=True, frozen=True)
class CritiqueResult:
    payload: dict[str, Any]
    model: str
    provider: str = "openai"
    response_id: str | None = None


class ImageCritic(Protocol):
    def critique(self, record: ExperimentRecord, image_path: Path) -> CritiqueResult: ...


def _score_properties() -> dict[str, dict[str, Any]]:
    return {
        key: {"type": "number", "minimum": 1, "maximum": 10}
        for key in VISUAL_SCORE_KEYS
    }


def _evidence_properties() -> dict[str, dict[str, Any]]:
    return {key: {"type": "string", "minLength": 1} for key in VISUAL_SCORE_KEYS}


def _fatal_properties() -> dict[str, dict[str, Any]]:
    return {key: {"type": "boolean"} for key in FATAL_FAILURE_KEYS}


CRITIQUE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "visual_scores",
        "evidence",
        "fatal_failures",
        "hypothesis_metric_score",
        "hypothesis_metric_evidence",
        "viewpoints",
        "hypothesis_result",
        "hypothesis_result_reason",
        "confounds",
        "candidate_learning",
        "confidence",
        "learning_scope",
        "learning_limits",
        "next_hypothesis",
    ],
    "properties": {
        "visual_scores": {
            "type": "object",
            "additionalProperties": False,
            "required": list(VISUAL_SCORE_KEYS),
            "properties": _score_properties(),
        },
        "evidence": {
            "type": "object",
            "additionalProperties": False,
            "required": list(VISUAL_SCORE_KEYS),
            "properties": _evidence_properties(),
        },
        "fatal_failures": {
            "type": "object",
            "additionalProperties": False,
            "required": list(FATAL_FAILURE_KEYS),
            "properties": _fatal_properties(),
        },
        "hypothesis_metric_score": {"type": "number", "minimum": 1, "maximum": 10},
        "hypothesis_metric_evidence": {"type": "string", "minLength": 1},
        "viewpoints": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "visual_craft",
                "prompt_adherence",
                "commercial_social_usability",
            ],
            "properties": {
                "visual_craft": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "prompt_adherence": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "commercial_social_usability": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        "hypothesis_result": {
            "type": "string",
            "enum": [item.value for item in HypothesisResult],
        },
        "hypothesis_result_reason": {"type": "string", "minLength": 1},
        "confounds": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "candidate_learning": {"type": "string", "minLength": 1},
        "confidence": {"type": "string", "enum": [item.value for item in Confidence]},
        "learning_scope": {"type": "string", "minLength": 1},
        "learning_limits": {"type": "string", "minLength": 1},
        "next_hypothesis": {"type": "string", "minLength": 1},
    },
}


RUBRIC_SUMMARY = """
Score each category from 1 to 10 using visible evidence only:
- composition: hierarchy, framing, balance, negative space
- lighting: coherent sources, highlights, shadows, reflections, intended mood
- color_design: palette coherence, contrast, hierarchy, emotional support
- materials_texture: plausible material distinction; avoid plastic/noisy/over-sharpened surfaces
- depth_spatial_coherence: perspective, scale, foreground/background separation, depth of field
- instruction_adherence: requested subject, layout, mood, constraints and exclusions
- artifact_control: anatomy/geometry/text/reflection/edge artifacts; 10 means few meaningful artifacts
- originality_concept_clarity: distinctive idea and clear concept rather than generic AI imagery
- professional_finish: art direction and real commercial/editorial usability
- social_stopping_power: visual first-read focal point and scroll-stopping clarity, not actual engagement data
""".strip()


class OpenAIImageCritic:
    def __init__(self, client: Any | None = None, model: str = DEFAULT_CRITIC_MODEL) -> None:
        self._client = client
        self.model = model

    def _client_or_create(self) -> Any:
        if self._client is not None:
            return self._client
        if not os.environ.get("OPENAI_API_KEY"):
            raise CritiqueError("OPENAI_API_KEY is not configured.")
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise CritiqueError("The 'openai' package is required for automated critique.") from exc
        self._client = OpenAI()
        return self._client

    def critique(self, record: ExperimentRecord, image_path: Path) -> CritiqueResult:
        if not image_path.exists():
            raise CritiqueError(f"Generated image does not exist: {image_path}")
        image_bytes = image_path.read_bytes()
        if not image_bytes:
            raise CritiqueError("Generated image is empty.")

        data_url = "data:image/png;base64," + base64.b64encode(image_bytes).decode("ascii")
        context = f"""
Experiment ID: {record.experiment_id}
Subject: {record.subject}
Investigation: {record.investigation}
Hypothesis: {record.hypothesis}
Primary variables: {', '.join(record.primary_variables)}
Held stable: {', '.join(record.held_stable)}
Expected benefit: {record.expected_benefit}
Possible downside: {record.possible_downside}
Prompt used:
{record.prompt}

Hypothesis-specific metric name: {record.critique.hypothesis_metric_name}

{RUBRIC_SUMMARY}

Judge the image itself, not the intention. Be demanding and evidence-driven. Do not reward prompt length.
Do not infer that an attractive image proves the hypothesis. Separate visible quality from causal claims.
A single bootstrap sample normally warrants low or medium confidence, not high confidence.
The next hypothesis must be a concrete follow-up that changes no more than two primary variables.
""".strip()

        client = self._client_or_create()
        try:
            response = client.responses.create(
                model=self.model,
                reasoning={"effort": "high"},
                instructions=(
                    "You are the independent visual critic for GPT-Image-Lab. "
                    "Return only the requested structured evaluation. Be strict, specific, "
                    "and willing to score below average when visible evidence warrants it."
                ),
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": context},
                            {
                                "type": "input_image",
                                "image_url": data_url,
                                "detail": "original",
                            },
                        ],
                    }
                ],
                text={
                    "verbosity": "low",
                    "format": {
                        "type": "json_schema",
                        "name": "gpt_image_lab_critique",
                        "strict": True,
                        "schema": CRITIQUE_SCHEMA,
                    },
                },
            )
        except Exception as exc:
            raise CritiqueError(f"OpenAI image critique failed: {exc}") from exc

        output_text = getattr(response, "output_text", None)
        if not output_text:
            raise CritiqueError("OpenAI returned no structured critique text.")
        try:
            payload = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise CritiqueError("OpenAI returned invalid critique JSON.") from exc

        _validate_payload(payload)
        return CritiqueResult(
            payload=payload,
            model=self.model,
            response_id=getattr(response, "id", None),
        )


def _validate_payload(payload: dict[str, Any]) -> None:
    missing_scores = [key for key in VISUAL_SCORE_KEYS if key not in payload.get("visual_scores", {})]
    missing_evidence = [key for key in VISUAL_SCORE_KEYS if not payload.get("evidence", {}).get(key)]
    missing_fatal = [key for key in FATAL_FAILURE_KEYS if key not in payload.get("fatal_failures", {})]
    if missing_scores or missing_evidence or missing_fatal:
        raise CritiqueError("Critique payload is missing required rubric fields.")
    if payload.get("hypothesis_result") not in {item.value for item in HypothesisResult}:
        raise CritiqueError("Critique payload contains an invalid hypothesis result.")
    if payload.get("confidence") not in {item.value for item in Confidence}:
        raise CritiqueError("Critique payload contains an invalid confidence value.")


def apply_critique_payload(record: ExperimentRecord, payload: dict[str, Any]) -> None:
    _validate_payload(payload)
    record.critique = Critique(
        visual_scores={key: float(payload["visual_scores"][key]) for key in VISUAL_SCORE_KEYS},
        evidence={key: str(payload["evidence"][key]) for key in VISUAL_SCORE_KEYS},
        fatal_failures={key: bool(payload["fatal_failures"][key]) for key in FATAL_FAILURE_KEYS},
        hypothesis_metric_name=record.critique.hypothesis_metric_name,
        hypothesis_metric_score=float(payload["hypothesis_metric_score"]),
        hypothesis_metric_evidence=str(payload["hypothesis_metric_evidence"]),
        viewpoints={
            "visual_craft": list(payload["viewpoints"]["visual_craft"]),
            "prompt_adherence": list(payload["viewpoints"]["prompt_adherence"]),
            "commercial_social_usability": list(
                payload["viewpoints"]["commercial_social_usability"]
            ),
        },
    )
    record.hypothesis_result = str(payload["hypothesis_result"])
    record.hypothesis_result_reason = str(payload["hypothesis_result_reason"])
    record.confounds = list(payload["confounds"])
    record.candidate_learning = str(payload["candidate_learning"])
    record.confidence = str(payload["confidence"])
    record.learning_scope = str(payload["learning_scope"])
    record.learning_limits = str(payload["learning_limits"])
    record.next_hypothesis = str(payload["next_hypothesis"])


def critique_experiment(
    memory: RepositoryMemory,
    experiment_id: str,
    critic: ImageCritic,
    *,
    overwrite: bool = False,
) -> Path:
    record = memory.load(experiment_id)
    if record.finalized_at:
        raise CritiqueError(f"Experiment {experiment_id} is finalized and cannot be re-critiqued.")
    if record.critique.visual_scores and not overwrite:
        raise CritiqueError(
            "Critique already exists. Use --overwrite only for an intentional pre-finalize re-review."
        )

    experiment_dir = memory.experiment_path(experiment_id).resolve()
    image_path = (experiment_dir / record.output_reference).resolve()
    try:
        image_path.relative_to(experiment_dir)
    except ValueError as exc:
        raise CritiqueError("output_reference must stay inside the experiment directory.") from exc
    if not record.generation.generated_at:
        raise CritiqueError("Experiment has no successful generation timestamp.")

    result = critic.critique(record, image_path)
    apply_critique_payload(record, result.payload)
    memory.save(record)

    metadata_path = experiment_dir / "critique-metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "experiment_id": experiment_id,
                "provider": result.provider,
                "model": result.model,
                "response_id": result.response_id,
                "critiqued_at": datetime.now(timezone.utc).isoformat(),
                "visual_average": record.critique.visual_average,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return metadata_path
