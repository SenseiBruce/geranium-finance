# Step 1: Ideation and Uniqueness

Use this step in Cursor or ChatGPT **before** creating any files under `tasks/`.

## Goal

Produce a finance-domain task seed that survives Geranium review: unique architecture, 5+ hour manual effort, authentic practitioner scenario.

## Inputs

- [`docs/finance-occupations.md`](../docs/finance-occupations.md) — occupation archetypes
- [`docs/geranium-guidelines-summary.md`](../docs/geranium-guidelines-summary.md) — quality bar
- Existing batch: [`registry/task-registry.jsonl`](../registry/task-registry.jsonl)

## Do

1. **Pick O*NET occupation** under Finance & Insurance at [onetonline.org/find/industry](https://www.onetonline.org/find/industry).
2. **Design on two levers:**
   - **Lever 1 — Input file archetype:** How facts are distributed (single workbook vs fragmented CSV+PDF+memo).
   - **Lever 2 — Task scaffold:** Situation, decision structure, deliverable type.
3. **Strip test:** Remove domain nouns. If the skeleton matches another seed, redesign opener, file mix, or decision structure. Check `registry/skeletons.json` / `gf skeleton status` — reuse of a mapped skeleton is a **hard register fail**.
4. **Name deliverable:** Exact output filename (e.g. `renewal_underwriting_review.xlsx`).
5. **Plan 2+ input files** with distinct roles; no file alone contains the answer.
6. **Note traps:** FX conversion, proration, void rows, governing hierarchy, budget caps, etc.
7. **Draft metadata:** O*NET code, 3–5 tasks, 3–5 skills, multimodal (yes only if images/audio/video), web search, time estimate (≥3, aim 5+).

## Skeleton gate

```bash
.venv/bin/python scripts/gf.py skeleton status
.venv/bin/python scripts/gf.py skeleton pick
```

`trueup_reconcile` is **CLOSED** (Pelliston Uniqueness FAIL vs Meridian). Prefer FREE skeletons (`covenant_headroom_pack`, `intercompany_settlement`, `claims_reserve_triangle`) for new work.
## Output

Append one JSON line to `registry/seeds.jsonl`:

```json
{
  "seed_id": "camelot-q1-consolidation",
  "slug": "camelot-q1-consolidation",
  "occupation": "Treasurers and Controllers",
  "onet_code": "11-3031.01",
  "opener_pattern": "situation_first",
  "file_mix": ["csv", "pdf", "pdf"],
  "deliverable_type": "xlsx",
  "deliverable_name": "consolidated_review_camelot_entertainment_group.xlsx",
  "scaffold": "multi_entity_consolidation_with_fx_and_acquisition",
  "topology": "Q1 board close with CAD label and mid-period acquisition",
  "input_filenames": ["camelot_entertainment_group_brand_ledger.csv", "nimue_digital_acquisition_memo.pdf", "excalibur_creative_fx_and_period_reference.pdf"],
  "time_estimate_hours": 5,
  "status": "seed"
}
```

Optional: `specs/<slug>-seed.md` with narrative notes.

## Gate

```bash
python3 scripts/seed_uniqueness_check.py check \
  --seed-id <slug> \
  --topology "<distinct topology phrase>" \
  --scaffold <scaffold_id> \
  --file-mix csv,pdf,pdf \
  --opener-pattern situation_first
```

Fix collisions before proceeding to Step 2a.

## Do NOT

- Reuse input filenames from another task in your batch.
- Use generic "You are a financial analyst" framing.
- Design a task answerable without opening input files.
- Copy Terminal-Bench or prior Geranium task skeletons verbatim.

## Next step

Fresh Cursor chat → [`step2a-task-spec.md`](step2a-task-spec.md)
