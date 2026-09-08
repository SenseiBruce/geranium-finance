# Portal Section 2 — pelliston-wc-premium-audit

Generated: 2026-09-04 06:48 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/pelliston-wc-premium-audit/submission/golden.zip`

**Expected deliverable in prompt:** `pelliston_open_claims_triangle.xlsx`

**Files inside golden.zip:**

- `self_insured_wc_reserve_pelliston.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **27** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 27 |
| Positive | 23 (+85) |
| Negative | 4 (-18) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 88 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named self_insured_wc_reserve_pelliston.xlsx.
```

### Criterion 2 — `workbook_sections`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 195 / 500 |

**Criterion** (paste into text field):

```
The workbook includes retention-capped case reserves, accident-year IBNR, an excess/ceded bridge, a reserve rollforward, and a controller recommendation; equivalent section labels are acceptable.
```

### Criterion 3 — `si_case_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 103 / 500 |

**Criterion** (paste into text field):

```
Self-insured case reserves after retention caps and closed-claim removals total approximately $745,065.
```

### Criterion 4 — `large_loss_cap`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 100 / 500 |

**Criterion** (paste into text field):

```
CLM-2024-1187 self-insured case is capped at $350,000 rather than the uncapped TPA case of $412,800.
```

### Criterion 5 — `large_loss_excess`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 128 / 500 |

**Criterion** (paste into text field):

```
Excess above retention on CLM-2024-1187 is approximately $62,800 and is treated as ceded / excess recoverable, not SI liability.
```

### Criterion 6 — `closed_claim_removed`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 140 / 500 |

**Criterion** (paste into text field):

```
CLM-2024-0901 is removed from self-insured case inventory (case $0) based on December final payments in pelliston_claims_payment_ledger.csv.
```

### Criterion 7 — `subro_not_credited`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 121 / 500 |

**Criterion** (paste into text field):

```
CLM-2023-0442 keeps its case reserve without reducing it for the $64,250 expected subrogation that has not been received.
```

### Criterion 8 — `ibnr_factor_2025`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Accident year 2025 IBNR uses factor 0.52 from actuarial_funding_memo.txt.
```

### Criterion 9 — `ibnr_factor_2024`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Accident year 2024 IBNR uses factor 0.28 from actuarial_funding_memo.txt.
```

### Criterion 10 — `ibnr_paid_from_triangle`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 179 / 500 |

**Criterion** (paste into text field):

```
Accident-year IBNR bases use AY Triangle cumulative_paid_as_of_2025_12 as the cumulative paid component rather than Open Inventory open-claim paid alone for mature accident years.
```

### Criterion 11 — `ibnr_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 59 / 500 |

**Criterion** (paste into text field):

```
Total IBNR across accident years is approximately $333,679.
```

### Criterion 12 — `ibnr_2025_amount`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 50 / 500 |

**Criterion** (paste into text field):

```
Accident year 2025 IBNR is approximately $119,263.
```

### Criterion 13 — `beginning_reserve`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 81 / 500 |

**Criterion** (paste into text field):

```
The rollforward opening balance is $1,842,660.40 from actuarial_funding_memo.txt.
```

### Criterion 14 — `ending_reserve`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
Ending self-insured reserve at 2025-12-31 is approximately $1,078,744.
```

### Criterion 15 — `rollforward_identity`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 119 / 500 |

**Criterion** (paste into text field):

```
The rollforward presents beginning reserve, calendar-year paid, incurred, and ending reserve in a reconciling identity.
```

### Criterion 16 — `live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 180 / 500 |

**Criterion** (paste into text field):

```
Retention-capped case reserves use MIN formulas against a central retention assumption, and IBNR amounts are formula-driven as IBNR base times factor rather than solely hard-coded.
```

### Criterion 17 — `ay2024_conflict_documented`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 157 / 500 |

**Criterion** (paste into text field):

```
The workbook documents that AY2024 Open Inventory open-claim paid exceeds AY Triangle cumulative paid and records the selected Triangle paid source for IBNR.
```

### Criterion 18 — `memo_citation_retention`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 120 / 500 |

**Criterion** (paste into text field):

```
Retention capping documentation cites actuarial_funding_memo.txt for the $350,000 per-occurrence limit on CLM-2024-1187.
```

### Criterion 19 — `controller_book_amount`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | accuracy |
| Characters | 153 / 500 |

**Criterion** (paste into text field):

```
The controller recommendation states booking self-insured WC liability of approximately $1,078,744 at 2025-12-31 for audit and the bank certificate pack.
```

### Criterion 20 — `controller_flags_excess`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | subjective |
| Category | completeness |
| Characters | 117 / 500 |

**Criterion** (paste into text field):

```
The recommendation discloses the large-loss excess as carrier recoverable and does not rewrite excess policy wording.
```

### Criterion 21 — `paid_from_ledger`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 117 / 500 |

**Criterion** (paste into text field):

```
Calendar-year 2025 net paid in the rollforward comes from pelliston_claims_payment_ledger.csv with void pairs netted.
```

### Criterion 22 — `ay2022_factor`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Accident year 2022 IBNR uses factor 0.04 from actuarial_funding_memo.txt.
```

### Criterion 23 — `ay2023_factor`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Accident year 2023 IBNR uses factor 0.11 from actuarial_funding_memo.txt.
```

### Criterion 24 — `neg_credit_subro`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 159 / 500 |

**Criterion** (paste into text field):

```
The controller recommendation instructs Controllers to credit the $64,250 expected subrogation on CLM-2023-0442 against the SI reserve before cash is received.
```

### Criterion 25 — `neg_uncapped_large`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 133 / 500 |

**Criterion** (paste into text field):

```
The controller recommendation instructs Controllers to carry CLM-2024-1187 on the SI books at the full uncapped TPA case of $412,800.
```

### Criterion 26 — `neg_stale_factor`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 126 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends applying the superseded mid-year factor 0.40 to accident year 2025 IBNR instead of the confirmed 0.52.
```

### Criterion 27 — `neg_keep_closed`

| Field | Value |
|-------|-------|
| **Weight** | **-3** |
| Importance | Failure mode (important) |
| Type | negative |
| Category | accuracy |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
The controller recommendation instructs Controllers to keep CLM-2024-0901 in SI case inventory despite the December final-payment closure in the ledger.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 pelliston-wc-premium-audit
```
