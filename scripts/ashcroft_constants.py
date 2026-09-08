"""Constants for Ashcroft Foods single-claim coverage determination."""

from __future__ import annotations

SLUG = "ashcroft-foods-claims-coverage"
ENTITY = "Ashcroft Foods"
ENTITY_SLUG = "ashcroft-foods"
CLAIM_ID = "CLM-CP-2025-8841"
POLICY = "CP-OH-448291"
LOSS_DATE = "2025-11-18"
REPORT_DATE = "2025-11-19"
EVAL_DATE = "2025-12-05"
COMMITTEE_DATE = "2025-12-12"
LOCATION = "Dayton, OH — Zone B freezer"

# lot_id, description, qty, unit_cost, unit_sell, line_cost, status, covered_stock
LOTS = [
    ("LOT-B-201", "IQF chicken thighs 40lb", 418, 115.35, 168.40, 48216.30, "Open", True),
    ("LOT-B-218", "Ground beef 80/20 20lb", 512, 119.81, 174.25, 61342.72, "Open", True),
    ("LOT-B-230", "Pork loin boneless 20lb", 287, 136.28, 198.90, 39112.36, "Open", True),
    ("LOT-B-441", "Turkey breast roast 30lb", 140, 300.71, 421.50, 42099.40, "Open-Salvage", True),
    ("LOT-B-256", "Pollock fillets 15lb", 356, 109.32, 159.80, 38917.92, "Open", True),
    ("LOT-B-271", "Mixed vegetables 30lb", 214, 115.09, 162.40, 24629.26, "Open", True),
    ("PKG-991", "Corrugated freezer cartons", 2200, 5.19, 8.25, 11418.00, "Open", False),
    ("LOT-B-099", "Withdrawn sample cartons", 40, 205.00, 290.00, 8200.00, "VOID", False),
    ("LOT-B-218-DUP", "Ground beef 80/20 20lb (rekey)", 512, 120.12, 174.25, 61501.44, "Duplicate", False),
]

COVERED_STOCK_COST = round(sum(r[5] for r in LOTS if r[7]), 2)  # 254317.96
assert COVERED_STOCK_COST == 254317.96, COVERED_STOCK_COST

SALVAGE_LOT = "LOT-B-441"
SALVAGE_LOT_COST = 42099.40
SALVAGE_RATE = 0.30
SALVAGE_AMOUNT = round(SALVAGE_LOT_COST * SALVAGE_RATE, 2)  # 12629.82
NET_AFTER_SALVAGE = round(COVERED_STOCK_COST - SALVAGE_AMOUNT, 2)  # 241688.14
COINSURANCE_FACTOR = 0.75
AFTER_COINSURANCE = round(NET_AFTER_SALVAGE * COINSURANCE_FACTOR, 2)  # 181266.11
SPOILAGE_DEDUCTIBLE = 5000.00
SUPERSEDED_DEDUCTIBLE = 10000.00
CASE_RESERVE = round(AFTER_COINSURANCE - SPOILAGE_DEDUCTIBLE, 2)  # 176266.11

# EQ-01..EQ-05 component quotes (source of truth for equipment demand footing)
EQUIPMENT_LINES = (
    ("EQ-01", "Compressor #3 rebuild / replace core", 61240.00),
    ("EQ-02", "Ammonia charge and leak test", 8840.50),
    ("EQ-03", "Controls board and sensors", 6912.10),
    ("EQ-04", "Crane / after-hours premium", 4525.00),
    ("EQ-05", "Temp logger calibration (Zone B)", 1000.00),
)
EQUIPMENT_COMPONENT_TOTAL = round(sum(r[2] for r in EQUIPMENT_LINES), 2)  # 82517.60
# Prior worksheet EQ-SUB overstated by $2,000 before desk footing (documented in N-09)
EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL = 84517.60
EQUIPMENT_FOOTING_VARIANCE = round(
    EQUIPMENT_PRIOR_MISSTATED_SUBTOTAL - EQUIPMENT_COMPONENT_TOTAL, 2
)  # 2000.00
EQUIPMENT_REPAIR = EQUIPMENT_COMPONENT_TOTAL  # footed EQ-SUB after desk correction
BI_CLAIMED = 67240.00
OUTAGE_HOURS = 14
BI_WAITING_HOURS = 72

OEM_SERVICE_DAYS = 90  # must appear in claim-file Adjuster Note N-02
LAST_SERVICE = "2025-08-12"
DAYS_SINCE_SERVICE = 98  # LOSS_DATE − LAST_SERVICE
GRACE_DAYS = 7
VENDOR_CANCEL_DATE = "2025-11-10"
VENDOR_CANCEL_DAYS_BEFORE_LOSS = 8  # within 14-day safe-harbor window
MAINTENANCE_THRESHOLD = OEM_SERVICE_DAYS + GRACE_DAYS  # 97
assert DAYS_SINCE_SERVICE > MAINTENANCE_THRESHOLD  # triggers 25% coinsurance

CLAIMED_SELL_COVERED = round(sum(round(r[2] * r[4], 2) for r in LOTS if r[7]), 2)

DELIVERABLE = f"claim_coverage_opinion_{ENTITY_SLUG}.xlsx"
CLAIM_FILE = f"{ENTITY_SLUG}_claim_file.xlsx"
POLICY_FILE = f"{ENTITY_SLUG}_policy_schedule.csv"
MEMO_FILE = "coverage_investigation_memo.txt"
