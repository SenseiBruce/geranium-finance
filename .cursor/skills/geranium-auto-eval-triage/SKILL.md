---
name: geranium-auto-eval-triage
description: >-
  Triages Project Geranium / Snorkel Section 2 auto-eval feedback for Finance
  tasks. ALWAYS use automatically (do not wait for the user to name this skill)
  whenever the user pastes auto-evaluation results, Needs Revision feedback,
  golden solution check FAILED or PASSED, dataset quality scores, LLM generated
  files check, LLM-authorship, oracle rewards like 0.66 or 0.97, accept rule
  3/3 at 1.0, CodeExecutionEnvironment, Build status FAILED, golden/rubric
  alignment, safety screen filing_sufficiency, or Expert Contributor guidance
  for a Geranium task slug.
---

# Geranium auto-eval triage

## Goal

Classify pasted portal feedback → apply the **smallest** fix. Do not rebuild the whole task when one box failed.

## Step 0 — First line of every reply (required)

Open with exactly one of:

- **`Content vs Infra: INFRA`** — Build FAILED / CodeExecutionEnvironment / sandbox provision failed, **and** Golden already PASSED 3/3 (or no content boxes populated). Action: `gf preflight` + re-upload zips only. **Do not** rewrite golden math, prompt, or rubric.
- **`Content vs Infra: CONTENT`** — Any Section 1/2 box failed on substance (Uniqueness, oracle &lt;1.0, dataset hard-fail, LLM authorship, rubric structure, safety).
- **`Content vs Infra: MIXED`** — Infra banner present **and** at least one content box failed. Fix content first; then fresh upload.

Vesper lesson (2026-09-04): Golden 3/3 + Dataset PASS + Build FAILED → uploads only.

## Step 1 — Identify slug

Confirm which task (`helix-biotech-valuation`, `granite-ridge-oct-renewal-desk`, etc.). If unclear, ask once.

## Step 2 — Score each box

| Box | Blocking? | Default action |
|-----|-----------|----------------|
| Golden Solution **PASSED** 3/3 @ 1.0 | No | **Do not** rewrite model math |
| Golden Solution **FAILED** (rewards &lt; 1.0) | Yes | Fix golden and/or rubric wording for failed criteria only |
| Dataset quality hard-fail (axis ≤2) | Yes | Fix golden labels / missing cases / source fidelity |
| LLM Generated Files / authorship FAIL | Yes if overall Needs Revision | Floats → sanitize + preflight; naming → entity-rename skill |
| Rubric Quality needs_improvement | Yes | Edit `rubric.json` + portal delta |
| Rubric Structure invalid weights (-7/-9, -1/-2) | Yes | Clamp negatives to **-3..-5** only (Ironclad lesson) |
| Section 1 **Uniqueness FAIL** | Yes | **Scaffold redesign** — new decision skeleton in `registry/skeletons.json`; not a polish pass (Pelliston vs Meridian true-up) |
| Alignment/Safety audit names **old** entities while golden has **new** | Usually stale paste | Portal find/replace delta — not golden rewrite |
| Build FAILED / CodeExecutionEnvironment | Infra | See Step 0 INFRA path |
| Difficulty (agents 0%) | Info only | Ignore unless both agents &gt;80% |

## Step 3 — Golden oracle failures

From EC-actionable failed criteria:

1. Open the cited sheet/row in `golden/`.
2. If criterion is a **conjunction** (board row + cites), put every required name/`cap_table.csv` on **that exact cell**.
3. If criterion names an entity missing from inputs → portal rubric is stale; sync names (do not invent phantom entities in golden).
4. After edits: regenerate if using generators → `gf preflight <slug>`.

## Step 4 — LLM authorship / float

1. Run `package_consistency_check.py tasks/<slug> --strict` (scans raw XML).
2. If float artifacts: `sanitize_office.py` on inputs+golden, then `gf preflight`.
3. If naming cluster: use **geranium-entity-rename** — do not only edit the golden Notes prose.

## Step 5 — Output to user

Always end with:

1. **Verdict** — which boxes block approval
2. **Minimal fix list** — files + portal deltas only
3. **Upload paths** — `tasks/<slug>/submission/*.zip` if a re-upload is needed
4. **What not to touch** — e.g. “golden math unchanged; portal criteria 5–8 only”

## Hard rules

- Golden 3/3 @ 1.0 → never “improve” valuation numbers for other boxes.
- Never wipe and re-enter all rubric criteria for a rename — delta find/replace only.
- Never upload without `gf preflight <slug>` after content edits.
- Prefer reading `docs/auto-eval-playbook.md` for edge cases.
- Uniqueness FAIL → change **skeleton** (see `registry/skeletons.json` / `gf skeleton status`), not nouns alone.
- Always lead the user reply with **Content vs Infra: …** (Step 0).
