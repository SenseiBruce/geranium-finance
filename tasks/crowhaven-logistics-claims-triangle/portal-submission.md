# Portal Submission Form — crowhaven-logistics-claims-triangle

Generated: 2026-09-07 09:50 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Crowhaven Logistics renews its commercial auto and general liability package on 2026-03-01. Before underwriting sets quote authority, actuarial has to review the financial soundness of the existing program, set year-end case and pure IBNR liabilities, and explain the technical results to the renewal committee.

Input files: crowhaven-logistics_loss_triangle.xlsx, crowhaven-logistics_open_claims.csv, actuarial_factor_memo.txt.

Build a single Excel workbook named claims_reserve_opinion_crowhaven-logistics.xlsx. Use the paid-loss triangle and the memo's governing paid LDFs to develop accident-year ultimates, applying the specified large-loss carve-out. Clean the open-claim inventory under the memo's closed-claim, duplicate, and VOID rules. Separate cleaned case from pure IBNR without double-counting. Calculate indicated ultimate losses and the ultimate loss ratio against the memo thresholds, then collaborate with underwriting on whether the existing Crowhaven program needs pricing improvements, referral, or exit by stating Quote, Refer, or Decline. Where the triangle Definitions sheet and the memo disagree, the memo governs. Document that choice and explain the technical reserve math in the workbook for company executives and underwriters.
```

Character count: 1257 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`15-2011.00|Actuaries`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Analyze statistical information to estimate mortality, accident, sickness, disability, and retirement rates.
2. Design, review, and help administer insurance, annuity and pension plans, determining financial soundness and calculating premiums.
3. Collaborate with programmers, underwriters, accounts, claims experts, and senior management to help companies develop plans for new lines of business or improvements to existing business.
4. Determine, or help determine, company policy, and explain complex technical matters to company executives, government officials, shareholders, policyholders, or the public.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Mathematics
- Critical Thinking
- Reading Comprehension

### Input File Uploader

Upload: `tasks/crowhaven-logistics-claims-triangle/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/crowhaven-logistics-claims-triangle/submission/golden.zip`
Expected deliverable: `claims_reserve_opinion_crowhaven-logistics.xlsx`

Rubric criteria: **31** (29 positive, 2 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal crowhaven-logistics-claims-triangle
```
