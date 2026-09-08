# Geranium Guidelines Summary (V5.1)

Condensed reference for Finance & Insurance task authoring. Full source: Project Geranium Guidelines V5.1.

## What you submit

1. **Prompt + input files** — colleague handoff voice; named deliverable; 2+ input files
2. **Golden solution + rubric** — human-verified; 15–60 criteria
3. **AHT** — honest minutes

## Quality bar

- **3+ hours** manual work without LLM (aim **5+**)
- Difficulty from **input files + reasoning**, not prompt length
- Frontier model first-pass success → task too easy
- US-based work (international OK for US companies abroad)

## Prompt rules

| Do | Don't |
|----|-------|
| Situation-first opener | "You are a financial analyst at…" |
| Exact input file names | "the attached spreadsheet" |
| Concrete output filename | "a comprehensive report" |
| State what & why | Numbered step-by-step how |
| Natural practitioner voice | "Utilizing your expertise…" |

Platform detection: use `Input files:` or `The following input files:` then list names.

## Input file rules

- Min 1 file; **2+ strongly preferred**; max 20 files, 30 MB
- Single zip; **root level only**; no subfolders
- Names match prompt exactly; no spaces; no double extensions
- Substantial, field-authentic, no leakage
- No copyrighted/restricted content

### Depth floors

| Type | Minimum |
|------|---------|
| Prose memo/report | 500 words body |
| Spreadsheet | 100 populated cells; 10+ per tab |
| Presentation | 5 slides; slide master required (golden) |
| Correspondence | 200 words |

## Golden solution rules

- Verify every number yourself
- Client/manager-ready polish
- Spreadsheets: **dynamic formulas**
- Output filename matches prompt
- Zip packaging same as inputs

## Rubric rules (V5.1)

| Weight | Use |
|--------|-----|
| +4 to +5 | Critical deliverable |
| +2 to +3 | Structure, key finding |
| +1 | Minor detail |
| -3 to -5 | Critical failure |

- 15–60 criteria; **atomic** (one check each)
- **≥2 negative** criteria; negatives ≥ **20%** of positive weight
- Style/formatting: **<50%** of criteria AND ≤ **25%** of reward
- Rigid: exact value. Subjective: bounded conditions (not vague)
- Negative wording: affirm failure ("The deliverable has X issue")
- Golden must score **~100** on your rubric

## O*NET metadata

- Occupation from [onetonline.org/find/industry](https://www.onetonline.org/find/industry) → Finance and Insurance
- 3–5 tasks, 3–5 skills (genuinely exercised)
- Multimodal: yes only with images/audio/video
- Web search: no if self-contained

## Uniqueness (strip test)

If stripping domain nouns leaves identical skeleton → same task. Change:

1. Opener style
2. File mix / information distribution
3. Decision structure / deliverable type

## Common rejections

- Thin or LLM-generated files
- Prompt answerable without files
- Overspecified prompt
- Rubric restates prompt vaguely
- Golden is raw LLM output
- File names don't match prompt
- Rubric grades golden.zip instead of the deliverable file
- Negative criteria mirror positive omissions (portal penalty-scope fail)
- Process-timing rubric language ("before recommending…") instead of document order

See [`portal-rubric-quality.md`](portal-rubric-quality.md) for Section 2 rubric check patterns.

## Portal rubric (Section 2)

- Copy criteria from `gf portal2 <slug>` — verbatim, weights in separate field only
- Negatives: -3 to -5, affirmative prohibited recommendations
- Final-outcome focus: every criterion inspectable in the submitted workbook/file
