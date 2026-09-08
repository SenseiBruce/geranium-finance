"""Constants for Haverford Process Equipment month-end GL flux close pack."""

from __future__ import annotations

SLUG = "haverford-process-equipment-gl-flux-close"
ENTITY = "Haverford Process Equipment"
ENTITY_LEGAL = "Haverford Process Equipment LLC"
LOCATION = "Lebanon, PA"
PERIOD = "2026-08"
PRIOR_PERIOD = "2026-07"
SOFT_CLOSE = "2026-09-05"
DELIVERABLE = "flux_close_pack_haverford-process-equipment.xlsx"
TB_XLSX = "haverford-process-equipment_trial_balance.xlsx"
SUPPORT_CSV = "haverford-process-equipment_support_schedules.csv"
MEMO_TXT = "flux_threshold_and_aje_memo.txt"

# Materiality / threshold rules (memo)
PNL_FLUX_ABS = 15_000.00
PNL_FLUX_PCT = 0.10
BS_FLUX_ABS = 25_000.00
CAPEX_MIN = 5_000.00
CAPEX_MIN_LIFE_YEARS = 1

# --- AJE amounts (golden) ---
VOID_JE_AMT = 55_280.40  # voided sales still in AR/Revenue
WARRANTY_TB = 182_440.55
WARRANTY_SUPPORT = 147_885.18  # W-04 governing support total
# Detail roll W-01+W-02+W-03 (authentic source gap vs W-04; do not silently erase)
WARRANTY_DETAIL_ROLL = round(176_110.55 - 41_220.18 + 18_994.81, 2)  # 153,885.18
WARRANTY_SOURCE_VARIANCE = round(WARRANTY_DETAIL_ROLL - WARRANTY_SUPPORT, 2)  # 6,000.00
WARRANTY_AJE = round(WARRANTY_TB - WARRANTY_SUPPORT, 2)  # 34,555.37 reduce liability to W-04

PREPAID_ANNUAL = 101_007.00
PREPAID_AUG_AMORT = round(PREPAID_ANNUAL / 12, 2)  # 8,417.25

INV_TB = 1_248_300.18
INV_PHYSICAL = 1_219_874.55
INV_WRITE_DOWN = round(INV_TB - INV_PHYSICAL, 2)  # 28,425.63

FREIGHT_OPEN = 41_288.40

PTO_TB = 95_220.18
PTO_SUPPORT = 71_440.55
PTO_AJE = round(PTO_TB - PTO_SUPPORT, 2)  # 23,779.63 reduce liability

CAPEX_REBUILD = 62_418.55  # misclassed in maintenance

CLOSE_STATUS = "Ready with AJEs"

assert WARRANTY_AJE == 34_555.37
assert WARRANTY_DETAIL_ROLL == 153_885.18
assert WARRANTY_SOURCE_VARIANCE == 6_000.00
assert PREPAID_AUG_AMORT == 8_417.25
assert INV_WRITE_DOWN == 28_425.63
assert PTO_AJE == 23_779.63

# Account catalog: (acct, name, type, normal)
ACCOUNTS = [
    ("1000", "Cash - Operating", "BS", "debit"),
    ("1100", "Accounts Receivable", "BS", "debit"),
    ("1200", "Inventory - Finished & WIP", "BS", "debit"),
    ("1400", "Prepaid Insurance", "BS", "debit"),
    ("1500", "Prepaid Other", "BS", "debit"),
    ("1600", "PP&E - Machinery", "BS", "debit"),
    ("1650", "Accumulated Depreciation", "BS", "credit"),
    ("2000", "Accounts Payable", "BS", "credit"),
    ("2100", "Accrued Payroll", "BS", "credit"),
    ("2200", "Accrued Warranty", "BS", "credit"),
    ("2210", "Accrued Freight", "BS", "credit"),
    ("2220", "Accrued PTO", "BS", "credit"),
    ("2300", "Customer Deposits", "BS", "credit"),
    ("2500", "Notes Payable - Current", "BS", "credit"),
    ("3000", "Common Stock", "BS", "credit"),
    ("3100", "Retained Earnings", "BS", "credit"),
    ("4100", "Product Sales", "PL", "credit"),
    ("4200", "Service & Parts Revenue", "PL", "credit"),
    ("4300", "Freight Billed to Customers", "PL", "credit"),
    ("5100", "Cost of Goods Sold", "PL", "debit"),
    ("5200", "Warranty Expense", "PL", "debit"),
    ("5300", "Insurance Expense", "PL", "debit"),
    ("5400", "Freight-In / Outbound", "PL", "debit"),
    ("5500", "Payroll Benefits / PTO", "PL", "debit"),
    ("5600", "Maintenance & Repairs", "PL", "debit"),
    ("5700", "Utilities", "PL", "debit"),
    ("5800", "Professional Fees", "PL", "debit"),
    ("5900", "Office & Admin", "PL", "debit"),
    ("6100", "Depreciation Expense", "PL", "debit"),
    ("6200", "Interest Expense", "PL", "debit"),
]

def _plug_re(period: dict) -> None:
    """Force TB equality by plugging Retained Earnings (credit)."""
    debit = credit = 0.0
    for acct, _name, _typ, norm in ACCOUNTS:
        if acct == "3100":
            continue
        v = float(period[acct])
        if norm == "debit":
            debit += v
        else:
            credit += v
    period["3100"] = round(debit - credit, 2)


# July (prior) natural-balance amounts
JUL = {
    "1000": 428_610.22,
    "1100": 1_084_220.55,
    "1200": 1_196_880.40,
    "1400": 92_589.75,
    "1500": 18_440.18,
    "1600": 3_842_110.55,
    "1650": 1_628_440.18,
    "2000": 612_880.40,
    "2100": 148_220.18,
    "2200": 176_110.55,
    "2210": 22_440.00,
    "2220": 88_110.40,
    "2300": 95_220.18,
    "2500": 420_000.00,
    "3000": 100_000.00,
    "3100": 0.0,  # plugged
    "4100": 1_842_110.55,
    "4200": 214_880.40,
    "4300": 38_220.18,
    "5100": 1_128_440.55,
    "5200": 42_110.18,
    "5300": 7_840.00,
    "5400": 61_220.55,
    "5500": 28_440.18,
    "5600": 48_220.55,
    "5700": 22_880.40,
    "5800": 31_110.18,
    "5900": 41_220.55,
    "6100": 64_880.40,
    "6200": 18_440.18,
}

# August TB before required AJEs (includes traps)
AUG = {
    "1000": 401_228.40,
    "1100": 1_162_880.40,
    "1200": INV_TB,
    "1400": 92_589.75,
    "1500": 16_110.55,
    "1600": 3_842_110.55,
    "1650": 1_693_320.58,
    "2000": 638_440.55,
    "2100": 151_880.40,
    "2200": WARRANTY_TB,
    "2210": 0.00,
    "2220": PTO_TB,
    "2300": 88_110.55,
    "2500": 405_000.00,
    "3000": 100_000.00,
    "3100": 0.0,  # plugged
    "4100": 1_978_440.18,
    "4200": 228_110.55,
    "4300": 41_880.40,
    "5100": 1_204_220.18,
    "5200": 38_880.40,
    "5300": 0.00,
    "5400": 58_110.55,
    "5500": 31_220.18,
    "5600": 118_880.40,
    "5700": 24_110.18,
    "5800": 29_440.55,
    "5900": 43_880.40,
    "6100": 64_880.40,
    "6200": 17_880.40,
}

_plug_re(JUL)
_plug_re(AUG)


def flux(acct: str) -> float:
    """August minus July on natural-balance amounts."""
    return round(AUG[acct] - JUL[acct], 2)
