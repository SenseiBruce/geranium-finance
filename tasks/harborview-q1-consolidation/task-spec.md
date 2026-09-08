# Task Spec: harborview-q1-consolidation

> Step 2a output. Sole handoff to Steps 2b–6.

## Decision

- **Status:** GO
- **Seed ID:** harborview-q1-consolidation
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (2) | Prepare financial reports; Analyze financial data |
| O*NET Skills (3) | Mathematics; Critical thinking; Reading comprehension |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Harborview Media Group closes Q1 2025 consolidated reporting for a board meeting next week. Three labels feed the ledger on different currencies and ownership timelines. Revenue from each label's billing system does not reconcile cleanly to a single consolidated Q1 figure without FX conversion, acquisition proration, and exclusion of void or out-of-period rows.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | consolidated_review_harborview_media_group.xlsx |
| Format | xlsx |
| Required sections | Assumptions, source data, rollup, reconciliation, recommendation (any clear worksheet structure) |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| harborview_media_group_brand_ledger.csv | csv | All brand transactions with status flags | 25+ rows | void, cancelled, out_of_period, pre-Q1 row | No consolidated total |
| lattice_digital_acquisition_memo.txt | txt | Feb 1 acquisition; proration rule | 300+ words | January Lattice rows still in ledger | No prorated total |
| cascade_creative_fx_and_period_reference.txt | txt | Q1 period and CAD/USD 0.74 rate | 200+ words | Exclusions by status | No converted total |

## Expert Judgment

1. Which ledger rows to exclude (void, cancelled, out_of_period, pre-Q1).
2. Whether to convert Cascade Creative at 0.74 or spot rates.
3. How to prorate Lattice Digital for mid-period acquisition (59/90 days vs transaction-level cutoff).
4. What to document in reconciliation for board-facing recommendation.

## Traps / Difficulty

- Lattice Digital January rows appear posted but pre-close memo says exclude from Q1 consolidated totals.
- Cascade Creative amounts are CAD; ledger mixes USD and CAD brands without converted column.
- void and cancelled rows inflate naive sums.
- HM-4001 dated 2024 must be excluded from Q1.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | consolidated_review_harborview_media_group.xlsx |
| Total consolidated Q1 2025 | approximately $1,590,686.30 |
| Lattice Digital consolidated USD | approximately $697,267.02 with ~65.6% proration |
| Cascade Creative consolidated USD | approximately $452,853.28 at 0.74 rate |
| Beacon Media consolidated USD | approximately $440,566.01 full quarter |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Reconciliation documentation | Reconciliation cites void/cancelled/out-of-period exclusions and names source files |
| Board recommendation | Recommendation states consolidated figure after FX, exclusions, and Lattice proration |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| January Lattice Digital revenue included in Q1 consolidated total | -5 |
| HM-4001 prior-year row included in Q1 total | -4 |
| HM-3007 April row included in Q1 total | -3 |

## Strip Test / Batch Diversity

First pilot task. Situation-first opener; consolidation scaffold; csv+txt file mix; treasurer/controller occupation.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Judgment on exclusions documented
- [x] FX and acquisition proration required
- [x] Board recommendation section
