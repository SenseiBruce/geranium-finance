# Golden ↔ Rubric evidence — northline-industrial-holdings-intercompany

Human verification after human-review repair (memo leakage + rubric double-count removal).

| Criterion theme | Golden evidence |
|-----------------|-----------------|
| Deliverable filename | `golden/intercompany_settlement_northline-industrial-holdings.xlsx` |
| Sections | AR_Settlement, AP_FX_TieOut, Exceptions, Counterparty_Netting, Recommendation, Notes |
| Appendix A six invoices | AR_Settlement rows INV-AR-8841/8790/8766/8812/8855/8688 (discovered via memo §2: Open/InTransit + ≥$35,000) |
| Total AR | F15 ≈ $551,001.71 |
| Canada / Mexico wires | F13 ≈ $319,520.76; F14 ≈ $231,480.95; Recommendation B5/B6 linked |
| InTransit FOB | INV-AR-8841 and INV-AR-8855 Include=Yes |
| Void AR | INV-AR-8820 Include=No |
| Memo FX | CAD 1.3724 / MXN 18.5800 on AP_FX_TieOut |
| AP-C-441 | Booked 1.3680 → memo 1.3724 → ~$92,582.62; FX diff ~$297.78 |
| Matched AP | AP-C-441/442, AP-M-210/205 with parent_invoice_ref |
| Void AP / orphan | AP-C-448 and AP-C-455 Include=No |
| Parent USD governs | Counterparty_Netting E5/E6 = AR totals |
| Exceptions table | Discovers InTransit, void, duplicate, orphan, stale FX with source facts |
| Negatives (retained) | Prohibited: stale CAD rate; Provisional settle; Settled re-sweep — golden does none |

Removed mirror negatives: neg_drop_intransit, neg_include_orphan, neg_settle_at_converted_ap, neg_settle_void_8820, neg_wire_void_ap.

Retained / added prohibited-decision negatives (no positive mirrors): stale CAD rate; Provisional settle; Settled re-sweep; below-$35k materiality settle.

Human verification: Canada 319520.76, Mexico 231480.95, Total 551001.71, AP-C-441 FX 297.78 — recomputed from the three input files after memo ID scrub.
