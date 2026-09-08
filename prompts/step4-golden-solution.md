# Step 4: Golden Solution

**Fresh Cursor chat (human leads).** LLM may assist drafting; you must verify every number.

## Input

- `prompt.txt`, all files in `inputs/`
- `task-spec.md` rubric preview

## Output

- `tasks/<slug>/golden/` — deliverable(s)
- `tasks/<slug>/golden.zip`
- `tasks/<slug>/.step4-complete`

## Do

1. **Perform the full task** as described in the prompt using only input files.
2. **Verify** every figure, name, and conclusion against source files manually.
3. **Format for client/manager:**
   - Excel: live formulas, professional tabs, no hard-coded derived values
   - Word: consistent headings, no self-describing subheadings
   - PowerPoint: slide master, charts for data comparisons
4. Name output file **exactly** as prompt specifies.
5. Package:

```bash
python3 scripts/package_zips.py tasks/<slug> --golden
```

## Gates

```bash
python3 scripts/validate_golden_zip.py tasks/<slug>/golden.zip --task-dir tasks/<slug>
python3 scripts/open_check.py tasks/<slug>/golden/
```

On success: `touch tasks/<slug>/.step4-complete`

## Do NOT

- Submit raw LLM output with surface edits only.
- Hard-code totals that should be formulas (spreadsheet tasks).
- Name files `golden_solution.*` or reference AI in the document.

## Next step

Fresh Cursor chat → [`step5-rubric.md`](step5-rubric.md)
