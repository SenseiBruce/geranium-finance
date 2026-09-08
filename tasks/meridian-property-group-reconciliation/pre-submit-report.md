# Pre-Submit Report — meridian-property-group-reconciliation

Generated: 2026-09-03

## Redesign note

Attempt 2 after portal uniqueness + human-voice failure on the GC allowance/retainage scaffold.
New scenario: **Meridian Commons 2025 CAM annual true-up** (property accounting), not contractor allowance closeout.

## Gate summary

| Gate | Result |
|------|--------|
| seed_uniqueness_check.py | PASS |
| lint_task_spec.py | PASS |
| validate_input_zip.py | PASS |
| lint_prompt.py | PASS |
| validate_golden_zip.py | PASS |
| lint_rubric.py --strict | PASS |
| package_consistency_check.py | PASS |
| golden_vs_rubric.py --strict | PASS |
| task_readiness.py --strict --package | PASS |

## Rubric stats

- Criteria: 25 (4 negative)
- Positive weight: ~74
- Negative weight: 17 (~23% of positive)

## Golden self-audit

- Eligible CAM pool: $412,680
- Contour true-up: +$25,913; Outfitters +$25,557; Harbor −$1,107; Lakeside −$1,405; Ridgeway $0 at cap
- Net additional billings: ~$48,958
- All 25 criteria verified in golden-rubric-evidence.md

## Strip test

- Scaffold: cam_annual_trueup_reconciliation
- Inputs: expense ledger CSV + lease abstracts XLSX + prior billing TXT
- Deliverable: cam_trueup_meridian_commons.xlsx
- Distinct from Harborview consolidation, renewal desks, Helix valuation, and allowance closeout audits

## Upload

From `tasks/meridian-property-group-reconciliation/submission/`:
- Section 1: portal-submission.md + inputs.zip
- Section 2: portal-section2.md + golden.zip
