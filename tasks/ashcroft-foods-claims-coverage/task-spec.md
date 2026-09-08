# Task Spec: ashcroft-foods-claims-coverage

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** ashcroft-foods-claims-coverage
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Claims Adjusters, Examiners, and Investigators |
| O*NET Code | 13-1031.00 |
| O*NET Tasks (3–5) | Examine claims forms and other records to determine insurance coverage.; Adjust reserves or provide reserve recommendations to ensure that reserve activities are consistent with corporate policies.; Verify and analyze data used in settling claims to ensure that claims are valid and that settlements are made according to company practices and procedures.; Analyze information gathered by investigation and report findings and recommendations. |
| O*NET Skills (3–5) | Critical Thinking; Reading Comprehension; Active Learning |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Ashcroft Foods LLC runs a frozen-food distribution warehouse in Dayton, Ohio. Overnight on 2025-11-18, ammonia refrigeration compressor #3 failed in Zone B. Product temperatures rose for roughly fourteen hours before temporary cooling restored the room. The insured filed commercial property claim CLM-CP-2025-8841 seeking spoilage, equipment repair, and business income. Claims must issue a coverage determination and case-reserve recommendation before the 2025-12-12 file-review committee. US commercial property; Ohio situs.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | claim_coverage_opinion_ashcroft-foods.xlsx |
| Format | xlsx |
| Required sections/tabs | Coverage determination; cleaned loss inventory; case reserve build; denied / excluded items; file recommendation notes |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| ashcroft-foods_claim_file.xlsx | xlsx | Loss notice, inventory lots, equipment estimate, BI worksheet, prior adjuster notes, payment/void rows | 100+ cells across Loss Notice, Inventory, Equipment, BI Claim, Adjuster Notes | Selling-price claim totals; packaging lot mixed into stock; duplicate invoice; VOID lot; stale note urging full sell-price payment; BI hours under waiting period | No final coverage decision; no net case reserve; no governing maintenance coinsurance math |
| ashcroft-foods_policy_schedule.csv | csv | Coverages, limits, deductibles, endorsements, exclusions, waiting periods | 25+ coverage/endorsement rows | Superseded mid-term spoilage deductible still listed; Mechanical Breakdown exclusion next to Spoilage endorsement; BI waiting period | No inventory cost totals; no coinsurance penalty; no reserve figure |
| coverage_investigation_memo.txt | txt | Governing hierarchy, stock definition, valuation rule, salvage/maintenance/deductible application rules, BI waiting-period rule | 500–800+ words | Supersedes stale notes/schedule rows; defines stock vs packaging without naming excluded lots; states coinsurance trigger rule without finished dispositions | No Accept/Deny/Partial conclusions; no named lot exclusion list; no five-step reserve recipe; no final reserve dollars |

## Expert Judgment

1. Whether Spoilage Coverage endorsement responds to temperature-driven stock loss from on-premises refrigeration mechanical failure even though equipment repair itself is excluded under Mechanical Breakdown.
2. How Delayed Maintenance applies given the claim-file OEM service interval (N-02), last service date, vendor-cancelled appointment, and the memo’s grace / coinsurance practice.
3. Whether inventory is valued at selling price (as claimed) or replacement/invoice cost per the endorsement and memo.
4. Whether packaging materials and VOID/duplicate lots belong in the covered stock pool.
5. How to apply salvage on the partially recoverable lot before deductible and coinsurance.
6. Whether Business Income is reserved given outage duration versus the policy waiting period.
7. What case reserve to recommend for covered stock after salvage, coinsurance, and deductible — and what to deny.

## Traps / Difficulty

- Claim file Inventory and Adjuster Notes push selling-price totals; memo and Spoilage endorsement require invoice/replacement cost for stock.
- Packaging lot is coded like frozen stock in the claim file but is not “stock” under the memo definition.
- Duplicate invoice row and a VOID lot inflate naive sums.
- Policy schedule still shows a superseded $10,000 spoilage deductible; memo states the current endorsement deductible governs.
- Mechanical Breakdown exclusion bars equipment repair; it does not automatically bar Spoilage endorsement stock coverage when the endorsement expressly responds to refrigeration breakdown.
- BI worksheet claims days of interruption; actual temperature outage is under the 72-hour waiting period.
- Stale field note recommends paying sell-price and equipment; memo supersedes that note for committee use.
- No single file yields the coverage disposition and the numeric case reserve.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | claim_coverage_opinion_ashcroft-foods.xlsx |
| Coverage on spoiled stock | Accept under Spoilage endorsement (with maintenance coinsurance) |
| Equipment repair | Deny — Mechanical Breakdown exclusion |
| Business Income | Deny — waiting period not met |
| Valuation basis | Invoice/replacement cost, not selling price |
| Spoilage deductible | Current endorsement amount per memo (not superseded schedule row) |
| Case reserve | Covered stock cost − salvage, × coinsurance factor, − deductible |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Endorsement vs exclusion | Explains Spoilage endorsement can respond to stock while equipment remains excluded |
| Maintenance hierarchy | Cites investigation memo for grace/coinsurance treatment of overdue service |
| Inventory hygiene | Documents drop of packaging, VOID, and duplicate rows |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends paying or reserving the equipment repair under the property form despite Mechanical Breakdown exclusion | -5 |
| Recommends approving payment of the insured's full selling-price spoilage demand as presented on the claim file | -5 |
| Recommends booking Business Income reserve despite outage shorter than the waiting period | -4 |
| Recommends Full Coverage accept authorizing payment of equipment repair and Business Income in addition to stock | -4 |

## Strip Test / Batch Diversity

Skeleton `claims_coverage_determination`: single large commercial claim → coverage vs exclusion determination + case reserve. Distinct from Crowhaven `claims_reserve_triangle` (portfolio paid triangle + pure IBNR), Pelliston `si_reserve_rollforward` (self-insured retention corridor), renewal Quote/Refer desk routing, FX consolidation, live-formula valuation, intercompany settlement, and CLOSED true-up / covenant scaffolds.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Coverage determination for stock, equipment, and BI
- [x] Governing hierarchy (memo over stale notes / superseded deductible)
- [x] Cleaned inventory (cost basis, drop packaging/VOID/duplicate)
- [x] Salvage, coinsurance, deductible → case reserve
- [x] File recommendation for committee
