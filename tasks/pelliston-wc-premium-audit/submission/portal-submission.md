# Portal Submission Form — pelliston-wc-premium-audit

Generated: 2026-09-04 06:48 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Pelliston Machine Works is preparing the 2025-12-31 self-insured workers' compensation reserve for external audit and the bank borrowing-base certificate. The company retains $350,000 per occurrence. Calendar-year TPA payments are in pelliston_claims_payment_ledger.csv. Open claims and the accident-year paid triangle are in pelliston_open_claims_triangle.xlsx. Retention, IBNR factors, closed-claim treatment, and subrogation recognition are governed by actuarial_funding_memo.txt.

Input files: pelliston_claims_payment_ledger.csv, pelliston_open_claims_triangle.xlsx, actuarial_funding_memo.txt.

Build self_insured_wc_reserve_pelliston.xlsx as the Controllers workpaper for the audit PBC and lender pack. Apply the memo retention cap to case reserves, compute accident-year IBNR from the memo factors using the appropriate cumulative-paid source, show the excess/ceded bridge for losses above retention, roll the reserve forward from the prior year-end balance, and include a short booking recommendation. Do not rewrite excess policy wording.
```

Character count: 1048 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`11-3031.01|Treasurers and Controllers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Handle all aspects of employee insurance, benefits, and casualty programs, including monitoring changes in health insurance regulations and creating budgets for benefits and worker's compensation.
2. Conduct or coordinate audits of company accounts and financial transactions to ensure compliance with state and federal requirements and statutes.
3. Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Mathematics
- Critical Thinking
- Reading Comprehension

### Input File Uploader

Upload: `tasks/pelliston-wc-premium-audit/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/pelliston-wc-premium-audit/submission/golden.zip`
Expected deliverable: `self_insured_wc_reserve_pelliston.xlsx`

Rubric criteria: **27** (23 positive, 4 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal pelliston-wc-premium-audit
```
