# Workflow Prompts — Geranium Finance

Canonical 7-step pipeline for Finance & Insurance task authoring on Project Geranium.

## Overview

Each Geranium submission has three platform sections:

1. **Prompt & Input Files** — practitioner voice, 3–5+ hour workflow, named deliverable
2. **Golden Solution & Rubric** — 15–60 atomic criteria; golden scores 100
3. **AHT** — honest submission time in minutes

**Quality bar:** Tasks must require judgment and multi-step reasoning a frontier model cannot solve perfectly in one pass. Difficulty comes from input files and reasoning, not prompt length alone.

**Drift guard:** Use one fresh Cursor chat per step. Do not skip gates. Do not edit upstream artifacts without re-running downstream gates.

```text
Step 1:   Cursor/ChatGPT → Ideation + seed registry entry
Step 2a:  Cursor          → tasks/<slug>/task-spec.md only
Step 2b:  Cursor          → tasks/<slug>/inputs/ + inputs.zip
Step 3:   Cursor          → tasks/<slug>/prompt.txt
Step 4:   Human + Cursor  → tasks/<slug>/golden/ + golden.zip
Step 5:   Human + Cursor  → tasks/<slug>/rubric.json
Step 6:   Cursor          → pre-submit-report.md + all gates green
Step 7:   Manual          → Platform upload + auto-eval loop
```

---

## Non-negotiable drift guards

- Step 2a produces **only** `tasks/<slug>/task-spec.md` (plus `metadata.yaml` draft).
- Step 2b consumes **only** `task-spec.md` — not a draft prompt with different file names.
- Step 3 references file names that **exactly** match `inputs.zip` contents.
- Golden solution output filename **exactly** matches prompt deliverable name.
- Rubric must score golden solution ~100; if golden fails rubric, fix rubric first.
- Any edit to inputs after Step 3 → re-run Steps 3–6.
- Any edit to task-spec → re-run Steps 2b–6.

---

## Canonical command sequence

```bash
# Step 2a
python3 scripts/lint_task_spec.py tasks/<slug>/task-spec.md --strict
python3 scripts/spec_satisfiability.py tasks/<slug>/task-spec.md

# Step 2b
python3 scripts/file_depth_check.py tasks/<slug>/inputs/
python3 scripts/package_zips.py tasks/<slug> --inputs
python3 scripts/validate_input_zip.py tasks/<slug>/inputs.zip --task-dir tasks/<slug>

# Step 3
python3 scripts/lint_prompt.py tasks/<slug>/prompt.txt --task-dir tasks/<slug>

# Step 4
python3 scripts/package_zips.py tasks/<slug> --golden
python3 scripts/validate_golden_zip.py tasks/<slug>/golden.zip --task-dir tasks/<slug>
python3 scripts/open_check.py tasks/<slug>/golden/

# Step 5
python3 scripts/lint_rubric.py tasks/<slug>/rubric.json --strict
python3 scripts/golden_vs_rubric.py tasks/<slug>/

# Step 6 (final)
python3 scripts/seed_uniqueness_check.py check --task-dir tasks/<slug>
python3 scripts/task_readiness.py tasks/<slug> --strict
```

---

## Step 1 — Ideation

**Prompt:** [`prompts/step1-ideation.md`](prompts/step1-ideation.md)

**Output:** `registry/seeds.jsonl` entry + optional `specs/<slug>-seed.md`

**Gate:** `python3 scripts/seed_uniqueness_check.py check --seed-id <slug> ...`

---

## Step 2a — Task Architecture Spec

**Prompt:** [`prompts/step2a-task-spec.md`](prompts/step2a-task-spec.md)

**Output:** `tasks/<slug>/task-spec.md`, `tasks/<slug>/metadata.yaml`

**Gate:** `lint_task_spec.py --strict`, `spec_satisfiability.py`

---

## Step 2b — Input Files

**Prompt:** [`prompts/step2b-input-files.md`](prompts/step2b-input-files.md)

**Output:** `tasks/<slug>/inputs/`, `inputs.zip`, `.step2b-complete`

**Gate:** `file_depth_check.py`, `validate_input_zip.py`

---

## Step 3 — Prompt

**Prompt:** [`prompts/step3-prompt.md`](prompts/step3-prompt.md)

**Output:** `tasks/<slug>/prompt.txt`, `.step3-complete`

**Gate:** `lint_prompt.py`

---

## Step 4 — Golden Solution

**Prompt:** [`prompts/step4-golden-solution.md`](prompts/step4-golden-solution.md)

**Output:** `tasks/<slug>/golden/`, `golden.zip`, `.step4-complete`

**Gate:** `validate_golden_zip.py`, `open_check.py`

---

## Step 5 — Rubric

**Prompt:** [`prompts/step5-rubric.md`](prompts/step5-rubric.md)

**Output:** `tasks/<slug>/rubric.json`, `.step5-complete`

**Gate:** `lint_rubric.py --strict`, `golden_vs_rubric.py`

---

## Step 6 — Quality Gates

**Prompt:** [`prompts/step6-quality-gates.md`](prompts/step6-quality-gates.md)

**Output:** `pre-submit-report.md`, `submission/` folder, `.step6-complete`

**Gate:** `task_readiness.py --strict`

---

## Step 7 — Platform Submit

**Prompt:** [`prompts/step7-submit.md`](prompts/step7-submit.md)

**Output:** `submission-log.md`, platform upload, auto-eval review

---

## Per-task directory

```
tasks/<slug>/
├── task-spec.md
├── metadata.yaml
├── prompt.txt
├── inputs/
├── inputs.zip
├── golden/
├── golden.zip
├── rubric.json
├── pre-submit-report.md
├── submission-log.md
├── submission/
├── .step2b-complete … .step6-complete
└── .metrics.jsonl
```
