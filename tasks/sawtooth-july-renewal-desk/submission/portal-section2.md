# Portal Section 2 — sawtooth-july-renewal-desk

Generated: 2026-09-02 18:52 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/sawtooth-july-renewal-desk/submission/golden.zip`

**Expected deliverable in prompt:** `renewal_underwriting_review.xlsx`

**Files inside golden.zip:**

- `renewal_underwriting_review.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **21** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 21 |
| Positive | 18 (+64) |
| Negative | 3 (-13) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 82 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named renewal_underwriting_review.xlsx.
```

### Criterion 2 — `accounts_reviewed_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 62 / 500 |

**Criterion** (paste into text field):

```
The workbook routes all 38 accounts in the July renewal batch.
```

### Criterion 3 — `workbook_structure`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 166 / 500 |

**Criterion** (paste into text field):

```
The workbook includes account routing, location exceptions, loss reconciliation, rules citations, and a disposition summary; equivalent section labels are acceptable.
```

### Criterion 4 — `si1015_quote`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 65 / 500 |

**Criterion** (paste into text field):

```
Account SI-1015 is assigned Quote on the account routing section.
```

### Criterion 5 — `si1021_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 148 / 500 |

**Criterion** (paste into text field):

```
Account SI-1021 is assigned Refer on the account routing section for TIV variance between renewal_account_list.csv and policy_location_schedule.csv.
```

### Criterion 6 — `si1042_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 65 / 500 |

**Criterion** (paste into text field):

```
Account SI-1042 is assigned Refer on the account routing section.
```

### Criterion 7 — `si1088_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 93 / 500 |

**Criterion** (paste into text field):

```
Account SI-1088 is assigned Refer on the account routing section for pending roof mitigation.
```

### Criterion 8 — `si1156_decline`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 67 / 500 |

**Criterion** (paste into text field):

```
Account SI-1156 is assigned Decline on the account routing section.
```

### Criterion 9 — `si1033_ask_broker`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
Account SI-1033 is assigned Ask Broker on the account routing section.
```

### Criterion 10 — `coastal_endorsement_flags`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 102 / 500 |

**Criterion** (paste into text field):

```
The location exception documentation flags at least four coastal wind locations in zones CW-1 or CW-2.
```

### Criterion 11 — `rules_source_cited`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 93 / 500 |

**Criterion** (paste into text field):

```
The workbook cites underwriting_rules_notes.txt for routing thresholds and referral triggers.
```

### Criterion 12 — `loss_run_reconciliation`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 151 / 500 |

**Criterion** (paste into text field):

```
The loss reconciliation section shows recomputed loss ratios wherever renewal_account_list.csv differs from loss_run_36mo.csv by more than five points.
```

### Criterion 13 — `si1156_recomputed_lr`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
Account SI-1156 recomputed 36-month loss ratio is approximately 95.8%.
```

### Criterion 14 — `si1042_location_incurred`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 82 / 500 |

**Criterion** (paste into text field):

```
Location ORL-1042-B total incurred in the loss analysis is approximately $278,400.
```

### Criterion 15 — `summary_quote_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 67 / 500 |

**Criterion** (paste into text field):

```
The disposition summary reports approximately 28 Quote assignments.
```

### Criterion 16 — `summary_refer_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 66 / 500 |

**Criterion** (paste into text field):

```
The disposition summary reports approximately 7 Refer assignments.
```

### Criterion 17 — `routing_rationale`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 129 / 500 |

**Criterion** (paste into text field):

```
Every Refer, Decline, and Ask Broker account includes a one-line rationale tied to underwriting_rules_notes.txt or a source file.
```

### Criterion 18 — `summary_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 110 / 500 |

**Criterion** (paste into text field):

```
Disposition summary counts use formulas referencing the account routing section rather than hard-coded totals.
```

### Criterion 19 — `cat_loss_in_attritional`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 123 / 500 |

**Criterion** (paste into text field):

```
The deliverable includes the CAT-2419 catastrophe-coded loss for account SI-1075 in the attritional loss-ratio calculation.
```

### Criterion 20 — `incomplete_account_list`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 76 / 500 |

**Criterion** (paste into text field):

```
The deliverable routes fewer than 38 accounts from renewal_account_list.csv.
```

### Criterion 21 — `stale_list_ratio_si1042`

| Field | Value |
|-------|-------|
| **Weight** | **-3** |
| Importance | Failure mode (important) |
| Type | negative |
| Category | negative |
| Characters | 161 / 500 |

**Criterion** (paste into text field):

```
The deliverable assigns Quote to account SI-1042 based solely on the renewal_account_list.csv loss ratio when loss_run_36mo.csv supports referral for ORL-1042-B.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 sawtooth-july-renewal-desk
```
