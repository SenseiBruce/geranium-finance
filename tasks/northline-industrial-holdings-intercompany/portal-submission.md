# Portal Submission Form — northline-industrial-holdings-intercompany

Generated: 2026-09-07 17:16 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Controllers need the Sep 3 intercompany cash-sweep report before treasury releases wires against the Aug 31 close. Parent AR still does not line up to the Canada and Mexico AP mirrors. Local-currency balances, a stale Canada FX booking, in-transit goods, a voided duplicate, and an orphan AP line are all in the way. Apply the cut-off and FX policies in the memo.

Work from the northline-industrial-holdings_ar_subledger.csv, northline-industrial-holdings_ap_mirror.csv, and intercompany_cutoff_and_fx_memo.txt source files.

Please produce intercompany_settlement_northline-industrial-holdings.xlsx as the Controllers settlement report. Use the memo for Appendix A population, FOB cut-off, and Aug 31 FX. Build the AR settlement, convert matching AP for the FX tie-out, log exceptions, and state the Sep 3 netting / wire recommendation by counterparty for disbursement authorization. Where the AR and AP ledgers conflict, the memo governs.
```

Character count: 941 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`11-3031.01|Treasurers and Controllers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Receive, record, and authorize requests for disbursements in accordance with company policies and procedures.
2. Maintain current knowledge of organizational policies and procedures, federal and state policies and directives, and current accounting standards.
3. Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Mathematics

### Input File Uploader

Upload: `tasks/northline-industrial-holdings-intercompany/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/northline-industrial-holdings-intercompany/submission/golden.zip`
Expected deliverable: `intercompany_settlement_northline-industrial-holdings.xlsx`

Rubric criteria: **35** (29 positive, 6 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal northline-industrial-holdings-intercompany
```
