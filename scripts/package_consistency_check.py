#!/usr/bin/env python3
"""Preflight checks that catch Helix-style portal auto-eval failures.

Detects:
- Rubric entity names missing from inputs / golden (name-drift after renames)
- IEEE-754 float artifacts in golden cached formula values
- Stale submission/ zips vs source folders
- Conjunction criteria that cite board recommendations + source files (judge variance)
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results

# Tokens that usually mark institutional entity names in Finance tasks (single-line only)
_ENTITY_HINT = re.compile(
    r"\b("
    r"[A-Z][a-zA-Z]+(?:[ \t]+[A-Z][a-zA-Z]+){0,3}[ \t]+"
    r"(?:Capital|Partners|Fund|Ventures|Equity|Regional|Labs|Diagnostics|"
    r"Group|Management|Holdings|Associates|Advisors|Bank|Insurance)"
    r")\b"
)

_FLOAT_ARTIFACT = re.compile(r"\.\d*99999|\.\d*00000\d")

_BOARD_CONJUNCTION = re.compile(
    r"(board|sign-?off|recommend).{0,80}(cite|citation|cap_table|investor_brief)",
    re.I | re.S,
)

# "The Cohort Build tab ...", "the Valuation Summary sheet ..."
_TAB_REF = re.compile(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})\s+(?:tab|sheet)\b")

_TAB_ESCAPE = re.compile(r"or equivalent section label", re.I)

# Share of positive weight allowed to depend on tab names the prompt never states
_UNGROUNDED_TAB_BUDGET = 0.25


def _gather_corpus(paths: list[Path]) -> str:
    chunks: list[str] = []
    for p in paths:
        if not p.exists():
            continue
        if p.suffix.lower() in {".txt", ".csv", ".md", ".json"}:
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
        elif p.suffix.lower() in {".xlsx", ".xlsm"}:
            try:
                from openpyxl import load_workbook

                wb = load_workbook(p, data_only=False)
                for ws in wb.worksheets:
                    for row in ws.iter_rows(values_only=True):
                        for cell in row:
                            if isinstance(cell, str):
                                chunks.append(cell)
            except Exception:
                continue
    return "\n".join(chunks)


def _entities_from_rubric(criteria: list[dict]) -> set[str]:
    found: set[str] = set()
    for c in criteria:
        text = c.get("text") or ""
        for m in _ENTITY_HINT.finditer(text):
            found.add(m.group(1).strip())
    return found


def _float_artifacts_in_xlsx(path: Path) -> list[str]:
    """Scan the stored XML, since the platform digest reads those raw strings."""
    hits: list[str] = []
    if not path.exists():
        return hits
    try:
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if not (name.startswith("xl/worksheets/") and name.endswith(".xml")):
                    continue
                xml = zf.read(name).decode("utf-8", errors="ignore")
                for m in re.finditer(r'<c r="([A-Z]+\d+)"[^>]*>(?:<f>[^<]*</f>)?<v>([^<]+)</v>', xml):
                    ref, val = m.group(1), m.group(2)
                    if "." not in val or "e" in val.lower():
                        continue
                    try:
                        shortest = repr(float(val))
                    except ValueError:
                        continue
                    if len(shortest) < len(val):
                        hits.append(f"{name.rsplit('/', 1)[-1]}!{ref}={val}")
    except Exception as exc:
        hits.append(f"could not scan {path.name}: {exc}")
    return hits[:20]


def _zip_stale(task_dir: Path) -> list[str]:
    issues: list[str] = []
    submission = task_dir / "submission"
    for name, src_dir in (("inputs.zip", "inputs"), ("golden.zip", "golden")):
        zpath = submission / name
        sdir = task_dir / src_dir
        if not zpath.exists() or not sdir.exists():
            continue
        z_mtime = zpath.stat().st_mtime
        newest_src = max((p.stat().st_mtime for p in sdir.rglob("*") if p.is_file()), default=0)
        if newest_src > z_mtime + 1:
            issues.append(
                f"{name} older than {src_dir}/ — run: gf repackage {task_dir.name}"
            )
        # Flat archive + expected deliverable presence for golden
        if name == "golden.zip":
            with zipfile.ZipFile(zpath) as zf:
                names = zf.namelist()
                if any("/" in n.rstrip("/") for n in names):
                    issues.append(f"{name} has nested paths: {names}")
    return issues


def _check_tab_grounding(r: CheckResult, criteria: list[dict], prompt_text: Path) -> None:
    """Platform `sound_aligned_rubric` fails when reward rides on tab names the prompt never states."""
    if not prompt_text.exists():
        return
    prompt = prompt_text.read_text(encoding="utf-8", errors="ignore").lower()

    positive_total = sum(c.get("weight", 0) for c in criteria if c.get("weight", 0) > 0)
    if not positive_total:
        return

    ungrounded_weight = 0
    ungrounded_tabs: set[str] = set()
    for c in criteria:
        weight = c.get("weight", 0)
        text = c.get("text") or ""
        if weight <= 0 or _TAB_ESCAPE.search(text):
            continue
        names = {m.group(1).removeprefix("The ").strip() for m in _TAB_REF.finditer(text)}
        missing = {n for n in names if n.lower() not in prompt}
        if missing:
            ungrounded_weight += weight
            ungrounded_tabs |= missing

    share = ungrounded_weight / positive_total
    if share > _UNGROUNDED_TAB_BUDGET:
        r.warn(
            f"{ungrounded_weight} of {positive_total} positive points ({share:.0%}) depend on "
            f"tab names absent from prompt.txt: {sorted(ungrounded_tabs)}. "
            f"Add 'or equivalent section label' to those criteria, or name the sections in the prompt "
            f"(platform audit: sound_aligned_rubric)."
        )


def check_task(task_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    r = CheckResult("package-consistency")

    input_paths = list((task_dir / "inputs").glob("*")) if (task_dir / "inputs").exists() else []
    golden_paths = list((task_dir / "golden").glob("*")) if (task_dir / "golden").exists() else []

    rubric_path = task_dir / "rubric.json"
    if not rubric_path.exists():
        # Step 4 runs this check before Step 5 creates rubric.json.
        r.warn("rubric.json missing — skip entity/tab grounding until Step 5")
    else:
        criteria = json.loads(rubric_path.read_text(encoding="utf-8")).get("criteria", [])
        entities = _entities_from_rubric(criteria)
        prompt_paths = [task_dir / "prompt.txt"]
        input_corpus = _gather_corpus(input_paths + prompt_paths)
        golden_corpus = _gather_corpus(golden_paths)

        prompt_text = ""
        if (task_dir / "prompt.txt").exists():
            prompt_text = (task_dir / "prompt.txt").read_text(encoding="utf-8", errors="ignore")

        for ent in sorted(entities):
            if ent not in input_corpus and ent not in prompt_text:
                r.error(
                    f"Rubric names '{ent}' but it does not appear in inputs/ or prompt.txt "
                    f"(rename drift — update rubric OR revert entity rename)"
                )
            elif ent not in golden_corpus and golden_paths:
                r.warn(
                    f"Rubric names '{ent}' but it was not found as text in golden/ — "
                    f"confirm Cap Table / Notes use the same spelling (oracle drift if portal is ahead of golden)"
                )

        # Reverse drift: investor-style names in inputs missing from rubric (stale portal risk)
        input_only_corpus = _gather_corpus(input_paths + prompt_paths)
        input_entities = {m.group(1).strip() for m in _ENTITY_HINT.finditer(input_only_corpus)}
        for ent in sorted(input_entities - entities):
            if any(
                tok in ent
                for tok in (
                    "Capital",
                    "Partners",
                    "Fund",
                    "Ventures",
                    "Equity",
                    "Holdings",
                    "Advisors",
                )
            ):
                r.warn(
                    f"Inputs/prompt name '{ent}' but no rubric criterion mentions it — "
                    f"if the portal still has an old name, apply find/replace delta before upload"
                )

        _check_tab_grounding(r, criteria, prompt_text=(task_dir / "prompt.txt"))

        for c in criteria:
            text = c.get("text") or ""
            if c.get("weight", 0) > 0 and _BOARD_CONJUNCTION.search(text):
                r.warn(
                    f"Criterion '{c.get('id')}' ties board recommendation + citations in one check "
                    f"(oracle judge variance risk). Put required cites ON the recommendation row "
                    f"in golden Notes, or split the criterion."
                )

    for gpath in golden_paths + input_paths:
        if gpath.suffix.lower() in {".xlsx", ".xlsm"}:
            for hit in _float_artifacts_in_xlsx(gpath):
                r.error(
                    f"Float artifact in {gpath.name}: {hit} — "
                    f"run sanitize_office.sanitize_xlsx (or gf preflight) before packaging"
                )

    for issue in _zip_stale(task_dir):
        r.error(issue)

    # Prompt deliverable must match golden basename
    prompt = (task_dir / "prompt.txt").read_text(encoding="utf-8", errors="ignore") if (
        task_dir / "prompt.txt"
    ).exists() else ""
    m = re.search(
        r"(?:named|workbook named|deliverable(?:\s+is)?|file named)\s+([A-Za-z0-9_\-]+\.xlsx)\b",
        prompt,
        re.I,
    )
    if not m:
        m = re.search(r"\bsingle Excel workbook named\s+([A-Za-z0-9_\-]+\.xlsx)\b", prompt, re.I)
    if m and golden_paths:
        expected = m.group(1)
        gold_names = {p.name for p in golden_paths}
        if expected not in gold_names:
            r.error(f"Prompt deliverable '{expected}' not found in golden/ ({sorted(gold_names)})")

    results.append(r)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir
    results = check_task(task_dir)
    print_results(results)
    if args.strict and any(not x.ok for x in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
