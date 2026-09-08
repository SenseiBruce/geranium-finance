# AGENTS.md — Geranium Finance Authoring

Rules for Cursor agents working in this repository.

## Pipeline discipline

1. **One step per conversation.** Do not combine Step 2a and 2b, or prompt + golden, in one chat.
2. **Respect handoff boundaries.** Step 2b reads only `task-spec.md`. Step 3 file names must match `inputs/`.
3. **Run gates before marking complete.** Write `.stepN-complete` only after the gate script exits 0.
4. **Never skip human verification** on golden solution numbers and rubric values.

## Geranium quality bar

- Prompt: practitioner voice, US-based, 3–5+ hour workflow, concrete output filename, input files by exact name.
- No "You are a [title] at [company]" opener. Lead with situation and stakes.
- Do not overspecify steps — state what to produce, not how.
- Input files: substantial, field-authentic, no answer leakage, no LLM tells.
- Golden: human-verified, client-ready, spreadsheets use live formulas.
- Rubric: 15–60 atomic criteria, ≥2 negative, style ≤25% of reward, golden scores 100.
- Rubric portal rules: grade the deliverable only (not golden.zip layout); prohibited-decision negatives; document-order wording. See `docs/portal-rubric-quality.md`.

## LLM tells to avoid

- Generic role framing, stacked adjectives + failure lists
- AI-blue Excel headers (#1C3557 family)
- Em dash overuse, hedged language ("it is worth noting")
- Round numbers, "Company A", placeholder text
- File names like `golden_solution.xlsx`
- Step-by-step numbered instructions disguised as a task

## Finance authenticity

- Use realistic entity names, irregular figures, sector-appropriate terminology.
- Distribute information across files — no single file gives the full answer.
- Build intentional messiness: duplicates, conflicting records, governing hierarchy.
- Match deliverable type to occupation (controller → workbook, underwriter → desk review sheet).

## Project skills (auto — no manual trigger)

Cursor must load these on its own via `.cursor/rules/geranium-auto-skills.mdc`:

| Skill | Auto when |
|-------|-----------|
| `geranium-auto-eval-triage` | Pasted Section 2 auto-eval / Needs Revision |
| `geranium-preflight` | Upload / resubmit / preflight |
| `geranium-entity-rename` | Entity rename / LLM naming cluster |

Do not ask the user to name the skill. Read `.cursor/skills/<name>/SKILL.md` and follow it.

```bash
python3 scripts/<script>.py tasks/<slug>/ ...
```

Before Step 7 portal upload, run `gf portal <slug>` and copy every field from `submission/portal-submission.md`. Use `gf onet <slug>` if you need to refresh O*NET dropdown strings.

**Zips:** Never upload stale `inputs.zip` / `golden.zip`. Before every portal resubmit run `gf repackage <slug>`. Gates and `package_zips.py` rebuild from `inputs/` and `golden/`; superseded zips go to `tasks/<slug>/archives/zips/<timestamp>/`. Use `submission/` after repackage or `gf gate 6 <slug> --package`.

**Skeletons:** Portal Uniqueness fails when two tasks share a decision shape. Check `gf skeleton status` / `registry/skeletons.json` before `/new`. `trueup_reconcile` is CLOSED. Bare `/new` uses `gf new --auto` (free skeleton).

**Preflight (Helix lessons):** Before every upload or resubmit run:

```bash
.venv/bin/python scripts/gf.py preflight <slug>
```

Rebuilds zips, then fails on rubric↔input entity rename drift, IEEE float artifacts in golden digests, stale `submission/` zips, deliverable-name mismatch, and ungrounded tab-name reward. `package_consistency_check.py` is also wired into `gf gate 4/5` and `task_readiness`.

**Entity renames:** Update constants + regenerate inputs/golden + `rubric.json` + prompt in one turn. Portal: find/replace **delta only** — never leave old names on the portal while uploading new zips.

## What not to do

- Do not paste platform-generated rubric criteria directly.
- Do not commit copyrighted or employer proprietary content.
- Do not reference "Geranium", "golden", or "eval" inside input files.
- Do not create commits unless the user asks.
