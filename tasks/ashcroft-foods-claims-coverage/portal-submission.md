# Portal Submission Form — ashcroft-foods-claims-coverage

Generated: 2026-09-05 14:07 UTC

Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.

---

## Section 1 — Prompt and Input Files

### User Prompt

Paste into **User Prompt** (max 3000 characters):

```
The Columbus property desk needs a coverage opinion and indemnity case reserve for Ashcroft Foods LLC before the 2025-12-12 file-review committee. Claim CLM-CP-2025-8841 is the Dayton warehouse loss on 2025-11-18 (Zone B warm ~14h). Packet mixes selling-price demand, equipment rebuild, and multi-day BI.

The following input files: ashcroft-foods_claim_file.xlsx, ashcroft-foods_policy_schedule.csv, coverage_investigation_memo.txt. Memo is not a finished opinion. Distinguish recorded facts, potentially controlling provisions, superseded items, and derived conclusions. Follow memo hierarchy over stale notes/superseded rows.

Deliver claim_coverage_opinion_ashcroft-foods.xlsx. Keep ALAE outside indemnity case reserve.

Required sheets (exact names):

Coverage Decision Tree — For stock, equipment, BI, packaging (before indemnity math): raw fact; controlling provision; competing evidence; hierarchy decision; rule test; intermediate result; Accept/Partial/Deny or Exclude; financial consequence.

Evidence & Rule Matrix — issue; source; status; fact/rule; conflict; governing source; reason; downstream calc. Reconcile selling-price vs invoice; Active vs Superseded deductible; equipment prior subtotal vs components vs footing + Mechanical Breakdown. Rejected ≠ actual.

Maintenance Timeline — From claim-file dates + memo rules: last service, loss, elapsed days, OEM interval, grace, allowed interval, overdue, vendor-cancel date, days to loss, safe-harbor limit, condition results, coinsurance factor. Sensitivity: source OEM + shorter/longer hypotheticals; show coinsurance/reserve change.

Inventory Audit Trail — Per lot: ID, zone, raw amount, status, duplicate/VOID flag, stock/non-stock, treatment, eligible amount, exclusion reason, valuation basis. Totals for eligible/VOID/duplicate/packaging/other denied. Formula: raw = eligible + exclusions → PASS/FAIL.

Reserve Bridge — Formula-linked raw→VOID→duplicates→non-stock→eligible→salvage→coinsurance→deductible→case reserve. No hard-coded final.

Pure vs Case — Case reserve; triangle/other indicated (or none); pure IBNR; total; PASS case not also in pure IBNR.

Scenario Checks — Formula counterfactuals (non-governing): superseded deductible; selling-price; no coinsurance; equipment hypothetically covered; VOID/excluded control (actual reserve unaffected).

Decision Trace — Stock, equipment, BI, packaging, coinsurance, valuation, deductible: Source→rule→test→conclusion→impact. Reserve/recommendation reference these traces.

Consistency Checks — PASS/FAIL: inventory; equipment footing vs components; BI hours; maintenance elapsed days; reserve=formula chain; ALAE excluded; recommendation matches coverage/finance.

File Recommendation — Coverage posture; indemnity reserve; ALAE; major uncertainty; key sensitivity; underwriting disposition — tied to calculations/sources; consistent with actual (not counterfactual) analysis. Include denied/excluded detail, equipment footing, ALAE, valuation reconciliation as needed.
```

Character count: 2996 / 3000

### O*NET Occupation

Select **one** occupation from the dropdown (select this before tasks/skills):

`13-1031.00|Claims Adjusters, Examiners, and Investigators`

### O*NET Tasks

Select from dropdown (minimum 2, maximum 10). Copy exact strings:

1. Examine claims forms and other records to determine insurance coverage.
2. Adjust reserves or provide reserve recommendations to ensure that reserve activities are consistent with corporate policies.
3. Verify and analyze data used in settling claims to ensure that claims are valid and that settlements are made according to company practices and procedures.
4. Analyze information gathered by investigation and report findings and recommendations.

### O*NET Skills

Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:

- Critical Thinking
- Reading Comprehension
- Active Learning

### Input File Uploader

Upload: `tasks/ashcroft-foods-claims-coverage/submission/inputs.zip`

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

Quick ref — upload golden: `tasks/ashcroft-foods-claims-coverage/submission/golden.zip`
Expected deliverable: `claim_coverage_opinion_ashcroft-foods.xlsx`

Rubric criteria: **37** (32 positive, 5 negative)

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal ashcroft-foods-claims-coverage
```
