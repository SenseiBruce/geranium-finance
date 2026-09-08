# Rubric Writing Guide (Geranium V5.1)

## Rigid vs subjective

| Type | When | Example |
|------|------|---------|
| **Rigid** | One verifiable answer | "Rollup tab reports total consolidated Q1 2025 revenue of approximately $1,590,686.30." |
| **Subjective** | Multiple defensible conclusions | "Recommendation documents judgment on mid-period acquisition proration with reasoning tied to nimue_digital_acquisition_memo.pdf." |

Subjective ≠ vague. Name the conditions:

- Bad: "Provides a well-reasoned recommendation."
- Good: "Recommendation states board-facing consolidated figure after FX conversion, void exclusions, and Nimue proration, citing the Assumptions sheet."

## Atomic rule

One criterion = one observation.

- Bad: "Workbook has Assumptions, Rollup, and Reconciliation tabs with correct totals."
- Good: Split into three criteria, one per tab or one per total.

## Result + method pairing

When wrong logic could reach the right number:

1. **Result:** "Nimue Digital Consolidated USD is approximately $697,267.02."
2. **Method:** "Nimue proration reflects February 1, 2025 acquisition start with factor approximately 0.6556 on Assumptions sheet."

## Negative criteria

Word so **TRUE = failure present** (penalty fires):

- Good: `"The deliverable reports Nimue Digital Consolidated USD equal to full gross with no acquisition-date proration."` → weight **-5**
- Bad: `"The deliverable does not apply proration."` → logic inversion risk

Require **≥2 distinct** failure modes.

## Weight budget

Example 20-criterion rubric:

- 4× (+5) = 20 — core totals and key findings
- 8× (+3) = 24 — line-item checks
- 6× (+2) = 12 — structure/support
- 2× (+1) = 2 — minor labels
- **Positive total:** 58
- 2× (-5) = -10 — critical failures
- Negative magnitude / positive = 10/58 ≈ 17% (need ≥20% → add one more -3 or increase a -5)

Style criteria (formatting, tone): cap at 4 criteria × +1 = 4 → 4/58 ≈ 7% of reward ✓

## Category tags (for lint_rubric.py)

- `deliverable` — filename, format, required sections
- `accuracy` — numeric and factual checks
- `method` — derivation and reasoning pathway
- `structure` — tabs, sections, tables
- `style` — formatting only (counts toward style cap)
- `negative` — failure modes

## LLM criterion pattern (avoid)

> "Provides a clear, thorough analysis, not vague or incomplete."

Replace with specific checkable statements naming worksheet, cell, or exact value.

## Self-audit

Before Step 6, score golden against every criterion manually. If golden fails any positive criterion, fix golden or rubric. If a correct alternative would fail a subjective criterion, broaden conditions.

## Portal Section 2 checks

Local `lint_rubric.py --strict` enforces Geranium rules plus portal heuristics from [`portal-rubric-quality.md`](portal-rubric-quality.md). Highlights:

### Final answer only

Grade observable content in the named deliverable. Never grade `golden.zip` root layout unless the prompt deliverable is itself a zip.

### Prohibited-decision negatives

| Safe negative | Unsafe negative |
|---------------|-----------------|
| "Notes tab **recommends** closing at 12% pool without presenting the 15% brief requirement." | "Notes tab **does not** present the 15% pool requirement." |
| "Notes tab **instructs** board pricing using headline ARR despite Footnote 1." | "Model **fails to** exclude Meridian from ARR." |

Pair positives reward correct model content; negatives penalize affirmatively wrong board/closing language.

### Document order

- Good: "citations appear **earlier on the Notes tab than** any board sign-off recommendation."
- Bad: "citations appear **before recommending** board sign-off."

### Portal paste

Run `gf portal2 <slug>`; copy criterion blocks verbatim. No weights in text, no agent parentheticals, no manual renumbering after rubric edits.
