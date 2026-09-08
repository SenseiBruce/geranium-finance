#!/usr/bin/env python3
"""Generate the reviewed Ironclad Telematics valuation workbook."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

from ironclad_constants import (
    BRIEF_RUN_RATE,
    COUNSEL_POOL_PCT,
    EXISTING_AVAILABLE_POOL,
    FCF_MARGIN,
    FD_PRE,
    FORECAST_GROWTH,
    LEAD_INVESTOR,
    MODEL_ARR,
    MULT_DOWN,
    MULT_HIGH,
    MULT_LOW,
    NOTE_A_CAP,
    NOTE_A_DISCOUNT,
    NOTE_A_HOLDER,
    NOTE_A_PRINCIPAL,
    NOTE_B_CAP,
    NOTE_B_HOLDER,
    NOTE_B_PRINCIPAL,
    PILOT_ARR,
    PILOT_CUSTOMER,
    POOL_TARGET_PCT,
    POST_MONEY,
    PRE_MONEY,
    PRIMARY,
    ROLLUP_2024,
    ROLLUP_TTM,
    SEED_INVESTOR,
    SEED_SHARES,
    TERMINAL_GROWTH,
    WACC_HIGH,
    WACC_LOW,
)
from sanitize_office import cache_xlsx_formula_values, sanitize_xlsx

TASK = Path(__file__).resolve().parent.parent / "tasks" / "ironclad-telematics-valuation"
INPUTS = TASK / "inputs"
OUT = TASK / "golden" / "ironclad_telematics_valuation.xlsx"


def money(value: float) -> float:
    return round(float(value), 2)


def ratio(value: float) -> float:
    return round(float(value), 8)


def existing_pool_from_cap_table() -> float:
    with (INPUTS / "ironclad_cap_table.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["holder"] == "2021 Equity Plan (available)":
                return float(row["shares"])
    raise ValueError("Available option pool row missing from ironclad_cap_table.csv")


def source_cohort_rows() -> list[tuple[object, ...]]:
    wb = load_workbook(INPUTS / "ironclad_fleet_cohort_arr.xlsx", data_only=True, read_only=True)
    ws = wb["Cohort Detail"]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    idx = {name: i for i, name in enumerate(headers)}
    rows = []
    for raw in ws.iter_rows(min_row=2, values_only=True):
        if raw[idx["calendar_quarter"]] == "2024-Q4":
            rows.append(
                (
                    raw[idx["cohort_id"]],
                    raw[idx["fiscal_month_label"]],
                    raw[idx["calendar_quarter"]],
                    raw[idx["starting_arr"]],
                    raw[idx["vehicle_count"]],
                    raw[idx["gross_retention_pct"]],
                    raw[idx["expansion_arr"]],
                    raw[idx["churn_arr"]],
                    raw[idx["revenue_tag"]],
                    raw[idx["notes"]],
                )
            )
    wb.close()
    return rows


def muni_ending_by_quarter() -> dict[str, float]:
    wb = load_workbook(INPUTS / "ironclad_fleet_cohort_arr.xlsx", data_only=True, read_only=True)
    ws = wb["Cohort Detail"]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    idx = {name: i for i, name in enumerate(headers)}
    out: dict[str, float] = {}
    for raw in ws.iter_rows(min_row=2, values_only=True):
        if raw[idx["cohort_id"]] == "IC-MUNI-24" and str(raw[idx["calendar_quarter"]]).startswith("2024"):
            out[str(raw[idx["calendar_quarter"]])] = money(float(raw[idx["ending_arr"]]))
    wb.close()
    return out


def compute_cap_table() -> dict[str, float]:
    existing_pool = money(existing_pool_from_cap_table())
    pps = ratio(PRE_MONEY / FD_PRE)
    note_a_cap_price = ratio(NOTE_A_CAP / FD_PRE)
    note_a_discount_price = ratio(pps * (1 - NOTE_A_DISCOUNT))
    note_a_price = min(note_a_cap_price, note_a_discount_price)
    note_b_price = ratio(NOTE_B_CAP / FD_PRE)
    note_a_shares = money(NOTE_A_PRINCIPAL / note_a_price)
    note_b_shares = money(NOTE_B_PRINCIPAL / note_b_price)
    seed_primary = money(PRIMARY * SEED_SHARES / FD_PRE)
    lead_primary = money(PRIMARY - seed_primary)
    seed_new_shares = money(seed_primary / pps)
    lead_new_shares = money(lead_primary / pps)
    fd_mid = money(FD_PRE + note_a_shares + note_b_shares + seed_new_shares + lead_new_shares)
    pool_refresh = money(max((POOL_TARGET_PCT * fd_mid - existing_pool) / (1 - POOL_TARGET_PCT), 0))
    pool_refresh_10 = money(max((COUNSEL_POOL_PCT * fd_mid - existing_pool) / (1 - COUNSEL_POOL_PCT), 0))
    return {
        "existing_pool": existing_pool,
        "pps": pps,
        "note_a_cap_price": note_a_cap_price,
        "note_a_discount_price": note_a_discount_price,
        "note_a_price": note_a_price,
        "note_b_price": note_b_price,
        "note_a_shares": note_a_shares,
        "note_b_shares": note_b_shares,
        "seed_primary": seed_primary,
        "lead_primary": lead_primary,
        "seed_new_shares": seed_new_shares,
        "lead_new_shares": lead_new_shares,
        "fd_mid": fd_mid,
        "pool_refresh": pool_refresh,
        "pool_refresh_10": pool_refresh_10,
        "fd_post": money(fd_mid + pool_refresh),
        "fd_post_10": money(fd_mid + pool_refresh_10),
    }


def forecast_values() -> list[float]:
    values = [money(MODEL_ARR)]
    for growth in FORECAST_GROWTH:
        values.append(money(values[-1] * (1 + growth)))
    return values


def dcf_value(forecast: list[float], wacc: float) -> float:
    pv = sum(forecast[y] * FCF_MARGIN / ((1 + wacc) ** y) for y in range(1, 6))
    terminal = forecast[5] * FCF_MARGIN * (1 + TERMINAL_GROWTH) / (wacc - TERMINAL_GROWTH)
    return pv + terminal / ((1 + wacc) ** 5)


def apply_display_formatting(wb: Workbook) -> None:
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for column in ws.columns:
            letter = column[0].column_letter
            max_len = min(max(len(str(cell.value or "")) for cell in column) + 2, 55)
            ws.column_dimensions[letter].width = max(12, max_len)


def build() -> None:
    cap = compute_cap_table()
    forecast = forecast_values()
    source_rows = source_cohort_rows()
    muni_q = muni_ending_by_quarter()
    dcf_high = dcf_value(forecast, WACC_LOW)
    dcf_low = dcf_value(forecast, WACC_HIGH)

    wb = Workbook()
    assumptions = wb.active
    assumptions.title = "Assumptions"
    assumptions["A1"] = "Ironclad Telematics — growth-equity valuation inputs"
    assumptions["B1"] = "Value"
    assumption_rows = [
        ("Pre-money valuation", PRE_MONEY),
        ("Primary proceeds", PRIMARY),
        ("Post-money before pool refresh", POST_MONEY),
        ("Calendar 2024 cohort TTM", ROLLUP_TTM),
        ("Municipal pilot excluded", PILOT_ARR),
        ("Normalized model ARR", MODEL_ARR),
        ("Brief headline run-rate (not used)", BRIEF_RUN_RATE),
        ("Fully diluted pre-money shares", FD_PRE),
        (f"{SEED_INVESTOR} Series Seed preferred shares", SEED_SHARES),
        ("Growth round price per share", cap["pps"]),
        ("Note A cap price", cap["note_a_cap_price"]),
        ("Note A discounted round price", cap["note_a_discount_price"]),
        ("Note A conversion price (lower)", cap["note_a_price"]),
        ("Note B cap conversion price", cap["note_b_price"]),
        ("Note A conversion shares", cap["note_a_shares"]),
        ("Note B conversion shares", cap["note_b_shares"]),
        ("Existing available option pool shares", cap["existing_pool"]),
        ("FD shares before pool refresh", cap["fd_mid"]),
        ("Sponsor post-money pool target", POOL_TARGET_PCT),
        ("Counsel available-pool reference", COUNSEL_POOL_PCT),
        ("Sponsor-case pool refresh shares", cap["pool_refresh"]),
        ("FCF margin", FCF_MARGIN),
        ("DCF WACC low", WACC_LOW),
        ("DCF WACC high", WACC_HIGH),
        ("Terminal growth", TERMINAL_GROWTH),
        ("Peer median NTM multiple", 5.2),
        ("NTM multiple — low", MULT_LOW),
        ("NTM multiple — high", MULT_HIGH),
        ("TTM downside multiple", MULT_DOWN),
        (f"{NOTE_A_HOLDER} Note A principal", NOTE_A_PRINCIPAL),
        (f"{NOTE_A_HOLDER} Note A valuation cap", NOTE_A_CAP),
        (f"{NOTE_A_HOLDER} Note A discount", NOTE_A_DISCOUNT),
        (f"{NOTE_B_HOLDER} Note B principal", NOTE_B_PRINCIPAL),
        (f"{NOTE_B_HOLDER} Note B valuation cap", NOTE_B_CAP),
        (f"{SEED_INVESTOR} pro-rata primary proceeds", cap["seed_primary"]),
        (f"{LEAD_INVESTOR} lead primary proceeds", cap["lead_primary"]),
    ]
    assumption_index: dict[str, int] = {}
    for row_num, (label, value) in enumerate(assumption_rows, start=3):
        assumptions.cell(row_num, 1, label)
        assumptions.cell(row_num, 2, value)
        assumption_index[label] = row_num

    cohort = wb.create_sheet("Fleet Cohort Build")
    cohort.append(
        [
            "cohort_id",
            "fiscal_month_label",
            "calendar_quarter",
            "starting_arr",
            "vehicle_count",
            "gross_retention_pct",
            "expansion_arr",
            "churn_arr",
            "ending_arr",
            "include_in_model",
            "adjusted_ending_arr",
            "source_treatment",
        ]
    )
    cohort_cache: dict[str, float] = {}
    for row_num, row in enumerate(source_rows, start=2):
        cohort_id, fiscal, quarter, start, vehicles, retention, expansion, churn, tag, note = row
        cohort.cell(row_num, 1, cohort_id)
        cohort.cell(row_num, 2, fiscal)
        cohort.cell(row_num, 3, quarter)
        cohort.cell(row_num, 4, money(float(start)))
        cohort.cell(row_num, 5, vehicles)
        cohort.cell(row_num, 6, round(float(retention), 1))
        cohort.cell(row_num, 7, money(float(expansion)))
        cohort.cell(row_num, 8, money(float(churn)))
        cohort.cell(row_num, 9, f"=D{row_num}*F{row_num}/100+G{row_num}-H{row_num}")
        is_duplicate = cohort_id == "IC-2023-02-XP"
        is_pilot = tag == "pilot_non_recurring"
        include = 0 if (is_duplicate or is_pilot) else 1
        cohort.cell(row_num, 10, include)
        cohort.cell(row_num, 11, f"=I{row_num}*J{row_num}")
        treatment = "Included"
        if is_duplicate:
            treatment = "Excluded: duplicate expansion row"
        elif is_pilot:
            treatment = "Excluded: pilot_non_recurring per brief Footnote 1"
        cohort.cell(row_num, 12, treatment if not note else f"{treatment}; {note}")
        ending = round(float(retention), 1) / 100 * float(start) + float(expansion) - float(churn)
        cohort_cache[f"I{row_num}"] = money(ending)
        cohort_cache[f"K{row_num}"] = money(ending * include)

    summary_start = len(source_rows) + 4
    cohort.cell(summary_start, 1, "calendar_quarter")
    cohort.cell(summary_start, 2, "source_rollup_arr")
    cohort.cell(summary_start, 3, "source")
    for offset, (quarter, arr) in enumerate(ROLLUP_2024.items(), start=1):
        row_num = summary_start + offset
        cohort.cell(row_num, 1, quarter)
        cohort.cell(row_num, 2, arr)
        cohort.cell(row_num, 3, "ironclad_fleet_cohort_arr.xlsx / Fleet Rollup")
    ttm_row = summary_start + 6
    model_row = summary_start + 7
    cohort.cell(ttm_row, 1, "Calendar 2024 TTM")
    cohort.cell(ttm_row, 2, f"=SUM(B{summary_start + 1}:B{summary_start + 4})")
    cohort.cell(model_row, 1, "Normalized model ARR")
    cohort.cell(model_row, 2, f"=B{ttm_row}-Assumptions!B{assumption_index['Municipal pilot excluded']}")
    cohort_cache[f"B{ttm_row}"] = money(ROLLUP_TTM)
    cohort_cache[f"B{model_row}"] = money(MODEL_ARR)

    revenue = wb.create_sheet("Revenue Forecast")
    revenue.append(["period", "growth_rate", "arr", "fcf_margin", "free_cash_flow"])
    revenue["A2"] = "Base / normalized TTM"
    revenue["B2"] = 0
    revenue["C2"] = f"='Fleet Cohort Build'!B{model_row}"
    revenue["D2"] = FCF_MARGIN
    revenue["E2"] = "=C2*D2"
    revenue_cache: dict[str, float] = {"C2": money(forecast[0]), "E2": money(forecast[0] * FCF_MARGIN)}
    for year, growth in enumerate(FORECAST_GROWTH, start=1):
        row_num = year + 2
        revenue.cell(row_num, 1, f"Year {year}")
        revenue.cell(row_num, 2, growth)
        revenue.cell(row_num, 3, f"=C{row_num - 1}*(1+B{row_num})")
        revenue.cell(row_num, 4, f"=Assumptions!B{assumption_index['FCF margin']}")
        revenue.cell(row_num, 5, f"=C{row_num}*D{row_num}")
        revenue_cache[f"C{row_num}"] = money(forecast[year])
        revenue_cache[f"D{row_num}"] = ratio(FCF_MARGIN)
        revenue_cache[f"E{row_num}"] = money(forecast[year] * FCF_MARGIN)

    dcf = wb.create_sheet("DCF Build")
    dcf.append(["year", "arr", "fcf", "discount_factor_13pct", "pv_13pct", "discount_factor_15pct", "pv_15pct"])
    dcf_cache: dict[str, float] = {}
    for year in range(1, 6):
        row_num = year + 1
        dcf.cell(row_num, 1, year)
        dcf.cell(row_num, 2, f"='Revenue Forecast'!C{year + 2}")
        dcf.cell(row_num, 3, f"=B{row_num}*Assumptions!B{assumption_index['FCF margin']}")
        dcf.cell(row_num, 4, f"=1/(1+Assumptions!B{assumption_index['DCF WACC low']})^A{row_num}")
        dcf.cell(row_num, 5, f"=C{row_num}*D{row_num}")
        dcf.cell(row_num, 6, f"=1/(1+Assumptions!B{assumption_index['DCF WACC high']})^A{row_num}")
        dcf.cell(row_num, 7, f"=C{row_num}*F{row_num}")
        fcf = forecast[year] * FCF_MARGIN
        df_low = 1 / ((1 + WACC_LOW) ** year)
        df_high = 1 / ((1 + WACC_HIGH) ** year)
        dcf_cache.update(
            {
                f"B{row_num}": money(forecast[year]),
                f"C{row_num}": money(fcf),
                f"D{row_num}": ratio(df_low),
                f"E{row_num}": money(fcf * df_low),
                f"F{row_num}": ratio(df_high),
                f"G{row_num}": money(fcf * df_high),
            }
        )

    cap_ws = wb.create_sheet("Cap Table Pro Forma")
    cap_ws.append(
        [
            "holder / security",
            "pre_shares",
            "principal_or_primary",
            "conversion_or_round_price",
            "conversion_shares",
            "primary_shares",
            "post_shares",
            "post_ownership",
            "treatment",
        ]
    )
    # Cap Table Pro Forma: transaction parameters linked to Assumptions where practical.
    a_fd = f"Assumptions!B{assumption_index['Fully diluted pre-money shares']}"
    a_note_a_prin = f"Assumptions!B{assumption_index[f'{NOTE_A_HOLDER} Note A principal']}"
    a_note_a_price = f"Assumptions!B{assumption_index['Note A conversion price (lower)']}"
    a_note_a_shares = f"Assumptions!B{assumption_index['Note A conversion shares']}"
    a_note_b_prin = f"Assumptions!B{assumption_index[f'{NOTE_B_HOLDER} Note B principal']}"
    a_note_b_price = f"Assumptions!B{assumption_index['Note B cap conversion price']}"
    a_note_b_shares = f"Assumptions!B{assumption_index['Note B conversion shares']}"
    a_seed_primary = f"Assumptions!B{assumption_index[f'{SEED_INVESTOR} pro-rata primary proceeds']}"
    a_lead_primary = f"Assumptions!B{assumption_index[f'{LEAD_INVESTOR} lead primary proceeds']}"
    a_pps = f"Assumptions!B{assumption_index['Growth round price per share']}"
    a_pool = f"Assumptions!B{assumption_index['Sponsor-case pool refresh shares']}"

    cap_rows = [
        (
            "Existing holders (including available pool)",
            f"={a_fd}",
            0,
            0,
            0,
            0,
            FD_PRE,
            0,
            0,
            "Pre-money FD from ironclad_cap_table.csv",
        ),
        (
            f"{NOTE_A_HOLDER} — Note A",
            0,
            f"={a_note_a_prin}",
            f"={a_note_a_price}",
            f"={a_note_a_shares}",
            0,
            0,
            cap["note_a_shares"],
            0,
            "Displayed first per brief; cap price wins",
        ),
        (
            f"{NOTE_B_HOLDER} — Note B",
            0,
            f"={a_note_b_prin}",
            f"={a_note_b_price}",
            f"={a_note_b_shares}",
            0,
            0,
            cap["note_b_shares"],
            0,
            "Cap-only conversion",
        ),
        (
            f"{SEED_INVESTOR} — pro-rata primary",
            0,
            f"={a_seed_primary}",
            f"={a_pps}",
            0,
            f"={a_seed_primary}/{a_pps}",
            0,
            0,
            cap["seed_new_shares"],
            "Full pro-rata modeling case",
        ),
        (
            f"{LEAD_INVESTOR} — lead primary",
            0,
            f"={a_lead_primary}",
            f"={a_pps}",
            0,
            f"={a_lead_primary}/{a_pps}",
            0,
            0,
            cap["lead_new_shares"],
            "Primary remainder",
        ),
        (
            "Incremental option pool refresh",
            0,
            0,
            0,
            0,
            f"={a_pool}",
            0,
            0,
            cap["pool_refresh"],
            "12% post-money sponsor case",
        ),
    ]
    post_shares: list[float] = []
    cap_cache: dict[str, float] = {}
    for row_num, (
        name,
        pre,
        proceeds,
        price,
        conversion,
        primary_shares,
        pre_val,
        conv_val,
        prim_val,
        treatment,
    ) in enumerate(cap_rows, start=2):
        cap_ws.cell(row_num, 1, name)
        cap_ws.cell(row_num, 2, pre)
        cap_ws.cell(row_num, 3, proceeds)
        cap_ws.cell(row_num, 4, price)
        cap_ws.cell(row_num, 5, conversion)
        cap_ws.cell(row_num, 6, primary_shares)
        cap_ws.cell(row_num, 7, f"=B{row_num}+E{row_num}+F{row_num}")
        cap_ws.cell(row_num, 8, f"=G{row_num}/SUM($G$2:$G$7)")
        cap_ws.cell(row_num, 9, treatment)
        post = pre_val + conv_val + prim_val
        post_shares.append(post)
        if isinstance(pre, (int, float)):
            cap_cache[f"B{row_num}"] = money(pre)
        else:
            cap_cache[f"B{row_num}"] = money(pre_val)
        if isinstance(proceeds, (int, float)) and proceeds:
            cap_cache[f"C{row_num}"] = money(proceeds)
        elif not isinstance(proceeds, (int, float)):
            # formula-linked proceeds
            if row_num == 3:
                cap_cache[f"C{row_num}"] = money(NOTE_A_PRINCIPAL)
            elif row_num == 4:
                cap_cache[f"C{row_num}"] = money(NOTE_B_PRINCIPAL)
            elif row_num == 5:
                cap_cache[f"C{row_num}"] = money(cap["seed_primary"])
            elif row_num == 6:
                cap_cache[f"C{row_num}"] = money(cap["lead_primary"])
        if not isinstance(price, (int, float)):
            if row_num == 3:
                cap_cache[f"D{row_num}"] = ratio(cap["note_a_price"])
            elif row_num == 4:
                cap_cache[f"D{row_num}"] = ratio(cap["note_b_price"])
            elif row_num in (5, 6):
                cap_cache[f"D{row_num}"] = ratio(cap["pps"])
        if not isinstance(conversion, (int, float)):
            if row_num == 3:
                cap_cache[f"E{row_num}"] = money(cap["note_a_shares"])
            elif row_num == 4:
                cap_cache[f"E{row_num}"] = money(cap["note_b_shares"])
        if not isinstance(primary_shares, (int, float)):
            if row_num == 5:
                cap_cache[f"F{row_num}"] = money(cap["seed_new_shares"])
            elif row_num == 6:
                cap_cache[f"F{row_num}"] = money(cap["lead_new_shares"])
            elif row_num == 7:
                cap_cache[f"F{row_num}"] = money(cap["pool_refresh"])
    post_total = sum(post_shares)
    for row_num, post in enumerate(post_shares, start=2):
        cap_cache[f"G{row_num}"] = money(post)
        cap_cache[f"H{row_num}"] = ratio(post / post_total)

    valuation = wb.create_sheet("Valuation Summary")
    valuation.append(["method", "enterprise_value", "basis"])
    a_mult_down = f"Assumptions!B{assumption_index['TTM downside multiple']}"
    a_mult_low = f"Assumptions!B{assumption_index['NTM multiple — low']}"
    a_mult_high = f"Assumptions!B{assumption_index['NTM multiple — high']}"
    valuation_rows = [
        ("Downside revenue multiple", f"=Assumptions!B{assumption_index['Normalized model ARR']}*{a_mult_down}", f"{MULT_DOWN}x normalized TTM"),
        ("NTM revenue multiple — low", f"='Revenue Forecast'!C3*{a_mult_low}", f"{MULT_LOW}x Year 1 NTM"),
        ("NTM revenue multiple — high", f"='Revenue Forecast'!C3*{a_mult_high}", f"{MULT_HIGH}x Year 1 NTM"),
        ("DCF — 13% WACC", f"=SUM('DCF Build'!E2:E6)+'DCF Build'!C6*(1+{TERMINAL_GROWTH})/({WACC_LOW}-{TERMINAL_GROWTH})/(1+{WACC_LOW})^5", "Five-year FCF plus terminal value"),
        ("DCF — 15% WACC", f"=SUM('DCF Build'!G2:G6)+'DCF Build'!C6*(1+{TERMINAL_GROWTH})/({WACC_HIGH}-{TERMINAL_GROWTH})/(1+{WACC_HIGH})^5", "Five-year FCF plus terminal value"),
        ("Midpoint revenue-multiple valuation", "=(B3+B4)/2", "Average of 4.5x–6.0x NTM cases"),
        ("Midpoint DCF-implied valuation", "=(B5+B6)/2", "Average of 13%–15% WACC cases"),
        ("Multiple vs DCF midpoint variance", "=B7-B8", "Reconciliation of market and DCF views"),
        ("Term-sheet pre-money", PRE_MONEY, "growth_equity_diligence_brief.txt"),
        ("Term-sheet post-money before pool", POST_MONEY, "growth_equity_diligence_brief.txt"),
    ]
    valuation_cache: dict[str, float] = {}
    mult_mid = money((forecast[1] * MULT_LOW + forecast[1] * MULT_HIGH) / 2)
    dcf_mid = money((dcf_high + dcf_low) / 2)
    valuation_values = [
        MODEL_ARR * MULT_DOWN,
        forecast[1] * MULT_LOW,
        forecast[1] * MULT_HIGH,
        dcf_high,
        dcf_low,
        mult_mid,
        dcf_mid,
        mult_mid - dcf_mid,
    ]
    for row_num, (method, value, basis) in enumerate(valuation_rows, start=2):
        valuation.cell(row_num, 1, method)
        valuation.cell(row_num, 2, value)
        valuation.cell(row_num, 3, basis)
        if row_num <= 9:
            valuation_cache[f"B{row_num}"] = money(valuation_values[row_num - 2])

    sensitivity = wb.create_sheet("Sensitivity")
    sensitivity.append(["net_retention", "fleet_growth", "implied_ntm_value", "method"])
    sensitivity["F1"] = "normalized_ttm"
    sensitivity["G1"] = f"=Assumptions!B{assumption_index['Normalized model ARR']}"
    sensitivity["F2"] = "selected_multiple"
    sensitivity["G2"] = f"=Assumptions!B{assumption_index['Peer median NTM multiple']}"
    sensitivity_cache: dict[str, float] = {"G1": money(MODEL_ARR), "G2": 5.2}
    row_num = 2
    for nrr in [1.04, 1.08, 1.12]:
        for growth in [0.20, 0.26, 0.32]:
            sensitivity.cell(row_num, 1, nrr)
            sensitivity.cell(row_num, 2, growth)
            sensitivity.cell(row_num, 3, f"=$G$1*A{row_num}*(1+B{row_num})*$G$2")
            sensitivity.cell(
                row_num,
                4,
                "Peer-median NTM multiple from Assumptions; NRR and fleet growth varied",
            )
            sensitivity_cache[f"C{row_num}"] = money(MODEL_ARR * nrr * (1 + growth) * 5.2)
            row_num += 1

    pools = wb.create_sheet("Option pool cases")
    pools.append(["case", "target_pct", "existing_available", "fd_before_refresh", "incremental_refresh", "fd_post", "combined_pool_pct", "treatment"])
    pool_cases = [
        ("Counsel reference", COUNSEL_POOL_PCT, cap["pool_refresh_10"], cap["fd_post_10"], "Alternate only; cap-table note"),
        ("Sponsor term sheet", POOL_TARGET_PCT, cap["pool_refresh"], cap["fd_post"], "Primary pro forma case"),
    ]
    pool_cache: dict[str, float] = {}
    for row_num, (name, target, refresh, fd_post, treatment) in enumerate(pool_cases, start=2):
        pools.cell(row_num, 1, name)
        pools.cell(row_num, 2, target)
        pools.cell(row_num, 3, f"=Assumptions!B{assumption_index['Existing available option pool shares']}")
        pools.cell(row_num, 4, f"=Assumptions!B{assumption_index['FD shares before pool refresh']}")
        pools.cell(row_num, 5, f"=MAX((B{row_num}*D{row_num}-C{row_num})/(1-B{row_num}),0)")
        pools.cell(row_num, 6, f"=D{row_num}+E{row_num}")
        pools.cell(row_num, 7, f"=(C{row_num}+E{row_num})/F{row_num}")
        pools.cell(row_num, 8, treatment)
        pool_cache.update(
            {
                f"C{row_num}": money(cap["existing_pool"]),
                f"D{row_num}": money(cap["fd_mid"]),
                f"E{row_num}": money(refresh),
                f"F{row_num}": money(fd_post),
                f"G{row_num}": ratio(target),
            }
        )

    notes = wb.create_sheet("Notes")
    notes["A1"] = "Workpaper notes — source conflicts, judgments, and citations"
    notes["A2"] = "topic"
    notes["B2"] = "detail"
    notes["A2"].font = Font(bold=True)
    notes["B2"].font = Font(bold=True)

    note_rows: list[tuple[str, str]] = [
        (
            "ARR bridge — Fleet Rollup TTM",
            f"Source: ironclad_fleet_cohort_arr.xlsx / Fleet Rollup. Sum of calendar 2024 fleet_arr = "
            f"${ROLLUP_TTM:,.2f}. Treatment: used as TTM reference before Footnote 1 exclusion. "
            f"Cite: growth_equity_diligence_brief.txt (ARR bridge paragraph).",
        ),
        (
            "Fleet Rollup vs Cohort Detail",
            "Sources: growth_equity_diligence_brief.txt — ARR/run-rate methodology (Fleet Rollup vs Cohort "
            "Detail recognition guidance); ironclad_fleet_cohort_arr.xlsx — Fleet Rollup (2024 quarterly "
            "fleet_arr totals), Cohort Detail (ending_arr by billing cohort), Recognition Bridge "
            "(fleet_arr identity), and Definitions (field definitions). Issue: Cohort Detail ending_arr "
            "(gross contracted ARR by billing cohort) does not equal Fleet Rollup fleet_arr "
            "(finance-recognized subscription ARR) at the quarterly total. Vehicle counts also differ "
            "because Fleet Rollup includes onboarding units not yet tagged to a cohort_id. Treatment: "
            "board TTM uses Fleet Rollup fleet_arr. Bridge identity on Recognition Bridge: fleet_arr = "
            "SUMIF(Cohort Detail ending_arr by calendar_quarter) − IC-2023-02-XP duplicate − "
            "recognition_timing_adj. Rationale: contracted billing view vs subscription-ledger "
            "recognition; timing adj covers implementation deferrals and multi-year billings not yet in "
            "the finance rollup. Consequence: do not substitute the raw Cohort Detail sum for board TTM.",
        ),
        (
            "MetroLink MUNI exclusion vs Cohort Detail",
            f"Source: growth_equity_diligence_brief.txt Footnote 1 states ${PILOT_ARR:,.0f} award-year "
            f"annualized exclusion for {PILOT_CUSTOMER} (pilot_non_recurring). Source schedule: "
            f"ironclad_fleet_cohort_arr.xlsx / Cohort Detail row IC-MUNI-24 shows higher 2024 ending_arr "
            f"(Q1 ${muni_q.get('2024-Q1', 0):,.0f}; Q2 ${muni_q.get('2024-Q2', 0):,.0f}; "
            f"Q3 ${muni_q.get('2024-Q3', 0):,.0f}; Q4 ${muni_q.get('2024-Q4', 0):,.0f}) after mid-pilot "
            f"vehicle adds and rate schedule. Issue: ${PILOT_ARR:,.0f} cannot be tied to any single IC-MUNI-24 "
            f"ending_arr cell. Treatment: model subtracts the brief's ${PILOT_ARR:,.0f} from Fleet Rollup TTM "
            f"(normalized ARR ${MODEL_ARR:,.2f}). Rationale: Footnote 1 is the governing sponsor/diligence "
            f"instruction. Consequence: if a reviewer instead excluded current-period IC-MUNI-24 ending_arr "
            f"(or a TTM average thereof), normalized ARR would be lower by roughly the excess of cohort MUNI "
            f"over ${PILOT_ARR:,.0f}; flag for board/committee review.",
        ),
        (
            "Management headline run-rate",
            f"Source: growth_equity_diligence_brief.txt quotes ${BRIEF_RUN_RATE:,.0f}. Issue: exceeds Fleet "
            f"Rollup TTM. Treatment: disclosed only; not used as valuation base.",
        ),
        (
            "Fiscal vs calendar period labels",
            "Sources: growth_equity_diligence_brief.txt — Footnote 2; ironclad_fleet_cohort_arr.xlsx — "
            "Cohort Detail fiscal_month_label vs calendar_quarter columns. Issue: FY25-M01/M04/M07 look "
            "like calendar 2025 but map to 2024-Q2/Q3/Q4. Treatment: calendar_quarter governs "
            "trailing-period selection on Fleet Cohort Build.",
        ),
        (
            "Duplicate expansion row",
            "Sources: growth_equity_diligence_brief.txt — duplicate expansion / retention guidance; "
            "ironclad_fleet_cohort_arr.xlsx — Cohort Detail row IC-2023-02-XP (and Recognition Bridge "
            "duplicate column). Issue: repeats IC-2022-04 fleet amendment. Treatment: IC-2023-02-XP is "
            "excluded from retention math because it duplicates the prior fleet amendment and is already "
            "captured in the earlier row. Implementation: include_in_model = FALSE on Fleet Cohort Build; "
            "also removed from the Recognition Bridge duplicate column.",
        ),
        (
            "Convertible note mechanics",
            f"Sources: growth_equity_diligence_brief.txt — note conversion order and mechanics; "
            f"ironclad_cap_table.csv — {NOTE_A_HOLDER} and {NOTE_B_HOLDER} convertible note rows. "
            f"{NOTE_A_HOLDER} Note A: ${NOTE_A_PRINCIPAL:,.0f}, ${NOTE_A_CAP:,.0f} cap, "
            f"{NOTE_A_DISCOUNT:.0%} discount — lower of cap price and discounted round price; displayed "
            f"before Note B. {NOTE_B_HOLDER} Note B: ${NOTE_B_PRINCIPAL:,.0f}, ${NOTE_B_CAP:,.0f} cap, "
            f"no discount. Both use the {FD_PRE:,}-share pre-money denominator; denominator does not "
            f"change between notes.",
        ),
        (
            "Option pool 10% vs 12%",
            f"Source: ironclad_cap_table.csv counsel note shows {COUNSEL_POOL_PCT:.0%} available pool; "
            f"growth_equity_diligence_brief.txt requires {POOL_TARGET_PCT:.0%} post-money at closing. "
            f"Treatment: Cap Table Pro Forma uses {POOL_TARGET_PCT:.0%} sponsor case "
            f"({cap['pool_refresh']:,.2f} incremental shares); Option pool cases also shows the "
            f"{COUNSEL_POOL_PCT:.0%} alternate.",
        ),
        (
            "Quorum pro-rata allocation",
            f"Source: growth_equity_diligence_brief.txt Primary allocation. Treatment: {SEED_INVESTOR} "
            f"purchases ${cap['seed_primary']:,.2f} ({SEED_SHARES:,}/{FD_PRE:,} × ${PRIMARY:,.0f}); "
            f"{LEAD_INVESTOR} takes ${cap['lead_primary']:,.2f}. Modeling convention pending executed "
            f"subscription documents.",
        ),
        (
            "Forecast and cross-checks",
            f"Revenue Forecast: 26%/22%/18%/15%/12% growth and {FCF_MARGIN:.0%} FCF margin from "
            f"growth_equity_diligence_brief.txt. DCF: {WACC_LOW:.0%}–{WACC_HIGH:.0%} WACC, "
            f"{TERMINAL_GROWTH:.0%} terminal growth. Multiples: {MULT_LOW:.1f}x–{MULT_HIGH:.1f}x NTM; "
            f"{MULT_DOWN:.1f}x TTM downside; Sensitivity uses Assumptions peer-median 5.2x.",
        ),
    ]
    for row_num, (topic, detail) in enumerate(note_rows, start=3):
        notes.cell(row_num, 1, topic)
        notes.cell(row_num, 2, detail)
    notes.column_dimensions["A"].width = 42
    notes.column_dimensions["B"].width = 120

    apply_display_formatting(wb)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    cache_xlsx_formula_values(
        OUT,
        {
            "Fleet Cohort Build": cohort_cache,
            "Revenue Forecast": revenue_cache,
            "DCF Build": dcf_cache,
            "Cap Table Pro Forma": cap_cache,
            "Valuation Summary": valuation_cache,
            "Sensitivity": sensitivity_cache,
            "Option pool cases": pool_cache,
        },
    )
    sanitize_xlsx(OUT)
    print(
        f"Wrote {OUT} | model_arr={MODEL_ARR:.2f} | fd_pre={FD_PRE} | pps={cap['pps']:.8f} | "
        f"note_a_shares={cap['note_a_shares']:.2f} | note_b_shares={cap['note_b_shares']:.2f} | "
        f"pool_refresh={cap['pool_refresh']:.2f}"
    )


if __name__ == "__main__":
    build()
