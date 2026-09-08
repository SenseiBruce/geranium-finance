# Golden vs Rubric Evidence — whitaker-precision-components-loan-underwriting

Human-verified against inputs, constants, and golden workbook (2026-09-06).
All positive criteria observed in golden; negatives not triggered.

- [x] **deliverable_filename** (+2): The final deliverable is an Excel workbook named loan_underwriting_decision_whitaker-precision-components.xlsx. — golden matches
- [x] **workbook_sections** (+3): The workbook includes an Adjusted EBITDA build, DSCR and leverage tests, a collateral eligibility and LTV analysis, an exception log, and a credit path decision with conditions; equivalent section labels are acceptable. — golden matches
- [x] **memo_hierarchy** (+5): The workbook states that credit_policy_and_exception_memo.txt governs over relationship-manager Approve-as-requested language in whitaker-precision-components_borrower_financials.xlsx. — golden matches
- [x] **reported_ebitda_start** (+3): The Adjusted EBITDA build starts from reported FY2025 EBITDA of approximately $1,248,620.18 from whitaker-precision-components_borrower_financials.xlsx. — golden matches
- [x] **one_time_gain_excluded** (+5): The Adjusted EBITDA build subtracts the FY2025 one-time parcel sale gain of approximately $185,400.00 from reported EBITDA. — golden matches
- [x] **owner_addback_capped** (+5): The Adjusted EBITDA build adds owner compensation of approximately $84,220.55 only, not the larger $210,000.00 relationship-manager claim. — golden matches
- [x] **rent_addback_disallowed** (+4): The Adjusted EBITDA build does not add back the $96,000.00 related-party rent normalization claimed in the borrower package. — golden matches
- [x] **adjusted_ebitda_total** (+5): Adjusted EBITDA equals approximately $1,147,440.73. — golden matches
- [x] **related_party_building_ineligible** (+5): The collateral analysis treats the Whitaker Realty LLC plant building as ineligible collateral for the equipment term loan. — golden matches
- [x] **soft_costs_ineligible** (+4): The collateral analysis treats install, freight, and deposit soft costs as ineligible for advance under the equipment term loan. — golden matches
- [x] **leased_forklift_ineligible** (+3): The collateral analysis treats the leased Toyota forklift as ineligible collateral. — golden matches
- [x] **obsolete_mill_ineligible** (+3): The collateral analysis treats the 1998 Bridgeport manual mill as ineligible under the age cutoff. — golden matches
- [x] **cnc_advance_80** (+4): Eligible new CNC assets are advanced at 80% of appraisal NOLV. — golden matches
- [x] **fixture_advance_50** (+4): Eligible fixtures are advanced at 50% of appraisal NOLV rather than the 70% relationship-manager claim. — golden matches
- [x] **eligible_nolv** (+4): Eligible collateral NOLV totals approximately $2,041,421.53. — golden matches
- [x] **bankable_collateral** (+5): Bankable collateral after policy advance rates equals approximately $1,568,673.10. — golden matches
- [x] **binding_commitment** (+5): The recommended commitment equals approximately $1,531,066.15, the lesser of bankable collateral and 75% of eligible NOLV. — golden matches
- [x] **ltv_full_ask_fails** (+4): LTV at the full requested commitment of $2,847,500.00 exceeds the 75% maximum on eligible NOLV. — golden matches
- [x] **debt_service_factor** (+4): Proposed annual debt service uses the memo factor of $16.42 per $1,000 of commitment per month, annualized. — golden matches
- [x] **existing_ds_used** (+3): DSCR tests include existing bank annual debt service of approximately $412,880.40. — golden matches
- [x] **dscr_full_ask_below_min** (+5): DSCR at the full requested commitment is approximately 1.1781x and below the 1.25x Approve minimum. — golden matches
- [x] **dscr_sized_passes** (+5): DSCR at the recommended commitment is approximately 1.6058x and meets the 1.25x threshold. — golden matches
- [x] **leverage_sized_passes** (+4): Leverage at the recommended commitment is approximately 3.2379x and does not exceed 3.50x. — golden matches
- [x] **path_conditional** (+5): The credit path decision is Approve with conditions, not Approve at the full request and not Decline. — golden matches
- [x] **condition_tenor_60** (+3): Conditions include shortening tenor to 60 months from the requested 84 months. — golden matches
- [x] **condition_personal_guaranty** (+3): Conditions include an unlimited personal guaranty of the principal owner. — golden matches
- [x] **notes_cite_before_rec** (+2): On the Notes section, or equivalent section label, citations to the input filenames and memo rules appear earlier than the committee path recommendation. — golden matches
- [x] **neg_full_ask_approve** (-5): The workbook recommends approving the full requested commitment of $2,847,500.00 despite LTV and DSCR failure at the ask. — golden does not exhibit this prohibited recommendation
- [x] **neg_related_party_collateral** (-5): The workbook recommends treating Whitaker Realty LLC real estate as eligible collateral for the equipment term facility. — golden does not exhibit this prohibited recommendation
- [x] **neg_mgmt_ebitda_dscr** (-5): The workbook recommends measuring DSCR on management EBITDA that retains the one-time parcel gain and the disallowed related-party rent add-back. — golden does not exhibit this prohibited recommendation
- [x] **neg_decline_without_sizing** (-5): The workbook recommends Decline without presenting a sized Approve-with-conditions commitment after the requested amount exceeds bankable collateral. — golden does not exhibit this prohibited recommendation
- [x] **neg_waive_guaranty** (-3): The workbook recommends waiving the personal guaranty on this Conditional-path equipment term loan. — golden does not exhibit this prohibited recommendation

**Self-score:** 100 (all positives met; no negatives triggered).

