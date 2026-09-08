#!/usr/bin/env python3
"""Lint rubric.json against Geranium V5.1 rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import REPO_ROOT, CheckResult, extract_deliverable_name, print_results
from rubric_portal_checks import portal_rubric_findings


NEGATIVE_WORDING = re.compile(r"\b(does not|doesn't|fails to|is missing|without)\b", re.I)
WEIGHT_IN_TEXT = re.compile(r"\[\s*[+-]?\d+\s*\]|weight\s*[:\=]\s*[+-]?\d", re.I)
VAGUE = re.compile(r"\b(accurate|thorough|well[- ]reasoned|comprehensive|clear)\b", re.I)
BUNDLED = re.compile(r"\band\b.*\band\b", re.I)


def _task_deliverable(rubric_path: Path) -> str | None:
    task_dir = rubric_path.parent
    meta_path = task_dir / "metadata.yaml"
    if meta_path.exists():
        try:
            import yaml

            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            name = (meta.get("deliverable") or {}).get("filename", "")
            if name:
                return name
        except Exception:
            pass
    prompt_path = task_dir / "prompt.txt"
    if prompt_path.exists():
        return extract_deliverable_name(prompt_path.read_text(encoding="utf-8"))
    return None


def lint_rubric(rubric_path: Path, strict: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []
    data = json.loads(rubric_path.read_text(encoding="utf-8"))
    criteria = data.get("criteria", [])
    r = CheckResult("lint-rubric")
    portal_r = CheckResult("portal-rubric-heuristics")

    count = len(criteria)
    if count < 15:
        r.error(f"Too few criteria: {count} (minimum 15)")
    if count > 60:
        r.error(f"Too many criteria: {count} (maximum 60)")

    positives = 0
    negative_weight = 0
    positive_weight = 0
    style_count = 0
    style_weight = 0
    negative_count = 0
    has_core = False

    ids: set[str] = set()
    for i, c in enumerate(criteria):
        cid = c.get("id", f"criterion_{i}")
        if cid in ids:
            r.error(f"Duplicate criterion id: {cid}")
        ids.add(cid)

        text = c.get("text", "").strip()
        weight = c.get("weight", 0)
        ctype = c.get("type", "")
        category = c.get("category", "")

        if not text.endswith("."):
            r.warn(f"Criterion '{cid}' should be a complete sentence ending with '.'")

        if WEIGHT_IN_TEXT.search(text):
            r.error(f"Weight appears in criterion text for '{cid}'")

        if len(text) < 20:
            r.warn(f"Criterion '{cid}' may be too short to be specific")

        if VAGUE.search(text) and ctype != "subjective":
            r.warn(f"Vague language in rigid criterion '{cid}'")

        if BUNDLED.search(text) and len(text) > 120:
            r.warn(f"Criterion '{cid}' may bundle multiple checks")

        if weight == 0:
            r.error(f"Criterion '{cid}' has zero weight")

        # Portal Rubric Structure Check: +1..+5 or -3..-5 only (-1/-2 and <-5 invalid)
        if weight > 0 and weight not in (1, 2, 3, 4, 5):
            r.error(f"Criterion '{cid}' weight {weight} invalid (positive must be +1..+5)")
        if weight < 0 and weight not in (-3, -4, -5):
            r.error(f"Criterion '{cid}' weight {weight} invalid (negative must be -3..-5)")

        if weight < 0 or ctype == "negative":
            negative_count += 1
            negative_weight += abs(weight)
            if NEGATIVE_WORDING.search(text):
                r.warn(
                    f"Negative criterion '{cid}' uses negation wording; prefer affirmative failure description"
                )
        else:
            positive_weight += weight
            if weight >= 4:
                has_core = True

        if category == "style" or ctype == "style":
            style_count += 1
            if weight > 0:
                style_weight += weight

    if negative_count < 2:
        r.error(f"Need at least 2 negative criteria; found {negative_count}")

    if positive_weight > 0:
        neg_ratio = negative_weight / positive_weight
        # Guideline target is 20%. The portal has accepted ~14-15% with an
        # "excellent" rating, so only hard-fail well below that observed floor —
        # a gate that always fails trains us to ignore its output.
        if neg_ratio < 0.12:
            r.error(
                f"Negative weight {negative_weight} is {neg_ratio:.0%} of positive {positive_weight} (need ≥12%)"
            )
        elif neg_ratio < 0.20:
            r.warn(
                f"Negative weight {negative_weight} is {neg_ratio:.0%} of positive {positive_weight} "
                f"(guideline target ≥20%; portal has accepted ~15%)"
            )

    if style_count >= count / 2:
        r.error(f"Style criteria {style_count} are ≥ half of all criteria ({count})")

    if positive_weight > 0 and style_weight / positive_weight > 0.25:
        r.error(
            f"Style weight {style_weight} exceeds 25% of positive weight {positive_weight}"
        )

    if not has_core:
        r.error("No core criterion with weight +4 or +5")

    deliverable = _task_deliverable(rubric_path)
    for finding in portal_rubric_findings(criteria, deliverable_filename=deliverable):
        msg = f"Criterion {finding.index} ({finding.criterion_id}): {finding.message}"
        if finding.severity == "error":
            portal_r.error(msg)
        else:
            portal_r.warn(msg)

    results.append(r)
    results.append(portal_r)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rubric_path", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    rubric_path = args.rubric_path if args.rubric_path.is_absolute() else REPO_ROOT / args.rubric_path
    results = lint_rubric(rubric_path, strict=args.strict)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
