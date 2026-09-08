# Portal Submission Form — haverford-process-equipment-gl-flux-close

Generated: 2026-09-08 10:14 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Haverford Process Equipment LLC is locking August 2026 books in Lebanon, Pennsylvania ahead of interim auditor fieldwork. Soft close is 2026-09-05. Plant accounting parked a “clean — no AJEs” note on the draft trial balance, but corporate still needs a re-performable month-end GL flux close pack before the books lock — not a one-pager that waves at the plant note.

That means walking prior vs current natural balances across roughly thirty accounts, JE activity crumbs, warranty / prepaid / physical inventory / open freight / PTO / CapEx tickets (plus noise aging and deposit lines), and the corporate threshold memo that sets absolute and percent investigation rules, mandatory AJE categories (voided billing still in the GL, accrual true-ups to support, prepaid amortization, inventory physical vs book, CapEx vs maintenance), hierarchy over the plant note, and the Ready / Ready with AJEs / Hold close matrix.

The following input files: haverford-process-equipment_trial_balance.xlsx, haverford-process-equipment_support_schedules.csv, flux_threshold_and_aje_memo.txt.

Deliver a workbook named flux_close_pack_haverford-process-equipment.xlsx with, equivalent section labels fine: material flux workpaper for every BS and P&L threshold breach (cause tied to JE crumbs and/or support line IDs); balanced proposed AJEs (account, debit, credit, amount, rationale, support ref) for every mandatory category the files evidence; TB-versus-support reconciliation per AJE; close-readiness with path-matrix check; short hierarchy note where plant commentary conflicts with the memo. Memo governs over the plant clean-close language. Before you call it done, confirm AJE debits equal credits and that flux explanations and AJEs do not talk past each other.
```

Character count: 1755 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`11-3031.01|Treasurers and Controllers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.
2. Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.
3. Maintain current knowledge of organizational policies and procedures, federal and state policies and directives, and current accounting standards.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Mathematics
- Reading Comprehension
- Monitoring

### Input File Uploader

Upload: `tasks/haverford-process-equipment-gl-flux-close/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/haverford-process-equipment-gl-flux-close/submission/golden.zip`
Expected deliverable: `flux_close_pack_haverford-process-equipment.xlsx`

Rubric criteria: **31** (26 positive, 5 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal haverford-process-equipment-gl-flux-close
```
