# Task Spec: pelliston-wc-premium-audit

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.
> Attempt 2 — self-insured WC reserve rollforward (replaces premium-audit true-up rejected for uniqueness).

## Decision

- **Status:** GO
- **Seed ID:** pelliston-wc-premium-audit
- **Attempt:** 2

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (3–5) | Handle all aspects of employee insurance, benefits, and casualty programs, including monitoring changes in health insurance regulations and creating budgets for benefits and worker's compensation.; Conduct or coordinate audits of company accounts and financial transactions to ensure compliance with state and federal requirements and statutes.; Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed |
| O*NET Skills (3–5) | Mathematics; Critical Thinking; Reading Comprehension |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Pelliston Machine Works carries a $350,000 per-occurrence self-insured retention on Ohio workers' compensation and books the SI liability for year-end. External audit and the bank's borrowing-base certificate both need Controllers' 2025-12-31 reserve number by Thursday. TPA payments hit a claims ledger all year, open claims and an accident-year payment triangle sit in a separate workbook, and the consulting actuary sent a funding memo with IBNR factors, retention treatment, and a subrogation rule. Getting the SI reserve wrong either understates liabilities on the certificate or locks excess cash in the trust that operations needs for the Holt Tooling integration.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | self_insured_wc_reserve_pelliston.xlsx |
| Format | xlsx |
| Required sections/tabs | Case reserve inventory (retention-capped); accident-year IBNR; reserve rollforward; excess/ceded bridge; controller recommendation |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| pelliston_claims_payment_ledger.csv | csv | 2025 and prior claim indemnity/medical payments by claim and accident year | 80+ payment rows | Partial payments on large loss; recovery coded as negative payment; duplicate check void | No ending reserve; no IBNR |
| pelliston_open_claims_triangle.xlsx | xlsx | Open claim inventory with case reserves + cumulative paid triangle by accident year | 3 sheets: Open Inventory, AY Triangle, Definitions | Large-loss case above retention; subrogation flag; one closed claim still listed open | No IBNR factors; no rollforward |
| actuarial_funding_memo.txt | txt | Year-end funding memo: retention, IBNR factors by AY, subrogation cash rule, stale mid-year factor warning | 500–800 words | Confirms 0.52 for 2025 not 0.40; caps SI at retention; forbids booking expected subro | No finished reserve total |

## Expert Judgment

1. Which open-claim case reserves stay on the SI books versus excess above the $350,000 retention.
2. How to treat CLM-2024-1187 when case plus paid already exceed retention.
3. Whether to reduce reserves for expected subrogation on CLM-2023-0442 before cash is received.
4. Which IBNR factor applies to each accident year (including rejecting the stale mid-year 2025 factor).
5. How paid activity in the ledger ties into the rollforward with beginning reserve from the memo.
6. Controller recommendation for the audited SI liability and what to tell the bank certificate pack.

## Traps / Difficulty

- CLM-2024-1187 case reserve $412,800 exceeds $350,000 retention — SI case must be capped; excess is carrier.
- Expected subrogation $64,250 on CLM-2023-0442 is not cash — memo forbids crediting until received.
- One claim still marked Open in inventory was closed in December per ledger final payment — drop from case inventory.
- 2025 IBNR factor 0.52 governs; a mid-year exhibit showing 0.40 is explicitly superseded.
- Negative payment rows that are voids vs true recoveries need different treatment per Definitions tab.
- Beginning reserve $1,842,660.40 is only in the actuarial memo, not in the triangle.
- No file alone yields ending SI reserve; cross-file build required.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | self_insured_wc_reserve_pelliston.xlsx |
| SI case reserves after retention caps | approximate from open inventory |
| IBNR by accident year | using memo factors 0.04 / 0.11 / 0.28 / 0.52 |
| Ending SI reserve | case (capped) + IBNR |
| Rollforward | beginning + incurred − paid = ending |
| Large-loss SI case | capped at $350,000 retention |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Retention documentation | Cites actuarial_funding_memo.txt for $350,000 cap on CLM-2024-1187 |
| Subrogation treatment | Does not credit expected recovery before cash |
| Controller recommendation | States ending SI liability for audit/bank pack and flags excess carrier recoverable |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends booking expected subrogation as a reserve credit before cash receipt | -5 |
| Recommends carrying CLM-2024-1187 case at the full uncapped $412,800 on the SI books | -5 |
| Recommends applying the superseded 0.40 factor to accident year 2025 IBNR | -4 |

## Strip Test / Batch Diversity

Attempt 2 after portal Uniqueness FAIL on workers' comp **premium audit true-up** (estimate vs audited premium), which stripped too close to Meridian's reconcile-and-true-up skeleton. New scaffold `self_insured_wc_reserve_rollforward`: case inventory + retention corridor + AY IBNR factors + liability rollforward for a self-insured retention — not premium billing, not CAM leases, not FX consolidation, not renewal Quote/Refer, not cap-table valuation.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Retention-capped case reserves
- [x] Accident-year IBNR using memo factors
- [x] Reserve rollforward to 2025-12-31
- [x] Controller recommendation for audit / bank certificate
