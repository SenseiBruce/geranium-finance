"""Constants for Pelliston Machine Works self-insured WC reserve (attempt 2 redesign)."""

from __future__ import annotations

SLUG = "pelliston-wc-premium-audit"
DELIVERABLE = "self_insured_wc_reserve_pelliston.xlsx"

# Attempt 2 after portal Uniqueness FAIL on premium-audit true-up scaffold
SCAFFOLD = "self_insured_wc_reserve_rollforward"
TOPOLOGY = (
    "Year-end self-insured WC reserve with per-occurrence retention, "
    "accident-year IBNR factors, and pending subrogation"
)

PELLISTON = "Pelliston Machine Works"
FEIN = "34-2187741"
POLICY_SI = "SI-WC-OH-2025"

# Per-occurrence self-insured retention
RETENTION = 350_000.00

# Beginning SI reserve at 2024-12-31 (case + IBNR combined on books)
BEGINNING_RESERVE = 1_842_660.40

# Actuarial unpaid factors (IBNR as % of cumulative paid+case for open AYs) — from memo
# Applied to (paid_to_date + case) for immature years as development factor method
IBNR_FACTORS = {
    2022: 0.04,   # nearly mature
    2023: 0.11,
    2024: 0.28,
    2025: 0.52,   # current AY
}

# Large loss claim — case reserve before retention cap
CLAIM_LARGE = "CLM-2024-1187"
CLAIM_LARGE_CASE = 412_800.00  # must cap SI share at RETENTION; excess is carrier
CLAIM_LARGE_PAID_YTD = 88_420.18

# Subrogation pending — do NOT credit until cash received per memo
CLAIM_SUBRO = "CLM-2023-0442"
CLAIM_SUBRO_EXPECTED = 64_250.00
CLAIM_SUBRO_CASE = 41_200.00

# Stale prior actuarial factor someone might misuse
STALE_2025_FACTOR = 0.40  # prior mid-year estimate; memo confirms 0.52
