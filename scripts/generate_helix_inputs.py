#!/usr/bin/env python3
"""Generate input files for helix-biotech-valuation."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from helix_constants import (
    BRIEF_RUN_RATE,
    FD_PRE,
    FOUNDERS_FD,
    LEAD_INVESTOR,
    PENDING_CUSTOMER,
    PENDING_RENEWAL_ARR,
    POST_MONEY,
    PRIMARY,
    SAFE_BIRCHWOOD,
    SAFE_STONEGATE,
    SAFE1_INVEST,
    SAFE2_INVEST,
    SERIES_A_INVESTOR,
    SERIES_A_PRICE,
    SERIES_A_SHARES,
)

TASK = Path(__file__).resolve().parent.parent / "tasks" / "helix-biotech-valuation" / "inputs"

QUARTERS = ["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"]

COHORT_DATA = {
    ("FY2022-Q3", "2023-Q1"): (1_842_600, 38, 94.2, 118_400, 42_800),
    ("FY2022-Q3", "2023-Q2"): (1_918_200, 37, 93.8, 96_200, 58_400),
    ("FY2022-Q4", "2023-Q1"): (2_214_800, 44, 95.1, 142_600, 31_200),
    ("FY2022-Q4", "2023-Q2"): (2_326_400, 43, 94.6, 128_900, 44_700),
    ("FY2023-Q1", "2023-Q2"): (2_684_200, 51, 96.4, 186_300, 28_900),
    ("FY2023-Q1", "2023-Q3"): (2_837_900, 50, 95.8, 164_700, 52_100),
    ("FY2023-Q2", "2023-Q3"): (3_118_400, 56, 94.9, 201_800, 67_400),
    ("FY2023-Q2", "2023-Q4"): (3_252_700, 55, 95.3, 178_600, 48_200),
    ("FY2023-Q3", "2023-Q4"): (3_642_800, 61, 96.1, 224_500, 39_800),
    ("FY2023-Q3", "2024-Q1"): (3_827_400, 60, 95.4, 198_700, 61_300),
    ("FY2023-Q4", "2024-Q1"): (4_218_600, 67, 95.7, 246_800, 55_900),
    ("FY2023-Q4", "2024-Q2"): (4_409_300, 66, 94.8, 231_400, 72_600),
    ("FY2024-Q1", "2024-Q2"): (4_886_200, 72, 96.3, 284_700, 48_500),
    ("FY2024-Q1", "2024-Q3"): (5_122_600, 71, 95.9, 256_400, 63_800),
    ("FY2024-Q2", "2024-Q3"): (5_684_300, 78, 95.2, 312_900, 81_400),
    ("FY2024-Q2", "2024-Q4"): (5_915_800, 77, 94.7, 298_600, 94_200),
    ("FY2024-Q3", "2024-Q4"): (6_482_400, 84, 96.0, 341_200, 57_300),
}

DUPLICATE_EXPANSION = ("FY2023-Q2", "2023-Q4", 178_600)

LOCKWOOD_PRORATA_USD = round(PRIMARY * SERIES_A_SHARES / FD_PRE, 2)
SUMMIT_PRIMARY_USD = round(PRIMARY - LOCKWOOD_PRORATA_USD, 2)


def write_cohort_xlsx(path: Path) -> None:
    wb = Workbook()
    bold = Font(bold=True)
    detail = wb.active
    detail.title = "Cohort Detail"
    headers = [
        "cohort_vintage",
        "calendar_quarter",
        "starting_arr",
        "logo_count",
        "gross_retention_pct",
        "expansion_arr",
        "churn_arr",
        "ending_arr",
        "notes",
    ]
    detail.append(headers)
    for cell in detail[1]:
        cell.font = bold

    for vintage, cal in COHORT_DATA:
        start, logos, gr, exp, churn = COHORT_DATA[(vintage, cal)]
        ending = round(start * gr / 100 + exp - churn, 2)
        notes = ""
        if vintage == "FY2024-Q3" and cal == "2024-Q4":
            notes = (
                f"Includes {PENDING_CUSTOMER} pending enterprise renewal "
                f"${PENDING_RENEWAL_ARR:,} ARR — contract out for signature, expected 2024-12-18"
            )
        detail.append([vintage, cal, start, logos, gr, exp, churn, ending, notes])

    v, cal, dup_exp = DUPLICATE_EXPANSION
    start, logos, gr, exp, churn = COHORT_DATA[(v, cal)]
    detail.append([v, cal, start, logos, gr, dup_exp, 0, "", "DUPLICATE ROW — expansion already captured on prior line"])

    rollup = wb.create_sheet("Quarterly Rollup")
    rollup.append(["calendar_quarter", "total_arr", "logo_count", "net_retention_pct"])
    for cell in rollup[1]:
        cell.font = bold
    quarter_totals: dict[str, list[float]] = {}
    for row in detail.iter_rows(min_row=2, values_only=True):
        if not row[0] or row[8] and str(row[8]).startswith("DUPLICATE"):
            continue
        q = row[1]
        quarter_totals.setdefault(q, [0.0, 0])
        quarter_totals[q][0] += float(row[7] or 0)
        quarter_totals[q][1] += int(row[3])
    nrr_by_quarter = {
        "2023-Q1": 107.2,
        "2023-Q2": 108.1,
        "2023-Q3": 107.8,
        "2023-Q4": 108.4,
        "2024-Q1": 108.6,
        "2024-Q2": 108.2,
        "2024-Q3": 107.9,
        "2024-Q4": 107.6,
    }
    for q in QUARTERS:
        if q in quarter_totals:
            arr, logos = quarter_totals[q]
            rollup.append([q, round(arr, 2), logos, nrr_by_quarter[q]])

    defs = wb.create_sheet("Definitions")
    defs.append(["field", "definition"])
    defs["A1"].font = bold
    defs["B1"].font = bold
    defs.append(["cohort_vintage", "Fiscal quarter label from NetSuite export; may not match calendar_quarter"])
    defs.append(["calendar_quarter", "Normalized calendar quarter for board reporting"])
    defs.append(["gross_retention_pct", "Starting ARR retained before expansion and churn"])
    defs.append(
        ["pending renewal", f"{PENDING_CUSTOMER} renewal flagged in CRM; ARR held in FY2024-Q3 cohort row"]
    )

    wb.save(path)


def write_cap_table(path: Path) -> None:
    rows = [
        ["holder", "security_type", "shares", "price", "investment_usd", "vesting_status", "notes"],
        ["Jane Okonkwo", "Common", 4200000, "", "", "n/a", "Co-founder CEO"],
        ["Marcus Chen", "Common", 3800000, "", "", "n/a", "Co-founder CTO"],
        [SERIES_A_INVESTOR, "Series A Preferred", SERIES_A_SHARES, SERIES_A_PRICE, 11830000, "n/a", "2022-04 close"],
        ["2021 Stock Plan (allocated)", "Options", 920000, 0.84, "", "unvested", "Grant tranche A"],
        ["2021 Stock Plan (allocated)", "Options", 530000, 1.12, "", "unvested", "Grant tranche B"],
        [
            "2021 Stock Plan (available)",
            "Options",
            0,
            "",
            "",
            "pool",
            "Counsel side letter: 12% fully diluted post-Series B target (2023)",
        ],
        [
            SAFE_BIRCHWOOD,
            "SAFE",
            0,
            "",
            SAFE1_INVEST,
            "outstanding",
            "Cap $45,000,000; 20% discount to Series B price; MFN clause outstanding",
        ],
        [
            SAFE_STONEGATE,
            "SAFE",
            0,
            "",
            SAFE2_INVEST,
            "outstanding",
            "Cap $55,000,000; no discount",
        ],
        ["Dr. Elena Ruiz", "Advisor Warrant", 85000, 0.01, "", "partial", "42,000 exercised 2024-03-11; 43,000 unexercised in FD"],
        ["Employee exercises (YTD)", "Common", 118400, 0.84, "", "vested", "Routine option exercises"],
        ["Board observer pool", "Options", 64000, 1.12, "", "unvested", "2024 director grant"],
        ["Treasury shares", "Common", 24000, "", "", "n/a", "Repurchase reserve"],
        ["2020 advisor grant", "Options", 36000, 0.42, "", "vested", "Fully vested"],
        ["2022 refresh grant", "Options", 212000, 1.24, "", "unvested", "Engineering retention"],
        ["Strategic partner warrant", "Warrant", 150000, 1.48, "", "unexercised", "LabCorp partnership"],
        ["2021 Stock Plan (reserved)", "Options", 180000, 0.96, "", "unvested", "Sales leadership"],
        ["Employee stock purchase", "Common", 48200, 1.06, "", "vested", "ESPP Q3 2024"],
        [
            SERIES_A_INVESTOR,
            "Series B Pro-Rata (planned)",
            0,
            "",
            LOCKWOOD_PRORATA_USD,
            "planned",
            f"Full pro-rata share of ${PRIMARY:,} primary per investor_brief.txt ({SERIES_A_SHARES/FD_PRE:.4%} of FD pre)",
        ],
        [
            "Helix Biotech (FD reconciliation)",
            "Reference",
            FOUNDERS_FD,
            "",
            "",
            "subtotal",
            "Sum of Common, Options, Warrant rows above (excludes Series A and SAFEs)",
        ],
        [
            "Helix Biotech (FD reconciliation)",
            "Reference",
            FD_PRE,
            "",
            "",
            "subtotal",
            "Founders/employee FD subtotal plus Series A preferred shares",
        ],
        [
            "Option pool refresh (proposed)",
            "Options",
            0,
            "",
            "",
            "pool",
            "Term sheet requests 15% post-money; counsel model shows 12%",
        ],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def write_investor_brief(path: Path) -> None:
    text = f"""HELIX BIOTECH — SERIES B DILIGENCE BRIEF (DRAFT)
Prepared for board finance committee review
Date: November 14, 2024
Lead investor draft: {LEAD_INVESTOR}

Executive summary
{LEAD_INVESTOR} is prepared to lead a ${PRIMARY:,} primary Series B at a ${112_000_000:,} pre-money valuation, subject to model sign-off and final docs. Helix sells lab-informatics subscriptions to hospital networks and regional reference labs. Expansion within installed cohorts has held up; management still thinks $60M+ ARR is reachable inside 24 months if the {PENDING_CUSTOMER} renewal closes on schedule.

Transaction terms (indicative)
- Primary proceeds: ${PRIMARY:,} (total new primary; includes {SERIES_A_INVESTOR} pro-rata)
- Pre-money valuation: ${112_000_000:,}
- Post-money valuation (before option pool refresh mechanics): ${POST_MONEY:,}
- Target post-money option pool: 15% (refresh from current allocated pool)
- {SERIES_A_INVESTOR} pro-rata primary allocation: ${LOCKWOOD_PRORATA_USD:,.2f} ({SERIES_A_SHARES / FD_PRE:.4%} of FD pre-money)
- {LEAD_INVESTOR} lead primary allocation: ${SUMMIT_PRIMARY_USD:,.2f} (remainder of primary)
- Board seat: {LEAD_INVESTOR} designated director at close

Pre-money FD share count (from cap_table.csv)
- Founders, employees, options, and warrants (excluding Series A): {FOUNDERS_FD:,} shares
- {SERIES_A_INVESTOR} Series A preferred: {SERIES_A_SHARES:,} shares
- Total FD pre-money: {FD_PRE:,} shares

ARR and growth
Management quotes a November run-rate of ${BRIEF_RUN_RATE:,} including one pending enterprise renewal. Finance's cohort export runs lower once calendar quarters are normalized. We think the gap is mostly timing on {PENDING_CUSTOMER} plus a duplicate expansion row in the FY2023-Q2 export.

Footnote 1 (modeling convention): For valuation modeling purposes, exclude the {PENDING_CUSTOMER} enterprise renewal (${PENDING_RENEWAL_ARR:,} ARR) until contract execution. Use normalized calendar-quarter cohort totals for TTM ARR rather than the headline run-rate figure above.

Footnote 2 (fiscal labels): cohort_summary.xlsx uses fiscal quarter labels on Cohort Detail. Map to calendar_quarter before computing trailing growth or net retention.

Footnote 3 (DCF inputs): Build a five-year explicit free-cash-flow forecast using 22% FCF margin on ARR, revenue growth of 28% / 24% / 20% / 16% / 14% in years 1–5, WACC 14%–16%, and 3.0% terminal growth. The DCF is a cross-check only. Apply the 5.5x–7.0x underwriting range to year-1 NTM revenue from that forecast (built off normalized TTM ARR); reserve the 5.0x downside multiple for normalized TTM ARR.

Comparable public diagnostics / informatics multiples (EV / NTM revenue)
- Peer set median: 6.1x
- Underwriting range: 5.5x to 7.0x NTM revenue
- Downside case multiple: 5.0x on normalized TTM ARR

Capitalization notes
Two outstanding SAFE instruments convert into the Series B:
1) {SAFE_BIRCHWOOD} — ${SAFE1_INVEST:,} invested; valuation cap $45,000,000 with 20% discount to Series B price (MFN clause noted on cap_table.csv)
2) {SAFE_STONEGATE} — ${SAFE2_INVEST:,} invested; valuation cap $55,000,000 with no discount

Counsel's cap-table extract still shows a 12% post-money pool side letter. The term sheet requires a 15% post-money pool refresh at closing. Model both references and document board-approved treatment.

Outstanding diligence items
- Confirm duplicate expansion line on FY2023-Q2 / 2023-Q4 cohort export
- Reconcile fiscal vs calendar quarter labels before publishing net retention
- Verify warrant exercise log matches cap_table.csv partial exercise on advisor tranche
- Confirm SAFE conversion order does not change {SERIES_A_INVESTOR} pro-rata allocation
- Document treatment of {SAFE_BIRCHWOOD} MFN clause relative to Series B price

Requested deliverable for Monday board call
Finance should circulate one Excel valuation workbook that ties cohort retention math to a forward revenue view, shows fully diluted ownership after the proposed primary and SAFE conversions, documents ARR bridge decisions, cross-checks valuation using revenue-multiple and DCF ranges, and includes sensitivity on growth and net retention. No PDF cap-table screenshots.

Confidential — Helix Biotech board materials only.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    TASK.mkdir(parents=True, exist_ok=True)
    write_cohort_xlsx(TASK / "cohort_summary.xlsx")
    write_cap_table(TASK / "cap_table.csv")
    write_investor_brief(TASK / "investor_brief.txt")
    print(f"Wrote inputs to {TASK}")


if __name__ == "__main__":
    main()
