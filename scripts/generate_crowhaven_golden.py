#!/usr/bin/env python3
"""Generate golden claims reserve opinion workbook for Crowhaven Logistics.

Architecture (formula-driven analytical workbook):
  Assumptions      — typed memo parameters (LDFs, thresholds, named claims)
  Case Inventory   — typed TPA source rows; inclusion / cleaned case via formulas
  AY Development   — triangle diagonal typed; carve-out, ultimates, IBNR via formulas
                    fed by SUMIFS from Case Inventory and Assumptions
  Reserve Opinion  — summary metrics linked to AY Development / Assumptions
  UW Recommendation — Quote/Refer/Decline derived from LR vs memo thresholds
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from crowhaven_constants import (
    AY_AGE_MONTHS,
    BEGINNING_BOOKED_RESERVE,
    CLAIM_CLOSED_STALE,
    CLAIM_DUP,
    CLAIM_LARGE,
    CLAIM_LARGE_PAID,
    CLAIM_VOID,
    CUM_PAID,
    DECLINE_LR,
    DELIVERABLE,
    EARNED_PREMIUM,
    ENTITY,
    EVAL_DATE,
    LDF,
    POLICY,
    RENEWAL_DATE,
    REFER_LR,
    SLUG,
    STALE_LDF,
)
from sanitize_office import cache_xlsx_formula_values, sanitize_xlsx

ROOT = Path(__file__).resolve().parent.parent
TASK = ROOT / "tasks" / SLUG
INPUTS = TASK / "inputs"
GOLDEN = TASK / "golden"

header_font = Font(bold=True)
section_font = Font(bold=True, size=12)
money_fmt = '#,##0.00'
pct_fmt = '0.00%'
ldf_fmt = '0.00'
# Excel-custom date format (serial values + display). Avoid text dates — MAXIFS fails.
date_fmt = 'yyyy-mm-dd'


def money(x: float) -> float:
    return round(float(x), 2)


def as_excel_date(value: str | date | datetime) -> date:
    """Parse source ISO dates into true Excel date serials (not text)."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value).strip()[:10], "%Y-%m-%d").date()


def load_open_claims() -> list[dict]:
    path = INPUTS / "crowhaven-logistics_open_claims.csv"
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def simulate_clean(rows: list[dict]) -> tuple[list[dict], dict[int, float], dict[int, float], float]:
    """Python mirror of Case Inventory formulas — used for cache + regression."""
    working = []
    for r in rows:
        if str(r["status"]).upper() == "VOID" or r["claim_number"] == CLAIM_VOID:
            continue
        if r["claim_number"] == CLAIM_CLOSED_STALE:
            continue
        working.append(r)

    by_claim: dict[str, list[dict]] = defaultdict(list)
    for r in working:
        by_claim[r["claim_number"]].append(r)

    kept = []
    for claim, group in by_claim.items():
        group_sorted = sorted(group, key=lambda x: x["as_of_date"], reverse=True)
        kept.append(group_sorted[0])

    case_by_ay: dict[int, float] = defaultdict(float)
    case_attr_by_ay: dict[int, float] = defaultdict(float)
    large_case = 0.0
    for r in kept:
        ay = int(r["accident_year"])
        case = money(float(r["case_reserve"]))
        case_by_ay[ay] += case
        if r["claim_number"] == CLAIM_LARGE:
            large_case = case
        else:
            case_attr_by_ay[ay] += case
    return kept, case_by_ay, case_attr_by_ay, large_case


def main() -> None:
    raw = load_open_claims()
    kept, case_by_ay, case_attr_by_ay, large_case = simulate_clean(raw)

    ay_rows = []
    for ay in sorted(CUM_PAID):
        age = AY_AGE_MONTHS[ay]
        ldf = LDF[age]
        gross_paid = money(CUM_PAID[ay])
        ll_paid = money(CLAIM_LARGE_PAID) if ay == 2023 else 0.0
        attr_paid = money(gross_paid - ll_paid)
        attr_ult = money(attr_paid * ldf)
        attr_case = money(case_attr_by_ay[ay])
        pure_ibnr = money(max(0.0, attr_ult - attr_paid - attr_case))
        ll_ult = money(ll_paid + large_case) if ay == 2023 else 0.0
        total_ult = money(attr_ult + ll_ult)
        total_case = money(case_by_ay[ay])
        ay_rows.append(
            {
                "ay": ay,
                "age": age,
                "ldf": ldf,
                "gross_paid": gross_paid,
                "ll_paid": ll_paid,
                "attr_paid": attr_paid,
                "attr_ult": attr_ult,
                "attr_case": attr_case,
                "pure_ibnr": pure_ibnr,
                "ll_case": large_case if ay == 2023 else 0.0,
                "ll_ult": ll_ult,
                "total_ult": total_ult,
                "total_case": total_case,
            }
        )

    total_case = money(sum(case_by_ay.values()))
    total_ibnr = money(sum(r["pure_ibnr"] for r in ay_rows))
    total_ult = money(sum(r["total_ult"] for r in ay_rows))
    total_reserve = money(total_case + total_ibnr)
    indicated_lr = total_ult / EARNED_PREMIUM
    # Memo: Refer if LR exceeds 68.5%; Decline if LR exceeds 85.0%; else Quote.
    if indicated_lr > DECLINE_LR:
        recommendation = "Decline"
    elif indicated_lr > REFER_LR:
        recommendation = "Refer"
    else:
        recommendation = "Quote"

    wb = Workbook()

    # ------------------------------------------------------------------ Assumptions
    wa = wb.active
    wa.title = "Assumptions"
    wa["A1"] = f"{ENTITY} — YE {EVAL_DATE} factors"
    wa["A1"].font = section_font
    wa["A2"] = "actuarial_factor_memo.txt | fully insured primary"
    wa["A5"] = "Item"
    wa["B5"] = "Value"
    wa["C5"] = "Source"
    for c in wa[5]:
        c.font = header_font

    # Row map (stable refs for downstream formulas)
    # 6..9 LDFs, 10 large claim, 11 large paid, 12 closed, 13 void, 14 premium,
    # 15 refer, 16 decline, 17 prior, 18 eval, 19 renewal, 20 policy
    params = [
        (6, "Paid LDF 12", LDF[12], "actuarial_factor_memo.txt"),
        (7, "Paid LDF 24", LDF[24], "actuarial_factor_memo.txt"),
        (8, "Paid LDF 36", LDF[36], "actuarial_factor_memo.txt"),
        (9, "Paid LDF 48", LDF[48], "actuarial_factor_memo.txt"),
        (10, "Large Loss Claim", CLAIM_LARGE, "Large Loss Adjustment"),
        (11, "Large Loss Paid", CLAIM_LARGE_PAID, "Carve from AY 2023 paid"),
        (12, "Closed Claim Drop", CLAIM_CLOSED_STALE, "Final payment 2025-12-12"),
        (13, "VOID Claim Drop", CLAIM_VOID, "VOID status"),
        (14, "Earned Premium", EARNED_PREMIUM, "actuarial_factor_memo.txt"),
        (15, "Refer Threshold", REFER_LR, "actuarial_factor_memo.txt"),
        (16, "Decline Threshold", DECLINE_LR, "actuarial_factor_memo.txt"),
        (17, "Prior Booked Reserve", BEGINNING_BOOKED_RESERVE, "2024-12-31 context"),
        (18, "Evaluation Date", as_excel_date(EVAL_DATE), "Year-end"),
        (19, "Renewal Date", as_excel_date(RENEWAL_DATE), "Package renewal"),
        (20, "Policy", POLICY, "Subject policy"),
        (21, "Draft LDF 12 (unused)", STALE_LDF[12], "Definitions superseded"),
        (22, "Draft LDF 24 (unused)", STALE_LDF[24], "Definitions superseded"),
        (23, "Draft LDF 36 (unused)", STALE_LDF[36], "Definitions superseded"),
        (24, "Draft LDF 48 (unused)", STALE_LDF[48], "Definitions superseded"),
        (25, "Duplicate Review", CLAIM_DUP, "Keep latest as_of"),
    ]
    for row, name, val, note in params:
        wa.cell(row, 1, name)
        cell = wa.cell(row, 2, val)
        wa.cell(row, 3, note)
        if isinstance(val, date):
            cell.number_format = date_fmt
        elif isinstance(val, float):
            if row in (15, 16):
                cell.number_format = pct_fmt
            elif row in (6, 7, 8, 9, 21, 22, 23, 24):
                cell.number_format = ldf_fmt
            else:
                cell.number_format = money_fmt

    wa["A27"] = "Governing source"
    wa["A27"].font = header_font
    wa["A28"] = (
        f"Paid LDFs {LDF[12]}/{LDF[24]}/{LDF[36]}/{LDF[48]} — actuarial_factor_memo.txt; "
        f"Definitions draft {STALE_LDF[12]}/{STALE_LDF[24]}/{STALE_LDF[36]}/{STALE_LDF[48]} superseded."
    )
    wa.freeze_panes = "A6"
    wa.column_dimensions["A"].width = 28
    wa.column_dimensions["B"].width = 22
    wa.column_dimensions["C"].width = 28

    # ------------------------------------------------------------------ Case Inventory
    ws = wb.create_sheet("Case Inventory")
    ws["A1"] = f"{ENTITY} — open claims @ {EVAL_DATE}"
    ws["A1"].font = section_font
    ws["A2"] = "Source: crowhaven-logistics_open_claims.csv"

    headers = [
        "Claim Number",
        "AY",
        "Line",
        "Claimant",
        "Status",
        "Paid to Date",
        "Case Reserve",
        "As Of",
        "LL Flag",
        "TPA Note",
        "Include",
        "Cleaned Case",
        "Is LL",
        "Attritional Case",
        "LL Case",
        "Disposition",
    ]
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(4, col, h)
        cell.font = header_font

    # Stable sort for reproducible layout
    ordered = sorted(
        raw,
        key=lambda x: (int(x["accident_year"]), x["claim_number"], x["as_of_date"]),
    )
    start = 5
    for i, r in enumerate(ordered):
        row = start + i
        ws.cell(row, 1, r["claim_number"])
        ws.cell(row, 2, int(r["accident_year"]))
        ws.cell(row, 3, r["line_of_business"])
        ws.cell(row, 4, r["claimant_or_desc"])
        ws.cell(row, 5, r["status"])
        ws.cell(row, 6, money(float(r["paid_to_date"]))).number_format = money_fmt
        ws.cell(row, 7, money(float(r["case_reserve"]))).number_format = money_fmt
        # True Excel date serials — MAXIFS on text dates fails on fresh recalculation
        asof = ws.cell(row, 8, as_excel_date(r["as_of_date"]))
        asof.number_format = date_fmt
        ws.cell(row, 9, r["large_loss_flag"])
        ws.cell(row, 10, r["tpa_note"])

    end = start + len(ordered) - 1
    # Formula columns for each inventory row
    for row in range(start, end + 1):
        # include: not VOID, not named closed claim, and latest as_of for this claim_number
        ws.cell(
            row,
            11,
            (
                f'=IF(OR(UPPER(E{row})="VOID",A{row}=Assumptions!$B$13),FALSE,'
                f'IF(A{row}=Assumptions!$B$12,FALSE,'
                f'IF(H{row}<>MAXIFS($H${start}:$H${end},$A${start}:$A${end},A{row}),FALSE,TRUE)))'
            ),
        )
        ws.cell(row, 12, f"=IF(K{row},G{row},0)").number_format = money_fmt
        ws.cell(row, 13, f"=IF(A{row}=Assumptions!$B$10,TRUE,FALSE)")
        ws.cell(row, 14, f"=IF(AND(K{row},NOT(M{row})),G{row},0)").number_format = money_fmt
        ws.cell(row, 15, f"=IF(AND(K{row},M{row}),G{row},0)").number_format = money_fmt
        ws.cell(
            row,
            16,
            (
                f'=IF(OR(UPPER(E{row})="VOID",A{row}=Assumptions!$B$13),"Drop-VOID",'
                f'IF(A{row}=Assumptions!$B$12,"Drop-closed",'
                f'IF(H{row}<>MAXIFS($H${start}:$H${end},$A${start}:$A${end},A{row}),'
                f'"Drop-dup",'
                f'IF(M{row},"Keep-LL","Keep"))))'
            ),
        )

    tot = end + 1
    ws.cell(tot, 4, "TOTALS").font = header_font
    ws.cell(tot, 12, f"=SUM(L{start}:L{end})").number_format = money_fmt
    ws.cell(tot, 14, f"=SUM(N{start}:N{end})").number_format = money_fmt
    ws.cell(tot, 15, f"=SUM(O{start}:O{end})").number_format = money_fmt
    inv_total_row = tot

    # Workpaper table presentation (header freeze + filter on data rows only)
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:P{end}"
    inv_widths = {
        "A": 20, "B": 8, "C": 16, "D": 18, "E": 10, "F": 12, "G": 12, "H": 12,
        "I": 10, "J": 36, "K": 10, "L": 12, "M": 8, "N": 14, "O": 12, "P": 12,
    }
    for col_letter, width in inv_widths.items():
        ws.column_dimensions[col_letter].width = width

    # ------------------------------------------------------------------ AY Development
    ws2 = wb.create_sheet("AY Development")
    ws2["A1"] = "AY Development"
    ws2["A1"].font = section_font
    ws2["A2"] = (
        "Paid LDFs per actuarial memo; draft factors on Definitions tab are superseded."
    )

    h2 = [
        "AY",
        "Age (mo)",
        "Paid LDF",
        "Gross Paid",
        "LL Paid Carve",
        "Attritional Paid",
        "Attritional Ult",
        "Attritional Case",
        "Pure IBNR",
        "LL Case",
        "LL Ultimate",
        "Indicated Ultimate",
        "Cleaned Case",
    ]
    for col, h in enumerate(h2, start=1):
        cell = ws2.cell(4, col, h)
        cell.font = header_font

    r0 = 5
    for i, a in enumerate(ay_rows):
        row = r0 + i
        ws2.cell(row, 1, a["ay"])
        ws2.cell(row, 2, a["age"])
        # LDF from Assumptions by maturity
        ws2.cell(
            row,
            3,
            (
                f"=IF(B{row}=12,Assumptions!$B$6,"
                f"IF(B{row}=24,Assumptions!$B$7,"
                f"IF(B{row}=36,Assumptions!$B$8,Assumptions!$B$9)))"
            ),
        )
        ws2.cell(row, 3).number_format = ldf_fmt
        ws2.cell(row, 4, a["gross_paid"]).number_format = money_fmt
        # Carve large-loss paid only for the AY that contains the named claim
        ws2.cell(
            row,
            5,
            f'=IF(COUNTIFS(\'Case Inventory\'!$A${start}:$A${end},Assumptions!$B$10,'
            f'\'Case Inventory\'!$B${start}:$B${end},A{row})>0,Assumptions!$B$11,0)',
        )
        ws2.cell(row, 5).number_format = money_fmt
        ws2.cell(row, 6, f"=D{row}-E{row}").number_format = money_fmt
        ws2.cell(row, 7, f"=ROUND(F{row}*C{row},2)").number_format = money_fmt
        ws2.cell(
            row,
            8,
            f"=SUMIFS('Case Inventory'!$N${start}:$N${end},"
            f"'Case Inventory'!$B${start}:$B${end},A{row})",
        )
        ws2.cell(row, 8).number_format = money_fmt
        ws2.cell(row, 9, f"=MAX(0,ROUND(G{row}-F{row}-H{row},2))").number_format = money_fmt
        ws2.cell(
            row,
            10,
            f"=SUMIFS('Case Inventory'!$O${start}:$O${end},"
            f"'Case Inventory'!$B${start}:$B${end},A{row})",
        )
        ws2.cell(row, 10).number_format = money_fmt
        ws2.cell(row, 11, f"=ROUND(E{row}+J{row},2)").number_format = money_fmt
        ws2.cell(row, 12, f"=ROUND(G{row}+K{row},2)").number_format = money_fmt
        ws2.cell(
            row,
            13,
            f"=SUMIFS('Case Inventory'!$L${start}:$L${end},"
            f"'Case Inventory'!$B${start}:$B${end},A{row})",
        )
        ws2.cell(row, 13).number_format = money_fmt

    last = r0 + len(ay_rows) - 1
    tot_ay = last + 1
    ws2.cell(tot_ay, 1, "TOTAL").font = header_font
    for letter in "DEFGHIJKLM":
        col = ord(letter) - ord("A") + 1
        ws2.cell(tot_ay, col, f"=SUM({letter}{r0}:{letter}{last})")
        ws2.cell(tot_ay, col).number_format = money_fmt

    ws2.cell(tot_ay + 2, 1, "Note").font = header_font
    ws2.cell(
        tot_ay + 3,
        1,
        f"Large Loss Adjustment — {CLAIM_LARGE}: carve paid pre-LDF; LL ult = paid+case.",
    )
    ws2.freeze_panes = "A5"
    for col in range(1, 14):
        ws2.column_dimensions[get_column_letter(col)].width = 14
    ws2.column_dimensions["A"].width = 10

    # ------------------------------------------------------------------ Reserve Opinion
    ws3 = wb.create_sheet("Reserve Opinion")
    ws3["A1"] = f"{ENTITY} — Reserve Opinion"
    ws3["A1"].font = section_font
    ws3["A2"] = f"{POLICY} | YE {EVAL_DATE} | Renewal {RENEWAL_DATE}"
    ws3["A4"] = "Item"
    ws3["B4"] = "Amount"
    for c in ("A4", "B4"):
        ws3[c].font = header_font

    # Primary metrics — all formula-linked (no pasted analytical totals)
    metrics = [
        (5, "Cleaned Case", f"='AY Development'!M{tot_ay}"),
        (6, "Pure IBNR", f"='AY Development'!I{tot_ay}"),
        (7, "Total Reserve", "=ROUND(B5+B6,2)"),
        (8, "Indicated Ultimate", f"='AY Development'!L{tot_ay}"),
        (9, "Earned Premium", "=Assumptions!B14"),
        (10, "Ultimate LR", "=B8/B9"),
        (11, "Refer Threshold", "=Assumptions!B15"),
        (12, "Decline Threshold", "=Assumptions!B16"),
        (13, "Prior Booked Reserve", "=Assumptions!B17"),
    ]
    for row, lab, formula in metrics:
        ws3.cell(row, 1, lab)
        ws3.cell(row, 2, formula)
        if row in (10, 11, 12):
            ws3.cell(row, 2).number_format = pct_fmt
        else:
            ws3.cell(row, 2).number_format = money_fmt

    ws3["A15"] = "Large Loss Adjustment"
    ws3["A15"].font = header_font
    ws3["A16"] = "LL Paid Carve"
    ws3["B16"] = f"='AY Development'!E{tot_ay}"
    ws3["B16"].number_format = money_fmt
    ws3["A17"] = "LL Case"
    ws3["B17"] = f"='AY Development'!J{tot_ay}"
    ws3["B17"].number_format = money_fmt
    ws3["A18"] = "LL Ultimate"
    ws3["B18"] = f"='AY Development'!K{tot_ay}"
    ws3["B18"].number_format = money_fmt

    ws3["A20"] = "Tie-out"
    ws3["A20"].font = header_font
    ws3["A21"] = "Cleaned Case (Inventory)"
    ws3["B21"] = f"='Case Inventory'!L{inv_total_row}"
    ws3["B21"].number_format = money_fmt
    ws3["A22"] = "Case Diff (AY − Inventory)"
    ws3["B22"] = "=ROUND(B5-B21,2)"
    ws3["B22"].number_format = money_fmt

    ws3["A24"] = "Note"
    ws3["A24"].font = header_font
    ws3["B24"] = (
        "Paid LDFs per actuarial memo; draft factors on Definitions tab are superseded."
    )
    ws3.freeze_panes = "A5"
    ws3.column_dimensions["A"].width = 28
    ws3.column_dimensions["B"].width = 16

    # ------------------------------------------------------------------ UW Recommendation
    # Visible Refer verdict + LR/thresholds + short rationale (plain text, not hidden).
    ws4 = wb.create_sheet("UW Recommendation")
    ws4["A1"] = f"UW Recommendation — {ENTITY}"
    ws4["A1"].font = section_font
    ws4["A2"] = f"{POLICY} | YE {EVAL_DATE} | Renewal {RENEWAL_DATE}"

    lr_pct_display = f"{indicated_lr * 100:.2f}%"
    refer_pct = f"{REFER_LR * 100:.1f}%"
    decline_pct = f"{DECLINE_LR * 100:.1f}%"

    ws4["A4"] = "Item"
    ws4["B4"] = "Value"
    for c in ("A4", "B4"):
        ws4[c].font = header_font

    # B5 must be a literal string (not formula-only / cache-only) for graders.
    ws4["A5"] = "Final Recommendation"
    ws4["B5"] = recommendation
    ws4["B5"].font = Font(bold=True, size=14)

    ws4["A6"] = "Ultimate LR"
    ws4["B6"] = "='Reserve Opinion'!B10"
    ws4["B6"].number_format = pct_fmt

    ws4["A7"] = "Refer Threshold"
    ws4["B7"] = "=Assumptions!B15"
    ws4["B7"].number_format = pct_fmt

    ws4["A8"] = "Decline Threshold"
    ws4["B8"] = "=Assumptions!B16"
    ws4["B8"].number_format = pct_fmt

    # Formula tie-out (must match literal B5).
    rec_formula = (
        '=IF(\'Reserve Opinion\'!B10>Assumptions!B16,"Decline",'
        'IF(\'Reserve Opinion\'!B10>Assumptions!B15,"Refer","Quote"))'
    )
    ws4["A9"] = "Decision Tie-out"
    ws4["B9"] = rec_formula

    rationale_text = (
        f"{lr_pct_display} > {refer_pct} refer threshold and < {decline_pct} decline threshold."
    )
    ws4["A11"] = "Rationale"
    ws4["A11"].font = header_font
    ws4["B11"] = rationale_text

    ws4["A13"] = "Reserve Summary"
    ws4["A13"].font = header_font
    uw_metrics = [
        (14, "Cleaned Case", "='Reserve Opinion'!B5", money_fmt),
        (15, "Pure IBNR", "='Reserve Opinion'!B6", money_fmt),
        (16, "Total Reserve", "='Reserve Opinion'!B7", money_fmt),
        (17, "Indicated Ultimate", "='Reserve Opinion'!B8", money_fmt),
        (18, "Earned Premium", "='Reserve Opinion'!B9", money_fmt),
    ]
    for row, lab, formula, fmt in uw_metrics:
        ws4.cell(row, 1, lab)
        ws4.cell(row, 2, formula)
        ws4.cell(row, 2).number_format = fmt

    ws4.freeze_panes = "A5"
    ws4.column_dimensions["A"].width = 22
    ws4.column_dimensions["B"].width = 56

    GOLDEN.mkdir(parents=True, exist_ok=True)
    out = GOLDEN / DELIVERABLE
    wb.save(out)

    # Cached numeric formula results for platform digests (no bool/text — those stay formula-only)
    inv_cache: dict[str, float] = {}
    latest_asof: dict[str, str] = {}
    for r in raw:
        cn = r["claim_number"]
        latest_asof[cn] = max(latest_asof.get(cn, ""), r["as_of_date"])

    for i, r in enumerate(ordered):
        row = start + i
        is_void = str(r["status"]).upper() == "VOID" or r["claim_number"] == CLAIM_VOID
        is_closed = r["claim_number"] == CLAIM_CLOSED_STALE
        is_dup = r["as_of_date"] != latest_asof[r["claim_number"]]
        include = not (is_void or is_closed or is_dup)
        is_ll = r["claim_number"] == CLAIM_LARGE
        case = money(float(r["case_reserve"]))
        # Cache include flags as 1/0 so digests / recalc tooling see a value
        inv_cache[f"K{row}"] = 1 if include else 0
        inv_cache[f"L{row}"] = case if include else 0.0
        inv_cache[f"N{row}"] = case if (include and not is_ll) else 0.0
        inv_cache[f"O{row}"] = case if (include and is_ll) else 0.0
        inv_cache[f"M{row}"] = 1 if is_ll else 0

    inv_cache[f"L{inv_total_row}"] = total_case
    inv_cache[f"N{inv_total_row}"] = money(sum(case_attr_by_ay.values()))
    inv_cache[f"O{inv_total_row}"] = money(large_case)

    ay_cache: dict[str, float] = {}
    for i, a in enumerate(ay_rows):
        row = r0 + i
        ay_cache[f"C{row}"] = a["ldf"]
        ay_cache[f"E{row}"] = a["ll_paid"]
        ay_cache[f"F{row}"] = a["attr_paid"]
        ay_cache[f"G{row}"] = a["attr_ult"]
        ay_cache[f"H{row}"] = a["attr_case"]
        ay_cache[f"I{row}"] = a["pure_ibnr"]
        ay_cache[f"J{row}"] = a["ll_case"]
        ay_cache[f"K{row}"] = a["ll_ult"]
        ay_cache[f"L{row}"] = a["total_ult"]
        ay_cache[f"M{row}"] = a["total_case"]
    ay_cache.update(
        {
            f"D{tot_ay}": money(sum(a["gross_paid"] for a in ay_rows)),
            f"E{tot_ay}": money(sum(a["ll_paid"] for a in ay_rows)),
            f"F{tot_ay}": money(sum(a["attr_paid"] for a in ay_rows)),
            f"G{tot_ay}": money(sum(a["attr_ult"] for a in ay_rows)),
            f"H{tot_ay}": money(sum(a["attr_case"] for a in ay_rows)),
            f"I{tot_ay}": total_ibnr,
            f"J{tot_ay}": money(sum(a["ll_case"] for a in ay_rows)),
            f"K{tot_ay}": money(sum(a["ll_ult"] for a in ay_rows)),
            f"L{tot_ay}": total_ult,
            f"M{tot_ay}": total_case,
        }
    )

    # Round LR cache to 6dp so digests never show IEEE tails
    lr_cached = round(indicated_lr, 6)

    formula_cache: dict[str, dict[str, float | str]] = {
        "Case Inventory": inv_cache,
        "AY Development": ay_cache,
        "Reserve Opinion": {
            "B5": total_case,
            "B6": total_ibnr,
            "B7": total_reserve,
            "B8": total_ult,
            "B9": money(EARNED_PREMIUM),
            "B10": lr_cached,
            "B11": REFER_LR,
            "B12": DECLINE_LR,
            "B13": money(BEGINNING_BOOKED_RESERVE),
            "B16": money(CLAIM_LARGE_PAID),
            "B17": money(large_case),
            "B18": money(CLAIM_LARGE_PAID + large_case),
            "B21": total_case,
            "B22": 0.0,
        },
        "UW Recommendation": {
            # B5 is literal text (not formula); do not overwrite with cache.
            "B6": lr_cached,
            "B7": REFER_LR,
            "B8": DECLINE_LR,
            "B9": recommendation,
            "B14": total_case,
            "B15": total_ibnr,
            "B16": total_reserve,
            "B17": total_ult,
            "B18": money(EARNED_PREMIUM),
        },
    }
    cache_xlsx_formula_values(out, formula_cache)
    sanitize_xlsx(out)

    print(f"Wrote {out}")
    print(f"cleaned_case={total_case:.2f} pure_ibnr={total_ibnr:.2f} total_reserve={total_reserve:.2f}")
    print(f"ultimate={total_ult:.2f} LR={indicated_lr:.4%} → {recommendation}")
    for a in ay_rows:
        print(
            f"  AY{a['ay']}: attr_ult={a['attr_ult']:.2f} ibnr={a['pure_ibnr']:.2f} "
            f"case={a['total_case']:.2f} ll_ult={a['ll_ult']:.2f}"
        )


if __name__ == "__main__":
    main()
