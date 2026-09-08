# Task Spec: helix-biotech-valuation

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** helix-biotech-valuation
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Financial and Investment Analysts |
| O*NET Code | 13-2051.00 |
| O*NET Tasks (3–5) | Employ financial models to develop solutions to financial problems or to assess the financial or capital impact of transactions.; Inform investment decisions by analyzing financial information to forecast business, industry, or economic conditions.; Perform securities valuation or pricing. |
| O*NET Skills (3–5) | Critical Thinking; Reading Comprehension; Mathematics |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Helix Biotech's CFO is finalizing a Series B term sheet with two lead candidates and needs a defendable valuation workbook before Monday's board call. The company sells lab-informatics subscriptions to hospital networks and regional reference labs. Finance pulled a cohort ARR export, the lawyer's cap-table extract, and the lead investor's diligence brief, but the three sources do not agree on run-rate ARR, the post-money option pool refresh, or how two outstanding SAFEs convert into the round.

The board wants one Excel model that ties cohort retention and expansion to a forward revenue view, shows fully diluted ownership after the proposed $28M primary at the investor's stated pre-money, and documents where you overrode a source file versus the investor brief.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | valuation_draft.xlsx |
| Format | xlsx |
| Required sections/tabs | Assumptions (documented overrides); Cohort Build (live retention/expansion math from cohort_summary.xlsx); Revenue Forecast (formula-driven, not hard-coded totals); Cap Table Pro Forma (pre- and post-money with SAFE conversion); Valuation Summary (revenue-multiple and DCF-style cross-check); Sensitivity (at least growth and net retention); Notes (conflict resolutions citing investor_brief.txt) |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| cohort_summary.xlsx | xlsx | Quarterly ARR by customer cohort with logo counts, gross retention, expansion, and churn dollars; 8–10 vintage cohorts across 6–8 quarters | 3 tabs: Cohort Detail, Quarterly Rollup, Definitions | One quarter uses fiscal period labels that do not align with calendar quarters in the brief; one enterprise renewal flagged pending should be excluded from run-rate per brief footnote; expansion dollars duplicated on two rows for same cohort | No implied valuation, no pre-money, no post-round ownership percentages |
| cap_table.csv | csv | Founders, Series A preferred, option pool, two SAFEs, advisor warrants | 25–35 rows | SAFE #1 cap $45M / 20% discount; SAFE #2 cap $55M / no discount; unvested options split across two grants; one warrant tranche partially exercised | No Series B price, no pro forma post-money table |
| investor_brief.txt | txt | Lead investor diligence memo: proposed $28M primary, stated pre-money, target option pool refresh, ARR run-rate claim, multiple comp set, DCF discount-rate range | 2–3 pages | Claims $42.1M ARR run-rate while cohort rollup supports lower TTM; specifies 15% post-money option pool vs cap table lawyer note at 12%; names revenue multiple range but not final price | No finished valuation tab, no dilution percentages, no model formulas |

## Expert Judgment

1. Whether to use TTM ARR, run-rate ARR, or brief-stated ARR for the revenue-multiple bridge, and how to treat the pending enterprise renewal.
2. Which SAFE conversion price applies under the proposed pre-money and whether conversion order matters for fully diluted share count.
3. Option pool refresh sizing (12% vs 15% post-money) and how much dilution falls on founders versus new investors.
4. Whether fiscal-vs-calendar quarter labeling in the cohort file changes trailing growth or net retention used in sensitivity.
5. How to reconcile DCF discount-rate range in the brief with the revenue-multiple cross-check without double-counting optimistic growth.

## Traps / Difficulty

- Cross-file ARR mismatch: brief run-rate vs cohort TTM vs pending-renewal exclusion rule in brief footnote.
- Two SAFE instruments with different cap/discount mechanics converting into the same Series B.
- Option pool refresh stated in brief conflicts with lawyer cap-table comment on available pool.
- Cohort expansion double-count on one vintage row inflates trailing net retention if not deduplicated.
- Model must use live Excel formulas on Cohort Build and Revenue Forecast tabs; hard-coded totals fail review.
- Sensitivity must vary at least net retention and growth assumptions, not decorative labels only.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | valuation_draft.xlsx |
| Series B primary proceeds | $28,000,000 on Cap Table Pro Forma or Assumptions |
| SAFE #1 conversion | Uses $45M cap and 20% discount mechanics per cap_table.csv |
| Pending renewal exclusion | Enterprise renewal excluded from run-rate ARR per investor_brief.txt footnote |
| Post-money pool target | Documents 15% post-money pool per brief vs 12% lawyer note and states chosen treatment |
| Formula integrity | Cohort Build and Revenue Forecast use live formulas referencing source-derived inputs |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| ARR bridge documentation | Notes tab explains TTM vs run-rate choice with cite to brief and cohort file |
| Valuation cross-check | Valuation Summary shows both revenue-multiple and DCF-style outputs that tie to Assumptions |
| Conflict traceability | Each override in Notes cites investor_brief.txt or specific cohort/cap-table row |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Hard-coded revenue or dilution totals on forecast or cap-table tabs | -8 |
| Uses brief ARR run-rate without addressing pending renewal or cohort mismatch | -6 |
| Missing SAFE conversion treatment for either instrument | -5 |

## Strip Test / Batch Diversity

Distinct from `harborview-q1-consolidation`: financial analyst valuation model (not controller consolidation), no FX/acquisition ledger, no multi-entity revenue rollup, occupation 13-2051.00 not 11-3031.01.

Distinct from `sawtooth-july-renewal-desk`: Series B capitalization and securities valuation (not insurance renewal routing), xlsx+cap-table+cohort inputs (not account/location/loss-run desk files), deliverable is `valuation_draft.xlsx` with live formulas (not `renewal_underwriting_review.xlsx` with Quote/Refer/Decline paths).

Opener: CFO/board term-sheet pressure for diagnostics SaaS, not July property renewal or Q1 media consolidation. File mix: xlsx+csv+txt. Scaffold: `live_formula_valuation_model`. Decision structure: ARR bridge, SAFE conversion, pool refresh, valuation cross-check — not four-way underwriting disposition.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file: valuation_draft.xlsx
- [x] Each input file referenced: cohort_summary.xlsx, cap_table.csv, investor_brief.txt
- [x] Live formulas required on cohort and forecast tabs
- [x] SAFE conversion and option pool refresh addressed
- [x] ARR run-rate vs TTM conflict documented
- [x] Sensitivity on growth and net retention
- [x] Notes tab with conflict resolutions citing investor_brief.txt
