# Portal Section 2 — vesper-culinary-brands-consolidation

Generated: 2026-09-08 08:33 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/vesper-culinary-brands-consolidation/submission/golden.zip`

**Expected deliverable in prompt:** `consolidated_review_vesper_culinary_brands.xlsx`

**Files inside golden.zip:**

- `consolidated_review_vesper_culinary_brands.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **25** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 25 |
| Positive | 22 (+75) |
| Negative | 3 (-15) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named consolidated_review_vesper_culinary_brands.xlsx.
```

### Criterion 2 — `reporting_period`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 162 / 500 |

**Criterion** (paste into text field):

```
The workbook states the Q3 2025 reporting period of July 1, 2025 through September 30, 2025 and frames the analysis as of the Q3 2025 close in early October 2025.
```

### Criterion 3 — `eur_usd_rate`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 72 / 500 |

**Criterion** (paste into text field):

```
The workbook states the governing EUR-to-USD board close rate of 1.0874.
```

### Criterion 4 — `kiln_ownership_start`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | accuracy |
| Characters | 209 / 500 |

**Criterion** (paste into text field):

```
The workbook records Kiln Spice Works ownership starting August 12, 2025 as the modeling date from the acquisition memo, and distinguishes that modeling basis from independent supporting-evidence confirmation.
```

### Criterion 5 — `kiln_method_and_approval`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 412 / 500 |

**Criterion** (paste into text field):

```
The workbook identifies the transaction-date cutoff method and its memo rule, states that approval evidence is not present in the supplied packet (e.g. Approval evidence in supplied packet: not present), selects 50/92 proration from kiln_spice_acquisition_memo.txt as the final Kiln board treatment, treats cutoff as conditional only, and does not invent an approval record, approver, approval date, or sign-off.
```

### Criterion 6 — `kiln_open_followups`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 254 / 500 |

**Criterion** (paste into text field):

```
The workbook identifies as open follow-up items that Schedule 2.1 and bank wire confirmation for the August 12 Kiln ownership date are not in the supplied packet, and that post-close Kiln billing shipment or service support is not in the supplied packet.
```

### Criterion 7 — `workbook_structure`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | structure |
| Characters | 196 / 500 |

**Criterion** (paste into text field):

```
The workbook presents assumptions, line or source inventory, consolidated rollup by brand, reconciliation of excluded transactions, and a board-facing recommendation, or equivalent section labels.
```

### Criterion 8 — `reconciliation_bridge`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 447 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a formula-driven reconciliation bridge from raw extract gross by brand through exclusion/adjustment categories in the packet (void/cancelled, duplicate, period/out-of-period, and Kiln 50/92 ownership) to adjusted board amounts of about $565,717.81 Hearth, $644,106.78 Brine, and $339,572.04 Kiln (consolidated about $1,549,396.63), with a control total tying the bridge to the brand-level revenue rollup at a zero difference.
```

### Criterion 9 — `total_consolidated_final`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 458 / 500 |

**Criterion** (paste into text field):

```
The workbook reports selected final consolidated Q3 2025 net revenue of approximately $1,549,396.63 under 50/92 proration, equal to the sum of the workbook's Hearth, Brine, and selected-final Kiln consolidated figures. If a transaction-date cutoff total of approximately $1,634,434.29 appears, it is labeled as a Conditional transaction-date cutoff scenario with the missing approval-evidence limitation documented, not as the unqualified final board figure.
```

### Criterion 10 — `hearth_consolidated`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 120 / 500 |

**Criterion** (paste into text field):

```
Hearth Kitchen Co consolidated USD is approximately $565,717.81 for the full quarter after status and period exclusions.
```

### Criterion 11 — `brine_consolidated`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 229 / 500 |

**Criterion** (paste into text field):

```
Brine & Barrel EU consolidated USD is approximately $644,106.78, reflecting EUR-to-USD conversion at the 1.0874 board close rate using sum-then-round treatment (native EUR summed before conversion; not line-by-line USD rounding).
```

### Criterion 12 — `kiln_consolidated_final`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 457 / 500 |

**Criterion** (paste into text field):

```
Kiln Spice Works selected-final consolidated USD is approximately $339,572.04 under 50/92 proration of post-exclusion full-quarter posted Kiln gross. A transaction-date cutoff amount of approximately $424,609.70 may be shown as a correctly calculated Conditional transaction-date cutoff scenario with the missing approval-evidence limitation noted, but must not be selected as the final Kiln board result when approval evidence is not present in the packet.
```

### Criterion 13 — `exclusion_log`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 236 / 500 |

**Criterion** (paste into text field):

```
The reconciliation documentation identifies void, cancelled, duplicate, and out-of-period ledger rows excluded from consolidated revenue, and for excluded Brine & Barrel EU rows shows USD impact computed from the governing EUR/USD rate.
```

### Criterion 14 — `prior_period_exclusion`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 109 / 500 |

**Criterion** (paste into text field):

```
The workbook excludes the June 2025 Hearth Kitchen Co prior-period catch-up row from consolidated Q3 revenue.
```

### Criterion 15 — `fx_source_cited`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 85 / 500 |

**Criterion** (paste into text field):

```
The workbook lists brine_barrel_fx_and_period_reference.txt among cited source files.
```

### Criterion 16 — `acquisition_source_cited`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 134 / 500 |

**Criterion** (paste into text field):

```
The workbook lists kiln_spice_acquisition_memo.txt among cited source files and attributes the 50/92 proration treatment to that memo.
```

### Criterion 17 — `ledger_source_used`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 144 / 500 |

**Criterion** (paste into text field):

```
The workbook reconciles brand totals to vesper_culinary_brands_brand_ledger.csv rather than introducing revenue figures absent from that ledger.
```

### Criterion 18 — `rollup_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | rigid |
| Category | method |
| Characters | 447 / 500 |

**Criterion** (paste into text field):

```
Derived consolidated figures are formula-linked to transaction detail so that changing an included transaction amount updates the full calculation chain—status or period inclusion or exclusion, brand native-currency gross, Brine EUR-to-USD conversion for EUR-denominated Brine transactions, Kiln ownership treatment, brand consolidated USD, and total consolidated revenue—rather than relying on manually typed brand gross or total constants alone.
```

### Criterion 19 — `judgment_documented`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 222 / 500 |

**Criterion** (paste into text field):

```
The workbook documents the governing FX-rate judgment call: selecting the 1.0874 board close rate from brine_barrel_fx_and_period_reference.txt and rejecting the informal 1.1025 spot aside for consolidated Brine reporting.
```

### Criterion 20 — `board_recommendation_final`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | deliverable |
| Characters | 234 / 500 |

**Criterion** (paste into text field):

```
The workbook includes a board-facing recommendation stating the selected final consolidated Q3 2025 revenue figure of approximately $1,549,396.63 and does not present the conditional cutoff total as the unqualified final board figure.
```

### Criterion 21 — `board_recommendation_kiln_ownership`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | deliverable |
| Characters | 241 / 500 |

**Criterion** (paste into text field):

```
The board-facing recommendation states that Kiln Spice Works is included under the selected 50/92 ownership treatment from kiln_spice_acquisition_memo.txt and does not treat pre-ownership Kiln revenue as full unprorated consolidated revenue.
```

### Criterion 22 — `presentation_no_cell_refs`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 106 / 500 |

**Criterion** (paste into text field):

```
The board-facing recommendation or board reporting note does not cite internal spreadsheet cell addresses.
```

### Criterion 23 — `recommends_spot_overrides_bulletin`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 204 / 500 |

**Criterion** (paste into text field):

```
The board recommendation instructs converting Brine & Barrel EU revenue using the informal 1.1025 spot aside as superseding brine_barrel_fx_and_period_reference.txt / VCB-FX-2025-03 for the board package.
```

### Criterion 24 — `recommends_salesops_full_quarter_kiln`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 189 / 500 |

**Criterion** (paste into text field):

```
The board recommendation recommends adopting the sales operations full-quarter Kiln contribution note as the board consolidation figure in place of the acquisition memo ownership treatment.
```

### Criterion 25 — `asserts_cutoff_approved_final`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | negative |
| Characters | 234 / 500 |

**Criterion** (paste into text field):

```
The board recommendation presents the transaction-date cutoff consolidated total as the unqualified final board figure, or fabricates approval evidence (approver, approval date, or sign-off) that is not present in the supplied packet.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 vesper-culinary-brands-consolidation
```
