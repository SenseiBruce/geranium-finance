# Golden vs Rubric Evidence

Updated after portal feedback remediation (brand rename + rubric rewrite).

## Positive criteria

- [x] **deliverable_filename** (+2): Workbook named consolidated_review_harborview_media_group.xlsx
- [x] **reporting_period** (+3): Q1 2025 period January 1 through March 31, 2025 on Assumptions
- [x] **cad_rate** (+3): CAD/USD rate 0.74 on Assumptions
- [x] **lattice_proration_factor** (+3): Lattice Digital ownership Feb 1, 2025; proration ~0.6556
- [x] **workbook_structure** (+3): Assumptions, Source_Data, Rollup, Reconciliation_Log, Recommendation sheets
- [x] **total_consolidated** (+5): Total ~$1,590,686.30 on Rollup
- [x] **lattice_consolidated** (+5): Lattice ~$697,267.02 with 65.6% proration
- [x] **cascade_consolidated** (+4): Cascade ~$452,853.28 at 0.74 FX
- [x] **beacon_consolidated** (+3): Beacon ~$440,566.01 full quarter
- [x] **exclusion_log** (+4): Reconciliation_Log documents void/cancelled/out-of-period exclusions
- [x] **fx_source_cited** (+3): cites cascade_creative_fx_and_period_reference.txt
- [x] **acquisition_source_cited** (+3): cites lattice_digital_acquisition_memo.txt
- [x] **judgment_documented** (+4): Reconciliation documents proration and exclusions
- [x] **board_recommendation** (+4): Recommendation after FX, exclusions, Lattice proration
- [x] **rollup_formulas** (+3): Rollup D column uses formulas
- [x] **ledger_source_used** (+3): Totals reconcile to harborview_media_group_brand_ledger.csv

## Negative criteria (golden should NOT trigger)

- [x] **january_lattice_in_total** (-5): Golden excludes pre-Feb-1 Lattice from consolidated total via proration method on gross
- [x] **prior_year_row_in_total** (-4): HM-4001 excluded in Reconciliation_Log
- [x] **april_row_in_total** (-3): HM-3007 excluded in Reconciliation_Log
