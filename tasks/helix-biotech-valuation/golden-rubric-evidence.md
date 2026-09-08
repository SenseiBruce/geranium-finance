Manual verification against `golden/valuation_draft.xlsx` (2026-09-08 final acceptance: whole-share ROUND, individual-holder ownership, professional input/formula formatting).

## Positive criteria (spot-check)

- [x] **series_a_price** (+3): Forsyth Equity Series A Preferred at $1.82/share, 6,500,000 shares (Assumptions B15–B16). Not Hartwell Partners.
- [x] **model_arr_base** (+5): Eight retained 2024 ending_arr rows → SUMIFS quarters → TTM $40,359,060.40 − Apex $2,252,680 = $38,106,380.40; feeds Revenue Forecast.
- [x] **cohort_live_formulas** (+4): ending_arr and quarterly totals are formulas; duplicate row include_flag=0.
- [x] **duplicate_expansion_excluded** (+3): FY2023-Q2 duplicate present in inventory, marked EXCLUDED, omitted from SUMIFS.
- [x] **sensitivity_table** (+4): Y1 ARR matrix uses same identity as Forecast (TTM × stress × (1+growth)); EV = Y1 × 6.1x; center = $297,534,618.15.
- [x] **safe_vesper_conversion** (+5): Cap price ≈$2.6745 < discounted Series B ≈$5.3252 → ROUND = 934,756 whole shares; MFN labeled outstanding (not cleared).
- [x] **safe_quorum_conversion** (+5): ROUND = 535,360 whole shares.
- [x] **post_money_fd_shares** (+4): 24,188,372 after whole-share SAFE + 15% pool refresh ROUND = 1,686,256.
- [x] **cap_table_ownership** (+5): Individual holders from cap_table.csv (no Founders & Employees rollup); Forsyth post-round 8,125,000 ≈ 33.5905%.
- [x] Retention definition documented: ending = start×GR%/100 + expansion − churn (GR before churn; no double-count).

## Negatives

- [x] No false MFN-cleared / no-better-terms claim (negative criterion only; positive MFN mirror removed).
- [x] No unsupported Hartwell Partners Series A attribution.

## Package

- Input integrity fail-closed in `tests/check_outputs.py` + `tests/test.sh`.
- Deliverable gated on exact `valuation_draft.xlsx` (no golden-only sheet-name gate).
- `task.toml` has sector / occupation / occupation_code / difficulty_tier.
