# Step 2b: Input Files

**Fresh Cursor chat.** Read **only** `tasks/<slug>/task-spec.md`.

## Output

- `tasks/<slug>/inputs/` — source files (edit here)
- `tasks/<slug>/inputs.zip` — platform-ready zip (root-level files only)
- `tasks/<slug>/.step2b-complete` — written after gates pass

## Do

1. Create each input file per the spec's input file plan.
2. Meet depth floors ([`docs/geranium-guidelines-summary.md`](../docs/geranium-guidelines-summary.md)):
   - Spreadsheets: 100+ populated cells, multiple tabs where appropriate
   - Memos/reports: 500+ words substantive body
   - PDFs: real structure, not placeholder
3. Use realistic names, irregular numbers, sector terminology.
4. Build cross-file dependencies — reconcile conflicts across files.
5. Scrub leakage: no totals to derive, no hidden answer tabs, no project references.
6. Remove LLM tells: AI-blue headers, em dashes, "Company A", round numbers.
7. Package (rebuilds zip; archives prior copy under `archives/zips/<timestamp>/`):

```bash
python3 scripts/package_zips.py tasks/<slug> --inputs
```

## Gates

```bash
python3 scripts/file_depth_check.py tasks/<slug>/inputs/
python3 scripts/validate_input_zip.py tasks/<slug>/inputs.zip --task-dir tasks/<slug>
```

If `prompt.txt` exists, validation also checks name alignment. Otherwise validate against `task-spec.md`.

On success:

```bash
touch tasks/<slug>/.step2b-complete
```

## Do NOT

- Add subfolders inside the zip.
- Use spaces or double extensions in filenames.
- Include empty files or copyrighted content.

## Next step

Fresh Cursor chat → [`step3-prompt.md`](step3-prompt.md)
