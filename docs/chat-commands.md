# Chat Commands — Geranium Finance

Use these phrases in **Cursor chat**. The agent runs `scripts/gf.py` for you — you don't need the terminal.

## One-shot: new task from archetype

```
/new task renewal desk for Meridian Property Group
```

Or bare `/new` (agent auto-picks a **FREE** decision skeleton):

```
/new
```

Agent runs:

```bash
.venv/bin/python scripts/gf.py new --auto --entity "…"
# or with explicit archetype:
.venv/bin/python scripts/gf.py new --archetype covenant_pack --entity "…"
```

Archetypes: `consolidation`, `renewal_desk`, `valuation`, `covenant_pack`, `intercompany`, `claims_triangle`  
(`reconciliation` / CAM true-up is **CLOSED** — portal Uniqueness collision with Meridian.)

Before register, skeletons are gated:

```bash
.venv/bin/python scripts/gf.py skeleton status
.venv/bin/python scripts/gf.py skeleton pick
```

---

## Generate a seed only

```
/generate seed for insurance renewal desk
```

Or with entity:
```
/suggest seed consolidation for Harborview Media Group
```

Agent runs:
```bash
.venv/bin/python scripts/gf.py seed suggest --archetype renewal_desk --entity "..." --register
```

---

## Check pipeline status

```
/gf status
/gf status harborview-q1-consolidation
/what's next for harborview-q1-consolidation
```

---

## Run a pipeline step

After the agent creates/edits the step artifacts, it runs the gate:

| You say | Agent does |
|---------|------------|
| `run step 2a for my-slug` | Fill/review `task-spec.md` → `gf gate 2a my-slug` |
| `run step 2b for my-slug` | Build `inputs/` → `gf gate 2b my-slug` |
| `run step 3 for my-slug` | Write `prompt.txt` → `gf gate 3 my-slug` |
| `run step 4 for my-slug` | Build `golden/` → `gf gate 4 my-slug` |
| `run step 5 for my-slug` | Write `rubric.json` + audit → `gf gate 5 my-slug --confirm-audit` |
| `validate my-slug` | `gf validate my-slug --strict --package` (rebuilds both zips, syncs `submission/`) |
| `package my-slug for submit` | `gf gate 6 my-slug --package` |
| `repackage my-slug` / `resubmit my-slug` | `gf repackage my-slug` — **always** before re-uploading to portal |
| `preflight my-slug` | `gf preflight my-slug` — zips + drift + portal forms |
| `portal-drift my-slug` | `gf portal-drift my-slug` — rubric ↔ inputs ↔ golden sync card |
| `skeleton status` | `gf skeleton status` — FREE / IN USE / CLOSED decision shapes |
| `portal for my-slug` / `portal form` | `gf portal my-slug` — Section 1 in `portal-submission.md` |
| `portal2 for my-slug` / `section 2 form` | `gf portal2 my-slug` — golden upload + rubric in `portal-section2.md` |
| `onet for my-slug` / `onet dropdown` | `gf onet my-slug` — exact O*NET task/skill strings for portal |

**Rubric portal pitfalls:** see [`docs/portal-rubric-quality.md`](portal-rubric-quality.md). Run `lint_rubric.py --strict` and fix `portal-section2.md` warnings before pasting criteria.

**Before every resubmit — one command:**
```
preflight helix-biotech-valuation
```

```bash
.venv/bin/python scripts/gf.py preflight <slug>
```

Rebuilds both zips, then checks entity rename drift (rubric vs inputs), IEEE float artifacts in golden, stale `submission/` zips, deliverable-name mismatch, and tab-name grounding — then regenerates both portal forms. See [`docs/auto-eval-playbook.md`](auto-eval-playbook.md) Helix lessons.

### Project skills (auto-loaded when relevant)

| Skill | When |
|-------|------|
| `.cursor/skills/geranium-preflight/` | preflight / ready to upload / resubmit |
| `.cursor/skills/geranium-auto-eval-triage/` | paste Section 2 auto-eval / Needs Revision |
| `.cursor/skills/geranium-entity-rename/` | rename entities / LLM naming cluster |

---

## Step 7a portal form (auto)

After step 6 (`gf gate 6 <slug> --package`) or before upload:

```
/portal for helix-biotech-valuation
```

Opens `tasks/<slug>/submission/portal-submission.md` with:

- User prompt (verbatim)
- O*NET occupation, tasks, skills
- Input count, multimodal, web search, hours
- Upload paths and portal check order

---

## Full flow example (all from chat)

1. **You:** `New consolidation task for Apex Entertainment Group`
2. **Agent:** runs `gf new --archetype consolidation --entity "Apex Entertainment Group"`, fills task-spec
3. **You:** `Run step 2b for apex-entertainment-group-consolidation`
4. **Agent:** creates input files, runs `gf gate 2b ...`
5. **You:** `Run step 3...` through step 6
6. **You:** `Validate and package for submit`
7. **You:** `portal for <slug>` / ready to upload — agent dumps zip paths + Section 1/2 paste pack in chat (see `prompts/step7-submit.md`), then you upload from `tasks/<slug>/submission/`

---

## Agent rule

When the user uses `/gf`, `/new task`, `/generate seed`, `run step`, or `validate` — **always execute** `scripts/gf.py` from `~/Projects/geranium-finance` using `.venv/bin/python`. Do the creative work (spec, files, prompt, golden, rubric) in chat, then run the matching gate command before marking the step complete.
