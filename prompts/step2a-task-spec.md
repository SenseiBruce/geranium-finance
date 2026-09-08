# Step 2a: Task Architecture Spec

**Fresh Cursor chat.** Output only the spec — no input files, no prompt, no golden yet.

## Input

- Approved seed from `registry/seeds.jsonl`
- [`templates/task-spec.md`](../templates/task-spec.md)

## Output

- `tasks/<slug>/task-spec.md` — **sole handoff artifact**
- `tasks/<slug>/metadata.yaml` — O*NET and platform fields

## Do

Fill every section of the task-spec template:

1. **Situation** — Concrete trigger, stakes, US context, deadline. No "You are a…" opener.
2. **Deliverable** — Exact filename and format; required sections/tabs if occupation-appropriate.
3. **Input file plan** — Each file: name, type, role, depth target, messiness built in, **no leakage**.
4. **Expert judgment** — Decisions the model must make (not step-by-step how).
5. **Traps / difficulty** — Cross-file reconciliation, governing rules, edge cases.
6. **Rubric preview** — List rigid checks (exact values) vs subjective (bounded conditions).
7. **Metadata** — O*NET occupation, tasks, skills, multimodal, web_search, time_estimate_hours.
8. **Strip test** — How this differs from other tasks in `registry/task-registry.jsonl`.

## Gates

```bash
python3 scripts/lint_task_spec.py tasks/<slug>/task-spec.md --strict
python3 scripts/spec_satisfiability.py tasks/<slug>/task-spec.md
```

Both must exit 0 before Step 2b.

## Do NOT

- Create files under `inputs/` or write `prompt.txt` in this step.
- Dictate every column, formula, or analytical step in the spec.
- Include pre-computed answers in the input file plan.

## Next step

Fresh Cursor chat → [`step2b-input-files.md`](step2b-input-files.md)
