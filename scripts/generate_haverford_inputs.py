#!/usr/bin/env python3
"""Generate inputs for Haverford Process Equipment GL flux close pack."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

from haverford_constants import (
    ACCOUNTS,
    AUG,
    CAPEX_REBUILD,
    ENTITY_LEGAL,
    FREIGHT_OPEN,
    INV_PHYSICAL,
    INV_TB,
    JUL,
    LOCATION,
    MEMO_TXT,
    PERIOD,
    PRIOR_PERIOD,
    PREPAID_ANNUAL,
    PTO_SUPPORT,
    PTO_TB,
    SLUG,
    SOFT_CLOSE,
    SUPPORT_CSV,
    TB_XLSX,
    VOID_JE_AMT,
    WARRANTY_SUPPORT,
    WARRANTY_TB,
)
from sanitize_office import sanitize_xlsx

TASK_INPUTS = Path(__file__).resolve().parent.parent / "tasks" / SLUG / "inputs"

body = Font(name="Calibri", size=10)
header_font = Font(name="Calibri", size=10, bold=True)
title_font = Font(name="Calibri", size=12, bold=True)
thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
money = '#,##0.00'


def autosize(ws, max_w: int = 42) -> None:
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        width = min(max(len(str(c.value or "")) for c in col) + 2, max_w)
        ws.column_dimensions[letter].width = max(width, 11)


def write_tb(path: Path) -> None:
    wb = Workbook()

    # Prior TB
    ws = wb.active
    ws.title = "Prior_TB"
    ws["A1"] = f"{ENTITY_LEGAL} — Trial balance {PRIOR_PERIOD}"
    ws["A1"].font = title_font
    ws["A2"] = f"Plant: {LOCATION} | Export: ERP GL_CLOSE_JUL"
    headers = ["Account", "Account Name", "Type", "Normal Balance", "Amount"]
    for i, h in enumerate(headers, 1):
        cell = ws.cell(3, i, h)
        cell.font = header_font
        cell.border = thin
    for r, (acct, name, typ, norm) in enumerate(ACCOUNTS, 4):
        vals = [acct, name, typ, norm, JUL[acct]]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.font = body
            cell.border = thin
            if c == 5:
                cell.number_format = money
    autosize(ws)

    # Current TB
    ws2 = wb.create_sheet("Current_TB")
    ws2["A1"] = f"{ENTITY_LEGAL} — Trial balance {PERIOD} (pre-close export)"
    ws2["A1"].font = title_font
    ws2["A2"] = f"Soft-close target {SOFT_CLOSE} | Export: ERP GL_CLOSE_AUG_DRAFT"
    for i, h in enumerate(headers, 1):
        cell = ws2.cell(3, i, h)
        cell.font = header_font
        cell.border = thin
    for r, (acct, name, typ, norm) in enumerate(ACCOUNTS, 4):
        vals = [acct, name, typ, norm, AUG[acct]]
        for c, v in enumerate(vals, 1):
            cell = ws2.cell(r, c, v)
            cell.font = body
            cell.border = thin
            if c == 5:
                cell.number_format = money
    autosize(ws2)

    # Account map / JE crumbs
    ws3 = wb.create_sheet("JE_Activity_Notes")
    ws3["A1"] = f"{ENTITY_LEGAL} — August JE activity excerpts (ERP crumbs)"
    ws3["A1"].font = title_font
    crumbs = [
        ("JE_ID", "Date", "Account", "Memo", "Debit", "Credit", "Status"),
        ("JE-8792", "2026-08-04", "5100", "COGS roll for batch HP-441", 88420.18, 0, "Posted"),
        ("JE-8792", "2026-08-04", "1200", "COGS roll for batch HP-441", 0, 88420.18, "Posted"),
        ("JE-8810", "2026-08-12", "5600", "CNC spindle rebuild ticket CAP-8821 (maint GL)", CAPEX_REBUILD, 0, "Posted"),
        ("JE-8810", "2026-08-12", "2000", "Vendor: Allegheny Machine Rebuilders", 0, CAPEX_REBUILD, "Posted"),
        ("JE-8841", "2026-08-19", "1100", "Invoice INV-9918 Keystone Foods skid system", VOID_JE_AMT, 0, "Voided-in-AR"),
        ("JE-8841", "2026-08-19", "4100", "Invoice INV-9918 Keystone Foods skid system", 0, VOID_JE_AMT, "Voided-in-AR"),
        ("JE-8841V", "2026-08-21", "1100", "Billing void flag for INV-9918 after customer cancellation", 0, 0, "Billing-void-only"),
        ("JE-8860", "2026-08-28", "6100", "Monthly depreciation run", 64880.40, 0, "Posted"),
        ("JE-8860", "2026-08-28", "1650", "Monthly depreciation run", 0, 64880.40, "Posted"),
        ("JE-8871", "2026-08-29", "2000", "AP weekly pay run", 214880.40, 0, "Posted"),
        ("JE-8871", "2026-08-29", "1000", "AP weekly pay run", 0, 214880.40, "Posted"),
        ("JE-8888", "2026-08-31", "2100", "Payroll accrual true-up", 3660.22, 0, "Posted"),
        ("JE-8888", "2026-08-31", "5500", "Payroll accrual true-up", 0, 3660.22, "Posted"),
    ]
    for r, row in enumerate(crumbs, 3):
        for c, v in enumerate(row, 1):
            cell = ws3.cell(r, c, v)
            cell.font = header_font if r == 3 else body
            cell.border = thin
            if r > 3 and c in (5, 6) and isinstance(v, (int, float)):
                cell.number_format = money
    ws3["A18"] = (
        "Note: JE-8841/JE-8841V relates to customer cancellation INV-9918; "
        "original billing remains in the listed ledger accounts."
    )
    ws3["A18"].alignment = Alignment(wrap_text=True)
    ws3.merge_cells("A18:G20")
    autosize(ws3)

    # Plant notes
    ws4 = wb.create_sheet("Plant_Notes")
    ws4["A1"] = "Plant controller soft-close note"
    ws4["A1"].font = title_font
    notes = [
        ("From", "Dana Okonkwo, Plant Controller"),
        ("To", "Corporate Accounting — month-end desk"),
        ("Date", "2026-09-02"),
        ("Subject", f"{PERIOD} TB draft — clean close"),
        ("Body", ""),
    ]
    for i, (k, v) in enumerate(notes, 3):
        ws4.cell(i, 1, k).font = header_font
        ws4.cell(i, 2, v).font = body
    ws4["B8"] = (
        f"Team — August TB export GL_CLOSE_AUG_DRAFT is ready for {SOFT_CLOSE} soft close. "
        "We walked the large account movements with operations. Cash down on AP pay-downs, AR up on late-month shipments, "
        "maintenance higher on CNC spindle work, inventory up on WIP for the Keystone skid. "
        "No adjusting entries from the plant. Treat as clean. Warranty and PTO look fine on the TB. "
        "Prepaid insurance still shows the July ending balance; we usually touch that in corporate. "
        "Freight accrual was zeroed after July payments — nothing open that I know of. "
        "Please do not hold the close for flux narrative. Dana."
    )
    ws4["B8"].alignment = Alignment(wrap_text=True)
    ws4.merge_cells("B8:B14")
    ws4.column_dimensions["A"].width = 14
    ws4.column_dimensions["B"].width = 88

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    sanitize_xlsx(path)


def write_support_csv(path: Path) -> None:
    rows = [
        [
            "schedule_type",
            "line_id",
            "as_of",
            "account_hint",
            "description",
            "qty_or_units",
            "amount",
            "status",
            "source_ref",
            "notes",
        ],
        # Warranty roll — W-04 remains the labeled governing support total;
        # W-01+W-02+W-03 detail roll differs by $6,000 (authentic source gap).
        ["warranty", "W-01", PERIOD, "2200", "Opening accrued warranty", "", 176110.55, "Open", "WR-ROLL", "July ending"],
        ["warranty", "W-02", PERIOD, "2200", "Claims paid August", "", -41220.18, "Paid", "CLM-8821", "Paid from AP"],
        ["warranty", "W-03", PERIOD, "2200", "New reserves August", "", 18994.81, "Open", "WR-NEW", "Ops estimate"],
        ["warranty", "W-04", PERIOD, "2200", "Support ending balance", "", WARRANTY_SUPPORT, "Support", "WR-ROLL", "Governing support total"],
        ["warranty", "W-05", PERIOD, "2200", "TB accrued warranty (Current_TB)", "", WARRANTY_TB, "TB", "ERP", "Current GL balance differs from support schedule"],
        # Prepaid insurance — monthly amort is annual/12 per memo; do not prestate AJE
        ["prepaid", "P-01", PERIOD, "1400", "Annual package premium (policy year)", "", PREPAID_ANNUAL, "Active", "POL-INS-26", "Commercial package"],
        ["prepaid", "P-02", PERIOD, "1400", "Months remaining before Aug amort", "", 11, "Calc", "POL-INS-26", "July booked 1/12"],
        ["prepaid", "P-03", PERIOD, "1400", "August amortization period under policy year", "", "", "Calc", "POL-INS-26", "Policy POL-INS-26; annual prepaid amount on P-01"],
        ["prepaid", "P-04", PERIOD, "1400", "TB prepaid insurance balance", "", 92589.75, "TB", "ERP", "August ledger review"],
        # Inventory count
        ["inventory", "I-01", "2026-08-31", "1200", "Physical finished goods", "184", 684220.18, "Counted", "CNT-AUG", "Floor count"],
        ["inventory", "I-02", "2026-08-31", "1200", "Physical WIP", "62", 412880.40, "Counted", "CNT-AUG", "Shop floor"],
        ["inventory", "I-03", "2026-08-31", "1200", "Physical raw / components", "1", 122773.97, "Counted", "CNT-AUG", "Cage A"],
        ["inventory", "I-04", "2026-08-31", "1200", "Physical total", "", INV_PHYSICAL, "Support", "CNT-AUG", "Sum of count lines"],
        ["inventory", "I-05", "2026-08-31", "1200", "TB inventory", "", INV_TB, "TB", "ERP", "August physical count compared with current ledger balance"],
        # Freight open
        ["freight", "F-01", PERIOD, "2210", "LTL inbound — Mid-Atlantic Carriers", "", 12880.40, "Open", "BOL-4412", "Open support item"],
        ["freight", "F-02", PERIOD, "2210", "Flatbed outbound — Susquehanna Heavy Haul", "", 18420.18, "Open", "BOL-4488", "Open support item"],
        ["freight", "F-03", PERIOD, "2210", "Expedite — overnight spindle parts", "", 9987.82, "Open", "AWB-991", "Open support item"],
        ["freight", "F-04", PERIOD, "2210", "Open freight total", "", FREIGHT_OPEN, "Support", "FR-OPEN", "Open freight balance identified in August support"],
        ["freight", "F-05", PERIOD, "2210", "TB accrued freight", "", 0.00, "TB", "ERP", "July ending cleared; August TB shows zero"],
        # PTO
        ["pto", "T-01", PERIOD, "2220", "Hourly PTO liability", "4120 hrs", 48220.18, "Calc", "HR-PTO", "Rate file Aug"],
        ["pto", "T-02", PERIOD, "2220", "Salaried PTO liability", "1880 hrs", 23220.37, "Calc", "HR-PTO", "Rate file Aug"],
        ["pto", "T-03", PERIOD, "2220", "Support PTO total", "", PTO_SUPPORT, "Support", "HR-PTO", "Governing"],
        ["pto", "T-04", PERIOD, "2220", "TB accrued PTO", "", PTO_TB, "TB", "ERP", "HR-supported PTO balance differs from the current GL balance"],
        # CapEx ticket
        ["capex", "C-01", "2026-08-12", "5600", "CNC spindle housing rebuild", "1", CAPEX_REBUILD, "Posted-to-expense", "CAP-8821", "Useful life 5 years"],
        ["capex", "C-02", "2026-08-12", "1600", "CNC spindle rebuild; useful life 5 years", "1", CAPEX_REBUILD, "Ticket", "CAP-8821", "Posted to Maintenance & Repairs"],
        ["capex", "C-03", "2026-08-08", "5600", "Routine coolant flush / filters", "1", 2240.18, "Posted", "WO-7712", "Amount $2,240.18; consumable maintenance"],
        ["capex", "C-04", "2026-08-22", "5600", "Belt / seal kit replacements", "1", 1880.40, "Posted", "WO-7790", "Consumables"],
        # Noise / red herrings
        ["deposits", "D-01", PERIOD, "2300", "Customer deposit — Riverton Dairy", "", 41220.18, "Open", "DEP-2201", "Still open"],
        ["deposits", "D-02", PERIOD, "2300", "Customer deposit — Blue Ridge Brewing", "", 46890.37, "Open", "DEP-2218", "Still open"],
        ["ap", "A-01", PERIOD, "2000", "AP aging 0-30", "", 412880.40, "Open", "AP-AGE", "Informational"],
        ["ap", "A-02", PERIOD, "2000", "AP aging 31-60", "", 184220.18, "Open", "AP-AGE", "Informational"],
        ["ap", "A-03", PERIOD, "2000", "AP aging 61+", "", 41339.97, "Open", "AP-AGE", "Informational"],
        ["sales", "S-01", "2026-08-19", "4100", "INV-9918 Keystone Foods (billing voided)", "", VOID_JE_AMT, "Billing-void", "INV-9918", "Original billing remains in the ledger after customer cancellation"],
        ["sales", "S-02", "2026-08-26", "4100", "INV-9940 Susquehanna Water Authority", "", 88420.18, "Open", "INV-9940", "Valid sale"],
        ["payroll", "H-01", PERIOD, "2100", "Accrued payroll support", "", 151880.40, "Support", "PR-ACC", "Matches TB"],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def write_memo(path: Path) -> None:
    text = f"""{ENTITY_LEGAL}
Corporate Accounting — Month-End Flux & Adjusting Entry Policy
Effective for closes on or after 2026-01-01
Applies to: Lebanon, PA plant and corporate books
Contact: close-desk@haverford.example (internal)

1. Purpose
This memo sets the governing rules for August (and subsequent) soft closes. It tells the close desk which period-over-period movements require investigation, which support mismatches require adjusting journal entries (AJEs), how CapEx vs expense is decided, and how to label close readiness. Where plant commentary conflicts with this memo, this memo controls.

2. Hierarchy
(a) This memo and attached support schedules govern soft-close decisions.
(b) ERP trial-balance exports are the starting point for balances, not the final answer when support differs.
(c) Plant controller emails or "Plant_Notes" language that the TB is "clean" or that "no AJEs" are needed do not clear required investigations or AJEs under this memo.
(d) Relationship or operations narratives may explain volume, but they do not replace threshold tests or cut-off AJEs.

3. Flux investigation thresholds
Compare Current_TB natural-balance amounts to Prior_TB for the same account.

3.1 P&L accounts (Type = PL)
Investigate and document an explanation when BOTH are true:
- Absolute flux |August − July| is at least $15,000, AND
- Absolute flux is at least 10% of the absolute July balance (if July is zero, the percent test is treated as met whenever the absolute test is met).

3.2 Balance-sheet accounts (Type = BS)
Investigate and document an explanation when absolute flux is at least $25,000.

3.3 Documentation standard
Each investigated account needs a short cause statement tied to JE activity notes and/or support schedule lines. "Ops said it looks fine" is not sufficient.

4. Mandatory AJE categories (book even if flux is below threshold)
Propose AJEs before soft close when any of the following appear:

4.1 Voided billing still in GL
If billing voided an invoice but the original revenue and AR postings remain in the Current_TB, reverse the remaining GL amounts in full. Billing-void status alone is not a GL reverse.

4.2 Accrual true-ups to support
When Accrued Warranty, Accrued PTO, or Accrued Freight on the TB differs from the governing support ending balance or open-item total in the support schedules file, true the TB to support. Direction: reduce or increase the liability (and the matching expense) so the TB equals support.

4.3 Prepaid amortization
Commercial package insurance is amortized straight-line over twelve months. If the Current_TB prepaid balance shows no August amortization, book the monthly amount from the prepaid support schedule (annual premium / 12).

4.4 Inventory physical vs book
If physical inventory support total is below TB inventory, write the book balance down to physical through COGS (or inventory write-down expense mapped to 5100). Do not leave the difference as "monitoring."

4.5 CapEx vs maintenance
Capitalize a maintenance ticket to PP&E (account 1600) when ALL are true:
- Amount is at least $5,000, AND
- Useful life is greater than one year (per ticket / engineering note).
Routine consumables and sub-threshold work stay in Maintenance & Repairs (5600).
If a qualifying ticket was posted to 5600, reclassify to 1600; do not leave it in P&L.

5. Close readiness matrix
Assign exactly one status:

- Ready — No required AJEs under sections 4.1–4.5; all threshold flux items explained.
- Ready with AJEs — Required AJEs are identified and proposed in the close pack; soft close may proceed once those AJEs are posted.
- Hold close — Required AJEs cannot be quantified from available files, or a threshold flux item cannot be explained with available support.

A plant "clean close" note does not, by itself, produce Ready. Presence of flux explanations alone does not force Hold close if the AJE pack is complete.

6. Deliverable expectations (for the close pack workbook)
Corporate expects a workbook that includes: material flux workpaper, proposed AJEs with accounts and amounts, reconciliation notes citing support line IDs, the close-readiness status, and a short note on hierarchy when plant commentary conflicts with this memo.

7. Illustrative non-authoritative notes for August 2026
Operations mentioned higher maintenance around CNC spindle work and a late Keystone shipment. Those narratives may inform flux wording but do not override CapEx capitalization, void-JE reverse, warranty/PTO/freight true-ups, prepaid amort, or inventory write-down rules above. Soft-close calendar target remains {SOFT_CLOSE}.

8. Revision
Supersedes the February 2025 draft flux checklist. Do not use plant informal checklists that omit mandatory AJE categories.

— End of memo —
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def main() -> None:
    TASK_INPUTS.mkdir(parents=True, exist_ok=True)
    write_tb(TASK_INPUTS / TB_XLSX)
    write_support_csv(TASK_INPUTS / SUPPORT_CSV)
    write_memo(TASK_INPUTS / MEMO_TXT)
    print(f"Wrote inputs to {TASK_INPUTS}")


if __name__ == "__main__":
    main()
