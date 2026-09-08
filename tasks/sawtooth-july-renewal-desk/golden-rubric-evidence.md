# Golden vs Rubric Evidence — sawtooth-july-renewal-desk

Manual verification against `golden/renewal_underwriting_review.xlsx`.

- [x] **deliverable_filename** (+2): Workbook named renewal_underwriting_review.xlsx.
- [x] **accounts_reviewed_count** (+3): Account_Routing lists 38 accounts.
- [x] **workbook_structure** (+3): Account_Routing, Location_Exceptions, Loss_Reconciliation, Rules_Citations, Summary present.
- [x] **si1015_quote** (+3): SI-1015 disposition Quote.
- [x] **si1021_refer** (+4): SI-1021 disposition Refer with TIV variance rationale.
- [x] **si1042_refer** (+5): SI-1042 disposition Refer.
- [x] **si1088_refer** (+5): SI-1088 disposition Refer for pending_roof_po.
- [x] **si1156_decline** (+5): SI-1156 disposition Decline.
- [x] **si1033_ask_broker** (+4): SI-1033 disposition Ask Broker.
- [x] **coastal_endorsement_flags** (+4): Four CW-1/CW-2 locations on Location_Exceptions.
- [x] **rules_source_cited** (+3): Rules_Citations cites underwriting_rules_notes.txt.
- [x] **loss_run_reconciliation** (+4): Loss_Reconciliation lists accounts with >5 pt LR delta.
- [x] **si1156_recomputed_lr** (+3): SI-1156 recomputed LR 95.8% on Account_Routing.
- [x] **si1042_location_incurred** (+3): ORL-1042-B incurred $278,400 in loss analysis rationale.
- [x] **summary_quote_count** (+3): Summary COUNTIF shows 28 Quote.
- [x] **summary_refer_count** (+3): Summary COUNTIF shows 7 Refer.
- [x] **routing_rationale** (+4): Non-Quote rows include rule-based rationale.
- [x] **summary_formulas** (+3): Summary uses COUNTIF formulas on Account_Routing.
- [x] **cat_loss_in_attritional** (-5): Golden excludes CAT-2419 from SI-1075 attritional LR.
- [x] **incomplete_account_list** (-5): Golden routes all 38 accounts.
- [x] **stale_list_ratio_si1042** (-3): Golden assigns SI-1042 Refer, not Quote from stale list ratio.
