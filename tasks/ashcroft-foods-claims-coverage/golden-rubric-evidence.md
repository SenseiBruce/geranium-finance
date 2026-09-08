# Golden ↔ Rubric Evidence — ashcroft-foods-claims-coverage

Generated for Core-difficulty revision. All numeric keys unchanged from prior golden.

| Criterion ID | Golden location | Evidence |
|---|---|---|
| deliverable_filename | workbook name | `claim_coverage_opinion_ashcroft-foods.xlsx` |
| workbook_sections | sheet list | Coverage Decision Tree, Evidence & Rule Matrix, Maintenance Timeline, Inventory Audit Trail, Reserve Bridge, Pure vs Case, Scenario Checks, Decision Trace, Consistency Checks, File Recommendation |
| coverage_decision_tree | Coverage Decision Tree!A3:I7 | 8-stage columns for stock/equipment/BI/packaging |
| evidence_matrix | Evidence & Rule Matrix!A3:H12 | Valuation, deductible, equipment footing/treatment, BI, maintenance |
| stock_partial_accept | Coverage Decision Tree!H4 | Accept — Partial |
| equipment_deny | Coverage Decision Tree!H5 | Deny |
| bi_deny | Coverage Decision Tree!H6 | Deny; 14h vs 72h |
| overall_partial | Coverage Decision Tree!B9 | Partial Coverage |
| valuation_reconciliation | Valuation Reconciliation!A4:E5 | Selling price rejected; invoice governing; E5→254317.96 |
| active_vs_superseded_deductible | Evidence & Rule Matrix rows B; Reserve Bridge!C13 | Active 5000; superseded 10000 non-governing |
| packaging_excluded | Inventory Audit Trail PKG-991 | Exclude |
| void_excluded | Inventory Audit Trail LOT-B-099 | Exclude |
| duplicate_excluded | Inventory Audit Trail LOT-B-218-DUP | Exclude |
| inventory_audit_trail | Inventory Audit Trail!A3:J12 + totals | Pipeline columns + separate totals |
| inventory_control_check | Inventory Audit Trail control row | PASS |
| covered_stock_cost | Inventory Audit Trail eligible total / Reserve Bridge!C8 | 254317.96 |
| salvage_credit | Reserve Bridge!C10 | 12629.82 |
| maintenance_timeline | Maintenance Timeline!A4:D16 | Dates, elapsed 98, OEM 90, grace 7, cancel window, factor |
| coinsurance_75 | Maintenance Timeline!B16 | 0.75 |
| oem_sensitivity_table | Maintenance Timeline!A19:H22 | Source 90 / short 80 / long 100 |
| equipment_footing_documented | Denied Items!A4:D12 | 84517.60 vs 82517.60 variance 2000 |
| reserve_bridge | Reserve Bridge!A4:D14 | Full chain to C14 |
| case_reserve_amount | Reserve Bridge!C14 / File Recommendation!B12 | 176266.11 |
| pure_vs_case | Pure vs Case!A4:C8 | Case only; pure IBNR 0; PASS |
| scenario_checks | Scenario Checks!A6:F10 | S1–S5 counterfactuals marked No |
| decision_trace | Decision Trace!A4:F10 + B12 | Seven decisions + reserve link |
| consistency_checks | Consistency Checks!A4:C10 | Seven PASS checks |
| formula_linkage | Reserve Bridge formulas | C8←audit trail; C12←timeline B16; C14=C12-C13 |
| alae_separate | ALAE!B9:B11 | Expense separate; PASS |
| committee_recommendation | File Recommendation!A4:C9 + B12 | Six elements + linked reserve |
| memo_over_field_note | Evidence & Rule Matrix / Decision Tree | Memo > N-01 |
| endorsement_vs_exclusion | Coverage Decision Tree stock vs equipment rows | Spoilage vs Mechanical Breakdown |
| negatives | File Recommendation + Scenario Checks | Actual conclusions reject equipment pay, sell-price pay, BI reserve, full coverage, counterfactual-as-actual |

## Unchanged numeric answers
- Covered stock 254317.96; salvage 12629.82; coinsurance 75%; deductible 5000; reserve 176266.11
- Equipment footing 82517.60; BI 14h < 72h; OEM 90; elapsed 98; grace threshold 97; vendor-cancel 8d ≤ 14d
