# Task Spec: whitaker-precision-components-loan-underwriting

> Step 2a output. Sole handoff to Steps 2b–6. Do not include pre-computed answers.

## Decision

- **Status:** GO
- **Seed ID:** whitaker-precision-components-loan-underwriting
- **Attempt:** 1

## Metadata

| Field | Value |
|-------|-------|
| O*NET Occupation | Loan Officers |
| O*NET Code | 13-2072.00 |
| O*NET Tasks (3–5) | Analyze applicants' financial status, credit, and property evaluations to determine feasibility of granting loans.; Approve loans within specified limits, and refer loan applications outside those limits to management for approval.; Obtain and compile copies of loan applicants' credit histories, corporate financial statements, and other financial information.; Compute payment schedules. |
| O*NET Skills (3–5) | Critical Thinking; Reading Comprehension; Mathematics; Active Learning |
| Multimodal | No |
| Web Search Allowed | No |
| Time Estimate (hours) | 5 |
| Sector | Finance and Insurance |

## Situation

Whitaker Precision Components LLC, a CNC job shop in Rockford, Illinois, applied for a commercial equipment term loan (application CL-2026-4418) to finance three new machines and fixtures. Relationship-manager notes in the borrower package push Approve at the full requested amount using "management EBITDA." Credit committee meets 2026-09-18 and needs a path decision — Approve, Approve with conditions, or Decline — with a sized commitment if policy requires. US commercial bank credit; Illinois borrower.

## Deliverable

| Field | Value |
|-------|-------|
| Filename | loan_underwriting_decision_whitaker-precision-components.xlsx |
| Format | xlsx |
| Required sections/tabs | EBITDA / cash-flow build; DSCR and leverage tests; collateral eligibility and LTV; exception log; credit path decision with conditions; committee notes |

## Input File Plan

| Filename | Type | Role | Depth target | Messiness / traps | Leakage checks |
|----------|------|------|--------------|-------------------|----------------|
| whitaker-precision-components_borrower_financials.xlsx | xlsx | Application summary, multi-year P&L, balance sheet, existing debt schedule, RM notes with stale Approve push | 100+ cells across Application, Income, Balance Sheet, Debt Schedule, RM Notes | Management EBITDA add-backs; one-time gain left in EBITDA; requested amount and 84-mo tenor as "approved in principle"; book-cost LTV footnote | No final path label; no sized commitment; no adjusted EBITDA total; no DSCR on policy basis |
| whitaker-precision-components_collateral_schedule.csv | csv | Asset list with book cost, appraisal NOLV, category, pledge flags, RM advance claims | 25+ asset rows | Related-party building and leased forklift listed as pledged; obsolete mill; soft-cost deposits; RM advance rates that ignore memo eligibility | No bankable total; no binding max commitment; no eligible-only NOLV sum labeled as governing |
| credit_policy_and_exception_memo.txt | txt | Governing DSCR/LTV/leverage thresholds, EBITDA adjustment rules, collateral eligibility, advance rates, path matrix, pricing debt-service factor, hierarchy over RM notes | 500–800+ words | Supersedes RM Approve; caps owner add-back; bars related-party realty and soft costs; defines Conditional sizing when full-ask DSCR/LTV fail | No named Approve/Conditional/Decline for this file; no finished commitment dollars; no lot-by-lot disposition list |

## Expert Judgment

1. Whether reported EBITDA must be adjusted for the one-time gain and how much owner compensation add-back the memo allows (vs the larger RM/borrower claim, and vs related-party rent add-back).
2. Whether related-party realty, leased equipment, obsolete tooling, and soft-cost deposits are eligible collateral.
3. How to compute bankable collateral (category advance rates on NOLV) and the binding maximum commitment (min of bankable vs 75% of eligible NOLV).
4. How to measure DSCR and LTV at the full request versus at the sized commitment using the memo debt-service factor.
5. Which credit path applies under the memo matrix (Approve / Approve with conditions / Decline) and what conditions attach if Conditional.
6. Whether the stale RM "Approve as requested" note governs for committee purposes.

## Traps / Difficulty

- RM notes and Application tab push full-ask Approve on management EBITDA that keeps the one-time gain and adds disallowed related-party rent plus excess owner add-back.
- Collateral schedule mixes eligible CNC/fixtures with related-party building, leased forklift, obsolete mill, and soft costs; naive LTV on book cost or gross NOLV fails policy.
- Requested amount exceeds both bankable collateral and 75% eligible NOLV; correct response is size-down Conditional, not automatic Decline and not full Approve.
- Debt-service for the proposed loan must use the memo per-$1,000 monthly factor, not an arbitrary amortization guess.
- Memo supersedes RM notes when they conflict.
- No single file yields adjusted EBITDA, bankable collateral, and the path decision together.

## Rubric Preview

### Rigid (exact values)

| Check | Expected value / location |
|-------|---------------------------|
| Deliverable filename | loan_underwriting_decision_whitaker-precision-components.xlsx |
| Adjusted EBITDA | Reported − one-time gain + allowed owner add-back only |
| Path | Approve with conditions (not full-ask Approve, not Decline) |
| Commitment | Binding max = min(bankable after advances, 75% eligible NOLV) |
| Valuation basis for LTV | Appraisal NOLV on eligible assets only |
| Proposed DS | Memo factor × principal (monthly × 12) |

### Subjective (bounded conditions)

| Judgment | Conditions for full credit |
|----------|---------------------------|
| Hierarchy | States memo governs over RM Approve-as-requested note |
| Collateral hygiene | Documents drop of related-party realty, lease, obsolete, soft costs |
| Conditions | States shortened tenor and/or guaranty / covenant conditions consistent with Conditional path |

### Planned negative criteria

| Failure mode | Weight |
|--------------|--------|
| Recommends approving the full requested commitment despite LTV/DSCR failure at the ask | -5 |
| Recommends treating related-party realty as eligible collateral for the term facility | -5 |
| Recommends measuring DSCR on management EBITDA that retains the one-time gain and disallowed add-backs | -4 |
| Instructs Decline solely because the requested amount exceeds bankable collateral without presenting a sized Conditional commitment | -4 |

## Strip Test / Batch Diversity

Skeleton `commercial_loan_underwriting`: new-facility borrower package → Approve / Conditional / Decline with exception documentation. Distinct from CLOSED `covenant_headroom_pack` (existing-facility covenant retest), renewal Quote/Refer/Decline desk routing, claims coverage determination, claims triangle IBNR, SI reserve rollforward, FX consolidation, live-formula valuation, intercompany settlement, and CLOSED true-up scaffolds.

## Prompt Requirements (for satisfiability)

- [x] Named deliverable file
- [x] Each input file referenced
- [x] Path decision Approve / Approve with conditions / Decline
- [x] Governing hierarchy (memo over RM notes)
- [x] Adjusted EBITDA build
- [x] Collateral eligibility, LTV, sized commitment
- [x] DSCR / leverage tests using memo debt-service factor
- [x] Committee-facing recommendation with conditions if Conditional
