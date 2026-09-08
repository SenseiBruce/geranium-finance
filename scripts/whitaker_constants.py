"""Constants for Whitaker Precision Components commercial loan underwriting."""

from __future__ import annotations

SLUG = "whitaker-precision-components-loan-underwriting"
ENTITY = "Whitaker Precision Components"
ENTITY_LEGAL = "Whitaker Precision Components LLC"
AS_OF = "2026-06-30"
FYE = "2025-12-31"
COMMITTEE_DATE = "2026-09-18"
APPLICATION_ID = "CL-2026-4418"
DELIVERABLE = "loan_underwriting_decision_whitaker-precision-components.xlsx"
FIN_XLSX = "whitaker-precision-components_borrower_financials.xlsx"
COLLATERAL_CSV = "whitaker-precision-components_collateral_schedule.csv"
MEMO_TXT = "credit_policy_and_exception_memo.txt"

# Request
REQUESTED = 2_847_500.00
REQUESTED_TENOR_MO = 84
PRICING_FACTOR_PER_1000_MO = 16.42  # memo SOFR+375 7-year level-pay factor

# Existing debt
EXISTING_ANNUAL_DS = 412_880.40
EXISTING_DEBT_BAL = 2_184_220.55

# EBITDA bridge (FY2025 reported in financials)
REPORTED_EBITDA = 1_248_620.18
ONE_TIME_GAIN = 185_400.00  # building parcel sale — inside reported EBITDA
OWNER_ADD_CLAIMED = 210_000.00
OWNER_ADD_ALLOWED = 84_220.55
RELATED_PARTY_RENT_ADD_CLAIMED = 96_000.00  # do not add back

ADJ_EBITDA = round(REPORTED_EBITDA - ONE_TIME_GAIN + OWNER_ADD_ALLOWED, 2)
assert ADJ_EBITDA == 1_147_440.73

# Fake "management" EBITDA used in stale RM note
MGMT_EBITDA = round(
    REPORTED_EBITDA + OWNER_ADD_CLAIMED + RELATED_PARTY_RENT_ADD_CLAIMED, 2
)
assert MGMT_EBITDA == 1_554_620.18

# Policy thresholds
MIN_DSCR = 1.25
COND_DSCR_FLOOR = 1.15
MAX_LTV = 0.75
MAX_LEVERAGE = 3.50
OFFICER_LIMIT = 2_000_000.00
CNC_ADVANCE = 0.80
FIXTURE_ADVANCE = 0.50

# Collateral NOLV (appraisal)
CNC_HAAS_NOLV = 485_220.18
CNC_DMG_NOLV = 612_880.40
CNC_MAZAK_NOLV = 728_440.55
FIXTURES_NOLV = 214_880.40
BUILDING_RP_NOLV = 1_850_000.00  # related-party — ineligible
OBSOLETE_NOLV = 12_400.55  # age > policy — 0% advance
SOFT_COST = 95_220.18  # deposits/freight — 0%
FORKLIFT_LEASE_NOLV = 28_440.00  # leased — ineligible

ELIGIBLE_NOLV = round(
    CNC_HAAS_NOLV + CNC_DMG_NOLV + CNC_MAZAK_NOLV + FIXTURES_NOLV, 2
)
assert ELIGIBLE_NOLV == 2_041_421.53

BANKABLE = round(
    round(CNC_HAAS_NOLV * CNC_ADVANCE, 2)
    + round(CNC_DMG_NOLV * CNC_ADVANCE, 2)
    + round(CNC_MAZAK_NOLV * CNC_ADVANCE, 2)
    + round(FIXTURES_NOLV * FIXTURE_ADVANCE, 2),
    2,
)
assert BANKABLE == 1_568_673.10

MAX_BY_LTV = round(ELIGIBLE_NOLV * MAX_LTV, 2)
assert MAX_BY_LTV == 1_531_066.15

COMMITMENT = min(BANKABLE, MAX_BY_LTV)
assert COMMITMENT == 1_531_066.15


def annual_debt_service(principal: float) -> float:
    monthly = round((float(principal) / 1000.0) * PRICING_FACTOR_PER_1000_MO, 2)
    return round(monthly * 12, 2)


PROPOSED_DS_FULL = annual_debt_service(REQUESTED)
assert PROPOSED_DS_FULL == 561_071.40
TOTAL_DS_FULL = round(EXISTING_ANNUAL_DS + PROPOSED_DS_FULL, 2)
assert TOTAL_DS_FULL == 973_951.80
DSCR_FULL = round(ADJ_EBITDA / TOTAL_DS_FULL, 4)
assert DSCR_FULL == 1.1781

PROPOSED_DS_SIZED = annual_debt_service(COMMITMENT)
assert PROPOSED_DS_SIZED == 301_681.32
TOTAL_DS_SIZED = round(EXISTING_ANNUAL_DS + PROPOSED_DS_SIZED, 2)
assert TOTAL_DS_SIZED == 714_561.72
DSCR_SIZED = round(ADJ_EBITDA / TOTAL_DS_SIZED, 4)
assert DSCR_SIZED == 1.6058

LTV_FULL = round(REQUESTED / ELIGIBLE_NOLV, 4)
assert LTV_FULL == 1.3949
LTV_SIZED = round(COMMITMENT / ELIGIBLE_NOLV, 4)
assert LTV_SIZED == 0.7500

TOTAL_DEBT_SIZED = round(EXISTING_DEBT_BAL + COMMITMENT, 2)
LEVERAGE_SIZED = round(TOTAL_DEBT_SIZED / ADJ_EBITDA, 4)
assert LEVERAGE_SIZED == 3.2379

PATH = "Approve with conditions"
CONDITIONS_TENOR_MO = 60  # memo shortens conditional path from 84 to 60
