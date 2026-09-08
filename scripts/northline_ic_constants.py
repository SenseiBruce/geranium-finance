"""Constants for Northline Industrial Holdings intercompany settlement."""

from __future__ import annotations

SLUG = "northline-industrial-holdings-intercompany"
ENTITY = "Northline Industrial Holdings"
AS_OF = "2026-08-31"
WIRE_DATE = "2026-09-03"
DELIVERABLE = "intercompany_settlement_northline-industrial-holdings.xlsx"
# Package author (git user.name for this repo) — set on golden workbook metadata
AUTHOR = "kinshuk.prasad"
AR_CSV = "northline-industrial-holdings_ar_subledger.csv"
AP_CSV = "northline-industrial-holdings_ap_mirror.csv"
MEMO_TXT = "intercompany_cutoff_and_fx_memo.txt"

# Memo-governing FX at Aug 31 close (foreign currency units per 1 USD)
CAD_PER_USD = 1.3724
MXN_PER_USD = 18.5800
STALE_CAD_PER_USD = 1.3680  # July close — Canada used on AP-C-441 (trap)

# Appendix A materiality (memo rule — discover population from AR ledger)
APPENDIX_A_MIN_USD = 35_000.00

# AR invoices (parent books USD) — Appendix A + known exceptions
AR_8841 = 185_420.18  # Canada tooling — in transit FOB shipper
AR_8790 = 92_880.40  # Canada components — matched
AR_8766 = 41_220.18  # Canada Jul management fee — matched
AR_8812 = 64_220.55  # Mexico spares — matched
AR_8855 = 128_440.00  # Mexico press rebuild — in transit
AR_8688 = 38_820.40  # Mexico consumables — matched
AR_8820_VOID = 15_500.00  # void duplicate — exclude

# Canada AP in CAD (source amounts)
AP_C_441_CAD = 127_060.39  # booked at stale July rate; ties to INV-AR-8790
AP_C_442_CAD = 56_570.58  # booked at memo rate; ties to INV-AR-8766
AP_C_448_DUP_CAD = AP_C_441_CAD  # duplicate of 441 — void
AP_C_455_ORPHAN_CAD = 22_840.55  # no parent AR — exclude

# Mexico AP in MXN (source amounts at memo rate)
AP_M_210_MXN = 1_193_217.82  # INV-AR-8812
AP_M_205_MXN = 721_283.03  # INV-AR-8688

# Per-row memo revaluation (round each conversion, then sum)
AP_C_441_USD_MEMO = round(AP_C_441_CAD / CAD_PER_USD, 2)  # 92,582.62
AP_C_441_USD_BOOKED = round(AP_C_441_CAD / STALE_CAD_PER_USD, 2)  # 92,880.40
AP_C_442_USD_MEMO = round(AP_C_442_CAD / CAD_PER_USD, 2)  # 41,220.18
AP_M_210_USD_MEMO = round(AP_M_210_MXN / MXN_PER_USD, 2)  # 64,220.55
AP_M_205_USD_MEMO = round(AP_M_205_MXN / MXN_PER_USD, 2)  # 38,820.40
AP_C_455_USD_MEMO = round(AP_C_455_ORPHAN_CAD / CAD_PER_USD, 2)

# AP-C-441 FX difference vs parent AR (evaluator figure)
AP_C_441_FX_DIFF = round(AR_8790 - AP_C_441_USD_MEMO, 2)  # 297.78

# Settlement USD = parent invoice USD (memo rule)
SETTLE_AR_CANADA = round(AR_8841 + AR_8790 + AR_8766, 2)  # 319,520.76
SETTLE_AR_MEXICO = round(AR_8812 + AR_8855 + AR_8688, 2)  # 231,480.95
SETTLE_AR_TOTAL = round(SETTLE_AR_CANADA + SETTLE_AR_MEXICO, 2)

# Matched-only AR (excludes in-transit) for FX tie-out
MATCHED_AR_CANADA = round(AR_8790 + AR_8766, 2)  # 134,100.58
MATCHED_AR_MEXICO = round(AR_8812 + AR_8688, 2)  # 103,040.95

# AP converted at memo month-end spot (matched only; sum of rounded rows)
SETTLE_AP_CANADA_USD = round(AP_C_441_USD_MEMO + AP_C_442_USD_MEMO, 2)  # 133,802.80
SETTLE_AP_MEXICO_USD = round(AP_M_210_USD_MEMO + AP_M_205_USD_MEMO, 2)  # 103,040.95

FX_DIFF_CANADA = round(MATCHED_AR_CANADA - SETTLE_AP_CANADA_USD, 2)  # 297.78
FX_DIFF_MEXICO = round(MATCHED_AR_MEXICO - SETTLE_AP_MEXICO_USD, 2)  # 0.00

# In-transit AR still in settlement instruction (FOB shipping point)
IN_TRANSIT_TOTAL = round(AR_8841 + AR_8855, 2)
ORPHAN_USD_AT_MEMO = AP_C_455_USD_MEMO
