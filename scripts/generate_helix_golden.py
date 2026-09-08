#!/usr/bin/env python3
"""Generate golden workbook for helix-biotech-valuation."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from helix_constants import (
    BRIEF_RUN_RATE,
    FCF_MARGIN,
    FD_PRE,
    FORECAST_GROWTH,
    FOUNDERS_FD,
    LEAD_INVESTOR,
    MODEL_ARR_NORMALIZED,
    MULT_DOWN,
    MULT_HIGH,
    MULT_LOW,
    PENDING_CUSTOMER,
    PENDING_RENEWAL_ARR,
    POOL_TARGET_PCT,
    POST_MONEY,
    PRE_MONEY,
    PRIMARY,
    ROLLUP_2024,
    ROLLUP_TTM_2024,
    SAFE_BIRCHWOOD,
    SAFE_STONEGATE,
    SAFE1_CAP,
    SAFE1_DISC,
    SAFE1_INVEST,
    SAFE2_CAP,
    SAFE2_INVEST,
    SERIES_A_INVESTOR,
    SERIES_A_PRICE,
    SERIES_A_SHARES,
    TERMINAL_GROWTH,
    WACC_HIGH,
    WACC_LOW,
)
from sanitize_office import cache_xlsx_formula_values, sanitize_xlsx

TASK = Path(__file__).resolve().parent.parent / "tasks" / "helix-biotech-valuation"
INPUTS = TASK / "inputs"
OUT = TASK / "golden" / "valuation_draft.xlsx"

PEER_MEDIAN_MULTIPLE = 6.1
BASE_NRR = 1.08
SENS_NRRS = (1.05, 1.08, 1.11)
SENS_GROWTHS = (0.22, 0.28, 0.34)

THIN = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
HEADER_FONT = Font(bold=True, color="1F1F1F")
SECTION_FONT = Font(bold=True, size=12, color="1F1F1F")
# Conventional financial-model cues: blue = hardcoded input, black = local formula,
# green = cross-sheet link. Light fills reinforce the distinction without dashboard chrome.
INPUT_FONT = Font(color="0000FF")
FORMULA_FONT = Font(color="000000")
LINK_FONT = Font(color="006600")
INPUT_FILL = PatternFill("solid", fgColor="DDEBF7")
FORMULA_FILL = PatternFill("solid", fgColor="FFF2CC")
LINK_FILL = PatternFill("solid", fgColor="E2EFDA")
HEADER_FILL = PatternFill("solid", fgColor="D9D9D9")
SECTION_FILL = PatternFill("solid", fgColor="F2F2F2")
TOTAL_FILL = PatternFill("solid", fgColor="FCE4D6")
WRAP = Alignment(wrap_text=True, vertical="top")
# Cap-table pre-round holders from cap_table.csv (FD treatment; Ruiz exercised
# 42k already in Employee exercises YTD — only 43k unexercised remain in FD).
INDIVIDUAL_PRE_ROUND: list[tuple[str, str, float, str]] = [
    ("Jane Okonkwo", "Common", 4_200_000, "cap_table.csv — co-founder CEO"),
    ("Marcus Chen", "Common", 3_800_000, "cap_table.csv — co-founder CTO"),
    ("Employee exercises (YTD)", "Common", 118_400, "cap_table.csv — routine option exercises"),
    ("Treasury shares", "Common", 24_000, "cap_table.csv — repurchase reserve"),
    ("Employee stock purchase", "Common", 48_200, "cap_table.csv — ESPP Q3 2024"),
    (
        "Dr. Elena Ruiz",
        "Advisor Warrant (unexercised FD)",
        43_000,
        "cap_table.csv — 43,000 unexercised in FD (42,000 exercised already in Employee exercises YTD)",
    ),
    ("Strategic partner warrant", "Warrant", 150_000, "cap_table.csv — LabCorp partnership"),
]


def money(value: float) -> float:
    return round(float(value), 2)


def ratio(value: float) -> float:
    return round(float(value), 8)


def load_cap_table() -> list[dict[str, str]]:
    with (INPUTS / "cap_table.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def existing_option_pool() -> float:
    """Stock-plan option inventory only (excludes advisor warrants / other FD securities)."""
    pool = 0.0
    for row in load_cap_table():
        if row["security_type"] == "Options" and row["vesting_status"] != "pool":
            pool += float(row["shares"] or 0)
    return pool


def advisor_warrant_unexercised() -> float:
    """Dr. Ruiz unexercised advisor warrant shares included in FD but not in option-pool base."""
    for row in load_cap_table():
        if row["holder"] == "Dr. Elena Ruiz" and row["security_type"] == "Advisor Warrant":
            return 43_000.0
    return 0.0


def safe1_shares(pps: float, fd_pre: float) -> float:
    return SAFE1_INVEST / min(SAFE1_CAP / fd_pre, pps * (1 - SAFE1_DISC))


def safe2_shares(pps: float, fd_pre: float) -> float:
    return SAFE2_INVEST / (SAFE2_CAP / fd_pre)


def compute_cap_table() -> dict[str, float]:
    """Whole-share issuance: ROUND conversion / primary / pool refresh before FD totals."""
    fd_pre = FD_PRE
    existing_pool = existing_option_pool()
    pps = PRE_MONEY / fd_pre
    lockwood_prorata_invest = PRIMARY * SERIES_A_SHARES / fd_pre
    summit_invest = PRIMARY - lockwood_prorata_invest
    # Match Excel ROUND((primary×SA/FD)/pps,0) ≡ ROUND(primary×SA/pre,0)
    lockwood_prorata_shares = float(round(PRIMARY * SERIES_A_SHARES / PRE_MONEY, 0))
    summit_shares = float(round(PRIMARY * (fd_pre - SERIES_A_SHARES) / PRE_MONEY, 0))
    s1 = float(round(safe1_shares(pps, fd_pre), 0))
    s2 = float(round(safe2_shares(pps, fd_pre), 0))
    fd_mid = fd_pre + s1 + s2 + lockwood_prorata_shares + summit_shares
    pool_refresh = float(
        round(max((POOL_TARGET_PCT * fd_mid - existing_pool) / (1 - POOL_TARGET_PCT), 0), 0)
    )
    fd_post = fd_mid + pool_refresh
    pool_refresh_12 = float(round(max((0.12 * fd_mid - existing_pool) / (1 - 0.12), 0), 0))
    fd_post_12 = fd_mid + pool_refresh_12
    return {
        "fd_pre": fd_pre,
        "existing_pool": existing_pool,
        "pps": pps,
        "lockwood_prorata_invest": lockwood_prorata_invest,
        "summit_invest": summit_invest,
        "lockwood_prorata_shares": lockwood_prorata_shares,
        "summit_shares": summit_shares,
        "s1": s1,
        "s2": s2,
        "fd_mid": fd_mid,
        "pool_refresh": pool_refresh,
        "fd_post": fd_post,
        "pool_pct": (existing_pool + pool_refresh) / fd_post,
        "pool_refresh_12": pool_refresh_12,
        "fd_post_12": fd_post_12,
        "pool_pct_12": (existing_pool + pool_refresh_12) / fd_post_12,
    }


def compute_forecast(model_arr: float) -> list[float]:
    arr = model_arr
    out = [model_arr]
    for g in FORECAST_GROWTH:
        arr *= 1 + g
        out.append(arr)
    return out


def compute_dcf(forecast_arr: list[float], wacc: float) -> float:
    pv = 0.0
    for year, arr in enumerate(forecast_arr[1:], start=1):
        fcf = arr * FCF_MARGIN
        pv += fcf / ((1 + wacc) ** year)
    fcf5 = forecast_arr[5] * FCF_MARGIN
    terminal = fcf5 * (1 + TERMINAL_GROWTH) / (wacc - TERMINAL_GROWTH)
    pv += terminal / ((1 + wacc) ** 5)
    return pv


def source_cohort_inventory() -> list[dict[str, object]]:
    """
    Load Cohort Detail inventory for the model:

    - all unique 2024 calendar-quarter rows (eight records)
    - the flagged FY2023-Q2 duplicate expansion row (excluded from totals)

    Preserves the source fiscal→calendar mapping; does not restamp quarters.
    """
    wb = load_workbook(INPUTS / "cohort_summary.xlsx", data_only=True, read_only=True)
    ws = wb["Cohort Detail"]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    idx = {name: i for i, name in enumerate(headers)}
    inventory: list[dict[str, object]] = []
    for raw in ws.iter_rows(min_row=2, values_only=True):
        vintage = raw[idx["cohort_vintage"]]
        quarter = raw[idx["calendar_quarter"]]
        notes = raw[idx["notes"]] or ""
        is_duplicate = "DUPLICATE" in str(notes).upper()
        is_2024 = str(quarter).startswith("2024")
        if not (is_2024 or is_duplicate):
            continue
        start = float(raw[idx["starting_arr"]])
        gr = float(raw[idx["gross_retention_pct"]])
        exp = float(raw[idx["expansion_arr"]])
        churn_raw = raw[idx["churn_arr"]]
        churn = float(churn_raw) if churn_raw not in (None, "") else 0.0
        ending = start * gr / 100.0 + exp - churn
        include = 0 if is_duplicate else 1
        reason = (
            "EXCLUDED — duplicate FY2023-Q2 expansion already captured on prior line"
            if is_duplicate
            else "RETAINED — unique 2024 calendar-quarter cohort record"
        )
        inventory.append(
            {
                "vintage": vintage,
                "quarter": quarter,
                "starting_arr": start,
                "gross_retention_pct": gr,
                "expansion_arr": exp,
                "churn_arr": churn,
                "ending_arr": ending,
                "include": include,
                "exclusion_reason": reason,
                "source_notes": str(notes) if notes else "",
            }
        )
    wb.close()
    retained = [r for r in inventory if r["include"] == 1]
    excluded = [r for r in inventory if r["include"] == 0]
    if len(retained) != 8:
        raise ValueError(f"Expected 8 unique 2024 Cohort Detail rows, found {len(retained)}")
    if len(excluded) != 1:
        raise ValueError(f"Expected 1 duplicate exclusion row, found {len(excluded)}")
    # Stable order: 2024 retained by calendar quarter then vintage, duplicate last.
    retained.sort(key=lambda r: (str(r["quarter"]), str(r["vintage"])))
    return retained + excluded


def apply_number_format(cell, fmt: str) -> None:
    if cell.value is not None and cell.value != "":
        cell.number_format = fmt


def _is_formula(value: object) -> bool:
    return isinstance(value, str) and value.startswith("=")


def _is_cross_sheet(value: object) -> bool:
    return _is_formula(value) and ("!" in value or "'" in value)


def style_value_cell(cell, *, kind: str | None = None) -> None:
    """Mark inputs / local formulas / cross-sheet links for financial-model readability."""
    value = cell.value
    if value is None or value == "":
        return
    if kind is None:
        if not _is_formula(value):
            kind = "input"
        elif _is_cross_sheet(value):
            kind = "link"
        else:
            kind = "formula"
    if kind == "input":
        cell.font = INPUT_FONT
        cell.fill = INPUT_FILL
    elif kind == "link":
        cell.font = LINK_FONT
        cell.fill = LINK_FILL
    else:
        cell.font = FORMULA_FONT
        cell.fill = FORMULA_FILL


def style_header_row(ws, row: int = 1) -> None:
    for cell in ws[row]:
        if cell.value is not None:
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = THIN


def style_section_label(cell, text: str) -> None:
    cell.value = text
    cell.font = SECTION_FONT
    cell.fill = SECTION_FILL
    cell.alignment = Alignment(vertical="center")


def autosize(ws, min_width: float = 12, max_width: float = 48, notes_col: str | None = None) -> None:
    for column in ws.columns:
        letter = get_column_letter(column[0].column)
        if notes_col and letter == notes_col:
            ws.column_dimensions[letter].width = 110
            continue
        lengths = []
        for cell in column:
            if cell.value is None:
                continue
            text = str(cell.value)
            lengths.append(min(len(text), 60))
        width = max(lengths) + 2 if lengths else min_width
        ws.column_dimensions[letter].width = max(min_width, min(width, max_width))


def build() -> None:
    cap = compute_cap_table()
    model_arr = money(MODEL_ARR_NORMALIZED)
    forecast = compute_forecast(model_arr)
    ntm_arr = money(forecast[1])
    mult_low_val = money(ntm_arr * MULT_LOW)
    mult_high_val = money(ntm_arr * MULT_HIGH)
    downside_ev = money(model_arr * MULT_DOWN)
    dcf_ev_high = compute_dcf(forecast, WACC_LOW)
    dcf_ev_low = compute_dcf(forecast, WACC_HIGH)
    mult_mid = money((mult_low_val + mult_high_val) / 2)
    dcf_mid = money((dcf_ev_high + dcf_ev_low) / 2)
    peer_base = money(ntm_arr * PEER_MEDIAN_MULTIPLE)
    inventory = source_cohort_inventory()
    retained_rows = [r for r in inventory if r["include"] == 1]

    wb = Workbook()

    # --- Assumptions (inputs + formula links to upstream calc sheets) ---
    asm = wb.active
    asm.title = "Assumptions"
    asm["A1"] = "Helix Biotech — Series B model inputs"
    asm["A1"].font = HEADER_FONT
    asm["B1"] = "Value"
    asm["B1"].font = HEADER_FONT

    # Row map is fixed so other sheets can reference by number after formulas are written.
    # True inputs first; derived values use formulas pointing at Cohort Build / Forecast / Cap / Pools.
    asm["A3"] = "Pre-money valuation"
    asm["B3"] = PRE_MONEY
    asm["A4"] = "Primary proceeds (total)"
    asm["B4"] = PRIMARY
    asm["A5"] = "Post-money (before pool refresh)"
    asm["B5"] = POST_MONEY
    asm["A6"] = "Calendar-quarter TTM rollup (2024-Q1:Q4)"
    asm["B6"] = "='Cohort Build'!B14"  # derived from rollup block
    asm["A7"] = f"Pending renewal excluded ({PENDING_CUSTOMER})"
    asm["B7"] = PENDING_RENEWAL_ARR
    asm["A8"] = "Model ARR (TTM, normalized per Footnote 1)"
    asm["B8"] = "='Cohort Build'!B15"
    asm["A9"] = "Model NTM ARR (Y1 / 28% growth per Footnote 3)"
    asm["B9"] = "='Revenue Forecast'!C3"
    asm["A10"] = "Brief headline run-rate (not used for model)"
    asm["B10"] = BRIEF_RUN_RATE
    asm["A11"] = "Series B price per share"
    asm["B11"] = "=B3/B12"
    asm["A12"] = "FD shares pre-money (cap_table.csv total)"
    asm["B12"] = FD_PRE
    asm["A13"] = "FD shares mid (pre-pool refresh)"
    asm["B13"] = "=B12+B19+B20+B21+B22"
    asm["A14"] = "Founders/employees FD subtotal (cap_table.csv)"
    asm["B14"] = FOUNDERS_FD
    asm["A15"] = f"{SERIES_A_INVESTOR} Series A shares"
    asm["B15"] = SERIES_A_SHARES
    asm["A16"] = f"{SERIES_A_INVESTOR} Series A price"
    asm["B16"] = SERIES_A_PRICE
    asm["A17"] = f"{SAFE_BIRCHWOOD} SAFE invested"
    asm["B17"] = SAFE1_INVEST
    asm["A18"] = f"{SAFE_STONEGATE} SAFE invested"
    asm["B18"] = SAFE2_INVEST
    asm["A19"] = f"{SAFE_BIRCHWOOD} SAFE conversion shares"
    # Cap price vs discounted Series B price (lower governs); whole-share issuance; MFN outstanding
    asm["B19"] = "=ROUND(B17/B43,0)"
    asm["A20"] = f"{SAFE_STONEGATE} SAFE conversion shares"
    asm["B20"] = f"=ROUND(B18/({SAFE2_CAP}/B12),0)"
    asm["A21"] = f"{SERIES_A_INVESTOR} Series B pro-rata shares"
    asm["B21"] = "=ROUND((B4*B15/B12)/B11,0)"
    asm["A22"] = f"{LEAD_INVESTOR} Series B lead shares"
    asm["B22"] = "=ROUND((B4-B4*B15/B12)/B11,0)"
    asm["A23"] = "Existing stock-plan option pool (allocated Options rows)"
    asm["B23"] = round(cap["existing_pool"], 0)
    asm["A24"] = "Option pool refresh shares (15% board case)"
    asm["B24"] = "='Option pool cases'!D3"
    asm["A25"] = "Option pool refresh shares (12% counsel case)"
    asm["B25"] = "='Option pool cases'!D2"
    asm["A26"] = "Post-money option pool target"
    asm["B26"] = POOL_TARGET_PCT
    asm["A27"] = "Counsel side-letter pool reference"
    asm["B27"] = 0.12
    asm["A28"] = f"{SAFE_BIRCHWOOD} MFN clause"
    asm["B28"] = (
        "Outstanding / unresolved per cap_table.csv and investor_brief.txt; "
        "no separately confirmed alternative MFN term in the source materials"
    )
    asm["A29"] = f"{SAFE_BIRCHWOOD} conversion treatment"
    asm["B29"] = (
        f"{SAFE_BIRCHWOOD} SAFE is modeled at the valuation-cap price for the base case "
        f"because the ${SAFE1_CAP / 1_000_000:.1f}M cap price is below the "
        f"{int(SAFE1_DISC * 100)}%-discounted Series B price. "
        "The MFN remains an outstanding diligence item and is not treated as cleared."
    )
    asm["A30"] = "FCF margin (Footnote 3)"
    asm["B30"] = FCF_MARGIN
    asm["A31"] = "NTM multiple — low"
    asm["B31"] = MULT_LOW
    asm["A32"] = "NTM multiple — high"
    asm["B32"] = MULT_HIGH
    asm["A33"] = "TTM downside multiple"
    asm["B33"] = MULT_DOWN
    asm["A34"] = "Peer median NTM multiple (sensitivity)"
    asm["B34"] = PEER_MEDIAN_MULTIPLE
    asm["A35"] = "Trailing cohort NRR diagnostic (not stacked onto Footnote 3 total growth)"
    asm["B35"] = BASE_NRR
    asm["A36"] = "DCF WACC low (high-EV case)"
    asm["B36"] = WACC_LOW
    asm["A37"] = "DCF WACC high (low-EV case)"
    asm["B37"] = WACC_HIGH
    asm["A38"] = "Terminal growth"
    asm["B38"] = TERMINAL_GROWTH
    asm["A39"] = "Y1 total ARR growth (Footnote 3 — total path, not additive to absolute NRR)"
    asm["B39"] = FORECAST_GROWTH[0]
    asm["A40"] = "Post-money FD shares (15% pool case)"
    asm["B40"] = "='Option pool cases'!E3"
    # Transparent SAFE price ladder (appended; does not renumber upstream refs)
    asm["A41"] = f"{SAFE_BIRCHWOOD} valuation-cap price"
    asm["B41"] = f"={SAFE1_CAP}/B12"
    asm["A42"] = f"{SAFE_BIRCHWOOD} discounted Series B price"
    asm["B42"] = f"=B11*(1-{SAFE1_DISC})"
    asm["A43"] = f"{SAFE_BIRCHWOOD} applicable conversion price (lower of cap vs discount)"
    asm["B43"] = "=MIN(B41,B42)"
    asm["A44"] = "Existing stock-plan option pool (excludes advisor warrant)"
    asm["B44"] = "=B23"
    asm["A45"] = "Dr. Elena Ruiz unexercised advisor warrant (FD, not pool)"
    asm["B45"] = advisor_warrant_unexercised()
    asm["A46"] = "Forecast retention stress scalar (1.00 = base Footnote 3 path; not absolute NRR)"
    asm["B46"] = 1.0
    asm["A47"] = "Ending-ARR definition (Cohort Build)"
    asm["B47"] = (
        "ending_arr = starting_arr × gross_retention_pct/100 + expansion_arr − churn_arr; "
        "gross_retention_pct is starting ARR retained before expansion and churn "
        "(cohort_summary.xlsx Definitions) — churn is applied once via −churn_arr"
    )

    for addr, fmt in {
        "B3": '"$"#,##0',
        "B4": '"$"#,##0',
        "B5": '"$"#,##0',
        "B6": '"$"#,##0.00',
        "B7": '"$"#,##0',
        "B8": '"$"#,##0.00',
        "B9": '"$"#,##0.00',
        "B10": '"$"#,##0',
        "B11": '"$"#,##0.0000',
        "B12": "#,##0",
        "B13": "#,##0",
        "B14": "#,##0",
        "B15": "#,##0",
        "B16": '"$"#,##0.00',
        "B17": '"$"#,##0',
        "B18": '"$"#,##0',
        "B19": "#,##0",
        "B20": "#,##0",
        "B21": "#,##0",
        "B22": "#,##0",
        "B23": "#,##0",
        "B24": "#,##0",
        "B25": "#,##0",
        "B26": "0%",
        "B27": "0%",
        "B30": "0%",
        "B31": '0.0"x"',
        "B32": '0.0"x"',
        "B33": '0.0"x"',
        "B34": '0.0"x"',
        "B35": "0.00",
        "B36": "0%",
        "B37": "0%",
        "B38": "0%",
        "B39": "0%",
        "B40": "#,##0",
        "B41": '"$"#,##0.0000',
        "B42": '"$"#,##0.0000',
        "B43": '"$"#,##0.0000',
        "B44": "#,##0",
        "B45": "#,##0",
        "B46": "0.00",
    }.items():
        apply_number_format(asm[addr], fmt)
        style_value_cell(asm[addr])
    # Legend for input vs formula treatment
    asm["A49"] = "Formatting legend"
    style_section_label(asm["A49"], "Formatting legend")
    asm["A50"] = "Blue fill / blue font"
    asm["B50"] = "Hardcoded source inputs (transaction terms, caps, rates, share bases)"
    style_value_cell(asm["B50"], kind="input")
    asm["A51"] = "Yellow fill / black font"
    asm["B51"] = "Local calculated formulas (prices, conversion shares, ownership math)"
    style_value_cell(asm["B51"], kind="formula")
    asm["A52"] = "Green fill / green font"
    asm["B52"] = "Cross-sheet links (cohort ARR, forecast, option-pool cases)"
    style_value_cell(asm["B52"], kind="link")
    asm["A53"] = "Whole-share policy"
    asm["B53"] = (
        "SAFE conversion shares, Series B primary shares, and option-pool refresh shares "
        "use ROUND(...,0) so issued share counts are whole numbers before FD ownership."
    )
    asm["B53"].alignment = WRAP
    asm.row_dimensions[53].height = 36

    asm["B28"].alignment = WRAP
    asm["B29"].alignment = WRAP
    asm["B47"].alignment = WRAP
    asm.row_dimensions[28].height = 45
    asm.row_dimensions[29].height = 60
    asm.row_dimensions[47].height = 48
    autosize(asm, max_width=55)
    asm.column_dimensions["B"].width = 88
    asm.column_dimensions["A"].width = 58

    # --- Cohort Build ---
    cohort = wb.create_sheet("Cohort Build")
    headers = [
        "cohort_vintage",
        "calendar_quarter",
        "starting_arr",
        "gross_retention_pct",
        "expansion_arr",
        "churn_arr",
        "ending_arr",
        "include_flag",
        "exclusion_reason",
        "source_notes",
    ]
    cohort.append(headers)
    style_header_row(cohort)
    start_row = 2
    ending_arr_cache: list[float] = []
    for i, row in enumerate(inventory, start=start_row):
        cohort.cell(i, 1, row["vintage"])
        cohort.cell(i, 2, row["quarter"])
        cohort.cell(i, 3, money(float(row["starting_arr"])))
        cohort.cell(i, 4, round(float(row["gross_retention_pct"]), 1))
        cohort.cell(i, 5, money(float(row["expansion_arr"])))
        cohort.cell(i, 6, money(float(row["churn_arr"])))
        # Gross retention is pre-churn per Definitions — churn subtracted once here.
        cohort.cell(i, 7, f"=C{i}*D{i}/100+E{i}-F{i}")
        style_value_cell(cohort.cell(i, 7), kind="formula")
        for col in (3, 4, 5, 6):
            style_value_cell(cohort.cell(i, col), kind="input")
        cohort.cell(i, 8, int(row["include"]))
        style_value_cell(cohort.cell(i, 8), kind="input")
        cohort.cell(i, 9, row["exclusion_reason"])
        cohort.cell(i, 10, row["source_notes"] or "cohort_summary.xlsx Cohort Detail")
        ending_arr_cache.append(money(float(row["ending_arr"])))
        apply_number_format(cohort.cell(i, 3), '"$"#,##0.00')
        apply_number_format(cohort.cell(i, 4), "0.0")
        apply_number_format(cohort.cell(i, 5), '"$"#,##0.00')
        apply_number_format(cohort.cell(i, 6), '"$"#,##0.00')
        apply_number_format(cohort.cell(i, 7), '"$"#,##0.00')
        cohort.cell(i, 9).alignment = WRAP
        cohort.cell(i, 10).alignment = WRAP

    inv_end = start_row + len(inventory) - 1  # row 10 with 9 inventory rows

    # Row control: raw vs excluded vs retained
    ctrl = inv_end + 2
    cohort.cell(ctrl, 1, "Inventory control")
    cohort.cell(ctrl, 1).font = HEADER_FONT
    cohort.cell(ctrl + 1, 1, "raw_source_rows_in_inventory")
    cohort.cell(ctrl + 1, 2, f"=COUNTA(A{start_row}:A{inv_end})")
    cohort.cell(ctrl + 2, 1, "excluded_duplicate_rows")
    cohort.cell(ctrl + 2, 2, f'=COUNTIF(H{start_row}:H{inv_end},0)')
    cohort.cell(ctrl + 3, 1, "retained_rows_for_normalized_ARR")
    cohort.cell(ctrl + 3, 2, f"=SUM(H{start_row}:H{inv_end})")
    cohort.cell(ctrl + 4, 1, "retention_formula")
    cohort.cell(
        ctrl + 4,
        2,
        "ending_arr = starting×gross_retention%/100 + expansion − churn "
        "(gross_retention is before expansion/churn; churn counted once)",
    )
    cohort.cell(ctrl + 4, 2).alignment = WRAP

    # Quarterly totals derived from retained ending_arr via SUMIFS (not hard-coded)
    q_header = ctrl + 6
    cohort.cell(q_header, 1, "calendar_quarter")
    cohort.cell(q_header, 2, "rollup_arr_from_retained_rows")
    cohort.cell(q_header, 3, "source")
    style_header_row(cohort, q_header)
    rollup_start = q_header + 1
    quarter_labels = ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"]
    for idx_q, q in enumerate(quarter_labels):
        r = rollup_start + idx_q
        cohort.cell(r, 1, q)
        cohort.cell(
            r,
            2,
            f'=SUMIFS(G${start_row}:G${inv_end},B${start_row}:B${inv_end},A{r},'
            f'H${start_row}:H${inv_end},1)',
        )
        cohort.cell(
            r,
            3,
            "SUMIFS of retained Cohort Detail ending_arr (reconciles to Quarterly Rollup)",
        )
        apply_number_format(cohort.cell(r, 2), '"$"#,##0.00')
    ttm_row = rollup_start + 4
    norm_row = rollup_start + 5
    cohort.cell(ttm_row, 1, "TTM rollup sum (2024 quarters)")
    cohort.cell(ttm_row, 2, f"=SUM(B{rollup_start}:B{rollup_start + 3})")
    cohort.cell(norm_row, 1, "Normalized model ARR (ex pending renewal)")
    cohort.cell(norm_row, 2, "=B{0}-Assumptions!B7".format(ttm_row))
    apply_number_format(cohort.cell(ttm_row, 2), '"$"#,##0.00')
    apply_number_format(cohort.cell(norm_row, 2), '"$"#,##0.00')

    # Point Assumptions B6/B8 at the live TTM / normalized cells (row numbers vary).
    # Rebuild formula links now that layout is known.
    asm["B6"] = f"='Cohort Build'!B{ttm_row}"
    asm["B8"] = f"='Cohort Build'!B{norm_row}"

    autosize(cohort, max_width=42)
    cohort.column_dimensions["I"].width = 56
    cohort.column_dimensions["J"].width = 64
    cohort.row_dimensions[ctrl + 4].height = 36

    # Store layout anchors for formula cache
    cohort_layout = {
        "start_row": start_row,
        "inv_end": inv_end,
        "ctrl": ctrl,
        "rollup_start": rollup_start,
        "ttm_row": ttm_row,
        "norm_row": norm_row,
        "ending_arr_cache": ending_arr_cache,
        "inventory": inventory,
    }

    # --- Revenue Forecast ---
    forecast_ws = wb.create_sheet("Revenue Forecast")
    forecast_ws.append(
        [
            "Year",
            "Growth rate (total ARR path)",
            "ARR",
            "FCF margin",
            "Free cash flow",
            "Driver notes",
        ]
    )
    style_header_row(forecast_ws)
    forecast_ws["A2"] = "Base (normalized TTM)"
    forecast_ws["B2"] = 0
    forecast_ws["C2"] = "=Assumptions!B8"
    forecast_ws["D2"] = "=Assumptions!B30"
    forecast_ws["E2"] = "=C2*D2"
    forecast_ws["F2"] = "From Cohort Build normalized TTM (formula-linked)"
    # Y1 uses retention stress scalar × (1 + total growth). Base scalar = 1.00 so
    # Footnote 3 total growth is not multiplied by absolute trailing NRR.
    forecast_ws["A3"] = "Y1"
    forecast_ws["B3"] = "=Assumptions!B39"
    forecast_ws["C3"] = "=C2*Assumptions!B46*(1+B3)"
    forecast_ws["D3"] = "=Assumptions!B30"
    forecast_ws["E3"] = "=C3*D3"
    forecast_ws["F3"] = (
        "Normalized TTM × retention stress scalar (Assumptions!B46, base 1.00) "
        "× (1 + Y1 total ARR growth). Absolute NRR is not re-applied."
    )
    for i, g in enumerate(FORECAST_GROWTH[1:], start=4):
        forecast_ws[f"A{i}"] = f"Y{i - 2}"
        forecast_ws[f"B{i}"] = g
        forecast_ws[f"C{i}"] = f"=C{i-1}*(1+B{i})"
        forecast_ws[f"D{i}"] = "=Assumptions!B30"
        forecast_ws[f"E{i}"] = f"=C{i}*D{i}"
        forecast_ws[f"F{i}"] = "Footnote 3 forward path on prior-year ARR"
    for r in range(2, 8):
        apply_number_format(forecast_ws[f"B{r}"], "0%")
        apply_number_format(forecast_ws[f"C{r}"], '"$"#,##0.00')
        apply_number_format(forecast_ws[f"D{r}"], "0%")
        apply_number_format(forecast_ws[f"E{r}"], '"$"#,##0.00')
        style_value_cell(forecast_ws[f"B{r}"])
        style_value_cell(forecast_ws[f"C{r}"])
        style_value_cell(forecast_ws[f"D{r}"])
        style_value_cell(forecast_ws[f"E{r}"])
        forecast_ws[f"F{r}"].alignment = WRAP
    forecast_ws.column_dimensions["F"].width = 72
    autosize(forecast_ws)

    # --- DCF Build ---
    dcf = wb.create_sheet("DCF Build")
    dcf.append(["year", "arr", "fcf", "df_14pct", "pv_14pct", "df_16pct", "pv_16pct"])
    style_header_row(dcf)
    dcf["I1"] = "WACC high-EV case"
    dcf["J1"] = "=Assumptions!B36"
    dcf["I2"] = "WACC low-EV case"
    dcf["J2"] = "=Assumptions!B37"
    dcf["I3"] = "FCF margin"
    dcf["J3"] = "=Assumptions!B30"
    dcf["I4"] = "Terminal growth"
    dcf["J4"] = "=Assumptions!B38"
    for year in range(1, 6):
        r = year + 1
        dcf[f"A{r}"] = year
        dcf[f"B{r}"] = f"='Revenue Forecast'!C{year + 2}"
        dcf[f"C{r}"] = f"=B{r}*$J$3"
        dcf[f"D{r}"] = f"=1/(1+$J$1)^A{r}"
        dcf[f"E{r}"] = f"=C{r}*D{r}"
        dcf[f"F{r}"] = f"=1/(1+$J$2)^A{r}"
        dcf[f"G{r}"] = f"=C{r}*F{r}"
        apply_number_format(dcf[f"B{r}"], '"$"#,##0.00')
        apply_number_format(dcf[f"C{r}"], '"$"#,##0.00')
        apply_number_format(dcf[f"D{r}"], "0.0000")
        apply_number_format(dcf[f"E{r}"], '"$"#,##0.00')
        apply_number_format(dcf[f"F{r}"], "0.0000")
        apply_number_format(dcf[f"G{r}"], '"$"#,##0.00')
    for addr in ("J1", "J2", "J3", "J4"):
        apply_number_format(dcf[addr], "0.00%")
    autosize(dcf)

    # --- Cap Table Pro Forma (individual holders from cap_table.csv) ---
    cap_ws = wb.create_sheet("Cap Table Pro Forma")
    style_section_label(cap_ws["A1"], "Post-round fully diluted ownership by individual holder")
    cap_ws.merge_cells("A1:G1")
    cap_ws["A2"] = (
        "Each legal holder from cap_table.csv is listed separately. Option Pool is a pool "
        "category (existing stock-plan Options rows + 15% refresh). Forsyth Equity combines "
        "Series A Preferred and Series B pro-rata primary. Share issuances use whole-share "
        "ROUND formulas from Assumptions."
    )
    cap_ws["A2"].alignment = WRAP
    cap_ws.merge_cells("A2:G2")
    cap_ws.row_dimensions[2].height = 48

    headers = [
        "Holder",
        "Security / Position",
        "Pre-Round Shares",
        "New Shares",
        "Post-Round Shares",
        "Post-Round FD Ownership",
        "Source / Notes",
    ]
    for col, h in enumerate(headers, start=1):
        cell = cap_ws.cell(3, col, h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.border = THIN
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    # Pre-round individuals (rows 4..)
    first_data = 4
    r = first_data
    for holder, security, shares, note in INDIVIDUAL_PRE_ROUND:
        cap_ws.cell(r, 1, holder)
        cap_ws.cell(r, 2, security)
        cap_ws.cell(r, 3, shares)
        cap_ws.cell(r, 4, 0)
        cap_ws.cell(r, 5, f"=C{r}+D{r}")
        # ownership denominator filled after last_data known — placeholder, rewritten below
        cap_ws.cell(r, 7, note)
        r += 1

    # Option Pool — existing allocated Options rows as pool category
    pool_existing_row = r
    cap_ws.cell(r, 1, "Option Pool")
    cap_ws.cell(r, 2, "Existing allocated Options (stock plan)")
    cap_ws.cell(r, 3, "=Assumptions!B23")
    cap_ws.cell(r, 4, 0)
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(
        r,
        7,
        "cap_table.csv Options rows (excludes available/empty pool stub; "
        "excludes Dr. Elena Ruiz advisor warrant from pool inventory)",
    )
    r += 1

    # Forsyth Equity — Series A + Series B pro-rata as one holder
    forsyth_row = r
    cap_ws.cell(r, 1, SERIES_A_INVESTOR)
    cap_ws.cell(r, 2, "Series A Preferred + Series B Pro-Rata")
    cap_ws.cell(r, 3, "=Assumptions!B15")
    cap_ws.cell(r, 4, "=Assumptions!B21")
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(
        r,
        7,
        "cap_table.csv Series A Preferred at $1.82; investor_brief.txt full pro-rata of $28M primary",
    )
    r += 1

    # SAFE holders
    vesper_row = r
    cap_ws.cell(r, 1, SAFE_BIRCHWOOD)
    cap_ws.cell(r, 2, "SAFE conversion (base case; MFN outstanding)")
    cap_ws.cell(r, 3, 0)
    cap_ws.cell(r, 4, "=Assumptions!B19")
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(
        r,
        7,
        "Whole-share ROUND of invested / applicable conversion price; MFN unresolved per sources",
    )
    r += 1

    quorum_row = r
    cap_ws.cell(r, 1, SAFE_STONEGATE)
    cap_ws.cell(r, 2, "SAFE conversion")
    cap_ws.cell(r, 3, 0)
    cap_ws.cell(r, 4, "=Assumptions!B20")
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(r, 7, "cap_table.csv — $55M cap, no discount; whole-share ROUND")
    r += 1

    # Lead primary
    lead_row = r
    cap_ws.cell(r, 1, LEAD_INVESTOR)
    cap_ws.cell(r, 2, "Series B Primary (lead)")
    cap_ws.cell(r, 3, 0)
    cap_ws.cell(r, 4, "=Assumptions!B22")
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(r, 7, "Remainder of $28M primary after Forsyth pro-rata")
    r += 1

    # Option pool refresh as new shares on pool category (separate line for clarity)
    pool_refresh_row = r
    cap_ws.cell(r, 1, "Option Pool")
    cap_ws.cell(r, 2, "15% post-money refresh (board case)")
    cap_ws.cell(r, 3, 0)
    cap_ws.cell(r, 4, "=Assumptions!B24")
    cap_ws.cell(r, 5, f"=C{r}+D{r}")
    cap_ws.cell(r, 7, "investor_brief.txt 15% target; ROUND whole shares; 12% alternate on Option pool cases")
    last_data = r
    r += 2

    total_row = r
    cap_ws.cell(total_row, 1, "Post-money FD total")
    cap_ws.cell(total_row, 1).font = HEADER_FONT
    cap_ws.cell(total_row, 5, f"=SUM(E{first_data}:E{last_data})")
    cap_ws.cell(total_row, 6, f"=SUM(F{first_data}:F{last_data})")
    cap_ws.cell(total_row, 7, "Must reconcile to Assumptions!B40 / Option pool cases E3")
    for col in range(1, 8):
        cap_ws.cell(total_row, col).fill = TOTAL_FILL
        cap_ws.cell(total_row, col).border = THIN

    # Ownership formulas + formatting for data rows
    for rr in range(first_data, last_data + 1):
        cap_ws.cell(rr, 6, f"=E{rr}/$E${total_row}")
        for col in (3, 4, 5):
            apply_number_format(cap_ws.cell(rr, col), "#,##0")
            style_value_cell(cap_ws.cell(rr, col))
        apply_number_format(cap_ws.cell(rr, 6), "0.0000%")
        style_value_cell(cap_ws.cell(rr, 6), kind="formula")
        cap_ws.cell(rr, 7).alignment = WRAP
        for col in range(1, 8):
            cap_ws.cell(rr, col).border = THIN
        cap_ws.row_dimensions[rr].height = 28

    apply_number_format(cap_ws.cell(total_row, 5), "#,##0")
    apply_number_format(cap_ws.cell(total_row, 6), "0.00%")
    style_value_cell(cap_ws.cell(total_row, 5), kind="formula")
    style_value_cell(cap_ws.cell(total_row, 6), kind="formula")

    # Forsyth callout — reviewer asked for 8,125,000 / ~33.5905% clearly
    callout = total_row + 2
    style_section_label(cap_ws.cell(callout, 1), f"{SERIES_A_INVESTOR} — post-round total (callout)")
    cap_ws.merge_cells(start_row=callout, start_column=1, end_row=callout, end_column=3)
    cap_ws.cell(callout + 1, 1, "Forsyth Equity post-round shares")
    cap_ws.cell(callout + 1, 2, f"=E{forsyth_row}")
    cap_ws.cell(callout + 1, 3, "Series A + Series B pro-rata (formula-linked)")
    cap_ws.cell(callout + 2, 1, "Forsyth Equity post-round FD ownership")
    cap_ws.cell(callout + 2, 2, f"=F{forsyth_row}")
    cap_ws.cell(callout + 2, 3, "Post-round shares ÷ FD total")
    apply_number_format(cap_ws.cell(callout + 1, 2), "#,##0")
    apply_number_format(cap_ws.cell(callout + 2, 2), "0.0000%")
    style_value_cell(cap_ws.cell(callout + 1, 2), kind="formula")
    style_value_cell(cap_ws.cell(callout + 2, 2), kind="formula")

    autosize(cap_ws, max_width=40)
    cap_ws.column_dimensions["A"].width = 28
    cap_ws.column_dimensions["B"].width = 42
    cap_ws.column_dimensions["G"].width = 72

    cap_layout = {
        "first_data": first_data,
        "last_data": last_data,
        "total_row": total_row,
        "forsyth_row": forsyth_row,
        "vesper_row": vesper_row,
        "quorum_row": quorum_row,
        "lead_row": lead_row,
        "pool_existing_row": pool_existing_row,
        "pool_refresh_row": pool_refresh_row,
        "callout": callout,
    }

    # --- Valuation Summary ---
    val = wb.create_sheet("Valuation Summary")
    style_section_label(val["A1"], "Valuation summary — Helix Biotech Series B")
    val.merge_cells("A1:C1")
    val["A2"] = "Method / metric"
    val["B2"] = "Value"
    val["C2"] = "Basis"
    style_header_row(val, 2)

    style_section_label(val["A3"], "Revenue basis")
    val.merge_cells("A3:C3")
    val["A4"] = "Normalized TTM ARR"
    val["B4"] = "=Assumptions!B8"
    val["C4"] = "Cohort build after pending-renewal exclusion"
    val["A5"] = "NTM / Y1 ARR (forecast)"
    val["B5"] = "=Assumptions!B9"
    val["C5"] = "Revenue Forecast Y1 (Footnote 3 growth path)"

    style_section_label(val["A7"], "Revenue-multiple valuation")
    val.merge_cells("A7:C7")
    val["A8"] = "Revenue multiple low (5.5x on Y1 NTM ARR)"
    val["B8"] = "=Assumptions!B9*Assumptions!B31"
    val["C8"] = "investor_brief.txt comps / Footnote 3"
    val["A9"] = "Revenue multiple high (7.0x on Y1 NTM ARR)"
    val["B9"] = "=Assumptions!B9*Assumptions!B32"
    val["C9"] = "investor_brief.txt comps / Footnote 3"
    val["A10"] = "Midpoint revenue-multiple valuation"
    val["B10"] = "=(B8+B9)/2"
    val["C10"] = "Average of 5.5x–7.0x NTM"
    val["A11"] = "Downside EV (5.0x normalized TTM ARR)"
    val["B11"] = "=Assumptions!B8*Assumptions!B33"
    val["C11"] = "investor_brief.txt downside"
    val["A12"] = "Peer-median NTM case (6.1x) — sensitivity base"
    val["B12"] = "='Revenue Forecast'!C3*Assumptions!B34"
    val["C12"] = "Ties to Sensitivity center cell ($297,534,618.15 base)"

    style_section_label(val["A14"], "DCF valuation")
    val.merge_cells("A14:C14")
    val["A15"] = "DCF implied EV high (14% WACC)"
    val["B15"] = (
        "='DCF Build'!E2+'DCF Build'!E3+'DCF Build'!E4+'DCF Build'!E5+'DCF Build'!E6"
        "+('DCF Build'!C6*(1+Assumptions!B38)/(Assumptions!B36-Assumptions!B38)"
        "/((1+Assumptions!B36)^5))"
    )
    val["C15"] = "Five-year FCF + terminal"
    val["A16"] = "DCF implied EV low (16% WACC)"
    val["B16"] = (
        "='DCF Build'!G2+'DCF Build'!G3+'DCF Build'!G4+'DCF Build'!G5+'DCF Build'!G6"
        "+('DCF Build'!C6*(1+Assumptions!B38)/(Assumptions!B37-Assumptions!B38)"
        "/((1+Assumptions!B37)^5))"
    )
    val["C16"] = "Five-year FCF + terminal"
    val["A17"] = "Midpoint DCF-implied valuation"
    val["B17"] = "=(B15+B16)/2"
    val["C17"] = "Average of 14%–16% WACC"

    style_section_label(val["A19"], "Selected / term-sheet cross-check")
    val.merge_cells("A19:C19")
    val["A20"] = "Term sheet pre-money"
    val["B20"] = "=Assumptions!B3"
    val["C20"] = "investor_brief.txt — transaction terms"
    val["A21"] = "Implied post-money before pool"
    val["B21"] = "=Assumptions!B5"
    val["C21"] = "investor_brief.txt"
    val["A22"] = "Multiple vs DCF midpoint variance"
    val["B22"] = "=B10-B17"
    val["C22"] = "Reconciliation of midpoint methods"

    for r in (4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 20, 21, 22):
        apply_number_format(val[f"B{r}"], '"$"#,##0.00')
        style_value_cell(val[f"B{r}"])
        val[f"C{r}"].alignment = WRAP
    autosize(val, max_width=55)
    val.column_dimensions["A"].width = 52
    val.column_dimensions["C"].width = 48

    # Keep peer-base cell address for Sensitivity cross-check (was B5; now B12)
    val_peer_cell = "B12"
    val_mult_low = "B8"
    val_mult_high = "B9"
    val_downside = "B11"
    val_dcf_high = "B15"
    val_dcf_low = "B16"
    val_mult_mid = "B10"
    val_dcf_mid = "B17"
    val_variance = "B22"

    # --- Sensitivity: drivers feed the same Y1 formula as Revenue Forecast ---
    sens = wb.create_sheet("Sensitivity")
    sens["A1"] = "Sensitivity — retention stress × Y1 total ARR growth → forecast ARR → peer EV"
    sens["A1"].font = HEADER_FONT
    sens["A2"] = (
        "Footnote 3 Y1 growth is TOTAL ARR growth. Retention stress is a multiplicative "
        "stress vs the base path (scalar = NRR_case / 1.08; base scalar = 1.00). Absolute "
        "trailing NRR is NOT multiplied on top of total growth. Each case uses the same "
        "Y1 identity as Revenue Forecast: Normalized TTM × retention_stress × (1+growth). "
        "Center case ties to live Revenue Forecast!C3 and Valuation Summary peer-median EV."
    )
    sens["A2"].alignment = WRAP
    sens.row_dimensions[2].height = 72

    # Live driver bridge (connected to forecast)
    sens["A3"] = "Live forecast drivers (linked)"
    sens["A3"].font = HEADER_FONT
    sens["A4"] = "normalized_ttm_arr"
    sens["B4"] = "=Assumptions!B8"
    sens["C4"] = "retention_stress_scalar_base"
    sens["D4"] = "=Assumptions!B46"
    sens["E4"] = "y1_total_arr_growth"
    sens["F4"] = "=Assumptions!B39"
    sens["A5"] = "trailing_nrr_diagnostic"
    sens["B5"] = "=Assumptions!B35"
    sens["C5"] = "peer_median_multiple"
    sens["D5"] = "=Assumptions!B34"
    sens["E5"] = "live_y1_arr_(Revenue Forecast)"
    sens["F5"] = "='Revenue Forecast'!C3"
    sens["A6"] = "live_peer_median_EV"
    sens["B6"] = "=F5*D5"
    sens["C6"] = "valuation_summary_peer_check"
    sens["D6"] = f"='Valuation Summary'!{val_peer_cell}"
    apply_number_format(sens["B4"], '"$"#,##0.00')
    apply_number_format(sens["D4"], "0.00")
    apply_number_format(sens["F4"], "0%")
    apply_number_format(sens["B5"], "0.00")
    apply_number_format(sens["D5"], '0.0"x"')
    apply_number_format(sens["F5"], '"$"#,##0.00')
    apply_number_format(sens["B6"], '"$"#,##0.00')
    apply_number_format(sens["D6"], '"$"#,##0.00')

    # Y1 ARR matrix
    sens["A8"] = "Y1 ARR cases (feeds valuation)"
    sens["A8"].font = HEADER_FONT
    sens["A9"] = "NRR case \\ Growth →"
    sens["A9"].font = HEADER_FONT
    sens["B8"] = "retention_stress = NRR_case / trailing_nrr_diagnostic"
    for col_idx, g in enumerate(SENS_GROWTHS, start=2):
        cell = sens.cell(9, col_idx, g)
        cell.font = HEADER_FONT
        cell.number_format = "0%"
        if abs(g - FORECAST_GROWTH[0]) < 1e-9:
            sens.cell(8, col_idx, "base growth")
            sens.cell(8, col_idx).font = Font(italic=True)

    sens_values: dict[str, float] = {
        "B4": model_arr,
        "D4": 1.0,
        "F4": FORECAST_GROWTH[0],
        "B5": BASE_NRR,
        "D5": PEER_MEDIAN_MULTIPLE,
        "F5": ntm_arr,
        "B6": peer_base,
        "D6": peer_base,
    }
    y1_base_coord = None
    for row_offset, nrr in enumerate(SENS_NRRS):
        r = 10 + row_offset
        sens.cell(r, 1, nrr).number_format = "0.00"
        stress = nrr / BASE_NRR
        sens.cell(r, 5, round(stress, 6)).number_format = "0.0000"
        if abs(nrr - BASE_NRR) < 1e-9:
            sens.cell(r, 6, "base row (stress=1.00)")
            sens.cell(r, 6).font = Font(italic=True)
        for col_offset, g in enumerate(SENS_GROWTHS):
            c = 2 + col_offset
            # Same identity as Revenue Forecast Y1: TTM × (NRR/base_NRR) × (1+g)
            formula = f"=$B$4*(A{r}/$B$5)*(1+{get_column_letter(c)}$9)"
            sens.cell(r, c, formula)
            apply_number_format(sens.cell(r, c), '"$"#,##0.00')
            y1_case = money(model_arr * (nrr / BASE_NRR) * (1 + g))
            sens_values[f"{get_column_letter(c)}{r}"] = y1_case
            if abs(nrr - BASE_NRR) < 1e-9 and abs(g - FORECAST_GROWTH[0]) < 1e-9:
                sens.cell(r, c).font = Font(bold=True)
                y1_base_coord = f"{get_column_letter(c)}{r}"

    sens["E9"] = "stress"
    sens["E9"].font = HEADER_FONT

    # EV matrix = Y1 ARR × peer multiple (connected through forecast math)
    sens["A14"] = "Peer-median EV cases (= Y1 ARR × peer multiple)"
    sens["A14"].font = HEADER_FONT
    sens["A15"] = "NRR case \\ Growth →"
    sens["A15"].font = HEADER_FONT
    for col_idx, g in enumerate(SENS_GROWTHS, start=2):
        cell = sens.cell(15, col_idx, g)
        cell.font = HEADER_FONT
        cell.number_format = "0%"

    for row_offset, nrr in enumerate(SENS_NRRS):
        r = 16 + row_offset
        y1_r = 10 + row_offset
        sens.cell(r, 1, nrr).number_format = "0.00"
        for col_offset, g in enumerate(SENS_GROWTHS):
            c = 2 + col_offset
            y1_ref = f"{get_column_letter(c)}{y1_r}"
            sens.cell(r, c, f"={y1_ref}*$D$5")
            apply_number_format(sens.cell(r, c), '"$"#,##0.00')
            sens_values[f"{get_column_letter(c)}{r}"] = money(
                model_arr * (nrr / BASE_NRR) * (1 + g) * PEER_MEDIAN_MULTIPLE
            )
            if abs(nrr - BASE_NRR) < 1e-9 and abs(g - FORECAST_GROWTH[0]) < 1e-9:
                sens.cell(r, c).font = Font(bold=True)
                # Force center EV cache through rounded Y1 path to preserve $297,534,618.15
                sens_values[f"{get_column_letter(c)}{r}"] = peer_base

    sens["A20"] = "Base-case tie-out"
    sens["A20"].font = HEADER_FONT
    sens["A21"] = "Base Y1 ARR (matrix)"
    sens["B21"] = f"={y1_base_coord}"
    sens["C21"] = "Live Revenue Forecast Y1"
    sens["D21"] = "=F5"
    sens["A22"] = "Base peer EV (matrix)"
    sens["B22"] = "=C17"  # center EV at NRR 1.08 / growth 28%
    sens["C22"] = "Live peer EV / Valuation Summary"
    sens["D22"] = "=B6"
    apply_number_format(sens["B21"], '"$"#,##0.00')
    apply_number_format(sens["D21"], '"$"#,##0.00')
    apply_number_format(sens["B22"], '"$"#,##0.00')
    apply_number_format(sens["D22"], '"$"#,##0.00')
    sens_values["B21"] = ntm_arr
    sens_values["D21"] = ntm_arr
    sens_values["B22"] = peer_base
    sens_values["D22"] = peer_base

    sens["A24"] = "Methodology note"
    sens["B24"] = (
        "Growth and retention are separate drivers. Base forecast uses retention_stress=1.00 "
        "and Footnote 3 total ARR growth (28%). Sensitivity NRR rows convert to stress via "
        "NRR/1.08 so the center does not re-apply absolute 108% NRR on top of total growth. "
        f"Center peer EV equals normalized TTM × 1.28 × 6.1x = ${peer_base:,.2f}."
    )
    sens["B24"].alignment = WRAP
    sens.row_dimensions[24].height = 56
    autosize(sens, max_width=28)
    sens.column_dimensions["A"].width = 36
    sens.column_dimensions["C"].width = 32
    sens.column_dimensions["E"].width = 28
    sens.column_dimensions["F"].width = 22

    # --- Option pool cases (before Notes) ---
    pool = wb.create_sheet("Option pool cases")
    pool.append(
        [
            "scenario",
            "target_post_money_pool_pct",
            "existing_pool_shares",
            "refresh_shares",
            "fd_post",
            "combined_pool_pct",
            "treatment",
        ]
    )
    style_header_row(pool)
    pool["A2"] = "Counsel side letter (12%)"
    pool["B2"] = "=Assumptions!B27"
    pool["C2"] = "=Assumptions!B23"
    pool["D2"] = "=ROUND(MAX((B2*Assumptions!B13-C2)/(1-B2),0),0)"
    pool["E2"] = "=Assumptions!B13+D2"
    pool["F2"] = "=(C2+D2)/E2"
    pool["G2"] = "12% side letter from cap_table.csv; alternate only; whole-share ROUND"
    pool["A3"] = "Term sheet (15%)"
    pool["B3"] = "=Assumptions!B26"
    pool["C3"] = "=Assumptions!B23"
    pool["D3"] = "=ROUND(MAX((B3*Assumptions!B13-C3)/(1-B3),0),0)"
    pool["E3"] = "=Assumptions!B13+D3"
    pool["F3"] = "=(C3+D3)/E3"
    pool["G3"] = "Board-approved; used on Cap Table Pro Forma; whole-share ROUND"
    for r in (2, 3):
        apply_number_format(pool[f"B{r}"], "0%")
        apply_number_format(pool[f"C{r}"], "#,##0")
        apply_number_format(pool[f"D{r}"], "#,##0")
        apply_number_format(pool[f"E{r}"], "#,##0")
        apply_number_format(pool[f"F{r}"], "0.0%")
        style_value_cell(pool[f"B{r}"])
        style_value_cell(pool[f"C{r}"])
        style_value_cell(pool[f"D{r}"])
        style_value_cell(pool[f"E{r}"])
        style_value_cell(pool[f"F{r}"])
        pool[f"G{r}"].alignment = WRAP
    autosize(pool, max_width=40)
    pool.column_dimensions["G"].width = 48

    # Rounded share totals used by Notes narrative and cached formula values.
    # compute_cap_table already applies whole-share ROUND at each issuance step.
    pool_refresh_r = cap["pool_refresh"]
    pool_refresh_12_r = cap["pool_refresh_12"]
    fd_mid_r = cap["fd_mid"]
    fd_post_r = cap["fd_post"]
    fd_post_12_r = cap["fd_post_12"]

    # --- Notes ---
    notes = wb.create_sheet("Notes")
    notes["A1"] = "Source conflicts, methodology, and outstanding diligence"
    notes["A1"].font = HEADER_FONT
    notes["A2"] = "section / topic"
    notes["B2"] = "detail"
    notes["A2"].font = HEADER_FONT
    notes["B2"].font = HEADER_FONT
    note_rows = [
        (
            "CONFIRMED — Series A Preferred holder",
            f"cap_table.csv lists {SERIES_A_INVESTOR} as the Series A Preferred holder: "
            f"{SERIES_A_SHARES:,} shares at ${SERIES_A_PRICE:.2f}/share (2022-04 close). "
            f"No other holder is shown for that security.",
        ),
        (
            "CONFIRMED — Forsyth Equity pro-rata",
            f"investor_brief.txt allocates ${cap['lockwood_prorata_invest']:,.2f} of the "
            f"${PRIMARY:,} primary to Forsyth Equity ({SERIES_A_SHARES / FD_PRE:.4%} of FD pre), "
            f"matching the Series B Pro-Rata stub on cap_table.csv. That full pro-rata slice is "
            f"used on the Cap Table Pro Forma.",
        ),
        (
            "CONFIRMED — ARR bridge from retained cohort rows",
            f"Cohort Build inventories all eight unique 2024 calendar-quarter Cohort Detail "
            f"records from cohort_summary.xlsx, visibly excludes the duplicate FY2023-Q2 "
            f"expansion line, and derives quarterly totals with SUMIFS on retained ending_arr. "
            f"Those totals reconcile to Quarterly Rollup TTM ${ROLLUP_TTM_2024:,.2f}. Footnote 1 "
            f"excludes the {PENDING_CUSTOMER} pending renewal (${PENDING_RENEWAL_ARR:,}), "
            f"producing normalized model ARR of ${model_arr:,.2f} that feeds Revenue Forecast.",
        ),
        (
            "CONFIRMED — Headline run-rate not binding",
            f"investor_brief.txt also quotes a ${BRIEF_RUN_RATE:,} headline run-rate that "
            f"includes the pending {PENDING_CUSTOMER} renewal. That headline is disclosed for "
            f"context only and is not the binding valuation basis.",
        ),
        (
            "CONFIRMED — Ending-ARR / retention definition",
            "Per cohort_summary.xlsx Definitions, gross_retention_pct is starting ARR retained "
            "before expansion and churn. Cohort Build ending_arr = starting_arr × "
            "gross_retention_pct/100 + expansion_arr − churn_arr. Churn is applied once via the "
            "−churn_arr term; gross_retention_pct is not a net-of-churn rate, so retention and "
            "churn are not double-counted.",
        ),
        (
            "CONFIRMED — Duplicate FY2023-Q2 expansion",
            "The duplicate FY2023-Q2 expansion line remains in the Cohort Build inventory with "
            "include_flag=0 and an explicit exclusion reason. It is excluded from SUMIFS "
            "quarterly totals and normalized ARR (excluded once).",
        ),
        (
            "CONFIRMED — Fiscal vs calendar quarters",
            "Per cohort_summary.xlsx fiscal-to-calendar mapping and investor_brief.txt Footnote 2, "
            "Cohort Build preserves calendar_quarter from the source map (e.g. FY2023-Q4 → 2024-Q1; "
            "FY2024-Q1 → 2024-Q3).",
        ),
        (
            "MODELING ASSUMPTION — Forward growth path",
            "Revenue Forecast Y1 uses Footnote 3 total ARR growth (28%) with retention stress "
            "scalar = 1.00 on Assumptions. Absolute trailing cohort NRR (~1.08) is a diagnostic "
            "only and is not stacked onto total growth in the base case. Sensitivity converts "
            "NRR cases to stress = NRR/1.08 so growth and retention remain separate drivers; "
            f"center peer-median EV = ${peer_base:,.2f}.",
        ),
        (
            "MODELING ASSUMPTION — Vesper base-case conversion price",
            f"{SAFE_BIRCHWOOD} SAFE is modeled at the lower valuation-cap price "
            f"(≈${SAFE1_CAP / FD_PRE:.4f}/share) versus the ≈20%-discounted Series B price "
            f"because that is the contractual lower-of mechanics. This is a modeling assumption "
            f"for the pro forma while MFN diligence remains open — not a finding that MFN was "
            f"cleared or that no better terms exist.",
        ),
        (
            "UNRESOLVED DILIGENCE — Vesper Growth MFN",
            f"The MFN remains outstanding/unresolved per cap_table.csv (status field: "
            f"'MFN clause outstanding') and investor_brief.txt (open diligence: document MFN "
            f"treatment relative to Series B price). No source clears the MFN, confirms review "
            f"completion, discloses a better MFN term, or waives the clause. Conversion shares "
            f"remain conditional until MFN diligence closes. No alternate MFN price is modeled "
            f"because the inputs do not quantify one.",
        ),
        (
            "CONDITIONAL — Option pool 12% vs 15%",
            f"investor_brief.txt / term sheet: 15% post-money refresh used on Cap Table Pro Forma "
            f"({pool_refresh_r:,.0f} refresh; {fd_post_r:,.0f} FD post). cap_table.csv counsel "
            f"side-letter: 12% alternate on Option pool cases ({pool_refresh_12_r:,.0f} refresh). "
            f"Existing stock-plan pool base = {cap['existing_pool']:,.0f} (Options rows only; "
            f"Dr. Elena Ruiz advisor warrant excluded from pool inventory but retained in FD).",
        ),
        (
            "CONFIRMED — Quorum Ventures SAFE",
            f"cap_table.csv and investor_brief.txt both show Quorum Ventures SAFE terms: "
            f"${SAFE2_INVEST:,} invested, $55M cap, no discount. Modeled conversion = "
            f"{cap['s2']:,.0f} whole shares (ROUND).",
        ),
        (
            "CONFIRMED — Whole-share issuance",
            f"SAFE conversion, Series B primary, and option-pool refresh use ROUND(...,0) live "
            f"formulas. Vesper = {cap['s1']:,.0f}; Quorum = {cap['s2']:,.0f}; pool refresh 15% = "
            f"{pool_refresh_r:,.0f}; post-money FD = {fd_post_r:,.0f}. Cap Table Pro Forma lists "
            f"each cap_table.csv holder individually (no Founders & Employees rollup); "
            f"{SERIES_A_INVESTOR} post-round = {SERIES_A_SHARES + cap['lockwood_prorata_shares']:,.0f} "
            f"shares ({(SERIES_A_SHARES + cap['lockwood_prorata_shares']) / fd_post_r:.4%} FD).",
        ),
        (
            "CONFIRMED — Revenue multiples & DCF",
            f"Valuation Summary applies 5.5x–7.0x to Y1 NTM ARR (${ntm_arr:,.2f}), a 5.0x "
            f"downside on normalized TTM, and DCF cases at 14%–16% WACC with 3% terminal growth "
            f"and 22% FCF margin (investor_brief.txt Footnote 3). Sensitivity center equals the "
            f"6.1x peer-median NTM case (${peer_base:,.2f}) and ties to live Revenue Forecast Y1.",
        ),
        (
            "Board recommendation / open items",
            f"Proceed with the {LEAD_INVESTOR} term sheet at $112M pre-money, ${PRIMARY:,} "
            f"primary, and 15% post-money pool per investor_brief.txt. Ownership and conversion "
            f"figures that depend on {SAFE_BIRCHWOOD} remain conditional while the MFN diligence "
            f"item is open; close that item before treating conversion shares as final.",
        ),
    ]
    note_heights = {
        3: 48,
        4: 52,
        5: 72,
        6: 48,
        7: 64,
        8: 52,
        9: 48,
        10: 64,
        11: 64,
        12: 72,
        13: 64,
        14: 44,
        15: 56,
        16: 56,
        17: 56,
    }
    for i, (topic, detail) in enumerate(note_rows, start=3):
        notes.cell(i, 1, topic)
        notes.cell(i, 2, detail)
        notes.cell(i, 1).alignment = WRAP
        notes.cell(i, 2).alignment = WRAP
        notes.row_dimensions[i].height = note_heights.get(i, 52)
    notes.column_dimensions["A"].width = 42
    notes.column_dimensions["B"].width = 108

    # Freeze panes on analytical sheets
    for ws in wb.worksheets:
        if ws.title != "Notes":
            ws.freeze_panes = "A2"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    post_share_rows: list[tuple[int, float]] = []
    for idx, (_h, _sec, shares, _note) in enumerate(INDIVIDUAL_PRE_ROUND):
        post_share_rows.append((cap_layout["first_data"] + idx, float(shares)))
    post_share_rows.append((cap_layout["pool_existing_row"], float(cap["existing_pool"])))
    forsyth_post = float(SERIES_A_SHARES + cap["lockwood_prorata_shares"])
    post_share_rows.append((cap_layout["forsyth_row"], forsyth_post))
    post_share_rows.append((cap_layout["vesper_row"], float(cap["s1"])))
    post_share_rows.append((cap_layout["quorum_row"], float(cap["s2"])))
    post_share_rows.append((cap_layout["lead_row"], float(cap["summit_shares"])))
    post_share_rows.append((cap_layout["pool_refresh_row"], float(pool_refresh_r)))
    total_post = sum(s for _, s in post_share_rows)
    assert abs(total_post - fd_post_r) < 0.5, (total_post, fd_post_r)
    ownership_by_row = {row: shares / total_post for row, shares in post_share_rows}

    dcf_pv_rows: dict[str, float] = {}
    for year in range(1, 6):
        r = year + 1
        arr = forecast[year]
        fcf = arr * FCF_MARGIN
        df14 = 1 / ((1 + WACC_LOW) ** year)
        df16 = 1 / ((1 + WACC_HIGH) ** year)
        dcf_pv_rows[f"C{r}"] = money(fcf)
        dcf_pv_rows[f"D{r}"] = ratio(df14)
        dcf_pv_rows[f"E{r}"] = money(fcf * df14)
        dcf_pv_rows[f"F{r}"] = ratio(df16)
        dcf_pv_rows[f"G{r}"] = money(fcf * df16)

    cap_cache: dict[str, float] = {
        f"E{cap_layout['total_row']}": money(total_post),
        f"F{cap_layout['total_row']}": ratio(1.0),
        f"B{cap_layout['callout'] + 1}": money(forsyth_post),
        f"B{cap_layout['callout'] + 2}": ratio(forsyth_post / total_post),
    }
    for row, shares in post_share_rows:
        # Pre / new / post / ownership
        if row < cap_layout["pool_existing_row"]:
            # individuals: pre = shares, new = 0
            cap_cache[f"C{row}"] = money(shares)
            cap_cache[f"D{row}"] = 0.0
        elif row == cap_layout["pool_existing_row"]:
            cap_cache[f"C{row}"] = money(cap["existing_pool"])
            cap_cache[f"D{row}"] = 0.0
        elif row == cap_layout["forsyth_row"]:
            cap_cache[f"C{row}"] = money(SERIES_A_SHARES)
            cap_cache[f"D{row}"] = money(cap["lockwood_prorata_shares"])
        elif row == cap_layout["vesper_row"]:
            cap_cache[f"C{row}"] = 0.0
            cap_cache[f"D{row}"] = money(cap["s1"])
        elif row == cap_layout["quorum_row"]:
            cap_cache[f"C{row}"] = 0.0
            cap_cache[f"D{row}"] = money(cap["s2"])
        elif row == cap_layout["lead_row"]:
            cap_cache[f"C{row}"] = 0.0
            cap_cache[f"D{row}"] = money(cap["summit_shares"])
        elif row == cap_layout["pool_refresh_row"]:
            cap_cache[f"C{row}"] = 0.0
            cap_cache[f"D{row}"] = money(pool_refresh_r)
        cap_cache[f"E{row}"] = money(shares)
        cap_cache[f"F{row}"] = ratio(ownership_by_row[row])

    cache_xlsx_formula_values(
        OUT,
        {
            "Assumptions": {
                "B6": money(ROLLUP_TTM_2024),
                "B8": money(model_arr),
                "B9": money(ntm_arr),
                "B11": round(cap["pps"], 4),  # per-share price; keep 4 dp (not money/cents)
                "B13": money(fd_mid_r),
                "B19": money(cap["s1"]),
                "B20": money(cap["s2"]),
                "B21": money(cap["lockwood_prorata_shares"]),
                "B22": money(cap["summit_shares"]),
                "B24": money(pool_refresh_r),
                "B25": money(pool_refresh_12_r),
                "B40": money(fd_post_r),
                "B41": round(SAFE1_CAP / FD_PRE, 4),
                "B42": round(cap["pps"] * (1 - SAFE1_DISC), 4),
                "B43": round(min(SAFE1_CAP / FD_PRE, cap["pps"] * (1 - SAFE1_DISC)), 4),
                "B44": money(cap["existing_pool"]),
                "B45": money(advisor_warrant_unexercised()),
                "B46": 1.0,
            },
            "Cohort Build": {
                **{
                    f"G{i}": cohort_layout["ending_arr_cache"][i - cohort_layout["start_row"]]
                    for i in range(
                        cohort_layout["start_row"],
                        cohort_layout["inv_end"] + 1,
                    )
                },
                f"B{cohort_layout['ctrl'] + 1}": float(len(inventory)),
                f"B{cohort_layout['ctrl'] + 2}": 1.0,
                f"B{cohort_layout['ctrl'] + 3}": float(len(retained_rows)),
                **{
                    f"B{cohort_layout['rollup_start'] + i}": money(ROLLUP_2024[q])
                    for i, q in enumerate(["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"])
                },
                f"B{cohort_layout['ttm_row']}": money(ROLLUP_TTM_2024),
                f"B{cohort_layout['norm_row']}": money(model_arr),
            },
            "Revenue Forecast": {
                **{f"C{i}": money(forecast[i - 2]) for i in range(2, 8)},
                **{f"D{i}": ratio(FCF_MARGIN) for i in range(2, 8)},
                **{f"E{i}": money(forecast[i - 2] * FCF_MARGIN) for i in range(2, 8)},
                "B3": ratio(FORECAST_GROWTH[0]),
            },
            "DCF Build": {
                **dcf_pv_rows,
                **{f"B{year + 1}": money(forecast[year]) for year in range(1, 6)},
                "J1": ratio(WACC_LOW),
                "J2": ratio(WACC_HIGH),
                "J3": ratio(FCF_MARGIN),
                "J4": ratio(TERMINAL_GROWTH),
            },
            "Cap Table Pro Forma": cap_cache,
            "Valuation Summary": {
                "B4": money(model_arr),
                "B5": money(ntm_arr),
                val_mult_low: money(mult_low_val),
                val_mult_high: money(mult_high_val),
                val_mult_mid: money(mult_mid),
                val_downside: money(downside_ev),
                val_peer_cell: money(peer_base),
                "B20": money(PRE_MONEY),
                "B21": money(POST_MONEY),
                val_dcf_high: money(dcf_ev_high),
                val_dcf_low: money(dcf_ev_low),
                val_dcf_mid: money(dcf_mid),
                val_variance: money(mult_mid - dcf_mid),
            },
            "Sensitivity": sens_values,
            "Option pool cases": {
                "B2": ratio(0.12),
                "C2": money(cap["existing_pool"]),
                "D2": money(pool_refresh_12_r),
                "E2": money(fd_post_12_r),
                "F2": ratio((cap["existing_pool"] + pool_refresh_12_r) / fd_post_12_r),
                "B3": ratio(POOL_TARGET_PCT),
                "C3": money(cap["existing_pool"]),
                "D3": money(pool_refresh_r),
                "E3": money(fd_post_r),
                "F3": ratio((cap["existing_pool"] + pool_refresh_r) / fd_post_r),
            },
        },
    )
    sanitize_xlsx(OUT)
    print(
        f"Wrote {OUT} | model_arr={model_arr:.2f} | ntm={ntm_arr:.2f} | "
        f"pps={cap['pps']:.4f} | s1={cap['s1']:.0f} | s2={cap['s2']:.0f} | "
        f"fd_post={fd_post_r:.0f} | peer_base={peer_base:.2f} | "
        f"pool_base={cap['existing_pool']:.0f} | refresh15={pool_refresh_r:.0f} | "
        f"forsyth_post={forsyth_post:.0f} | forsyth_own={forsyth_post/total_post:.6%} | "
        f"retained={len(retained_rows)} | inventory={len(inventory)} | "
        f"ttm_row={cohort_layout['ttm_row']} | norm_row={cohort_layout['norm_row']}"
    )


if __name__ == "__main__":
    build()
