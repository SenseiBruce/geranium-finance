# Portal Section 2 — whitaker-precision-components-loan-underwriting

Generated: 2026-09-06 02:58 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/whitaker-precision-components-loan-underwriting/submission/golden.zip`

**Expected deliverable in prompt:** `loan_underwriting_decision_whitaker-precision-components.xlsx`

**Files inside golden.zip:**

- `loan_underwriting_decision_whitaker-precision-components.xlsx`

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
| Positive | 27 (+107) |
| Negative | 5 (-23) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 111 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named loan_underwriting_decision_whitaker-precision-components.xlsx.
```

### Criterion 2 — `workbook_sections`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 219 / 500 |

**Criterion** (paste into text field):

```
The workbook includes an Adjusted EBITDA build, DSCR and leverage tests, a collateral eligibility and LTV analysis, an exception log, and a credit path decision with conditions; equivalent section labels are acceptable.
```

### Criterion 3 — `memo_hierarchy`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 184 / 500 |

**Criterion** (paste into text field):

```
The workbook states that credit_policy_and_exception_memo.txt governs over relationship-manager Approve-as-requested language in whitaker-precision-components_borrower_financials.xlsx.
```

### Criterion 4 — `reported_ebitda_start`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
The Adjusted EBITDA build starts from reported FY2025 EBITDA of approximately $1,248,620.18 from whitaker-precision-components_borrower_financials.xlsx.
```

### Criterion 5 — `one_time_gain_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 123 / 500 |

**Criterion** (paste into text field):

```
The Adjusted EBITDA build subtracts the FY2025 one-time parcel sale gain of approximately $185,400.00 from reported EBITDA.
```

### Criterion 6 — `owner_addback_capped`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 138 / 500 |

**Criterion** (paste into text field):

```
The Adjusted EBITDA build adds owner compensation of approximately $84,220.55 only, not the larger $210,000.00 relationship-manager claim.
```

### Criterion 7 — `rent_addback_disallowed`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 124 / 500 |

**Criterion** (paste into text field):

```
The Adjusted EBITDA build does not add back the $96,000.00 related-party rent normalization claimed in the borrower package.
```

### Criterion 8 — `adjusted_ebitda_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 51 / 500 |

**Criterion** (paste into text field):

```
Adjusted EBITDA equals approximately $1,147,440.73.
```

### Criterion 9 — `related_party_building_ineligible`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 123 / 500 |

**Criterion** (paste into text field):

```
The collateral analysis treats the Whitaker Realty LLC plant building as ineligible collateral for the equipment term loan.
```

### Criterion 10 — `soft_costs_ineligible`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 128 / 500 |

**Criterion** (paste into text field):

```
The collateral analysis treats install, freight, and deposit soft costs as ineligible for advance under the equipment term loan.
```

### Criterion 11 — `leased_forklift_ineligible`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 83 / 500 |

**Criterion** (paste into text field):

```
The collateral analysis treats the leased Toyota forklift as ineligible collateral.
```

### Criterion 12 — `obsolete_mill_ineligible`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 98 / 500 |

**Criterion** (paste into text field):

```
The collateral analysis treats the 1998 Bridgeport manual mill as ineligible under the age cutoff.
```

### Criterion 13 — `cnc_advance_80`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 62 / 500 |

**Criterion** (paste into text field):

```
Eligible new CNC assets are advanced at 80% of appraisal NOLV.
```

### Criterion 14 — `fixture_advance_50`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 103 / 500 |

**Criterion** (paste into text field):

```
Eligible fixtures are advanced at 50% of appraisal NOLV rather than the 70% relationship-manager claim.
```

### Criterion 15 — `eligible_nolv`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 60 / 500 |

**Criterion** (paste into text field):

```
Eligible collateral NOLV totals approximately $2,041,421.53.
```

### Criterion 16 — `bankable_collateral`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 82 / 500 |

**Criterion** (paste into text field):

```
Bankable collateral after policy advance rates equals approximately $1,568,673.10.
```

### Criterion 17 — `binding_commitment`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 122 / 500 |

**Criterion** (paste into text field):

```
The recommended commitment equals approximately $1,531,066.15, the lesser of bankable collateral and 75% of eligible NOLV.
```

### Criterion 18 — `ltv_full_ask_fails`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 95 / 500 |

**Criterion** (paste into text field):

```
LTV at the full requested commitment of $2,847,500.00 exceeds the 75% maximum on eligible NOLV.
```

### Criterion 19 — `debt_service_factor`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 107 / 500 |

**Criterion** (paste into text field):

```
Proposed annual debt service uses the memo factor of $16.42 per $1,000 of commitment per month, annualized.
```

### Criterion 20 — `existing_ds_used`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 82 / 500 |

**Criterion** (paste into text field):

```
DSCR tests include existing bank annual debt service of approximately $412,880.40.
```

### Criterion 21 — `dscr_full_ask_below_min`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 99 / 500 |

**Criterion** (paste into text field):

```
DSCR at the full requested commitment is approximately 1.1781x and below the 1.25x Approve minimum.
```

### Criterion 22 — `dscr_sized_passes`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 90 / 500 |

**Criterion** (paste into text field):

```
DSCR at the recommended commitment is approximately 1.6058x and meets the 1.25x threshold.
```

### Criterion 23 — `leverage_sized_passes`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 90 / 500 |

**Criterion** (paste into text field):

```
Leverage at the recommended commitment is approximately 3.2379x and does not exceed 3.50x.
```

### Criterion 24 — `path_conditional`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 101 / 500 |

**Criterion** (paste into text field):

```
The credit path decision is Approve with conditions, not Approve at the full request and not Decline.
```

### Criterion 25 — `condition_tenor_60`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 78 / 500 |

**Criterion** (paste into text field):

```
Conditions include shortening tenor to 60 months from the requested 84 months.
```

### Criterion 26 — `condition_personal_guaranty`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | accuracy |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Conditions include an unlimited personal guaranty of the principal owner.
```

### Criterion 27 — `notes_cite_before_rec`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 153 / 500 |

**Criterion** (paste into text field):

```
On the Notes section, or equivalent section label, citations to the input filenames and memo rules appear earlier than the committee path recommendation.
```

### Criterion 28 — `neg_full_ask_approve`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | safety |
| Characters | 121 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends approving the full requested commitment of $2,847,500.00 despite LTV and DSCR failure at the ask.
```

### Criterion 29 — `neg_related_party_collateral`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | safety |
| Characters | 120 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends treating Whitaker Realty LLC real estate as eligible collateral for the equipment term facility.
```

### Criterion 30 — `neg_mgmt_ebitda_dscr`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | safety |
| Characters | 145 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends measuring DSCR on management EBITDA that retains the one-time parcel gain and the disallowed related-party rent add-back.
```

### Criterion 31 — `neg_decline_without_sizing`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | safety |
| Characters | 148 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends an immediate Decline path that omits any sized Approve-with-conditions commitment after the ask exceeds bankable collateral.
```

### Criterion 32 — `neg_waive_guaranty`

| Field | Value |
|-------|-------|
| **Weight** | **-3** |
| Importance | Failure mode (important) |
| Type | negative |
| Category | safety |
| Characters | 99 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends waiving the personal guaranty on this Conditional-path equipment term loan.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 whitaker-precision-components-loan-underwriting
```
