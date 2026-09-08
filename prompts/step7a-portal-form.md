# Step 7a: Portal Submission Form

**Automated step** — generates copy-paste answers for the Snorkel platform form.

## Input

- `prompt.txt`, `metadata.yaml`, `inputs.zip`, `rubric.json`
- O*NET cache at `registry/onet-cache/<code>.json`

## Output

- `tasks/<slug>/portal-submission.md` — Section 1–3 form answers
- `tasks/<slug>/submission/portal-submission.md` — mirror for upload folder
- `tasks/<slug>/.step7a-complete` — after gate passes

## Command

```bash
.venv/bin/python scripts/gf.py portal <slug>
```

Or:

```bash
.venv/bin/python scripts/gf.py gate 7a <slug>
```

Also runs automatically during `gf gate 6 <slug> --package`.

## What it includes

| Portal field | Source |
|--------------|--------|
| User Prompt | `prompt.txt` verbatim |
| O*NET Occupation | `metadata.yaml` → `code\|occupation` |
| O*NET Tasks | Exact dropdown strings from cache |
| O*NET Skills | Essential Skills only from cache |
| Input file count | `metadata.yaml` `input_files` or zip count |
| Multimodal | `platform.multimodal` |
| Web search | `platform.web_search_allowed` |
| Hours | `platform.time_estimate_hours` |
| Golden / rubric | Paths + rubric stats for Section 2 |

## Gate

```bash
python3 scripts/portal_form.py tasks/<slug> --sync-submission
```

Fails if `prompt.txt` or `metadata.yaml` missing, or O*NET tasks/skills fail dropdown validation.

## Do NOT

- Paraphrase O*NET task/skill strings
- Use technology skills from O*NET (Essential Skills only)
- Paste a different occupation than `metadata.yaml` specifies

## After this step (agent duty)

Do **not** end with only “forms written.” Per [`step7-submit.md`](step7-submit.md), put the **Section 1 paste pack in chat**: user prompt, O\*NET occupation/tasks/skills, input count / multimodal / web search / hours, and absolute `submission/inputs.zip` path.

## Next step

Manual → [`step7-submit.md`](step7-submit.md) — upload on platform using `portal-submission.md`
