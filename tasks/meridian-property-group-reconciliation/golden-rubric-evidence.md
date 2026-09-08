# Golden vs Rubric Evidence — meridian-property-group-reconciliation

Manual verification against `golden/cam_trueup_meridian_commons.xlsx` (CAM true-up redesign).

- [x] **deliverable_filename** (+2): cam_trueup_meridian_commons.xlsx
- [x] **workbook_structure** (+3): Expense Pool, Tenant True-up, Exceptions, Recommendation
- [x] **eligible_cam_pool** (+5): Expense Pool eligible = $412,680
- [x] **roof_capital_excluded** (+4): JE-9001 / SR-4419 classified exclude_capital_roof $186,420
- [x] **hvac_capital_excluded** (+4): JE-9002 classified exclude_capital_hvac $42,850
- [x] **insurance_excluded** (+3): JE-9003 exclude_insurance $118,600
- [x] **duplicate_exp4482** (+4): JE-9006 exclude_duplicate; JE-9005 kept once
- [x] **marketing_pool_exclusion** (+3): marketing excluded from shared pool
- [x] **outfitters_marketing_addon** (+4): T-107 marketing_addon = $6,183 (22.5% × $27,480)
- [x] **ridgeway_cap** (+5): T-104 charged = $13,774
- [x] **contour_expansion** (+5): T-118 H1/H2 alloc at 18.2% / 27.1%
- [x] **contour_trueup** (+4): T-118 true-up ≈ $25,913
- [x] **harbor_credit** (+3): T-101 true-up ≈ −$1,107
- [x] **outfitters_trueup** (+4): T-107 true-up ≈ $25,557
- [x] **lakeside_credit** (+3): T-112 true-up ≈ −$1,405
- [x] **net_trueup** (+4): net ≈ $48,958
- [x] **vacancy_absorption** (+4): Exceptions + alloc logic; Outfitters/Contour absorb
- [x] **prior_billing_source** (+3): prior billed from prior_cam_billing_register.txt
- [x] **exceptions_documented** (+4): Exceptions tab lists all trap treatments
- [x] **pool_sumif_formula** (+3): Expense Pool uses SUMIF on eligible_cam
- [x] **recommendation_invoices** (+4): Recommendation names invoice vs credit tenants
- [x] **bill_roof_as_cam** (−5): Golden excludes roof; recommends not billing as CAM
- [x] **contour_full_year_old_share** (−5): Golden uses mid-year split, not full-year 18.2%
- [x] **ignore_ridgeway_cap** (−4): Golden applies $13,774 cap
- [x] **include_insurance_in_pool** (−3): Golden excludes insurance
