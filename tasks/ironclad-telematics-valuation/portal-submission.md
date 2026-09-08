# Portal Submission Form — ironclad-telematics-valuation

Generated: 2026-09-04 11:49 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Ironclad Telematics' CFO is locking a growth-equity term sheet for Thursday's board packet. Hartwell Partners proposed a $35M primary at $145M pre-money with a 12% post-money option pool refresh, but counsel's cap-table extract still shows a 10% available-pool note. The diligence memo quotes a $28.4M ARR run-rate that does not match the fleet cohort rollup once you drop MetroLink Transit Authority's municipal pilot and clear the duplicate expansion line finance keeps carrying. Two convertible notes also have to convert cleanly — Octavian Capital at a $50M cap with 20% discount, Vesper Growth at a $65M cap with no discount — and Quorum Ventures expects its full pro-rata slice of the primary.

Input files: ironclad_fleet_cohort_arr.xlsx, ironclad_cap_table.csv, growth_equity_diligence_brief.txt.

I need a single Excel workbook named ironclad_telematics_valuation.xlsx that ties fleet cohort retention and expansion math to a forward revenue view, shows fully diluted ownership after the proposed primary and note conversions, cross-checks valuation using the sponsor's revenue-multiple and DCF ranges, and includes sensitivity on fleet growth and net retention. Where the sources disagree on run-rate, pool sizing, pro-rata allocation, or conversion mechanics, document what you used and why on a notes tab with a clear cite back to growth_equity_diligence_brief.txt.
```

Character count: 1377 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`13-2051.00|Financial and Investment Analysts`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Employ financial models to develop solutions to financial problems or to assess the financial or capital impact of transactions.
2. Inform investment decisions by analyzing financial information to forecast business, industry, or economic conditions.
3. Perform securities valuation or pricing.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Mathematics

### Input File Uploader

Upload: `tasks/ironclad-telematics-valuation/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/ironclad-telematics-valuation/submission/golden.zip`
Expected deliverable: `ironclad_telematics_valuation.xlsx`

Rubric criteria: **32** (29 positive, 3 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal ironclad-telematics-valuation
```
