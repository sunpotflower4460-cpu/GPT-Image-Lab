from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from .models import ExperimentRecord
from .storage import RepositoryMemory


class GenerationError(RuntimeError):
    """Raised when an image generation run cannot be completed safely."""


@dataclass(slots=True, frozen=True)
class GenerationRequest:
    model: str
    prompt: str
    size: str
    quality: str


@dataclass(slots=True, frozen=True)
class GenerationResult:
    image_bytes: bytes
    provider: str = "openai"

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.image_bytes).hexdigest()


class ImageGenerator(Protocol):
    def generate(self, request: GenerationRequest) -> GenerationResult: ...


class OpenAIImageGenerator:
    """Thin adapter around the OpenAI Image API.

    The adapter intentionally keeps provider-specific behavior out of the
    experiment model so a future generator can be swapped in without changing
    the research record format.
    """

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    def _client_or_create(self) -> Any:
        if self._client is not None:
            return self._client
        if not os.environ.get("OPENAI_API_KEY"):
            raise GenerationError("OPENAI_API_KEY is not configured.")
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - packaging guard
            raise GenerationError(
                "The 'openai' package is required for OpenAI image generation."
            ) from exc
        self._client = OpenAI()
        return self._client

    def generate(self, request: GenerationRequest) -> GenerationResult:
        client = self._client_or_create()
        try:
            response = client.images.generate(
                model=request.model,
                prompt=request.prompt,
                size=request.size,
                quality=request.quality,
            )
        except Exception as exc:  # provider errors are normalized at this boundary
            raise GenerationError(f"OpenAI image generation failed: {exc}") from exc

        if not getattr(response, "data", None):
            raise GenerationError("OpenAI returned no image data.")
        image_base64 = getattr(response.data[0], "b64_json", None)
        if not image_base64:
            raise GenerationError("OpenAI returned an image item without b64_json data.")
        try:
            image_bytes = base64.b64decode(image_base64, validate=True)
        except (ValueError, TypeError) as exc:
            raise GenerationError("OpenAI returned invalid base64 image data.") from exc
        if not image_bytes:
            raise GenerationError("OpenAI returned an empty image payload.")
        return GenerationResult(image_bytes=image_bytes)


def build_generation_request(record: ExperimentRecord) -> GenerationRequest:
    if not record.prompt.strip():
        raise GenerationError("Experiment prompt is empty.")
    if not record.generation.model.strip():
        raise GenerationError("generation.model is required.")
    if not record.generation.width or not record.generation.height:
        raise GenerationError("generation width and height are required.")
    if record.generation.quality not in {"low", "medium", "high", "auto"}:
        raise GenerationError("generation.quality must be low, medium, high, or auto.")

    size = f"{record.generation.width}x{record.generation.height}"
    return GenerationRequest(
        model=record.generation.model,
        prompt=record.prompt,
        size=size,
        quality=record.generation.quality,
    )


def _safe_output_path(memory: RepositoryMemory, record: ExperimentRecord) -> Path:
    if not record.output_reference.strip():
        raise GenerationError("output_reference is required before generation.")

    experiment_dir = memory.experiment_path(record.experiment_id).resolve()
    output_path = (experiment_dir / record.output_reference).resolve()
    try:
        output_path.relative_to(experiment_dir)
    except ValueError as exc:
        raise GenerationError("output_reference must stay inside the experiment directory.") from exc
    if output_path.suffix.lower() != ".png":
        raise GenerationError("GPT-Image-Lab currently stores generated results as PNG files.")
    return output_path


def generate_experiment(
    memory: RepositoryMemory,
    experiment_id: str,
    generator: ImageGenerator,
    *,
    overwrite: bool = False,
) -> Path:
    record = memory.load(experiment_id)
    if record.finalized_at:
        raise GenerationError(
            f"Experiment {experiment_id} is finalized and cannot be regenerated."
        )

    request = build_generation_request(record)
    output_path = _safe_output_path(memory, record)
    if output_path.exists() and not overwrite:
        raise GenerationError(
            f"Output already exists: {output_path}. Use --overwrite only for an intentional pre-finalize retry."
        )

    result = generator.generate(request)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary_path.write_bytes(result.image_bytes)
    temporary_path.replace(output_path)

    generated_at = datetime.now(timezone.utc).isoformat()
    record.generation.generated_at = generated_at
    memory.save(record)

    metadata = {
        "experiment_id": record.experiment_id,
        "provider": result.provider,
        "model": request.model,
        "generated_at": generated_at,
        "prompt_version": record.generation.prompt_version,
        "size": request.size,
        "quality": request.quality,
        "output_reference": record.output_reference,
        "bytes": len(result.image_bytes),
        "sha256": result.sha256,
    }
    metadata_path = memory.experiment_path(experiment_id) / "result-metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path
