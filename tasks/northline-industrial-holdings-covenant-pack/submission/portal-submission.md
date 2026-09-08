# Portal Submission Form — northline-industrial-holdings-covenant-pack

Generated: 2026-09-04 08:17 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Northline Industrial Holdings closed the quarter on June 30, 2026, and Mid-Market Credit needs the Q2 covenant certificate pack before Friday's portfolio committee. The borrower says Total Leverage, Interest Coverage, and the CapEx basket are all fine, but the debt extract, EBITDA add-back bridge, and credit agreement excerpts do not reconcile on their face. If Funded Debt or Adjusted EBITDA is wrong, the bank either clears a revolver draw that trips a financial covenant or pushes an amendment the credit does not need.

Input files: northline-industrial-holdings_debt_schedule.xlsx, northline-industrial-holdings_ebitda_bridge.csv, credit_agreement_covenant_excerpts.txt

Produce a workbook named covenant_headroom_northline-industrial-holdings.xlsx for the committee file. Build Consolidated Funded Debt and Consolidated Adjusted EBITDA using the credit agreement definitions (not the borrower's claimed treatments), test Total Leverage, Interest Coverage, and CapEx basket usage as of 2026-06-30, document each material add-back or debt inclusion/exclusion you accept or reject, and state a clear pass/fail recommendation for the certificate. The agreement governs where the borrower pack conflicts.
```

Character count: 1207 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`13-2041.00|Credit Analysts`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Analyze credit data and financial statements to determine the degree of risk involved in extending credit or lending money.
2. Generate financial ratios, using computer programs, to evaluate customers' financial status.
3. Prepare reports that include the degree of risk involved in extending credit or lending money.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Mathematics

### Input File Uploader

Upload: `tasks/northline-industrial-holdings-covenant-pack/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/northline-industrial-holdings-covenant-pack/submission/golden.zip`
Expected deliverable: `covenant_headroom_northline-industrial-holdings.xlsx`

Rubric criteria: **33** (28 positive, 5 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal northline-industrial-holdings-covenant-pack
```
