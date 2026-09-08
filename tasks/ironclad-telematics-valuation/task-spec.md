# Task Spec: ironclad-telematics-valuation

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** ironclad-telematics-valuation
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

Ironclad Telematics is a Chicago-based fleet SaaS company selling connected-vehicle subscriptions to regional trucking fleets and municipal transit agencies. The CFO is prepping a growth-equity term sheet for Thursday's board packet and needs a single valuation workbook that the lead sponsor and outside counsel can defend.

Finance exported a fleet ARR cohort workbook, counsel sent a cap-table CSV with two convertible notes still outstanding, and the sponsor's diligence brief states a primary raise, a pre-money, a post-money option-pool target, and an ARR run-rate claim that does not match the cohort rollup. The model has to convert the notes correctly, size the pool refresh, bridge fleet ARR into a forward view with live formulas, and document every override against the diligence brief.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | ironclad_telematics_valuation.xlsx |
| Format | xlsx |
| Required sections/tabs | Assumptions (documented overrides); Fleet Cohort Build (live retention/expansion from ironclad_fleet_cohort_arr.xlsx); Revenue Forecast (formula-driven, not hard-coded totals); Cap Table Pro Forma (pre- and post-money with convertible note conversion); Valuation Summary (revenue-multiple and DCF-style cross-check); Sensitivity (at least fleet growth and net retention); Notes (conflict resolutions citing growth_equity_diligence_brief.txt) |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| ironclad_fleet_cohort_arr.xlsx | xlsx | Monthly/quarterly ARR by fleet cohort with unit counts (vehicles), gross retention, expansion, and churn; 8–12 vintage cohorts across 6–8 periods | 3 tabs: Cohort Detail, Fleet Rollup, Definitions | One municipal pilot tagged "pilot_non_recurring" must be excluded from run-rate per brief footnote; one fleet expansion row duplicated across two cohort IDs; fiscal-month labels in one tab vs calendar quarters in the brief | No implied valuation, no pre-money, no post-round ownership percentages |
| ironclad_cap_table.csv | csv | Founders, Series Seed preferred, employee option pool, two convertible notes, advisor warrants | 28–40 rows | Note A: $4.2M principal, $50M cap, 20% discount; Note B: $2.8M principal, $65M cap, no discount; unvested options across two grant vintages; one warrant tranche partially exercised | No growth-equity price, no pro forma post-money table |
| growth_equity_diligence_brief.txt | txt | Lead sponsor diligence memo: proposed primary raise, stated pre-money, target post-money option pool, ARR run-rate claim, revenue-multiple comps, DCF discount-rate range, note conversion order preference | 2–3 pages | Claims higher ARR run-rate than cohort TTM; specifies 12% post-money pool vs counsel email note in cap-table header of 10% available; prefers Note A converts before Note B; names multiple range but not final price | No finished valuation tab, no dilution percentages, no model formulas |

## Expert Judgment

1. Whether to use TTM fleet ARR, run-rate ARR, or brief-stated ARR for the revenue-multiple bridge, and how to treat the municipal pilot exclusion.
2. Convertible note conversion prices under the proposed pre-money (cap vs discount for Note A; cap-only for Note B) and whether conversion order changes fully diluted share count.
3. Option pool refresh sizing (10% available vs 12% post-money target) and who absorbs the dilution.
4. Whether fiscal-vs-calendar period labeling in the cohort file changes trailing growth or net retention used in sensitivity.
5. How to reconcile the brief's DCF discount-rate range with the revenue-multiple cross-check without double-counting optimistic fleet growth.

## Traps / Difficulty

- Cross-file ARR mismatch: brief run-rate vs cohort TTM vs pilot_non_recurring exclusion rule.
- Two convertible notes with different cap/discount mechanics converting into the same growth-equity round.
- Option pool refresh in the brief conflicts with counsel's available-pool note on the cap-table extract.
- Duplicate expansion dollars across two cohort IDs inflate trailing net retention if not deduplicated.
- Model must use live Excel formulas on Fleet Cohort Build and Revenue Forecast tabs; hard-coded totals fail review.
- Sensitivity must vary at least net retention and fleet growth, not decorative labels only.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | ironclad_telematics_valuation.xlsx |
| Growth-equity primary proceeds | Stated primary amount from growth_equity_diligence_brief.txt on Cap Table Pro Forma or Assumptions |
| Note A conversion | Uses $50M cap and 20% discount mechanics per ironclad_cap_table.csv |
| Note B conversion | Uses $65M cap / no-discount mechanics per ironclad_cap_table.csv |
| Pilot exclusion | Municipal pilot excluded from run-rate ARR per brief footnote |
| Post-money pool target | Documents 12% post-money pool per brief vs 10% counsel note and states chosen treatment |
| Formula integrity | Fleet Cohort Build and Revenue Forecast use live formulas referencing source-derived inputs |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| ARR bridge documentation | Notes tab explains TTM vs run-rate choice with cite to brief and cohort file |
| Valuation cross-check | Valuation Summary shows both revenue-multiple and DCF-style outputs that tie to Assumptions |
| Conflict traceability | Each override in Notes cites growth_equity_diligence_brief.txt or specific cohort/cap-table row |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends closing the round without converting either outstanding note | -8 |
| Hard-codes revenue or dilution totals on forecast or cap-table tabs | -6 |
| Uses brief ARR run-rate without addressing pilot exclusion or cohort mismatch | -5 |

## Strip Test / Batch Diversity

Distinct from `helix-biotech-valuation`: growth-equity prep for fleet telematics SaaS (not Series B lab-informatics), convertible notes (not SAFEs), entity-prefixed input filenames, deliverable `ironclad_telematics_valuation.xlsx` (not `valuation_draft.xlsx`), topology centers on fleet ARR cohorts + note stack + pool refresh.

Distinct from `harborview-q1-consolidation` / `vesper-culinary-brands-consolidation`: analyst valuation model, not controller multi-entity FX consolidation.

Distinct from `sawtooth-july-renewal-desk` / `granite-ridge-oct-renewal-desk`: securities valuation with live formulas, not insurance Quote/Refer/Decline routing.

Distinct from `meridian-property-group-reconciliation`: not CAM true-up / lease-cap reconciliation.

Opener: growth-equity board-packet pressure for fleet SaaS. File mix: xlsx+csv+txt with Ironclad-specific names. Scaffold: `growth_equity_fleet_note_stack_valuation` (distinct from Helix Series B SAFE scaffold).

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file: ironclad_telematics_valuation.xlsx
- [x] Each input file referenced: ironclad_fleet_cohort_arr.xlsx, ironclad_cap_table.csv, growth_equity_diligence_brief.txt
- [x] Live formulas required on cohort and forecast tabs
- [x] Convertible note conversion and option pool refresh addressed
- [x] ARR run-rate vs TTM conflict documented
- [x] Sensitivity on fleet growth and net retention
- [x] Notes tab with conflict resolutions citing growth_equity_diligence_brief.txt
