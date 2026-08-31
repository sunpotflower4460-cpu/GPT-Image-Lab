from __future__ import annotations

from pathlib import Path

from gpt_image_lab.generation import build_generation_request
from gpt_image_lab.runner import inspect_prepared_experiment
from gpt_image_lab.storage import RepositoryMemory


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_experiment_0001_is_ready_for_phase1_runner() -> None:
    memory = RepositoryMemory(REPO_ROOT)
    problems = inspect_prepared_experiment(memory, "0001")
    assert problems == []


def test_experiment_0001_generation_contract_is_pinned() -> None:
    memory = RepositoryMemory(REPO_ROOT)
    record = memory.load("0001")
    request = build_generation_request(record)

    assert request.model == "gpt-image-2-2026-04-21"
    assert request.size == "1024x1536"
    assert request.quality == "high"
    assert record.output_reference == "assets/result.png"
    assert record.bootstrap_experiment is True
