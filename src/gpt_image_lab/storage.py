from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .models import ExperimentRecord


EXPERIMENT_DIR_RE = re.compile(r"^(\d{4})$")


class RepositoryMemory:
    """Filesystem-backed memory for raw experiments and candidate learnings."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.experiments_dir = self.root / "experiments"
        self.knowledge_dir = self.root / "knowledge"
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

    def experiment_ids(self) -> list[str]:
        ids: list[str] = []
        if not self.experiments_dir.exists():
            return ids
        for child in self.experiments_dir.iterdir():
            if child.is_dir() and EXPERIMENT_DIR_RE.match(child.name):
                ids.append(child.name)
        return sorted(ids)

    def next_experiment_id(self) -> str:
        ids = self.experiment_ids()
        if not ids:
            return "0001"
        return f"{int(ids[-1]) + 1:04d}"

    def experiment_path(self, experiment_id: str) -> Path:
        if not EXPERIMENT_DIR_RE.match(experiment_id):
            raise ValueError("experiment_id must be a four-digit string such as 0001")
        return self.experiments_dir / experiment_id

    def create_draft(self, record: ExperimentRecord) -> Path:
        path = self.experiment_path(record.experiment_id)
        if path.exists():
            raise FileExistsError(f"experiment {record.experiment_id} already exists")
        path.mkdir(parents=True)
        (path / "assets").mkdir()
        self.save(record)
        (path / "assets" / "README.md").write_text(
            "# Experiment assets\n\nPlace generated images and relevant visual references here.\n",
            encoding="utf-8",
        )
        return path

    def save(self, record: ExperimentRecord) -> None:
        path = self.experiment_path(record.experiment_id)
        path.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(record.to_dict(), ensure_ascii=False, indent=2) + "\n"
        (path / "experiment.json").write_text(payload, encoding="utf-8")

    def load(self, experiment_id: str) -> ExperimentRecord:
        path = self.experiment_path(experiment_id) / "experiment.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return ExperimentRecord.from_dict(data)

    def latest(self) -> ExperimentRecord | None:
        ids = self.experiment_ids()
        return self.load(ids[-1]) if ids else None

    def recent(self, limit: int = 5) -> list[ExperimentRecord]:
        ids = self.experiment_ids()[-limit:]
        return [self.load(experiment_id) for experiment_id in ids]

    def finalize(self, record: ExperimentRecord) -> Path:
        if record.finalized_at:
            raise ValueError(
                f"Experiment {record.experiment_id} is already finalized. "
                "Create a new experiment for corrections or replication."
            )

        errors = record.validate()
        if errors:
            raise ValueError("Experiment is incomplete:\n- " + "\n- ".join(errors))

        record.generation.ensure_timestamp()
        record.finalized_at = datetime.now(timezone.utc).isoformat()
        self.save(record)

        path = self.experiment_path(record.experiment_id)
        (path / "REPORT.md").write_text(self.render_report(record), encoding="utf-8")
        self.append_candidate_learning(record)
        return path

    def append_candidate_learning(self, record: ExperimentRecord) -> None:
        """Append evidence to LEARNINGS.md. Never auto-promote to the durable playbook."""
        target = self.knowledge_dir / "LEARNINGS.md"
        if not target.exists():
            target.write_text("# Candidate Learnings\n", encoding="utf-8")

        block = (
            f"\n\n## Experiment {record.experiment_id}\n\n"
            f"- **Candidate learning:** {record.candidate_learning}\n"
            f"- **Confidence:** {record.confidence}\n"
            f"- **Scope:** {record.learning_scope or 'Not yet specified'}\n"
            f"- **Limits:** {record.learning_limits or 'Not yet specified'}\n"
            f"- **Hypothesis result:** {record.hypothesis_result}\n"
            f"- **Playbook promotion requested:** {'yes' if record.promote_to_playbook else 'no'}\n"
            f"- **Next hypothesis:** {record.next_hypothesis}\n"
        )
        with target.open("a", encoding="utf-8") as handle:
            handle.write(block)

    @staticmethod
    def render_report(record: ExperimentRecord) -> str:
        scores = "\n".join(
            f"- {key}: {score}/10 — {record.critique.evidence.get(key, '')}"
            for key, score in record.critique.visual_scores.items()
        )
        confounds = "\n".join(f"- {item}" for item in record.confounds) or "- None recorded"
        prior = "\n".join(f"- {item}" for item in record.relevant_prior_findings) or "- None"
        sources = "\n".join(f"- {item}" for item in record.research.sources) or "- No external sources recorded"

        return f"""# Experiment {record.experiment_id} — {record.subject}

## Investigation

{record.investigation}

**Why it matters:** {record.why_it_matters}

## Prior memory

{prior}

**Unresolved question:** {record.unresolved_question or 'None recorded'}

## Previous observation and reflection

### Worked
{chr(10).join(f'- {x}' for x in record.reflection.worked)}

### Failed
{chr(10).join(f'- {x}' for x in record.reflection.failed)}

### Uncertain
{chr(10).join(f'- {x}' for x in record.reflection.uncertain)}

## Research

{chr(10).join(f'- {x}' for x in record.research.learned) or '- No new external research; see relevance note.'}

**Relevance:** {record.research.relevance}

### Sources
{sources}

## Hypothesis

{record.hypothesis}

**Primary variables:** {', '.join(record.primary_variables)}

**Held stable:** {', '.join(record.held_stable) or 'Not specified'}

**Expected benefit:** {record.expected_benefit}

**Possible downside:** {record.possible_downside}

## Prompt

```text
{record.prompt}
```

**Prompt rationale:** {record.prompt_rationale}

## Output

- Reference: `{record.output_reference}`
- Model: {record.generation.model or 'Not recorded'}
- Generated at: {record.generation.generated_at or 'Not recorded'}
- Prompt version: {record.generation.prompt_version}
- Dimensions: {record.generation.width or '?'}×{record.generation.height or '?'}
- Quality: {record.generation.quality or 'Not recorded'}

## Visual critique

**Visual average:** {record.critique.visual_average}/10

{scores}

### Hypothesis-specific metric

- **{record.critique.hypothesis_metric_name}:** {record.critique.hypothesis_metric_score}/10
- {record.critique.hypothesis_metric_evidence}

### Three viewpoints

**Visual craft**
{chr(10).join(f'- {x}' for x in record.critique.viewpoints.get('visual_craft', []))}

**Prompt adherence / model behavior**
{chr(10).join(f'- {x}' for x in record.critique.viewpoints.get('prompt_adherence', []))}

**Commercial / social usability**
{chr(10).join(f'- {x}' for x in record.critique.viewpoints.get('commercial_social_usability', []))}

## Hypothesis result

**{record.hypothesis_result}** — {record.hypothesis_result_reason}

### Confounds
{confounds}

## Candidate learning

{record.candidate_learning}

- Confidence: {record.confidence}
- Scope: {record.learning_scope or 'Not yet specified'}
- Limits: {record.learning_limits or 'Not yet specified'}
- Promote to playbook now: {'yes' if record.promote_to_playbook else 'no'}

## Next hypothesis

{record.next_hypothesis}
"""
