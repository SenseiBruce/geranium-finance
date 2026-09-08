#!/usr/bin/env python3
"""Generate input files for Meridian Commons CAM true-up redesign."""

from __future__ import annotations

import csv
import random
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

TASK = (
    Path(__file__).resolve().parent.parent
    / "tasks"
    / "meridian-property-group-reconciliation"
    / "inputs"
)

rng = random.Random(20251231)


def write_expense_ledger(path: Path) -> None:
    headers = [
        "entry_id",
        "gl_date",
        "gl_account",
        "gl_account_name",
        "vendor",
        "amount",
        "invoice_ref",
        "memo",
    ]
    rows: list[list] = []

    # Trap lines
    traps = [
        (
            "JE-9001",
            "2025-08-14",
            "6210",
            "Repairs & Maintenance",
            "Summit Roofing LLC",
            ROOF_CAPITAL,
            "SR-4419",
            "Full roof replacement — south wing",
        ),
        (
            "JE-9002",
            "2025-05-22",
            "6225",
            "HVAC",
            "ClimateWorks Mechanical",
            HVAC_REPLACEMENT,
            "CW-2281",
            "Rooftop unit replacement RTU-3",
        ),
        (
            "JE-9003",
            "2025-03-18",
            "6300",
            "Property Insurance",
            "Midwest Mutual",
            INSURANCE,
            "MM-2025-PREM",
            "Annual property insurance premium",
        ),
        (
            "JE-9004",
            "2025-06-30",
            "6450",
            "Marketing & Promotions",
            "Commons Marketing Co-op",
            MARKETING,
            "MKT-2025-Q2",
            "Center-wide promo and events",
        ),
        (
            "JE-9005",
            "2025-04-09",
            "6150",
            "Landscaping",
            "GreenRibbon Grounds",
            DUP_LANDSCAPING,
            "EXP-4482",
            "Spring plantings — frontage",
        ),
        (
            "JE-9006",
            "2025-04-11",
            "6150",
            "Landscaping",
            "GreenRibbon Grounds",
            DUP_LANDSCAPING,
            "EXP-4482",
            "Spring plantings — frontage (repost)",
        ),
    ]
    rows.extend(traps)

    eligible_categories = [
        ("6110", "Common Area Electric", "Buckeye Power"),
        ("6120", "Common Water/Sewer", "City of Columbus Utilities"),
        ("6130", "Trash Removal", "Republic Waste"),
        ("6140", "Snow Removal", "Northland Plow"),
        ("6150", "Landscaping", "GreenRibbon Grounds"),
        ("6160", "Parking Lot Maintenance", "Asphalt Partners OH"),
        ("6170", "Janitorial Common", "Sparkle Commons"),
        ("6180", "Security Patrol", "Watchline Security"),
        ("6190", "Fire Monitoring", "AlertNet"),
        ("6225", "HVAC", "ClimateWorks Mechanical"),
    ]

    # Filler sums to TARGET - one kept landscaping invoice (JE-9005), so pool = TARGET after dropping JE-9006.
    n = 36
    keep_dup = DUP_LANDSCAPING
    filler_total = round(TARGET_ELIGIBLE_POOL - keep_dup, 2)
    weights = [rng.uniform(0.5, 1.5) for _ in range(n)]
    s = sum(weights)
    amounts = [round(filler_total * w / s, 2) for w in weights]
    amounts[-1] = round(filler_total - sum(amounts[:-1]), 2)

    for i, amt in enumerate(amounts):
        gl, name, vendor = eligible_categories[i % len(eligible_categories)]
        month = 1 + (i % 12)
        day = 5 + (i % 20)
        memo = "Contract service"
        if gl == "6225" and i % 7 == 0:
            memo = "Quarterly HVAC service agreement"
        rows.append(
            [
                f"JE-{9100 + i}",
                f"2025-{month:02d}-{day:02d}",
                gl,
                name,
                vendor,
                amt,
                f"INV-{5200 + i}",
                memo,
            ]
        )

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def write_lease_abstracts(path: Path) -> None:
    wb = Workbook()
    bold = Font(bold=True)

    sched = wb.active
    sched.title = "Suite Schedule"
    sched.append(["Meridian Commons — Lease Abstract Extract (as of 2025-12-31)"])
    sched.append([])
    headers = [
        "suite",
        "tenant",
        "gla_sf",
        "prorata_pct",
        "lease_start",
        "status",
        "notes",
    ]
    sched.append(headers)
    for c in sched[3]:
        c.font = bold

    starts = {
        "T-101": "2021-03-01",
        "T-104": "2019-08-15",
        "T-107": "2020-11-01",
        "T-112": "2022-02-01",
        "T-118": "2018-06-01",
        "T-122": "n/a",
    }
    for t in TENANTS:
        status = "Vacant" if t.get("vacant") else "Occupied"
        note = ""
        if t["suite"] == "T-118":
            note = (
                f"Expanded {t['expansion_date']}: prorata was {t['prorata_pct_h1']}% "
                f"through 2025-06-30; {t['prorata_pct']}% from 2025-07-01"
            )
        if t.get("vacant"):
            note = "Dark since 2025-03-01; GLA held in vacancy"
        sched.append(
            [
                t["suite"],
                t["tenant"],
                t["gla_sf"],
                t["prorata_pct"],
                starts[t["suite"]],
                status,
                note,
            ]
        )

    cam = wb.create_sheet("CAM Provisions")
    cam.append(["suite", "tenant", "cam_cap_psf", "includes_marketing", "vacancy_clause", "provision_text"])
    for c in cam[1]:
        c.font = bold
    for t in TENANTS:
        if t.get("vacant"):
            continue
        cap = "" if t["cam_cap_psf"] is None else t["cam_cap_psf"]
        if t["vacancy_clause"] == "owner_absorbs":
            vac_text = (
                "Landlord absorbs vacant GLA; Tenant's share is not grossed up for vacancy."
            )
        else:
            vac_text = (
                "Tenant's pro-rata share is recalculated excluding vacant GLA so remaining "
                "tenants absorb vacancy cost."
            )
        mkt = "Yes — marketing/promo in CAM definition" if t["includes_marketing"] else "No — marketing excluded from CAM"
        cap_txt = (
            f"Absolute CAM cap ${t['cam_cap_psf']:.2f}/SF on suite GLA"
            if t["cam_cap_psf"]
            else "No absolute CAM dollar cap"
        )
        cam.append(
            [
                t["suite"],
                t["tenant"],
                cap,
                "Y" if t["includes_marketing"] else "N",
                t["vacancy_clause"],
                f"{cap_txt}. {mkt}. {vac_text}",
            ]
        )

    notes = wb.create_sheet("Abstract Notes")
    notes.append(["topic", "detail"])
    for c in notes[1]:
        c.font = bold
    note_rows = [
        (
            "Expansion area",
            "Contour Fitness expansion occupied former storage bay counted in Contour GLA from 2025-07-01; "
            "H1 unleased expansion share (8.9%) treated as vacancy/owner-held for H1 allocation only.",
        ),
        (
            "Insurance",
            "Property insurance is billed under a separate lease exhibit and is not part of CAM.",
        ),
        (
            "Capital vs R&M",
            "Roof replacements and HVAC unit replacements are landlord capital and excluded from CAM "
            "regardless of GL coding.",
        ),
        (
            "Marketing",
            "Only Meridian Outfitters' lease includes center marketing in CAM; other leases exclude it.",
        ),
        (
            "True-up timing",
            "Annual CAM true-up is calculated on calendar-year actuals after December close; "
            "monthly estimates are interim only.",
        ),
        (
            "GLA basis",
            "Pro-rata percentages are fixed in each lease and may differ slightly from raw GLA "
            "arithmetic after prior amendments; use the abstract prorata_pct column.",
        ),
        (
            "Vacancy start",
            "Suite T-122 went dark 2025-03-01. For annual CAM modeling treat the suite as vacant "
            "for the full true-up year unless a lease says otherwise.",
        ),
        (
            "Cap measurement",
            "Absolute CAM caps are tested on the final annual CAM charge including any "
            "tenant-specific inclusions such as marketing add-ons.",
        ),
        (
            "Duplicate costs",
            "If the same vendor invoice reference appears twice in the expense extract, count it once.",
        ),
        (
            "Owner absorption",
            "Where vacancy_clause is owner_absorbs, do not gross up that tenant for vacant GLA.",
        ),
    ]
    for row in note_rows:
        notes.append(list(row))

    # Extra depth: monthly share history for Contour
    hist = wb.create_sheet("Share History")
    hist.append(["suite", "tenant", "effective_from", "effective_to", "prorata_pct", "event"])
    for c in hist[1]:
        c.font = bold
    for t in TENANTS:
        if t.get("vacant"):
            hist.append([t["suite"], t["tenant"], "2025-03-01", "2025-12-31", t["prorata_pct"], "Vacant"])
            continue
        if t["suite"] == "T-118":
            hist.append([t["suite"], t["tenant"], "2025-01-01", "2025-06-30", t["prorata_pct_h1"], "Pre-expansion"])
            hist.append([t["suite"], t["tenant"], "2025-07-01", "2025-12-31", t["prorata_pct"], "Post-expansion"])
        else:
            hist.append([t["suite"], t["tenant"], "2025-01-01", "2025-12-31", t["prorata_pct"], "No change"])
    # Pad with prior-year reference rows for depth
    for year in (2023, 2024):
        for t in TENANTS:
            if t.get("vacant"):
                continue
            pct = t.get("prorata_pct_h1", t["prorata_pct"]) if t["suite"] == "T-118" else t["prorata_pct"]
            hist.append([t["suite"], t["tenant"], f"{year}-01-01", f"{year}-12-31", pct, f"{year} reference"])

    wb.save(path)


def write_billing_register(path: Path) -> None:
    text = """MERIDIAN PROPERTY GROUP — PROPERTY ACCOUNTING
Meridian Commons CAM Estimated Billing Register — Calendar Year 2025
Prepared by: A. Nguyen, Property Accountant
As of: 2025-12-28

Purpose
This register summarizes estimated common-area maintenance charges billed to occupied
tenants during 2025. Estimates were set in January from the 2024 CAM pool forecast and
were not formally reforecast after the Contour Fitness expansion. Controllers asked for
this extract ahead of the year-end true-up so allocated actuals can be compared to cash
already collected through monthly CAM invoices.

Billing policy used in 2025
Monthly CAM invoices equal one-twelfth of each tenant's estimated annual CAM charge.
Estimated annual charges used January pro-rata shares from the lease abstract in effect
on 2025-01-01. Contour Fitness expanded on 2025-07-01; the billing system was never
updated, so Contour continued to receive invoices based on its pre-expansion 18.2% share
for July through December. No mid-year catch-up invoice was issued.

Tenant estimated CAM billed (annual total invoiced in 2025)

Suite T-101 Harbor Coffee Co — billed $43,200.00
Suite T-104 Ridgeway Dental — billed $13,774.00 (estimate held at the lease CAM cap)
Suite T-107 Meridian Outfitters — billed $98,400.00
Suite T-112 Lakeside Books — billed $46,800.00 (billing alias on two invoices shows "Lakeside Bookshop"; same TIN)
Suite T-118 Contour Fitness — billed $92,160.00 (entire year at 18.2% share)

Suite T-122 remained vacant after March and was not billed.

Open items for Controllers
1. Contour expansion documentation is on the lease abstract workbook; billing did not follow it.
2. Ridgeway Dental's estimate already sits at the $4.85/SF cap on 2,840 SF ($13,774). Confirm whether
   actual allocation before cap still exceeds that figure.
3. Marketing co-op invoices hit GL 6450; confirm whether any tenant lease pulls marketing into CAM.
4. Large roof and HVAC replacement invoices hit R&M and HVAC accounts; confirm capital exclusions
   before tenant true-ups are issued.

Totals above are billed amounts only. Do not treat them as the final CAM pool or as approved
true-up figures. The true-up workbook should recompute eligible expenses from the GL extract and
apply current lease economics from the abstract file.
"""
    # Verify PRIOR_BILLINGS alignment
    assert PRIOR_BILLINGS["T-101"] == 43200.00
    path.write_text(text, encoding="utf-8")


def main() -> None:
    TASK.mkdir(parents=True, exist_ok=True)
    write_expense_ledger(TASK / "meridian_commons_expense_ledger.csv")
    write_lease_abstracts(TASK / "tenant_lease_abstracts.xlsx")
    write_billing_register(TASK / "prior_cam_billing_register.txt")
    print(f"Wrote CAM inputs to {TASK}")


if __name__ == "__main__":
    main()
