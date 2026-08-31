from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .generation import (
    GenerationError,
    OpenAIImageGenerator,
    build_generation_request,
    generate_experiment,
)
from .models import ExperimentRecord
from .storage import RepositoryMemory


def _memory(root: str) -> RepositoryMemory:
    return RepositoryMemory(Path(root))


def cmd_new(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    experiment_id = memory.next_experiment_id()
    latest = memory.latest()
    is_bootstrap = latest is None and experiment_id == "0001"

    prior_findings: list[str] = []
    unresolved_question = ""
    if latest:
        if latest.candidate_learning:
            prior_findings.append(latest.candidate_learning)
        unresolved_question = latest.next_hypothesis
    elif is_bootstrap:
        prior_findings.append(
            "No prior GPT-Image-Lab experiment exists; this bootstrap run establishes the first measured baseline."
        )

    record = ExperimentRecord(
        experiment_id=experiment_id,
        bootstrap_experiment=is_bootstrap,
        subject=args.subject or "",
        investigation=args.investigation or "",
        why_it_matters=args.why or "",
        hypothesis=args.hypothesis or (latest.next_hypothesis if latest else ""),
        primary_variables=args.variable or [],
        relevant_prior_findings=prior_findings,
        unresolved_question=unresolved_question,
    )
    path = memory.create_draft(record)
    print(f"Created Experiment {experiment_id}: {path}")
    if is_bootstrap:
        print("Marked as the bootstrap experiment; no fake previous-image reflection is required.")
    elif latest:
        print(f"Inherited next hypothesis from Experiment {latest.experiment_id}.")
    print(f"Edit {path / 'experiment.json'} and add generated assets under {path / 'assets'}.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    ids = memory.experiment_ids()
    latest = memory.latest()

    print(f"Experiments: {len(ids)}")
    if not latest:
        print("Latest: none")
        return 0

    state = "finalized" if latest.finalized_at else "draft"
    kind = "bootstrap" if latest.bootstrap_experiment else "standard"
    generated = "generated" if latest.generation.generated_at else "not generated"
    print(
        f"Latest: {latest.experiment_id} ({state}, {kind}, {generated}) — "
        f"{latest.subject or 'subject not set'}"
    )
    print(f"Candidate learning: {latest.candidate_learning or 'not yet recorded'}")
    print(f"Next hypothesis: {latest.next_hypothesis or 'not yet recorded'}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    try:
        record = memory.load(args.experiment_id)
        request = build_generation_request(record)
        if args.dry_run:
            print(f"Experiment: {record.experiment_id}")
            print(f"Model: {request.model}")
            print(f"Size: {request.size}")
            print(f"Quality: {request.quality}")
            print(f"Output: {record.output_reference}")
            print("Dry run only; no API request was made.")
            return 0

        output = generate_experiment(
            memory,
            args.experiment_id,
            OpenAIImageGenerator(),
            overwrite=args.overwrite,
        )
    except (GenerationError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Generated Experiment {args.experiment_id}: {output}")
    print(
        f"Metadata: {memory.experiment_path(args.experiment_id) / 'result-metadata.json'}"
    )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    record = memory.load(args.experiment_id)
    errors = record.validate()
    if errors:
        print(f"Experiment {record.experiment_id} is incomplete:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Experiment {record.experiment_id} passes the research-loop completion gate.")
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    record = memory.load(args.experiment_id)
    try:
        path = memory.finalize(record)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Finalized Experiment {record.experiment_id}: {path / 'REPORT.md'}")
    print("Candidate learning appended to knowledge/LEARNINGS.md.")
    print("No automatic promotion to PROMPT_PLAYBOOK.md was performed.")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    memory = _memory(args.root)
    record = memory.load(args.experiment_id)
    print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gpt-image-lab",
        description="Run and validate evidence-driven GPT image experiments.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to the current directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new = subparsers.add_parser("new", help="Create the next experiment draft.")
    new.add_argument("--subject", default="")
    new.add_argument("--investigation", default="")
    new.add_argument("--why", default="")
    new.add_argument("--hypothesis", default="")
    new.add_argument(
        "--variable",
        action="append",
        default=[],
        help="Primary experimental variable; repeat at most twice.",
    )
    new.set_defaults(func=cmd_new)

    status = subparsers.add_parser("status", help="Show experiment count and latest learning.")
    status.set_defaults(func=cmd_status)

    generate = subparsers.add_parser(
        "generate", help="Generate the image for an experiment with the OpenAI Image API."
    )
    generate.add_argument("experiment_id")
    generate.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and show generation settings without making an API request.",
    )
    generate.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow an intentional pre-finalize retry to replace an existing result image.",
    )
    generate.set_defaults(func=cmd_generate)

    validate = subparsers.add_parser("validate", help="Validate an experiment without finalizing it.")
    validate.add_argument("experiment_id")
    validate.set_defaults(func=cmd_validate)

    finalize = subparsers.add_parser("finalize", help="Finalize and render a complete experiment.")
    finalize.add_argument("experiment_id")
    finalize.set_defaults(func=cmd_finalize)

    show = subparsers.add_parser("show", help="Print one experiment as JSON.")
    show.add_argument("experiment_id")
    show.set_defaults(func=cmd_show)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
