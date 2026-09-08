# Geranium Finance Task Workflow

A step-based authoring factory for **Project Geranium** submissions in the **Finance & Insurance** sector. Adapted from the Terminal-Bench pipeline (handoff boundaries, gates, progress tracking) for Geranium's three-part deliverable: prompt + input files, golden solution + rubric, and AHT.

## Quick Start

1. Set up the environment:

```bash
cd ~/Projects/geranium-finance
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Read [`docs/chat-commands.md`](docs/chat-commands.md) — **trigger everything from Cursor chat** (see below).
3. Read [`workflow-prompts.md`](workflow-prompts.md) for the full 7-step pipeline.

## Chat commands (no terminal needed)

Say any of these in Cursor chat; the agent runs `scripts/gf.py` for you:

| Say this | What happens |
|----------|----------------|
| `/gf status` | Show all tasks and next steps |
| `/new task renewal desk for Acme Corp` | Create seed + task folder from archetype |
| `/generate seed consolidation for Apex Media` | Suggest and register a seed |
| `run step 2b for my-slug` | Build inputs + run gates |
| `validate my-slug` | Full pre-submit check + package |

Archetypes: `consolidation`, `renewal_desk`, `valuation`, `reconciliation`

Full reference: [`docs/chat-commands.md`](docs/chat-commands.md)

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
