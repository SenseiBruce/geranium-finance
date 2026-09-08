# Task Spec: northline-industrial-holdings-covenant-pack

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** northline-industrial-holdings-covenant-pack
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Credit Analysts |
| O*NET Code | 13-2041.00 |
| O*NET Tasks (3–5) | Analyze credit data and financial statements to determine the degree of risk involved in extending credit or lending money.; Generate financial ratios, using computer programs, to evaluate customers' financial status.; Prepare reports that include the degree of risk involved in extending credit or lending money. |
| O*NET Skills (3–5) | Critical Thinking; Reading Comprehension; Mathematics |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Northline Industrial Holdings closed Q2 2026 on June 30. The bank's Mid-Market Credit portfolio committee meets Friday and needs a covenant headroom pack before the borrowing-base certificate goes out. Borrower-prepared materials claim full compliance on Total Leverage, Interest Coverage, and the CapEx basket, but the add-back schedule and debt inventory do not line up cleanly with the credit agreement excerpts. Getting Adjusted EBITDA or Funded Debt wrong either green-lights a draw that trips a financial covenant or forces an unnecessary amendment ask.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | covenant_headroom_northline-industrial-holdings.xlsx |
| Format | xlsx |
| Required sections/tabs | Funded debt build; Adjusted EBITDA build with add-back dispositions; covenant tests (leverage, interest coverage, CapEx basket); exception / disputed items; analyst recommendation for committee |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| northline-industrial-holdings_debt_schedule.xlsx | xlsx | Facility inventory, outstanding balances, cash interest TTM, CapEx YTD detail, LC and affiliate notes | 3+ sheets, 100+ cells | Seller note vs intercompany; undrawn LC; CapEx tagged as acquisition vs maintenance; stale draft tab | No finished leverage ratio; no pass/fail |
| northline-industrial-holdings_ebitda_bridge.csv | csv | Borrower TTM EBITDA bridge with claimed add-backs and narrative codes | 40+ line items / supporting rows | Restructuring above basket; run-rate synergies; sponsor fee over cap; ordinary-course litigation labeled extraordinary | No Adjusted EBITDA total labeled as covenant-ready |
| credit_agreement_covenant_excerpts.txt | txt | Governing definitions: Funded Debt, Consolidated Adjusted EBITDA, add-back caps, CapEx basket carve-outs, ratio thresholds | 600–900 words | Hierarchy: agreement governs over borrower bridge notes; explicit caps and exclusions | No computed headroom figures |

## Expert Judgment

1. Which debt balances enter Consolidated Funded Debt (seller note in; intercompany Guarantor note and undrawn LCs out).
2. Which borrower EBITDA add-backs are permitted under the agreement versus capped or disallowed.
3. How much of the Dayton restructuring charge survives the trailing-twelve-month Permitted Restructuring cap.
4. Whether projected Bolt & Die run-rate synergies may be added before they are realized in cash P&L.
5. How CapEx basket usage treats acquisition-integration spend carved out under the Permitted Acquisition CapEx exclusion.
6. Whether Total Leverage and Interest Coverage pass after lender-adjusted figures, and what the committee recommendation should be.

## Traps / Difficulty

- Borrower bridge adds the full $2,840,000 Dayton restructuring charge; agreement caps Permitted Restructuring Charges at $2,000,000 TTM.
- $1,100,000 "run-rate synergy savings" is not realized — agreement requires amounts reflected in consolidated results.
- Sponsor management fee $750,000 exceeds the $500,000 permitted affiliate fee basket.
- $425,000 warranty/customer dispute coded as extraordinary litigation — agreement limits litigation add-backs to non-ordinary-course matters.
- Seller note from Bolt & Die ($4,500,000) is Funded Debt; $1,200,000 intercompany note to Guarantor affiliate is excluded; $3,200,000 undrawn LCs are excluded.
- CapEx YTD gross exceeds the $8,500,000 basket unless $1,840,000 Bolt integration CapEx is carved out per the agreement.
- Debt schedule includes a superseded "Draft_Q1" tab with different revolver balance — Q2 As-Of balances govern.
- No single file yields pass/fail; agreement definitions must be applied across debt schedule and EBITDA bridge.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | covenant_headroom_northline-industrial-holdings.xlsx |
| Consolidated Funded Debt | Term + revolver drawn + finance leases + seller note |
| Adjusted EBITDA | Reported + permitted add-backs only (restructuring capped; synergies and ordinary litigation out; sponsor fee capped) |
| Total Leverage Ratio | Funded Debt / Adjusted EBITDA vs 4.50x max |
| Interest Coverage | Adjusted EBITDA / Cash Interest TTM vs 2.50x min |
| CapEx basket usage | Gross CapEx YTD minus Permitted Acquisition CapEx carve-out vs $8,500,000 |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Add-back documentation | Cites credit_agreement_covenant_excerpts.txt for each disallowed or capped item |
| Debt inclusion rationale | States seller note included and intercompany/undrawn LC excluded with agreement basis |
| Committee recommendation | States pass/fail on each tested covenant and flags residual exception risk |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends treating the full uncapped Dayton restructuring add-back as permitted Adjusted EBITDA | -5 |
| Recommends including projected Bolt & Die run-rate synergies in Adjusted EBITDA before realization | -5 |
| Recommends counting the undrawn letter-of-credit amount in Consolidated Funded Debt | -4 |

## Strip Test / Batch Diversity

Skeleton `covenant_headroom_pack` is FREE in the batch. Decision shape is debt schedule + EBITDA bridge + covenant definitions → headroom workbook with exception dispositions — not FX consolidation, not renewal Quote/Refer, not live-formula equity valuation, not CAM/premium true-up, not SI reserve rollforward.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Funded debt build under agreement definitions
- [x] Adjusted EBITDA with add-back dispositions
- [x] Leverage, interest coverage, and CapEx basket tests
- [x] Analyst recommendation for portfolio committee
