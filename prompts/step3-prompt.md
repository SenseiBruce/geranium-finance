# Step 3: Prompt

**Fresh Cursor chat.** Inputs: `task-spec.md`, `inputs/` (verify names match zip).

## Output

- `tasks/<slug>/prompt.txt`
- `tasks/<slug>/.step3-complete`

## Do

1. Write as handoff to a knowledgeable colleague — read aloud; rewrite if it sounds LLM-generated.
2. Open with **situation**, not role title.
3. Reference **every input file by exact name** from `inputs.zip`.
4. Name **concrete deliverable filename** matching spec.
5. Include platform detection phrase:

   `Input files:` or `The following input files:`

   followed immediately by file names (not the zip name).

6. State **what** to produce and **why** — not step-by-step how.
7. Leave expert judgment open where the spec requires it.

## Gate

```bash
python3 scripts/lint_prompt.py tasks/<slug>/prompt.txt --task-dir tasks/<slug>
python3 scripts/validate_input_zip.py tasks/<slug>/inputs.zip --task-dir tasks/<slug> --prompt tasks/<slug>/prompt.txt
```

On success: `touch tasks/<slug>/.step3-complete`

## Anti-patterns (reject and rewrite)

- "You are a financial analyst. Utilizing your expertise…"
- Numbered step lists (1. Open… 2. Calculate…)
- "Clear, comprehensive, well-structured analysis, not vague or incomplete"
- Generic references to "the spreadsheet" or "the PDF"

## Next step

Fresh Cursor chat → [`step4-golden-solution.md`](step4-golden-solution.md)
