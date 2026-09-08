# Portal Submission Form — whitaker-precision-components-loan-underwriting

Generated: 2026-09-06 02:58 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
Whitaker Precision Components LLC filed commercial equipment term loan application CL-2026-4418 to finance three CNC machines and fixtures for the Rockford, Illinois shop. Relationship-manager notes in the borrower package still push Approve at the full requested amount on "management EBITDA." Credit committee meets 2026-09-18 and needs a path decision with a sized commitment if policy requires it.

The following input files: whitaker-precision-components_borrower_financials.xlsx, whitaker-precision-components_collateral_schedule.csv, credit_policy_and_exception_memo.txt.

Deliver loan_underwriting_decision_whitaker-precision-components.xlsx. Rebuild Adjusted EBITDA under the memo rules, test DSCR and leverage at the full request and at any sized commitment, determine eligible collateral and LTV on appraisal NOLV, and state Approve, Approve with conditions, or Decline with the commitment and conditions that follow from the memo path matrix. Where the RM notes or application conflict with the credit policy memo, the memo governs.
```

Character count: 1044 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`13-2072.00|Loan Officers`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Analyze applicants' financial status, credit, and property evaluations to determine feasibility of granting loans.
2. Approve loans within specified limits, and refer loan applications outside those limits to management for approval.
3. Obtain and compile copies of loan applicants' credit histories, corporate financial statements, and other financial information.
4. Compute payment schedules.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Mathematics
- Active Learning

### Input File Uploader

Upload: `tasks/whitaker-precision-components-loan-underwriting/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/whitaker-precision-components-loan-underwriting/submission/golden.zip`
Expected deliverable: `loan_underwriting_decision_whitaker-precision-components.xlsx`

Rubric criteria: **32** (27 positive, 5 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal whitaker-precision-components-loan-underwriting
```
