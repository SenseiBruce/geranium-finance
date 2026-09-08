#!/usr/bin/env python3
"""Shared constants for Meridian Commons CAM true-up task."""

from __future__ import annotations

# Shares sum to 100.0 including vacant suite T-122.
TENANTS = [
    {
        "suite": "T-101",
        "tenant": "Harbor Coffee Co",
        "gla_sf": 1680,
        "prorata_pct": 10.2,
        "cam_cap_psf": None,
        "includes_marketing": False,
        "vacancy_clause": "owner_absorbs",
    },
    {
        "suite": "T-104",
        "tenant": "Ridgeway Dental",
        "gla_sf": 2840,
        "prorata_pct": 17.2,
        "cam_cap_psf": 4.85,
        "includes_marketing": False,
        "vacancy_clause": "owner_absorbs",
    },
    {
        "suite": "T-107",
        "tenant": "Meridian Outfitters",
        "gla_sf": 3720,
        "prorata_pct": 22.5,
        "cam_cap_psf": None,
        "includes_marketing": True,
        "vacancy_clause": "tenants_absorb",
    },
    {
        "suite": "T-112",
        "tenant": "Lakeside Books",
        "gla_sf": 1820,
        "prorata_pct": 11.0,
        "cam_cap_psf": None,
        "includes_marketing": False,
        "vacancy_clause": "owner_absorbs",
    },
    {
        "suite": "T-118",
        "tenant": "Contour Fitness",
        "gla_sf": 4480,
        "prorata_pct": 27.1,
        "prorata_pct_h1": 18.2,
        "cam_cap_psf": None,
        "includes_marketing": False,
        "vacancy_clause": "tenants_absorb",
        "expansion_date": "2025-07-01",
    },
    {
        "suite": "T-122",
        "tenant": "VACANT",
        "gla_sf": 1960,
        "prorata_pct": 12.0,
        "cam_cap_psf": None,
        "includes_marketing": False,
        "vacancy_clause": "n/a",
        "vacant": True,
    },
]

ROOF_CAPITAL = 186_420.00
HVAC_REPLACEMENT = 42_850.00
DUP_LANDSCAPING = 3_240.00
INSURANCE = 118_600.00
MARKETING = 27_480.00

# Eligible shared CAM pool after removing capital, insurance, marketing, and one duplicate.
TARGET_ELIGIBLE_POOL = 412_680.00

# Prior estimated CAM billed in 2025 (Contour at H1 share all year).
PRIOR_BILLINGS = {
    "T-101": 43_200.00,
    "T-104": 13_774.00,
    "T-107": 98_400.00,
    "T-112": 46_800.00,
    "T-118": 92_160.00,
}
