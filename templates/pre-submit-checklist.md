# Pre-Submission Checklist (Geranium V5.1)

Use before Step 7 platform upload. Mark each line PASS / FAIL / N/A.

## Prompt

- [ ] Written in natural voice (not LLM-generated)
- [ ] Specific expert context (who, for whom, why now)
- [ ] Multi-step reasoning; 3+ hour workflow (target 5+)
- [ ] Names concrete output file
- [ ] References input files by exact name
- [ ] Includes `Input files:` or `The following input files:` phrase
- [ ] Not solvable by frontier LLM in single pass
- [ ] No spelling/grammar errors
- [ ] No step-by-step how-to disguised as task
- [ ] No reference to zip filename instead of inner files

## Input Files

- [ ] Real documents in depth and structure
- [ ] Substantial (not placeholder)
- [ ] Not 100% synthetic / no LLM tells
- [ ] Zip: no subfolders, no empty files, no double extensions, no spaces
- [ ] Names match prompt exactly (case and extension)
- [ ] No paywalled/copyrighted/restricted content
- [ ] No answer leakage (totals, conclusions, hidden tabs)
- [ ] No project/eval references in files or metadata

## Metadata

- [ ] O*NET occupation matches sector
- [ ] `gf onet <slug>` run — tasks/skills copied verbatim from dropdown list
- [ ] Tasks from O*NET page (3–5, genuinely exercised)
- [ ] Skills from **Essential Skills** section only (3–5)
- [ ] Multimodal boolean matches file contents
- [ ] Web-search boolean matches prompt
- [ ] Time estimate reflects 3+ hour workflow

## Golden Solution

- [ ] Answers every part of prompt
- [ ] Fact-checked against input files
- [ ] Would score 100 on rubric
- [ ] Mostly human-edited
- [ ] Client/manager-ready formatting
- [ ] Spreadsheets: live formulas (if applicable)
- [ ] Presentations: backgrounds/charts/tables (if applicable)
- [ ] Output filename matches prompt
- [ ] Opens cleanly; zip rules same as inputs

## Rubric

- [ ] 15–60 criteria
- [ ] Each criterion atomic and specific
- [ ] Correct answers human-calculated
- [ ] No weights in criterion text
- [ ] Rigid vs subjective correctly typed
- [ ] Reasoning checked where wrong method could reach right answer
- [ ] ≥2 negative criteria; negatives ≥20% of positive weight (portal may accept ~15% — local lint enforces 20%)
- [ ] Style/formatting <50% of criteria and ≤25% of reward
- [ ] Filename criterion if prompt names exact file
- [ ] Negative criteria worded affirmatively
- [ ] Golden scores ~100 on self-audit
- [ ] No golden.zip / archive-root criteria (grade submitted deliverable only)
- [ ] No process-timing language; use tab document order where sequencing matters
- [ ] Negatives are prohibited *decisions*, not omission mirrors of positives
- [ ] `lint_rubric.py --strict` passes portal heuristics; `portal-section2.md` has no ERROR warnings

## Batch / Uniqueness

- [ ] Strip test passed vs other tasks in batch
- [ ] No shared input filenames with other tasks
- [ ] Distinct opener, file mix, and scaffold

## Auto-Eval Readiness

- [ ] `gf portal <slug>` run — `portal-submission.md` reviewed (Section 1)
- [ ] `gf portal2 <slug>` run — `portal-section2.md` reviewed (Section 2)
- [ ] Unzipped and opened every file locally
- [ ] xlsx files sanitized (no `openpyxl` creator in docProps) — `gf repackage` does this automatically
- [ ] Rubric Quality Check run on platform (pre-submit if available)
- [ ] Optional: frontier model test noted in pre-submit-report
