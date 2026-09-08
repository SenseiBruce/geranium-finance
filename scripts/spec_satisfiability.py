#!/usr/bin/env python3
"""Check that prompt requirements have rubric coverage hooks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import REPO_ROOT, CheckResult, extract_deliverable_name, print_results, read_text


def spec_satisfiability(spec_path: Path) -> list[CheckResult]:
    text = read_text(spec_path)
    r = CheckResult("spec-satisfiability")

    deliverable = extract_deliverable_name(text)
    if not deliverable:
        r.error("Spec must name a deliverable file for rubric satisfiability")

    requirements_section = re.search(
        r"## Prompt Requirements.*?(?=## |\Z)",
        text,
        re.I | re.S,
    )
    if not requirements_section:
        r.warn("No 'Prompt Requirements' checklist section — add for satisfiability tracking")

    unchecked = len(re.findall(r"- \[ \]", text))
    if unchecked > 0:
        r.warn(f"Spec has {unchecked} unchecked prompt requirement items")

    task_dir = spec_path.parent
    rubric_path = task_dir / "rubric.json"
    if rubric_path.exists():
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        texts = " ".join(c.get("text", "") for c in rubric.get("criteria", []))
        if deliverable and deliverable not in texts:
            r.error(f"Rubric missing criterion referencing deliverable filename: {deliverable}")
    else:
        r.warn("rubric.json not yet present — re-run after Step 5")

    return [r]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec_path", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    spec_path = args.spec_path if args.spec_path.is_absolute() else REPO_ROOT / args.spec_path
    results = spec_satisfiability(spec_path)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
