# Portal Section 2 — ashcroft-foods-claims-coverage

Generated: 2026-09-05 16:07 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/ashcroft-foods-claims-coverage/submission/golden.zip`

**Expected deliverable in prompt:** `claim_coverage_opinion_ashcroft-foods.xlsx`

**Files inside golden.zip:**

- `claim_coverage_opinion_ashcroft-foods.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **36** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 36 |
| Positive | 31 (+113) |
| Negative | 5 (-25) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 92 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named claim_coverage_opinion_ashcroft-foods.xlsx.
```

### Criterion 2 — `coverage_decision_tree`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 304 / 500 |

**Criterion** (paste into text field):

```
For spoiled stock, equipment, business income, and packaging, the workbook shows a multi-stage coverage decision tree covering raw fact identification, potentially controlling provision, competing evidence, hierarchy decision, rule test, intermediate result, final disposition, and financial consequence.
```

### Criterion 3 — `evidence_matrix`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 206 / 500 |

**Criterion** (paste into text field):

```
The workbook includes an evidence/rule matrix that distinguishes recorded, potentially controlling, superseded, and derived items and documents governing-source selection with downstream calculation impact.
```

### Criterion 4 — `stock_partial_accept`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | accuracy |
| Characters | 139 / 500 |

**Criterion** (paste into text field):

```
The workbook accepts coverage for cleaned Zone B spoiled stock under the Spoilage Coverage endorsement, subject to maintenance coinsurance.
```

### Criterion 5 — `equipment_deny`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 100 / 500 |

**Criterion** (paste into text field):

```
The workbook denies the compressor/equipment repair demand under the Mechanical Breakdown exclusion.
```

### Criterion 6 — `bi_deny`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 129 / 500 |

**Criterion** (paste into text field):

```
The workbook denies Business Income because the temperature outage of about 14 hours does not satisfy the 72-hour waiting period.
```

### Criterion 7 — `overall_partial`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 126 / 500 |

**Criterion** (paste into text field):

```
The overall coverage determination is Partial Coverage (stock accepted with adjustment; equipment and Business Income denied).
```

### Criterion 8 — `valuation_reconciliation`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 203 / 500 |

**Criterion** (paste into text field):

```
The workbook reconciles selling-price versus invoice/replacement-cost candidates, rejects selling price because the rider was not elected, and uses invoice/replacement cost for the actual covered amount.
```

### Criterion 9 — `active_vs_superseded_deductible`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 159 / 500 |

**Criterion** (paste into text field):

```
The workbook selects the Active spoilage deductible of 5000.00 and documents that the Superseded 10000.00 schedule row is non-governing for the actual reserve.
```

### Criterion 10 — `packaging_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 60 / 500 |

**Criterion** (paste into text field):

```
PKG-991 corrugated packaging is excluded from covered stock.
```

### Criterion 11 — `void_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 58 / 500 |

**Criterion** (paste into text field):

```
LOT-B-099 with VOID status is excluded from covered stock.
```

### Criterion 12 — `duplicate_excluded`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 61 / 500 |

**Criterion** (paste into text field):

```
LOT-B-218-DUP duplicate rekey is excluded from covered stock.
```

### Criterion 13 — `inventory_audit_trail`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 285 / 500 |

**Criterion** (paste into text field):

```
Every inventory demand lot is traced through a status pipeline showing raw amount, status, duplicate/VOID flag, stock/non-stock class, coverage treatment, eligible amount, exclusion reason, and valuation basis, with separate totals for eligible, VOID, duplicate, and packaging amounts.
```

### Criterion 14 — `inventory_control_check`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 178 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a formula-driven inventory control check showing raw inventory equals eligible plus VOID, duplicate, and packaging exclusions, with an explicit PASS result.
```

### Criterion 15 — `covered_stock_cost`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 52 / 500 |

**Criterion** (paste into text field):

```
Cleaned covered stock invoice cost totals 254317.96.
```

### Criterion 16 — `salvage_credit`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 73 / 500 |

**Criterion** (paste into text field):

```
Salvage credit on LOT-B-441 is 12629.82 (30% of that lot's invoice cost).
```

### Criterion 17 — `maintenance_timeline`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 234 / 500 |

**Criterion** (paste into text field):

```
The workbook shows a maintenance timeline deriving elapsed days from last service 2025-08-12 to loss 2025-11-18, applying OEM interval, 7-day grace, overdue amount, vendor-cancellation timing, and the resulting coinsurance pay factor.
```

### Criterion 18 — `coinsurance_75`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
Maintenance coinsurance applies a 75% pay factor (25% reduction) to the stock loss after salvage.
```

### Criterion 19 — `oem_sensitivity_table`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 208 / 500 |

**Criterion** (paste into text field):

```
The workbook includes an OEM-interval sensitivity table with the source-supported interval plus shorter and longer hypothetical intervals, showing whether coinsurance and reserve change under each assumption.
```

### Criterion 20 — `equipment_footing_documented`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 314 / 500 |

**Criterion** (paste into text field):

```
The workbook documents the equipment demand footing issue: prior EQ-SUB 84517.60 versus EQ-01 through EQ-05 component sum 82517.60 (variance 2000.00), selects the component sum as source of truth after desk correction, and states that the variance does not affect the indemnity reserve because equipment is denied.
```

### Criterion 21 — `reserve_bridge`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 220 / 500 |

**Criterion** (paste into text field):

```
The workbook presents a formula-linked reserve bridge from raw inventory through VOID/duplicate/non-stock exclusions, eligible stock, salvage, maintenance coinsurance, and Active deductible to the indemnity case reserve.
```

### Criterion 22 — `case_reserve_amount`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 52 / 500 |

**Criterion** (paste into text field):

```
Recommended indemnity case reserve equals 176266.11.
```

### Criterion 23 — `pure_vs_case`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 246 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a Pure vs Case bridge showing the cleaned case reserve, any triangle/other indicated amount (or none), pure IBNR, total reserve, and an explicit PASS double-counting test that the case amount is not also booked in pure IBNR.
```

### Criterion 24 — `scenario_checks`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 253 / 500 |

**Criterion** (paste into text field):

```
The workbook includes formula-linked counterfactual scenarios for superseded deductible, selling-price basis, no maintenance coinsurance, equipment hypothetically covered, and excluded/VOID lot control, each marked as not used for the actual conclusion.
```

### Criterion 25 — `decision_trace`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 244 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a decision trace from source evidence through rule, test, conclusion, and financial impact for stock, equipment, BI, packaging, maintenance coinsurance, valuation, and deductible, and links the final reserve to that trace.
```

### Criterion 26 — `consistency_checks`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 235 / 500 |

**Criterion** (paste into text field):

```
The workbook includes explicit PASS/FAIL consistency checks covering inventory reconciliation, equipment footing, BI hours, maintenance elapsed days, reserve formula chain, ALAE exclusion from indemnity, and recommendation consistency.
```

### Criterion 27 — `formula_linkage`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 202 / 500 |

**Criterion** (paste into text field):

```
The indemnity case reserve is formula-linked to cleaned eligible inventory and the maintenance coinsurance factor so changing an eligible included amount or the timeline factor would change the reserve.
```

### Criterion 28 — `alae_separate`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 82 / 500 |

**Criterion** (paste into text field):

```
The workbook keeps ALAE/expense payments outside the indemnity case reserve total.
```

### Criterion 29 — `committee_recommendation`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 251 / 500 |

**Criterion** (paste into text field):

```
The File Recommendation separately addresses coverage posture, indemnity reserve, ALAE, major uncertainty, key financial sensitivity, and recommended underwriting disposition, and is consistent with Partial Coverage and the linked actual case reserve.
```

### Criterion 30 — `memo_over_field_note`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 130 / 500 |

**Criterion** (paste into text field):

```
The workbook treats coverage_investigation_memo.txt as governing over Adjuster Notes N-01 selling-price / full-equipment guidance.
```

### Criterion 31 — `endorsement_vs_exclusion`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 205 / 500 |

**Criterion** (paste into text field):

```
The workbook explains that the Spoilage endorsement can respond to temperature-driven stock loss from on-premises refrigeration breakdown while equipment repair remains excluded under Mechanical Breakdown.
```

### Criterion 32 — `neg_equipment_pay`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 132 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends paying or reserving the equipment repair under the property form despite the Mechanical Breakdown exclusion.
```

### Criterion 33 — `neg_approve_sell_price_pay`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 125 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends approving payment of the insured's full selling-price spoilage demand as presented on the claim file.
```

### Criterion 34 — `neg_bi_reserve`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 128 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends booking a Business Income case reserve despite the outage being shorter than the 72-hour waiting period.
```

### Criterion 35 — `neg_full_coverage_authorize`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
The workbook recommends a Full Coverage accept disposition that authorizes payment of equipment repair and Business Income in addition to spoiled stock.
```

### Criterion 36 — `neg_use_counterfactual_as_actual`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 181 / 500 |

**Criterion** (paste into text field):

```
The workbook adopts a Scenario Checks counterfactual (superseded deductible, selling-price basis, no coinsurance, or equipment covered) as the actual committee indemnity conclusion.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 ashcroft-foods-claims-coverage
```
