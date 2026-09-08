#!/usr/bin/env python3
"""Shared Helix task constants — keep inputs and golden aligned."""

from __future__ import annotations

# Investors / counterparties — mixed institutional styles (avoid LLM compound geo/nature clusters)
LEAD_INVESTOR = "Octavian Capital"
SERIES_A_INVESTOR = "Forsyth Equity"
SAFE_BIRCHWOOD = "Vesper Growth"
SAFE_STONEGATE = "Quorum Ventures"
PENDING_CUSTOMER = "Apex Diagnostics"

PENDING_RENEWAL_ARR = 2_252_680
ROLLUP_TTM_2024 = 40_359_060.40
MODEL_ARR_NORMALIZED = ROLLUP_TTM_2024 - PENDING_RENEWAL_ARR
BRIEF_RUN_RATE = 42_100_000

PRE_MONEY = 112_000_000
PRIMARY = 28_000_000
POST_MONEY = 140_000_000
POOL_TARGET_PCT = 0.15
SERIES_A_SHARES = 6_500_000
SERIES_A_PRICE = 1.82
FD_PRE = 16_825_600
FOUNDERS_FD = FD_PRE - SERIES_A_SHARES  # 10,325,600 — sum of cap_table.csv ex Series A

SAFE1_INVEST = 2_500_000
SAFE1_CAP = 45_000_000
SAFE1_DISC = 0.20
SAFE2_INVEST = 1_750_000
SAFE2_CAP = 55_000_000

FCF_MARGIN = 0.22
MULT_LOW = 5.5
MULT_HIGH = 7.0
MULT_DOWN = 5.0
WACC_LOW = 0.14
WACC_HIGH = 0.16
TERMINAL_GROWTH = 0.03
FORECAST_GROWTH = [0.28, 0.24, 0.20, 0.16, 0.14]

ROLLUP_2024 = {
    "2024-Q1": 8_016_839.80,
    "2024-Q2": 9_280_427.00,
    "2024-Q3": 10_748_127.00,
    "2024-Q4": 12_313_666.60,
}
