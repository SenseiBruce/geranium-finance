---
name: geranium-preflight
description: >-
  Runs Project Geranium upload preflight for a task slug (rebuild zips, drift
  checks, portal forms). ALWAYS use automatically (do not wait for the user to
  name this skill) when the user says preflight, ready to upload, resubmit,
  package for submit, before portal upload, or asks for submission zip paths
  for inputs.zip or golden.zip.
---

# Geranium preflight

## Goal

Make `tasks/<slug>/submission/` safe to upload. One command, then a clear paste checklist.

## Procedure

1. Resolve slug (ask if missing).
2. Run from repo root:

```bash
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py preflight <slug>
```

3. If `package-consistency` or lint **FAIL**s → fix errors before telling the user to upload. Warnings (tab grounding, conjunction criteria) may proceed but surface them.
4. Confirm zips exist and list absolute paths:

```
tasks/<slug>/submission/inputs.zip
tasks/<slug>/submission/golden.zip
tasks/<slug>/submission/portal-submission.md
tasks/<slug>/submission/portal-section2.md
```

## User response template

```
Preflight: PASS | FAIL
Upload from:
  <absolute path>/submission/inputs.zip
  <absolute path>/submission/golden.zip

Section 1: portal-submission.md (prompt if changed)
Section 2: golden.zip + rubric deltas only if names/count changed

Warnings:
  - …
```

## After entity renames

Do **not** tell the user to re-enter all criteria. Give find/replace pairs (old → new) for affected criteria. Full re-paste only if criterion count changed.

## Never

- Point at `tasks/<slug>/inputs.zip` or `golden.zip` outside `submission/` after preflight (prefer submission/).
- Hand-zip in Finder.
- Say “upload” while consistency check still errors.
