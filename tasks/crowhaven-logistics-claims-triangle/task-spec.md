# Task Spec: crowhaven-logistics-claims-triangle

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** crowhaven-logistics-claims-triangle
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Actuaries |
| O*NET Code | 15-2011.00 |
| O*NET Tasks (3–5) | Analyze statistical information to estimate mortality, accident, sickness, disability, and retirement rates.; Design, review, and help administer insurance, annuity and pension plans, determining financial soundness and calculating premiums.; Collaborate with programmers, underwriters, accounts, claims experts, and senior management to help companies develop plans for new lines of business or improvements to existing business.; Determine, or help determine, company policy, and explain complex technical matters to company executives, government officials, shareholders, policyholders, or the public. |
| O*NET Skills (3–5) | Mathematics; Critical Thinking; Reading Comprehension |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Crowhaven Logistics renews its commercial auto and general liability package on 2026-03-01. Actuarial must review financial soundness of the existing program, construct accident-year loss development from the paid triangle, set year-end case and pure IBNR, and explain Quote/Refer/Decline to underwriting for pricing improvements or exit on the existing book. Fully insured primary program — no SI retention.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | claims_reserve_opinion_crowhaven-logistics.xlsx |
| Format | xlsx |
| Required sections/tabs | Accident-year triangle development; case inventory (cleaned); indicated ultimate and pure IBNR; reserve opinion summary; underwriting recommendation |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| crowhaven-logistics_loss_triangle.xlsx | xlsx | Cumulative paid triangle by accident year and development age; line of business tags; definitions with stale mid-year LDFs | 100+ cells across Paid Triangle, AY Summary, Definitions | Stale LDF table; large-loss note pointing to memo; one AY label typo risk | No case inventory; no final IBNR; no booking total |
| crowhaven-logistics_open_claims.csv | csv | Open claim case reserves by claim, AY, line, status | 40+ claim rows | Duplicate claim id; closed claim still Open; large loss; void row; GL vs Auto mix | No LDFs; no ultimates; no IBNR factors |
| actuarial_factor_memo.txt | txt | Governing paid LDFs by age, large-loss IBNR rule, closed-claim rule, target loss ratio for referral | 500–800 words | Supersedes triangle Definitions LDFs; excludes named large loss from triangle IBNR; forbids crediting expected salvage | No finished reserve opinion total |

## Expert Judgment

1. Which paid LDFs govern — memo year-end factors versus stale mid-year factors printed on the triangle Definitions sheet.
2. How to treat CLM-AUTO-2023-4412 (large loss): case held, but excluded from triangle-developed pure IBNR per memo.
3. Whether to keep CLM-AUTO-2024-0908 in case inventory when status is still Open but the claim closed in December.
4. How to resolve the duplicate open-claim row for CLM-GL-2025-0144.
5. How pure IBNR relates to indicated ultimate, cumulative paid, and cleaned case (no double-counting case inside IBNR).
6. Underwriting recommendation for the 2026-03-01 renewal given indicated ultimate loss ratio versus the memo target.

## Traps / Difficulty

- Triangle Definitions still show mid-year LDFs; memo states those are superseded as of 2025-12-15.
- CLM-AUTO-2023-4412 case is material; memo requires holding case but excluding that claim’s AY paid from chain-ladder pure IBNR (develop the rest of the AY, then add large-loss case separately).
- CLM-AUTO-2024-0908 remains Open in the CSV with a residual case after a final payment closed the file — drop from case.
- Duplicate rows for CLM-GL-2025-0144 with conflicting case amounts — keep the higher-confidence / later as-of row per memo tie-break.
- One VOID flagged row must be ignored.
- Fully insured primary program: do not apply a self-insured retention cap (that would invent Pelliston-style SI logic).
- No single file yields indicated ultimate, pure IBNR, and the renewal recommendation.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | claims_reserve_opinion_crowhaven-logistics.xlsx |
| Governing LDFs | memo year-end factors, not Definitions mid-year |
| Cleaned case total | open inventory after drop/duplicate/void rules |
| Indicated ultimate by AY | paid (adjusted) × LDF with large-loss carve-out |
| Pure IBNR | ultimate − paid − cleaned case (floor at 0) by AY / total |
| Total reserve opinion | cleaned case + pure IBNR |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Large-loss documentation | Cites actuarial_factor_memo.txt for excluding CLM-AUTO-2023-4412 from triangle IBNR |
| Factor hierarchy | States memo supersedes triangle Definitions LDFs |
| Renewal recommendation | Compares indicated ultimate LR to memo target and Quote / Refer / Decline accordingly |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends applying the superseded mid-year LDFs from the triangle Definitions sheet | -5 |
| Recommends including CLM-AUTO-2023-4412 paid dollars in chain-ladder pure IBNR contrary to the memo carve-out | -5 |
| Recommends booking a self-insured retention cap on Crowhaven case reserves | -4 |

## Strip Test / Batch Diversity

Skeleton `claims_reserve_triangle`: insured/claims-side paid triangle + open case inventory + actuarial factors → reserve opinion (case vs pure IBNR). Distinct from Pelliston `si_reserve_rollforward` (self-insured retention corridor + controller SI liability), from renewal Quote/Refer desk routing on account/location files, from FX consolidation, valuation, covenant headroom, intercompany settlement, and true-up reconcile (CLOSED).

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Governing LDF hierarchy (memo over Definitions)
- [x] Cleaned case inventory rules
- [x] Large-loss carve-out for triangle IBNR
- [x] Indicated ultimate, pure IBNR, and total reserve opinion
- [x] Underwriting renewal recommendation vs target loss ratio
