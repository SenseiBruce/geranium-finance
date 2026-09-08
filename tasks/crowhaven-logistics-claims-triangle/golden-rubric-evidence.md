# Golden ↔ rubric evidence — crowhaven-logistics-claims-triangle

Human-verified against inputs after generating formula-driven golden.

## Key figures

| Item | Value | Source / method |
|------|------:|-----------------|
| Governing LDFs 12/24/36/48 | 1.82 / 1.41 / 1.18 / 1.06 | actuarial_factor_memo.txt |
| Stale Definitions LDFs (not used) | 1.65 / 1.28 / 1.12 / 1.03 | triangle Definitions DRAFT |
| Gross cum paid AY2022–2025 | 412,840.55 / 628,410.22 / 391,220.18 / 148,640.55 | AY Summary latest diagonal |
| CLM-AUTO-2023-4412 paid / case | 185,220.40 / 142,880.40 | open claims + memo |
| AY2023 attritional paid | 443,189.82 | 628,410.22 − 185,220.40 |
| AY2023 attritional ultimate | 522,963.99 | 443,189.82 × 1.18 |
| AY2024 ultimate | 551,620.45 | 391,220.18 × 1.41 |
| AY2025 ultimate | 270,525.80 | 148,640.55 × 1.82 |
| AY2022 ultimate | 437,610.98 | 412,840.55 × 1.06 |
| Dropped closed / VOID / dup | CLM-AUTO-2024-0908; CLM-AUTO-2024-0000; older CLM-GL-2025-0144 | inventory rules |
| Dup kept case | 19,850.55 | later as_of 2025-12-28 |
| Cleaned case total | 460,089.00 | SUM retained case |
| Pure IBNR total | 94,892.67 | Σ max(0, ult − paid − attr case) |
| Total reserve opinion | 554,981.67 | case + pure IBNR |
| Total indicated ultimate | 2,110,822.02 | attr ultimates + LL paid+case |
| Earned premium | 2,850,220.40 | memo |
| Indicated LR | 74.06% | ultimate / premium |
| Recommendation | Refer | LR > 68.5% target; < 85% decline |

## Pure IBNR by AY

| AY | Attr ult | Attr paid | Attr case | Pure IBNR |
|----|--------:|---------:|----------:|----------:|
| 2022 | 437,610.98 | 412,840.55 | 23,803.35 | 967.08 |
| 2023 | 522,963.99 | 443,189.82 | 51,683.95 | 28,090.22 |
| 2024 | 551,620.45 | 391,220.18 | 94,564.90 | 65,835.37 |
| 2025 | 270,525.80 | 148,640.55 | 147,156.40 | 0.00 |
| **Total** | | | | **94,892.67** |

## Checklist

- [x] Deliverable filename matches prompt
- [x] Every rigid dollar/factor above traced to inputs or memo
- [x] Criterion section_reserve_summary includes answer keys: case ~$460,089.00 / pure IBNR ~$94,892.67 / total ~$554,981.67
- [x] Structure split: case inventory / AY development / reserve summary / UW recommendation (atomic)
- [x] One Refer positive (recommendation_refer) with 74.06% + memo thresholds — not triple-counted
- [x] Two negatives: (1) wrong Quote/Decline disposition in refer band; (2) applying DRAFT LDFs over memo (distinct method prohibition)
- [x] No golden.zip layout criteria
- [x] UW Recommendation B5 visibly states `Refer`; B11 rationale cites memo thresholds + indicated LR
- [x] Reserve Opinion B5–B10: Cleaned Case / Pure IBNR / Total Reserve / Indicated Ultimate / Earned Premium / Ultimate LR
- [x] Case Inventory H5:H45 true Excel dates; freeze A5 + filter A4:P45; duplicate MAXIFS keeps latest as_of
- [x] Case Inventory `as_of_date` (H) stored as Excel date serials (not text); strip-cache MAXIFS recalc → cleaned case $460,089
- [x] Criteria remain atomic (inventory / AY / reserve / UW / LR / recommendation)

## Formula audit

- Case Inventory: `as_of_date` true dates; include = not VOID/closed and `H = MAXIFS(H:H, claim)`; SUM of cleaned case column
- AY Development: attr paid = gross − LL carve; ultimate = ROUND(attr×LDF,2); pure IBNR = MAX(0, ROUND(ult−paid−case,2))
- Reserve Opinion: linked totals from AY Development; LR = ultimate / premium
- UW Recommendation: B5 literal `Refer`; B9 formula tie-out =IF(LR>decline,"Decline",IF(LR>refer,"Refer","Quote")); B11 rationale `74.06% > 68.5% refer threshold and < 85.0% decline threshold.`
- Reserve Opinion: compact Item/Amount labels (Cleaned Case, Pure IBNR, Total Reserve, Indicated Ultimate, Ultimate LR)
- Case Inventory: Excel date serials in H; include/disposition formulas; cleaned case L46 = $460,089.00 after fresh recalc
- Negatives: one disposition prohibition (Quote or Decline in refer band) + one method prohibition (DRAFT LDFs) — recommendation not scored three times
- Verified after regenerate + formulas strip-cache recalculation + Python mirror: cleaned case 460089, pure IBNR 94892.67, total reserve 554981.67, ultimate 2110822.02, LR 74.06%, Refer; CLM-GL-2025-0144 keeps 2025-12-28 $19,850.55 (K42=TRUE, K41=FALSE); text-date control yields L46=$0
