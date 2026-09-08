# Portal Submission Form — granite-ridge-oct-renewal-desk

Generated: 2026-09-06 09:17 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Granite Ridge Apartment Partners' habitational renewal desk is clearing the October 1 effective-date batch for our Midwest multi-family book. I report to the chief underwriting officer, and binders need to go out Thursday. The account list export looks mostly clean at the summary level, but the location schedule, 36-month loss run, and our routing notes do not always agree on unit counts, subsidized occupancy flags, life-safety inspection status, or whether turnover-related vacancy is actually firm.

Input files: granite_ridge_renewal_accounts.csv, granite_ridge_location_schedule.csv, granite_ridge_loss_run_36mo.csv, granite_ridge_routing_notes.txt. The October batch has 36 accounts and roughly 80 location rows across the four files. Several accounts still show renewal-ready at the summary level even where child locations, inspection dates, or loss detail would push a different path.

I need a single Excel workbook named renewal_underwriting_review.xlsx that routes every account in the batch as Quote, Refer, Decline, or Ask Broker; flags location exceptions including subsidized-housing and inspection lapses; reconciles loss ratios where the account list disagrees with the loss run; and summarizes disposition counts for the desk. Where the source files conflict or require a judgment call, document what you did and why in the workbook, citing granite_ridge_routing_notes.txt for the routing rule you applied.
```

Character count: 1428 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`13-2053.00|Insurance Underwriters`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Examine documents to determine degree of risk from factors such as applicant health, financial standing and value, and condition of property.
2. Review company records to determine amount of insurance in force on single risk or group of closely related risks.
3. Decline excessive risks.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Mathematics

### Input File Uploader

Upload: `tasks/granite-ridge-oct-renewal-desk/submission/inputs.zip`

### How many input files are tied to your prompt?

4

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

Quick ref — upload golden: `tasks/granite-ridge-oct-renewal-desk/submission/golden.zip`
Expected deliverable: `renewal_underwriting_review.xlsx`

Rubric criteria: **31** (27 positive, 4 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal granite-ridge-oct-renewal-desk
```
