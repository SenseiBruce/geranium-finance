# Portal Section 2 — ironclad-telematics-valuation

Generated: 2026-09-04 11:49 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/ironclad-telematics-valuation/submission/golden.zip`

**Expected deliverable in prompt:** `ironclad_telematics_valuation.xlsx`

**Files inside golden.zip:**

- `ironclad_telematics_valuation.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **32** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 32 |
| Positive | 29 (+101) |
| Negative | 3 (-15) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 84 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named ironclad_telematics_valuation.xlsx.
```

### Criterion 2 — `workbook_organization`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 260 / 500 |

**Criterion** (paste into text field):

```
The workbook organizes content into sections covering assumptions, fleet cohort/ARR build, revenue projections, DCF analysis, cap table pro forma, valuation summary, sensitivity analysis, and documentation notes. Equivalent section or tab names are acceptable.
```

### Criterion 3 — `primary_proceeds`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 105 / 500 |

**Criterion** (paste into text field):

```
The workbook records growth-equity primary proceeds of $35,000,000 per growth_equity_diligence_brief.txt.
```

### Criterion 4 — `pre_money_valuation`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 94 / 500 |

**Criterion** (paste into text field):

```
The workbook records a $145,000,000 pre-money valuation per growth_equity_diligence_brief.txt.
```

### Criterion 5 — `model_arr_base`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 333 / 500 |

**Criterion** (paste into text field):

```
The model uses normalized TTM ARR of approximately $24,001,610.80, calculated as the sum of the four 2024 calendar-quarter totals from ironclad_fleet_cohort_arr.xlsx Fleet Rollup ($26,041,610.80) minus the MetroLink Transit Authority pilot_non_recurring amount of $2,040,000 excluded per growth_equity_diligence_brief.txt Footnote 1.
```

### Criterion 6 — `pilot_exclusion_amount`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 146 / 500 |

**Criterion** (paste into text field):

```
The workbook identifies MetroLink Transit Authority's excluded municipal pilot as $2,040,000 ARR per growth_equity_diligence_brief.txt Footnote 1.
```

### Criterion 7 — `note_a_conversion`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 166 / 500 |

**Criterion** (paste into text field):

```
The workbook converts the Octavian Capital Note A using a $50,000,000 valuation cap and 20% discount per ironclad_cap_table.csv and growth_equity_diligence_brief.txt.
```

### Criterion 8 — `note_b_conversion`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 163 / 500 |

**Criterion** (paste into text field):

```
The workbook converts the Vesper Growth Note B using a $65,000,000 valuation cap with no discount per ironclad_cap_table.csv and growth_equity_diligence_brief.txt.
```

### Criterion 9 — `note_a_principal`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 100 / 500 |

**Criterion** (paste into text field):

```
The workbook records the Octavian Capital Note A principal as $4,200,000 per ironclad_cap_table.csv.
```

### Criterion 10 — `note_b_principal`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
The workbook records the Vesper Growth Note B principal as $2,800,000 per ironclad_cap_table.csv.
```

### Criterion 11 — `pool_refresh_12pct`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 105 / 500 |

**Criterion** (paste into text field):

```
The workbook documents a 12% post-money option pool refresh target per growth_equity_diligence_brief.txt.
```

### Criterion 12 — `pool_counsel_10pct`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 139 / 500 |

**Criterion** (paste into text field):

```
The workbook references the 10% available-pool note from ironclad_cap_table.csv alongside the 12% growth_equity_diligence_brief.txt target.
```

### Criterion 13 — `cohort_live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 106 / 500 |

**Criterion** (paste into text field):

```
The fleet cohort/ARR build section calculates ending ARR with live formulas rather than hard-coded totals.
```

### Criterion 14 — `forecast_live_formulas`

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

### Criterion 15 — `revenue_multiple_range`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 153 / 500 |

**Criterion** (paste into text field):

```
The valuation summary applies a revenue multiple between 4.5x and 6.0x to year-1 NTM ARR from the revenue forecast per growth_equity_diligence_brief.txt.
```

### Criterion 16 — `downside_multiple_case`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 146 / 500 |

**Criterion** (paste into text field):

```
The valuation summary records a downside enterprise value using a 4.0x multiple on normalized model TTM ARR per growth_equity_diligence_brief.txt.
```

### Criterion 17 — `dcf_wacc_range`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 111 / 500 |

**Criterion** (paste into text field):

```
The DCF analysis or valuation summary references a 13% to 15% WACC range per growth_equity_diligence_brief.txt.
```

### Criterion 18 — `sensitivity_table`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 107 / 500 |

**Criterion** (paste into text field):

```
The sensitivity analysis varies both net retention and fleet growth assumptions in a two-dimensional table.
```

### Criterion 19 — `duplicate_expansion_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 139 / 500 |

**Criterion** (paste into text field):

```
Documentation notes state that the duplicate IC-2023-02-XP expansion row in ironclad_fleet_cohort_arr.xlsx is excluded from retention math.
```

### Criterion 20 — `fiscal_calendar_mapping`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 161 / 500 |

**Criterion** (paste into text field):

```
Documentation notes explain fiscal versus calendar period normalization using ironclad_fleet_cohort_arr.xlsx per Footnote 2 in growth_equity_diligence_brief.txt.
```

### Criterion 21 — `arr_bridge_notes`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 144 / 500 |

**Criterion** (paste into text field):

```
Documentation notes explain the ARR bridge between headline run-rate and normalized TTM ARR with citations to growth_equity_diligence_brief.txt.
```

### Criterion 22 — `cap_table_ownership`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 121 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma shows post-money ownership percentages that sum to 100% after note conversion and primary shares.
```

### Criterion 23 — `brief_citations`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 170 / 500 |

**Criterion** (paste into text field):

```
Each conflict resolution in the documentation notes cites growth_equity_diligence_brief.txt or a specific row in ironclad_fleet_cohort_arr.xlsx or ironclad_cap_table.csv.
```

### Criterion 24 — `dcf_valuation_output`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 223 / 500 |

**Criterion** (paste into text field):

```
The DCF analysis or valuation summary calculates a DCF-implied enterprise value range using a five-year explicit FCF forecast from the revenue projections and the 13% to 15% WACC range per growth_equity_diligence_brief.txt.
```

### Criterion 25 — `dcf_multiple_reconciliation`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 140 / 500 |

**Criterion** (paste into text field):

```
The valuation summary compares or reconciles the DCF-implied valuation range with the 4.5x to 6.0x revenue-multiple range on year-1 NTM ARR.
```

### Criterion 26 — `seed_share_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 106 / 500 |

**Criterion** (paste into text field):

```
The workbook records Quorum Ventures Series Seed preferred shares as 4,600,000 per ironclad_cap_table.csv.
```

### Criterion 27 — `quorum_prorata_primary`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 342 / 500 |

**Criterion** (paste into text field):

```
The cap table pro forma records Quorum Ventures pro-rata primary proceeds of $8,750,000.00 per growth_equity_diligence_brief.txt and corresponding pro-rata shares of approximately 1,110,344.83 derived as $8,750,000.00 divided by approximately $7.88043478 growth-round price per share ($145,000,000 pre-money / 18,400,000 FD pre-money shares).
```

### Criterion 28 — `notes_prorata_resolution`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 183 / 500 |

**Criterion** (paste into text field):

```
Documentation notes document Quorum Ventures's full pro-rata allocation from the $35,000,000 primary, explain why that allocation was used, and cite growth_equity_diligence_brief.txt.
```

### Criterion 29 — `fd_pre_share_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 93 / 500 |

**Criterion** (paste into text field):

```
The workbook records fully diluted pre-money shares as 18,400,000 per ironclad_cap_table.csv.
```

### Criterion 30 — `notes_headline_arr_binding`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 186 / 500 |

**Criterion** (paste into text field):

```
Documentation notes instruct the board to price the round using the $28,400,000 headline run-rate ARR as the binding valuation basis despite growth_equity_diligence_brief.txt Footnote 1.
```

### Criterion 31 — `notes_ten_pct_binding_close`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 202 / 500 |

**Criterion** (paste into text field):

```
Documentation notes instruct the board to close using the 10% available-pool note from ironclad_cap_table.csv as the final binding refresh and omit the 12% growth_equity_diligence_brief.txt requirement.
```

### Criterion 32 — `notes_skip_note_conversion`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 109 / 500 |

**Criterion** (paste into text field):

```
Documentation notes recommend closing the round with both convertible notes left outstanding and unconverted.
```

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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 ironclad-telematics-valuation
```
