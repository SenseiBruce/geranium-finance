# Task Spec: northline-industrial-holdings-intercompany

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.
> Attempt 2 after portal Uniqueness FAIL on covenant headroom scaffold (CLOSED).

## Decision

- **Status:** GO
- **Seed ID:** northline-industrial-holdings-intercompany
- **Attempt:** 2

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (3–5) | Monitor financial activities and details, such as cash flow and reserve levels, to ensure that all legal and regulatory requirements are met.; Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.; Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.; Receive, record, and authorize requests for disbursements in accordance with company policies and procedures. |
| O*NET Skills (3–5) | Critical Thinking; Reading Comprehension; Mathematics |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Controllers are preparing the September 3 intercompany settlement after the August 31 close. The US parent AR does not fully reconcile to the Canada and Mexico AP mirrors because of local-currency balances, one stale Canada FX rate, in-transit goods, a voided duplicate, and an orphan AP item. Treasury needs a USD settlement workbook and netting recommendation before wires go out.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | intercompany_settlement_northline-industrial-holdings.xlsx |
| Format | xlsx |
| Required sections/tabs | AR inventory (USD); AP mirror converted at memo FX; pair tie-out by counterparty; cut-off / exception log; controller netting and wire recommendation |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| northline-industrial-holdings_ar_subledger.csv | csv | Parent USD AR open items to Canada and Mexico affiliates | 40+ invoice rows | In-transit FOB shipper; void duplicate; management-fee timing | No finished net settlement |
| northline-industrial-holdings_ap_mirror.csv | csv | Affiliate AP mirrors in CAD and MXN with local refs | 40+ payable rows | Stale CAD rate; duplicate void; orphan AP; missing in-transit receipts | No governing FX table |
| intercompany_cutoff_and_fx_memo.txt | txt | Month-end FX spots, FOB cut-off rule, settlement currency hierarchy, void/orphan treatment | 600–900 words | Memo rate governs over sub booking rate; parent USD invoice governs settlement | No completed wire amounts |

## Expert Judgment

1. Which AR lines stay in the settlement population (including FOB shipping-point in-transit) versus voids.
2. Which AP lines are matched, voided duplicates, orphans, or absent because goods are still in transit.
3. Whether to revalue Canada AP using the August 31 memo CAD rate or the stale July rate on the sub's books.
4. Whether parent USD invoice amounts or converted affiliate AP control the wire.
5. How to present FX tie-out differences without changing the settlement USD.
6. Netting recommendation by counterparty for the September 3 cash sweep.

## Traps / Difficulty

- INV-AR-8841 and INV-AR-8855 shipped FOB shipping point before August 31 but not received by affiliates until September — keep AR; no AP yet.
- INV-AR-8820 is a voided duplicate — exclude.
- AP-C-448 duplicates AP-C-441 — void; exclude.
- AP-C-455 is an orphan Canada payable with no parent AR — exclude from settlement net.
- AP-C-441 was booked using July CAD rate 1.3680; memo August 31 rate 1.3724 governs revaluation.
- Settlement USD equals parent invoice USD; converted AP is for tie-out only.
- Prior-month average rates appear in a footnote — superseded by August 31 spots in the memo table.
- No file alone yields the wire schedule; memo hierarchy binds AR and AP together.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | intercompany_settlement_northline-industrial-holdings.xlsx |
| Settlement AR Canada USD | sum of includable Canada AR (incl. in-transit 8841) |
| Settlement AR Mexico USD | sum of includable Mexico AR (incl. in-transit 8855) |
| Memo FX rates | CAD 1.3724 / MXN 18.5800 per USD |
| Orphan / void exclusions | AR-8820, AP-C-448, AP-C-455 out |
| Net wires by counterparty | parent USD settlement totals |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Cut-off documentation | Cites memo FOB shipping-point rule for in-transit invoices |
| FX hierarchy | Uses Aug 31 memo spots; notes stale July rate on AP-C-441 |
| Controller recommendation | States net USD receivable by Canada and Mexico for Sep 3 sweep |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends dropping in-transit AR-8841 / AR-8855 from settlement because affiliates have not booked AP | -5 |
| Recommends settling Canada using the stale July CAD rate 1.3680 instead of the Aug 31 memo rate | -5 |
| Recommends including orphan AP-C-455 in the Canada settlement net | -4 |

## Strip Test / Batch Diversity

Attempt 2 after Uniqueness FAIL on `covenant_headroom_pack` (lender re-test of borrower EBITDA/Funded Debt certificate — now CLOSED). New skeleton `intercompany_settlement`: AR/AP mirrors + FX + cut-off disputes → settlement worksheet + netting recommendation. Not FX consolidation of external revenue, not renewal routing, not valuation, not true-up, not SI reserve, not covenant headroom.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] AR settlement population under memo cut-off
- [x] AP conversion at memo FX with exclusions
- [x] Pair tie-out and exception log
- [x] Controller netting / wire recommendation
