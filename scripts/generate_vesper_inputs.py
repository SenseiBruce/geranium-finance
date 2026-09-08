#!/usr/bin/env python3
"""Generate input files for Vesper Culinary Brands Q3 consolidation."""

from __future__ import annotations

import csv
from pathlib import Path

TASK = (
    Path(__file__).resolve().parent.parent
    / "tasks"
    / "vesper-culinary-brands-consolidation"
    / "inputs"
)

# Governing assumptions (for golden; not printed as totals in inputs)
Q3_START = "2025-07-01"
Q3_END = "2025-09-30"
Q3_DAYS = 92  # Jul 31 + Aug 31 + Sep 30
KILN_CLOSE = "2025-08-12"
KILN_OWNED_DAYS = 50  # Aug 12–Sep 30 inclusive
EUR_USD_CLOSE = 1.0874
EUR_USD_SPOT_ASIDE = 1.1025  # distractor only


LEDGER_HEADERS = [
    "transaction_id",
    "brand",
    "transaction_date",
    "description",
    "amount",
    "currency",
    "status",
]

# Same economics as the prior package; IDs and row order naturalized so the
# extract no longer reads as tidy per-brand exception blocks.
LEDGER_ROWS: list[list] = [
    # Mixed-brand chronological extract (billing system sequence, not brand blocks)
    ["VC-66208", "Hearth Kitchen Co", "2025-06-28", "June sell-in catch-up", "41000.00", "USD", "posted"],
    ["VC-78421", "Hearth Kitchen Co", "2025-07-03", "Retail sell-in - Northeast DSD", "128447.36", "USD", "posted"],
    ["VC-55102", "Brine & Barrel EU", "2025-07-08", "DE grocery sell-in - Q3 wave 1", "118622.47", "EUR", "posted"],
    ["KS-33408", "Kiln Spice Works", "2025-07-09", "Club channel sell-in - Midwest", "88412.33", "USD", "posted"],
    ["VC-79104", "Hearth Kitchen Co", "2025-07-11", "Club channel slotting fee recovery", "38412.88", "USD", "posted"],
    ["VC-55840", "Brine & Barrel EU", "2025-07-18", "NL foodservice distributor draw", "64218.93", "EUR", "posted"],
    ["VC-80233", "Hearth Kitchen Co", "2025-07-22", "Foodservice distributor rebate true-up", "22109.54", "USD", "posted"],
    ["KS-34155", "Kiln Spice Works", "2025-07-23", "Foodservice distributor draw", "51207.18", "USD", "posted"],
    ["VC-56411", "Brine & Barrel EU", "2025-07-29", "FR specialty retail booking", "89104.55", "EUR", "posted"],
    ["KS-34802", "Kiln Spice Works", "2025-08-04", "Private label trial shipment", "37664.90", "USD", "posted"],
    ["VC-81055", "Hearth Kitchen Co", "2025-08-05", "Private label co-pack milestone", "97533.17", "USD", "posted"],
    ["VC-81091", "Hearth Kitchen Co", "2025-08-05", "Private label co-pack milestone", "97533.17", "USD", "duplicate"],
    ["VC-57188", "Brine & Barrel EU", "2025-08-09", "BE club trial shipment", "45781.26", "EUR", "posted"],
    ["KS-35220", "Kiln Spice Works", "2025-08-11", "Retail sell-in - early August", "22918.45", "USD", "posted"],
    ["KS-36001", "Kiln Spice Works", "2025-08-12", "Close-day retail sell-in", "67428.56", "USD", "posted"],
    ["VC-82107", "Hearth Kitchen Co", "2025-08-14", "E-commerce marketplace settlement", "61208.43", "USD", "posted"],
    ["KS-36544", "Kiln Spice Works", "2025-08-19", "Club pack first post-close order", "95817.22", "USD", "posted"],
    ["VC-58204", "Brine & Barrel EU", "2025-08-21", "EU trade promo clawback", "-6233.48", "EUR", "void"],
    ["VC-82591", "Hearth Kitchen Co", "2025-08-27", "Seasonal SKU promo accrual reverse", "-8416.22", "USD", "void"],
    ["KS-37102", "Kiln Spice Works", "2025-08-28", "Spice blend co-pack milestone", "81244.67", "USD", "posted"],
    ["VC-59033", "Brine & Barrel EU", "2025-09-02", "DE reorder - autumn assortment", "102447.18", "EUR", "posted"],
    ["VC-83340", "Hearth Kitchen Co", "2025-09-04", "Grocery chain scan-down billback", "44917.65", "USD", "posted"],
    ["KS-37888", "Kiln Spice Works", "2025-09-05", "Grocery scan-down recovery", "44109.38", "USD", "posted"],
    ["VC-59710", "Brine & Barrel EU", "2025-09-11", "UK broker settlement (EUR billed)", "73819.64", "EUR", "posted"],
    ["VC-84012", "Hearth Kitchen Co", "2025-09-12", "Club pack extension order", "88344.91", "USD", "posted"],
    ["KS-38401", "Kiln Spice Works", "2025-09-15", "Voided duplicate broker fee", "-3900.00", "USD", "void"],
    ["VC-60144", "Brine & Barrel EU", "2025-09-18", "Cancelled sample program invoice", "12800.00", "EUR", "cancelled"],
    ["VC-84108", "Hearth Kitchen Co", "2025-09-19", "Quarter close stub - zeroed", "0.00", "USD", "cancelled"],
    ["KS-39055", "Kiln Spice Works", "2025-09-22", "Foodservice September draw", "70355.14", "USD", "posted"],
    ["VC-60882", "Brine & Barrel EU", "2025-09-24", "Nordics distributor true-up", "56933.71", "EUR", "posted"],
    ["VC-84776", "Hearth Kitchen Co", "2025-09-26", "Export broker commission offset", "31782.09", "USD", "posted"],
    ["KS-39510", "Kiln Spice Works", "2025-09-27", "E-comm marketplace settlement", "38912.80", "USD", "posted"],
    ["VC-61205", "Brine & Barrel EU", "2025-09-28", "Close-week EU DSD residual", "41408.82", "EUR", "posted"],
    ["KS-39788", "Kiln Spice Works", "2025-09-29", "Cancelled inventory transfer bill", "15000.00", "USD", "cancelled"],
    ["VC-84991", "Hearth Kitchen Co", "2025-09-29", "Late September DSD catch-up", "52961.78", "USD", "posted"],
    ["KS-39902", "Kiln Spice Works", "2025-09-30", "Quarter-end residual sell-in", "26741.93", "USD", "posted"],
    ["VC-62091", "Brine & Barrel EU", "2025-10-03", "October prebill - EU clubs", "22000.00", "EUR", "out_of_period"],
]


ACQUISITION_MEMO = """Vesper Culinary Brands  -  Kiln Spice Works Tuck-In Acquisition Memo
Prepared by Corporate Development | August 14, 2025
Distribution: Finance, Corporate Controller, Treasury Operations, FP&A

Summary
Vesper Culinary Brands completed the tuck-in acquisition of Kiln Spice Works on August 12, 2025. Kiln is a specialty dry-spice and rub manufacturer selling through club, grocery, and foodservice distributors in the United States. For Q3 2025 consolidated management reporting and the Friday board packet, only revenue earned on or after the economic close date may be attributed to Vesper ownership. Pre-close Kiln billings that remain in the brand ledger as posted must not roll into the consolidated Q3 net revenue figure used for board materials.

Background and deal chronology
Kiln operated as an independent seller through early August. The stock purchase agreement was signed August 6, 2025, with economic transfer and ownership start effective August 12, 2025 per Schedule 2.1 of the disclosure package. Billing continued on Kiln's legacy entity code during the transition week, which means the consolidated brand ledger extract still contains July and early-August Kiln rows tagged posted. Those rows reflect Kiln's standalone activity before Vesper ownership; they are real invoices that simply fall outside Vesper's ownership window.

A sales operations email circulated August 13 describing "full quarter Kiln contribution" for internal pipeline tracking. That note is a commercial forecast convenience only. It does not override Corporate Development close mechanics or this memo's ownership treatment for the board package. Controllers should ignore the full-quarter sales note when building consolidated Q3 revenue.

Transaction structure and key dates
- Transaction document: stock purchase agreement
- Signing date: August 6, 2025
- Closing date and governing ownership start date: August 12, 2025 (Schedule 2.1)
- Reporting entity after close: Kiln Spice Works LLC (wholly owned subsidiary of Vesper Culinary Brands)
- Pre-close activity through August 11, 2025 remains outside Vesper consolidated totals for Q3 2025
- Post-close activity from August 12, 2025 through September 30, 2025 is in scope for Q3 consolidation subject to the proration guidance below

Ownership / proration treatment for Q3 consolidation (governing authority)
The permitted ownership treatment for Q3 consolidation, including the 50/92 proration method, is established by this acquisition memo. Q3 2025 runs July 1, 2025 through September 30, 2025 (92 calendar days). Post-close ownership covers August 12, 2025 through September 30, 2025 inclusive (50 days).

Finance should apply a 50/92 proration factor to Kiln Spice Works gross Q3 revenue that survives standard revenue exclusions when consolidating, unless a pure transaction-level ownership cutoff is documented and the controller signs off on that alternative method. No controller sign-off for the transaction-date cutoff is attached to this packet; until such approval is obtained, treat the cutoff approach as a conditional scenario only.

Recommended practice for this close: start from Kiln ledger rows with status posted (and in currency USD), exclude void, cancelled, duplicate, and out_of_period statuses, then either (a) drop rows dated before August 12 and sum the remainder, or (b) sum all in-period posted Kiln rows for the full quarter and multiply by 50/92. Do not mix both methods. Do not apply proration on top of an already ownership-cutoff sum. Retain a clear record of which ownership method is used for board reporting and whether controller approval for the cutoff alternative exists.

Systems and extract notes
The brand ledger extract still contains July and early-August Kiln rows from the pre-close billing run. Transactions occurring before the ownership start date are treated according to the ownership method above. Void and cancelled rows are excluded. Qualifying post-close transactions follow the selected ownership treatment. Identify affected rows from the ledger itself; do not rely on informal sales-ops forecasts.

Controller review points
- Confirm the August 12 close date matches Schedule 2.1 of the signed stock purchase agreement and the bank wire confirmation.
- Tie August 12 and later Kiln billings to post-close service and shipment evidence where practical.
- Confirm void and cancelled Kiln stubs do not inflate the ownership-window sum.
- Coordinate with Treasury on EUR conversion for Brine & Barrel EU using brine_barrel_fx_and_period_reference.txt; Kiln itself bills in USD.

Contact and sign-off
N. Calder, VP Corporate Development
cc: R. Vasquez, Corporate Controller; Treasury Operations mailbox VCB-FX series
"""


FX_PERIOD_MEMO = """Vesper Culinary Brands  -  FX and Period Reference
Treasury Policy Bulletin VCB-FX-2025-03 | Effective Q3 2025
Owner: Treasury Operations | Review cycle: Quarterly

Reporting period
Consolidated management reporting for the board packet uses calendar Q3 2025: July 1, 2025 through September 30, 2025. Weekly flash and monthly management packs may use alternate cutoffs for operational dashboards. This bulletin governs the board consolidation package only. Rows dated before July 1, 2025 or after September 30, 2025 are out of scope for Q3 consolidated net revenue even when the extract still lists them as posted.

Functional currency by brand
- Hearth Kitchen Co: USD (report directly to consolidated USD)
- Brine & Barrel EU: EUR (convert to USD for consolidated view)
- Kiln Spice Works: USD (subject to acquisition ownership rules in kiln_spice_acquisition_memo.txt; this bulletin does not establish Kiln ownership or proration mechanics)

EUR to USD conversion for board consolidation
Use the Q3 2025 board close rate of 1.0874 USD per EUR for all Brine & Barrel EU revenue in consolidated reporting. Do not use month-end spot rates, payment-date rates, or trader screens for this package. A desk note from August mentioned an informal spot of approximately 1.1025 during a volatile session; that aside is informational only and does not supersede this bulletin. If Brine submits invoices in EUR, translate using 1.0874 unless Treasury publishes a later VCB-FX bulletin that explicitly replaces the close rate.

Status exclusion hierarchy
Exclude ledger rows with status void, cancelled, duplicate, or out_of_period from consolidated revenue. Posted is the only status that may enter the recognition set, and even posted rows can be removed when they fail period or ownership tests. Duplicate rows often reuse the same commercial description as a valid posted invoice; keeping both would double-count. Cancelled and void rows may carry positive or negative amounts and must still be excluded rather than netted as if they were recognized adjustments unless a separate controller-approved reclass journal exists outside this extract.

Period and ownership boundary rules
- Any brand row dated before July 1, 2025 that remains in the extract is prior-period and must not enter Q3 consolidated totals.
- Any brand row dated after September 30, 2025, including rows tagged out_of_period, is next-period and must stay out of Q3.
- Kiln Spice Works ownership timing, including the August 12, 2025 close and the 50/92 proration (or optional transaction-date cutoff with controller sign-off), is governed by kiln_spice_acquisition_memo.txt. This bulletin defers to that memo for ownership/proration and does not restate a separate Treasury ownership formula.

Reconciliation expectations
Controllers should retain an exclusion trail for rows removed from consolidated revenue, including transaction id, brand, status or exclusion reason, native amount, and USD impact after FX where relevant. Where the ledger mixes currencies, show both native currency and consolidated USD. State the EUR rate used and the Kiln ownership method (transaction cutoff or 50/92) so board readers can follow the bridge from raw extract to the recommended consolidated figure.

Governing FX rounding convention
Brine EUR revenue is summed in native EUR before conversion to USD; the converted total is rounded to cents. Line-level USD rounding is not used for the consolidated Brine total. Multiply the aggregated eligible EUR amount by the 1.0874 board close rate, then round the USD product to cents once. Retain that sum-then-round treatment in the close support. A line-by-line convert-and-round-then-sum control will differ by one cent and is not the governing method for board consolidation. Do not blend the informal 1.1025 spot into any line. Hearth and Kiln USD lines do not need FX; they still need status, period, and (for Kiln) ownership filters before they enter the rollup.

Contact
Treasury Operations — VCB-FX series mailbox
Policy questions: route through the VCB-FX distribution list
"""


def write_ledger(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(LEDGER_HEADERS)
        writer.writerows(LEDGER_ROWS)


def write_text(path: Path, body: str) -> None:
    path.write_text(body.strip() + "\n", encoding="utf-8")


def preview_totals() -> None:
    """Dev-only sanity print; not written to inputs."""
    from collections import defaultdict

    by_brand: dict[str, float] = defaultdict(float)
    for row in LEDGER_ROWS:
        _tid, brand, date, _desc, amount, currency, status = row
        amt = float(amount)
        if status != "posted":
            continue
        if date < Q3_START or date > Q3_END:
            continue
        if brand == "Kiln Spice Works" and date < KILN_CLOSE:
            continue
        if currency == "EUR":
            amt *= EUR_USD_CLOSE
        by_brand[brand] += amt
    print("Preview recognized USD by brand (transaction cutoff for Kiln):")
    for brand, total in sorted(by_brand.items()):
        print(f"  {brand}: {round(total, 2)}")
    print(f"  TOTAL: {round(sum(by_brand.values()), 2)}")


def main() -> None:
    TASK.mkdir(parents=True, exist_ok=True)
    write_ledger(TASK / "vesper_culinary_brands_brand_ledger.csv")
    write_text(TASK / "kiln_spice_acquisition_memo.txt", ACQUISITION_MEMO)
    write_text(TASK / "brine_barrel_fx_and_period_reference.txt", FX_PERIOD_MEMO)
    print(f"Wrote inputs to {TASK}")
    preview_totals()


if __name__ == "__main__":
    main()
