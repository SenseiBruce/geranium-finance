# Finance & Insurance Occupations — Scenario Archetypes

Multi-role guide for Step 1 ideation. Pick one O*NET occupation and a **distinct** scaffold per task.

## Occupation map

| O*NET Role | Code | Example deliverable | Core judgment |
|------------|------|---------------------|---------------|
| Treasurers & Controllers | 11-3031.01 | Consolidation workbook | FX, proration, void rows, acquisition timing |
| Insurance Underwriters | 13-2053.00 | Desk review workbook | Quote/Refer/Ask broker/Decline paths |
| Financial Analysts | 13-2051.00 | Model / valuation xlsx | Live formulas, sensitivity, unit economics |
| Budget Analysts | 13-2031.00 | Variance memo + workbook | Actual vs plan, reclass, capex vs opex |
| Credit Analysts | 13-2041.00 | Credit memo docx | Covenant headroom, cash flow adjustments |
| Loan Officers | 13-2072.00 | Underwriting summary | DTI, collateral, exception documentation |
| Personal Financial Advisors | 13-2052.00 | Client plan docx | Tax-lot selection, RMD, allocation drift |
| Claims Adjusters | 13-1031.00 | Claim determination | Coverage vs exclusion, reserve, subrogation |

## Archetype library (rotate across batch)

### A — Multi-entity consolidation (Controllers)

- **Files:** brand ledger CSV, acquisition memo PDF, FX reference PDF
- **Traps:** mid-period acquisition proration, CAD conversion, void/cancelled lines
- **Deliverable:** `consolidated_review_<entity>.xlsx`
- **Exemplar:** Camelot Entertainment Group Q1 2025

### B — Renewal desk review (Underwriters)

- **Files:** account list CSV, location schedule CSV, loss run CSV, rules notes TXT
- **Traps:** account-level looks fine but location/loss changes path; pending POs not firm
- **Deliverable:** `renewal_underwriting_review.xlsx`
- **Exemplar:** Southeast commercial property July renewal

### C — Live-formula model (Financial Analyst)

- **Files:** cohort data xlsx, cap table csv, brief docx
- **Traps:** assumption on specific tab, sensitivity range, formula vs hard-code check
- **Deliverable:** `valuation_draft.xlsx`

### D — Budget triage under cap (FP&A / Events crossover)

- **Files:** vendor PDFs (alterations, cake, catering, rentals)
- **Traps:** fee order (pre-tax vs post-tax), guest-count split, stated cut priority
- **Deliverable:** `*_budget.pptx`

### E — Reconciliation audit (Finance ops)

- **Files:** contractor reconciliation xlsx, contract exhibit csv, modifications log, cost ledger, PO log, supplementary conditions pdf
- **Traps:** modification roll-forward, cost basis rules, duplicate invoices
- **Deliverable:** `*_reconciliation_audit.xlsx`

## Good vs bad prompt patterns

### Controllers — Good

> Our team handles consolidated reporting across three labels under Camelot Entertainment Group. I report to the CFO, and we're closing out Q1 2025 for the board meeting next week. The revenue figures came in from each label's own system and they don't reconcile cleanly. The following input files: camelot_entertainment_group_brand_ledger.csv, nimue_digital_acquisition_memo.pdf, excalibur_creative_fx_and_period_reference.pdf. I need consolidated_review_camelot_entertainment_group.xlsx …

### Controllers — Bad

> You are a financial controller at a media company. Using the attached transaction data, consolidate revenue and prepare a summary. Handle currency and acquisition adjustments as appropriate.

## Strip test checklist

Before Step 2a, confirm:

- [ ] Opener is situation-first, not title-first
- [ ] File count and types differ from last 2 tasks
- [ ] Deliverable type differs (xlsx vs docx vs pptx) when possible
- [ ] Decision structure is occupation-specific (not generic "analyze and recommend")
- [ ] No shared input filenames with other batch tasks

## O*NET task/skill selection tips

Pick tasks/skills the prompt **directly exercises**:

- Controllers: "Prepare financial reports", "Analyze financial data", "Manage budgets"
- Underwriters: "Evaluate insurance applications", "Analyze financial information", "Make decisions"
- Analysts: "Analyze financial data", "Develop financial models", "Present findings"

Do not select listening comprehension or unrelated skills for text-only analytical tasks.
