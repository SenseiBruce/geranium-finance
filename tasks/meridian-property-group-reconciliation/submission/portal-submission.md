# Portal Submission Form — meridian-property-group-reconciliation

Generated: 2026-09-03 09:02 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Meridian Commons is wrapping calendar-year 2025 and I need the CAM true-up locked before Controllers cuts tenant adjustment invoices next Tuesday. We billed monthly estimates all year off the January shares, Contour Fitness expanded in July, and suite T-122 has been dark since March — so the estimates are not going to tie to actuals without a rebuild.

I've pulled meridian_commons_expense_ledger.csv from property accounting, tenant_lease_abstracts.xlsx from the leasing file, and prior_cam_billing_register.txt with what we already invoiced. Input files: meridian_commons_expense_ledger.csv, tenant_lease_abstracts.xlsx, prior_cam_billing_register.txt.

I need a single Excel workbook named cam_trueup_meridian_commons.xlsx that rebuilds the eligible CAM expense pool from the ledger, allocates it using each lease's pro-rata share, caps, vacancy clause, and marketing rules from the abstracts (including Contour's mid-year share change), compares the result to the prior estimated billings, and gives Controllers a clear recommendation on which tenants get additional invoices versus credits. Where this year's actuals versus estimates point to better 2026 CAM estimate assumptions or lease-cap handling, call those out in the workbook so we can improve next year's process. Where the files conflict or a lease rule drives a judgment call, document it in the workbook and cite the source you relied on.
```

Character count: 1407 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`11-3031.01|Treasurers and Controllers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.
2. Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Mathematics
- Critical Thinking
- Reading Comprehension

### Input File Uploader

Upload: `tasks/meridian-property-group-reconciliation/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/meridian-property-group-reconciliation/submission/golden.zip`
Expected deliverable: `cam_trueup_meridian_commons.xlsx`

Rubric criteria: **25** (21 positive, 4 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal meridian-property-group-reconciliation
```
