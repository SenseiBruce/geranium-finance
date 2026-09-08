#!/usr/bin/env python3
"""Generate input files for sawtooth-july-renewal-desk."""

from __future__ import annotations

import csv
import random
from pathlib import Path

TASK = Path(__file__).resolve().parent.parent / "tasks" / "sawtooth-july-renewal-desk" / "inputs"
random.seed(20260701)

ACCOUNT_IDS = [
    "SI-1001", "SI-1004", "SI-1007", "SI-1010", "SI-1015", "SI-1018", "SI-1021", "SI-1024",
    "SI-1027", "SI-1030", "SI-1033", "SI-1036", "SI-1039", "SI-1042", "SI-1045", "SI-1048",
    "SI-1051", "SI-1054", "SI-1057", "SI-1060", "SI-1063", "SI-1066", "SI-1069", "SI-1072",
    "SI-1075", "SI-1078", "SI-1081", "SI-1084", "SI-1088", "SI-1091", "SI-1094", "SI-1097",
    "SI-1100", "SI-1103", "SI-1106", "SI-1109", "SI-1112", "SI-1156",
]

STATES = ["GA", "AL", "SC", "NC", "TN", "FL", "MS", "LA"]
NAMES = [
    "Piedmont Coil Works", "Delta Packaging LLC", "Sunbelt Metal Fab", "Carolina Adhesives",
    "Lowcountry Plastics", "Tri-Rivers Warehousing", "Gulf Shore Machining", "Appalachian Foods",
    "Meridian Conveyor", "Oak Hollow Lumber", "Coastal Crate Co", "Riverbend Chemical",
    "Summit Fasteners", "Harbor Industrial Supply", "Blue Ridge Motors", "Magnolia Textiles",
    "Keystone Pallet", "Cumberland Pipe", "Bayou Fabrication", "Highland Gear",
]

# (location_id, paid, reserved, peril, loss_date) — attritional unless cat_code set separately
ACCOUNT_LOSS_OVERRIDES: dict[str, list[tuple[str, float, float, str, str]]] = {
    "SI-1015": [("ORL-1015-A", 9840.00, 5120.00, "Water", "2024-03-14")],
    "SI-1021": [
        ("ORL-1021-A", 6420.00, 2180.00, "Theft", "2024-06-02"),
        ("ORL-1021-B", 5180.00, 0.00, "GL", "2024-09-18"),
    ],
    "SI-1042": [
        ("ORL-1042-A", 4820.00, 0.00, "Fire", "2024-02-11"),
        ("ORL-1042-B", 198240.00, 80160.00, "Water", "2024-08-17"),
    ],
    "SI-1088": [
        ("ORL-1088-B", 11240.00, 3840.00, "Wind", "2024-05-22"),
    ],
    "SI-1156": [
        ("ORL-1156-A", 28440.00, 9200.00, "Fire", "2024-11-03"),
        ("ORL-1156-A", 19880.00, 0.00, "Water", "2024-07-19"),
        ("ORL-1156-B", 22110.00, 15400.00, "Wind", "2024-10-08"),
        ("ORL-1156-B", 12642.00, 0.00, "Theft", "2024-04-30"),
    ],
    "SI-1033": [("ORL-1033-A", 8240.00, 1920.00, "Water", "2024-01-27")],
    "SI-1097": [("ORL-1097-B", 28440.00, 11880.00, "Fire", "2024-12-06")],
    "SI-1103": [("ORL-1103-A", 31880.00, 14220.00, "Wind", "2024-08-30")],
}


def write_accounts(path: Path) -> None:
    rows = []
    for i, acct in enumerate(ACCOUNT_IDS):
        premium = round(random.uniform(52000, 128000), 2)
        tiv = round(random.uniform(3200000, 15600000), 0)
        lr = round(random.uniform(14, 36), 1)
        prior = "Quoted"
        renewal_ready = "Y"
        if acct == "SI-1015":
            premium, tiv, lr, prior = 67340.00, 6120000, 22.4, "Quoted"
        elif acct == "SI-1021":
            premium, tiv, lr = 95680.00, 12450000, 31.2
        elif acct == "SI-1042":
            premium, tiv, lr, prior = 562400.00, 9870000, 38.1, "Quoted"
        elif acct == "SI-1088":
            premium, tiv, lr, prior, renewal_ready = 71850.00, 8450000, 29.7, "Renewal Ready", "Y"
        elif acct == "SI-1156":
            premium, tiv, lr, prior = 112400.00, 14280000, 52.0, "Quoted"
        elif acct == "SI-1033":
            premium, tiv, lr = 58420.00, 4980000, 27.8
        rows.append({
            "account_id": acct,
            "named_insured": NAMES[i % len(NAMES)] + f" ({acct})",
            "state": random.choice(STATES),
            "expiring_premium": premium,
            "account_tiv": tiv,
            "occupancy_class": random.choice(["Manufacturing", "Warehouse", "Office", "Processing"]),
            "prior_disposition": prior,
            "account_loss_ratio_36mo": lr,
            "renewal_ready_flag": renewal_ready,
        })
    rows[ACCOUNT_IDS.index("SI-1015")]["state"] = "GA"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def write_locations(path: Path, accounts_path: Path) -> None:
    accounts = {r["account_id"]: r for r in csv.DictReader(accounts_path.open())}
    rows = []
    coastal_patches = {
        "ORL-1045-A": ("Tampa", "FL", "CW-2"),
        "ORL-1072-A": ("Mobile", "AL", "CW-1"),
        "ORL-1094-B": ("Pensacola", "FL", "CW-2"),
        "ORL-1106-A": ("Biloxi", "MS", "CW-1"),
    }

    for acct in ACCOUNT_IDS:
        loc_count = 3 if acct in {"SI-1021", "SI-1042"} else 2
        if acct == "SI-1094":
            loc_count = 2
        weights = [random.uniform(0.85, 1.15) for _ in range(loc_count)]
        account_tiv = float(accounts[acct]["account_tiv"])
        if acct == "SI-1021":
            target_sum = 11287340
        else:
            target_sum = account_tiv * random.uniform(0.985, 1.015)
        scale = target_sum / sum(weights)
        for n in range(loc_count):
            loc_id = f"ORL-{acct.split('-')[1]}-{chr(65 + n)}"
            mit = "complete"
            vacancy = "N"
            broker = "yes"
            if acct == "SI-1088" and n == 0:
                mit = "pending_roof_po"
            if acct == "SI-1033" and n == 1:
                vacancy = "Y"
                broker = "no"
            rows.append({
                "location_id": loc_id,
                "account_id": acct,
                "address_city": random.choice(["Macon", "Birmingham", "Greenville", "Chattanooga"]),
                "state": random.choice(["GA", "AL", "SC", "TN", "NC"]),
                "building_tiv": round(weights[n] * scale, 0),
                "protection_class": random.choice(["3", "4", "5", "6"]),
                "coastal_wind_zone": "",
                "vacancy_flag": vacancy,
                "mitigation_status": mit,
                "broker_confirmation": broker,
            })

    for r in rows:
        patch = coastal_patches.get(r["location_id"])
        if patch:
            r["address_city"], r["state"], r["coastal_wind_zone"] = patch

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
        target_incurred = premium * random.uniform(0.08, 0.32)
        loc_id = loc_ids_by_acct[acct][0]
        rows.append({
            "loss_id": f"LR-{loss_num:04d}",
            "location_id": loc_id,
            "account_id": acct,
            "loss_date": "2024-06-15",
            "peril": random.choice(["Water", "Wind", "Theft"]),
            "paid_amount": round(target_incurred * 0.72, 2),
            "reserved_amount": round(target_incurred * 0.28, 2),
            "cat_code": "",
        })
        loss_num += 1

    rows.append({
        "loss_id": f"LR-{loss_num:04d}",
        "location_id": "ORL-1075-A",
        "account_id": "SI-1075",
        "loss_date": "2024-09-26",
        "peril": "Wind",
        "paid_amount": 318400.00,
        "reserved_amount": 0.00,
        "cat_code": "CAT-2419",
    })

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


RULES_TEXT = """Sawtooth Industrial Group — Commercial Property Renewal Routing Notes
Program: SIG-CP-SE Manufacturing | Effective batch: July 1 | UW desk reference SIG-RNW-2025-07

Purpose
These notes govern July renewal routing for the Southeast manufacturing book. When the renewal account list export disagrees with the policy location schedule or 36-month loss run, apply the hierarchy in Section 1 before assigning Quote, Refer, Decline, or Ask Broker on renewal_underwriting_review.xlsx.

Section 1 — Source hierarchy
1. underwriting_rules_notes.txt (this file) controls routing thresholds and documentation requirements.
2. loss_run_36mo.csv governs loss history and recomputed loss ratios when the account list loss ratio appears stale or incomplete.
3. policy_location_schedule.csv governs location TIV, coastal wind zones, vacancy flags, and mitigation status.
4. renewal_account_list.csv is a summary export only. Do not quote solely on account-level loss ratio or account TIV when location or loss detail conflicts.

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

Section 4 — TIV reconciliation
Refer if absolute difference between account_tiv on the account list and the sum of building_tiv on the location schedule exceeds 3% of account_tiv.
Document the variance on Loss_Reconciliation and Location_Exceptions.

Section 5 — Mitigation and coastal wind
Refer any account with mitigation_status of pending_roof_po or pending_hurricane_straps until completion evidence is uploaded.
Locations with coastal_wind_zone CW-1 or CW-2 require coastal wind endorsement documentation on Location_Exceptions before Quote, even if the account summary is otherwise clean.
Completed mitigation may be quoted if all other triggers are clear.

Section 6 — Vacancy and broker confirmation
Ask Broker when vacancy_flag is Y on any location and broker_confirmation is no on that row.
Do not decline solely for vacancy without CUO sign-off; route Ask Broker first.

Section 7 — Documentation requirements
Account_Routing must list all accounts in the July batch (38 accounts in the current export).
Every Refer, Decline, and Ask Broker row requires a one-line rationale citing the rule section and source file.
Rules_Citations must cite this file for loss-ratio, mitigation, coastal, and TIV referral triggers.
Loss_Reconciliation must show recomputed ratios wherever the account list ratio differs from the loss run by more than 5 points.

Section 8 — Prior disposition field
prior_disposition and renewal_ready_flag on the account list are informational. They do not override referral triggers from location or loss files.

Section 9 — Cat losses
Catastrophe-coded rows (cat_code populated) are tracked separately. Exclude them from attritional loss-ratio calculations unless CUO memo SIG-CAT-2025-02 applies; default treatment is exclusion for routing thresholds in Section 3.

Section 10 — Desk contacts
Renewal desk lead: J. Whitfield | Coastal referral queue: SIG-COAST | Broker update queue: SIG-BRK-UPD
Questions on ambiguous occupancy changes go to SIG-APPETITE before bind.

End of routing notes.
"""


def main() -> None:
    TASK.mkdir(parents=True, exist_ok=True)
    accounts = TASK / "renewal_account_list.csv"
    locations = TASK / "policy_location_schedule.csv"
    losses = TASK / "loss_run_36mo.csv"
    rules = TASK / "underwriting_rules_notes.txt"

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
