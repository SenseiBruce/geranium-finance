# Portal Submission Form — vesper-culinary-brands-consolidation

Generated: 2026-09-08 08:33 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Vesper Culinary Brands is closing Q3 2025 consolidated net revenue for the board packet due Friday. Perform the analysis as of the Q3 2025 close in early October 2025. I report to the corporate controller. Three brands feed one extract: Hearth Kitchen Co (USD, owned all quarter), Brine & Barrel EU (EUR subsidiary), and Kiln Spice Works (tuck-in that closed mid-quarter). The billing pull does not roll cleanly once you hit FX, ownership timing, and status tagging in the extract.

Input files: vesper_culinary_brands_brand_ledger.csv, kiln_spice_acquisition_memo.txt, brine_barrel_fx_and_period_reference.txt. The ledger is a multi-brand export with roughly three dozen lines spanning two currencies and mixed posting statuses; row tags do not always match the memo and FX bulletin. Use both source texts, not just ledger columns, for board inclusion, EUR conversion, and mid-quarter ownership.

I need a single Excel workbook named consolidated_review_vesper_culinary_brands.xlsx that a controller can review before the packet goes out. Build it so the math is auditable end to end:

- Line-level inventory of the extract with inclusion or exclusion flags and reasons grounded in the governing sources
- Brand and consolidated Q3 net revenue in USD after applying the governing EUR conversion and Kiln ownership treatment
- A reconciliation bridge from raw extract gross by brand to adjusted board revenue, broken out by exclusion category, with control totals that tie back to the line inventory
- An exception or exclusion log showing transaction id, brand, reason, native amount, and USD impact after FX where relevant, with formula links where those amounts feed the rollup
- Documentation of both memo-supported Kiln ownership approaches: the selected final board method, and the alternative quantified only as a Conditional transaction-date cutoff scenario. Identify whether approval evidence is present in the packet; if not, document that absence (e.g., Approval evidence in supplied packet: not present). Do not invent approvals or treat cutoff as the final board method.
- Carry forward Kiln memo open items this packet cannot close: August 12 ownership-date confirmation vs Schedule 2.1 and bank wire confirmation, and post-close billing shipment/service support. Use August 12 as the modeling date from the memo, distinguish modeling from independent evidence confirmation, and leave both open. Do not invent those records.
- Short board recommendation stating the final consolidated figure and key judgments; where sources disagree or evidence is missing, document what you chose, why, and what remains unresolved

Include assumptions, detail, rollup, reconciliation, and recommendation content (or equivalent labels). Prefer live formulas for rollups, FX conversion, ownership factors, and exception USD impacts so changing an included line updates the bridge. Do not invent outside rates, approvals, or ledger rows that are not in the packet.
```

Character count: 2960 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`11-3031.01|Treasurers and Controllers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.
2. Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.
3. Advise management on short-term and long-term financial objectives, policies, and actions.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Mathematics
- Critical Thinking
- Reading Comprehension

### Input File Uploader

Upload: `tasks/vesper-culinary-brands-consolidation/submission/inputs.zip`

### How many input files are tied to your prompt?

3

### Are any input files in the task multi-modal?

No

_Check Yes only if input files contain video, audio, or images in addition to text._

### Is web search required for your task?

No

### If you were to complete this prompt manually without the help of any LLM's, how long would this task take?

5

---

## Section 2 — Golden Solution & Rubric

_Section 1 must pass first. Then run `gf portal2 <slug>` for full Section 2 copy-paste fields._

Quick ref — upload golden: `tasks/vesper-culinary-brands-consolidation/submission/golden.zip`
Expected deliverable: `consolidated_review_vesper_culinary_brands.xlsx`

Rubric criteria: **25** (22 positive, 3 negative)

---

## Section 3 — AHT

Report honest minutes from task start through submit.

---

## Portal check order

1. Paste **User Prompt**
2. Select **O*NET Occupation** (one only)
3. Run **O*NET Compliance Check**
4. Select **O*NET Tasks** and **O*NET Skills**
5. Run **O*NET Tasks & Skills Compliance Check**
6. Run **Prompt Quality Check**
7. Upload **inputs.zip** and set input count / multimodal
8. Run **Input Files Quality Check**
9. Set **web search** and **hours**
10. Continue to Section 2 — run `gf portal2 <slug>`

## Regenerate Section 1

```bash
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal vesper-culinary-brands-consolidation
```
