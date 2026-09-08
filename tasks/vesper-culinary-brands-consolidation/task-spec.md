# Task Spec: vesper-culinary-brands-consolidation

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** vesper-culinary-brands-consolidation
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (3) | Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.; Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.; Advise management on short-term and long-term financial objectives, policies, and actions. |
| O*NET Skills (3) | Mathematics; Critical Thinking; Reading Comprehension |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Vesper Culinary Brands closes Q3 2025 consolidated net revenue for a board packet due Friday. Three operating brands feed one ledger on different currencies and ownership timelines: Hearth Kitchen Co (USD, owned all quarter), Brine & Barrel EU (EUR subsidiary), and Kiln Spice Works (tuck-in closed mid-quarter). Brand billing extracts do not reconcile to a single board figure without FX conversion, acquisition-day proration, and exclusion of void, cancelled, duplicate, and out-of-period rows.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | consolidated_review_vesper_culinary_brands.xlsx |
| Format | xlsx |
| Required sections/tabs | Assumptions, source inventory, brand rollup, exclusions & reconciling items, board recommendation |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| vesper_culinary_brands_brand_ledger.csv | csv | All brand revenue lines with status, currency, brand, and post date | 35+ rows | void, cancelled, duplicate, out_of_period, pre-close Kiln rows, mixed EUR/USD | No consolidated Q3 total; no FX-converted column |
| kiln_spice_acquisition_memo.txt | txt | Closing date, ownership start rule, proration method for tuck-in | 350+ words | July/early-August Kiln rows still posted in ledger; conflicting “full quarter” sales note | No prorated Kiln total |
| brine_barrel_fx_and_period_reference.txt | txt | Q3 window, governing EUR→USD rate, status exclusion hierarchy | 250+ words | Spot-rate aside that must lose to stated close rate; period boundary examples | No converted Brine total; no final consolidated figure |

## Expert Judgment

1. Which ledger rows to exclude (void, cancelled, duplicate, out_of_period, and Kiln pre-ownership rows).
2. Whether Brine & Barrel EU converts at the memo close rate or the informal spot aside.
3. How to prorate Kiln Spice Works from the acquisition effective date through quarter-end (day-count vs transaction cutoff).
4. What reconciling narrative and board recommendation to attach to the consolidated Q3 figure.

## Traps / Difficulty

- Kiln Spice Works July and early-August revenue appears posted, but the acquisition memo governs ownership start mid-August.
- Brine & Barrel EU amounts are EUR; the ledger has no USD equivalent column.
- An informal spot-rate comment in the FX note conflicts with the stated board close rate — close rate governs.
- void, cancelled, and one duplicate invoice inflate naive brand sums.
- At least one prior-quarter and one post-Q3 dated row sit in the extract.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | consolidated_review_vesper_culinary_brands.xlsx |
| Q3 period window | 2025-07-01 through 2025-09-30 (Assumptions) |
| Governing EUR→USD rate | exact rate stated in brine_barrel_fx_and_period_reference.txt |
| Kiln ownership start | acquisition effective date from kiln_spice_acquisition_memo.txt |
| Consolidated Q3 USD total | exact cents after exclusions, FX, and Kiln proration (set in golden) |
| Brand subtotals (Hearth / Brine USD / Kiln prorated) | exact cents matching golden rollup |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Reconciliation documentation | Names excluded statuses, cites both memos, and shows bridge from raw ledger to consolidated |
| Board recommendation | States the consolidated Q3 figure after FX, exclusions, and Kiln proration |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends including pre-ownership Kiln Spice revenue in the Q3 consolidated total | -5 |
| Recommends converting Brine & Barrel at the informal spot rate instead of the governing close rate | -4 |
| Instructs the board to treat void or cancelled ledger rows as recognized Q3 revenue | -3 |

## Strip Test / Batch Diversity

Same consolidation scaffold as Harborview, but culinary CPG (not media), Q3 (not Q1), EUR brand label (not CAD), and tuck-in spice brand (not digital acquisition). Distinct input filenames and entity. Avoids second renewal-desk topology already used twice in batch.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced by exact filename
- [x] Judgment on exclusions documented
- [x] FX conversion and mid-period acquisition proration required
- [x] Board recommendation section required
