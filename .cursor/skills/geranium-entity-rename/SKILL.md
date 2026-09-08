---
name: geranium-entity-rename
description: >-
  Atomically renames investor/customer/entity names across a Geranium Finance
  task and produces a portal find/replace delta. ALWAYS use automatically (do
  not wait for the user to name this skill) when the user asks to rename
  entities, de-bias LLM naming clusters, fix entity drift, replace investor
  names, or when LLM-authorship / synthetic boilerplate feedback flags compound
  nature/geography fund names (Capital, Partners, Fund, Regional, Creek, Mesa).
---

# Geranium entity rename

## Goal

One rename lands everywhere in **one turn**. Partial sync → oracle ~0.66 and safety audits.

## Preconditions

1. Identify slug.
2. Prefer a `scripts/<task>_constants.py` (Helix pattern). If names are only inline in generators (granite/sawtooth/meridian), **extract constants first** — then rename once.

## Naming guidance

Avoid five entities sharing compound geo/nature patterns (`Canyon Creek`, `Red Mesa`, `Bayline`, …). Prefer mixed institutional styles (`Octavian Capital`, `Hartwell Partners`, `Vesper Growth`).

## Procedure (same turn)

1. Edit constants (or create them) with the new names.
2. Regenerate:

```bash
cd ~/Projects/geranium-finance/scripts
../.venv/bin/python generate_<task>_inputs.py
../.venv/bin/python generate_<task>_golden.py
```

3. Update `tasks/<slug>/prompt.txt` (same names as constants).
4. Update `tasks/<slug>/rubric.json` — every criterion that mentions old names (search all old strings).
5. Verify no old names remain:

```bash
rg -n 'OldName1|OldName2' tasks/<slug>/rubric.json tasks/<slug>/prompt.txt tasks/<slug>/inputs tasks/<slug>/golden
```

6. Preflight:

```bash
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py preflight <slug>
```

7. Append a short note to `tasks/<slug>/submission-log.md`.

## Portal output (required)

Give the user a **delta table only** — do not instruct wiping all criteria:

| Find | Replace |
|------|---------|
| Old Entity A | New Entity A |
| … | … |

List which criterion numbers typically contain those strings (from `portal-section2.md`). Weights unchanged.

Full re-paste only if criterion **count** changed.

## Never

- Upload new zips while portal still has old names.
- Rename golden only.
- Invent names in rubric that do not appear in inputs.
