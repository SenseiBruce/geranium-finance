#!/usr/bin/env python3
"""Generate inputs for Whitaker Precision Components loan underwriting."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter

from sanitize_office import sanitize_xlsx
from whitaker_constants import (
    APPLICATION_ID,
    AS_OF,
    BUILDING_RP_NOLV,
    CNC_DMG_NOLV,
    CNC_HAAS_NOLV,
    CNC_MAZAK_NOLV,
    COLLATERAL_CSV,
    COMMITTEE_DATE,
    ENTITY,
    ENTITY_LEGAL,
    EXISTING_ANNUAL_DS,
    EXISTING_DEBT_BAL,
    FIN_XLSX,
    FIXTURES_NOLV,
    FORKLIFT_LEASE_NOLV,
    FYE,
    MEMO_TXT,
    MGMT_EBITDA,
    OBSOLETE_NOLV,
    ONE_TIME_GAIN,
    OWNER_ADD_CLAIMED,
    RELATED_PARTY_RENT_ADD_CLAIMED,
    REPORTED_EBITDA,
    REQUESTED,
    REQUESTED_TENOR_MO,
    SLUG,
    SOFT_COST,
)

TASK_INPUTS = Path(__file__).resolve().parent.parent / "tasks" / SLUG / "inputs"

body = Font(name="Calibri", size=10)
header_font = Font(name="Calibri", size=10, bold=True)
title_font = Font(name="Calibri", size=13, bold=True)
thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
money_fmt = "#,##0.00"


def autosize(ws, max_w: int = 44) -> None:
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        width = min(max(len(str(c.value or "")) for c in col) + 2, max_w)
        ws.column_dimensions[letter].width = max(width, 10)


def write_financials(path: Path) -> None:
    wb = Workbook()

    # --- Application ---
    ws = wb.active
    ws.title = "Application"
    ws["A1"] = f"{ENTITY_LEGAL} — Commercial term loan application"
    ws["A1"].font = title_font
    rows = [
        ("Application ID", APPLICATION_ID),
        ("Borrower", ENTITY_LEGAL),
        ("NAICS", "332710 — Machine shops"),
        ("HQ / plant", "4418 Kishwaukee St, Rockford, IL 61109"),
        ("Request type", "Equipment term loan — CNC expansion cell"),
        ("Requested commitment (USD)", REQUESTED),
        ("Requested tenor (months)", REQUESTED_TENOR_MO),
        ("Requested amortization", "Level pay; interest floating SOFR+3.75%"),
        ("Use of proceeds", "Purchase Haas VF-4SS, DMG MORI NLX2500, Mazak Integrex i-200S; fixtures; install"),
        ("Financials as-of", AS_OF),
        ("Fiscal year end", FYE),
        ("Committee target", COMMITTEE_DATE),
        ("RM preliminary path", "Approve as requested"),
        ("RM stated DSCR", "1.60x on management EBITDA"),
        ("RM stated LTV basis", "Book cost of all pledged assets including building"),
        ("Guarantor offered", "None — borrower requests no PG"),
        ("Existing bank debt annual service", EXISTING_ANNUAL_DS),
        ("Existing bank debt UPB", EXISTING_DEBT_BAL),
    ]
    ws["A3"] = "Field"
    ws["B3"] = "Value"
    ws["A3"].font = header_font
    ws["B3"].font = header_font
    for i, (k, v) in enumerate(rows, 4):
        ws.cell(i, 1, k).font = body
        cell = ws.cell(i, 2, v)
        cell.font = body
        if isinstance(v, float):
            cell.number_format = money_fmt
    ws["A24"] = (
        "Borrower certification: figures on Income and Balance Sheet tabs are from "
        "internally prepared statements. One-time gain on vacant parcel sale in FY2025 "
        "is included in other income. Owner compensation add-backs and related-party "
        "rent normalization are detailed in RM Notes."
    )
    ws["A24"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A24:B28")
    autosize(ws)

    # --- Income ---
    ws = wb.create_sheet("Income")
    ws["A1"] = f"{ENTITY} — Income statement summary (USD)"
    ws["A1"].font = title_font
    headers = ["Line", "FY2023", "FY2024", "FY2025", "TTM to 2026-06-30", "Notes"]
    for c, h in enumerate(headers, 1):
        ws.cell(3, c, h).font = header_font
        ws.cell(3, c).border = thin
    income_rows = [
        ("Net sales", 8_220_418.55, 8_884_220.18, 9_412_880.40, 9_688_440.22, ""),
        ("COGS", 5_412_880.40, 5_780_220.18, 6_084_110.55, 6_220_880.40, ""),
        ("Gross profit", 2_807_538.15, 3_104_000.00, 3_328_769.85, 3_467_559.82, ""),
        ("SG&A (ex-D&A)", 1_684_220.18, 1_792_880.40, 1_884_220.55, 1_942_110.18, "Includes owner W-2"),
        ("Owner W-2 compensation", 312_880.40, 328_440.18, 341_220.55, 348_880.40, "RM proposes add-back"),
        ("Related-party rent (Whitaker Realty LLC)", 216_000.00, 228_000.00, 240_000.00, 240_000.00, "Above-market claim $96k"),
        ("EBITDA (reported)", 1_018_440.22, 1_142_880.55, REPORTED_EBITDA, 1_288_220.18, "FY2025 includes parcel gain"),
        ("Other income — parcel sale gain", 0.00, 0.00, ONE_TIME_GAIN, 0.00, "Vacant lot adjacent to plant"),
        ("Depreciation", 288_440.18, 312_880.40, 341_220.55, 352_110.22, ""),
        ("Interest expense", 168_220.55, 184_880.40, 198_440.18, 204_220.55, ""),
        ("Pretax income", 561_779.49, 645_119.77, 708_959.45, 731_889.41, ""),
        ("Management EBITDA (RM calc)", 1_214_440.22, 1_388_880.55, MGMT_EBITDA, 1_594_220.18, "Adds owner+rent; keeps gain"),
    ]
    for r, row in enumerate(income_rows, 4):
        for c, val in enumerate(row, 1):
            cell = ws.cell(r, c, val)
            cell.font = body
            cell.border = thin
            if c in (2, 3, 4, 5) and isinstance(val, float):
                cell.number_format = money_fmt
    ws["A18"] = (
        "RM Notes cross-ref: management EBITDA for FY2025 = reported EBITDA "
        f"+ owner add-back ${OWNER_ADD_CLAIMED:,.2f} + related-party rent add-back "
        f"${RELATED_PARTY_RENT_ADD_CLAIMED:,.2f}."
    )
    ws["A18"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A18:F20")
    autosize(ws)

    # --- Balance Sheet ---
    ws = wb.create_sheet("Balance_Sheet")
    ws["A1"] = f"{ENTITY} — Balance sheet excerpts (USD)"
    ws["A1"].font = title_font
    for c, h in enumerate(["Line", "FY2024", "FY2025", f"As of {AS_OF}", "Notes"], 1):
        ws.cell(3, c, h).font = header_font
        ws.cell(3, c).border = thin
    bs_rows = [
        ("Cash", 418_220.18, 386_880.40, 352_110.55, ""),
        ("AR net", 1_284_440.22, 1_412_880.55, 1_488_220.18, ""),
        ("Inventory", 922_880.40, 984_220.18, 1_012_440.55, "Not pledged for this facility"),
        ("Net PP&E", 3_884_220.18, 4_128_440.55, 4_412_880.40, "Includes building at book"),
        ("Total assets", 7_214_880.55, 7_688_440.22, 8_012_220.18, ""),
        ("AP / accrued", 688_440.18, 712_880.40, 744_220.55, ""),
        ("Current portion LTD", 312_880.40, 328_440.18, 341_220.55, ""),
        ("Long-term debt", 1_984_220.55, 2_012_880.40, EXISTING_DEBT_BAL, "Bank term + revolver"),
        ("Related-party note (Whitaker Realty)", 420_000.00, 380_000.00, 360_000.00, "Subordinated claim"),
        ("Equity", 3_809_339.42, 4_254_239.24, 4_382_779.08, ""),
    ]
    for r, row in enumerate(bs_rows, 4):
        for c, val in enumerate(row, 1):
            cell = ws.cell(r, c, val)
            cell.font = body
            cell.border = thin
            if c in (2, 3, 4) and isinstance(val, float):
                cell.number_format = money_fmt
    autosize(ws)

    # --- Debt Schedule ---
    ws = wb.create_sheet("Debt_Schedule")
    ws["A1"] = f"{ENTITY} — Existing debt schedule as of {AS_OF}"
    ws["A1"].font = title_font
    headers = [
        "Facility",
        "Lender",
        "UPB",
        "Rate",
        "Maturity",
        "Annual debt service",
        "Collateral",
        "Status",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(3, c, h).font = header_font
        ws.cell(3, c).border = thin
    debt_rows = [
        (
            "Term A — machinery",
            "First Mid Bank & Trust",
            1_284_220.18,
            "SOFR+2.85%",
            "2029-04-30",
            268_440.22,
            "Existing CNC / fixtures",
            "Current",
        ),
        (
            "Revolver",
            "First Mid Bank & Trust",
            612_880.40,
            "SOFR+2.50%",
            "2027-11-30",
            98_220.18,
            "AR / inventory blanket",
            "Current — $900k limit",
        ),
        (
            "Capex note — 2023 retrofit",
            "First Mid Bank & Trust",
            287_119.97,
            "5.85% fixed",
            "2028-08-15",
            46_220.00,
            "Specific equipment",
            "Current",
        ),
        (
            "Related-party note",
            "Whitaker Realty LLC",
            360_000.00,
            "4.00% fixed",
            "2031-12-31",
            0.00,
            "Unsecured / soft",
            "Interest deferred — not in bank DS",
        ),
    ]
    for r, row in enumerate(debt_rows, 4):
        for c, val in enumerate(row, 1):
            cell = ws.cell(r, c, val)
            cell.font = body
            cell.border = thin
            if c in (3, 6) and isinstance(val, float):
                cell.number_format = money_fmt
    ws["A9"] = "Bank annual debt service (ex-related-party)"
    ws["B9"] = EXISTING_ANNUAL_DS
    ws["B9"].number_format = money_fmt
    ws["A10"] = "Bank UPB total (ex-related-party)"
    ws["B10"] = EXISTING_DEBT_BAL
    ws["B10"].number_format = money_fmt
    # filler historical facilities
    ws["A12"] = "Closed / paid facilities (context only — not in DSCR)"
    ws["A12"].font = header_font
    closed = [
        ("PPP forgiveness residual", "SBA", 0.00, "n/a", "2022-06-30", 0.00, "n/a", "Closed"),
        ("Prior term 2018", "First Mid Bank & Trust", 0.00, "n/a", "2024-03-31", 0.00, "Released", "Paid"),
        ("Vehicle note F-250", "Ally", 0.00, "n/a", "2025-01-15", 0.00, "Released", "Paid"),
        ("Tooling vendor note", "Sandvik", 0.00, "n/a", "2023-09-30", 0.00, "n/a", "Paid"),
        ("Insurance premium finance", "AFCO", 0.00, "n/a", "2025-11-01", 0.00, "n/a", "Paid"),
        ("ERTC bridge (temp)", "First Mid Bank & Trust", 0.00, "n/a", "2023-02-28", 0.00, "n/a", "Paid"),
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(13, c, h).font = header_font
    for r, row in enumerate(closed, 14):
        for c, val in enumerate(row, 1):
            cell = ws.cell(r, c, val)
            cell.font = body
            if c in (3, 6) and isinstance(val, float):
                cell.number_format = money_fmt
    autosize(ws)

    # --- RM Notes ---
    ws = wb.create_sheet("RM_Notes")
    ws["A1"] = f"Relationship manager file notes — {APPLICATION_ID}"
    ws["A1"].font = title_font
    notes = [
        "2026-08-12 — Site visit. Shop floor busy on aerospace Tier-2 contracts. "
        "Borrower wants three new machines to take Mazak Integrex work currently farmed out.",
        "2026-08-18 — Borrower delivered internally prepared FY2025 pack. EBITDA looks strong. "
        f"I calculated management EBITDA at ${MGMT_EBITDA:,.2f} after adding owner compensation "
        f"(${OWNER_ADD_CLAIMED:,.2f}) and related-party rent normalization "
        f"(${RELATED_PARTY_RENT_ADD_CLAIMED:,.2f}). Parcel sale gain of ${ONE_TIME_GAIN:,.2f} "
        "stays in because cash was real.",
        "2026-08-22 — Collateral schedule from borrower includes the Rockford building titled "
        "in Whitaker Realty LLC (related). RM view: building support justifies full ask. "
        "Book-cost LTV under 65% if building included.",
        "2026-08-28 — PRELIMINARY RECOMMENDATION: Approve as requested at "
        f"${REQUESTED:,.2f} / {REQUESTED_TENOR_MO} months. DSCR approx 1.60x on management "
        "EBITDA vs bank DS + proposed. No personal guaranty required given equity and building.",
        "2026-09-02 — Credit policy memo circulated by Credit Admin. RM has not restated "
        "the recommendation; Application tab still shows Approve as requested.",
        "2026-09-05 — Soft costs (~install, freight, deposits) of about $95k are in the "
        "collateral schedule at cost. Borrower expects them in the advance.",
    ]
    for i, text in enumerate(notes, 3):
        ws.cell(i, 1, text).font = body
        ws.cell(i, 1).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 48
    ws.column_dimensions["A"].width = 110
    # depth filler emails
    fillers = [
        "Email 2026-07-14 — AR aging clean; no >90 past due over $25k.",
        "Email 2026-07-22 — Insurance binder renewal OK; loss runs clean 36 mo.",
        "Email 2026-08-01 — UCC search draft ordered on Whitaker Precision Components LLC.",
        "Email 2026-08-04 — Environmental Phase I not required (equipment-only pledge per RM).",
        "Email 2026-08-09 — Appraisal order placed with MidWest Machinery Appraisers (NOLV).",
        "Email 2026-08-15 — Appraisal received; values loaded to collateral CSV by analyst.",
        "Email 2026-08-19 — Tax returns FY2023-FY2024 match sales within 2%.",
        "Email 2026-08-25 — Customer concentration: top 3 = 41% of TTM sales.",
        "Email 2026-08-29 — Banking references satisfactory; NSF history none in 24 mo.",
        "Email 2026-09-01 — Flood zone determination N/A for equipment collateral.",
    ]
    ws["A10"] = "Supporting correspondence log (depth)"
    ws["A10"].font = header_font
    for i, t in enumerate(fillers, 11):
        ws.cell(i, 1, t).font = body

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    sanitize_xlsx(path)


def write_collateral(path: Path) -> None:
    headers = [
        "asset_id",
        "description",
        "category",
        "year",
        "book_cost",
        "appraisal_nolv",
        "pledged_flag",
        "rm_advance_pct",
        "title_holder",
        "notes",
    ]
    rows = [
        [
            "CNC-4418-01",
            "Haas VF-4SS vertical machining center (to be purchased)",
            "CNC_new",
            2026,
            "612880.40",
            f"{CNC_HAAS_NOLV:.2f}",
            "Y",
            "80",
            ENTITY_LEGAL,
            "Purchase order PO-8841; deposit in soft-cost line",
        ],
        [
            "CNC-4418-02",
            "DMG MORI NLX2500 turning center (to be purchased)",
            "CNC_new",
            2026,
            "788220.18",
            f"{CNC_DMG_NOLV:.2f}",
            "Y",
            "80",
            ENTITY_LEGAL,
            "PO-8842",
        ],
        [
            "CNC-4418-03",
            "Mazak Integrex i-200S multitasking (to be purchased)",
            "CNC_new",
            2026,
            "912440.55",
            f"{CNC_MAZAK_NOLV:.2f}",
            "Y",
            "80",
            ENTITY_LEGAL,
            "PO-8843; longest lead item",
        ],
        [
            "FIX-4418-10",
            "Workholding fixtures / tombstones package",
            "Fixtures",
            2026,
            "248880.40",
            f"{FIXTURES_NOLV:.2f}",
            "Y",
            "70",
            ENTITY_LEGAL,
            "RM advance 70% — policy may differ",
        ],
        [
            "BLD-ROCK-01",
            "Plant building 4418 Kishwaukee St",
            "RealEstate_related",
            1998,
            "2140220.18",
            f"{BUILDING_RP_NOLV:.2f}",
            "Y",
            "65",
            "Whitaker Realty LLC",
            "Related-party title; RM treats as support collateral",
        ],
        [
            "MILL-1998-04",
            "Bridgeport Series I standard mill",
            "Obsolete_manual",
            1998,
            "18440.22",
            f"{OBSOLETE_NOLV:.2f}",
            "Y",
            "25",
            ENTITY_LEGAL,
            "Age exceeds equipment advance schedule",
        ],
        [
            "SOFT-4418",
            "Install / freight / deposits pool",
            "SoftCost",
            2026,
            f"{SOFT_COST:.2f}",
            f"{SOFT_COST:.2f}",
            "Y",
            "100",
            ENTITY_LEGAL,
            "Borrower wants 100% advance on soft costs",
        ],
        [
            "FL-LEASE-02",
            "Toyota 8FGU25 forklift",
            "Leased_equipment",
            2022,
            "0.00",
            f"{FORKLIFT_LEASE_NOLV:.2f}",
            "Y",
            "50",
            "Toyota Industries Finance",
            "Operating lease — not owned",
        ],
        # depth / noise — existing owned equipment (already encumbered; context)
        [
            "CNC-EXIST-11",
            "Haas VF-2SS (existing)",
            "CNC_existing_encumbered",
            2019,
            "142880.40",
            "88420.18",
            "N",
            "0",
            ENTITY_LEGAL,
            "Already pledged to Term A — not for new facility",
        ],
        [
            "CNC-EXIST-12",
            "Doosan Puma 2600 (existing)",
            "CNC_existing_encumbered",
            2018,
            "168220.55",
            "96220.40",
            "N",
            "0",
            ENTITY_LEGAL,
            "Term A collateral",
        ],
        [
            "CNC-EXIST-14",
            "Okuma GENOS M560-V (existing)",
            "CNC_existing_encumbered",
            2020,
            "198440.18",
            "124880.55",
            "N",
            "0",
            ENTITY_LEGAL,
            "Term A collateral",
        ],
        [
            "CNC-EXIST-15",
            "Mazak QT-250MY (existing)",
            "CNC_existing_encumbered",
            2017,
            "154220.18",
            "71220.40",
            "N",
            "0",
            ENTITY_LEGAL,
            "Term A collateral",
        ],
        [
            "FIX-EXIST-22",
            "Legacy fixture crib",
            "Fixtures_encumbered",
            2016,
            "62440.18",
            "18820.55",
            "N",
            "0",
            ENTITY_LEGAL,
            "Term A",
        ],
        [
            "QC-CMM-01",
            "Hexagon CMM",
            "QC_encumbered",
            2021,
            "88420.40",
            "51220.18",
            "N",
            "0",
            ENTITY_LEGAL,
            "Capex note collateral",
        ],
        [
            "COMP-AIR-03",
            "Atlas Copco compressor",
            "Plant_support",
            2015,
            "41220.18",
            "12440.55",
            "N",
            "0",
            ENTITY_LEGAL,
            "Not requested for new pledge",
        ],
        [
            "VEH-F150",
            "Ford F-150 shop truck",
            "Vehicle",
            2021,
            "38440.22",
            "18420.18",
            "N",
            "0",
            ENTITY_LEGAL,
            "Excluded from industrial advance",
        ],
        [
            "IT-SRV-01",
            "Shopfloor server rack",
            "IT",
            2023,
            "22480.40",
            "8840.22",
            "N",
            "0",
            ENTITY_LEGAL,
            "Excluded",
        ],
        [
            "TOOL-CRIB",
            "Consumable tooling inventory",
            "Inventory",
            2026,
            "112880.55",
            "112880.55",
            "N",
            "0",
            ENTITY_LEGAL,
            "Revolver blanket — not this term loan",
        ],
        [
            "WIP-FLOOR",
            "WIP / finished goods",
            "Inventory",
            2026,
            "288440.18",
            "288440.18",
            "N",
            "0",
            ENTITY_LEGAL,
            "Revolver blanket",
        ],
        [
            "LAND-VACANT",
            "Vacant parcel sold FY2025 (historical)",
            "RealEstate_sold",
            1998,
            "0.00",
            "0.00",
            "N",
            "0",
            "n/a",
            "Gain already recognized; not collateral",
        ],
        [
            "CNC-QUOTE-99",
            "Optional 4th machine (not in request)",
            "CNC_optional",
            2026,
            "540220.18",
            "410880.40",
            "N",
            "0",
            ENTITY_LEGAL,
            "Borrower may add later — out of scope",
        ],
        [
            "LEASEHOLD-IMP",
            "Leasehold paint / epoxy (related building)",
            "Leasehold",
            2019,
            "88420.18",
            "22440.55",
            "Y",
            "40",
            "Whitaker Realty LLC",
            "Improvements on related-party realty",
        ],
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def write_memo(path: Path) -> None:
    text = f"""
CREDIT ADMINISTRATION — POLICY AND EXCEPTION MEMO
Commercial Equipment Term Loans | Mid-Market Manufacturing
Effective for committee packages on or after 2026-09-01
Applies to: {ENTITY_LEGAL} application {APPLICATION_ID}

1. Purpose and governing hierarchy
This memo states the credit policy tests Credit Administration expects on equipment
term loan recommendations. Where relationship-manager file notes, borrower
application narratives, or informal "approved in principle" language conflict with
this memo, this memo governs for committee use. Preliminary RM path labels are not
binding determinations.

2. Facility in scope
New commercial equipment term loans secured primarily by machinery and fixtures
being financed. Real estate titled outside the borrower, leased equipment, inventory,
and soft costs are outside the standard advance framework for this product.

3. EBITDA adjustments (mandatory)
Start from reported EBITDA on the borrower's income statement for the latest full
fiscal year unless Credit Administration directs use of a defined TTM. Then:
(a) Subtract one-time gains and non-operating gains embedded in reported EBITDA,
    including gains on sales of real estate parcels or idle assets.
(b) Add owner compensation only to the extent documented excess over peer W-2 for
    the role. For Illinois machine shops under $12m sales, the documented excess
    add-back for this file is capped at $84,220.55. Larger "management" add-backs
    on RM notes are not accepted without a separate exception memo from Credit
    Administration (none is on file for {APPLICATION_ID}).
(c) Do not add back related-party rent. Rent paid to a related realty entity is a
    continuing cash cost of the operating company even if the RM labels a portion
    "above market." Related-party rent normalization requires an approved appraisal
    of market rent and a written Credit Administration exception; none is present.
Adjusted EBITDA from these rules is the sole EBITDA measure for DSCR and leverage.

4. Debt service measurement
Existing bank annual debt service equals the sum of scheduled principal and interest
on bank facilities excluding related-party notes that are contractually deferred and
expressly subordinated (confirm on the debt schedule).
Proposed annual debt service for pricing used on this desk equals:
    monthly payment = (commitment_usd / 1000) × {16.42}
    annual debt service = monthly payment × 12
rounded to cents at each step. Use this factor for SOFR+3.75% seven-year level-pay
indicative pricing when comparing paths. Do not invent an alternate amortization
schedule for the policy test.

5. DSCR and leverage tests
DSCR = Adjusted EBITDA / (existing bank annual debt service + proposed annual debt
service on the commitment being tested).
Minimum DSCR for unrestricted Approve: 1.25x.
If DSCR on the full requested commitment is below 1.25x but at least 1.15x, the
file may proceed only as Approve with conditions after sizing (Section 7).
If DSCR remains below 1.15x even at the binding maximum commitment, Decline.
Leverage = (existing bank UPB + proposed commitment) / Adjusted EBITDA.
Maximum leverage: 3.50x at the commitment recommended to committee.

6. Collateral eligibility and advances
Eligible collateral for this product: borrower-owned CNC equipment and fixtures
being financed, valued at appraisal net orderly liquidation value (NOLV), not book
cost. Ineligible regardless of RM pledge flags:
    - Real estate titled in a related party (including Whitaker Realty LLC)
    - Leasehold improvements on related-party realty
    - Equipment on operating lease (lessor title)
    - Manual machine tools beyond the age cutoff on the equipment advance schedule
      (generally pre-2005 Bridgeport-class mills for this desk)
    - Soft costs: freight, installation, deposits, training, software subscriptions
    - Inventory and AR (covered by revolver product, not this term loan)
    - Assets already pledged and required for existing Term A / capex notes
Advance rates on eligible NOLV:
    - New CNC in purchase contracts: 80%
    - Fixtures / workholding packaged with the CNC purchase: 50%
    - RM-proposed advance percentages that exceed these rates do not control
Bankable collateral = sum over eligible assets of (NOLV × category advance rate),
rounding each asset advance to cents before summing.

7. LTV and binding maximum commitment
LTV = proposed commitment / eligible NOLV (eligible assets only; NOLV basis).
Maximum LTV: 75%.
Binding maximum commitment = the lesser of (a) bankable collateral and (b) 75% of
eligible NOLV. If the borrower requested amount exceeds the binding maximum, do not
Approve the full ask. Size the commitment to the binding maximum and apply the
Conditional path in Section 8 when DSCR/LTV at the full ask fail but pass after sizing.

8. Path matrix (Approve / Approve with conditions / Decline)
Approve: full requested commitment passes DSCR ≥ 1.25x, LTV ≤ 75%, leverage ≤ 3.50x,
and collateral is limited to eligible assets.
Approve with conditions: full ask fails DSCR or LTV, but after sizing to the binding
maximum commitment the file passes DSCR ≥ 1.25x, LTV ≤ 75%, and leverage ≤ 3.50x.
Required conditions for Conditional equipment term loans on this desk:
    - Commitment capped at binding maximum
    - Tenor shortened to 60 months (from 84) unless Credit Administration waives
    - Unlimited personal guaranty of the principal owner
    - Affirmative quarterly DSCR covenant at 1.25x tested on Adjusted EBITDA
    - Explicit exclusion of related-party realty and soft costs from the pledge
Decline: even at binding maximum, DSCR < 1.15x, or leverage > 3.50x, or eligible
collateral cannot support a commitment that clears the floor tests.
Do not Decline solely because the requested amount exceeds bankable collateral when
a sized Conditional commitment would clear the tests. Do not Approve the full
requested amount when LTV or DSCR at the ask fail.

9. Authority
Officer authority for equipment term loans is $2,000,000. Conditional path files and
any file that required sizing under Section 7 still go to committee with a written
recommendation even when the sized commitment is under officer authority.

10. Documentation expectations for the decision workbook
Committee expects a single workbook that rebuilds Adjusted EBITDA, tests DSCR and
leverage at the full ask and at the sized commitment, shows eligible vs ineligible
collateral with bankable advances, states the path, states the commitment, and lists
conditions when Conditional. Cite the input filenames that supply each material fact.

11. Items expressly out of scope for this memo
This memo does not re-open existing Term A covenants, does not set deposit pricing,
and does not authorize an exception for related-party rent add-backs on {APPLICATION_ID}.

Prepared by: Credit Administration, Mid-Market Manufacturing desk
Distribution: Committee packet preparers; relationship managers (informational)
""".strip()

    # Ensure depth ≥500 words
    words = len(text.split())
    if words < 500:
        raise SystemExit(f"memo too short: {words} words")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    print(f"Wrote memo ({words} words)")


def main() -> None:
    TASK_INPUTS.mkdir(parents=True, exist_ok=True)
    fin = TASK_INPUTS / FIN_XLSX
    col = TASK_INPUTS / COLLATERAL_CSV
    memo = TASK_INPUTS / MEMO_TXT
    write_financials(fin)
    write_collateral(col)
    write_memo(memo)
    print(f"Wrote {fin}")
    print(f"Wrote {col}")
    print(f"Wrote {memo}")


if __name__ == "__main__":
    main()
