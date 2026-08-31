from __future__ import annotations

import json
from pathlib import Path

import pytest

from gpt_image_lab.generation import (
    GenerationError,
    GenerationRequest,
    GenerationResult,
    build_generation_request,
    generate_experiment,
)
from gpt_image_lab.models import ExperimentRecord, GenerationMetadata
from gpt_image_lab.storage import RepositoryMemory


class FakeGenerator:
    def __init__(self, image_bytes: bytes = b"fake-png-bytes") -> None:
        self.image_bytes = image_bytes
        self.requests: list[GenerationRequest] = []

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.requests.append(request)
        return GenerationResult(image_bytes=self.image_bytes, provider="fake")


def draft_record(experiment_id: str = "0001") -> ExperimentRecord:
    return ExperimentRecord(
        experiment_id=experiment_id,
        bootstrap_experiment=experiment_id == "0001",
        subject="Clear glass fragrance bottle",
        prompt="A controlled studio photograph of a clear glass fragrance bottle.",
        output_reference="assets/result.png",
        generation=GenerationMetadata(
            model="gpt-image-2",
            width=1024,
            height=1536,
            quality="high",
        ),
    )


def test_build_generation_request_uses_record_settings() -> None:
    request = build_generation_request(draft_record())
    assert request.model == "gpt-image-2"
    assert request.size == "1024x1536"
    assert request.quality == "high"


def test_generate_experiment_writes_image_metadata_and_timestamp(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = draft_record()
    memory.create_draft(record)
    generator = FakeGenerator(b"image-content")

    output = generate_experiment(memory, "0001", generator)

    assert output.read_bytes() == b"image-content"
    assert len(generator.requests) == 1
    saved = memory.load("0001")
    assert saved.generation.generated_at

    metadata = json.loads(
        (tmp_path / "experiments" / "0001" / "result-metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["provider"] == "fake"
    assert metadata["model"] == "gpt-image-2"
    assert metadata["size"] == "1024x1536"
    assert metadata["quality"] == "high"
    assert metadata["bytes"] == len(b"image-content")
    assert len(metadata["sha256"]) == 64


def test_existing_result_is_not_overwritten_by_default(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    memory.create_draft(draft_record())
    output = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    output.write_bytes(b"original")

    with pytest.raises(GenerationError, match="Output already exists"):
        generate_experiment(memory, "0001", FakeGenerator(b"replacement"))

    assert output.read_bytes() == b"original"


def test_explicit_overwrite_is_allowed_before_finalize(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    memory.create_draft(draft_record())
    output = tmp_path / "experiments" / "0001" / "assets" / "result.png"
    output.write_bytes(b"original")

    generate_experiment(
        memory,
        "0001",
        FakeGenerator(b"replacement"),
        overwrite=True,
    )

    assert output.read_bytes() == b"replacement"


def test_finalized_experiment_cannot_generate(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = draft_record()
    record.finalized_at = "2026-08-31T00:00:00+00:00"
    memory.create_draft(record)

    with pytest.raises(GenerationError, match="finalized"):
        generate_experiment(memory, "0001", FakeGenerator())


def test_output_reference_cannot_escape_experiment_directory(tmp_path: Path) -> None:
    memory = RepositoryMemory(tmp_path)
    record = draft_record()
    record.output_reference = "../../escape.png"
    memory.create_draft(record)

    with pytest.raises(GenerationError, match="inside the experiment directory"):
        generate_experiment(memory, "0001", FakeGenerator())


def test_generation_requires_supported_quality() -> None:
    record = draft_record()
    record.generation.quality = "ultra"
    with pytest.raises(GenerationError, match="quality"):
        build_generation_request(record)
