#!/usr/bin/env python3
"""Generate inputs for Northline intercompany FX/cut-off settlement."""

from __future__ import annotations

import csv
from pathlib import Path

from northline_ic_constants import (
    AP_C_441_CAD,
    AP_C_442_CAD,
    AP_C_448_DUP_CAD,
    AP_C_455_ORPHAN_CAD,
    AP_CSV,
    AP_M_205_MXN,
    AP_M_210_MXN,
    APPENDIX_A_MIN_USD,
    AR_8688,
    AR_8766,
    AR_8790,
    AR_8812,
    AR_8820_VOID,
    AR_8841,
    AR_8855,
    AR_CSV,
    AS_OF,
    CAD_PER_USD,
    ENTITY,
    MEMO_TXT,
    MXN_PER_USD,
    SLUG,
    STALE_CAD_PER_USD,
)

TASK_INPUTS = Path(__file__).resolve().parent.parent / "tasks" / SLUG / "inputs"


def _amt(value: float | str) -> str:
    """Consistent CSV amount formatting (no thousands separators)."""
    if isinstance(value, str):
        return f"{float(value.replace(',', '')):.2f}"
    return f"{float(value):.2f}"


def write_ar(path: Path) -> None:
    headers = [
        "invoice_id",
        "invoice_date",
        "ship_date",
        "counterparty",
        "counterparty_code",
        "description",
        "amount_usd",
        "fob_terms",
        "status_flag",
        "bol_or_ref",
        "notes",
    ]
    # All rows use the same amount formatting. Rows are ordered by invoice_id so
    # Appendix A / void lines are interleaved with ordinary noise (not blocked at top).
    rows = [
        ["INV-AR-8601", "2026-06-12", "2026-06-12", "Northline Canada Ltd", "NLC", "Prior period - settled July sweep", _amt(44220.18), "FOB_ShippingPoint", "Settled", "BOL-8601", "Paid 2026-07-08"],
        ["INV-AR-8612", "2026-06-20", "2026-06-21", "Northline Mexico SA de CV", "NLM", "Prior period - settled July sweep", _amt(28110.40), "FOB_ShippingPoint", "Settled", "BOL-8612", "Paid 2026-07-08"],
        ["INV-AR-8620", "2026-07-02", "2026-07-03", "Northline Canada Ltd", "NLC", "Prior period - settled July sweep", _amt(19880.55), "FOB_ShippingPoint", "Settled", "BOL-8620", "Paid 2026-07-08"],
        ["INV-AR-8633", "2026-07-08", "2026-07-09", "Northline Mexico SA de CV", "NLM", "Prior period - settled July sweep", _amt(33440.22), "FOB_ShippingPoint", "Settled", "BOL-8633", "Paid 2026-07-08"],
        ["INV-AR-8640", "2026-07-18", "2026-07-18", "Northline Canada Ltd", "NLC", "Prior period - settled Aug 5 wire", _amt(12640.18), "n/a", "Settled", "MSA-NLC", "Mgmt fee June remainder"],
        ["INV-AR-8655", "2026-07-22", "2026-07-23", "Northline Mexico SA de CV", "NLM", "Prior period - settled Aug 5 wire", _amt(21220.40), "FOB_ShippingPoint", "Settled", "BOL-8655", ""],
        ["INV-AR-8660", "2026-07-28", "2026-07-29", "Northline Canada Ltd", "NLC", "Prior period - settled Aug 5 wire", _amt(8880.22), "FOB_ShippingPoint", "Settled", "BOL-8660", ""],
        ["INV-AR-8668", "2026-07-30", "2026-07-30", "Northline Mexico SA de CV", "NLM", "Prior period - settled Aug 5 wire", _amt(15110.55), "FOB_ShippingPoint", "Settled", "BOL-8668", ""],
        ["INV-AR-8688", "2026-08-04", "2026-08-05", "Northline Mexico SA de CV", "NLM", "Consumables / tooling inserts", _amt(AR_8688), "FOB_ShippingPoint", "Open", "BOL-8688-MX", "Received 8/8"],
        ["INV-AR-8702", "2026-08-01", "2026-08-01", "Northline Canada Ltd", "NLC", "Engineering support hours - August", _amt(6420.18), "n/a", "Open", "TS-8702", "Service; no BOL"],
        ["INV-AR-8708", "2026-08-03", "2026-08-03", "Northline Mexico SA de CV", "NLM", "Engineering support hours - August", _amt(5880.40), "n/a", "Open", "TS-8708", "Service; no BOL"],
        ["INV-AR-8715", "2026-08-06", "2026-08-07", "Northline Canada Ltd", "NLC", "Fixture repair billable", _amt(9220.55), "FOB_ShippingPoint", "Open", "BOL-8715-CA", "Received 8/9"],
        ["INV-AR-8722", "2026-08-08", "2026-08-09", "Northline Mexico SA de CV", "NLM", "Fixture repair billable", _amt(7640.18), "FOB_ShippingPoint", "Open", "BOL-8722-MX", "Received 8/11"],
        ["INV-AR-8730", "2026-08-10", "2026-08-10", "Northline Canada Ltd", "NLC", "IT shared services August", _amt(4110.22), "n/a", "Open", "IT-ALLOC-08", ""],
        ["INV-AR-8738", "2026-08-13", "2026-08-13", "Northline Mexico SA de CV", "NLM", "IT shared services August", _amt(3880.40), "n/a", "Open", "IT-ALLOC-08", ""],
        ["INV-AR-8744", "2026-08-16", "2026-08-17", "Northline Canada Ltd", "NLC", "Prototype brackets", _amt(11220.18), "FOB_ShippingPoint", "Open", "BOL-8744-CA", "Received 8/19"],
        ["INV-AR-8750", "2026-08-18", "2026-08-19", "Northline Mexico SA de CV", "NLM", "Prototype brackets", _amt(10440.55), "FOB_ShippingPoint", "Open", "BOL-8750-MX", "Received 8/21"],
        ["INV-AR-8758", "2026-08-21", "2026-08-21", "Northline Canada Ltd", "NLC", "Warranty rebill - OEM customer pass-through", _amt(2840.22), "n/a", "Open", "WR-8758", "Disputed by Canada ops - still open on AR"],
        ["INV-AR-8764", "2026-08-22", "2026-08-23", "Northline Mexico SA de CV", "NLM", "Gauge calibration kit", _amt(4520.18), "FOB_ShippingPoint", "Open", "BOL-8764-MX", "Received 8/25"],
        ["INV-AR-8766", "2026-07-15", "2026-07-15", "Northline Canada Ltd", "NLC", "Q3 management fee allocation", _amt(AR_8766), "n/a", "Open", "MSA-NLC-2026", "Canada booked AP 8/2"],
        ["INV-AR-8771", "2026-08-24", "2026-08-24", "Northline Canada Ltd", "NLC", "HR shared services August", _amt(3220.40), "n/a", "Open", "HR-ALLOC-08", ""],
        ["INV-AR-8778", "2026-08-25", "2026-08-25", "Northline Mexico SA de CV", "NLM", "HR shared services August", _amt(2980.55), "n/a", "Open", "HR-ALLOC-08", ""],
        ["INV-AR-8785", "2026-08-26", "2026-08-26", "Northline Canada Ltd", "NLC", "Safety supplies recharge", _amt(1640.18), "FOB_ShippingPoint", "Open", "BOL-8785-CA", "Received 8/27"],
        ["INV-AR-8790", "2026-08-11", "2026-08-12", "Northline Canada Ltd", "NLC", "Machined components lot Q3-12", _amt(AR_8790), "FOB_ShippingPoint", "Open", "BOL-8790-CA", "Received Canada 8/14"],
        ["INV-AR-8798", "2026-08-27", "2026-08-27", "Northline Mexico SA de CV", "NLM", "Safety supplies recharge", _amt(1480.40), "n/a", "Open", "PO-8798", "Local buy - parent rebill"],
        ["INV-AR-8805", "2026-08-28", "2026-08-28", "Northline Canada Ltd", "NLC", "Quality lab overtime recharge", _amt(2110.55), "n/a", "Open", "QL-8805", ""],
        ["INV-AR-8812", "2026-08-14", "2026-08-15", "Northline Mexico SA de CV", "NLM", "Spare parts kit - press line", _amt(AR_8812), "FOB_ShippingPoint", "Open", "BOL-8812-MX", "Received Queretaro 8/18"],
        ["INV-AR-8818", "2026-08-29", "2026-08-29", "Northline Mexico SA de CV", "NLM", "Quality lab overtime recharge", _amt(1920.18), "n/a", "Open", "QL-8818", ""],
        ["INV-AR-8820", "2026-08-19", "2026-08-20", "Northline Canada Ltd", "NLC", "DUPLICATE - void of partial 8790 billing error", _amt(AR_8820_VOID), "FOB_ShippingPoint", "Void", "VOID-8820", "Controller voided 8/22; do not settle"],
        ["INV-AR-8830", "2026-08-30", "2026-08-30", "Northline Canada Ltd", "NLC", "Freight prepaid recharge", _amt(3440.22), "n/a", "Open", "FR-8830", ""],
        ["INV-AR-8841", "2026-08-27", "2026-08-28", "Northline Canada Ltd", "NLC", "Custom tooling package - press cell 4", _amt(AR_8841), "FOB_ShippingPoint", "InTransit", "BOL-8841-CA", "Departed Toledo dock 8/28; Canada receipt expected 9/2"],
        ["INV-AR-8848", "2026-08-30", "2026-08-30", "Northline Mexico SA de CV", "NLM", "Freight prepaid recharge", _amt(2880.40), "n/a", "Open", "FR-8848", ""],
        ["INV-AR-8855", "2026-08-28", "2026-08-29", "Northline Mexico SA de CV", "NLM", "Press rebuild modules", _amt(AR_8855), "FOB_ShippingPoint", "InTransit", "BOL-8855-MX", "In transit Laredo corridor; receipt expected 9/3"],
        ["INV-AR-8860", "2026-08-31", "2026-08-31", "Northline Canada Ltd", "NLC", "Month-end true-up estimate (provisional)", _amt(5000.00), "n/a", "Provisional", "EST-8860", "Controller: provisional - exclude until final invoice"],
        ["INV-AR-8866", "2026-08-31", "2026-08-31", "Northline Mexico SA de CV", "NLM", "Month-end true-up estimate (provisional)", _amt(4500.00), "n/a", "Provisional", "EST-8866", "Controller: provisional - exclude until final invoice"],
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(headers)
        w.writerows(rows)


def write_ap(path: Path) -> None:
    headers = [
        "ap_id",
        "booked_date",
        "counterparty_books",
        "currency",
        "amount_local",
        "vendor_ref",
        "parent_invoice_ref",
        "fx_rate_used",
        "status_flag",
        "notes",
    ]
    # Interleaved by ap_id so relevant Appendix A / exception rows are not blocked first.
    rows = [
        ["AP-C-401", "2026-07-05", "Northline Canada Ltd", "CAD", _amt(60680.22), "PO-CA-7601", "INV-AR-8601", "1.3680", "Settled", "Paid July sweep"],
        ["AP-C-410", "2026-07-12", "Northline Canada Ltd", "CAD", _amt(27280.40), "PO-CA-7620", "INV-AR-8620", "1.3680", "Settled", "Paid July sweep"],
        ["AP-C-418", "2026-07-20", "Northline Canada Ltd", "CAD", _amt(17340.18), "MSA-NLC", "INV-AR-8640", "1.3680", "Settled", "Paid Aug 5"],
        ["AP-C-425", "2026-07-28", "Northline Canada Ltd", "CAD", _amt(12160.55), "PO-CA-7660", "INV-AR-8660", "1.3680", "Settled", "Paid Aug 5"],
        ["AP-C-441", "2026-08-14", "Northline Canada Ltd", "CAD", _amt(AP_C_441_CAD), "PO-CA-7790", "INV-AR-8790", f"{STALE_CAD_PER_USD:.4f}", "Open", "Booked at July month-end CAD rate"],
        ["AP-C-442", "2026-08-02", "Northline Canada Ltd", "CAD", _amt(AP_C_442_CAD), "MSA-NLC-2026", "INV-AR-8766", f"{CAD_PER_USD:.4f}", "Open", "July mgmt fee - booked after July close"],
        ["AP-C-448", "2026-08-15", "Northline Canada Ltd", "CAD", _amt(AP_C_448_DUP_CAD), "PO-CA-7790-DUP", "INV-AR-8790", f"{STALE_CAD_PER_USD:.4f}", "Void", "Duplicate of AP-C-441 - AP clerk void 8/16"],
        ["AP-C-455", "2026-08-20", "Northline Canada Ltd", "CAD", _amt(AP_C_455_ORPHAN_CAD), "PO-CA-LOCAL-12", "", f"{CAD_PER_USD:.4f}", "Open", "Local Canada vendor reclassed to intercompany - no parent invoice"],
        ["AP-C-460", "2026-08-07", "Northline Canada Ltd", "CAD", _amt(8810.22), "TS-8702", "INV-AR-8702", f"{CAD_PER_USD:.4f}", "Open", "Under Sep 3 threshold - leave for Oct"],
        ["AP-C-462", "2026-08-09", "Northline Canada Ltd", "CAD", _amt(12650.40), "PO-CA-7715", "INV-AR-8715", f"{CAD_PER_USD:.4f}", "Open", ""],
        ["AP-C-464", "2026-08-13", "Northline Canada Ltd", "CAD", _amt(5640.18), "IT-ALLOC", "INV-AR-8730", f"{CAD_PER_USD:.4f}", "Open", "IT allocation - immaterial this sweep"],
        ["AP-C-466", "2026-08-19", "Northline Canada Ltd", "CAD", _amt(15400.55), "PO-CA-7744", "INV-AR-8744", f"{CAD_PER_USD:.4f}", "Open", ""],
        ["AP-C-468", "2026-08-21", "Northline Canada Ltd", "CAD", _amt(3890.22), "WR-8758", "INV-AR-8758", f"{CAD_PER_USD:.4f}", "Disputed", "Canada disputes warranty rebill"],
        ["AP-C-470", "2026-08-24", "Northline Canada Ltd", "CAD", _amt(4420.40), "HR-ALLOC", "INV-AR-8771", f"{CAD_PER_USD:.4f}", "Open", ""],
        ["AP-C-472", "2026-08-27", "Northline Canada Ltd", "CAD", _amt(2250.18), "PO-CA-7785", "INV-AR-8785", f"{CAD_PER_USD:.4f}", "Open", "Small PO - next cycle"],
        ["AP-C-474", "2026-08-29", "Northline Canada Ltd", "CAD", _amt(2890.55), "QL-8805", "INV-AR-8805", f"{CAD_PER_USD:.4f}", "Open", ""],
        ["AP-C-476", "2026-08-30", "Northline Canada Ltd", "CAD", _amt(4720.22), "FR-8830", "INV-AR-8830", f"{CAD_PER_USD:.4f}", "Open", "Freight true-up queued for Oct"],
        ["AP-M-180", "2026-07-06", "Northline Mexico SA de CV", "MXN", _amt(522280.40), "PO-MX-4201", "INV-AR-8612", "18.4200", "Settled", "Paid July sweep"],
        ["AP-M-188", "2026-07-14", "Northline Mexico SA de CV", "MXN", _amt(621220.18), "PO-MX-4233", "INV-AR-8633", "18.4200", "Settled", "Paid July sweep"],
        ["AP-M-194", "2026-07-24", "Northline Mexico SA de CV", "MXN", _amt(394220.55), "PO-MX-4255", "INV-AR-8655", "18.4200", "Settled", "Paid Aug 5"],
        ["AP-M-198", "2026-07-31", "Northline Mexico SA de CV", "MXN", _amt(280880.22), "PO-MX-4268", "INV-AR-8668", "18.4200", "Settled", "Paid Aug 5"],
        ["AP-M-205", "2026-08-08", "Northline Mexico SA de CV", "MXN", _amt(AP_M_205_MXN), "PO-MX-4388", "INV-AR-8688", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-210", "2026-08-18", "Northline Mexico SA de CV", "MXN", _amt(AP_M_210_MXN), "PO-MX-4412", "INV-AR-8812", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-220", "2026-08-03", "Northline Mexico SA de CV", "MXN", _amt(109220.40), "TS-8708", "INV-AR-8708", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-222", "2026-08-11", "Northline Mexico SA de CV", "MXN", _amt(141980.18), "PO-MX-4422", "INV-AR-8722", f"{MXN_PER_USD:.4f}", "Open", "Below materiality - roll to next close"],
        ["AP-M-224", "2026-08-13", "Northline Mexico SA de CV", "MXN", _amt(72100.55), "IT-ALLOC", "INV-AR-8738", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-226", "2026-08-21", "Northline Mexico SA de CV", "MXN", _amt(194000.22), "PO-MX-4450", "INV-AR-8750", f"{MXN_PER_USD:.4f}", "Open", "Hold for Oct sweep"],
        ["AP-M-228", "2026-08-25", "Northline Mexico SA de CV", "MXN", _amt(84000.40), "PO-MX-4464", "INV-AR-8764", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-230", "2026-08-25", "Northline Mexico SA de CV", "MXN", _amt(55380.18), "HR-ALLOC", "INV-AR-8778", f"{MXN_PER_USD:.4f}", "Open", "HR shared-cost - defer"],
        ["AP-M-232", "2026-08-27", "Northline Mexico SA de CV", "MXN", _amt(27500.55), "PO-MX-4478", "INV-AR-8798", f"{MXN_PER_USD:.4f}", "Open", ""],
        ["AP-M-234", "2026-08-29", "Northline Mexico SA de CV", "MXN", _amt(35680.22), "QL-8818", "INV-AR-8818", f"{MXN_PER_USD:.4f}", "Open", "QC chargeback - next cycle"],
        ["AP-M-236", "2026-08-30", "Northline Mexico SA de CV", "MXN", _amt(53520.40), "FR-8848", "INV-AR-8848", f"{MXN_PER_USD:.4f}", "Open", ""],
    ]
    # Natural extract order: booked_date then ap_id (interleaves exceptions with noise)
    rows.sort(key=lambda r: (r[1], r[0]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(headers)
        w.writerows(rows)


def write_memo(path: Path) -> None:
    # Rules only — no planted exception invoice / AP IDs. Solvers discover rows in ledgers.
    text = f"""\
{ENTITY} — Intercompany Cut-off and FX Memo
Month-end: {AS_OF}
Prepared by: Corporate Controllers / Treasury
Distribution: Entity controllers (US, Canada, Mexico); Treasury ops
Classification: Internal — closing file

1. Purpose
This memo sets the governing rules for the September 3, 2026 intercompany cash sweep covering open affiliate balances as of {AS_OF}. Controllers must apply these rules to the parent AR subledger and the Canada / Mexico AP mirrors. Where the AR subledger, AP mirrors, and this memo conflict, this memo controls. Do not invent external FX rates, cut-off policies, or treasury systems outside this closing file and the two ledger extracts.

2. Settlement population (Appendix A — material sweep)
For the September 3 wire cycle, the Appendix A settlement population is defined by source attributes on the parent AR subledger — Controllers must identify qualifying invoices from the extract rather than from a pre-printed ID list.

Include a parent AR invoice in Appendix A when ALL of the following are true as of {AS_OF}:
(a) counterparty is Northline Canada Ltd or Northline Mexico SA de CV;
(b) status_flag is Open or InTransit;
(c) amount_usd is greater than or equal to ${APPENDIX_A_MIN_USD:,.2f} (materiality threshold for this sweep).

Exclude from Appendix A (and from the September 3 wire) any AR line that fails the tests above, including:
- status Settled (prior-period items retained on the extract for audit trail only);
- status Provisional (month-end estimates awaiting a final invoice);
- status Void (never settled);
- Open or InTransit lines below the ${APPENDIX_A_MIN_USD:,.2f} materiality threshold (those roll to the mid-September cycle);
- disputed warranty / pass-through rebills that do not meet the Appendix A tests.

Apply the same materiality lens when selecting affiliate AP for the FX tie-out: only Open AP rows that reference an Appendix A parent invoice (via parent_invoice_ref) enter the matched AP conversion set, subject to the void / duplicate / orphan rules in section 6.

3. Cut-off — FOB shipping point
Intercompany product shipments use FOB shipping point. The parent recognizes AR when goods leave the US dock (ship_date on the AR subledger). The affiliate recognizes AP when goods are received at the affiliate facility.

Consequence for {AS_OF}:
- If ship_date is on or before {AS_OF} and the affiliate has not received the goods (status_flag InTransit on AR; no matching AP row yet), any such invoice that otherwise meets Appendix A remains in the settlement population. No affiliate AP is expected for those lines on the September 3 wire cycle.
- Do not drop InTransit AR from the sweep solely because the affiliate AP mirror has no matching row.
- Affiliates will book AP on receipt in September; those future AP bookings are not required for the September 3 parent receivable wire instruction.
- Controllers must discover InTransit Appendix A receivables by inspecting status_flag and ship_date on the AR extract and confirming the absence of a matching parent_invoice_ref on the AP mirror.

4. Foreign exchange
Governing August 31, 2026 month-end spots for converting affiliate local-currency AP to USD for tie-out:

- CAD per 1 USD: {CAD_PER_USD:.4f}
- MXN per 1 USD: {MXN_PER_USD:.4f}

Superseded rates (do not use for this certificate):
- July 31, 2026 CAD per 1 USD: {STALE_CAD_PER_USD:.4f} (may still appear as fx_rate_used on some Canada AP bookings)
- July average CAD and MXN rates in the treasury dashboard footnote

Conversion formula for tie-out: USD equivalent = local currency amount ÷ (foreign units per 1 USD).

Stale FX booking treatment: any Open affiliate AP row included in the matched Appendix A tie-out whose fx_rate_used differs from the August 31 memo spot for that currency must be revalued at the memo spot for the tie-out column. Controllers identify stale bookings by comparing fx_rate_used on the AP mirror to the rates in this section. Quantify the USD difference versus the related parent invoice USD. The cash settlement / wire for that pair remains the parent invoice USD under section 5.

5. Settlement currency hierarchy
Parent USD invoice amounts govern the cash settlement. Affiliate AP local balances are converted at the August 31 memo spots solely to tie out and to quantify FX differences. Do not replace parent invoice USD with the converted AP USD when instructing wires. Present both the parent AR settlement total and the memo-converted AP total so Treasury can see the FX tie-out without changing the wire basis.

6. Voids, duplicates, and orphans
Apply these status and reference rules after selecting the Appendix A AR population and candidate AP tie-out rows. Controllers must discover affected rows from status_flag, parent_invoice_ref, and duplicate indicators on the ledger extracts — this memo does not enumerate the exception IDs.

- Void AR: any AR row with status_flag Void is excluded from settlement and from the September 3 wire, even if the dollar amount would otherwise meet materiality.
- Void AP / duplicate AP: any AP row with status_flag Void is excluded from the AP FX tie-out and is not wired. When more than one AP row references the same parent_invoice_ref and one of those rows is Void (including a voided duplicate of an Open payable), exclude the Void row and retain only the eligible Open payable for tie-out.
- Orphan AP: any Open AP row with a blank parent_invoice_ref is an orphan payable. Exclude it from the Canada / Mexico settlement net. Route it to entity controllers for local AP reclass; do not wire against it on September 3.
- Matched AP only: for FX tie-out, include only Open (non-void, non-orphan) AP rows whose parent_invoice_ref equals an Appendix A AR invoice ID that is included in settlement. Missing AP for InTransit Appendix A AR is expected and is not an orphan.

Document each discovered exception in the settlement workbook with the record ID, counterparty, exception type, source fact, governing memo rule, treatment, and settlement impact.

7. Netting recommendation format
Present, in USD:
(a) Appendix A AR settlement total by counterparty (Canada; Mexico), including InTransit invoices that meet Appendix A and the FOB cut-off rule;
(b) matched Appendix A AP converted at memo FX (excluding voids, orphans, and missing in-transit AP);
(c) FX tie-out difference on matched pairs only, after revaluing any stale fx_rate_used bookings to the August 31 memo spots;
(d) recommended September 3 wire: Canada pays parent the Canada Appendix A AR total; Mexico pays parent the Mexico Appendix A AR total.

State the September 3 recommendation by counterparty for disbursement authorization. Distinguish settlement amounts (parent AR USD) from exception items that are logged but not wired.

8. Prior-period note
July and early-August Settled items remain on the extracts for audit trail only. Do not re-sweep them. Provisional estimates remain out of scope until Controllers replace them with final invoices in a later cycle.

End of memo.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    assert len(text.split()) >= 500, len(text.split())


def main() -> None:
    TASK_INPUTS.mkdir(parents=True, exist_ok=True)
    write_ar(TASK_INPUTS / AR_CSV)
    write_ap(TASK_INPUTS / AP_CSV)
    write_memo(TASK_INPUTS / MEMO_TXT)
    print(f"Wrote {TASK_INPUTS}")
    for p in sorted(TASK_INPUTS.iterdir()):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
