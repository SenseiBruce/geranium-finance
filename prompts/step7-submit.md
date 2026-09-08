# Step 7: Platform Submit and Auto-Eval Loop

**Manual step** with Cursor support for revisions.

When the user says **autopilot through last step**, **ready to upload**, **portal for \<slug\>**, or finishes Step 6/7a/7b — the agent must **surface the submission pack in chat** (not only point at files).

## Agent: provide the submission pack in chat

After `gf preflight <slug>` (or confirm Step 6 already packaged), **print the following in the reply** so the user can paste without hunting files:

### 1. Upload paths (absolute)

```
tasks/<slug>/submission/inputs.zip
tasks/<slug>/submission/golden.zip
```

### 2. Section 1 — copy blocks from `submission/portal-submission.md`

In the chat reply, include **verbatim**:

- **User Prompt** (full text in a fenced block)
- **O\*NET occupation** (`code|name`)
- **O\*NET tasks** (exact dropdown strings, numbered)
- **O\*NET skills** (Essential Skills only)
- **Input file count**, multimodal, web search, hours
- **Section 1 check order** (as listed in the portal form)

### 3. Section 2 — from `submission/portal-section2.md`

In the same reply (or immediately after Section 1 if the message is huge):

- **Golden zip path** + note that golden files must match the deliverable name
- **Every rubric criterion** as paste-ready blocks: Criterion text + Weight on separate lines (no weights inside criterion text)
- **Section 2 check order**
- Any **Warnings** from the portal form (fix before paste)

### 4. Do not skip

- Run `gf preflight <slug>` before dumping paths if anything changed since last package
- Prefer reading `tasks/<slug>/submission/portal-submission.md` and `portal-section2.md` (synced copies) over task-root drafts
- If the reply would exceed a comfortable length, paste Section 1 fully in chat and say Section 2 is in `submission/portal-section2.md` **plus** still list criterion count, total positive/negative weight, and the first few criteria as a sanity check

## Before you open the portal

```bash
.venv/bin/python scripts/gf.py preflight <slug>
```

Or at minimum:

```bash
gf portal <slug>
gf portal2 <slug>
```

Open **`tasks/<slug>/submission/portal-submission.md`** for Section 1, then **`portal-section2.md`** for golden + rubric.

## Platform upload (Snorkel Expert Platform)

### Section 1 — Prompt & Input Files

Use **`portal-submission.md`** for every field:

- User Prompt
- O*NET occupation (`code|name`)
- O*NET tasks and skills (Essential Skills only)
- Input count, multimodal, web search, hours
- Upload `inputs.zip` from `submission/`

### Section 2 — Golden Solution & Rubric

After Section 1 passes:

```bash
gf portal2 <slug>
```

Use **`portal-section2.md`** for:

- Golden zip upload path
- Each rubric criterion (text + weight in separate fields)
- Section 2 check order

### Section 3 — AHT

- Report honest minutes from start to submit

## Auto-eval (wait 60–120 minutes)

| Check | Pass condition |
|-------|----------------|
| Golden Solution | PASSED |
| Dataset Quality | PASSED |
| LLM Generated Files | PASSED |
| Difficulty | At least one agent accuracy ≤80% |
| Rubric Quality | good or excellent |

## Track in `submission-log.md`

```markdown
# Submission Log — <slug>

## Upload
- Date:
- Task/Submission ID:

## Auto-eval results
- Golden Solution:
- Dataset Quality:
- LLM Files:
- Difficulty (best/worst %):
- Rubric Quality:

## Reviewer feedback

## Revisions
```

## If auto-eval fails

| Failure | Return to |
|---------|-----------|
| **Build status FAILED** / `CodeExecutionEnvironment` | Fresh `gf repackage <slug>` → re-upload zips + rubric → retry; see [`docs/auto-eval-playbook.md`](../docs/auto-eval-playbook.md) |
| Difficulty (both >80%) | Step 2a — harden inputs/reasoning |
| LLM Files / Dataset Quality | Step 2b or 4 — edit files, remove tells |
| Rubric Quality needs_improvement | Step 5 — see `docs/portal-rubric-quality.md` |
| Golden Solution | Step 4 or 5 |

## Rebuttals

Post in `#ec-geranium-project` daily Eval & Review thread with Task ID + screenshot. Do not DM.

## Register outcome

Update `registry/metrics-summary.json` when task reaches Accepted or Needs Revision.
