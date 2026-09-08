# Task Spec: meridian-property-group-reconciliation

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.
> Redesign attempt 2 — CAM annual true-up (replaces allowance closeout scaffold rejected for uniqueness).

## Decision

- **Status:** GO
- **Seed ID:** meridian-property-group-reconciliation
- **Attempt:** 2

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Treasurers and Controllers |
| O*NET Code | 11-3031.01 |
| O*NET Tasks (2) | Prepare or direct preparation of financial statements, business activity reports, financial position forecasts, annual budgets, or reports required by regulatory agencies; Analyze the financial details of past, present, and expected operations to identify development opportunities and areas where improvement is needed |
| O*NET Skills (3) | Mathematics; Critical thinking; Reading comprehension |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Meridian Property Group is closing the 2025 calendar-year common-area maintenance (CAM) true-up for Meridian Commons, a six-tenant retail strip in Columbus, OH. Property accounting billed tenants monthly estimates all year; Contour Fitness expanded mid-year and one suite sat vacant for nine months. Before Controllers issues year-end adjustment invoices and credits next Tuesday, the team must rebuild the CAM expense pool from the GL extract, apply each lease's pro-rata share and caps from the abstract workbook, and compare to what was already billed. Wrong true-ups flow straight into tenant disputes and lender covenant reporting.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | cam_trueup_meridian_commons.xlsx |
| Format | xlsx |
| Required sections/tabs | Eligible expense pool; tenant allocation and true-up; cap and vacancy exceptions; billing variance; controller recommendation |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| meridian_commons_expense_ledger.csv | csv | FY2025 GL extract of property operating expenses | 40+ rows | Capital roof coded as R&M; HVAC replacement mixed with service; duplicate invoice; insurance and marketing lines mixed in | No CAM pool total; no tenant allocations |
| tenant_lease_abstracts.xlsx | xlsx | Lease abstract tabs: suite schedule, pro-rata shares, CAM caps, inclusion/exclusion flags, vacancy clause | 5 occupied tenants + vacancy suite; 3 sheets | Contour mid-year share change; Ridgeway absolute $/SF cap; Outfitters uniquely includes marketing; vacancy absorption differs by lease | No true-up dollars |
| prior_cam_billing_register.txt | txt | Property accounting memo of 2025 estimated CAM billed by tenant with expansion note | 400+ words | Contour billed at pre-expansion share all twelve months; one tenant billed under wrong suite ID alias | No recomputed pool or true-up |

## Expert Judgment

1. Which ledger lines belong in the CAM pool versus capital, insurance (separately billed), or non-CAM marketing.
2. How to treat the Contour Fitness mid-year expansion when abstracts show two pro-rata rates but billings used one rate all year.
3. Whether vacancy GLA is absorbed by remaining tenants or by the owner under each lease's vacancy clause.
4. How Ridgeway Dental's absolute CAM dollar-per-SF cap truncates its allocated share.
5. Whether Meridian Outfitters' marketing-inclusion clause pulls otherwise-excluded marketing spend into that tenant's allocation only or into the common pool.
6. Net true-up (additional bill vs credit) per tenant and the controller recommendation for invoice issuance.

## Traps / Difficulty

- Roof replacement $186,420 coded GL 6210 Repairs & Maintenance — capital, exclude from CAM pool.
- HVAC package replacement $42,850 sits next to HVAC service contracts — exclude capital portion.
- Duplicate EXP-4482 ($3,240 landscaping) posted twice.
- Property insurance $118,600 is separately billed — exclude from CAM.
- Marketing/promo $27,480 excluded from common pool; Meridian Outfitters lease alone includes marketing in its CAM definition (allocate Outfitters' pro-rata share of marketing as an add-on, not into the shared pool).
- Contour Fitness expanded 2025-07-01 from 15.0% to 22.4% GLA share; abstracts document both; prior billings used 15.0% for all twelve months.
- Ridgeway Dental CAM capped at $4.85/SF on 2,840 SF ($13,774 max).
- Vacancy suite T-122 (9.8% GLA): most leases say owner absorbs vacancy; Outfitters and Contour say remaining tenants absorb — apply per lease.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | cam_trueup_meridian_commons.xlsx |
| Eligible shared CAM pool | approximately $412,680 after exclusions and duplicate removal |
| Contour Fitness true-up | additional bill approximately $25,913 |
| Ridgeway Dental charged | capped at $13,774 |
| Harbor Coffee true-up | credit approximately $1,107 |
| Meridian Outfitters true-up | additional bill approximately $25,557 |
| Net additional billings | approximately $48,958 |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Expense classification | Pool build cites capital roof, HVAC replacement, insurance exclusion, and duplicate EXP-4482 with ledger source |
| Vacancy treatment | Allocation documents owner-absorb vs tenant-absorb by lease clause from tenant_lease_abstracts.xlsx |
| Controller recommendation | States which tenants receive additional invoices vs credits and flags Ridgeway cap and Contour expansion |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends billing tenants for the capital roof replacement as CAM | -5 |
| Allocates Contour Fitness at 15% for the full year ignoring the July expansion in the abstracts | -4 |
| Ignores Ridgeway Dental's $4.85/SF CAM cap | -3 |

## Strip Test / Batch Diversity

Attempt 2 redesign after portal uniqueness rejection of allowance closeout scaffold. Differs from Harborview consolidation, Sawtooth/Granite renewal desks, Helix valuation, and from construction-allowance retainage audits. Property-accounting CAM true-up: expense classification + lease economics + billing variance, not GC invoice build-up against contract allowances.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Eligible CAM pool reconstruction required
- [x] Tenant allocation with lease caps and vacancy rules
- [x] Comparison to prior estimated billings
- [x] Controller recommendation on invoices/credits
