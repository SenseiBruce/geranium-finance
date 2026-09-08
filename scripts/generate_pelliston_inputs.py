#!/usr/bin/env python3
"""Generate inputs for Pelliston self-insured WC reserve (attempt 2)."""

from __future__ import annotations

import csv
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from pelliston_constants import (
    BEGINNING_RESERVE,
    CLAIM_LARGE,
    CLAIM_LARGE_CASE,
    CLAIM_LARGE_PAID_YTD,
    CLAIM_SUBRO,
    CLAIM_SUBRO_CASE,
    CLAIM_SUBRO_EXPECTED,
    FEIN,
    IBNR_FACTORS,
    PELLISTON,
    POLICY_SI,
    RETENTION,
    SLUG,
    STALE_2025_FACTOR,
)

TASK_INPUTS = Path(__file__).resolve().parent.parent / "tasks" / SLUG / "inputs"
rng = random.Random(20260904)


def money(x: float) -> float:
    return round(float(x), 2)


def write_payment_ledger(path: Path) -> None:
    headers = [
        "payment_id",
        "payment_date",
        "claim_number",
        "accident_year",
        "claimant",
        "payment_type",
        "amount",
        "check_ref",
        "memo",
    ]
    rows: list[list] = []
    pid = 1

    # Open / active claims payment history (irregular)
    claims = [
        ("CLM-2022-0198", 2022, "R. Kessler", [12_420.18, 8_110.40, 3_220.55]),
        ("CLM-2022-0311", 2022, "J. Okonkwo", [22_840.22, 6_480.00]),
        ("CLM-2023-0088", 2023, "A. Nguyen", [18_220.40, 14_880.15, 9_410.22, 4_120.00]),
        ("CLM-2023-0275", 2023, "S. Patel", [31_640.18, 12_200.55, 7_880.40]),
        (CLAIM_SUBRO, 2023, "M. Ortega", [28_400.00, 15_220.18, 9_880.40]),
        ("CLM-2024-0044", 2024, "L. Briggs", [24_110.22, 18_640.55, 11_200.18, 6_480.40]),
        ("CLM-2024-0612", 2024, "K. Chen", [16_880.40, 9_220.18, 5_410.00]),
        (CLAIM_LARGE, 2024, "D. Vasquez", [42_200.18, 28_110.00, 18_110.00]),  # sum ~88,420
        ("CLM-2025-0012", 2025, "T. Quinn", [8_420.18, 6_110.40, 4_880.22]),
        ("CLM-2025-0188", 2025, "N. Blake", [12_640.55, 9_220.18]),
        ("CLM-2025-0330", 2025, "H. Park", [5_880.40, 3_210.15, 2_640.00]),
        ("CLM-2025-0419", 2025, "I. Mendel", [7_220.18]),
    ]

    months = list(range(1, 13))
    for claim, ay, claimant, pays in claims:
        # Force large-loss paid total
        if claim == CLAIM_LARGE:
            pays = [42_200.18, 28_110.00, money(CLAIM_LARGE_PAID_YTD - 42_200.18 - 28_110.00)]
        for i, amt in enumerate(pays):
            mo = months[(hash(claim) + i * 3) % 12]
            day = 5 + (i * 7) % 20
            rows.append(
                [
                    f"PAY-{pid:04d}",
                    f"{ay if ay < 2025 else 2025}-{mo:02d}-{day:02d}" if ay == 2025 else f"2025-{mo:02d}-{day:02d}",
                    claim,
                    ay,
                    claimant,
                    "Indemnity" if i % 2 == 0 else "Medical",
                    f"{money(amt):.2f}",
                    f"CHK-{8000 + pid}",
                    "TPA weekly funding",
                ]
            )
            pid += 1

    # Closed claim still lingering in open inventory — final payment Dec
    rows.append(
        [
            f"PAY-{pid:04d}",
            "2025-12-18",
            "CLM-2024-0901",
            2024,
            "C. Delgado",
            "Indemnity",
            "2140.55",
            f"CHK-{8000 + pid}",
            "Final indemnity — claim closed",
        ]
    )
    pid += 1
    rows.append(
        [
            f"PAY-{pid:04d}",
            "2025-12-18",
            "CLM-2024-0901",
            2024,
            "C. Delgado",
            "Medical",
            "880.20",
            f"CHK-{8000 + pid}",
            "Final medical — claim closed",
        ]
    )
    pid += 1

    # Voided duplicate check
    rows.append(
        [
            f"PAY-{pid:04d}",
            "2025-08-14",
            "CLM-2025-0012",
            2025,
            "T. Quinn",
            "Medical",
            "1880.40",
            "CHK-VOID-441",
            "VOID — duplicate of CHK-8041; do not count",
        ]
    )
    pid += 1
    rows.append(
        [
            f"PAY-{pid:04d}",
            "2025-08-15",
            "CLM-2025-0012",
            2025,
            "T. Quinn",
            "Medical",
            "-1880.40",
            "CHK-VOID-441R",
            "Reversal of VOID duplicate",
        ]
    )
    pid += 1

    # Fill depth with smaller AY2022–2025 payments
    extras = [
        ("CLM-2022-0402", 2022, "P. Nanda", 4_220.18),
        ("CLM-2022-0402", 2022, "P. Nanda", 2_110.40),
        ("CLM-2023-0510", 2023, "E. Soto", 6_840.22),
        ("CLM-2023-0510", 2023, "E. Soto", 3_220.15),
        ("CLM-2024-0777", 2024, "B. Mooney", 9_110.40),
        ("CLM-2024-0777", 2024, "B. Mooney", 4_880.18),
        ("CLM-2024-0777", 2024, "B. Mooney", 2_640.55),
        ("CLM-2025-0502", 2025, "F. Noor", 3_420.18),
        ("CLM-2025-0502", 2025, "F. Noor", 1_880.40),
        ("CLM-2025-0555", 2025, "G. Alvarez", 2_640.22),
    ]
    for claim, ay, claimant, amt in extras:
        mo = rng.randint(1, 12)
        rows.append(
            [
                f"PAY-{pid:04d}",
                f"2025-{mo:02d}-{rng.randint(3, 27):02d}",
                claim,
                ay,
                claimant,
                "Medical" if pid % 2 else "Indemnity",
                f"{money(amt):.2f}",
                f"CHK-{8000 + pid}",
                "TPA weekly funding",
            ]
        )
        pid += 1

    # Aged residual payments on closed / residual claims (realistic claimant labels)
    aged_claimants = [
        "W. Harlan",
        "M. Duarte",
        "S. Kowalski",
        "J. Belmont",
        "A. Freitag",
        "C. Yuen",
        "D. McBride",
        "L. Sabatini",
        "R. Holcomb",
        "T. Ibarra",
        "E. Dunlap",
        "N. Varela",
        "P. Okafor",
        "H. Lindgren",
        "B. Castor",
        "K. Mendez",
        "F. Whitaker",
        "G. Ramos",
        "I. Sheffield",
        "O. Banerjee",
        "U. Carmichael",
        "V. Horton",
        "Y. Petrov",
        "Z. Quintero",
        "Q. Ambrose",
        "X. Navarro",
        "S. Redding",
        "J. Pfeiffer",
        "M. Solano",
        "A. Beckett",
        "C. Unger",
        "D. Farley",
        "L. Cho",
        "R. Estes",
        "T. Gagnon",
        "E. Prado",
        "N. Ashford",
        "P. Rhee",
        "H. Boone",
        "B. Langston",
    ]
    for i in range(40):
        ay = 2022 + (i % 4)
        claim = f"CLM-{ay}-{6000 + i}"
        amt = money(800 + rng.random() * 4200)
        rows.append(
            [
                f"PAY-{pid:04d}",
                f"2025-{(i % 12) + 1:02d}-{(i % 25) + 2:02d}",
                claim,
                ay,
                aged_claimants[i],
                "Indemnity" if i % 3 else "Medical",
                f"{amt:.2f}",
                f"CHK-{9000 + pid}",
                "Aged claim residual payment",
            ]
        )
        pid += 1

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def write_open_triangle(path: Path) -> None:
    wb = Workbook()

    # Open Inventory
    ws = wb.active
    ws.title = "Open Inventory"
    headers = [
        "claim_number",
        "accident_year",
        "claimant",
        "status",
        "case_reserve",
        "paid_to_date",
        "subrogation_flag",
        "expected_subrogation",
        "notes",
    ]
    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True)

    inventory = [
        ("CLM-2022-0198", 2022, "R. Kessler", "Open", 18_400.00, 23_751.13, "N", 0, ""),
        ("CLM-2022-0311", 2022, "J. Okonkwo", "Open", 8_220.40, 29_320.22, "N", 0, ""),
        ("CLM-2022-0402", 2022, "P. Nanda", "Open", 4_110.18, 6_330.58, "N", 0, ""),
        ("CLM-2023-0088", 2023, "A. Nguyen", "Open", 22_640.55, 46_630.77, "N", 0, ""),
        ("CLM-2023-0275", 2023, "S. Patel", "Open", 31_200.18, 51_721.13, "N", 0, ""),
        (
            CLAIM_SUBRO,
            2023,
            "M. Ortega",
            "Open",
            CLAIM_SUBRO_CASE,
            53_500.58,
            "Y",
            CLAIM_SUBRO_EXPECTED,
            "Third-party recovery expected; not yet received",
        ),
        ("CLM-2023-0510", 2023, "E. Soto", "Open", 12_880.40, 10_060.37, "N", 0, ""),
        ("CLM-2024-0044", 2024, "L. Briggs", "Open", 48_220.18, 60_431.35, "N", 0, ""),
        ("CLM-2024-0612", 2024, "K. Chen", "Open", 27_640.55, 31_510.58, "N", 0, ""),
        (
            CLAIM_LARGE,
            2024,
            "D. Vasquez",
            "Open",
            CLAIM_LARGE_CASE,
            CLAIM_LARGE_PAID_YTD,
            "N",
            0,
            "Catastrophic machine-guarding injury — TPA case exceeds SI retention",
        ),
        ("CLM-2024-0777", 2024, "B. Mooney", "Open", 19_420.18, 16_631.13, "N", 0, ""),
        (
            "CLM-2024-0901",
            2024,
            "C. Delgado",
            "Open",
            6_400.00,
            18_220.40,
            "N",
            0,
            "TPA still shows Open; ledger has December final payments",
        ),
        ("CLM-2025-0012", 2025, "T. Quinn", "Open", 34_880.22, 19_410.80, "N", 0, ""),
        ("CLM-2025-0188", 2025, "N. Blake", "Open", 28_640.18, 21_860.73, "N", 0, ""),
        ("CLM-2025-0330", 2025, "H. Park", "Open", 22_110.40, 11_730.55, "N", 0, ""),
        ("CLM-2025-0419", 2025, "I. Mendel", "Open", 41_200.18, 7_220.18, "N", 0, ""),
        ("CLM-2025-0502", 2025, "F. Noor", "Open", 18_420.55, 5_300.58, "N", 0, ""),
        ("CLM-2025-0555", 2025, "G. Alvarez", "Open", 15_880.40, 2_640.22, "N", 0, ""),
    ]
    for row in inventory:
        ws.append(
            [
                row[0],
                row[1],
                row[2],
                row[3],
                money(row[4]),
                money(row[5]),
                row[6],
                money(row[7]) if row[7] else 0,
                row[8],
            ]
        )

    # AY Triangle — cumulative paid by development year (simplified)
    wt = wb.create_sheet("AY Triangle")
    wt.append(
        [
            "accident_year",
            "dev_12",
            "dev_24",
            "dev_36",
            "dev_48",
            "cumulative_paid_as_of_2025_12",
            "notes",
        ]
    )
    for c in wt[1]:
        c.font = Font(bold=True)
    triangle = [
        (2022, 84_220.18, 112_480.40, 128_640.22, 136_220.55, 136_220.55, "Mature"),
        (2023, 96_480.40, 148_220.18, 172_640.55, "", 172_640.55, "Developing"),
        (2024, 118_640.22, 186_420.18, "", "", 186_420.18, "Includes large loss paid portion"),
        (2025, 68_220.40, "", "", "", 68_220.40, "Immature current year"),
    ]
    for r in triangle:
        wt.append(list(r))

    wd = wb.create_sheet("Definitions")
    wd.append(["term", "definition"])
    for c in wd[1]:
        c.font = Font(bold=True)
    defs = [
        ("case_reserve", "TPA outstanding case estimate at 2025-12-31 before SI retention cap"),
        ("paid_to_date", "Cumulative indemnity + medical paid on the claim through 2025-12-31"),
        ("status Open", "TPA open inventory; Controllers must reconcile to ledger closures"),
        ("VOID payments", "Paired positive/negative VOID rows net to zero; exclude from incurred analysis"),
        ("subrogation_flag Y", "Third-party recovery pursued; see actuarial memo for booking rule"),
        ("SI retention", "See actuarial_funding_memo.txt — not restated here to avoid dual sources"),
        ("Named insured", f"{PELLISTON} FEIN {FEIN} policy {POLICY_SI}"),
    ]
    for a, b in defs:
        wd.append([a, b])

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def write_memo(path: Path) -> None:
    # Keep in sync with tasks/.../inputs/actuarial_funding_memo.txt
    text = f"""
NORTH RIVER ACTUARIAL CONSULTING
Self-Insured Workers Compensation — Year-End Funding Memo
Insured: {PELLISTON} | FEIN {FEIN} | Program {POLICY_SI}
Valuation date: 2025-12-31 | Issued: 2026-01-12 | Attention: Controllers

PURPOSE
This memo governs the calendar-year 2025 self-insured workers compensation reserve Controllers will book for external audit and the bank borrowing-base certificate. Source data for Controllers are pelliston_claims_payment_ledger.csv (cash payments and voids) and pelliston_open_claims_triangle.xlsx (Open Inventory of open claims plus the AY Triangle of accident-year cumulative paid). Where TPA case estimates and this memo conflict on retention, IBNR factors, or subrogation, this memo controls.

SELF-INSURED RETENTION
{PELLISTON} retains the first ${RETENTION:,.2f} of loss and allocated loss adjustment expense per occurrence. Cap each claim's self-insured case reserve at the lesser of the TPA case estimate and ${RETENTION:,.2f}. Amounts above the retention are recoverable from the excess carrier and must not remain in the self-insured case reserve on Controllers' SI liability. For claim {CLAIM_LARGE}, the TPA case reserve of ${CLAIM_LARGE_CASE:,.2f} exceeds the retention. Cap the SI case portion at ${RETENTION:,.2f}. Record the uncapped excess as ceded / excess recoverable for disclosure, not as SI liability. Keep the retention limit in a central assumptions area and reference it in the case inventory.

BEGINNING RESERVE
The audited self-insured reserve at 2024-12-31 was ${BEGINNING_RESERVE:,.2f} (case plus IBNR combined). Use that figure as the opening balance in the 2025 rollforward. Do not rebuild 2024 from the current triangle.

CUMULATIVE PAID FOR IBNR
Apply IBNR factors to (cumulative paid_to_date + SI case reserve after retention caps) by accident year. Cumulative paid_to_date for this calculation means accident-year lifetime paid through 2025-12-31 for the full AY population, including closed claims. That measure is on the AY Triangle sheet as cumulative_paid_as_of_2025_12. Open Inventory paid_to_date is claim-level detail for open claims only and is not a substitute for AY-level cumulative paid on mature years, where closed-claim payments sit outside the open subset. If Open Inventory open-claim paid for an accident year exceeds the Triangle's AY cumulative paid, Controllers must document the conflict, select the Triangle as the AY-level paid source for IBNR, and note that the two figures cannot both be literal cumulative measures of the same population. Do not invent a bridge the source workbook does not provide.

IBNR FACTORS BY ACCIDENT YEAR
Factors are expressed as IBNR divided by (cumulative paid + SI case). Use:

Accident year 2022: {IBNR_FACTORS[2022]:.2f}
Accident year 2023: {IBNR_FACTORS[2023]:.2f}
Accident year 2024: {IBNR_FACTORS[2024]:.2f}
Accident year 2025: {IBNR_FACTORS[2025]:.2f}

A mid-year 2025 planning exhibit used factor {STALE_2025_FACTOR:.2f} for accident year 2025. That exhibit is superseded. Do not use {STALE_2025_FACTOR:.2f} for year-end funding. Factors come from North River's Ohio manufacturing SI development study for similar retention programs; cite this memo and keep the four factors in the workpaper assumptions area.

CLOSED CLAIMS STILL SHOWN OPEN
Claim CLM-2024-0901 appears on the Open Inventory with a case reserve, but the payment ledger shows final indemnity and medical on 2025-12-18 with a closed memo. Remove CLM-2024-0901 from the SI case inventory (case = 0). Do not carry its leftover TPA case into the reserve. Closed claims remain in the AY Triangle cumulative paid totals; they should not be double-counted as open case.

SUBROGATION
Claim {CLAIM_SUBRO} shows expected subrogation of ${CLAIM_SUBRO_EXPECTED:,.2f}. Controllers' policy and this funding memo require recognition only when cash is received. Do not reduce case reserves or IBNR for expected recoveries that remain unpaid at valuation date. Keep the SI case at ${CLAIM_SUBRO_CASE:,.2f} without a subrogation credit.

VOIDS
Paired VOID and reversal rows in the payment ledger net to zero. Exclude them from paid totals used in the rollforward paid leg. Net calendar-year 2025 paid for the rollforward comes from the ledger after that exclusion.

ROLLFORWARD STRUCTURE
Ending SI reserve = SI case reserves (after retention caps and closed-claim removals) + IBNR by accident year.
Rollforward identity Controllers should show: Beginning reserve + Net incurred − Net paid = Ending reserve.
Net paid is calendar-year 2025 payments from the ledger excluding void pairs. Net incurred is the plug that makes the identity hold once ending reserve is computed from case + IBNR.

DOCUMENTATION EXPECTATIONS
The Controllers workpaper should be formula-driven where amounts are derived: retention-capped case = MIN(TPA case, retention), IBNR = IBNR base × factor, and rollforward ending balances linked to case and IBNR totals. Centralize the retention, beginning reserve, and IBNR factors. Cite actuarial_funding_memo.txt, the AY Triangle, and the Open Inventory wherever source choice or memo treatment drives a booking decision. Document any material cross-file conflict (including AY2024 paid) on a Notes or methodology tab.

CONTROLLER DELIVERABLE
Produce self_insured_wc_reserve_pelliston.xlsx with a retention-capped case inventory, accident-year IBNR, excess/ceded bridge for the large loss, a rollforward to 2025-12-31, and a short recommendation Controllers can drop into the audit PBC and bank certificate pack. Do not rewrite excess policy wording; flag the recoverable only.

DISTRIBUTION
Controllers, CFO, external audit PBC folder, lender reporting pack. Not for TPA redistribution.
""".strip()
    path.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    # Remove obsolete attempt-1 files
    TASK_INPUTS.mkdir(parents=True, exist_ok=True)
    for stale in TASK_INPUTS.glob("*"):
        if stale.is_file():
            stale.unlink()
    write_payment_ledger(TASK_INPUTS / "pelliston_claims_payment_ledger.csv")
    write_open_triangle(TASK_INPUTS / "pelliston_open_claims_triangle.xlsx")
    write_memo(TASK_INPUTS / "actuarial_funding_memo.txt")
    print(f"Wrote attempt-2 inputs to {TASK_INPUTS}")
    print(f"words={len((TASK_INPUTS / 'actuarial_funding_memo.txt').read_text().split())}")


if __name__ == "__main__":
    main()
