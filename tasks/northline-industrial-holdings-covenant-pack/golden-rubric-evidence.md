# Golden ↔ rubric evidence — northline-industrial-holdings-covenant-pack

Human-verified against inputs and `credit_agreement_covenant_excerpts.txt`.

## Key figures

| Item | Value | Source / build |
|------|------:|----------------|
| Term Loan A | $42,850,000.00 | Facilities |
| Revolver drawn | $18,250,000.00 | Facilities |
| Finance leases | $2,184,620.18 | Facilities |
| Seller note | $4,500,000.00 | Facilities — included |
| Intercompany Holdco | $1,200,000.00 | Excluded (Guarantor) |
| Undrawn LC face | $3,200,000.00 | Excluded |
| **Consolidated Funded Debt** | **$67,784,620.18** | TL+RCF+leases+seller |
| Reported EBITDA | $14,228,440.25 | EBITDA bridge E-001 |
| SBC allowed | $412,880.40 | CA (a) |
| Restructuring allowed | $2,000,000.00 | Cap of $2,840,000 claimed |
| Acq costs allowed | $685,220.18 | CA (c) |
| Sponsor fee allowed | $500,000.00 | Cap of $750,000 claimed |
| Inventory step-up | $318,450.22 | CA (d) |
| Synergies rejected | $1,100,000.00 | CA negative (i) |
| Warranty rejected | $425,000.00 | Ordinary Course Warranty |
| **Adjusted EBITDA** | **$18,144,991.05** | Sum of allowed |
| Cash Interest TTM | $4,882,110.40 | Facilities control |
| Total Leverage | 3.7357x | 67,784,620.18 / 18,144,991.05 |
| Interest Coverage | 3.7166x | 18,144,991.05 / 4,882,110.40 |
| Gross CapEx YTD | $9,120,400.55 | CapEx_YTD |
| Permitted Acq CapEx | $1,840,000.00 | CX-2606+CX-2607 |
| CapEx Basket Usage | $7,280,400.55 | Gross − carve-out |
| CapEx remaining | $1,219,599.45 | vs $8,500,000 limit |

## Pass/fail

- Leverage 3.7357 ≤ 4.50 → PASS
- ICR 3.7166 ≥ 2.50 → PASS
- CapEx usage 7,280,400.55 ≤ 8,500,000 → PASS

## Formula audit

- Funded_Debt!B13 = B6+B7+B8+B9 (included components)
- Adjusted_EBITDA!C15 = SUM of lender-allowed column
- Covenant_Tests leverage/ICR/CapEx usage formula-linked
- Recommendation cells link to Covenant_Tests results

## Rubric coverage

All rigid numeric criteria above verified in golden. Negatives are prohibited committee instructions (full restructuring, run-rate synergies, undrawn LC in Funded Debt) — not omission mirrors.
