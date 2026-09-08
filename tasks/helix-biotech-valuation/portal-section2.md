# Portal Section 2 — helix-biotech-valuation

Generated: 2026-09-08 09:27 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/helix-biotech-valuation/submission/golden.zip`

**Expected deliverable in prompt:** `valuation_draft.xlsx`

**Files inside golden.zip:**

- `valuation_draft.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **37** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 37 |
| Positive | 33 (+118) |
| Negative | 4 (-20) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named valuation_draft.xlsx.
```

### Criterion 2 — `workbook_organization`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 254 / 500 |

**Criterion** (paste into text field):

```
The workbook organizes content into sections covering assumptions, cohort/ARR build, revenue projections, DCF analysis, cap table pro forma, valuation summary, sensitivity analysis, and documentation notes. Equivalent section or tab names are acceptable.
```

### Criterion 3 — `primary_proceeds`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 85 / 500 |

**Criterion** (paste into text field):

```
The workbook records Series B primary proceeds of $28,000,000 per investor_brief.txt.
```

### Criterion 4 — `pre_money_valuation`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 79 / 500 |

**Criterion** (paste into text field):

```
The workbook records a $112,000,000 pre-money valuation per investor_brief.txt.
```

### Criterion 5 — `model_arr_base`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 309 / 500 |

**Criterion** (paste into text field):

```
The model uses normalized TTM ARR of approximately $38,106,380.40, derived from all eight unique 2024 Cohort Detail records in cohort_summary.xlsx (formula-linked quarterly totals reconciling to Quarterly Rollup $40,359,060.40) after excluding the pending enterprise renewal per investor_brief.txt Footnote 1.
```

### Criterion 6 — `pending_renewal_amount`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 161 / 500 |

**Criterion** (paste into text field):

```
The workbook labels Apex Diagnostics by name as the excluded pending renewal and states the exclusion amount as $2,252,680 ARR per investor_brief.txt Footnote 1.
```

### Criterion 7 — `safe_vesper_conversion`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 471 / 500 |

**Criterion** (paste into text field):

```
The workbook converts the Vesper Growth SAFE at the lower applicable price under the stated mechanics: $45,000,000 valuation cap and 20% discount to Series B price per cap_table.csv and investor_brief.txt, producing a valuation-cap price of approximately $2.6745/share ($45,000,000 / 16,825,600 FD pre-money shares), a discounted Series B price of approximately $5.3252/share ($6.6565 × 80%), selection of the lower cap price, and approximately 934,756 conversion shares.
```

### Criterion 8 — `safe_quorum_conversion`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 189 / 500 |

**Criterion** (paste into text field):

```
The workbook converts the Quorum Ventures SAFE using a $55,000,000 valuation cap with no discount per cap_table.csv and investor_brief.txt, yielding approximately 535,360 conversion shares.
```

### Criterion 9 — `series_b_price`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 161 / 500 |

**Criterion** (paste into text field):

```
The workbook records a Series B price of approximately $6.6565 per share, derived as $112,000,000 pre-money divided by 16,825,600 fully diluted pre-money shares.
```

### Criterion 10 — `post_money_fd_shares`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 378 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma records approximately 24,188,372 fully diluted post-money shares under the modeled 15% option-pool refresh case after SAFE conversions and Series B primary issuance, using an existing stock-plan option-pool base of 1,942,000 shares (Options rows only; Dr. Elena Ruiz unexercised advisor warrant excluded from pool inventory but retained in FD pre-money).
```

### Criterion 11 — `pool_refresh_15pct`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 90 / 500 |

**Criterion** (paste into text field):

```
The workbook documents a 15% post-money option pool refresh target per investor_brief.txt.
```

### Criterion 12 — `pool_lawyer_12pct`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 105 / 500 |

**Criterion** (paste into text field):

```
The workbook references the 12% post-money pool side letter from cap_table.csv as an alternate pool case.
```

### Criterion 13 — `cohort_live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 246 / 500 |

**Criterion** (paste into text field):

```
The cohort/ARR build derives the four 2024 quarterly totals with SUMIFS or equivalent source-linked formulas from retained inventory rows rather than hard-coded quarterly totals, and the revenue forecast references that normalized TTM ARR result.
```

### Criterion 14 — `ending_arr_live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 172 / 500 |

**Criterion** (paste into text field):

```
Each retained cohort inventory row computes ending ARR with a live formula from starting ARR, gross retention, expansion, and churn rather than a hard-coded ending balance.
```

### Criterion 15 — `forecast_live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 135 / 500 |

**Criterion** (paste into text field):

```
The revenue projection section projects forward ARR through five years with live formulas referencing assumptions or cohort/ARR inputs.
```

### Criterion 16 — `revenue_multiple_range`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 138 / 500 |

**Criterion** (paste into text field):

```
The valuation summary applies a revenue multiple between 5.5x and 7.0x to year-1 NTM ARR from the revenue forecast per investor_brief.txt.
```

### Criterion 17 — `downside_multiple_case`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 131 / 500 |

**Criterion** (paste into text field):

```
The valuation summary records a downside enterprise value using a 5.0x multiple on normalized model TTM ARR per investor_brief.txt.
```

### Criterion 18 — `dcf_wacc_range`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 124 / 500 |

**Criterion** (paste into text field):

```
The DCF analysis discounts free cash flows under both a 14% WACC case and a 16% WACC case per investor_brief.txt Footnote 3.
```

### Criterion 19 — `sensitivity_axes`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 150 / 500 |

**Criterion** (paste into text field):

```
The sensitivity analysis presents a two-dimensional table with retention (or retention-stress) cases on one axis and Y1 ARR growth rates on the other.
```

### Criterion 20 — `sensitivity_table`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 296 / 500 |

**Criterion** (paste into text field):

```
The sensitivity section recalculates forward Y1 ARR and peer-median valuation outputs from separate retention-stress and Y1 total-ARR-growth drivers, and the base-case peer-median result ties to the live revenue forecast without multiplying absolute trailing NRR onto Footnote 3 total ARR growth.
```

### Criterion 21 — `duplicate_expansion_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 172 / 500 |

**Criterion** (paste into text field):

```
The cohort/ARR build visibly retains the duplicate FY2023-Q2 expansion row from cohort_summary.xlsx, marks it excluded, and omits it from normalized ARR / quarterly totals.
```

### Criterion 22 — `fiscal_calendar_mapping`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 136 / 500 |

**Criterion** (paste into text field):

```
Documentation notes explain fiscal versus calendar quarter normalization using cohort_summary.xlsx per Footnote 2 in investor_brief.txt.
```

### Criterion 23 — `arr_bridge_notes`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 129 / 500 |

**Criterion** (paste into text field):

```
Documentation notes explain the ARR bridge between headline run-rate and normalized TTM ARR with citations to investor_brief.txt.
```

### Criterion 24 — `cap_table_ownership`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 434 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma lists ownership by individual holder from cap_table.csv (not a Founders & Employees rollup), includes Vesper and Quorum SAFE conversion shares, Forsyth Equity Series B pro-rata of approximately 1,625,000 shares, lead primary issuance, and the 15% option-pool refresh, shows Forsyth Equity post-round shares of approximately 8,125,000, and derives ownership as post-money shares divided by the modeled FD total.
```

### Criterion 25 — `brief_citations`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 135 / 500 |

**Criterion** (paste into text field):

```
Each conflict resolution in the documentation notes cites investor_brief.txt or a specific row in cohort_summary.xlsx or cap_table.csv.
```

### Criterion 26 — `dcf_valuation_output`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 219 / 500 |

**Criterion** (paste into text field):

```
The DCF analysis or valuation summary calculates a DCF-implied enterprise value range using a five-year explicit FCF forecast from the revenue projections and the 14% to 16% WACC range per investor_brief.txt Footnote 3.
```

### Criterion 27 — `dcf_multiple_reconciliation`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 140 / 500 |

**Criterion** (paste into text field):

```
The valuation summary compares or reconciles the DCF-implied valuation range with the 5.5x to 7.0x revenue-multiple range on year-1 NTM ARR.
```

### Criterion 28 — `series_a_share_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 104 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma records Forsyth Equity Series A preferred shares as 6,500,000 per cap_table.csv.
```

### Criterion 29 — `forsyth_prorata_primary`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 359 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma records Forsyth Equity Series B pro-rata primary proceeds of approximately $10,816,850.51 per investor_brief.txt and cap_table.csv, and corresponding pro-rata shares of approximately 1,625,000 derived as $10,816,850.51 divided by approximately $6.6565 Series B price per share ($112,000,000 pre-money / 16,825,600 FD pre-money shares).
```

### Criterion 30 — `notes_prorata_resolution`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 167 / 500 |

**Criterion** (paste into text field):

```
Documentation notes document Forsyth Equity's full pro-rata allocation from the $28,000,000 primary, explain why that allocation was used, and cite investor_brief.txt.
```

### Criterion 31 — `safe_vesper_principal`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 92 / 500 |

**Criterion** (paste into text field):

```
The workbook records the Vesper Growth SAFE invested amount as $2,500,000 per cap_table.csv.
```

### Criterion 32 — `safe_quorum_principal`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 94 / 500 |

**Criterion** (paste into text field):

```
The workbook records the Quorum Ventures SAFE invested amount as $1,750,000 per cap_table.csv.
```

### Criterion 33 — `series_a_price`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 178 / 500 |

**Criterion** (paste into text field):

```
The workbook identifies Forsyth Equity as the Series A Preferred holder and records the Series A Preferred price as $1.82 per share per cap_table.csv (not any other holder name).
```

### Criterion 34 — `notes_headline_arr_binding`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 156 / 500 |

**Criterion** (paste into text field):

```
Documentation notes instruct board pricing using the $42,100,000 headline run-rate ARR as the binding valuation basis despite investor_brief.txt Footnote 1.
```

### Criterion 35 — `notes_twelve_pct_binding_close`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 199 / 500 |

**Criterion** (paste into text field):

```
Documentation notes recommend closing the Series B using the 12% post-money pool side-letter from cap_table.csv as the final binding refresh without presenting the 15% investor_brief.txt requirement.
```

### Criterion 36 — `notes_sub_pre_money_close`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 158 / 500 |

**Criterion** (paste into text field):

```
Documentation notes recommend board acceptance of the Series B at a pre-money valuation below $112,000,000 without documented override per investor_brief.txt.
```

### Criterion 37 — `notes_mfn_cleared_false`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 240 / 500 |

**Criterion** (paste into text field):

```
Documentation notes assert that the Vesper Growth MFN has been cleared, that no better MFN terms exist, or that legal confirmation of MFN treatment has been received, despite cap_table.csv and investor_brief.txt leaving the MFN outstanding.
```

---

## Warnings

- [WARN] Criterion 35 (notes_twelve_pct_binding_close): Negative may mirror a positive omission (penalty-scope risk). Prefer an affirmative prohibited recommendation or decision.

---

## Section 2 check order

1. Upload **golden.zip**
2. Run **Golden Solution Files Quality Check**
3. Enter all rubric criteria (text + weight separately)
4. Run **Rubric Quality Check**
5. Run **Name Check**
6. Wait for auto-eval feedback boxes (~15–30 min) if submission needs revision

---

## Regenerate

```bash
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 helix-biotech-valuation
```
