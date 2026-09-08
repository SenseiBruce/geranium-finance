#!/usr/bin/env python3
"""Generate inputs for Northline Industrial Holdings covenant headroom pack."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

from northline_constants import (
    ADD_ACQ_COSTS,
    ADD_INVENTORY_STEPUP,
    ADD_LITIGATION,
    ADD_RESTRUCT_CLAIMED,
    ADD_SBC,
    ADD_SPONSOR_FEE_CLAIMED,
    ADD_SYNERGY_RUNRATE,
    AS_OF,
    CA_TXT,
    CAPEX_EXCLUDED_ACQ,
    CAPEX_GROSS_YTD,
    CASH_INTEREST_TTM,
    DEBT_XLSX,
    DRAFT_Q1_REVOLVER,
    EBITDA_CSV,
    ENTITY,
    FINANCE_LEASES,
    INTERCOMPANY_GUARANTOR,
    LC_UNDRAWN,
    REPORTED_EBITDA,
    REVOLVER_COMMITMENT,
    REVOLVER_DRAWN,
    SELLER_NOTE,
    SLUG,
    TERM_LOAN_A,
    TTM_LABEL,
)

TASK_INPUTS = Path(__file__).resolve().parent.parent / "tasks" / SLUG / "inputs"

thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
header_fill = PatternFill("solid", fgColor="37474F")  # slate, not AI-blue
header_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
money_format = '#,##0.00'


def money(x: float) -> float:
    return round(float(x), 2)


def write_debt_schedule(path: Path) -> None:
    wb = Workbook()

    # --- Facilities ---
    ws = wb.active
    ws.title = "Facilities"
    ws["A1"] = f"{ENTITY} — Debt Schedule"
    ws["A2"] = f"As of {AS_OF}"
    ws["A3"] = "Source: Agent bank borrowing-base extract + borrower treasury workbook"
    ws["A1"].font = Font(bold=True, size=14, name="Calibri")

    headers = [
        "facility_id",
        "facility_name",
        "facility_type",
        "commitment",
        "outstanding",
        "rate_index",
        "spread_bps",
        "maturity",
        "cash_interest_ttm",
        "inclusion_note",
    ]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(4, col, h)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin

    rows = [
        (
            "TL-A",
            "Term Loan A",
            "Term",
            TERM_LOAN_A,
            TERM_LOAN_A,
            "SOFR",
            325,
            "2029-09-30",
            2_612_418.22,
            "Senior secured term; always Funded Debt",
        ),
        (
            "RCF-1",
            "Revolving Credit Facility",
            "Revolver",
            REVOLVER_COMMITMENT,
            REVOLVER_DRAWN,
            "SOFR",
            300,
            "2028-09-30",
            1_684_220.18,
            "Drawn portion only; undrawn commitment excluded",
        ),
        (
            "FL-OPS",
            "Equipment finance leases",
            "FinanceLease",
            FINANCE_LEASES,
            FINANCE_LEASES,
            "Fixed",
            0,
            "various",
            148_220.40,
            "Capitalized leases per CA §1.01 Finance Lease Obligations",
        ),
        (
            "SN-BOLT",
            "Bolt & Die seller note",
            "SellerNote",
            SELLER_NOTE,
            SELLER_NOTE,
            "Fixed",
            650,
            "2027-12-15",
            292_500.00,
            "Subordinated purchase-price note — still Funded Debt unless expressly carved",
        ),
        (
            "IC-PAR",
            "Intercompany note — Northline Holdco LLC",
            "Intercompany",
            INTERCOMPANY_GUARANTOR,
            INTERCOMPANY_GUARANTOR,
            "Fixed",
            0,
            "on demand",
            0.00,
            "Owing to Guarantor affiliate; borrower flags as Funded Debt (verify CA)",
        ),
        (
            "LC-POOL",
            "Standby letters of credit (undrawn)",
            "LetterOfCredit",
            LC_UNDRAWN,
            0.00,
            "n/a",
            0,
            "2027-03-31",
            0.00,
            "Undrawn face $3,200,000; zero drawn as of as-of date",
        ),
    ]

    for r_i, row in enumerate(rows, 5):
        for c_i, val in enumerate(row, 1):
            cell = ws.cell(r_i, c_i, val)
            cell.border = thin
            if c_i in (4, 5, 9) and isinstance(val, (int, float)):
                cell.number_format = money_format

    ws["A12"] = "Cash interest TTM (sum of facility cash interest columns)"
    ws["B12"] = CASH_INTEREST_TTM
    ws["B12"].number_format = money_format
    ws["C12"] = (
        "Note: TL-A + RCF + leases + seller note interest; intercompany carries no cash coupon; "
        "LC fees are Commitment Fees under §2.09 and are NOT Cash Interest Expense for ICR."
    )

    ws["A14"] = "Revolver availability"
    ws["B14"] = REVOLVER_COMMITMENT - REVOLVER_DRAWN
    ws["B14"].number_format = money_format

    for col in range(1, 11):
        ws.column_dimensions[chr(64 + col) if col <= 26 else "A"].width = 18
    ws.column_dimensions["B"].width = 42
    ws.column_dimensions["J"].width = 55

    # --- CapEx YTD ---
    ws2 = wb.create_sheet("CapEx_YTD")
    ws2["A1"] = f"{ENTITY} — Capital expenditures YTD through {AS_OF}"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = "Calendar 2026 YTD (agreement CapEx basket is calendar-year)"

    cap_headers = [
        "capex_id",
        "project",
        "site",
        "category",
        "amount",
        "month",
        "acq_related_flag",
        "notes",
    ]
    for col, h in enumerate(cap_headers, 1):
        cell = ws2.cell(4, col, h)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin

    capex_rows = [
        ("CX-2601", "CNC cell refresh", "Dayton OH", "Maintenance", 412_880.40, "2026-01", "N", "Replacement spindles"),
        ("CX-2602", "Roof & HVAC", "Dayton OH", "Maintenance", 288_220.18, "2026-01", "N", ""),
        ("CX-2603", "Forklift fleet", "Toledo OH", "Maintenance", 164_110.55, "2026-02", "N", ""),
        ("CX-2604", "ERP module licenses capitalized", "HQ Cleveland", "Growth", 220_450.00, "2026-02", "N", "Borrower IT capitalization"),
        ("CX-2605", "Press line tooling", "Toledo OH", "Growth", 685_220.18, "2026-03", "N", ""),
        ("CX-2606", "Bolt & Die integration CapEx — paint line", "Fort Wayne IN", "AcquisitionIntegration", 920_000.00, "2026-03", "Y", "Permitted Acquisition closing 2025-11-18"),
        ("CX-2607", "Bolt & Die integration CapEx — QA lab", "Fort Wayne IN", "AcquisitionIntegration", 920_000.00, "2026-04", "Y", "Same Permitted Acquisition"),
        ("CX-2608", "Wastewater upgrade", "Dayton OH", "Maintenance", 512_840.22, "2026-04", "N", "EPA consent order related"),
        ("CX-2609", "Warehouse racking", "Toledo OH", "Growth", 318_450.22, "2026-05", "N", ""),
        ("CX-2610", "Safety interlocks", "Dayton OH", "Maintenance", 148_220.40, "2026-05", "N", ""),
        ("CX-2611", "Die-cast cell expansion", "Toledo OH", "Growth", 1_240_880.18, "2026-06", "N", ""),
        ("CX-2612", "IT network backbone", "HQ Cleveland", "Growth", 385_220.18, "2026-06", "N", ""),
        ("CX-2613", "Parking lot resurfacing", "Dayton OH", "Maintenance", 96_440.55, "2026-06", "N", ""),
        ("CX-2614", "Spare tooling inventory capitalized", "Toledo OH", "Maintenance", 412_880.40, "2026-06", "N", "Controller reclass from inventory"),
        ("CX-2615", "Compressor replacement", "Fort Wayne IN", "Maintenance", 194_587.09, "2026-06", "N", ""),
        # filler detail lines to hit depth
        ("CX-2616", "Metrology gauges", "Dayton OH", "Maintenance", 42_880.40, "2026-02", "N", ""),
        ("CX-2617", "Office furniture capitalized", "HQ Cleveland", "Growth", 28_110.55, "2026-03", "N", "Threshold policy $5k"),
        ("CX-2618", "Dock levelers", "Toledo OH", "Maintenance", 55_220.18, "2026-04", "N", ""),
        ("CX-2619", "Fire suppression retrofit", "Dayton OH", "Maintenance", 88_640.22, "2026-05", "N", ""),
        ("CX-2620", "Prototype cell (R&D capitalized)", "Dayton OH", "Growth", 185_443.65, "2026-05", "N", "Borrower treats as growth CapEx"),
    ]

    # Scale so sum equals CAPEX_GROSS_YTD
    raw_sum = sum(r[4] for r in capex_rows)
    # Adjust last maintenance line to force exact total
    adjusted = list(capex_rows)
    delta = money(CAPEX_GROSS_YTD - raw_sum)
    last = list(adjusted[-1])
    last[4] = money(last[4] + delta)
    adjusted[-1] = tuple(last)

    for r_i, row in enumerate(adjusted, 5):
        for c_i, val in enumerate(row, 1):
            cell = ws2.cell(r_i, c_i, val)
            cell.border = thin
            if c_i == 5:
                cell.number_format = money_format

    total_row = 5 + len(adjusted)
    ws2.cell(total_row, 4, "Gross CapEx YTD")
    ws2.cell(total_row, 5, CAPEX_GROSS_YTD).number_format = money_format
    ws2.cell(total_row + 1, 4, "Rows flagged acq_related_flag=Y")
    ws2.cell(total_row + 1, 5, CAPEX_EXCLUDED_ACQ).number_format = money_format
    ws2.cell(total_row + 2, 1, "Borrower note: CapEx basket limit per CA is $8,500,000 calendar 2026; borrower claims full gross is under limit after carve-outs.")

    for col, w in enumerate([12, 48, 16, 22, 14, 10, 16, 40], 1):
        ws2.column_dimensions[chr(64 + col)].width = w

    # --- Interest detail (supporting) ---
    ws3 = wb.create_sheet("Interest_Detail")
    ws3["A1"] = f"Cash interest detail — {TTM_LABEL}"
    ws3["A1"].font = Font(bold=True)
    ih = ["period", "facility_id", "interest_paid", "pik_interest", "commitment_fee", "lc_fee"]
    for col, h in enumerate(ih, 1):
        cell = ws3.cell(3, col, h)
        cell.fill = header_fill
        cell.font = header_font

    # Distribute cash interest across 4 quarters irregularly
    interest_blocks = [
        ("2025-Q3", "TL-A", 648_220.18, 0, 0, 0),
        ("2025-Q3", "RCF-1", 402_110.40, 0, 22_840.18, 8_220.40),
        ("2025-Q3", "FL-OPS", 36_880.22, 0, 0, 0),
        ("2025-Q3", "SN-BOLT", 73_125.00, 0, 0, 0),
        ("2025-Q4", "TL-A", 655_440.55, 0, 0, 0),
        ("2025-Q4", "RCF-1", 418_220.18, 0, 24_110.55, 8_220.40),
        ("2025-Q4", "FL-OPS", 37_220.18, 0, 0, 0),
        ("2025-Q4", "SN-BOLT", 73_125.00, 0, 0, 0),
        ("2026-Q1", "TL-A", 648_880.40, 0, 0, 0),
        ("2026-Q1", "RCF-1", 428_640.22, 0, 25_880.40, 8_220.40),
        ("2026-Q1", "FL-OPS", 36_980.55, 0, 0, 0),
        ("2026-Q1", "SN-BOLT", 73_125.00, 0, 0, 0),
        ("2026-Q2", "TL-A", 659_877.09, 0, 0, 0),
        ("2026-Q2", "RCF-1", 435_249.38, 0, 26_220.18, 8_220.40),
        ("2026-Q2", "FL-OPS", 37_139.45, 0, 0, 0),
        ("2026-Q2", "SN-BOLT", 73_125.00, 0, 0, 0),
    ]
    # Force TL+RCF+FL+SN interest_paid sum = CASH_INTEREST_TTM
    paid_sum = sum(r[2] for r in interest_blocks)
    adj_blocks = [list(r) for r in interest_blocks]
    adj_blocks[-1][2] = money(adj_blocks[-1][2] + (CASH_INTEREST_TTM - paid_sum))

    for r_i, row in enumerate(adj_blocks, 4):
        for c_i, val in enumerate(row, 1):
            cell = ws3.cell(r_i, c_i, val)
            if c_i >= 3:
                cell.number_format = money_format

    ws3["A22"] = "Definition reminder from agent: Cash Interest Expense for Interest Coverage excludes commitment fees and LC fees (see CA §1.01)."
    ws3["A23"] = f"Control total cash interest_paid (should equal Facilities!B12): {CASH_INTEREST_TTM:,.2f}"

    # --- Stale draft tab (trap) ---
    ws4 = wb.create_sheet("Draft_Q1")
    ws4["A1"] = "SUPERSEDED — Q1 2026 draft extract (do not use for Q2 certificate)"
    ws4["A1"].font = Font(bold=True, color="B71C1C")
    ws4["A2"] = "As of 2026-03-31"
    ws4["A4"] = "facility_id"
    ws4["B4"] = "outstanding"
    ws4["A5"] = "TL-A"
    ws4["B5"] = 43_500_000.00
    ws4["A6"] = "RCF-1"
    ws4["B6"] = DRAFT_Q1_REVOLVER
    ws4["A7"] = "FL-OPS"
    ws4["B7"] = 2_240_880.40
    ws4["A8"] = "SN-BOLT"
    ws4["B8"] = SELLER_NOTE
    ws4["A10"] = "This tab retained for audit trail only. Facilities tab is the governing as-of extract."

    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.font and cell.font.name is None:
                    cell.font = Font(name="Calibri", size=11)

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def write_ebitda_bridge(path: Path) -> None:
    headers = [
        "line_id",
        "section",
        "description",
        "amount",
        "addback_code",
        "borrower_treatment",
        "source_ref",
        "notes",
    ]
    rows: list[list] = []

    # Opening GAAP / reported
    rows.append(
        [
            "E-001",
            "Reported",
            "Consolidated EBITDA per borrower pack (TTM)",
            REPORTED_EBITDA,
            "",
            "base",
            "Borrower_Q2_pack_p12",
            TTM_LABEL,
        ]
    )

    addbacks = [
        ("E-010", "Add-back", "Non-cash stock-based compensation", ADD_SBC, "SBC", "include", "GL-7100", "ASC 718 expense"),
        (
            "E-011",
            "Add-back",
            "Dayton plant consolidation restructuring",
            ADD_RESTRUCT_CLAIMED,
            "RESTRUCT",
            "include",
            "Project_Dayton_Closeout",
            "Severance, lease exit, move costs — borrower includes full amount",
        ),
        (
            "E-012",
            "Add-back",
            "Bolt & Die transaction costs (legal/advisory)",
            ADD_ACQ_COSTS,
            "ACQ_TXN",
            "include",
            "Deal_room_invoice_roll",
            "Closed 2025-11-18 Permitted Acquisition",
        ),
        (
            "E-013",
            "Add-back",
            "Bolt & Die run-rate cost synergies (projected)",
            ADD_SYNERGY_RUNRATE,
            "SYNERGY",
            "include",
            "Synergy_tracker_v3",
            "Annualized savings not yet fully in P&L; management estimate",
        ),
        (
            "E-014",
            "Add-back",
            "Sponsor management fee — Ridgepath Capital",
            ADD_SPONSOR_FEE_CLAIMED,
            "MGMT_FEE",
            "include",
            "MSA_Ridgepath",
            "Annual fee billed monthly",
        ),
        (
            "E-015",
            "Add-back",
            "Inventory step-up amortization (purchase accounting)",
            ADD_INVENTORY_STEPUP,
            "PPA_NCI",
            "include",
            "Purchase_acct_memo",
            "Non-cash; Bolt & Die opening balance sheet",
        ),
        (
            "E-016",
            "Add-back",
            "Customer warranty dispute settlement",
            ADD_LITIGATION,
            "LIT",
            "include",
            "Legal_reserve_Q2",
            "Borrower codes as extraordinary litigation add-back",
        ),
    ]
    rows.extend([list(a) for a in addbacks])

    # Supporting detail / noise rows (depth, no covenant answer)
    detail = [
        ("E-101", "Support", "SBC — options tranche A", 188_220.18, "SBC", "detail", "Equity_comp_roll", "Rolls into E-010"),
        ("E-102", "Support", "SBC — RSUs tranche B", 224_660.22, "SBC", "detail", "Equity_comp_roll", "Rolls into E-010"),
        ("E-110", "Support", "Restructuring — severance", 1_420_000.00, "RESTRUCT", "detail", "HR_severance_file", "Part of E-011"),
        ("E-111", "Support", "Restructuring — lease exit Dayton Bldg 2", 680_000.00, "RESTRUCT", "detail", "Lease_exit_calc", "Part of E-011"),
        ("E-112", "Support", "Restructuring — equipment move / dual-run", 740_000.00, "RESTRUCT", "detail", "Ops_dual_run", "Part of E-011"),
        ("E-120", "Support", "Acq costs — outside counsel", 312_440.18, "ACQ_TXN", "detail", "Inv_Baker_legal", "Part of E-012"),
        ("E-121", "Support", "Acq costs — quality of earnings", 248_220.00, "ACQ_TXN", "detail", "Inv_QoE_firm", "Part of E-012"),
        ("E-122", "Support", "Acq costs — success fee remainder", 124_560.00, "ACQ_TXN", "detail", "Banker_fee_sched", "Part of E-012"),
        ("E-130", "Support", "Synergy — purchasing consolidation (est.)", 480_000.00, "SYNERGY", "detail", "Synergy_tracker_v3", "Not booked"),
        ("E-131", "Support", "Synergy — headcount overlap (est.)", 420_000.00, "SYNERGY", "detail", "Synergy_tracker_v3", "Not booked"),
        ("E-132", "Support", "Synergy — freight lane overlap (est.)", 200_000.00, "SYNERGY", "detail", "Synergy_tracker_v3", "Not booked"),
        ("E-140", "Support", "Mgmt fee — Jul–Dec 2025", 375_000.00, "MGMT_FEE", "detail", "MSA_Ridgepath", "Part of E-014"),
        ("E-141", "Support", "Mgmt fee — Jan–Jun 2026", 375_000.00, "MGMT_FEE", "detail", "MSA_Ridgepath", "Part of E-014"),
        ("E-150", "Support", "PPA inventory step-up amort monthly avg", 53_075.04, "PPA_NCI", "detail", "Purchase_acct_memo", "x6 months in TTM window post-close"),
        ("E-160", "Support", "Warranty settlement — OEM customer Atlas Forge", 425_000.00, "LIT", "detail", "Legal_reserve_Q2", "Recurring product line dispute pattern 2023–2026"),
        ("E-200", "Memo", "Borrower claimed Adjusted EBITDA (sum of includes)", "", "CLAIMED_TOTAL", "memo", "Borrower_Q2_pack_p14", "Do not treat as lender figure"),
        ("E-201", "Memo", "Prior quarter lender-adjusted EBITDA (Q1 certificate)", 17_640_220.18, "HIST", "memo", "Bank_Q1_cert", "Reference only; not governing for Q2"),
        ("E-202", "Memo", "Board-approved restructuring plan date", 0.0, "RESTRUCT", "memo", "Board_minutes_2025-10-12", "Plan dated; amount still subject to CA cap"),
        ("E-203", "Memo", "Void duplicate add-back row (cancelled)", 0.0, "VOID", "exclude", "AP_void_log", "Duplicate of E-011 portion — already zeroed"),
    ]
    # Fix SBC detail to sum to ADD_SBC
    sbc_detail_sum = 188_220.18 + 224_660.22
    detail[1] = (
        "E-102",
        "Support",
        "SBC — RSUs tranche B",
        money(ADD_SBC - 188_220.18),
        "SBC",
        "detail",
        "Equity_comp_roll",
        "Rolls into E-010",
    )
    # Fix acq cost details
    acq_a, acq_b = 312_440.18, 248_220.00
    detail[6] = (
        "E-122",
        "Support",
        "Acq costs — success fee remainder",
        money(ADD_ACQ_COSTS - acq_a - acq_b),
        "ACQ_TXN",
        "detail",
        "Banker_fee_sched",
        "Part of E-012",
    )
    # Fix restruct details to sum
    detail[2] = ("E-110", "Support", "Restructuring — severance", 1_420_000.00, "RESTRUCT", "detail", "HR_severance_file", "Part of E-011")
    detail[3] = ("E-111", "Support", "Restructuring — lease exit Dayton Bldg 2", 680_000.00, "RESTRUCT", "detail", "Lease_exit_calc", "Part of E-011")
    detail[4] = (
        "E-112",
        "Support",
        "Restructuring — equipment move / dual-run",
        money(ADD_RESTRUCT_CLAIMED - 1_420_000.00 - 680_000.00),
        "RESTRUCT",
        "detail",
        "Ops_dual_run",
        "Part of E-011",
    )

    rows.extend([list(d) for d in detail])

    # Extra operational noise lines for depth (non-addback P&L context)
    for i, (desc, amt) in enumerate(
        [
            ("Net sales TTM (context)", 96_440_220.18),
            ("COGS TTM (context)", -68_220_440.55),
            ("SG&A TTM before add-backs (context)", -12_840_880.40),
            ("D&A TTM already in EBITDA bridge start (context)", 4_880_220.18),
            ("Other income/(expense) net (context)", -1_030_679.16),
        ],
        start=300,
    ):
        rows.append(
            [
                f"E-{i}",
                "Context",
                desc,
                amt,
                "",
                "context",
                "Borrower_IS_TTM",
                "Not an add-back; contextual only",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for row in rows:
            if isinstance(row[3], float):
                row[3] = f"{row[3]:.2f}"
            w.writerow(row)


def write_credit_agreement(path: Path) -> None:
    text = f"""\
NORTHLINE INDUSTRIAL HOLDINGS, INC.
Credit Agreement — Selected Covenant and Definition Excerpts
First Lien Credit Agreement dated as of September 30, 2024, as amended by Amendment No. 1 (Bolt & Die acquisition consent) dated November 12, 2025
Borrower: {ENTITY}, Inc. and certain subsidiaries as Guarantors
Administrative Agent: Harbor Mid-Market Lending LLC
Confidential — for credit file use

These excerpts govern the Q2 {AS_OF} financial covenant certificate. Where borrower-prepared schedules conflict with this agreement, the agreement controls. Defined terms not set out below have the meanings given in §1.01 of the Credit Agreement.

--------------------------------------------------------------------------------
SECTION 1.01 — SELECTED DEFINITIONS
--------------------------------------------------------------------------------

"Cash Interest Expense" means, for any period, the consolidated interest expense of the Borrower and its Restricted Subsidiaries for such period determined in accordance with GAAP, but excluding (a) amortization of deferred financing fees, (b) non-cash interest or payment-in-kind interest, (c) commitment fees, ticking fees, and letter-of-credit fees, and (d) interest on Indebtedness owing to a Guarantor or other Restricted Subsidiary that is a Loan Party. For the avoidance of doubt, Cash Interest Expense includes cash interest on the Bolt & Die seller note.

"Consolidated Adjusted EBITDA" means, for any period, Consolidated EBITDA for such period, adjusted by adding (without duplication) the following amounts to the extent deducted in arriving at Consolidated EBITDA and permitted under this definition:

(a) non-cash stock-based compensation expense;

(b) Permitted Restructuring Charges in an aggregate amount not to exceed $2,000,000 for any Trailing Twelve Month period;

(c) fees, costs, and expenses incurred in connection with a Permitted Acquisition (including the Bolt & Die acquisition), limited to amounts actually paid or accrued within twelve (12) months of the applicable closing date;

(d) non-cash purchase accounting adjustments, including amortization of inventory step-up;

(e) management, monitoring, or similar fees payable to Ridgepath Capital LP or its Affiliates, in an aggregate amount not to exceed $500,000 in any Trailing Twelve Month period;

(f) extraordinary, non-recurring litigation settlements that are not Ordinary Course Warranty Matters, limited to amounts disclosed in writing to the Administrative Agent.

Notwithstanding anything to the contrary in this definition, Consolidated Adjusted EBITDA shall NOT include: (i) projected, run-rate, or "yet to be realized" cost synergies or savings; (ii) add-backs for Ordinary Course Warranty Matters (including product warranty disputes in the Borrower's historical lines of business); (iii) any portion of Permitted Restructuring Charges above the $2,000,000 Trailing Twelve Month cap; or (iv) management fees above the $500,000 Trailing Twelve Month basket in clause (e).

"Consolidated Funded Debt" means, as of any date, the sum (without duplication) of (a) the outstanding principal amount of the Term Loans, (b) the outstanding Revolving Loans (drawn amounts only), (c) Finance Lease Obligations, (d) the outstanding principal amount of the Bolt & Die seller note, and (e) other Indebtedness for borrowed money of the Borrower and its Restricted Subsidiaries, but excluding:

(1) undrawn letters of credit and undrawn revolving commitments;
(2) Indebtedness owing to a Guarantor or other Loan Party (including the intercompany note payable to Northline Holdco LLC while it remains a Guarantor);
(3) earn-out obligations until such obligations become fixed and payable.

"Finance Lease Obligations" means obligations that are required to be classified and accounted for as finance leases on a balance sheet of such Person under GAAP.

"Ordinary Course Warranty Matters" means product warranty, customer quality, or similar claims arising in the ordinary course of the Borrower's industrial components business, whether or not reserved or settled in a particular period.

"Permitted Acquisition CapEx" means Capital Expenditures incurred within eighteen (18) months after the closing of a Permitted Acquisition that are (a) identified in the acquisition integration budget delivered to the Administrative Agent and (b) solely related to integration of the acquired business. Permitted Acquisition CapEx is excluded from the CapEx Basket Usage calculation in §6.12.

"Permitted Restructuring Charges" means cash charges for severance, facility exit, and relocation incurred pursuant to a restructuring plan approved by the Board of Directors and disclosed to the Administrative Agent, subject to the $2,000,000 Trailing Twelve Month cap in the Consolidated Adjusted EBITDA definition.

"Trailing Twelve Month" or "TTM" means the four fiscal quarters most recently ended on or prior to the applicable Test Date.

--------------------------------------------------------------------------------
SECTION 6.10 — FINANCIAL COVENANTS
--------------------------------------------------------------------------------

(a) Total Leverage Ratio. The Borrower will not permit the Total Leverage Ratio as of the last day of any Test Period to exceed 4.50 to 1.00.
    Total Leverage Ratio = Consolidated Funded Debt / Consolidated Adjusted EBITDA.

(b) Interest Coverage Ratio. The Borrower will not permit the Interest Coverage Ratio as of the last day of any Test Period to be less than 2.50 to 1.00.
    Interest Coverage Ratio = Consolidated Adjusted EBITDA / Cash Interest Expense.

Test Date for this certificate: {AS_OF}. Test Period: Trailing Twelve Months ended on the Test Date.

--------------------------------------------------------------------------------
SECTION 6.12 — CAPITAL EXPENDITURES BASKET
--------------------------------------------------------------------------------

The Borrower will not permit CapEx Basket Usage for any calendar year to exceed $8,500,000.
CapEx Basket Usage = aggregate Capital Expenditures of the Borrower and its Restricted Subsidiaries during such calendar year, excluding Permitted Acquisition CapEx.

For calendar year 2026, CapEx Basket Usage is measured year-to-date through the Test Date for interim certificates, against the full-year $8,500,000 basket (no proration of the basket itself).

--------------------------------------------------------------------------------
SECTION 6.05 — AFFILIATE TRANSACTIONS (excerpt)
--------------------------------------------------------------------------------

Management fees to Ridgepath Capital LP are permitted solely to the extent they do not exceed $500,000 in any Trailing Twelve Month period for purposes of Consolidated Adjusted EBITDA add-backs. Amounts paid above that basket remain Affiliate Transactions subject to other conditions and are not addable to Consolidated Adjusted EBITDA.

--------------------------------------------------------------------------------
AGENT INTERPRETIVE NOTES (credit file)
--------------------------------------------------------------------------------

1. The Draft_Q1 balances in any superseded workbook tab are not the Test Date balances. Use the as-of {AS_OF} Facilities extract.

2. Letter-of-credit undrawn face amounts are not Consolidated Funded Debt. If an LC is drawn, the resulting Revolving Loan or reimbursement obligation is included when outstanding.

3. Borrower synergy trackers that label savings as "run-rate" or "annualized" do not satisfy clause (i) of the Consolidated Adjusted EBITDA negative list until the savings are reflected in consolidated results.

4. The Atlas Forge / OEM warranty settlement pattern (recurring quality disputes on legacy product) is an Ordinary Course Warranty Matter under this agreement.

5. These excerpts are controlling for the Q2 certificate. Do not rely on borrower pack narrative that restates definitions more loosely than the text above.

End of excerpts.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    assert len(text.split()) >= 500, len(text.split())


def main() -> None:
    TASK_INPUTS.mkdir(parents=True, exist_ok=True)
    write_debt_schedule(TASK_INPUTS / DEBT_XLSX)
    write_ebitda_bridge(TASK_INPUTS / EBITDA_CSV)
    write_credit_agreement(TASK_INPUTS / CA_TXT)
    print(f"Wrote inputs to {TASK_INPUTS}")
    for p in sorted(TASK_INPUTS.iterdir()):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
