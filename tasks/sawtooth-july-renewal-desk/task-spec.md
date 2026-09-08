# Task Spec: sawtooth-july-renewal-desk

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** sawtooth-july-renewal-desk
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Insurance Underwriters |
| O*NET Code | 13-2053.00 |
| O*NET Tasks (3) | Examine documents to determine degree of risk; Review company records to determine amount of insurance in force; Decrease value of policy when risk is substandard and specify applicable endorsements or apply rating |
| O*NET Skills (3) | Critical Thinking; Reading Comprehension; Judgment and Decision Making |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Sawtooth Industrial Group's commercial property renewal desk is clearing the July 1 effective-date batch for the Southeast manufacturing book. I report to the chief underwriting officer, and binders need to go out Friday. The account list export looks mostly clean at the summary level, but location schedules, the 36-month loss run, and our internal routing notes do not always agree on TIV, occupancy, coastal wind exposure, or whether mitigation work is actually complete.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | renewal_underwriting_review.xlsx |
| Format | xlsx |
| Required sections/tabs | Account_Routing, Location_Exceptions, Loss_Reconciliation, Rules_Citations, Summary (equivalent labels acceptable) |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| renewal_account_list.csv | csv | Expiring accounts with summary premium, TIV, occupancy class, prior-year disposition, and account-level loss ratio | 35–40 accounts | Stale account-level loss ratios; TIV totals that do not tie to locations; accounts marked Quote at summary level despite child issues | No final routing column |
| policy_location_schedule.csv | csv | Location-level schedule with building TIV, protection class, coastal wind zone, vacancy flag, and mitigation status | 90–110 location rows | Duplicate-style location codes; one vacant occupancy change not rolled to account file; open roof-mitigation PO flagged pending on one account | No disposition |
| loss_run_36mo.csv | csv | Paid and reserved losses by location across 36 months | 60–80 loss rows | Location-level losses not reflected in account summary ratios; one large water claim at child location; catastrophe-coded rows separated | No account routing |
| underwriting_rules_notes.txt | txt | Renewal routing thresholds, referral triggers, coastal endorsement rules, documentation requirements | 500+ words | Governing hierarchy over account list when sources conflict; explicit treatment of pending mitigation and loss-ratio caps | No account-by-account answers |

## Expert Judgment

1. Whether an account routes **Quote**, **Refer**, **Decline**, or **Ask Broker** when account-level metrics look acceptable but location or loss detail triggers referral under the rules notes.
2. How to treat **pending mitigation** (open purchase order without completion evidence) versus completed work when applying coastal and roof credits.
3. Whether **account TIV** or **loss ratio** from the account list can be relied on, or must be recomputed from location schedule and loss run before routing.
4. Which **coastal wind locations** require endorsement flags or referral even when the account summary shows a clean renewal path.
5. What to document in **Rules_Citations** when two source files disagree on occupancy, TIV, or loss history.

## Traps / Difficulty

- Account **SI-1042** shows a moderate account-level loss ratio but location **ORL-1042-B** carries a large year-2 water loss that forces referral under the rules.
- Account **SI-1088** remains marked renewal-ready in the account list while the location schedule shows **pending roof mitigation** not completed.
- Account **SI-1021** account-list TIV does not tie to summed location TIV beyond materiality tolerance.
- Account **SI-1156** exceeds the decline threshold on recomputed 36-month loss ratio.
- Coastal wind zone codes on several Florida and Gulf Coast locations require endorsement documentation before quote.
- Loss run uses location IDs that must be mapped to accounts through the schedule; naive merges double-count or miss reserved losses.
- A few accounts look like **Ask Broker** because occupancy changed to vacant at one location but broker update is not confirmed.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | renewal_underwriting_review.xlsx |
| Accounts reviewed | 38 accounts on Account_Routing |
| SI-1042 disposition | Refer on Account_Routing |
| SI-1088 disposition | Refer on Account_Routing (pending mitigation) |
| SI-1156 disposition | Decline on Account_Routing |
| SI-1015 disposition | Quote on Account_Routing |
| SI-1021 disposition | Refer on Account_Routing (TIV mismatch) |
| Coastal endorsement flag | Location_Exceptions flags at least 4 coastal wind locations requiring endorsement review |
| Rules citation | Rules_Citations cites underwriting_rules_notes.txt for loss-ratio and mitigation referral triggers |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Routing rationale | Account_Routing documents rule-based rationale for every non-Quote disposition |
| Loss reconciliation | Loss_Reconciliation shows recomputed account loss ratios where account list differed from loss run |
| Broker follow-up | Ask Broker accounts identify the specific missing broker confirmation |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| SI-1156 quoted despite loss ratio above decline threshold | -5 |
| SI-1088 quoted while mitigation remains pending | -4 |
| Account-list loss ratio used without recomputing when loss run conflicts | -3 |

## Strip Test / Batch Diversity

Distinct from `harborview-q1-consolidation`: insurance underwriting (not controller consolidation), renewal routing decisions (Quote/Refer/Decline/Ask Broker), four-file mix including loss run CSV, July effective-date property book, no FX/acquisition memo pattern, deliverable is underwriting review workbook not consolidated revenue rollup.

Opener: situation-first renewal desk pressure, not CFO board close. File mix: csv+csv+csv+txt. Scaffold: `renewal_desk_multi_file_routing`.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Routing disposition required per account
- [x] Location and loss exceptions documented
- [x] Rules notes cited for judgment calls
- [x] Summary counts by disposition
