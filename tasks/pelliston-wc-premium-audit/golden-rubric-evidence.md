# Golden ↔ rubric evidence — pelliston-wc-premium-audit

Generated after methodology correction (Triangle cumulative paid for IBNR base; formula-driven workpaper).

## Key figures

| Item | Value | Source |
|------|------:|--------|
| SI case total | $745,064.55 | Case Inventory SUM of retention-capped SI case |
| Excess CLM-2024-1187 | $62,800.00 | MAX(0, 412800 − 350000) |
| IBNR AY2022 | $6,678.05 | (136220.55 + 30730.58) × 0.04 |
| IBNR AY2023 | $30,861.78 | (172640.55 + 107921.13) × 0.11 |
| IBNR AY2024 | $176,876.31 | (186420.18 + 445280.91) × 0.28 |
| IBNR AY2025 | $119,263.21 | (68220.40 + 161131.93) × 0.52 |
| Total IBNR | $333,679.35 | Sum of AY IBNR |
| Beginning reserve | $1,842,660.40 | actuarial_funding_memo.txt |
| Net paid 2025 | $600,226.54 | Ledger (voids net) |
| Ending SI reserve | $1,078,743.90 | Case + IBNR |
| Net incurred plug | −$163,689.96 | Ending − Beginning + Paid |

## Methodology change vs prior gold

Prior gold used Open Inventory open-claim `paid_to_date` for every AY IBNR base. Corrected gold uses AY Triangle `cumulative_paid_as_of_2025_12` for cumulative paid (memo: full AY population including closed claims). SI case still from Open Inventory after retention caps / CLM-2024-0901 removal.

AY2024 conflict documented on Notes: OI open paid excl. CLM-2024-0901 = $196,993.24 vs Triangle = $186,420.18 (delta $10,573.06). Triangle selected; no invented bridge.

## Formula audit

- Assumptions: central retention, beginning reserve, AY factors
- Case Inventory: `SI = IF(closed,0,MIN(TPA, retention))`; excess formula-driven
- IBNR: base = Triangle paid + SUMIF SI case; IBNR = ROUND(base × factor, 2)
- Excess Bridge / Rollforward / Recommendation: linked formulas

## Rubric delta (portal)

Update criteria that cite old IBNR/ending amounts:

- `ibnr_total`: ~$332,357 → ~$333,679
- `ibnr_2025_amount`: ~$119,233 → ~$119,263
- `ending_reserve` / `controller_book_amount`: ~$1,077,422 → ~$1,078,744
- Add `ibnr_paid_from_triangle` and `ay2024_conflict_documented`
- Strengthen `live_formulas` for MIN / base×factor
