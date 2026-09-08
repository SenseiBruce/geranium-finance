# Portal Submission Form — harborview-q1-consolidation

Generated: 2026-09-02 18:52 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Our team handles consolidated reporting across three labels under Harborview Media Group. I report to the CFO, and we're closing Q1 2025 (January 1 through March 31) for the board meeting next week. Revenue came in from each label's billing system and it doesn't reconcile cleanly when you roll it up.

I've pulled harborview_media_group_brand_ledger.csv, lattice_digital_acquisition_memo.txt, and cascade_creative_fx_and_period_reference.txt from finance and treasury. The ledger has about 25 posted rows across Beacon Media, Cascade Creative, and Lattice Digital, mixes USD and CAD, and includes void, cancelled, out-of-period, and pre-close rows that don't belong in Q1. The acquisition memo and FX bulletin don't always agree with how those rows are tagged.

I need a single Excel workbook named consolidated_review_harborview_media_group.xlsx that shows consolidated revenue per label and overall for the quarter, flags transactions that shouldn't count toward the total, and gives a short recommendation for the board. Where the source files disagree or require a judgment call, document what you did and why in the workbook.
```

Character count: 1131 / 3000

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

Upload: `tasks/harborview-q1-consolidation/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/harborview-q1-consolidation/submission/golden.zip`
Expected deliverable: `consolidated_review_harborview_media_group.xlsx`

Rubric criteria: **19** (16 positive, 3 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal harborview-q1-consolidation
```
