# Portal Section 2 — crowhaven-logistics-claims-triangle

Generated: 2026-09-07 09:34 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/crowhaven-logistics-claims-triangle/submission/golden.zip`

**Expected deliverable in prompt:** `claims_reserve_opinion_crowhaven-logistics.xlsx`

**Files inside golden.zip:**

- `claims_reserve_opinion_crowhaven-logistics.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **31** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 31 |
| Positive | 29 (+83) |
| Negative | 2 (-10) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | rigid |
| Category | deliverable |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named claims_reserve_opinion_crowhaven-logistics.xlsx.
```

### Criterion 2 — `section_case_inventory`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | subjective |
| Category | structure |
| Characters | 176 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a cleaned open-claim inventory applying the memo closed-claim, duplicate latest-as-of, and VOID exclusion rules; equivalent section labels are acceptable.
```

### Criterion 3 — `section_ay_development`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | subjective |
| Category | structure |
| Characters | 158 / 500 |

**Criterion** (paste into text field):

```
The workbook includes accident-year paid development applying the memo governing paid LDFs to the triangle diagonal; equivalent section labels are acceptable.
```

### Criterion 4 — `section_reserve_summary`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | rigid |
| Category | accuracy |
| Characters | 257 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a reserve opinion summary separately reporting cleaned case reserves of approximately $460,089.00, pure IBNR of approximately $94,892.67, and total reserve opinion of approximately $554,981.67; equivalent section labels are acceptable.
```

### Criterion 5 — `section_uw_recommendation`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | subjective |
| Category | structure |
| Characters | 150 / 500 |

**Criterion** (paste into text field):

```
The workbook includes an underwriting Quote/Refer/Decline recommendation section with a visible disposition; equivalent section labels are acceptable.
```

### Criterion 6 — `section_executive_explanation`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | subjective |
| Category | documentation |
| Characters | 191 / 500 |

**Criterion** (paste into text field):

```
The workbook explains the indicated ultimate loss ratio relative to the actuarial_factor_memo.txt referral threshold for executives and underwriters; equivalent section labels are acceptable.
```

### Criterion 7 — `governing_ldf_12`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 112 / 500 |

**Criterion** (paste into text field):

```
Accident year 2025 paid development uses the governing 12-month paid LDF of 1.82 from actuarial_factor_memo.txt.
```

### Criterion 8 — `governing_ldf_24`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 112 / 500 |

**Criterion** (paste into text field):

```
Accident year 2024 paid development uses the governing 24-month paid LDF of 1.41 from actuarial_factor_memo.txt.
```

### Criterion 9 — `governing_ldf_36`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 112 / 500 |

**Criterion** (paste into text field):

```
Accident year 2023 paid development uses the governing 36-month paid LDF of 1.18 from actuarial_factor_memo.txt.
```

### Criterion 10 — `governing_ldf_48`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 112 / 500 |

**Criterion** (paste into text field):

```
Accident year 2022 paid development uses the governing 48-month paid LDF of 1.06 from actuarial_factor_memo.txt.
```

### Criterion 11 — `memo_over_definitions`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
The workbook uses the year-end governing paid LDFs from actuarial_factor_memo.txt rather than the mid-year DRAFT LDFs on the triangle Definitions sheet.
```

### Criterion 12 — `closed_claim_removed`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 136 / 500 |

**Criterion** (paste into text field):

```
CLM-AUTO-2024-0908 is excluded from cleaned case reserves based on the TPA note that the file closed after the 2025-12-12 final payment.
```

### Criterion 13 — `void_ignored`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 94 / 500 |

**Criterion** (paste into text field):

```
CLM-AUTO-2024-0000 with VOID status and a $99,999 case is excluded from cleaned case reserves.
```

### Criterion 14 — `duplicate_latest_asof`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 148 / 500 |

**Criterion** (paste into text field):

```
For duplicate claim CLM-GL-2025-0144, cleaned case uses the 2025-12-28 as-of amount of $19,850.55 rather than the 2025-11-30 preliminary $22,400.00.
```

### Criterion 15 — `cleaned_case_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
Cleaned case reserves after closed-claim, VOID, and duplicate rules total approximately $460,089.
```

### Criterion 16 — `large_loss_paid_carved`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 117 / 500 |

**Criterion** (paste into text field):

```
Accident year 2023 attritional paid excludes CLM-AUTO-2023-4412 paid of $185,220.40 before applying the 36-month LDF.
```

### Criterion 17 — `large_loss_case_held`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 76 / 500 |

**Criterion** (paste into text field):

```
CLM-AUTO-2023-4412 case of $142,880.40 is retained in cleaned case reserves.
```

### Criterion 18 — `large_loss_no_triangle_ibnr`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 159 / 500 |

**Criterion** (paste into text field):

```
The workbook does not generate pure IBNR on the carved-out CLM-AUTO-2023-4412 paid dollars; large-loss indicated ultimate equals paid plus case for that claim.
```

### Criterion 19 — `ay2023_attritional_ultimate`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 79 / 500 |

**Criterion** (paste into text field):

```
Accident year 2023 attritional indicated ultimate is approximately $522,963.99.
```

### Criterion 20 — `ay2024_ultimate`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 67 / 500 |

**Criterion** (paste into text field):

```
Accident year 2024 indicated ultimate is approximately $551,620.45.
```

### Criterion 21 — `ay2025_ultimate`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 67 / 500 |

**Criterion** (paste into text field):

```
Accident year 2025 indicated ultimate is approximately $270,525.80.
```

### Criterion 22 — `pure_ibnr_definition`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 160 / 500 |

**Criterion** (paste into text field):

```
Pure IBNR by accident year equals max(0, attritional ultimate minus attritional paid minus attritional cleaned case), so case is not double-counted inside IBNR.
```

### Criterion 23 — `pure_ibnr_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 66 / 500 |

**Criterion** (paste into text field):

```
Total pure IBNR across accident years is approximately $94,892.67.
```

### Criterion 24 — `total_reserve_opinion`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 81 / 500 |

**Criterion** (paste into text field):

```
Total reserve opinion (cleaned case plus pure IBNR) is approximately $554,981.67.
```

### Criterion 25 — `indicated_ultimate_total`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 64 / 500 |

**Criterion** (paste into text field):

```
Total indicated ultimate losses are approximately $2,110,822.02.
```

### Criterion 26 — `earned_premium_basis`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | rigid |
| Category | method |
| Characters | 106 / 500 |

**Criterion** (paste into text field):

```
Indicated ultimate loss ratio uses subject earned premium of $2,850,220.40 from actuarial_factor_memo.txt.
```

### Criterion 27 — `indicated_lr`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 54 / 500 |

**Criterion** (paste into text field):

```
Indicated ultimate loss ratio is approximately 74.06%.
```

### Criterion 28 — `recommendation_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | judgment |
| Characters | 182 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends Refer and supports that decision with the calculated 74.06% indicated ultimate loss ratio and the memo thresholds of 68.5% for referral and 85.0% for decline.
```

### Criterion 29 — `live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+1** |
| Importance | Minor |
| Type | subjective |
| Category | structure |
| Characters | 147 / 500 |

**Criterion** (paste into text field):

```
Accident-year development uses live spreadsheet formulas for attritional paid, ultimate, pure IBNR, and totals rather than only hard-coded results.
```

### Criterion 30 — `neg_quote_despite_refer_lr`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | judgment |
| Characters | 253 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends Quote at standard authority, or instructs underwriting to bind or renew Crowhaven at expiring terms with no regional referral, despite an indicated ultimate loss ratio above the 68.5% refer threshold in actuarial_factor_memo.txt.
```

### Criterion 31 — `neg_decline_in_refer_band`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | judgment |
| Characters | 173 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends Decline for the 2026-03-01 Crowhaven renewal despite an indicated ultimate loss ratio below the 85.0% decline threshold in actuarial_factor_memo.txt.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 crowhaven-logistics-claims-triangle
```
