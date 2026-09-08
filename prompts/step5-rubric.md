# Step 5: Rubric

**Fresh Cursor chat.** Human must verify all numeric values and rigid criteria.

## Input

- `prompt.txt`, `golden/`, `inputs/`, `task-spec.md` rubric preview

## Output

- `tasks/<slug>/rubric.json`
- `tasks/<slug>/.step5-complete`

## Format (`rubric.json`)

```json
{
  "criteria": [
    {
      "id": "deliverable_filename",
      "text": "The final deliverable is an Excel workbook named consolidated_review_camelot_entertainment_group.xlsx.",
      "weight": 2,
      "type": "rigid",
      "category": "deliverable"
    },
    {
      "id": "nimue_proration_error",
      "text": "The deliverable reports Nimue Digital Consolidated USD equal to full gross with no acquisition-date proration.",
      "weight": -5,
      "type": "negative",
      "category": "accuracy"
    }
  ]
}
```

## Rules (V5.1)

- 15–60 criteria; one atomic check each
- Weights: +4/+5 critical, +2/+3 important, +1 minor, -3/-5 penalties
- ≥2 negative criteria; negative points ≥20% of total positive weight
- Style/formatting criteria: <50% of count AND ≤25% of total positive weight
- Rigid: state exact value. Subjective: name conditions a sound answer must meet.
- Pair result + method where wrong logic could reach right number
- Negative criteria: word failure affirmatively ("The deliverable has X issue")
- Weights in JSON only — never in criterion text
- If prompt names exact file, include filename criterion

### Tab/section grounding (platform `sound_aligned_rubric`)

The prompt states **what to produce**, not the workbook layout. So a criterion must not hang reward on a sheet name the prompt never uses.

- Keep ungrounded tab-name weight **≤25%** of positive weight
- Either name the section in the criterion **with** `or equivalent section label`, or drop the tab reference and grade the content

| Do | Don't |
|----|-------|
| "The workbook records Series A preferred shares as 6,500,000 per cap_table.csv." | "The Cap Table Pro Forma tab records…" (tab never named in prompt) |
| "The cap table section, or equivalent section label, shows ownership summing to 100%." | "The Cohort Build tab calculates…" |

### Conjunction criteria (oracle judge variance)

If a criterion requires a fact **and** a citation on the same statement (e.g. "the board recommendation cites cap_table.csv"), the golden must carry both on **that exact row**. Facts elsewhere on the tab will fail some oracle runs, and a single 0.97 run blocks the whole submission.

## Gate

```bash
python3 scripts/lint_rubric.py tasks/<slug>/rubric.json --strict
python3 scripts/package_consistency_check.py tasks/<slug>/ --strict
python3 scripts/golden_vs_rubric.py tasks/<slug>/
```

Golden must score ~100. If not, fix rubric or golden before proceeding.

On success: `touch tasks/<slug>/.step5-complete`

## Do NOT

- Copy platform-generated rubric criteria verbatim.
- Bundle multiple checks in one criterion.
- Use vague words: "accurate", "thorough", "well-reasoned".
- Grade `golden.zip` layout or archive root structure when the prompt deliverable is a file inside the zip.
- Use process-timing language ("before recommending…") — use observable document order on a tab instead.
- Write omission negatives that mirror positive content checks (penalty-scope failure on portal).
- Put weights, point labels, or agent notes like `(platform accepted…)` in criterion text.

## Portal pre-flight (Step 7)

After `lint_rubric.py --strict` passes, read [`docs/portal-rubric-quality.md`](../docs/portal-rubric-quality.md) and run `gf portal2 <slug>`. Copy criteria verbatim from `portal-section2.md`; fix any warnings before portal entry.

## Next step

Fresh Cursor chat → [`step6-quality-gates.md`](step6-quality-gates.md)
