#!/usr/bin/env python3
"""Lint task-spec.md for required sections."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results, read_text

REQUIRED_SECTIONS = [
    "Situation",
    "Deliverable",
    "Input File Plan",
    "Expert Judgment",
    "Traps",
    "Rubric Preview",
    "Metadata",
]


def lint_task_spec(spec_path: Path) -> list[CheckResult]:
    text = read_text(spec_path)
    r = CheckResult("lint-task-spec")

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^#{{1,3}}\s+.*{re.escape(section)}", text, re.I | re.M):
            if section == "Traps":
                if not re.search(r"traps|difficulty", text, re.I):
                    r.error(f"Missing section: {section} / Difficulty")
            else:
                r.error(f"Missing section: {section}")

    if re.search(r"you are a (?:financial )?(?:analyst|controller)", text, re.I):
        r.warn("Spec situation uses generic role opener — prefer situation-first in final prompt")

    if not re.search(r"\.(?:xlsx|docx|pptx|pdf)", text, re.I):
        r.error("No deliverable filename with extension found in spec")

    file_rows = re.findall(r"[\w\-]+\.(?:csv|xlsx|pdf|docx|pptx|txt)", text, re.I)
    if len(set(file_rows)) < 2:
        r.warn("Fewer than 2 distinct input filenames in spec (2+ strongly preferred)")

    time_match = re.search(r"time estimate.*?(\d+)", text, re.I)
    if time_match:
        hours = int(time_match.group(1))
        if hours < 3:
            r.error(f"Time estimate {hours}h below 3-hour minimum")
        elif hours < 5:
            r.warn(f"Time estimate {hours}h — aim 5+ for safety buffer")

    return [r]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec_path", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    spec_path = args.spec_path if args.spec_path.is_absolute() else REPO_ROOT / args.spec_path
    results = lint_task_spec(spec_path)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
