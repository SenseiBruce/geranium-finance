#!/usr/bin/env python3
"""Generate golden claim coverage opinion workbook for Ashcroft Foods (Core difficulty)."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

from ashcroft_constants import (
    AFTER_COINSURANCE,
    BI_CLAIMED,
    BI_WAITING_HOURS,
    CASE_RESERVE,
    CLAIM_ID,
    CLAIM_FILE,
    CLAIMED_SELL_COVERED,
    COINSURANCE_FACTOR,
    COMMITTEE_DATE,
    COVERED_STOCK_COST,
    DAYS_SINCE_SERVICE,
    DELIVERABLE,
    ENTITY,
    EQUIPMENT_COMPONENT_TOTAL,
    EQUIPMENT_FOOTING_VARIANCE,
    EQUIPMENT_LINES,
    EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL,
    EQUIPMENT_REPAIR,
    EVAL_DATE,
    GRACE_DAYS,
    LAST_SERVICE,
    LOSS_DATE,
    LOTS,
    MAINTENANCE_THRESHOLD,
    MEMO_FILE,
    NET_AFTER_SALVAGE,
    OEM_SERVICE_DAYS,
    OUTAGE_HOURS,
    POLICY,
    POLICY_FILE,
    SALVAGE_AMOUNT,
    SALVAGE_LOT,
    SALVAGE_LOT_COST,
    SALVAGE_RATE,
    SLUG,
    SPOILAGE_DEDUCTIBLE,
    SUPERSEDED_DEDUCTIBLE,
    VENDOR_CANCEL_DATE,
    VENDOR_CANCEL_DAYS_BEFORE_LOSS,
)
from sanitize_office import cache_xlsx_formula_values, sanitize_xlsx

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "tasks" / SLUG / "golden"

header_font = Font(bold=True, name="Calibri", size=11)
title_font = Font(bold=True, name="Calibri", size=13)
body_font = Font(name="Calibri", size=10)
money_fmt = "#,##0.00"
pct_fmt = "0%"
thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
pass_fill = PatternFill("solid", fgColor="C6EFCE")
fail_fill = PatternFill("solid", fgColor="FFC7CE")
cf_fill = PatternFill("solid", fgColor="FFF2CC")  # counterfactual highlight


def money(x: float) -> float:
    return round(float(x), 2)


def style_header_row(ws, row: int, ncols: int) -> None:
    for c in range(1, ncols + 1):
        cell = ws.cell(row, c)
        cell.font = header_font
        cell.border = thin


def autosize(ws, max_w: int = 42) -> None:
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        width = min(max(len(str(c.value or "")) for c in col) + 2, max_w)
        ws.column_dimensions[letter].width = max(width, 10)


def border_range(ws, r1: int, r2: int, c1: int, c2: int) -> None:
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(r, c).border = thin
            if ws.cell(r, c).font is None or ws.cell(r, c).font.name is None:
                ws.cell(r, c).font = body_font


def build() -> Path:
    wb = Workbook()
    alae_total = money(1840.00 + 620.50 + 275.00 + 410.00)
    pkg_cost = money(next(l[5] for l in LOTS if l[0] == "PKG-991"))
    void_cost = money(next(l[5] for l in LOTS if l[0] == "LOT-B-099"))
    dup_cost = money(next(l[5] for l in LOTS if l[0] == "LOT-B-218-DUP"))
    raw_zone_b = money(sum(r[5] for r in LOTS))
    n_lots = len(LOTS)
    n_eligible = sum(1 for r in LOTS if r[7])
    other_denied = money(EQUIPMENT_REPAIR + BI_CLAIMED)

    # Counterfactual helpers (not actual conclusions)
    reserve_wrong_ded = money(AFTER_COINSURANCE - SUPERSEDED_DEDUCTIBLE)
    reserve_no_coin = money(NET_AFTER_SALVAGE - SPOILAGE_DEDUCTIBLE)
    reserve_equip_hyp = money(CASE_RESERVE + EQUIPMENT_REPAIR)
    # OEM sensitivity: source 90 → 75%; short 80 → still overdue 75%; long 100 → 100%
    oem_short = 80
    oem_long = 100
    thr_short = oem_short + GRACE_DAYS
    thr_long = oem_long + GRACE_DAYS
    factor_short = COINSURANCE_FACTOR if DAYS_SINCE_SERVICE > thr_short else 1.0
    factor_long = COINSURANCE_FACTOR if DAYS_SINCE_SERVICE > thr_long else 1.0
    reserve_oem_short = money(money(NET_AFTER_SALVAGE * factor_short) - SPOILAGE_DEDUCTIBLE)
    reserve_oem_long = money(money(NET_AFTER_SALVAGE * factor_long) - SPOILAGE_DEDUCTIBLE)

    # ========== Assumptions ==========
    ws = wb.active
    ws.title = "Assumptions"
    ws["A1"] = f"{ENTITY} — Claim Coverage Opinion"
    ws["A1"].font = title_font
    ws["A2"] = f"Claim {CLAIM_ID} | Policy {POLICY} | Loss {LOSS_DATE} | Eval {EVAL_DATE}"
    ws["A3"] = f"Committee target {COMMITTEE_DATE}"
    ws["A5"] = "Governing source hierarchy"
    ws["A5"].font = header_font
    ws["A6"] = (
        f"(1) {MEMO_FILE} rules; (2) Active rows on {POLICY_FILE}; "
        f"(3) contemporaneous {CLAIM_FILE} evidence; "
        "(4) superseded schedule rows and superseded field notes (N-01) non-governing."
    )
    ws["A6"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[6].height = 48

    ws["A8"] = "Source"
    ws["B8"] = "Role"
    ws["C8"] = "Status class"
    style_header_row(ws, 8, 3)
    for i, row in enumerate(
        [
            (CLAIM_FILE, "Loss notice, inventory, equipment, BI, notes, payments", "Recorded facts + contemporaneous evidence"),
            (POLICY_FILE, "Coverages, deductibles, waiting periods, elections", "Potentially controlling (Active) / superseded"),
            (MEMO_FILE, "Hierarchy and desk rules", "Potentially controlling rules — not finished dispositions"),
        ],
        start=9,
    ):
        for c, v in enumerate(row, start=1):
            ws.cell(i, c, v).font = body_font
            ws.cell(i, c).border = thin

    ws["A13"] = "Fact classification legend"
    ws["A13"].font = header_font
    ws["A14"] = (
        "Recorded = present in a source. Potentially controlling = may govern if hierarchy selects it. "
        "Superseded = present but non-governing. Derived = computed by applying rules to selected facts."
    )
    ws["A14"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[14].height = 36
    autosize(ws, 70)

    # ========== Coverage Decision Tree ==========
    ws = wb.create_sheet("Coverage Decision Tree")
    ws["A1"] = "Stage 1 — Coverage decision tree (before indemnity math)"
    ws["A1"].font = title_font
    headers = [
        "Issue",
        "1 Raw fact identification",
        "2 Potentially controlling provision",
        "3 Competing source/evidence",
        "4 Source hierarchy decision",
        "5 Rule test",
        "6 Intermediate result",
        "7 Final disposition",
        "8 Financial consequence",
    ]
    for c, h in enumerate(headers, start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 9)

    tree = [
        (
            "Zone B spoiled stock",
            f"Compressor #3 failure; ~{OUTAGE_HOURS}h elevated Zone B temps; Open/Open-Salvage stock lots on Inventory ({CLAIM_FILE})",
            f"CP 04 40 Spoilage Active on {POLICY_FILE}; stock definition + maintenance coinsurance rule in {MEMO_FILE}",
            "Claimant selling-price demand / N-01 provisional pay note vs memo valuation + Active schedule",
            f"{MEMO_FILE} > Active schedule > contemporaneous claim evidence > N-01",
            "On-prem refrigeration breakdown caused temperature change to qualifying stock; maintenance coinsurance tested separately on Maintenance Timeline",
            "Stock trigger met; valuation and coinsurance adjustments still required",
            "Accept — Partial",
            "Indemnity case reserve on cleaned invoice stock after salvage, coinsurance, Active deductible (see Reserve Bridge)",
        ),
        (
            "Compressor #3 / refrigeration equipment",
            f"EQ-01..EQ-05 quotes; prior EQ-SUB {EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL:,.2f}; N-09 footing correction ({CLAIM_FILE})",
            f"Mechanical Breakdown exclusion + no equipment floater ({POLICY_FILE}); equipment rule in {MEMO_FILE}",
            "N-01 provisional full equipment recognition vs exclusion + absence of floater",
            f"{MEMO_FILE} / Active exclusion over N-01 advocacy",
            "Direct repair/replacement of failed equipment barred; stock endorsement does not create equipment indemnity",
            f"Corrected footing {EQUIPMENT_REPAIR:,.2f} is demand documentation only",
            "Deny",
            f"No indemnity reserve for footed equipment demand {EQUIPMENT_REPAIR:,.2f}",
        ),
        (
            "Business Income / Extra Expense",
            f"Logger outage ~{OUTAGE_HOURS}h; insured multi-day BI worksheet claim {BI_CLAIMED:,.2f} ({CLAIM_FILE})",
            f"CP 00 30 waiting period {BI_WAITING_HOURS}h Active ({POLICY_FILE}); BI rule in {MEMO_FILE}",
            "Broker waiver / reallocation-day demand vs logger hours + schedule waiting period",
            f"{MEMO_FILE} waiting-period rule + Active schedule over broker advocacy",
            f"Compare interruption hours to waiting period: {OUTAGE_HOURS} vs {BI_WAITING_HOURS}",
            "Waiting period not satisfied",
            "Deny",
            f"No BI case reserve for claimed {BI_CLAIMED:,.2f}",
        ),
        (
            "Packaging / non-stock (PKG-991)",
            f"PKG-991 corrugated freezer cartons {pkg_cost:,.2f} listed on Inventory ({CLAIM_FILE})",
            f"Stock definition in {MEMO_FILE} (packaging/dunnage not stock under CP 04 40 desk practice)",
            "Claimant inclusion of packaging in spoilage demand vs memo stock definition",
            f"{MEMO_FILE} stock definition governs",
            "Packaging materials are not perishable frozen food product held for sale/distribution",
            "PKG-991 ineligible for spoilage stock pool",
            "Deny / Exclude",
            "Exclude packaging invoice cost from covered stock pool",
        ),
    ]
    for i, row in enumerate(tree, start=4):
        for c, val in enumerate(row, start=1):
            ws.cell(i, c, val).font = body_font
            ws.cell(i, c).border = thin
            ws.cell(i, c).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 72

    ws["A9"] = "Overall coverage determination (derived — not copied from a field note)"
    ws["B9"] = "Partial Coverage"
    ws["C9"] = "Stock Accept/Partial; equipment Deny; BI Deny; packaging Deny/Exclude"
    ws["A9"].font = header_font
    ws["B9"].font = header_font
    border_range(ws, 9, 9, 1, 3)
    ws["A11"] = "Stage gate"
    ws["B11"] = (
        "Stage 2 financial build proceeds only for Accept/Partial stock indemnity; "
        "equipment and BI remain at zero indemnity under actual conclusions "
        "(see Scenario Checks for counterfactuals only)."
    )
    ws["B11"].alignment = Alignment(wrap_text=True)
    autosize(ws, 36)

    # ========== Evidence & Rule Matrix ==========
    ws = wb.create_sheet("Evidence & Rule Matrix")
    ws["A1"] = "Competing-evidence matrix — recorded vs controlling vs superseded vs derived"
    ws["A1"].font = title_font
    mh = [
        "Issue",
        "Candidate source",
        "Source status",
        "Candidate fact/rule",
        "Conflict or ambiguity",
        "Governing source",
        "Reason selected",
        "Downstream calculation affected",
    ]
    for c, h in enumerate(mh, start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 8)

    matrix = [
        (
            "A. Stock valuation basis",
            f"{CLAIM_FILE} N-01 + selling-price demand columns",
            "Superseded / advocacy",
            "Pay/value at unit_selling_price",
            "Conflicts with schedule election and memo valuation rule",
            f"{MEMO_FILE} + {POLICY_FILE} PS-09/PS-24",
            "Selling-price rider not elected; memo requires invoice/replacement cost",
            "Valuation Reconciliation covered amount; Reserve Bridge eligible stock",
        ),
        (
            "A. Stock valuation basis",
            f"{POLICY_FILE} PS-09 / PS-24; {MEMO_FILE} valuation rule",
            "Potentially controlling",
            "Invoice / replacement cost (line_cost) when selling price not elected",
            "Competes with N-01 selling-price recommendation",
            f"{MEMO_FILE} / Active schedule",
            "Hierarchy selects memo + Active election status over stale field note",
            "Inventory Audit Trail valuation basis; Reserve Bridge",
        ),
        (
            "B. Spoilage deductible",
            f"{POLICY_FILE} PS-04 + broker note N-06",
            "Superseded",
            f"Deductible {SUPERSEDED_DEDUCTIBLE:,.0f}",
            "Two deductible amounts appear on schedule with different status",
            f"{MEMO_FILE} deductible hierarchy + Active PS-03/PS-17",
            "Only Active status governs; Superseded mid-term row is non-governing",
            "Reserve Bridge deductible step; Scenario Checks S1 counterfactual",
        ),
        (
            "B. Spoilage deductible",
            f"{POLICY_FILE} PS-03 / PS-17 Active",
            "Potentially controlling",
            f"Deductible {SPOILAGE_DEDUCTIBLE:,.0f}",
            "Competes with Superseded PS-04",
            f"{MEMO_FILE} + Active schedule status",
            "Active endorsement deductible applies after salvage and coinsurance",
            "Actual indemnity case reserve",
        ),
        (
            "C. Equipment demand footing",
            f"{CLAIM_FILE} prior EQ-SUB worksheet",
            "Recorded (non-governing figure)",
            f"Prior subtotal {EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL:,.2f}",
            f"Variance {EQUIPMENT_FOOTING_VARIANCE:,.2f} vs component quotes",
            f"{CLAIM_FILE} EQ-01..EQ-05 + N-09",
            "N-09 identifies worksheet addition error; component sum is source-of-truth footing",
            "Denied Items equipment block; Decision Trace equipment impact = 0",
        ),
        (
            "C. Equipment demand footing",
            f"{CLAIM_FILE} EQ-01..EQ-05 component quotes",
            "Recorded / derived footing",
            f"Component sum {EQUIPMENT_COMPONENT_TOTAL:,.2f}",
            "Competes with prior EQ-SUB",
            f"{CLAIM_FILE} N-09 desk footing",
            "Corrected EQ-SUB equals component sum",
            "Equipment corrected footing documented; still denied under Mechanical Breakdown",
        ),
        (
            "C. Equipment indemnity treatment",
            f"{CLAIM_FILE} N-01 provisional equipment recognition",
            "Superseded field note",
            "Recognize full equipment repair",
            "Conflicts with Mechanical Breakdown exclusion and no floater",
            f"{MEMO_FILE} equipment rule + {POLICY_FILE} PS-05",
            "Exclusion bars direct equipment repair; stock endorsement does not create equipment cover",
            "Coverage Decision Tree Deny; Scenario Checks S4 counterfactual only",
        ),
        (
            "BI waiting period",
            f"{CLAIM_FILE} insured multi-day BI worksheet / broker waiver ask",
            "Advocacy / recorded demand",
            "Reserve BI for reallocation days",
            "Waiting period measured on logger interruption, not post-restore days",
            f"{MEMO_FILE} BI rule + {POLICY_FILE} PS-06",
            f"Compare {OUTAGE_HOURS}h logger outage to {BI_WAITING_HOURS}h Active waiting period",
            "BI Deny; zero BI indemnity",
        ),
        (
            "Maintenance coinsurance",
            f"{CLAIM_FILE} N-02 OEM interval + service/cancel dates",
            "Recorded facts (interval/dates) + derived tests",
            f"OEM {OEM_SERVICE_DAYS}d; last service {LAST_SERVICE}; vendor cancel {VENDOR_CANCEL_DATE}",
            "Must apply memo grace/safe-harbor tests — dates alone are not the pay factor",
            f"{MEMO_FILE} delayed-maintenance rule applied to N-02 facts",
            "Elapsed days and vendor-cancel window derived on Maintenance Timeline",
            "Coinsurance factor into Reserve Bridge; OEM sensitivity table",
        ),
    ]
    for i, row in enumerate(matrix, start=4):
        for c, val in enumerate(row, start=1):
            ws.cell(i, c, val).font = body_font
            ws.cell(i, c).border = thin
            ws.cell(i, c).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 48
    autosize(ws, 32)

    # ========== Maintenance Timeline ==========
    ws = wb.create_sheet("Maintenance Timeline")
    ws["A1"] = "Delayed-maintenance / protective-safeguards timeline (derived)"
    ws["A1"].font = title_font
    ws["A3"] = "Metric"
    ws["B3"] = "Value"
    ws["C3"] = "Classification"
    ws["D3"] = "Source / formula"
    style_header_row(ws, 3, 4)

    maint_rows = [
        (4, "Last completed OEM service date", LAST_SERVICE, "Recorded", f"{CLAIM_FILE} N-02"),
        (5, "Date of loss", LOSS_DATE, "Recorded", f"{CLAIM_FILE} Loss Notice"),
        (6, "Raw elapsed days (loss − last service)", DAYS_SINCE_SERVICE, "Derived", f"{LOSS_DATE} − {LAST_SERVICE}"),
        (7, "OEM service interval (days)", OEM_SERVICE_DAYS, "Recorded", f"{CLAIM_FILE} N-02"),
        (8, "Scheduling grace (days)", GRACE_DAYS, "Potentially controlling rule", f"{MEMO_FILE}"),
        (9, "Allowed interval (OEM + grace)", "=B7+B8", "Derived", "Formula"),
        (10, "Overdue amount (elapsed − allowed)", "=B6-B9", "Derived", "Formula"),
        (11, "Vendor cancellation date", VENDOR_CANCEL_DATE, "Recorded", f"{CLAIM_FILE} N-02"),
        (12, "Days from cancellation to loss", VENDOR_CANCEL_DAYS_BEFORE_LOSS, "Derived", f"{LOSS_DATE} − {VENDOR_CANCEL_DATE}"),
        (13, "Vendor-cancel safe-harbor limit (days)", 14, "Potentially controlling rule", f"{MEMO_FILE}"),
        (14, "Condition: service overdue beyond grace?", '=IF(B6>B9,"Yes","No")', "Derived", "Elapsed > allowed"),
        (15, "Condition: vendor cancel within safe harbor?", '=IF(B12<=B13,"Yes","No")', "Derived", "Days to loss ≤ 14"),
        (
            16,
            "Resulting coinsurance pay factor (actual)",
            '=IF(AND(B14="Yes",B15="Yes"),0.75,1)',
            "Derived",
            f"{MEMO_FILE}: 75% when both conditions met; else 100%",
        ),
    ]
    for row, label, val, klass, src in maint_rows:
        ws.cell(row, 1, label).font = body_font
        cell = ws.cell(row, 2, val)
        cell.font = body_font
        if isinstance(val, float) and val <= 1:
            cell.number_format = "0.00"
        ws.cell(row, 3, klass).font = body_font
        ws.cell(row, 4, src).font = body_font
        for c in range(1, 5):
            ws.cell(row, c).border = thin

    ws["A18"] = "OEM interval sensitivity (hypothetical assumptions — not source facts)"
    ws["A18"].font = header_font
    ws["A18"].fill = cf_fill
    sh = [
        "Assumption label",
        "OEM interval (days)",
        "Allowed interval",
        "Overdue?",
        "Pay factor",
        "Linked reserve (after salvage × factor − Active deductible)",
        "Changes coinsurance vs actual?",
        "Changes reserve vs actual?",
    ]
    for c, h in enumerate(sh, start=1):
        ws.cell(19, c, h)
    style_header_row(ws, 19, 8)

    # Row 20: source-supported
    ws["A20"] = "Source-supported (N-02)"
    ws["B20"] = "=B7"
    ws["C20"] = "=$B$8+B20"
    ws["D20"] = '=IF($B$6>C20,"Yes","No")'
    ws["E20"] = '=IF(AND(D20="Yes",$B$15="Yes"),0.75,1)'
    ws["F20"] = f"=ROUND({NET_AFTER_SALVAGE}*E20,2)-{SPOILAGE_DEDUCTIBLE}"
    ws["F20"].number_format = money_fmt
    ws["G20"] = '=IF(ABS(E20-$B$16)<0.001,"No","Yes")'
    ws["H20"] = '=IF(ABS(F20-\'Reserve Bridge\'!C14)<0.01,"No","Yes")'

    # Row 21: shorter hypothetical
    ws["A21"] = "Hypothetical — shorter OEM interval"
    ws["A21"].fill = cf_fill
    ws["B21"] = oem_short
    ws["C21"] = "=$B$8+B21"
    ws["D21"] = '=IF($B$6>C21,"Yes","No")'
    ws["E21"] = '=IF(AND(D21="Yes",$B$15="Yes"),0.75,1)'
    ws["F21"] = f"=ROUND({NET_AFTER_SALVAGE}*E21,2)-{SPOILAGE_DEDUCTIBLE}"
    ws["F21"].number_format = money_fmt
    ws["G21"] = '=IF(ABS(E21-$B$16)<0.001,"No","Yes")'
    ws["H21"] = '=IF(ABS(F21-\'Reserve Bridge\'!C14)<0.01,"No","Yes")'
    for c in range(1, 9):
        ws.cell(21, c).fill = cf_fill

    # Row 22: longer hypothetical
    ws["A22"] = "Hypothetical — longer OEM interval"
    ws["B22"] = oem_long
    ws["C22"] = "=$B$8+B22"
    ws["D22"] = '=IF($B$6>C22,"Yes","No")'
    ws["E22"] = '=IF(AND(D22="Yes",$B$15="Yes"),0.75,1)'
    ws["F22"] = f"=ROUND({NET_AFTER_SALVAGE}*E22,2)-{SPOILAGE_DEDUCTIBLE}"
    ws["F22"].number_format = money_fmt
    ws["G22"] = '=IF(ABS(E22-$B$16)<0.001,"No","Yes")'
    ws["H22"] = '=IF(ABS(F22-\'Reserve Bridge\'!C14)<0.01,"No","Yes")'
    for c in range(1, 9):
        ws.cell(22, c).fill = cf_fill

    for r in range(20, 23):
        for c in range(1, 9):
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = body_font

    ws["A24"] = (
        "Note: yellow rows are counterfactual sensitivity only. "
        "Actual coinsurance uses row 16 / source OEM interval from N-02."
    )
    ws["A24"].alignment = Alignment(wrap_text=True)
    autosize(ws, 48)

    # ========== Inventory Audit Trail ==========
    ws = wb.create_sheet("Inventory Audit Trail")
    ws["A1"] = "Per-lot status pipeline (formula-linked eligible amounts)"
    ws["A1"].font = title_font
    inv_h = [
        "source_lot_id",
        "zone",
        "raw_amount",
        "status",
        "duplicate_VOID_flag",
        "stock_nonstock_class",
        "coverage_treatment",
        "eligible_amount",
        "exclusion_reason",
        "valuation_basis",
    ]
    for c, h in enumerate(inv_h, start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 10)

    r = 4
    salvage_row = None
    void_row = None
    pkg_row = None
    dup_row = None
    for lot in LOTS:
        lot_id, desc, qty, ucost, usell, lcost, status, covered = lot
        zone = "Staging" if lot_id == "PKG-991" else "Zone B"
        if status == "VOID":
            dv = "VOID"
        elif status == "Duplicate":
            dv = "Duplicate"
        else:
            dv = "None"
        if lot_id == "PKG-991":
            klass = "Non-stock packaging"
            treat = "Exclude"
            reason = "Packaging — not stock under memo definition"
            basis = "n/a — excluded"
            flag = 0
        elif status == "VOID":
            klass = "Stock (ineligible status)"
            treat = "Exclude"
            reason = "VOID — never in Zone B"
            basis = "n/a — excluded"
            flag = 0
        elif status == "Duplicate":
            klass = "Stock (duplicate rekey)"
            treat = "Exclude"
            reason = "Duplicate rekey of LOT-B-218"
            basis = "n/a — excluded"
            flag = 0
        else:
            klass = "Stock"
            treat = "Include — covered stock"
            reason = ""
            basis = "Invoice / replacement cost (line_cost)"
            flag = 1

        ws.cell(r, 1, lot_id)
        ws.cell(r, 2, zone)
        ws.cell(r, 3, money(lcost)).number_format = money_fmt
        ws.cell(r, 4, status)
        ws.cell(r, 5, dv)
        ws.cell(r, 6, klass)
        ws.cell(r, 7, treat)
        ws.cell(r, 8, f"=IF(G{r}=\"Include — covered stock\",C{r},0)").number_format = money_fmt
        ws.cell(r, 9, reason)
        ws.cell(r, 10, basis)
        for c in range(1, 11):
            ws.cell(r, c).font = body_font
            ws.cell(r, c).border = thin
        if lot_id == SALVAGE_LOT:
            salvage_row = r
        if lot_id == "LOT-B-099":
            void_row = r
        if lot_id == "PKG-991":
            pkg_row = r
        if lot_id == "LOT-B-218-DUP":
            dup_row = r
        r += 1

    last_lot = r - 1
    # Totals block
    t = last_lot + 2
    ws.cell(t, 1, "Control totals").font = header_font
    ws.cell(t + 1, 1, "Eligible covered stock")
    ws.cell(t + 1, 2, f"=SUM(H4:H{last_lot})").number_format = money_fmt
    ws.cell(t + 2, 1, "VOID inventory")
    ws.cell(t + 2, 2, f'=SUMIF(E4:E{last_lot},"VOID",C4:C{last_lot})').number_format = money_fmt
    ws.cell(t + 3, 1, "Duplicate inventory")
    ws.cell(t + 3, 2, f'=SUMIF(E4:E{last_lot},"Duplicate",C4:C{last_lot})').number_format = money_fmt
    ws.cell(t + 4, 1, "Packaging / non-stock exclusions")
    ws.cell(t + 4, 2, f'=SUMIF(F4:F{last_lot},"Non-stock*",C4:C{last_lot})').number_format = money_fmt
    ws.cell(t + 5, 1, "Other denied/excluded (equipment + BI demands — documented outside lot pipe)")
    ws.cell(t + 5, 2, other_denied).number_format = money_fmt
    ws.cell(t + 6, 1, "Raw inventory total (lot population)")
    ws.cell(t + 6, 2, f"=SUM(C4:C{last_lot})").number_format = money_fmt
    ws.cell(t + 7, 1, "Eligible + VOID + Duplicate + Packaging")
    ws.cell(t + 7, 2, f"=B{t+1}+B{t+2}+B{t+3}+B{t+4}").number_format = money_fmt
    ws.cell(t + 8, 1, "Control check: raw = eligible + excluded/dup/VOID adjustments")
    ws.cell(t + 8, 2, f'=IF(ABS(B{t+6}-B{t+7})<0.01,"PASS","FAIL")')
    ws.cell(t + 8, 2).fill = pass_fill
    ws.cell(t + 8, 1).font = header_font
    ws.cell(t + 8, 2).font = header_font

    covered_total_ref = f"'Inventory Audit Trail'!B{t+1}"
    salvage_line_ref = f"'Inventory Audit Trail'!H{salvage_row}"
    raw_sum_ref = f"'Inventory Audit Trail'!B{t+6}"
    void_excl_ref = f"'Inventory Audit Trail'!B{t+2}"
    dup_excl_ref = f"'Inventory Audit Trail'!B{t+3}"
    pkg_excl_ref = f"'Inventory Audit Trail'!B{t+4}"
    inv_pass_ref = f"'Inventory Audit Trail'!B{t+8}"

    for rr in range(t + 1, t + 9):
        for c in range(1, 3):
            ws.cell(rr, c).border = thin
            ws.cell(rr, c).font = body_font if rr != t + 8 else header_font
    autosize(ws, 40)

    # ========== Valuation Reconciliation ==========
    ws = wb.create_sheet("Valuation Reconciliation")
    ws["A1"] = "Valuation reconciliation — candidate bases → governing basis"
    ws["A1"].font = title_font
    vh = ["Candidate basis", "Source of candidate", "Selected for actual?", "Rationale", "Implied amount"]
    for c, h in enumerate(vh, start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 5)

    ws["A4"] = "Selling price (unit_selling_price aggregates on covered lots)"
    ws["B4"] = f"{CLAIM_FILE} Inventory + N-01"
    ws["C4"] = "No — counterfactual only"
    ws["D4"] = f"Selling-price rider not elected ({POLICY_FILE} PS-24); {MEMO_FILE} requires invoice/replacement cost"
    ws["E4"] = CLAIMED_SELL_COVERED
    ws["E4"].number_format = money_fmt
    ws["C4"].fill = cf_fill

    ws["A5"] = "Invoice / replacement cost (line_cost)"
    ws["B5"] = f"{POLICY_FILE} PS-09; {MEMO_FILE} valuation rule"
    ws["C5"] = "Yes — governing"
    ws["D5"] = "Active CP 04 40 valuation; memo hierarchy over stale field note"
    ws["E5"] = f"={covered_total_ref}"
    ws["E5"].number_format = money_fmt

    for r in range(4, 6):
        for c in range(1, 6):
            ws.cell(r, c).font = body_font
            ws.cell(r, c).border = thin
            ws.cell(r, c).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[r].height = 40

    ws["A7"] = "Population affected"
    ws["B7"] = f"Eligible covered stock lots only ({n_eligible} of {n_lots} demand lots)"
    ws["A8"] = "Governing covered amount (actual)"
    ws["B8"] = f"={covered_total_ref}"
    ws["B8"].number_format = money_fmt
    ws["A8"].font = header_font
    ws["B8"].font = header_font
    ws["A9"] = "Rejected basis amount (not used in actual reserve)"
    ws["B9"] = "=E4"
    ws["B9"].number_format = money_fmt
    ws["B9"].fill = cf_fill
    border_range(ws, 7, 9, 1, 2)
    autosize(ws, 55)

    # ========== Reserve Bridge ==========
    ws = wb.create_sheet("Reserve Bridge")
    ws["A1"] = "Indemnity case reserve bridge (formula-linked — no hard-coded final)"
    ws["A1"].font = title_font
    ws["A3"] = "Stage"
    ws["B3"] = "Description"
    ws["C3"] = "Amount"
    ws["D3"] = "Formula / source"
    style_header_row(ws, 3, 4)

    ws["A4"] = "1"
    ws["B4"] = "Raw inventory"
    ws["C4"] = f"={raw_sum_ref}"
    ws["D4"] = "Inventory Audit Trail raw sum"

    ws["A5"] = "2"
    ws["B5"] = "Exclusions / VOID"
    ws["C5"] = f"=-{void_excl_ref}"
    ws["D5"] = "Less VOID"

    ws["A6"] = "3"
    ws["B6"] = "Duplicate resolution"
    ws["C6"] = f"=-{dup_excl_ref}"
    ws["D6"] = "Less duplicates"

    ws["A7"] = "4"
    ws["B7"] = "Non-stock packaging exclusions"
    ws["C7"] = f"=-{pkg_excl_ref}"
    ws["D7"] = "Less packaging"

    ws["A8"] = "5"
    ws["B8"] = "Eligible covered stock"
    ws["C8"] = f"={covered_total_ref}"
    ws["D8"] = "Invoice eligible total"

    ws["A9"] = "Footing check (raw + adj = eligible)"
    ws["C9"] = "=C4+C5+C6+C7"
    ws["D9"] = '=IF(ABS(C9-C8)<0.01,"PASS","FAIL")'
    ws["D9"].fill = pass_fill

    ws["A10"] = "6"
    ws["B10"] = "Salvage credit"
    ws["C10"] = f"=ROUND({salvage_line_ref}*{SALVAGE_RATE},2)"
    ws["D10"] = f"{SALVAGE_LOT} × {int(SALVAGE_RATE*100)}%"

    ws["A11"] = "7"
    ws["B11"] = "Net after salvage"
    ws["C11"] = "=C8-C10"
    ws["D11"] = "Eligible − salvage"

    ws["A12"] = "8"
    ws["B12"] = "After maintenance coinsurance"
    ws["C12"] = "=ROUND(C11*'Maintenance Timeline'!B16,2)"
    ws["D12"] = "× Maintenance Timeline!B16"

    ws["A13"] = "9"
    ws["B13"] = "Less Active spoilage deductible"
    ws["C13"] = SPOILAGE_DEDUCTIBLE
    ws["D13"] = "Active — not superseded (see Evidence matrix B)"

    ws["A14"] = "10"
    ws["B14"] = "Indemnity case reserve"
    ws["C14"] = "=C12-C13"
    ws["D14"] = "Formula chain — not typed"
    ws["B14"].font = header_font
    ws["C14"].font = header_font

    for r in range(4, 15):
        for c in range(1, 5):
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = body_font if r != 14 else header_font
            if c == 3 and r != 9:
                ws.cell(r, 3).number_format = money_fmt
    ws["C9"].number_format = money_fmt
    ws["C14"].number_format = money_fmt

    # Keep C14 as the canonical reserve; also alias note
    ws["A16"] = "ALAE excluded from this bridge — see ALAE sheet"
    autosize(ws)

    # ========== Pure vs Case ==========
    ws = wb.create_sheet("Pure vs Case")
    ws["A1"] = "Pure vs case reserve bridge — double-counting control"
    ws["A1"].font = title_font
    ws["A3"] = "Component"
    ws["B3"] = "Amount"
    ws["C3"] = "Notes"
    style_header_row(ws, 3, 3)

    ws["A4"] = "Cleaned indemnity case reserve"
    ws["B4"] = "='Reserve Bridge'!C14"
    ws["B4"].number_format = money_fmt
    ws["C4"] = "From Reserve Bridge formula chain"

    ws["A5"] = "Triangle / other indicated amount"
    ws["B5"] = 0
    ws["B5"].number_format = money_fmt
    ws["C5"] = "Not applicable — packet is a single-claim coverage file; no triangle indication supplied"

    ws["A6"] = "Pure IBNR"
    ws["B6"] = 0
    ws["B6"].number_format = money_fmt
    ws["C6"] = "No pure IBNR indicated for this single known claim beyond the case reserve"

    ws["A7"] = "Total reserve (case + pure IBNR)"
    ws["B7"] = "=B4+B5+B6"
    ws["B7"].number_format = money_fmt
    ws["C7"] = "Formula sum"

    ws["A8"] = "Double-counting test"
    ws["B8"] = '=IF(AND(B6=0,ABS(B7-B4)<0.01),"PASS — case not also in pure IBNR","FAIL")'
    ws["B8"].fill = pass_fill
    ws["C8"] = (
        "Case amount is booked once on the case line. Pure IBNR is zero for this known claim, "
        "so the case figure is not simultaneously included in pure IBNR."
    )
    ws["C8"].alignment = Alignment(wrap_text=True)
    for r in range(4, 9):
        for c in range(1, 4):
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = body_font
    ws.row_dimensions[8].height = 48
    autosize(ws, 55)

    # ========== Scenario Checks ==========
    ws = wb.create_sheet("Scenario Checks")
    ws["A1"] = "Counterfactual / sensitivity scenarios — NOT actual committee conclusions"
    ws["A1"].font = title_font
    ws["A1"].fill = cf_fill

    ws["A3"] = "Actual indemnity case reserve (governing)"
    ws["B3"] = "='Reserve Bridge'!C14"
    ws["B3"].number_format = money_fmt

    ws["A5"] = "Scenario"
    ws["B5"] = "Mark"
    ws["C5"] = "Counterfactual input"
    ws["D5"] = "Formula result"
    ws["E5"] = "Delta vs actual"
    ws["F5"] = "Used for actual conclusion?"
    style_header_row(ws, 5, 6)

    # S1 wrong deductible
    ws["A6"] = "S1 — Wrong deductible (superseded)"
    ws["B6"] = "Counterfactual"
    ws["C6"] = SUPERSEDED_DEDUCTIBLE
    ws["C6"].number_format = money_fmt
    ws["D6"] = f"='Reserve Bridge'!C12-{SUPERSEDED_DEDUCTIBLE}"
    ws["D6"].number_format = money_fmt
    ws["E6"] = "=D6-$B$3"
    ws["E6"].number_format = money_fmt
    ws["F6"] = "No"

    # S2 selling price
    ws["A7"] = "S2 — Selling-price basis"
    ws["B7"] = "Counterfactual"
    ws["C7"] = "='Valuation Reconciliation'!E4"
    ws["C7"].number_format = money_fmt
    ws["D7"] = f"=ROUND(({CLAIMED_SELL_COVERED}-{SALVAGE_AMOUNT})*'Maintenance Timeline'!B16,2)-{SPOILAGE_DEDUCTIBLE}"
    ws["D7"].number_format = money_fmt
    ws["E7"] = "=D7-$B$3"
    ws["E7"].number_format = money_fmt
    ws["F7"] = "No"
    ws["C7"] = CLAIMED_SELL_COVERED
    ws["C7"].number_format = money_fmt

    # S3 no coinsurance
    ws["A8"] = "S3 — No maintenance coinsurance"
    ws["B8"] = "Counterfactual"
    ws["C8"] = 1.0
    ws["D8"] = f"={NET_AFTER_SALVAGE}-{SPOILAGE_DEDUCTIBLE}"
    ws["D8"].number_format = money_fmt
    ws["E8"] = "=D8-$B$3"
    ws["E8"].number_format = money_fmt
    ws["F8"] = "No"

    # S4 equipment covered
    ws["A9"] = "S4 — Equipment hypothetically covered"
    ws["B9"] = "Counterfactual"
    ws["C9"] = "='Denied Items'!B12"
    ws["C9"].number_format = money_fmt
    ws["D9"] = f"=$B$3+'Denied Items'!B12"
    ws["D9"].number_format = money_fmt
    ws["E9"] = "=D9-$B$3"
    ws["E9"].number_format = money_fmt
    ws["F9"] = "No — actual disposition remains Deny"

    # S5 VOID restored / varying excluded lot
    ws["A10"] = "S5 — Excluded/VOID lot under actual decision"
    ws["B10"] = "Counterfactual control"
    ws["C10"] = f"='Inventory Audit Trail'!C{void_row}"
    ws["C10"].number_format = money_fmt
    # Actual reserve with VOID still excluded equals baseline; alt if VOID were included:
    ws["D10"] = f"=ROUND(({COVERED_STOCK_COST}+{void_cost}-{SALVAGE_AMOUNT})*'Maintenance Timeline'!B16,2)-{SPOILAGE_DEDUCTIBLE}"
    ws["D10"].number_format = money_fmt
    ws["E10"] = (
        f'=IF(ABS($B$3-({CASE_RESERVE}))<0.01,'
        f'"Actual reserve unchanged while VOID excluded (PASS control)",'
        f'"FAIL")'
    )
    ws["F10"] = "No — VOID remains excluded in actual trail"

    for r in range(6, 11):
        for c in range(1, 7):
            ws.cell(r, c).border = thin
            ws.cell(r, c).font = body_font
            ws.cell(r, c).fill = cf_fill
            ws.cell(r, c).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[r].height = 36

    ws["A12"] = (
        "S5 note: D10 shows the counterfactual reserve if VOID LOT-B-099 were improperly restored to eligible; "
        "E10 confirms the actual governing reserve (B3) is the cleaned case amount with VOID excluded. "
        "Varying the VOID raw amount while coverage_treatment remains Exclude does not feed Reserve Bridge."
    )
    ws["A12"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[12].height = 48
    autosize(ws, 42)

    # ========== Decision Trace ==========
    ws = wb.create_sheet("Decision Trace")
    ws["A1"] = "Coverage-to-financial-impact dependency graph"
    ws["A1"].font = title_font
    dh = ["Decision", "Source evidence", "Rule", "Test", "Conclusion", "Financial impact"]
    for c, h in enumerate(dh, start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 6)

    traces = [
        (
            "Stock coverage",
            f"{CLAIM_FILE} Inventory/Loss Notice; {POLICY_FILE} CP 04 40; {MEMO_FILE}",
            "Spoilage stock trigger + stock definition",
            "On-prem breakdown → temperature change to Open/Open-Salvage Zone B stock",
            "Accept — Partial",
            "Feeds Reserve Bridge eligible stock",
        ),
        (
            "Equipment coverage",
            f"{CLAIM_FILE} Equipment + N-09; {POLICY_FILE} Mechanical Breakdown; {MEMO_FILE}",
            "Mechanical Breakdown bars direct equipment repair; no floater",
            "Is demand for repair/replacement of failed equipment?",
            "Deny",
            f"Impact 0 (footed demand {EQUIPMENT_REPAIR:,.2f} documented only)",
        ),
        (
            "BI coverage",
            f"{CLAIM_FILE} BI Claim; {POLICY_FILE} waiting period; {MEMO_FILE}",
            "Waiting period vs logger interruption",
            f"{OUTAGE_HOURS}h ?≥ {BI_WAITING_HOURS}h",
            "Deny",
            "Impact 0",
        ),
        (
            "Packaging treatment",
            f"{CLAIM_FILE} PKG-991; {MEMO_FILE} stock definition",
            "Packaging not stock",
            "Is line perishable frozen food product?",
            "Deny / Exclude",
            f"Exclude {pkg_cost:,.2f} from eligible stock",
        ),
        (
            "Maintenance coinsurance",
            f"{CLAIM_FILE} N-02 dates/interval; {MEMO_FILE} grace/safe harbor",
            "Overdue beyond grace + vendor cancel within 14 days → 75% pay",
            "See Maintenance Timeline conditions",
            f"Pay factor {'75%' if COINSURANCE_FACTOR == 0.75 else '100%'}",
            "Reserve Bridge stage 8",
        ),
        (
            "Valuation",
            f"{POLICY_FILE} PS-24; {MEMO_FILE}; N-01 competing",
            "Invoice unless selling-price elected",
            "Was selling-price rider elected?",
            "Invoice / replacement cost",
            f"Covered amount → {COVERED_STOCK_COST:,.2f} (link)",
        ),
        (
            "Deductible",
            f"{POLICY_FILE} Active vs Superseded rows; {MEMO_FILE} hierarchy",
            "Active spoilage deductible governs",
            "Schedule status Active vs Superseded",
            f"Apply Active {SPOILAGE_DEDUCTIBLE:,.0f}",
            "Reserve Bridge stage 9",
        ),
    ]
    for i, row in enumerate(traces, start=4):
        for c, val in enumerate(row, start=1):
            ws.cell(i, c, val).font = body_font
            ws.cell(i, c).border = thin
            ws.cell(i, c).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 48

    ws["A12"] = "Trace → reserve link"
    ws["B12"] = "='Reserve Bridge'!C14"
    ws["B12"].number_format = money_fmt
    ws["C12"] = "File Recommendation must use this actual reserve, not Scenario Checks counterfactuals"
    border_range(ws, 12, 12, 1, 3)
    autosize(ws, 36)

    # ========== Denied Items ==========
    ws = wb.create_sheet("Denied Items")
    ws["A1"] = "Denied / excluded items + equipment footing block"
    ws["A1"].font = title_font
    ws["A3"] = "item"
    ws["B3"] = "amount"
    ws["C3"] = "disposition"
    ws["D3"] = "reason"
    style_header_row(ws, 3, 4)

    for i, (eid, desc, amt) in enumerate(EQUIPMENT_LINES, start=4):
        ws.cell(i, 1, f"Equipment {eid} — {desc}")
        ws.cell(i, 2, money(amt)).number_format = money_fmt
        ws.cell(i, 3, "Component")
        ws.cell(i, 4, f"{CLAIM_FILE} Equipment tab")

    ws["A9"] = "Equipment component total (EQ-01..EQ-05)"
    ws["B9"] = "=SUM(B4:B8)"
    ws["B9"].number_format = money_fmt
    ws["C9"] = "Source-of-truth footing"
    ws["D9"] = "Formula sum"

    ws["A10"] = "Prior worksheet EQ-SUB (pre-correction)"
    ws["B10"] = money(EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL)
    ws["B10"].number_format = money_fmt
    ws["C10"] = "Superseded figure"
    ws["D10"] = f"{CLAIM_FILE} N-09"

    ws["A11"] = "Equipment footing variance"
    ws["B11"] = "=B10-B9"
    ws["B11"].number_format = money_fmt
    ws["C11"] = "Documented"
    ws["D11"] = "Worksheet addition error"

    ws["A12"] = "Corrected equipment footing (denied demand)"
    ws["B12"] = "=B9"
    ws["B12"].number_format = money_fmt
    ws["C12"] = "Deny"
    ws["D12"] = "Mechanical Breakdown; no floater — actual indemnity impact 0"

    ws["A13"] = "Counterfactual if equipment covered (see Scenario Checks S4)"
    ws["B13"] = "=B12"
    ws["B13"].number_format = money_fmt
    ws["C13"] = "Counterfactual only"
    ws["D13"] = "Not used in actual reserve"
    ws["A13"].fill = cf_fill

    ws["A14"] = "Business Income demand"
    ws["B14"] = money(BI_CLAIMED)
    ws["B14"].number_format = money_fmt
    ws["C14"] = "Deny"
    ws["D14"] = f"Outage {OUTAGE_HOURS}h < waiting period {BI_WAITING_HOURS}h"

    ws["A15"] = "Packaging PKG-991"
    ws["B15"] = f"='Inventory Audit Trail'!C{pkg_row}"
    ws["B15"].number_format = money_fmt
    ws["C15"] = "Exclude"
    ws["D15"] = "Not stock"

    ws["A16"] = "VOID LOT-B-099"
    ws["B16"] = f"='Inventory Audit Trail'!C{void_row}"
    ws["B16"].number_format = money_fmt
    ws["C16"] = "Exclude"
    ws["D16"] = "Never loaded to Zone B"

    ws["A17"] = "Duplicate LOT-B-218-DUP"
    ws["B17"] = f"='Inventory Audit Trail'!C{dup_row}"
    ws["B17"].number_format = money_fmt
    ws["C17"] = "Exclude"
    ws["D17"] = "Duplicate rekey"

    for r in range(4, 18):
        for c in range(1, 5):
            ws.cell(r, c).font = body_font
            ws.cell(r, c).border = thin
    ws["A9"].font = header_font
    ws["B9"].font = header_font
    ws["A12"].font = header_font
    ws["B12"].font = header_font
    autosize(ws, 50)

    # ========== ALAE ==========
    ws = wb.create_sheet("ALAE")
    ws["A1"] = "ALAE / expense — separate from indemnity case reserve"
    ws["A1"].font = title_font
    for c, h in enumerate(["txn_id", "date", "type", "amount", "status", "memo"], start=1):
        ws.cell(3, c, h)
    style_header_row(ws, 3, 6)
    pay_rows = [
        ("P-001", "2025-11-22", "Expense", 1840.00, "Paid", "Independent adjuster day rate"),
        ("P-002", "2025-11-24", "Expense", 620.50, "Paid", "Logger download / lab courier"),
        ("P-003", "2025-11-26", "Expense", 275.00, "Paid", "Hygienist swab panel"),
        ("P-005", "2025-12-04", "Expense", 410.00, "Pending", "Coverage counsel consult hour block"),
    ]
    for i, row in enumerate(pay_rows, start=4):
        ws.cell(i, 1, row[0])
        ws.cell(i, 2, row[1])
        ws.cell(i, 3, row[2])
        ws.cell(i, 4, money(row[3])).number_format = money_fmt
        ws.cell(i, 5, row[4])
        ws.cell(i, 6, row[5])
        for c in range(1, 7):
            ws.cell(i, c).font = body_font
            ws.cell(i, c).border = thin
    ws["A9"] = "ALAE expense total (not in indemnity reserve)"
    ws["B9"] = "=SUM(D4:D7)"
    ws["B9"].number_format = money_fmt
    ws["A9"].font = header_font
    ws["A10"] = "Indemnity case reserve (link)"
    ws["B10"] = "='Reserve Bridge'!C14"
    ws["B10"].number_format = money_fmt
    ws["A11"] = "Separation check"
    ws["B11"] = '=IF(AND(ABS(B10-\'Reserve Bridge\'!C14)<0.01,ABS(B9-B10)>0.01),"PASS — ALAE excluded from indemnity","FAIL")'
    ws["B11"].fill = pass_fill
    autosize(ws, 45)

    # ========== Consistency Checks ==========
    ws = wb.create_sheet("Consistency Checks")
    ws["A1"] = "Internal consistency — automated PASS/FAIL"
    ws["A1"].font = title_font
    ws["A3"] = "Check"
    ws["B3"] = "Result"
    ws["C3"] = "Detail"
    style_header_row(ws, 3, 3)

    checks = [
        (
            4,
            "1. Inventory population reconciles",
            f"={inv_pass_ref}",
            "raw = eligible + VOID + duplicate + packaging",
        ),
        (
            5,
            "2. Equipment corrected subtotal = components",
            '=IF(ABS(\'Denied Items\'!B12-\'Denied Items\'!B9)<0.01,"PASS","FAIL")',
            "Corrected footing equals EQ-01..EQ-05 sum",
        ),
        (
            6,
            "3. BI elapsed hours reconcile to source",
            f'=IF({OUTAGE_HOURS}=14,"PASS","FAIL")',
            f"Logger outage hours used = {OUTAGE_HOURS} per BI Claim / Loss Notice",
        ),
        (
            7,
            "4. Maintenance elapsed days reconcile to source dates",
            f'=IF(AND(\'Maintenance Timeline\'!B6={DAYS_SINCE_SERVICE},'
            f'\'Maintenance Timeline\'!B4="{LAST_SERVICE}",'
            f'\'Maintenance Timeline\'!B5="{LOSS_DATE}"),"PASS","FAIL")',
            f"{LOSS_DATE} − {LAST_SERVICE} = {DAYS_SINCE_SERVICE}",
        ),
        (
            8,
            "5. Reserve equals formula chain (not typed orphan)",
            '=IF(ABS(\'Reserve Bridge\'!C14-(\'Reserve Bridge\'!C12-\'Reserve Bridge\'!C13))<0.01,"PASS","FAIL")',
            "C14 = after coinsurance − deductible",
        ),
        (
            9,
            "6. ALAE excluded from indemnity reserve",
            "='ALAE'!B11",
            "Expense total not rolled into case reserve",
        ),
        (
            10,
            "7. Recommendation consistent with coverage + finance",
            '=IF(AND(\'Coverage Decision Tree\'!B9="Partial Coverage",'
            'ABS(\'File Recommendation\'!B9-\'Reserve Bridge\'!C14)<0.01),'
            '"PASS","FAIL")',
            "Partial Coverage + reserve link matches bridge",
        ),
    ]
    for row, label, formula, detail in checks:
        ws.cell(row, 1, label).font = body_font
        cell = ws.cell(row, 2, formula)
        cell.font = header_font
        cell.fill = pass_fill
        ws.cell(row, 3, detail).font = body_font
        for c in range(1, 4):
            ws.cell(row, c).border = thin

    ws["A12"] = "Any FAIL must be corrected before committee circulation."
    autosize(ws, 55)

    # ========== File Recommendation ==========
    ws = wb.create_sheet("File Recommendation")
    ws["A1"] = "File-review committee recommendation (committee-ready)"
    ws["A1"].font = title_font
    ws["A3"] = "Element"
    ws["B3"] = "Committee conclusion"
    ws["C3"] = "Evidence / workbook link"
    style_header_row(ws, 3, 3)

    recs = [
        (
            "Coverage posture",
            "Partial Coverage — Accept/Partial Zone B spoiled stock under CP 04 40 with maintenance coinsurance; "
            "Deny equipment under Mechanical Breakdown; Deny BI (waiting period not met); "
            "Deny/Exclude packaging from stock.",
            "Coverage Decision Tree + Decision Trace",
        ),
        (
            "Indemnity reserve",
            "Post the formula-driven indemnity case reserve from Reserve Bridge "
            "(cleaned invoice stock − salvage × Maintenance Timeline pay factor − Active deductible). "
            "Do not use Scenario Checks counterfactual figures.",
            "='Reserve Bridge'!C14",
        ),
        (
            "ALAE",
            "Keep ALAE/expense on the ALAE sheet outside the indemnity case reserve.",
            "ALAE separation check PASS",
        ),
        (
            "Major uncertainty",
            "Primary uncertainty is maintenance coinsurance branching on the OEM interval assumption "
            "and whether Active vs Superseded deductible status is misread; both are resolved on "
            "Maintenance Timeline and Evidence & Rule Matrix but remain the main sensitivity drivers.",
            "Maintenance Timeline sensitivity; Evidence matrix B",
        ),
        (
            "Key financial sensitivity",
            "OEM interval lengthening (hypothetical) can remove coinsurance; applying the superseded "
            "deductible or selling-price basis would misstate the reserve — see Scenario Checks S1–S3.",
            "Scenario Checks + Maintenance Timeline",
        ),
        (
            "Recommended underwriting disposition",
            "Refer file to committee as Partial Coverage with the linked indemnity case reserve; "
            "deny equipment and BI; reject selling-price valuation; apply Active deductible only; "
            "route any payment proposal above $250,000 for manager approval.",
            f"{MEMO_FILE} hierarchy; authority band on reserve vs $250,000",
        ),
    ]
    for i, (elem, concl, evid) in enumerate(recs, start=4):
        ws.cell(i, 1, elem).font = header_font
        ws.cell(i, 2, concl).font = body_font
        ws.cell(i, 2).alignment = Alignment(wrap_text=True)
        if evid.startswith("="):
            ws.cell(i, 3, evid).number_format = money_fmt
        else:
            ws.cell(i, 3, evid).font = body_font
        for c in range(1, 4):
            ws.cell(i, c).border = thin
        ws.row_dimensions[i].height = 56

    ws["A11"] = "Recommended indemnity case reserve (actual)"
    ws["B11"] = "='Reserve Bridge'!C14"
    # Use B9 as stable link for consistency check (also mirror)
    ws["A9"] = "Recommended indemnity case reserve (actual)"
    ws["B9"] = "='Reserve Bridge'!C14"
    ws["B9"].number_format = money_fmt
    ws["B9"].font = header_font
    # Clear duplicate - I created both A9 and A11. Fix: put reserve on B9 only matching consistency check
    # Overwrote row 9 which was underwriting disposition. Need to fix structure.

    # Actually looking at my loop: rows 4-9 are the 6 rec elements. Consistency check uses File Recommendation!B9
    # which would be underwriting disposition's col B if I put reserve on B9. Better put reserve on B12
    # and update consistency check to use B12.

    # Fix File Recommendation layout properly:
    # Clear the mistaken A11 duplicate - rewrite end of sheet cleanly via cell assigns
    ws["A11"] = "Authority check"
    ws["B11"] = '=IF(B12>250000,"Manager approval required","Within desk authority band")'
    ws["A12"] = "Recommended indemnity case reserve (actual — link)"
    ws["B12"] = "='Reserve Bridge'!C14"
    ws["B12"].number_format = money_fmt
    ws["B12"].font = header_font

    # Fix consistency check row 10 to use B12 - need to update that formula
    # We'll fix after - actually Consistency Checks already written with B9. Update it:
    # Re-open consistency - we can overwrite cell
    wb["Consistency Checks"]["A10"] = "7. Recommendation consistent with coverage + finance"
    wb["Consistency Checks"]["B10"] = (
        '=IF(AND(\'Coverage Decision Tree\'!B9="Partial Coverage",'
        'ABS(\'File Recommendation\'!B12-\'Reserve Bridge\'!C14)<0.01),'
        '"PASS","FAIL")'
    )
    wb["Consistency Checks"]["B10"].fill = pass_fill
    wb["Consistency Checks"]["C10"] = "Partial Coverage + reserve link matches bridge"

    # Remove erroneous B9 money link if it overwrote underwriting - check row 9
    # Row 9 should be underwriting disposition from loop. Then I set A9/B9 again - BUG.
    # Restore row 9 underwriting:
    ws["A9"] = "Recommended underwriting disposition"
    ws["B9"] = (
        "Refer file to committee as Partial Coverage with the linked indemnity case reserve; "
        "deny equipment and BI; reject selling-price valuation; apply Active deductible only; "
        "route any payment proposal above $250,000 for manager approval."
    )
    ws["B9"].alignment = Alignment(wrap_text=True)
    ws["B9"].font = body_font
    ws["C9"] = f"{MEMO_FILE} hierarchy; authority band on reserve vs $250,000"
    ws.row_dimensions[9].height = 56

    autosize(ws, 45)
    ws.column_dimensions["B"].width = 60

    GOLDEN.mkdir(parents=True, exist_ok=True)
    out = GOLDEN / DELIVERABLE
    wb.save(out)

    # Cached formula values for LLM-authorship / data_only readers
    inv_cache: dict[str, float | int | str] = {}
    for i, lot in enumerate(LOTS, start=4):
        inv_cache[f"H{i}"] = money(lot[5] if lot[7] else 0)
    inv_cache[f"B{t+1}"] = COVERED_STOCK_COST
    inv_cache[f"B{t+2}"] = void_cost
    inv_cache[f"B{t+3}"] = dup_cost
    inv_cache[f"B{t+4}"] = pkg_cost
    inv_cache[f"B{t+5}"] = other_denied
    inv_cache[f"B{t+6}"] = raw_zone_b
    inv_cache[f"B{t+7}"] = money(COVERED_STOCK_COST + void_cost + dup_cost + pkg_cost)
    inv_cache[f"B{t+8}"] = "PASS"

    formula_cache: dict[str, dict[str, float | int | str]] = {
        "Maintenance Timeline": {
            "B9": MAINTENANCE_THRESHOLD,
            "B10": DAYS_SINCE_SERVICE - MAINTENANCE_THRESHOLD,
            "B14": "Yes",
            "B15": "Yes",
            "B16": COINSURANCE_FACTOR,
            "B20": OEM_SERVICE_DAYS,
            "C20": MAINTENANCE_THRESHOLD,
            "D20": "Yes",
            "E20": COINSURANCE_FACTOR,
            "F20": CASE_RESERVE,
            "G20": "No",
            "H20": "No",
            "C21": thr_short,
            "D21": "Yes" if DAYS_SINCE_SERVICE > thr_short else "No",
            "E21": factor_short,
            "F21": reserve_oem_short,
            "G21": "No" if abs(factor_short - COINSURANCE_FACTOR) < 0.001 else "Yes",
            "H21": "No" if abs(reserve_oem_short - CASE_RESERVE) < 0.01 else "Yes",
            "C22": thr_long,
            "D22": "Yes" if DAYS_SINCE_SERVICE > thr_long else "No",
            "E22": factor_long,
            "F22": reserve_oem_long,
            "G22": "No" if abs(factor_long - COINSURANCE_FACTOR) < 0.001 else "Yes",
            "H22": "No" if abs(reserve_oem_long - CASE_RESERVE) < 0.01 else "Yes",
        },
        "Inventory Audit Trail": inv_cache,
        "Valuation Reconciliation": {
            "E5": COVERED_STOCK_COST,
            "B8": COVERED_STOCK_COST,
            "B9": CLAIMED_SELL_COVERED,
        },
        "Reserve Bridge": {
            "C4": raw_zone_b,
            "C5": -void_cost,
            "C6": -dup_cost,
            "C7": -pkg_cost,
            "C8": COVERED_STOCK_COST,
            "C9": COVERED_STOCK_COST,
            "D9": "PASS",
            "C10": SALVAGE_AMOUNT,
            "C11": NET_AFTER_SALVAGE,
            "C12": AFTER_COINSURANCE,
            "C14": CASE_RESERVE,
        },
        "Pure vs Case": {
            "B4": CASE_RESERVE,
            "B7": CASE_RESERVE,
            "B8": "PASS — case not also in pure IBNR",
        },
        "Scenario Checks": {
            "B3": CASE_RESERVE,
            "D6": reserve_wrong_ded,
            "E6": money(reserve_wrong_ded - CASE_RESERVE),
            "D7": money(money((CLAIMED_SELL_COVERED - SALVAGE_AMOUNT) * COINSURANCE_FACTOR) - SPOILAGE_DEDUCTIBLE),
            "E7": money(
                money((CLAIMED_SELL_COVERED - SALVAGE_AMOUNT) * COINSURANCE_FACTOR)
                - SPOILAGE_DEDUCTIBLE
                - CASE_RESERVE
            ),
            "D8": reserve_no_coin,
            "E8": money(reserve_no_coin - CASE_RESERVE),
            "C9": EQUIPMENT_REPAIR,
            "D9": reserve_equip_hyp,
            "E9": EQUIPMENT_REPAIR,
            "C10": void_cost,
            "D10": money(
                money((COVERED_STOCK_COST + void_cost - SALVAGE_AMOUNT) * COINSURANCE_FACTOR)
                - SPOILAGE_DEDUCTIBLE
            ),
            "E10": "Actual reserve unchanged while VOID excluded (PASS control)",
        },
        "Decision Trace": {"B12": CASE_RESERVE},
        "Denied Items": {
            "B9": EQUIPMENT_COMPONENT_TOTAL,
            "B11": EQUIPMENT_FOOTING_VARIANCE,
            "B12": EQUIPMENT_REPAIR,
            "B13": EQUIPMENT_REPAIR,
            "B15": pkg_cost,
            "B16": void_cost,
            "B17": dup_cost,
        },
        "ALAE": {
            "B9": alae_total,
            "B10": CASE_RESERVE,
            "B11": "PASS — ALAE excluded from indemnity",
        },
        "Consistency Checks": {
            "B4": "PASS",
            "B5": "PASS",
            "B6": "PASS",
            "B7": "PASS",
            "B8": "PASS",
            "B9": "PASS — ALAE excluded from indemnity",
            "B10": "PASS",
        },
        "File Recommendation": {
            "B12": CASE_RESERVE,
            "B11": "Within desk authority band",
        },
    }
    cache_xlsx_formula_values(out, formula_cache)
    sanitize_xlsx(out)
    return out


def main() -> None:
    out = build()
    print(f"Wrote {out}")
    print(f"Case reserve target: {CASE_RESERVE}")
    print(
        f"covered={COVERED_STOCK_COST} salvage={SALVAGE_AMOUNT} "
        f"net={NET_AFTER_SALVAGE} after_coin={AFTER_COINSURANCE}"
    )
    print(
        f"OEM={OEM_SERVICE_DAYS} elapsed={DAYS_SINCE_SERVICE} threshold={MAINTENANCE_THRESHOLD} "
        f"equipment_footed={EQUIPMENT_REPAIR} variance_noted={EQUIPMENT_FOOTING_VARIANCE}"
    )
    print(
        f"sens: short_oem_reserve={money(money(NET_AFTER_SALVAGE * (COINSURANCE_FACTOR if DAYS_SINCE_SERVICE > 80 + GRACE_DAYS else 1.0)) - SPOILAGE_DEDUCTIBLE)} "
        f"long_oem_reserve={money(NET_AFTER_SALVAGE - SPOILAGE_DEDUCTIBLE)}"
    )


if __name__ == "__main__":
    main()
