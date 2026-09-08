# Golden ↔ rubric evidence — vesper-culinary-brands-consolidation

Human verification that the golden workbook satisfies every positive criterion and fires no negative.

- [x] **deliverable_filename** (+2): `golden/consolidated_review_vesper_culinary_brands.xlsx`.
- [x] **reporting_period** (+3): Assumptions / title block state Q3 2025 (July 1–September 30, 2025) and as-of early October 2025.
- [x] **eur_usd_rate** (+4): Assumptions EUR/USD = 1.0874.
- [x] **kiln_ownership_start** (+3): Assumptions ownership start (modeling date) = 2025-08-12; modeling basis labeled “August 12, 2025 — per acquisition memo”; supporting evidence status states not independently confirmed from Schedule 2.1 / bank wire.
- [x] **kiln_method_and_approval** (+4): Selected final = 50/92 from kiln_spice_acquisition_memo.txt; cutoff identified as Conditional transaction-date cutoff scenario; Approval evidence in supplied packet: not present.
- [x] **kiln_open_followups** (+3): Notes Open Follow-Up Items table + Assumptions/Kiln_Audit Ownership Date Evidence Status and Post-Close Billing Support fields document Schedule 2.1 / bank wire and shipment/service support as open because records are not in the packet.
- [x] **workbook_structure** (+2): Assumptions, line inventory, brand rollup, Kiln audit, Reconciliation, Notes, Recommendation (or equivalent).
- [x] **reconciliation_bridge** (+4): Reconciliation sheet bridges raw extract gross by brand through void/cancelled, duplicate, period, and Kiln 50/92 ownership adjustment to adjusted board amounts ($565,717.81 / $644,106.78 / $339,572.04 / $1,549,396.63) with PASS controls tying to the brand-level rollup; D12/F12/D13 live-linked.
- [x] **total_consolidated_final** (+5): Brand-level selected-final total = 1,549,396.63; Case 2 total 1,634,434.29 labeled Conditional transaction-date cutoff scenario.
- [x] **hearth_consolidated** (+4): 565,717.81 after status/period exclusions.
- [x] **brine_consolidated** (+5): 644,106.78 at 1.0874 sum-then-round.
- [x] **kiln_consolidated_final** (+5): Selected-final Kiln 339,572.04 under 50/92; cutoff 424,609.70 shown as conditional only.
- [x] **exclusion_log** (+4): Reconciliation lists void/cancelled/duplicate/out_of_period rows with formula-driven USD_Impact for EUR lines.
- [x] **prior_period_exclusion** (+3): June 2025 Hearth catch-up excluded.
- [x] **fx_source_cited** (+3): Notes cites brine_barrel_fx_and_period_reference.txt.
- [x] **acquisition_source_cited** (+3): Notes cites kiln_spice_acquisition_memo.txt and attributes 50/92 to that memo.
- [x] **ledger_source_used** (+3): Line_Detail / Kiln_Audit tied to vesper_culinary_brands_brand_ledger.csv.
- [x] **rollup_formulas** (+3): Brand rollup chain Line_Detail → Reconciliation!D12/F12/D13 → brand rollup; Case comparison formula-driven; bridge and exclusion USD_Impact formulas.
- [x] **judgment_documented** (+3): Notes/Assumptions document selecting 1.0874 and rejecting the 1.1025 spot aside.
- [x] **board_recommendation_final** (+4): Recommendation states selected-final ~$1,549,396.63; cutoff not presented as unqualified final.
- [x] **board_recommendation_kiln_ownership** (+3): Recommendation states 50/92 Kiln treatment from kiln_spice_acquisition_memo.txt; no full unprorated pre-ownership Kiln.
- [x] **presentation_no_cell_refs** (+2): Board note uses amounts/method text, not cell addresses.
- [x] Negatives do not fire: no spot-overrides-bulletin instruction, no sales-ops full-quarter Kiln adoption, no fabricated cutoff approval as final.

## Cutoff math (ledger clean-room)

Post-close posted Kiln: **424,609.70**  
Hearth 565,717.81 + Brine 644,106.78 + Kiln cutoff 424,609.70 = **1,634,434.29** (conditional only)  
Selected final: Hearth + Brine + Kiln 50/92 **339,572.04** = **1,549,396.63**
