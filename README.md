# Geranium Finance Task Workflow

A step-based authoring factory for **Project Geranium** submissions in the **Finance & Insurance** sector. Adapted from the Terminal-Bench pipeline (handoff boundaries, gates, progress tracking) for Geranium's three-part deliverable: prompt + input files, golden solution + rubric, and AHT.

## Quick Start

1. Read [`workflow-prompts.md`](workflow-prompts.md) for the full 7-step pipeline.
2. Start a **fresh Cursor chat** for each step — do not combine steps in one conversation.
3. Pick a task slug and create `tasks/<slug>/` following the per-step prompts in [`prompts/`](prompts/).

```bash
# Example: validate a task before platform upload
python3 scripts/task_readiness.py tasks/<slug> --strict
```

## Pipeline Overview

| Step | Output | Gate |
|------|--------|------|
| 1 Ideation | `registry/seeds.jsonl` entry | `seed_uniqueness_check.py` |
| 2a Task Spec | `tasks/<slug>/task-spec.md` | `lint_task_spec.py` |
| 2b Input Files | `tasks/<slug>/inputs.zip` | `validate_input_zip.py` |
| 3 Prompt | `tasks/<slug>/prompt.txt` | `lint_prompt.py` |
| 4 Golden Solution | `tasks/<slug>/golden.zip` | `validate_golden_zip.py` |
| 5 Rubric | `tasks/<slug>/rubric.json` | `lint_rubric.py` |
| 6 Quality Gates | `pre-submit-report.md` | `task_readiness.py --strict` |
| 7 Platform Submit | Snorkel upload + auto-eval | Manual |

## Directory Layout

```
geranium-finance/
├── workflow-prompts.md    # Canonical pipeline
├── AGENTS.md              # Cursor agent rules
├── docs/                  # Guidelines, occupation guides
├── prompts/               # Per-step agent instructions
├── templates/             # Blank task-spec, checklist
├── scripts/               # Validation gates
├── registry/              # Seed/task uniqueness tracking
├── specs/                 # Optional seed notes
└── tasks/<slug>/          # Per-task workspace
```

## Reference

- Geranium Guidelines V5.1 (condensed): [`docs/geranium-guidelines-summary.md`](docs/geranium-guidelines-summary.md)
- Finance occupation archetypes: [`docs/finance-occupations.md`](docs/finance-occupations.md)
- Inspiration: Terminal-Bench workflow at `~/Downloads/Terminal-main`
