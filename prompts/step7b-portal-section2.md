# Step 7b: Portal Section 2 — Golden & Rubric

**Run after Section 1 passes** on the platform.

## Command

```bash
.venv/bin/python scripts/gf.py portal2 <slug>
```

Also generated during `gf gate 6 <slug> --package` when `golden.zip` and `rubric.json` exist.

## Output

- `tasks/<slug>/portal-section2.md`
- `tasks/<slug>/submission/portal-section2.md`
- `tasks/<slug>/.step7b-complete`

## What it includes

| Portal field | Source |
|--------------|--------|
| Golden upload path | `submission/golden.zip` |
| Files inside golden zip | Listed from zip manifest |
| Each rubric criterion | Text block (≤500 chars) for **Criterion** field |
| Each weight | Separate **Weight** field (+1 to +5 or -3 to -5) |
| Check order | Golden Quality → enter criteria → Rubric Quality → Name Check |

## Gate

```bash
python3 scripts/portal_form.py tasks/<slug> --section2 --sync-submission
```

Requires `golden.zip`, `rubric.json`, and deliverable filename match.

## Do NOT

- Put weights inside criterion text
- Paste platform-generated rubric criteria verbatim
- Upload golden before Section 1 checks pass
- Add agent commentary, parentheticals, or renumber criteria while pasting
- Paste from an old `portal-section2.md` after rubric edits without regenerating

## Portal rubric pitfalls (read before paste)

See [`docs/portal-rubric-quality.md`](../docs/portal-rubric-quality.md). Common Section 2 failures:

1. **Final outcome focus** — no golden-zip or invisible-process criteria
2. **Penalty scope** — negatives = prohibited board/closing *recommendations*, not missing-content mirrors
3. **Document order** — "appears earlier on the tab than…", not "before recommending…"
4. **Weight separation** — no `[+5]`, `(5 points)`, or platform notes in text fields

`portal-section2.md` ends with **Warnings** if `rubric_portal_checks.py` flags issues. Fix `rubric.json`, rerun `gf portal2 <slug>`, then paste.

## After this step (agent duty)

Per [`step7-submit.md`](step7-submit.md), put the **Section 2 paste pack in chat**: absolute `submission/golden.zip` path, each criterion text + weight (separate), check order, and any portal warnings. If the rubric is long, paste all criteria or explicitly point to `submission/portal-section2.md` after listing count and weight totals.

## Next step

Manual → finish Section 2 on platform, then [`step7-submit.md`](step7-submit.md) for auto-eval tracking
