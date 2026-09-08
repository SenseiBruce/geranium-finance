# Step 6: Quality Gates and Packaging

**Fresh Cursor chat.** Final local validation before platform upload.

## Input

Complete task directory with Steps 2b–5 markers.

## Output

- `tasks/<slug>/pre-submit-report.md`
- `tasks/<slug>/portal-submission.md` — **Step 7a** portal form answers (auto-generated)
- `tasks/<slug>/submission/` — copies of prompt, zips, rubric, portal form
- `tasks/<slug>/.step6-complete`
- `tasks/<slug>/.step7a-complete` — written when portal form is generated
- Updated `registry/task-registry.jsonl`

## Checklist

Run [`templates/pre-submit-checklist.md`](../templates/pre-submit-checklist.md) line by line.

## Gates (all must pass)

```bash
python3 scripts/seed_uniqueness_check.py check --task-dir tasks/<slug>
python3 scripts/task_readiness.py tasks/<slug> --strict
```

## Pre-submit report

Document in `pre-submit-report.md`:

- Gate command outputs (pass/fail summary)
- Rubric stats: count, negative count, style %, total positive weight
- Golden self-audit: confirms 100 on rubric
- Optional frontier model test: note if first-pass was too easy
- Strip test vs batch

## Package submission folder

```bash
python3 scripts/task_readiness.py tasks/<slug> --strict --package
```

`--package` rebuilds **both** `inputs.zip` and `golden.zip` from source folders (archiving any existing zips), runs validation, then copies fresh artifacts into `submission/`.

Registers task in `registry/task-registry.jsonl` on success.

On success: `touch tasks/<slug>/.step6-complete`

## Next step

Automated → [`step7a-portal-form.md`](step7a-portal-form.md) (runs during `--package`)

Manual → [`step7-submit.md`](step7-submit.md)
