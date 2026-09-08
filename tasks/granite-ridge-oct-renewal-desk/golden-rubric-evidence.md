# Golden vs Rubric Evidence — granite-ridge-oct-renewal-desk

Manual verification against `golden/renewal_underwriting_review.xlsx` after GR-2047 Quote correction (Section 6 literal reading; invented occ≥93 threshold removed), removal of redundant full_routing_table_consistency, and split of Campus Edge appetite criteria.

- [x] **deliverable_filename** (+2): Workbook named renewal_underwriting_review.xlsx.
- [x] **routing_completeness** (+3): All 36 accounts have exactly one of Quote/Refer/Decline/Ask Broker.
- [x] **location_exceptions_present** (+2): Clearly labeled Location_Exceptions section present and usable (structural only; specific flags scored elsewhere).
- [x] **loss_reconciliation_present** (+2): Clearly labeled Loss_Reconciliation section presents reconciliation framework (structural only; detailed ratios scored elsewhere).
- [x] **disposition_summary_present** (+2): Summary counts Quote/Refer/Decline/Ask Broker.
- [x] **gr2018_quote** (+3): GR-2018 disposition Quote.
- [x] **gr2047_quote** (+4): GR-2047 disposition Quote; occupancy 94.0% does not imply full occupancy under Section 6; HAB-2047-B broker_confirmation=yes.
- [x] **gr2089_refer** (+5): GR-2089 disposition Refer for expired sprinkler inspection.
- [x] **gr2113_refer** (+4): GR-2113 disposition Refer for unit count and TIV variance; Location_Exceptions TIV detail shows variance +$970,880.
- [x] **gr2162_refer** (+5): GR-2162 Refer with LR 67.5% ($265,360 / $392,850) and HAB-2162-C incurred $260,120 under Section 3.
- [x] **gr2074_refer_pool** (+4): GR-2074 Refer because HAB-2074-A pending_fence_po under Section 5.
- [x] **gr2195_decline** (+5): GR-2195 disposition Decline.
- [x] **gr2033_ask_broker** (+4): GR-2033 disposition Ask Broker.
- [x] **gr2007_refer_appetite** (+3): GR-2007 Refer with Section 10 GRP-APPETITE rationale; Location_Exceptions includes Section 10 appetite note for GR-2007 (sole criterion scoring the appetite-note documentation).
- [x] **gr2065_refer_appetite** (+2): GR-2065 Refer for Section 10 GRP-APPETITE review before bind (routing disposition only; Location Exceptions note scored on gr2007_refer_appetite).
- [x] **subsidized_endorsement_flags** (+4): Three subsidized locations on Location_Exceptions.
- [x] **rules_source_cited** (+3): Rules_Citations cites granite_ridge_routing_notes.txt.
- [x] **loss_run_reconciliation** (+4): Loss_Reconciliation lists accounts with >5 pt LR delta.
- [x] **loss_run_controls_routing** (+4): Routing uses recomputed loss-run LR as controlling metric when delta >5 (e.g. GR-2195 Decline on 292.3%).
- [x] **gr2195_recomputed_lr** (+3): GR-2195 recomputed LR 292.3% on Account_Routing ($142,100 / $48,620).
- [x] **summary_quote_count** (+3): Summary COUNTIF shows 25 Quote.
- [x] **summary_refer_count** (+3): Summary COUNTIF shows 9 Refer.
- [x] **summary_decline_ask_broker_counts** (+3): Summary shows 1 Decline, 1 Ask Broker, 36 total.
- [x] **routing_rationale** (+4): Non-Quote rows include rule-based rationale citing source files.
- [x] **summary_formulas** (+3): Summary uses COUNTIF/COUNTA formulas on Account_Routing.
- [x] **cat_loss_excluded_attritional** (+3): Golden excludes CAT-2408 from GR-2071 attritional LR (9.6% Quote).
- [x] **gr2071_section9_rationale** (+3): GR-2071 rationale cites Section 9 for CAT-2408 exclusion.
- [x] **false_cat_exclusion_rationale** (-5): Golden only cites Section 9 cat exclusion for GR-2071 (CAT-2408).
- [x] **false_quote_gr2195_decline_lr** (-5): Golden assigns Decline (not Quote) to GR-2195 on 292.3% LR.
- [x] **false_appetite_clearance** (-5): Golden does not claim GRP-APPETITE clearance already obtained.
- [x] **false_broker_confirmation** (-5): Golden does not claim broker confirmation on file for HAB-2033-B (broker_confirmation=no).

Removed: **full_routing_table_consistency** (redundant with account-level routing criteria and summary counts).
Counts reconcile: 25 + 9 + 1 + 1 = 36.
