# Task Spec: granite-ridge-oct-renewal-desk

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** granite-ridge-oct-renewal-desk
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Insurance Underwriters |
| O*NET Code | 13-2053.00 |
| O*NET Tasks (3) | Examine documents to determine degree of risk; Review company records to determine amount of insurance in force; Decline excessive risks |
| O*NET Skills (3) | Critical Thinking; Reading Comprehension; Mathematics |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Granite Ridge Apartment Partners' habitational renewal desk is clearing the October 1 effective-date batch for the Midwest multi-family book. I report to the chief underwriting officer, and binders need to go out Thursday. The account list export looks mostly clean at the summary level, but location schedules, the 36-month loss run, and our internal routing notes do not always agree on unit counts, subsidized occupancy flags, life-safety inspection status, or whether turnover-related vacancy is actually firm.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | renewal_underwriting_review.xlsx |
| Format | xlsx |
| Required sections/tabs | Account_Routing, Location_Exceptions, Loss_Reconciliation, Rules_Citations, Summary (equivalent labels acceptable) |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| granite_ridge_renewal_accounts.csv | csv | Expiring accounts with summary premium, TIV, unit count, occupancy percentage, subsidized-housing flag, prior-year disposition, and account-level loss ratio | 32–38 accounts | Stale unit counts after renovations; occupancy percentages that do not tie to location vacancy flags; accounts marked Quote at summary level despite child issues | No final routing column |
| granite_ridge_location_schedule.csv | csv | Location-level schedule with building TIV, unit count, subsidized-unit count, protection class, vacancy flag, sprinkler and fire-alarm inspection dates, and pool liability flag | 75–95 location rows | Duplicate-style location codes after portfolio acquisition; one building marked vacant not rolled to account occupancy; expired life-safety certificates; open pool-fence remediation PO flagged pending on one account | No disposition |
| granite_ridge_loss_run_36mo.csv | csv | Paid and reserved losses by location across 36 months | 55–70 loss rows | Location-level losses not reflected in account summary ratios; slip-and-fall and kitchen-fire claims at child buildings; catastrophe-coded rows separated | No account routing |
| granite_ridge_routing_notes.txt | txt | Renewal routing thresholds, referral triggers for inspection lapses, subsidized-housing endorsement rules, turnover vacancy documentation requirements | 500+ words | Governing hierarchy over account list when sources conflict; explicit treatment of expired inspections, pending remediation, and loss-ratio caps | No account-by-account answers |

## Expert Judgment

1. Whether an account routes **Quote**, **Refer**, **Decline**, or **Ask Broker** when account-level metrics look acceptable but location detail, inspection status, or loss history triggers referral under the rules notes.
2. How to treat **expired life-safety inspections** (sprinkler or fire alarm past due) versus recently renewed certificates when applying habitational credits and referral thresholds.
3. Whether **account unit count, TIV, or loss ratio** from the account list can be relied on, or must be recomputed from location schedule and loss run before routing.
4. Which **subsidized-housing locations** require endorsement flags or referral even when the account summary shows a clean renewal path.
5. What to document in **Rules_Citations** when two source files disagree on occupancy, unit count, inspection status, or loss history.

## Traps / Difficulty

- Account **GR-2047** shows 94% occupied at summary level with location **HAB-2047-B** vacant since August turnover; broker_confirmation=yes documents the turnover, and Section 6 does not treat 94.0% as full occupancy, so the account routes Quote.
- Account **GR-2113** account-list unit count and TIV are stale after a mid-term renovation that added eight units at **GR-2113-A**.
- Account **GR-2089** remains marked renewal-ready while the location schedule shows **expired sprinkler inspection** beyond the rules grace period.
- Account **GR-2162** shows a moderate account-level loss ratio but location **GR-2162-C** carries a large year-2 kitchen-fire loss that forces referral under the rules.
- Account **GR-2195** exceeds the decline threshold on recomputed 36-month loss ratio after location-level losses are rolled up correctly.
- Subsidized-housing flags on several Ohio and Illinois locations require endorsement documentation before quote.
- Loss run uses location IDs that must be mapped to accounts through the schedule; naive merges double-count or miss reserved losses.
- A few accounts look like **Ask Broker** because seasonal student-housing vacancy is shown at one location but broker occupancy certification is not confirmed.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | renewal_underwriting_review.xlsx |
| Accounts reviewed | 36 accounts on Account_Routing |
| GR-2047 disposition | Quote on Account_Routing (94.0% occupancy; broker-confirmed turnover vacancy) |
| GR-2089 disposition | Refer on Account_Routing (expired sprinkler inspection) |
| GR-2113 disposition | Refer on Account_Routing (stale unit count / TIV) |
| GR-2162 disposition | Refer on Account_Routing (location loss) |
| GR-2195 disposition | Decline on Account_Routing |
| GR-2018 disposition | Quote on Account_Routing |
| Subsidized endorsement flag | Location_Exceptions flags at least 3 subsidized-housing locations requiring endorsement review |
| Rules citation | Rules_Citations cites granite_ridge_routing_notes.txt for inspection-lapse and loss-ratio referral triggers |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Routing rationale | Account_Routing documents rule-based rationale for every non-Quote disposition |
| Loss reconciliation | Loss_Reconciliation shows recomputed account loss ratios where account list differed from loss run |
| Broker follow-up | Ask Broker accounts identify the specific missing broker confirmation |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| GR-2195 quoted despite loss ratio above decline threshold | -5 |
| GR-2162 quoted despite HAB-2162-C location incurred referral | -5 |
| GR-2089 quoted while sprinkler inspection remains expired | -4 |
| Account-list loss ratio used without recomputing when loss run conflicts | -3 |

## Strip Test / Batch Diversity

Distinct from `sawtooth-july-renewal-desk`: October 1 Midwest habitational multi-family book (not July Southeast manufacturing commercial property); traps center on occupancy turnover, unit-count drift after renovation, life-safety inspection lapses, and subsidized-housing endorsements rather than coastal wind, roof mitigation, and TIV/coastal zone conflicts. Same scaffold and deliverable type but different sector topology, account prefix (GR- vs SI-), and governing rule emphasis.

Distinct from `harborview-q1-consolidation` and `helix-biotech-valuation`: insurance underwriting renewal routing, four-file csv+csv+csv+txt mix, no FX/acquisition memo or valuation model pattern.

Opener: situation-first renewal desk pressure for habitational binders, not CFO board close or Series B valuation. Scaffold: `renewal_desk_multi_file_routing`.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Routing disposition required per account
- [x] Location and loss exceptions documented
- [x] Rules notes cited for judgment calls
- [x] Summary counts by disposition
