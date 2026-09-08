#!/usr/bin/env python3
"""Generate golden CAM true-up workbook for Meridian Commons."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from meridian_cam_constants import (
    DUP_LANDSCAPING,
    HVAC_REPLACEMENT,
    INSURANCE,
    MARKETING,
    PRIOR_BILLINGS,
    ROOF_CAPITAL,
    TARGET_ELIGIBLE_POOL,
    TENANTS,
)
from sanitize_office import cache_xlsx_formula_values, sanitize_xlsx

TASK = Path(__file__).resolve().parent.parent / "tasks" / "meridian-property-group-reconciliation"
INPUTS = TASK / "inputs"
OUT = TASK / "golden" / "cam_trueup_meridian_commons.xlsx"

HALF_POOL = round(TARGET_ELIGIBLE_POOL / 2, 2)
VACANCY_PCT = 12.0
H1_EXPANSION_HELD = 8.9  # Contour 27.1 - 18.2


def load_ledger() -> list[dict]:
    with (INPUTS / "meridian_commons_expense_ledger.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_row(row: dict) -> tuple[str, float]:
    amt = float(row["amount"])
    inv = row["invoice_ref"]
    gl = row["gl_account"]
    memo = (row["memo"] or "").lower()

    if inv == "EXP-4482" and row["entry_id"] == "JE-9006":
        return "exclude_duplicate", amt
    if abs(amt - ROOF_CAPITAL) < 0.01 or "roof replacement" in memo:
        return "exclude_capital_roof", amt
    if abs(amt - HVAC_REPLACEMENT) < 0.01 or "replacement rtu" in memo:
        return "exclude_capital_hvac", amt
    if gl == "6300" or abs(amt - INSURANCE) < 0.01:
        return "exclude_insurance", amt
    if gl == "6450" or abs(amt - MARKETING) < 0.01:
        return "exclude_marketing_pool", amt
    return "eligible_cam", amt


def half_shares(period: str) -> dict[str, float]:
    """Return suite -> share % for H1 or H2 (sums to 100)."""
    shares: dict[str, float] = {}
    for t in TENANTS:
        if t.get("vacant"):
            shares[t["suite"]] = VACANCY_PCT
            continue
        if t["suite"] == "T-118":
            shares["T-118"] = t["prorata_pct_h1"] if period == "H1" else t["prorata_pct"]
        else:
            shares[t["suite"]] = t["prorata_pct"]
    if period == "H1":
        shares["EXPANSION-HELD"] = H1_EXPANSION_HELD
    return shares


def allocate_half(pool: float, period: str) -> dict[str, float]:
    shares = half_shares(period)
    alloc = {s: round(pool * pct / 100.0, 2) for s, pct in shares.items()}

    vacancy_cost = alloc.get("T-122", 0.0)
    # H1 expansion-held GLA stays with owner (not yet Contour; not vacancy gross-up).
    absorbing = [
        t["suite"]
        for t in TENANTS
        if not t.get("vacant") and t["vacancy_clause"] == "tenants_absorb"
    ]
    abs_share_sum = sum(shares[s] for s in absorbing)
    for s in absorbing:
        alloc[s] = round(alloc[s] + vacancy_cost * shares[s] / abs_share_sum, 2)

    alloc.pop("T-122", None)
    alloc.pop("EXPANSION-HELD", None)
    return alloc


def apply_cap_and_marketing(annual_alloc: dict[str, float]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for t in TENANTS:
        if t.get("vacant"):
            continue
        suite = t["suite"]
        base = annual_alloc[suite]
        marketing_add = round(MARKETING * t["prorata_pct"] / 100.0, 2) if t["includes_marketing"] else 0.0
        before_cap = round(base + marketing_add, 2)
        cap = None
        if t["cam_cap_psf"] is not None:
            cap = round(t["cam_cap_psf"] * t["gla_sf"], 2)
        charged = before_cap if cap is None else min(before_cap, cap)
        billed = PRIOR_BILLINGS[suite]
        trueup = round(charged - billed, 2)
        out[suite] = {
            "tenant": t["tenant"],
            "base_alloc": base,
            "marketing_add": marketing_add,
            "before_cap": before_cap,
            "cap": cap,
            "charged": charged,
            "billed": billed,
            "trueup": trueup,
        }
    return out


def main() -> None:
    ledger = load_ledger()
    classified = []
    eligible = 0.0
    for row in ledger:
        flag, amt = classify_row(row)
        classified.append({**row, "flag": flag, "amount_f": amt})
        if flag == "eligible_cam":
            eligible += amt
    eligible = round(eligible, 2)
    assert abs(eligible - TARGET_ELIGIBLE_POOL) < 0.05, (eligible, TARGET_ELIGIBLE_POOL)

    h1 = allocate_half(HALF_POOL, "H1")
    h2 = allocate_half(HALF_POOL, "H2")
    annual = {s: round(h1.get(s, 0) + h2.get(s, 0), 2) for s in h1}
    results = apply_cap_and_marketing(annual)

    wb = Workbook()
    bold = Font(bold=True)
    formula_cache: dict[str, dict[str, float]] = {}

    # Expense Pool
    ws = wb.active
    ws.title = "Expense Pool"
    ws.append(["Meridian Commons 2025 CAM — eligible expense pool"])
    ws.append([])
    ws.append(["entry_id", "gl_account", "vendor", "amount", "classification", "source"])
    for c in ws[3]:
        c.font = bold
    r = 4
    for row in classified:
        ws.append(
            [
                row["entry_id"],
                row["gl_account"],
                row["vendor"],
                row["amount_f"],
                row["flag"],
                "meridian_commons_expense_ledger.csv",
            ]
        )
        r += 1
    last = r - 1
    ws.append([])
    ws.append(["Eligible CAM pool", None])
    pool_row = last + 2
    ws[f"B{pool_row}"] = f'=SUMIF(E4:E{last},"eligible_cam",D4:D{last})'
    formula_cache["Expense Pool"] = {f"B{pool_row}": eligible}
    ws.append(["Excluded capital roof", ROOF_CAPITAL])
    ws.append(["Excluded capital HVAC", HVAC_REPLACEMENT])
    ws.append(["Excluded insurance", INSURANCE])
    ws.append(["Excluded marketing from shared pool", MARKETING])
    ws.append(["Excluded duplicate EXP-4482", DUP_LANDSCAPING])

    # Tenant True-up
    wt = wb.create_sheet("Tenant True-up")
    wt.append(["suite", "tenant", "h1_alloc", "h2_alloc", "base_annual", "marketing_addon", "before_cap", "cam_cap", "charged", "prior_billed", "true_up", "action"])
    for c in wt[1]:
        c.font = bold
    row_i = 2
    for t in TENANTS:
        if t.get("vacant"):
            continue
        suite = t["suite"]
        res = results[suite]
        action = "Additional invoice" if res["trueup"] > 0 else ("Credit" if res["trueup"] < 0 else "No adjustment")
        wt.append(
            [
                suite,
                res["tenant"],
                h1[suite],
                h2[suite],
                None,
                res["marketing_add"],
                None,
                res["cap"] if res["cap"] is not None else "None",
                None,
                res["billed"],
                None,
                action,
            ]
        )
        wt[f"E{row_i}"] = f"=C{row_i}+D{row_i}"
        wt[f"G{row_i}"] = f"=E{row_i}+F{row_i}"
        if res["cap"] is not None:
            wt[f"I{row_i}"] = f"=MIN(G{row_i},H{row_i})"
        else:
            wt[f"I{row_i}"] = f"=G{row_i}"
        wt[f"K{row_i}"] = f"=I{row_i}-J{row_i}"
        formula_cache.setdefault("Tenant True-up", {}).update(
            {
                f"E{row_i}": res["base_alloc"],
                f"G{row_i}": res["before_cap"],
                f"I{row_i}": res["charged"],
                f"K{row_i}": res["trueup"],
            }
        )
        row_i += 1
    end = row_i - 1
    wt.append([])
    wt.append(["Total true-up (net additional billings)", None])
    tot_row = end + 2
    wt[f"B{tot_row}"] = f"=SUM(K2:K{end})"
    net_trueup = round(sum(results[s]["trueup"] for s in results), 2)
    formula_cache.setdefault("Tenant True-up", {})[f"B{tot_row}"] = net_trueup

    # Exceptions
    we = wb.create_sheet("Exceptions")
    we.append(["exception_type", "reference", "amount", "treatment", "source"])
    for c in we[1]:
        c.font = bold
    we.append(
        [
            "Capital roof in R&M",
            "SR-4419 / JE-9001",
            ROOF_CAPITAL,
            "Excluded from CAM pool",
            "meridian_commons_expense_ledger.csv; tenant_lease_abstracts.xlsx Abstract Notes",
        ]
    )
    we.append(
        [
            "Capital HVAC replacement",
            "CW-2281 / JE-9002",
            HVAC_REPLACEMENT,
            "Excluded from CAM pool",
            "meridian_commons_expense_ledger.csv; tenant_lease_abstracts.xlsx Abstract Notes",
        ]
    )
    we.append(
        [
            "Duplicate landscaping invoice",
            "EXP-4482",
            DUP_LANDSCAPING,
            "Count once; exclude JE-9006 repost",
            "meridian_commons_expense_ledger.csv",
        ]
    )
    we.append(
        [
            "Property insurance separately billed",
            "MM-2025-PREM",
            INSURANCE,
            "Excluded from CAM pool",
            "meridian_commons_expense_ledger.csv; tenant_lease_abstracts.xlsx",
        ]
    )
    we.append(
        [
            "Marketing excluded from shared pool",
            "MKT-2025-Q2",
            MARKETING,
            "Add Meridian Outfitters pro-rata only",
            "tenant_lease_abstracts.xlsx CAM Provisions",
        ]
    )
    we.append(
        [
            "Ridgeway Dental CAM cap",
            "T-104",
            round(4.85 * 2840, 2),
            "Charge limited to $4.85/SF × 2,840 SF",
            "tenant_lease_abstracts.xlsx CAM Provisions",
        ]
    )
    we.append(
        [
            "Contour mid-year expansion",
            "T-118",
            results["T-118"]["trueup"],
            "H1 at 18.2%, H2 at 27.1%; prior billings used 18.2% all year",
            "tenant_lease_abstracts.xlsx; prior_cam_billing_register.txt",
        ]
    )
    we.append(
        [
            "Vacancy absorption split",
            "T-122 + H1 expansion-held",
            round(TARGET_ELIGIBLE_POOL * (VACANCY_PCT + H1_EXPANSION_HELD / 2) / 100, 2),
            "Outfitters and Contour absorb vacancy; other tenants owner-absorb",
            "tenant_lease_abstracts.xlsx CAM Provisions",
        ]
    )

    # Recommendation
    wr = wb.create_sheet("Recommendation")
    wr["A1"] = "Controller recommendation — Meridian Commons 2025 CAM true-up"
    wr["A3"] = "Eligible shared CAM pool"
    wr["B3"] = f"='Expense Pool'!B{pool_row}"
    wr["A4"] = "Net additional billings / (credits)"
    wr["B4"] = f"='Tenant True-up'!B{tot_row}"
    wr["A6"] = "Recommendation"
    lines = []
    for suite, res in results.items():
        if res["trueup"] > 0.5:
            lines.append(f"Issue additional CAM invoice to {res['tenant']} ({suite}) for ${res['trueup']:,.2f}.")
        elif res["trueup"] < -0.5:
            lines.append(f"Issue CAM credit to {res['tenant']} ({suite}) for ${abs(res['trueup']):,.2f}.")
    lines.append(
        "Do not bill capital roof or HVAC replacement as CAM. Apply Ridgeway Dental's $4.85/SF cap. "
        "Contour Fitness true-up reflects the July expansion documented in tenant_lease_abstracts.xlsx "
        "and under-billing noted in prior_cam_billing_register.txt. "
        "For 2026 estimate assumptions: (1) update Contour's share in the billing system on expansion "
        "effective dates, (2) hold Ridgeway estimates at the lease CAM cap until abstracts change, and "
        "(3) exclude capital rounds and separately billed insurance from the shared CAM forecast."
    )
    wr["A7"] = " ".join(lines)
    formula_cache["Recommendation"] = {
        "B3": eligible,
        "B4": net_trueup,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    cache_xlsx_formula_values(OUT, formula_cache)
    sanitize_xlsx(OUT)

    print(f"Wrote {OUT}")
    print(f"Eligible pool: {eligible}")
    print(f"Net true-up: {net_trueup}")
    for suite, res in results.items():
        print(f"  {suite} {res['tenant']}: charged={res['charged']} billed={res['billed']} trueup={res['trueup']}")


if __name__ == "__main__":
    main()
