# Portal Section 2 — northline-industrial-holdings-covenant-pack

Generated: 2026-09-04 08:17 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/northline-industrial-holdings-covenant-pack/submission/golden.zip`

**Expected deliverable in prompt:** `covenant_headroom_northline-industrial-holdings.xlsx`

**Files inside golden.zip:**

- `covenant_headroom_northline-industrial-holdings.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **33** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 33 |
| Positive | 28 (+112) |
| Negative | 5 (-25) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 102 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named covenant_headroom_northline-industrial-holdings.xlsx.
```

### Criterion 2 — `workbook_sections`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 252 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a funded debt build, an Adjusted EBITDA build with add-back dispositions, covenant tests for leverage, interest coverage, and CapEx basket, an exception log, and an analyst recommendation; equivalent section labels are acceptable.
```

### Criterion 3 — `funded_debt_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 75 / 500 |

**Criterion** (paste into text field):

```
Consolidated Funded Debt as of 2026-06-30 equals approximately $67,784,620.
```

### Criterion 4 — `term_and_revolver_included`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 101 / 500 |

**Criterion** (paste into text field):

```
Funded Debt includes Term Loan A outstanding of $42,850,000 and Revolving Loans drawn of $18,250,000.
```

### Criterion 5 — `seller_note_included`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 81 / 500 |

**Criterion** (paste into text field):

```
The Bolt & Die seller note of $4,500,000 is included in Consolidated Funded Debt.
```

### Criterion 6 — `finance_leases_included`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 95 / 500 |

**Criterion** (paste into text field):

```
Finance Lease Obligations of approximately $2,184,620 are included in Consolidated Funded Debt.
```

### Criterion 7 — `intercompany_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 105 / 500 |

**Criterion** (paste into text field):

```
The $1,200,000 intercompany note owing to Northline Holdco LLC is excluded from Consolidated Funded Debt.
```

### Criterion 8 — `undrawn_lc_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 102 / 500 |

**Criterion** (paste into text field):

```
The $3,200,000 undrawn standby letter-of-credit face amount is excluded from Consolidated Funded Debt.
```

### Criterion 9 — `stale_q1_not_used`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 120 / 500 |

**Criterion** (paste into text field):

```
Funded Debt uses the 2026-06-30 Facilities balances rather than the superseded Draft_Q1 revolver balance of $16,400,000.
```

### Criterion 10 — `adjusted_ebitda_total`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 110 / 500 |

**Criterion** (paste into text field):

```
Consolidated Adjusted EBITDA for the trailing twelve months ended 2026-06-30 equals approximately $18,144,991.
```

### Criterion 11 — `reported_ebitda_base`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 86 / 500 |

**Criterion** (paste into text field):

```
Adjusted EBITDA starts from reported Consolidated EBITDA of approximately $14,228,440.
```

### Criterion 12 — `sbc_allowed`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 102 / 500 |

**Criterion** (paste into text field):

```
Non-cash stock-based compensation of approximately $412,880 is allowed as an Adjusted EBITDA add-back.
```

### Criterion 13 — `restructuring_capped`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 139 / 500 |

**Criterion** (paste into text field):

```
Dayton restructuring is allowed at only $2,000,000 under the Permitted Restructuring Charges cap, not the full borrower-claimed $2,840,000.
```

### Criterion 14 — `acq_costs_allowed`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
Bolt & Die transaction costs of approximately $685,220 are allowed as Permitted Acquisition fees.
```

### Criterion 15 — `synergies_rejected`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 88 / 500 |

**Criterion** (paste into text field):

```
Projected Bolt & Die run-rate synergies of $1,100,000 are excluded from Adjusted EBITDA.
```

### Criterion 16 — `sponsor_fee_capped`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 143 / 500 |

**Criterion** (paste into text field):

```
Ridgepath Capital sponsor management fee is allowed at only $500,000 for Northline Industrial Holdings, not the full borrower-claimed $750,000.
```

### Criterion 17 — `inventory_stepup_allowed`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 111 / 500 |

**Criterion** (paste into text field):

```
Inventory step-up amortization of approximately $318,450 is allowed as a non-cash purchase accounting add-back.
```

### Criterion 18 — `warranty_litigation_rejected`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 122 / 500 |

**Criterion** (paste into text field):

```
The $425,000 Atlas Forge / OEM warranty settlement is excluded from Adjusted EBITDA as an Ordinary Course Warranty Matter.
```

### Criterion 19 — `leverage_ratio`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 89 / 500 |

**Criterion** (paste into text field):

```
Total Leverage Ratio equals approximately 3.74x (Funded Debt divided by Adjusted EBITDA).
```

### Criterion 20 — `leverage_pass`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 56 / 500 |

**Criterion** (paste into text field):

```
Total Leverage is marked PASS against the 4.50x maximum.
```

### Criterion 21 — `interest_coverage_ratio`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 107 / 500 |

**Criterion** (paste into text field):

```
Interest Coverage Ratio equals approximately 3.72x using Cash Interest Expense of approximately $4,882,110.
```

### Criterion 22 — `icr_pass`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 59 / 500 |

**Criterion** (paste into text field):

```
Interest Coverage is marked PASS against the 2.50x minimum.
```

### Criterion 23 — `capex_usage`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 171 / 500 |

**Criterion** (paste into text field):

```
CapEx Basket Usage equals approximately $7,280,401 after carving out $1,840,000 of Bolt & Die Permitted Acquisition CapEx from gross YTD CapEx of approximately $9,120,401.
```

### Criterion 24 — `capex_pass`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 127 / 500 |

**Criterion** (paste into text field):

```
CapEx Basket Usage is marked PASS against the $8,500,000 calendar-year limit with remaining basket of approximately $1,219,599.
```

### Criterion 25 — `cash_interest_excludes_fees`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 136 / 500 |

**Criterion** (paste into text field):

```
Cash Interest Expense used for Interest Coverage excludes commitment fees and letter-of-credit fees per the credit agreement definition.
```

### Criterion 26 — `exception_log_present`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 196 / 500 |

**Criterion** (paste into text field):

```
The workbook documents lender dispositions for restructuring excess, run-rate synergies, sponsor fee excess, and ordinary-course warranty, with citations to credit_agreement_covenant_excerpts.txt.
```

### Criterion 27 — `recommendation_pass`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | judgment |
| Characters | 194 / 500 |

**Criterion** (paste into text field):

```
The analyst recommendation states PASS / certify compliance on Total Leverage, Interest Coverage, and CapEx basket using lender-adjusted figures rather than the borrower-claimed Adjusted EBITDA.
```

### Criterion 28 — `live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 179 / 500 |

**Criterion** (paste into text field):

```
Funded Debt total, Adjusted EBITDA total, leverage, interest coverage, and CapEx basket usage are formula-linked to their component inputs rather than solely hard-coded endpoints.
```

### Criterion 29 — `neg_full_restructuring`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 138 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs the committee to treat the full uncapped $2,840,000 Dayton restructuring charge as permitted Adjusted EBITDA.
```

### Criterion 30 — `neg_runrate_synergies`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 185 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs the committee to include the $1,100,000 projected Bolt & Die run-rate synergies in Adjusted EBITDA before the savings are reflected in consolidated results.
```

### Criterion 31 — `neg_undrawn_lc_in_debt`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 132 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs the committee to count the $3,200,000 undrawn letter-of-credit face amount in Consolidated Funded Debt.
```

### Criterion 32 — `neg_intercompany_in_debt`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 145 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs the committee to include the $1,200,000 intercompany note owing to Northline Holdco LLC in Consolidated Funded Debt.
```

### Criterion 33 — `neg_capex_ignore_carveout`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 169 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs the committee to fail the CapEx basket using gross YTD CapEx while ignoring the $1,840,000 Bolt & Die Permitted Acquisition CapEx carve-out.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 northline-industrial-holdings-covenant-pack
```
