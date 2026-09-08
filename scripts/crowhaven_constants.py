"""Constants for Crowhaven Logistics insured claims triangle reserve opinion."""

from __future__ import annotations

SLUG = "crowhaven-logistics-claims-triangle"
DELIVERABLE = "claims_reserve_opinion_crowhaven-logistics.xlsx"
SCAFFOLD = "claims_triangle_case_ibnr_opinion"
TOPOLOGY = (
    "Year-end commercial auto GL claims triangle with case vs IBNR "
    "for insured program (not SI)"
)

ENTITY = "Crowhaven Logistics"
POLICY = "PKG-CA-GL-IN-2025-4418"
EVAL_DATE = "2025-12-31"
RENEWAL_DATE = "2026-03-01"

# Year-end paid LDFs to ultimate (governing — actuarial_factor_memo.txt)
LDF = {
    12: 1.82,
    24: 1.41,
    36: 1.18,
    48: 1.06,
}

# Stale mid-year LDFs still printed on triangle Definitions (superseded)
STALE_LDF = {
    12: 1.65,
    24: 1.28,
    36: 1.12,
    48: 1.03,
}

AY_AGE_MONTHS = {
    2022: 48,
    2023: 36,
    2024: 24,
    2025: 12,
}

# Latest diagonal cumulative paid by accident year (includes large-loss paid in 2023)
CUM_PAID = {
    2022: 412_840.55,
    2023: 628_410.22,
    2024: 391_220.18,
    2025: 148_640.55,
}

CLAIM_LARGE = "CLM-AUTO-2023-4412"
CLAIM_LARGE_PAID = 185_220.40
CLAIM_LARGE_CASE = 142_880.40

CLAIM_CLOSED_STALE = "CLM-AUTO-2024-0908"
CLAIM_CLOSED_STALE_CASE = 18_220.00

CLAIM_DUP = "CLM-GL-2025-0144"
CLAIM_DUP_CASE_OLD = 22_400.00
CLAIM_DUP_CASE_NEW = 19_850.55  # later as_of wins

CLAIM_VOID = "CLM-AUTO-2024-0000"

EARNED_PREMIUM = 2_850_220.40
TARGET_LR = 0.685  # 68.5%
REFER_LR = 0.685
DECLINE_LR = 0.85

# Booked beginning reserve (memo only — for opinion context, not SI rollforward)
BEGINNING_BOOKED_RESERVE = 1_104_220.18
