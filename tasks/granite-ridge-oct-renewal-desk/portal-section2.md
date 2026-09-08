# Portal Section 2 — granite-ridge-oct-renewal-desk

Generated: 2026-09-06 09:17 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/granite-ridge-oct-renewal-desk/submission/golden.zip`

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

Enter **31** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 31 |
| Positive | 27 (+90) |
| Negative | 4 (-20) |

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

### Criterion 2 — `routing_completeness`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 135 / 500 |

**Criterion** (paste into text field):

```
Every one of the 36 accounts on the account routing section receives exactly one disposition from Quote, Refer, Decline, or Ask Broker.
```

### Criterion 3 — `location_exceptions_present`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 127 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a clearly labeled Location Exceptions section that is present and usable for reviewing flagged locations.
```

### Criterion 4 — `loss_reconciliation_present`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 154 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a clearly labeled Loss Reconciliation section that presents the reconciliation framework comparing account-list and loss-run ratios.
```

### Criterion 5 — `disposition_summary_present`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 128 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a disposition summary that counts Quote, Refer, Decline, and Ask Broker assignments for the October batch.
```

### Criterion 6 — `gr2018_quote`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 65 / 500 |

**Criterion** (paste into text field):

```
Account GR-2018 is assigned Quote on the account routing section.
```

### Criterion 7 — `gr2047_quote`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 297 / 500 |

**Criterion** (paste into text field):

```
Account GR-2047 is assigned Quote on the account routing section because occupancy_pct 94.0% does not imply full occupancy under Section 6 of granite_ridge_routing_notes.txt, HAB-2047-B has broker_confirmation=yes documenting turnover vacancy, and no other Section 3–10 referral trigger is active.
```

### Criterion 8 — `gr2089_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 98 / 500 |

**Criterion** (paste into text field):

```
Account GR-2089 is assigned Refer on the account routing section for expired sprinkler inspection.
```

### Criterion 9 — `gr2113_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 142 / 500 |

**Criterion** (paste into text field):

```
Account GR-2113 is assigned Refer on the account routing section for stale unit count and TIV relative to granite_ridge_location_schedule.csv.
```

### Criterion 10 — `gr2162_refer`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 378 / 500 |

**Criterion** (paste into text field):

```
Account GR-2162 is assigned Refer on the account routing section with a recomputed attritional incurred loss ratio of 67.5% from granite_ridge_loss_run_36mo.csv and HAB-2162-C total incurred of $260,120, applying the Section 3 referral thresholds in granite_ridge_routing_notes.txt (loss ratio at or above 45% and below 70%, and/or single-location incurred of $250,000 or more).
```

### Criterion 11 — `gr2074_refer_pool`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 250 / 500 |

**Criterion** (paste into text field):

```
Account GR-2074 is assigned Refer on the account routing section because location HAB-2074-A has pool_liability_flag pending_fence_po (pending pool-fence work) on granite_ridge_location_schedule.csv under Section 5 of granite_ridge_routing_notes.txt.
```

### Criterion 12 — `gr2195_decline`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 67 / 500 |

**Criterion** (paste into text field):

```
Account GR-2195 is assigned Decline on the account routing section.
```

### Criterion 13 — `gr2033_ask_broker`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
Account GR-2033 is assigned Ask Broker on the account routing section.
```

### Criterion 14 — `gr2007_refer_appetite`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 334 / 500 |

**Criterion** (paste into text field):

```
Account GR-2007 (Campus Edge Housing Co.) is assigned Refer on the account routing section because Section 10 of granite_ridge_routing_notes.txt requires GRP-APPETITE review before bind, and the Location Exceptions section includes a Section 10 appetite note for GR-2007 stating that GRP-APPETITE review must be submitted before bind.
```

### Criterion 15 — `gr2065_refer_appetite`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 186 / 500 |

**Criterion** (paste into text field):

```
Account GR-2065 (Campus Edge Housing Co.) is assigned Refer on the account routing section because Section 10 of granite_ridge_routing_notes.txt requires GRP-APPETITE review before bind.
```

### Criterion 16 — `subsidized_endorsement_flags`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 116 / 500 |

**Criterion** (paste into text field):

```
The location exception documentation flags at least three subsidized-housing locations requiring endorsement review.
```

### Criterion 17 — `rules_source_cited`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 96 / 500 |

**Criterion** (paste into text field):

```
The workbook cites granite_ridge_routing_notes.txt for routing thresholds and referral triggers.
```

### Criterion 18 — `loss_run_reconciliation`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 175 / 500 |

**Criterion** (paste into text field):

```
The loss reconciliation section shows recomputed loss ratios wherever granite_ridge_renewal_accounts.csv differs from granite_ridge_loss_run_36mo.csv by more than five points.
```

### Criterion 19 — `loss_run_controls_routing`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 223 / 500 |

**Criterion** (paste into text field):

```
Where granite_ridge_renewal_accounts.csv and granite_ridge_loss_run_36mo.csv loss ratios differ by more than five points, the account routing disposition uses the recomputed loss-run ratio as the controlling routing metric.
```

### Criterion 20 — `gr2195_recomputed_lr`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 71 / 500 |

**Criterion** (paste into text field):

```
Account GR-2195 recomputed 36-month loss ratio is approximately 292.3%.
```

### Criterion 21 — `summary_quote_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 53 / 500 |

**Criterion** (paste into text field):

```
The disposition summary reports 25 Quote assignments.
```

### Criterion 22 — `summary_refer_count`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 52 / 500 |

**Criterion** (paste into text field):

```
The disposition summary reports 9 Refer assignments.
```

### Criterion 23 — `summary_decline_ask_broker_counts`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 116 / 500 |

**Criterion** (paste into text field):

```
The disposition summary reports 1 Decline assignment and 1 Ask Broker assignment, for a total of 36 routed accounts.
```

### Criterion 24 — `routing_rationale`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 132 / 500 |

**Criterion** (paste into text field):

```
Every Refer, Decline, and Ask Broker account includes a one-line rationale tied to granite_ridge_routing_notes.txt or a source file.
```

### Criterion 25 — `summary_formulas`

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

### Criterion 26 — `cat_loss_excluded_attritional`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 153 / 500 |

**Criterion** (paste into text field):

```
The attritional loss-ratio calculation excludes the CAT-2408 catastrophe-coded loss for account GR-2071 per Section 9 of granite_ridge_routing_notes.txt.
```

### Criterion 27 — `gr2071_section9_rationale`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
Account GR-2071 routing rationale cites Section 9 of granite_ridge_routing_notes.txt for excluding CAT-2408 from the attritional loss-ratio calculation.
```

### Criterion 28 — `false_cat_exclusion_rationale`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 174 / 500 |

**Criterion** (paste into text field):

```
The deliverable states that cat-coded rows were excluded from the attritional loss ratio for an account that has no catastrophe-coded loss on granite_ridge_loss_run_36mo.csv.
```

### Criterion 29 — `false_quote_gr2195_decline_lr`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 241 / 500 |

**Criterion** (paste into text field):

```
The account routing section recommends Quote for GR-2195 despite the recomputed attritional loss ratio of approximately 292.3% from granite_ridge_loss_run_36mo.csv exceeding the Section 3 decline threshold in granite_ridge_routing_notes.txt.
```

### Criterion 30 — `false_appetite_clearance`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 100 / 500 |

**Criterion** (paste into text field):

```
The deliverable states that GRP-APPETITE clearance has already been obtained for GR-2007 or GR-2065.
```

### Criterion 31 — `false_broker_confirmation`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 145 / 500 |

**Criterion** (paste into text field):

```
The deliverable states that broker confirmation is on file for HAB-2033-B while granite_ridge_location_schedule.csv shows broker_confirmation=no.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 granite-ridge-oct-renewal-desk
```
