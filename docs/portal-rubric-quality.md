# Portal Rubric Quality — Lessons from Section 2 Checks

Snorkel's **Rubric Quality Check** runs many dimensions beyond local `lint_rubric.py`. Use this guide when writing Step 5 criteria and before pasting into the portal.

Reference task: `helix-biotech-valuation` (30 criteria, all Section 2 checks passed).

## Golden rule: grade the final answer only

Every criterion must be verifiable by inspecting the **submitted deliverable** named in the prompt (e.g. `valuation_draft.xlsx`).

| Do | Don't |
|----|-------|
| "The Notes tab cites SAFE terms from cap_table.csv." | "The analyst researched SAFE terms before modeling." |
| "Those citations appear earlier on the Notes tab than any board sign-off recommendation." | "Citations appear before recommending board sign-off." |
| "The Cap Table Pro Forma tab records Series A shares as 6,500,000 per cap_table.csv." | "The golden solution zip places valuation_draft.xlsx at the archive root." |

**Zip/archive criteria:** Only include zip-structure checks if the prompt requires a zip as the deliverable. Never grade `golden.zip` layout when the prompt asks for a single workbook inside it.

## Negative criteria (penalty scope)

Portal **penalty scope** rejects dual-polarity pairs: a positive that rewards correct content plus a negative that penalizes the same omission.

### Safe pattern (prohibited decisions)

Negatives describe an **affirmative bad board/closing recommendation** the workbook makes:

- "The Notes tab **instructs** board pricing using the $42,100,000 headline run-rate ARR as the binding valuation basis despite Footnote 1."
- "The Notes tab **recommends closing** the Series B using the 12% pool … **without presenting** the 15% requirement."
- "The Notes tab **recommends board acceptance** … at a pre-money valuation below $112,000,000 **without documented override**."

### Unsafe pattern (omission mirrors)

- "The deliverable does not exclude Meridian from ARR." (mirrors positive Criterion 5)
- "Cap table shows wrong SAFE conversion." (mirrors positives 7–8)
- Formatting / zip / filename negatives when positives already cover structure

Use **-3 to -5** only. Portal rejects **-1/-2**. Keep at least **2** distinct failure modes.

## Document order vs process timing

When sequencing matters on a tab, state **observable layout**:

**Good:** "…those citations appear earlier on the tab than any written board sign-off recommendation for the Series B."

**Bad:** "…before recommending board sign-off on the Series B."

The grader can scroll the Notes tab; they cannot verify when a recommendation was "made" as a process step.

## Style vs substance budget

Portal classifies some criteria as **STYLE/FORMATTING**:

- Tab/section **presence or labels** (especially with "or equivalent section labels")
- **Citation placement/order** when the cited facts are graded elsewhere

Keep style reward **≤25%** of positive weight and **<50%** of criterion count. Pair substance checks (values, formulas, reconciliations) separately from presentation order.

## Tab-name grounding budget

Platform dimension `sound_aligned_rubric` fails when reward rides on **sheet names the instruction never states**. The prompt says what to produce; it does not dictate layout, so "The Cohort Build tab…" is ungrounded unless the prompt names that section.

Keep ungrounded tab weight **≤25%** of positive weight. Fixes, in order of preference:

1. Drop the tab reference and grade the content ("The workbook records…")
2. Add `or equivalent section label` to the criterion
3. Only as a last resort, name the sections in the prompt (raises over-prescription risk)

`package_consistency_check.py` reports the exact share and the offending tab names.

## Rigidity budget

Each criterion requiring a **single exact number with no tolerance** counts as RIGID. One or two rigid checks are fine; dozens of exact-dollar criteria inflate rigid share. Prefer ranges where the prompt allows them (WACC 14–16%, multiple 5.5x–7.0x).

## Portal entry discipline

1. Run `gf portal2 <slug>` and copy criterion text **verbatim** from `submission/portal-section2.md`.
2. Put weights **only** in the Weight field — never `[+5]`, `(5 points)`, or notes like `(platform accepted this type)`.
3. Do not add agent commentary, renumber manually, or merge criteria during paste.
4. After rubric edits, run `gf repackage <slug>` if golden changed, then re-enter **all** criteria if counts shifted.
5. **After an entity rename:** do **not** wipe the rubric. Find/replace old → new names on the affected criteria only. Leaving old names on the portal while uploading a renamed golden is the #1 cause of 0.66 oracle scores.
6. Before upload, run `package_consistency_check.py tasks/<slug> --strict` — it catches rubric↔input name drift and golden float artifacts.

## Entity naming (LLM authorship + oracle sync)

Prefer **mixed institutional styles**, not five compounds of Nature+Geography (`Canyon Creek`, `Red Mesa`, `Bayline`, …):

| Prefer | Avoid clustering |
|--------|------------------|
| Octavian Capital, Hartwell Partners, Vesper Growth | Five `X Y Capital/Fund/Regional` names |
| Real-feeling irregular spellings | Identical adjective stacks |

When renaming mid-flight, update constants → regenerate inputs+golden → update `rubric.json` → `gf portal2` → **delta-paste** portal.

## Check dimension map

| Portal dimension | How we prevent it |
|------------------|-------------------|
| Final outcome focus | No zip/process criteria; document-order wording |
| Penalty scope | Prohibited-decision negatives only |
| Negative polarity | Affirmative failure wording; no inversion |
| Weight separation | Weights in JSON/portal field only |
| Output filename as source | Cite inputs; deliverable criterion names file only |
| Style weight budget | Substance criteria carry the reward |
| Over-prescription | "or equivalent section labels" for tabs |
| Coverage | Map each prompt bullet to ≥1 criterion before Step 6 |

## Optional improvement (advisory)

Portal may suggest a dedicated criterion for "Notes tab states which SAFE conversion treatment was selected and why" even when citations and mechanics are covered elsewhere. Add only if coverage check fails — not required when existing criteria plausibly reach the requirement.
