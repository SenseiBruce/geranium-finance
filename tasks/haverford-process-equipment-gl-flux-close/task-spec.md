# Task Spec: haverford-process-equipment-gl-flux-close

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** haverford-process-equipment-gl-flux-close
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (3–5) | Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies.; Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed.; Maintain current knowledge of organizational policies and procedures, federal and state policies and directives, and current accounting standards. |
| O*NET Skills (3–5) | Critical Thinking; Mathematics; Reading Comprehension; Monitoring |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Haverford Process Equipment LLC (Lebanon, Pennsylvania) is locking August 2026 books ahead of interim auditor fieldwork. Soft close is 2026-09-05. The plant controller emailed that the trial balance is "clean — no AJEs." The corporate accounting manager needs a month-end GL flux close pack: material period-over-period explanations, proposed adjusting entries grounded in support schedules, and a close-readiness call (Ready / Ready with AJEs / Hold close). US GAAP private manufacturer; Pennsylvania entity.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | flux_close_pack_haverford-process-equipment.xlsx |
| Format | xlsx |
| Required sections/tabs | Flux workpaper (material accounts); proposed AJEs; support reconciliation notes; close readiness decision; hierarchy / committee notes |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| haverford-process-equipment_trial_balance.xlsx | xlsx | July and August trial balances, account roll, plant-controller clean-close note tab | 100+ cells across Prior TB, Current TB, Account Map, Plant Notes | Voided JE still in revenue/AR; expense that should capitalize; missing freight accrual; plant "no AJEs" push | No materiality flags; no AJE list; no close-status label; no flux $ already marked pass/fail |
| haverford-process-equipment_support_schedules.csv | csv | Accrual, prepaid, inventory count, AP open items, fixed-asset / CapEx tickets, vacation true-up | 40+ line items across schedule types | Warranty reserve vs TB conflict; unamortized prepaid; physical inventory below book; CapEx ticket buried in maintenance; freight open items not accrued | No labeled "required AJE"; no net close-ready conclusion; no governing threshold applied |
| flux_threshold_and_aje_memo.txt | txt | Materiality / flux investigation rules, CapEx capitalization policy, AJE mandatory categories, hierarchy over plant note, close-status matrix | 500–800+ words | Supersedes plant clean-close email; forces explain-or-AJE on threshold breaches; CapEx vs expense rule; void JE treatment | No finished AJE amounts for this close; no Ready/Hold label for Haverford August |

## Expert Judgment

1. Which accounts breach the memo’s flux investigation thresholds (absolute and percent rules) and therefore require explanation.
2. Whether the plant controller’s “clean — no AJEs” note governs for soft close.
3. Which support-schedule mismatches require proposed AJEs (warranty, prepaid amortization, inventory write-down, freight accrual, vacation true-up, void JE reverse, CapEx capitalization).
4. Whether maintenance spend that meets CapEx criteria must be reclassified to PP&E rather than left in P&L.
5. What close-readiness status applies under the memo matrix once required AJEs are identified (Ready / Ready with AJEs / Hold close).

## Traps / Difficulty

- Plant Notes tab and soft-close email language push “no AJEs”; memo hierarchy overrides that note.
- Voided JE remains in August revenue and AR until reversed.
- CapEx ticket sits inside maintenance expense; naive flux explanation as “volume” is wrong.
- Warranty and vacation balances on the TB disagree with support schedules; freight open items have no TB accrual.
- Prepaid insurance amortization is missing for August.
- Inventory physical is below book; write-down is required, not optional “monitoring.”
- Flux thresholds use both dollar and percent tests; explaining only large dollars misses % breaches (and vice versa).
- No single file yields the full AJE set and the close-status call.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | flux_close_pack_haverford-process-equipment.xlsx |
| Hierarchy | Memo governs over plant clean-close note |
| Close status | Ready with AJEs (not Ready, not Hold solely for plant comfort) |
| Void JE | Reverse voided revenue/AR still in August TB |
| CapEx reclass | Capitalize qualifying maintenance rebuild to PP&E |
| Inventory | Write book down to physical count support |
| Warranty / vacation | True TB to support schedule balances |
| Freight | Accrue open freight support items |
| Prepaid | Book August amortization per memo/support |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Flux coverage | Material threshold breaches explained with cross-file support refs |
| AJE documentation | Each proposed AJE cites account, amount, and support source |
| Notes | States plant note does not clear required AJEs |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends Ready / soft-close with no AJEs based on the plant controller clean-close note | -5 |
| Recommends leaving the voided August revenue/AR posting unreversed | -5 |
| Instructs expensing the CapEx-qualifying rebuild that the memo requires to capitalize | -4 |
| Recommends Hold close solely because flux explanations exist, after a complete AJE pack is prepared | -3 |

## Strip Test / Batch Diversity

Skeleton `gl_flux_close_pack`: current vs prior TB + support schedules + threshold/AJE rules → flux explanations + proposed AJEs + close readiness. Distinct from FX consolidation, intercompany AR/AP settlement, CLOSED billed true-up, covenant headroom, loan Approve/Conditional/Decline, renewal Quote/Refer/Decline, claims coverage, claims triangle IBNR, SI reserve rollforward, and live-formula valuation.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Flux investigation against memo thresholds
- [x] Governing hierarchy (memo over plant clean-close note)
- [x] Proposed adjusting journal entries from support conflicts
- [x] CapEx vs expense and void-JE treatment
- [x] Close readiness Ready / Ready with AJEs / Hold close
