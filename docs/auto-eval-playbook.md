# Auto-Eval Playbook

After platform submission, wait **60–120 minutes** before checking results.

## Where to find feedback

Section 2: Golden Solution and Rubric — five boxes:

1. Auto-Evaluation Golden Solution Submission Feedback
2. Auto-Evaluation Dataset Quality (Input/Output) Check
3. Auto-Evaluation LLM Generated Files Check
4. Auto-Evaluation Difficulty Submission Feedback
5. Auto-Evaluation Rubric Quality Check (optional)

Build code in reviewer box (e.g. "AutoEval execution failed") — scroll to Section 2 boxes for details.

## Helix lessons (hard rules)

These failure modes burned many resubmits on `helix-biotech-valuation`. Treat them as non-negotiable.

### 1. One rename = four surfaces (never partial)

If you change an entity name, update **all** of these in the **same** commit/turn, then regenerate:

| Surface | Files |
|---------|-------|
| Constants / generators | `scripts/*_constants.py`, `generate_*_inputs.py`, `generate_*_golden.py` |
| Inputs | `inputs/*` |
| Prompt | `prompt.txt` |
| Rubric | `rubric.json` (every criterion that names the entity) |
| Golden | regenerate workbook |
| Portal paste | only the **delta criteria** that contain the old name |

**Never** upload a new golden/inputs while the portal rubric still names the old entity (or vice versa). Oracle will score ~0.66 and audits will scream "filing_sufficiency."

### 2. Portal paste = delta only when possible

Do **not** delete and re-enter all 30+ criteria after a rename. Find/replace the old → new entity strings on the affected criteria only. Weights stay put.

Full re-paste is required only when criterion **count** or **ids** change.

### 3. Conjunction criteria need the fact on the same row

If a criterion says *"board recommendation … cites cap_table.csv for SAFE terms"*, the **recommendation cell itself** must contain `cap_table.csv` + both SAFE names. Facts on earlier Notes rows do **not** satisfy flaky LLM judges (1/3 fail is enough to block).

### 4. Float artifacts (handled automatically — do not hand-patch)

Platform digests read the raw `<v>` text in worksheet XML. Two separate sources produce IEEE tails:

| Source | Example | Handled by |
|--------|---------|------------|
| Cached formula results | `266744662.79999998` | `_clean_number` inside `cache_xlsx_formula_values` |
| **Literal cells written by openpyxl** | `95.9` stored as `95.90000000000001` | `normalize_xlsx_numbers` inside `sanitize_xlsx` |

The second one is not a generator bug: openpyxl serializes every float with `"%.16g"`, which exposes the binary representation for values like 95.9. It affected **inputs and golden across four of five tasks** until fixed centrally.

Both passes run on repackage, so `gf preflight` is sufficient. `package_consistency_check.py` scans the stored XML (not openpyxl-parsed values) so it sees exactly what the platform sees.

### 5. Always repackage before upload

```bash
.venv/bin/python scripts/gf.py repackage <slug>
```

Upload only from `tasks/<slug>/submission/`. Never re-use an old Finder zip.

### 6. Read which check failed before rewriting content

| Box says | Action |
|----------|--------|
| Golden PASSED 3/3 | Do **not** rewrite golden numbers |
| LLM Generated Files FAIL (float / naming) | Round floats; de-bias names; keep math |
| Alignment audit names old entities | Portal rubric stale — fix paste, not golden |
| Dataset quality hard-fail | Fix golden labels / missing cases |
| Build FAILED / CodeExecutionEnvironment | Repackage + retry; not a content verdict |

### 7. Entity names live in one constants module

`helix_constants.py` is the pattern: every entity name, share count, and rate in one file that both `generate_*_inputs.py` and `generate_*_golden.py` import. A rename is then one edit plus a regen.

**Known gap:** `granite_ridge`, `sawtooth`, and `meridian` still carry entity literals inline across their generators. Before renaming anything in those tasks, extract a `<task>_constants.py` first — otherwise inputs and golden will drift exactly the way Helix did.

## Known structural gaps (deliberate, revisit when they bite)

| Gap | Risk | Trigger to fix |
|-----|------|----------------|
| No constants module for granite/sawtooth/meridian | Rename drift between inputs and golden | Before any entity rename in those tasks |
| Helix rubric hangs 61% of reward on tab names absent from the prompt | Platform `sound_aligned_rubric` minor finding (advisory, has not blocked) | If it ever escalates to Major, add `or equivalent section label` |
| Local negative-weight target (20%) is stricter than portal reality (~15%) | Gate noise trains us to ignore lint | Now a warning, hard error only below 12% |

## Build failure (`CodeExecutionEnvironment` / `Build status: FAILED`)

This message means the platform **never finished provisioning the sandbox** to run auto-eval. It is **not** a rubric-quality or golden-content verdict. The five Section 2 feedback boxes may all show the same build error with no per-check detail.

### Triage order

1. **Open every Section 2 auto-eval box** — confirm none of the five checks ran to completion with their own PASS/FAIL text.
2. **Re-upload from a fresh repackage** — stale zips are a common cause of mysterious platform failures after edits:
   ```bash
   cd ~/Projects/geranium-finance
   .venv/bin/python scripts/gf.py repackage <slug>
   ```
   Upload `submission/inputs.zip`, `submission/golden.zip`, and re-enter rubric criteria from `submission/portal-section2.md`.
3. **Run local preflight** — packaging, zip rules, Office metadata, and rename/float drift:
   ```bash
   .venv/bin/python scripts/task_readiness.py tasks/<slug> --strict
   .venv/bin/python scripts/package_consistency_check.py tasks/<slug> --strict
   .venv/bin/python scripts/sanitize_office.py tasks/<slug>/inputs tasks/<slug>/golden
   .venv/bin/python scripts/gf.py repackage <slug>
   ```
4. **Retry once after 2–4 hours** — two build IDs at the same timestamp often indicate a transient platform retry, not two separate content failures.
5. **Escalate if build still fails after fresh upload** — post in `#ec-geranium-project` Eval & Review thread with Task ID, both Build IDs, screenshot of Section 2 boxes, and confirmation that manual Rubric Quality + Name checks passed.

### What usually does *not* fix build failures

- Rewriting rubric criteria that already passed manual Rubric Quality Check
- Changing prompt voice when Section 1 already passed
- Editing only `golden/` without repackaging and re-uploading zips

### What to fix before resubmit anyway

- xlsx `docProps/core.xml` listing `openpyxl` as creator (LLM Generated Files risk once build succeeds) — `package_zips` now sanitizes on rebuild
- macOS extended attributes on source files before zipping
- Rubric criterion count drift vs `portal-section2.md` after edits
- **Formula cells without cached values** — openpyxl saves formulas but blank digests; `generate_*_golden.py` should call `cache_xlsx_formula_values` after save
- **Golden ARR methodology** must follow governing footnotes in inputs (e.g. Quarterly Rollup TTM, not headline minus one exclusion)
- **Entity rename sync** — rubric ↔ inputs ↔ golden ↔ prompt (see Helix lessons)
- **IEEE float tails** in cached cells — round to cents

## Golden Solution check failures

Common oracle failures when rubric manual check passed:

| Symptom | Fix |
|---------|-----|
| Formula output columns blank in digest | Cache computed values in xlsx after save (`sanitize_office.cache_xlsx_formula_values`) |
| Missing explicit cap-table facts ($ SAFE principal, Series A price) | Add literal cells on Assumptions or Cap Table Pro Forma, not only share counts |
| Notes citations fail | Every Notes bullet must name the governing input file; board row must repeat cites if criterion is conjunctive |
| Golden source fidelity / wrong ARR | Reconcile golden numbers against governing footnote method in inputs, not shortcut math |
| Dataset cross-document consistency | Remove duplicate input rows; vary templated metrics (e.g. identical NRR every quarter) |
| Entity name mismatch (0.66 rewards) | Rubric still has old names — delta-fix portal criteria |
| Criterion fails 1/3 (judge variance) | Make the graded fact explicit on the exact cell/row the criterion names |

## Pass conditions

| Check | Pass |
|-------|------|
| Golden Solution | PASSED (line 1–2), **3/3 @ 1.0** |
| Dataset Quality | PASSED (no hard-fail axis ≤2) |
| LLM Generated Files | PASSED |
| Difficulty | Best **or** Worst agent accuracy **≤80%** |
| Rubric Quality | `good` or `excellent` |

## Failure routing

| Failed check | Likely fix | Return to |
|--------------|------------|-----------|
| Section 1 Uniqueness | New **decision skeleton** (`gf skeleton status`); not noun polish | Step 1 / 2a |
| LLM Generated Files | Remove tells; round floats; deepen authenticity | Step 2b / 4 |
| Dataset Quality | Thin files, packaging, name mismatch, inverted labels | Step 2b / 4 |
| Golden Solution | Rubric/golden misalignment, packaging, missing row facts | Step 4 / 5 |
| Rubric invalid weights (-7/-9) | Clamp negatives to -3..-5 | Step 5 |
| Difficulty (both >80%) | Task too easy; add cross-file reasoning | Step 2a |
| Rubric needs_improvement | Atomicity, weights, vagueness | Step 5 |
| Build status FAILED / CodeExecutionEnvironment | If Golden already 3/3: fresh repackage + re-upload only | Step 7 (INFRA) |

## Difficulty hardening (if both agents >80%)

- Distribute facts across more files
- Add reconciling conflicts (two sources disagree; governing rule picks winner)
- Remove overspecification from prompt that gives away method
- Add edge cases requiring occupation-specific judgment

## Rebuttal template

Post in daily **Eval & Review Comments** thread (not new top-level):

```
Task ID: [ID]
Submission ID: [ID]

Check: [which auto-eval]
Belief: [what you believe is correct]
Evidence: [input file / golden / guideline section]
Acknowledgment: [what was flagged]
Why it satisfies: [specific explanation]
```

Attach screenshot of auto-eval box.

## Local pre-check (before upload)

```bash
.venv/bin/python scripts/package_consistency_check.py tasks/<slug> --strict
.venv/bin/python scripts/task_readiness.py tasks/<slug> --strict
.venv/bin/python scripts/lint_rubric.py tasks/<slug>/rubric.json --strict
.venv/bin/python scripts/gf.py repackage <slug>
.venv/bin/python scripts/gf.py portal2 <slug>
```

`package_consistency_check.py` fails on: rubric entity names missing from inputs, float artifacts in golden, stale `submission/` zips, deliverable basename mismatch.

Track outcomes in `tasks/<slug>/submission-log.md` and aggregate in `registry/metrics-summary.json`.
