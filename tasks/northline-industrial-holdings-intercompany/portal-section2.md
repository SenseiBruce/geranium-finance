# Portal Section 2 — northline-industrial-holdings-intercompany

Generated: 2026-09-07 17:16 UTC

Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.
Put **weight only** in the Weight field — never in the criterion text.

---

## Golden Solution File Uploader

**Upload:** `tasks/northline-industrial-holdings-intercompany/submission/golden.zip`

**Expected deliverable in prompt:** `intercompany_settlement_northline-industrial-holdings.xlsx`

**Files inside golden.zip:**

- `intercompany_settlement_northline-industrial-holdings.xlsx`

### Before upload

- Human-reviewed golden (not raw LLM output with surface edits only)
- Client-ready formatting; spreadsheets use live formulas where the prompt requires them
- Flat zip at root level (no subfolders)
- Filename matches prompt exactly

---

## Rubric criteria

Enter **35** criteria in order. Portal limit: **500** characters per criterion text.

| Stat | Value |
|------|-------|
| Total criteria | 35 |
| Positive | 29 (+122) |
| Negative | 6 (-30) |

### Criterion 1 — `deliverable_filename`

| Field | Value |
|-------|-------|
| **Weight** | **+2** |
| Importance | Important |
| Type | rigid |
| Category | deliverable |
| Characters | 108 / 500 |

**Criterion** (paste into text field):

```
The final deliverable is an Excel workbook named intercompany_settlement_northline-industrial-holdings.xlsx.
```

### Criterion 2 — `workbook_sections`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | structure |
| Characters | 297 / 500 |

**Criterion** (paste into text field):

```
The workbook includes an AR settlement population, an AP FX tie-out, an exception log with memo section 6 documentation fields, a section 6 exception-test evaluation, a self-consistency control, counterparty netting, and a September 3 wire recommendation; equivalent section labels are acceptable.
```

### Criterion 3 — `appendix_a_six_invoices`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 145 / 500 |

**Criterion** (paste into text field):

```
The AR settlement population covers the six Appendix A invoices INV-AR-8841, INV-AR-8790, INV-AR-8766, INV-AR-8812, INV-AR-8855, and INV-AR-8688.
```

### Criterion 4 — `total_ar_settlement`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 68 / 500 |

**Criterion** (paste into text field):

```
Total Appendix A AR settlement USD equals approximately $551,001.71.
```

### Criterion 5 — `intransit_8841_included`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 122 / 500 |

**Criterion** (paste into text field):

```
InTransit INV-AR-8841 for $185,420.18 is included in the Canada AR settlement population under FOB shipping-point cut-off.
```

### Criterion 6 — `intransit_8855_included`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 122 / 500 |

**Criterion** (paste into text field):

```
InTransit INV-AR-8855 for $128,440.00 is included in the Mexico AR settlement population under FOB shipping-point cut-off.
```

### Criterion 7 — `s6_test1_void_ar`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 147 / 500 |

**Criterion** (paste into text field):

```
Under memo section 6 test 1, Void AR invoice INV-AR-8820 (status_flag Void) is excluded from the AR settlement population and the September 3 wire.
```

### Criterion 8 — `memo_cad_rate`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 69 / 500 |

**Criterion** (paste into text field):

```
Canada AP tie-out uses the August 31 memo rate of 1.3724 CAD per USD.
```

### Criterion 9 — `memo_mxn_rate`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 70 / 500 |

**Criterion** (paste into text field):

```
Mexico AP tie-out uses the August 31 memo rate of 18.5800 MXN per USD.
```

### Criterion 10 — `stale_rate_revalued`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 167 / 500 |

**Criterion** (paste into text field):

```
AP-C-441 is identified as booked at the stale July CAD rate of 1.3680 and is revalued at the August 31 memo CAD rate of 1.3724, producing approximately $92,582.62 USD.
```

### Criterion 11 — `ap_c_441_fx_diff`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 97 / 500 |

**Criterion** (paste into text field):

```
AP-C-441 FX difference versus parent INV-AR-8790 after memo revaluation is approximately $297.78.
```

### Criterion 12 — `matched_ap_examples`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 126 / 500 |

**Criterion** (paste into text field):

```
Matched AP rows AP-C-441, AP-C-442, AP-M-210, and AP-M-205 reference the corresponding parent invoice IDs on the AR subledger.
```

### Criterion 13 — `canada_ap_converted`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 88 / 500 |

**Criterion** (paste into text field):

```
Canada matched Appendix A AP converts to approximately $133,802.80 USD at the memo rate.
```

### Criterion 14 — `mexico_ap_converted`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 88 / 500 |

**Criterion** (paste into text field):

```
Mexico matched Appendix A AP converts to approximately $103,040.95 USD at the memo rate.
```

### Criterion 15 — `s6_test2_void_ap`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 121 / 500 |

**Criterion** (paste into text field):

```
Under memo section 6 test 2, Void AP-C-448 (status_flag Void) is excluded from the Canada AP FX tie-out and is not wired.
```

### Criterion 16 — `s6_test3_duplicate_ap`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 202 / 500 |

**Criterion** (paste into text field):

```
Under memo section 6 test 3, AP-C-448 is identified as a Void duplicate sharing parent_invoice_ref INV-AR-8790 with Open AP-C-441, the Void row is excluded, and the Open payable is retained for tie-out.
```

### Criterion 17 — `s6_test4_orphan_ap`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 150 / 500 |

**Criterion** (paste into text field):

```
Under memo section 6 test 4, orphan payable AP-C-455 (Open with blank parent_invoice_ref) is excluded from the Canada settlement net and is not wired.
```

### Criterion 18 — `s6_test7_intransit_not_orphan`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 179 / 500 |

**Criterion** (paste into text field):

```
Under memo section 6 test 7, missing AP for InTransit Appendix A invoices INV-AR-8841 and INV-AR-8855 is treated as an expected FOB gap and is not classified as an orphan payable.
```

### Criterion 19 — `s6_seven_tests_documented`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 258 / 500 |

**Criterion** (paste into text field):

```
The workbook documents all seven memo section 6 exception tests independently (Void AR; Void AP; duplicate AP; orphan AP; matched Open-only; matched parent_invoice_ref; InTransit missing AP not orphan) rather than collapsing them into fewer than seven tests.
```

### Criterion 20 — `exception_log_seven_fields`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 210 / 500 |

**Criterion** (paste into text field):

```
Each discovered exception in the exception log records the seven memo section 6 documentation fields: record ID, counterparty, exception type, source fact, governing memo rule, treatment, and settlement impact.
```

### Criterion 21 — `exception_self_consistency`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 304 / 500 |

**Criterion** (paste into text field):

```
A self-consistency control compares row-level Include / settlement classification to the exception-log treatment and reports PASS only when there is no contradiction (for example, a row marked Include=Yes is not exception-excluded from settlement, and an exception-excluded row is not still Include=Yes).
```

### Criterion 22 — `parent_usd_governs_wire`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | method |
| Characters | 98 / 500 |

**Criterion** (paste into text field):

```
Wire instructions use parent invoice USD settlement totals rather than converted affiliate AP USD.
```

### Criterion 23 — `canada_settlement_wire`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 174 / 500 |

**Criterion** (paste into text field):

```
Canada Appendix A AR settlement for INV-AR-8841, INV-AR-8790, and INV-AR-8766 equals approximately $319,520.76, and that same amount is the recommended Canada wire to parent.
```

### Criterion 24 — `mexico_settlement_wire`

| Field | Value |
|-------|-------|
| **Weight** | **+5** |
| Importance | Critical |
| Type | rigid |
| Category | accuracy |
| Characters | 174 / 500 |

**Criterion** (paste into text field):

```
Mexico Appendix A AR settlement for INV-AR-8812, INV-AR-8855, and INV-AR-8688 equals approximately $231,480.95, and that same amount is the recommended Mexico wire to parent.
```

### Criterion 25 — `netting_direction`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | judgment |
| Characters | 105 / 500 |

**Criterion** (paste into text field):

```
Counterparty netting states that each affiliate pays the parent for the Appendix A AR settlement amounts.
```

### Criterion 26 — `cutoff_citation`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 151 / 500 |

**Criterion** (paste into text field):

```
The Exceptions section, or equivalent section label, cites intercompany_cutoff_and_fx_memo.txt for FOB shipping-point treatment of in-transit invoices.
```

### Criterion 27 — `memo_governs`

| Field | Value |
|-------|-------|
| **Weight** | **+3** |
| Importance | Important |
| Type | subjective |
| Category | method |
| Characters | 106 / 500 |

**Criterion** (paste into text field):

```
The workbook states that intercompany_cutoff_and_fx_memo.txt governs where the AR and AP ledgers conflict.
```

### Criterion 28 — `recommendation_sweep`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | judgment |
| Characters | 149 / 500 |

**Criterion** (paste into text field):

```
The controller recommendation states September 3 wires collecting Appendix A AR from Canada and Mexico and cites intercompany_cutoff_and_fx_memo.txt.
```

### Criterion 29 — `live_formulas`

| Field | Value |
|-------|-------|
| **Weight** | **+4** |
| Importance | Critical |
| Type | subjective |
| Category | method |
| Characters | 183 / 500 |

**Criterion** (paste into text field):

```
AR settlement totals, AP memo conversions, FX differences, self-consistency PASS/FAIL, and wire amounts are formula-linked to component inputs rather than solely hard-coded endpoints.
```

### Criterion 30 — `neg_stale_cad_rate`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 151 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs Controllers to settle or revalue Canada AP using the stale July CAD rate 1.3680 instead of the August 31 memo rate 1.3724.
```

### Criterion 31 — `neg_settle_provisional`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 124 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs treasury to include Provisional month-end estimate invoices in the September 3 settlement wire.
```

### Criterion 32 — `neg_resweep_settled`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 152 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs Controllers to re-sweep Settled prior-period invoices from the July or early-August extracts on the September 3 wire cycle.
```

### Criterion 33 — `neg_below_materiality`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 143 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs treasury to settle Open AR lines below the Appendix A $35,000 materiality threshold on the September 3 wire cycle.
```

### Criterion 34 — `neg_contradictory_exceptions`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 208 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs treasury to wire a record that the same workbook's exception log excludes from settlement, or to exclude from the wire a record the same workbook marks Include=Yes for settlement.
```

### Criterion 35 — `neg_intransit_as_orphan`

| Field | Value |
|-------|-------|
| **Weight** | **-5** |
| Importance | Failure mode (critical) |
| Type | negative |
| Category | accuracy |
| Characters | 210 / 500 |

**Criterion** (paste into text field):

```
The recommendation instructs Controllers to treat missing affiliate AP for InTransit Appendix A receivables as orphan payables and to exclude those InTransit AR invoices from the September 3 wire on that basis.
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
cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 northline-industrial-holdings-intercompany
```
