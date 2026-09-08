#!/usr/bin/env python3
"""Generate input files for granite-ridge-oct-renewal-desk."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

TASK = Path(__file__).resolve().parent.parent / "tasks" / "granite-ridge-oct-renewal-desk" / "inputs"
random.seed(20261001)

EFFECTIVE = date(2025, 10, 1)

ACCOUNT_IDS = [
    "GR-2001", "GR-2004", "GR-2007", "GR-2010", "GR-2013", "GR-2016", "GR-2018", "GR-2021",
    "GR-2024", "GR-2027", "GR-2030", "GR-2033", "GR-2036", "GR-2039", "GR-2042", "GR-2045",
    "GR-2047", "GR-2050", "GR-2053", "GR-2056", "GR-2059", "GR-2062", "GR-2065", "GR-2068",
    "GR-2071", "GR-2074", "GR-2077", "GR-2080", "GR-2083", "GR-2086", "GR-2089", "GR-2092",
    "GR-2113", "GR-2162", "GR-2195", "GR-2200",
]

CITY_STATE = {
    "Columbus": "OH",
    "Chicago": "IL",
    "Indianapolis": "IN",
    "Madison": "WI",
    "Des Moines": "IA",
    "Peoria": "IL",
    "Cleveland": "OH",
    "Minneapolis": "MN",
    "Kansas City": "MO",
    "Grand Rapids": "MI",
}

STATES = list({s for s in CITY_STATE.values()})
# One unique insured per account index (36 names). Student-housing trade name applied separately.
NAMES = [
    "Ashland Court Apts LP",
    "Berwyn Arms LLC",
    "Campus Edge Housing Co.",  # GR-2007
    "Damen Square Residences",
    "Eastgate Manor LLC",
    "Fairmount Village Apts",
    "Glenwood Terrace LLC",
    "Halsted Walkup Partners",
    "Irving Park Rentals Inc",
    "Jefferson Grove MF LLC",
    "Kenwood Station Apts",
    "Lincolnwood Place LLC",
    "Monon Trail Residences",
    "Norwood Court Apts",
    "Ottawa River Flats",
    "Pullman Yard Housing",
    "Quincy Street Apts LLC",
    "Ravenswood Arms Co.",
    "Southport Lane LLC",
    "Troy Hill Apartments",
    "Union Depot Lofts LLC",
    "Vernon Park Residences",
    "Campus Edge Housing Co.",  # GR-2065 — same student-housing sponsor, second policy
    "Westchester Court LLC",
    "Buckeye Garden Apts LLC",
    "Yorktown Flats LLC",
    "Zion Road Residences",
    "Archer Avenue Apts LLC",
    "Belmont Court Partners",
    "Cermak Place LLC",
    "Devonshire Arms LLC",
    "Elston Crossing Apts",
    "Fulton Market Residences",
    "Grandview Portfolio LLC",
    "Humboldt Yard Apts LLC",
    "Indiana Ave Partners LLC",
]

# Explicit student-housing accounts under Campus Edge (Section 10)
STUDENT_HOUSING_ACCOUNTS = {"GR-2007", "GR-2065"}

INSPECTION_EXPIRED = "2025-04-02"

# paid / reserved pairs keep intentional incurred totals; reserve shares vary by claim stage.
ACCOUNT_LOSS_OVERRIDES: dict[str, list[tuple[str, float, float, str, str]]] = {
    "GR-2018": [("HAB-2018-A", 4860.00, 540.00, "Slip-Fall", "2024-05-09")],  # nearly closed
    "GR-2047": [("HAB-2047-A", 3600.00, 1200.00, "Water", "2024-02-18")],  # moderate
    "GR-2113": [
        ("HAB-2113-A", 5560.00, 2400.00, "Theft", "2024-07-03"),  # developing
        ("HAB-2113-B", 4980.00, 0.00, "GL", "2024-11-21"),  # paid-only
    ],
    "GR-2162": [
        ("HAB-2162-A", 5240.00, 0.00, "Slip-Fall", "2024-03-27"),  # paid-only
        ("HAB-2162-C", 187640.00, 72480.00, "Fire", "2024-09-14"),  # large open fire
    ],
    "GR-2195": [
        ("HAB-2195-A", 31840.00, 11220.00, "Fire", "2024-08-02"),
        ("HAB-2195-A", 22680.00, 0.00, "Water", "2024-04-11"),
        ("HAB-2195-B", 28440.00, 18620.00, "Wind", "2024-10-19"),
        ("HAB-2195-B", 19880.00, 9420.00, "Slip-Fall", "2024-01-06"),
    ],
    "GR-2089": [("HAB-2089-A", 6580.00, 2840.00, "Water", "2024-06-28")],  # substantial reserve
    "GR-2033": [("HAB-2033-B", 6120.00, 0.00, "Slip-Fall", "2024-08-30")],  # paid-only
}

# Reserve as share of incurred — cycles so rows are not a uniform paid/reserve formula.
RESERVE_SHARE_PROFILES = (
    0.00,  # closed / paid-only
    0.04,  # nearly closed
    0.11,  # low remaining reserve
    0.18,  # maturing
    0.27,  # moderate outstanding
    0.41,  # developing
    0.58,  # newer claim, larger case reserve
    0.72,  # recently reserved / heavy outstanding
)


def random_loss_date() -> str:
    start = date(2023, 10, 15)
    end = date(2025, 8, 30)
    span = (end - start).days
    return (start + timedelta(days=random.randint(0, span))).isoformat()


def inspection_date_for(acct: str, loc_index: int) -> tuple[str, str]:
    if acct == "GR-2089" and loc_index == 0:
        return INSPECTION_EXPIRED, INSPECTION_EXPIRED
    offset = random.randint(8, 28)
    insp = (EFFECTIVE - timedelta(days=offset)).isoformat()
    alarm_offset = random.randint(8, 28)
    alarm = (EFFECTIVE - timedelta(days=alarm_offset)).isoformat()
    return insp, alarm


def write_accounts(path: Path) -> None:
    rows = []
    for i, acct in enumerate(ACCOUNT_IDS):
        premium = round(random.uniform(42000, 98000), 2)
        tiv = round(random.uniform(8200000, 18400000), 0)
        units = random.randint(48, 186)
        occ = round(random.uniform(91.0, 98.5), 1)
        lr = round(random.uniform(12.0, 34.0), 1)
        subsidized = "N"
        prior = "Quoted"
        renewal_ready = "Y"

        if acct == "GR-2018":
            premium, tiv, units, occ, lr = 54820.00, 9340000, 112, 97.2, 18.6
        elif acct == "GR-2047":
            premium, tiv, units, occ, lr = 61240.00, 10280000, 128, 94.0, 21.3
        elif acct == "GR-2113":
            premium, tiv, units, occ, lr = 78450.00, 11840000, 142, 96.1, 28.4
        elif acct == "GR-2089":
            premium, tiv, units, occ, lr, prior = 67380.00, 8960000, 96, 95.8, 24.7, "Renewal Ready"
        elif acct == "GR-2162":
            # Large 3-building portfolio: elevated premium justified by TIV/units (keeps LR < 70% with $260k fire)
            premium, tiv, units, occ, lr = 392850.00, 48260000, 412, 93.4, 31.8
        elif acct == "GR-2195":
            premium, tiv, units, occ, lr = 48620.00, 7420000, 88, 92.6, 48.2
        elif acct == "GR-2033":
            premium, tiv, units, occ, lr = 52180.00, 6840000, 72, 88.4, 19.2
        elif acct == "GR-2071":
            premium, tiv, units, occ, lr = 49959.06, 9120000, 104, 95.1, 14.8

        if acct in {"GR-2053", "GR-2068", "GR-2092"}:
            subsidized = "Y"

        insured = NAMES[i]
        # Placeholder state; write_locations overwrites account state from the location schedule.
        city = random.choice(list(CITY_STATE.keys()))
        rows.append({
            "account_id": acct,
            "named_insured": insured,
            "state": CITY_STATE[city],
            "expiring_premium": premium,
            "account_tiv": tiv,
            "unit_count": units,
            "occupancy_pct": occ,
            "subsidized_housing_flag": subsidized,
            "prior_disposition": prior,
            "account_loss_ratio_36mo": lr,
            "renewal_ready_flag": renewal_ready,
        })

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def _cities_for_state(state: str) -> list[str]:
    return [city for city, st in CITY_STATE.items() if st == state]


def write_locations(path: Path, accounts_path: Path) -> None:
    accounts = {r["account_id"]: r for r in csv.DictReader(accounts_path.open())}
    rows = []
    subsidized_patches = {
        "HAB-2053-A": ("Columbus", "OH", 24),
        "HAB-2068-B": ("Peoria", "IL", 18),
        "HAB-2092-A": ("Cleveland", "OH", 22),
    }
    # One home metro per account so account-level state matches every building.
    account_home_city = {acct: random.choice(list(CITY_STATE.keys())) for acct in ACCOUNT_IDS}
    account_home_city["GR-2053"] = "Columbus"
    account_home_city["GR-2068"] = "Peoria"
    account_home_city["GR-2092"] = "Cleveland"
    account_home_city["GR-2033"] = "Minneapolis"
    account_home_city["GR-2007"] = "Indianapolis"
    account_home_city["GR-2065"] = "Columbus"

    for acct in ACCOUNT_IDS:
        loc_count = 3 if acct in {"GR-2162", "GR-2113", "GR-2047"} else 2
        weights = [random.uniform(0.85, 1.15) for _ in range(loc_count)]
        account_tiv = float(accounts[acct]["account_tiv"])
        account_units = int(accounts[acct]["unit_count"])
        home_city = account_home_city[acct]
        home_state = CITY_STATE[home_city]
        peer_cities = _cities_for_state(home_state) or [home_city]

        if acct == "GR-2113":
            target_sum = account_tiv * 1.082
            target_units = account_units + 8
        elif acct == "GR-2047":
            target_sum = account_tiv * random.uniform(0.992, 1.008)
            target_units = account_units
        else:
            target_sum = account_tiv * random.uniform(0.985, 1.015)
            target_units = account_units

        scale = target_sum / sum(weights)
        unit_weights = [random.uniform(0.9, 1.1) for _ in range(loc_count)]
        unit_scale = target_units / sum(unit_weights)

        for n in range(loc_count):
            loc_id = f"HAB-{acct.split('-')[1]}-{chr(65 + n)}"
            city = home_city if n == 0 else random.choice(peer_cities)
            vacancy = "N"
            broker = "yes"
            sprinkler, fire_alarm = inspection_date_for(acct, n)
            pool = "N"
            subsidized_units = 0

            if acct == "GR-2047" and n == 1:
                vacancy = "Y"
            if acct == "GR-2033" and n == 1:
                vacancy = "Y"
                broker = "no"
            if acct == "GR-2074" and n == 0:
                pool = "pending_fence_po"

            rows.append({
                "location_id": loc_id,
                "account_id": acct,
                "address_city": city,
                "state": home_state,
                "building_tiv": round(weights[n] * scale, 0),
                "unit_count": max(1, round(unit_weights[n] * unit_scale)),
                "subsidized_unit_count": subsidized_units,
                "protection_class": random.choice(["2", "3", "4", "5"]),
                "vacancy_flag": vacancy,
                "sprinkler_inspection_date": sprinkler,
                "fire_alarm_inspection_date": fire_alarm,
                "pool_liability_flag": pool,
                "broker_confirmation": broker,
            })

    for r in rows:
        patch = subsidized_patches.get(r["location_id"])
        if patch:
            r["address_city"], r["state"], r["subsidized_unit_count"] = patch
            if int(r["subsidized_unit_count"]) > int(r["unit_count"]):
                r["unit_count"] = int(r["subsidized_unit_count"]) + random.randint(4, 12)

    # Align account-list state to the location schedule (same state for all buildings).
    account_rows = list(csv.DictReader(accounts_path.open()))
    loc_state_by_acct = {r["account_id"]: r["state"] for r in rows}
    for acct_row in account_rows:
        acct_row["state"] = loc_state_by_acct[acct_row["account_id"]]
    with accounts_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=account_rows[0].keys())
        w.writeheader()
        w.writerows(account_rows)

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def write_loss_run(path: Path, accounts_path: Path, locations_path: Path) -> None:
    accounts = {r["account_id"]: float(r["expiring_premium"]) for r in csv.DictReader(accounts_path.open())}
    loc_rows = list(csv.DictReader(locations_path.open()))
    loc_ids_by_acct: dict[str, list[str]] = {}
    for loc in loc_rows:
        loc_ids_by_acct.setdefault(loc["account_id"], []).append(loc["location_id"])

    rows = []
    loss_num = 1

    for acct in ACCOUNT_IDS:
        if acct in ACCOUNT_LOSS_OVERRIDES:
            for loc_id, paid, reserved, peril, loss_date in ACCOUNT_LOSS_OVERRIDES[acct]:
                rows.append({
                    "loss_id": f"LR-{loss_num:04d}",
                    "location_id": loc_id,
                    "account_id": acct,
                    "loss_date": loss_date,
                    "peril": peril,
                    "paid_amount": paid,
                    "reserved_amount": reserved,
                    "cat_code": "",
                })
                loss_num += 1
            continue
        premium = accounts[acct]
        target_incurred = round(premium * random.uniform(0.06, 0.28), 2)
        loc_id = loc_ids_by_acct[acct][0]
        reserve_share = RESERVE_SHARE_PROFILES[(loss_num - 1) % len(RESERVE_SHARE_PROFILES)]
        reserved = round(target_incurred * reserve_share, 2)
        paid = round(target_incurred - reserved, 2)
        rows.append({
            "loss_id": f"LR-{loss_num:04d}",
            "location_id": loc_id,
            "account_id": acct,
            "loss_date": random_loss_date(),
            "peril": random.choice(["Water", "Slip-Fall", "Theft"]),
            "paid_amount": paid,
            "reserved_amount": reserved,
            "cat_code": "",
        })
        loss_num += 1

    rows.append({
        "loss_id": f"LR-{loss_num:04d}",
        "location_id": "HAB-2071-A",
        "account_id": "GR-2071",
        "loss_date": "2024-08-19",
        "peril": "Wind",
        "paid_amount": 284600.00,
        "reserved_amount": 0.00,
        "cat_code": "CAT-2408",
    })

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


RULES_TEXT = """Granite Ridge Apartment Partners — Habitational Renewal Routing Notes
Program: GRP-HAB-MW Multi-Family | Effective batch: October 1 | UW desk reference GRP-RNW-2025-10

Purpose
These notes govern October renewal routing for the Midwest habitational book. When the renewal account list export disagrees with the policy location schedule or 36-month loss run, apply the hierarchy in Section 1 before assigning Quote, Refer, Decline, or Ask Broker on renewal_underwriting_review.xlsx.

Section 1 — Source hierarchy
1. granite_ridge_routing_notes.txt (this file) controls routing thresholds and documentation requirements.
2. granite_ridge_loss_run_36mo.csv governs loss history and recomputed loss ratios when the account list loss ratio appears stale or incomplete.
3. granite_ridge_location_schedule.csv governs location TIV, unit counts, subsidized units, vacancy flags, life-safety inspection dates, and pool liability flags.
4. granite_ridge_renewal_accounts.csv is a summary export only. Do not quote solely on account-level occupancy, unit count, TIV, or loss ratio when location or loss detail conflicts.

Section 2 — Disposition definitions
Quote: Account meets appetite, documentation complete, no mandatory referral trigger active.
Refer: Underwriter review required before bind; may quote after clearance.
Decline: Account exceeds decline threshold or fails appetite.
Ask Broker: Material exposure change pending broker confirmation; do not quote until updated.

Section 3 — Loss ratio rules (36 months, attritional)
Recompute account loss ratio as (sum of paid_amount + reserved_amount for all locations on the account) divided by expiring_premium, excluding rows with a non-blank cat_code.
Decline if recomputed loss ratio is 70% or greater.
Refer if recomputed loss ratio is 45% or greater but below 70%.
Refer if any single location has total incurred (paid plus reserved) of $250,000 or more in the 36-month window, even when the account-level summary looks acceptable.

Section 4 — Unit count and TIV reconciliation
Refer if absolute difference between account unit_count on the account list and the sum of unit_count on the location schedule exceeds 5% of account unit_count.
Refer if absolute difference between account_tiv on the account list and the sum of building_tiv on the location schedule exceeds 3% of account_tiv.
Document the variance on Loss_Reconciliation and Location_Exceptions.

Section 5 — Life-safety inspections and pool remediation
Refer any location where sprinkler_inspection_date or fire_alarm_inspection_date is more than 30 days before the batch effective date (October 1, 2025) without a renewed certificate on file.
Refer any account with pool_liability_flag of pending_fence_po until completion evidence is uploaded.
Completed inspections within the grace window may be quoted if all other triggers are clear.

Section 6 — Subsidized housing and vacancy
Refer any location with subsidized_unit_count greater than zero before Quote, even if the account summary subsidized_housing_flag is N.
Flag subsidized locations on Location_Exceptions and cite Section 6 for endorsement documentation requirements.
Ask Broker when vacancy_flag is Y on any location and broker_confirmation is no on that row.
Refer when account occupancy_pct implies full occupancy but any location row shows vacancy_flag Y without a documented turnover exception in broker files.

Section 7 — Documentation requirements
Account_Routing must list all accounts in the October batch (36 accounts in the current export).
Every Refer, Decline, and Ask Broker row requires a one-line rationale citing the rule section and source file.
Rules_Citations must cite this file for loss-ratio, inspection-lapse, subsidized-housing, unit-count, and vacancy referral triggers.
Loss_Reconciliation must show recomputed ratios wherever the account list ratio differs from the loss run by more than 5 points.

Section 8 — Prior disposition field
prior_disposition and renewal_ready_flag on the account list are informational. They do not override referral triggers from location or loss files.

Section 9 — Cat losses
Catastrophe-coded rows (cat_code populated) are tracked separately. Exclude them from attritional loss-ratio calculations unless CUO memo GRP-CAT-2025-03 applies; default treatment is exclusion for routing thresholds in Section 3.

Section 10 — Desk contacts and student housing
Renewal desk lead: M. Calderon | Subsidized housing queue: GRP-SUB-HAB | Broker update queue: GRP-BRK-UPD
Any account whose named insured is Campus Edge Housing Co. (student-housing book; currently GR-2007 and GR-2065) requires a Section 10 appetite note on Location_Exceptions stating that GRP-APPETITE review must be submitted before bind, even if no vacancy_flag is set. Do not state that clearance has already been obtained unless a separate CUO clearance memo is in the file package.
Questions on ambiguous student-housing seasonal vacancy go to GRP-APPETITE before bind.

End of routing notes.
"""


def main() -> None:
    TASK.mkdir(parents=True, exist_ok=True)
    accounts = TASK / "granite_ridge_renewal_accounts.csv"
    locations = TASK / "granite_ridge_location_schedule.csv"
    losses = TASK / "granite_ridge_loss_run_36mo.csv"
    rules = TASK / "granite_ridge_routing_notes.txt"

    write_accounts(accounts)
    write_locations(locations, accounts)
    write_loss_run(losses, accounts, locations)
    rules.write_text(RULES_TEXT, encoding="utf-8")

    print(f"Wrote {accounts}")
    print(f"Wrote {locations}")
    print(f"Wrote {losses}")
    print(f"Wrote {rules} ({len(RULES_TEXT.split())} words)")


if __name__ == "__main__":
    main()
