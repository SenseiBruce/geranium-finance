#!/usr/bin/env python3
"""Lint practitioner prompt for Geranium quality."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    REPO_ROOT,
    CheckResult,
    extract_deliverable_name,
    extract_filenames_from_spec,
    print_results,
    read_text,
)


LLM_OPENER = re.compile(
    r"^you are a (?:financial )?(?:analyst|controller|underwriter|advisor)",
    re.I | re.M,
)
UTILIZING = re.compile(r"utilizing your expertise|leveraging the provided", re.I)
STEP_LIST = re.compile(r"(?:^|\n)\s*\d+[\.)]\s+(?:open|calculate|check|sort|write|for each)", re.I)
ADJECTIVE_PATTERN = re.compile(
    r"clear,?\s+(?:well[- ]structured|comprehensive|thorough).{0,40}not vague",
    re.I,
)
VAGUE_SUCCESS = re.compile(
    r"make it (?:clear|accurate|comprehensive|thorough|well[- ]organized|easy to follow)",
    re.I,
)


def lint_prompt(prompt_path: Path, task_dir: Path | None = None) -> list[CheckResult]:
    results: list[CheckResult] = []
    text = read_text(prompt_path)
    r = CheckResult("lint-prompt")

    if LLM_OPENER.search(text):
        r.error("Generic role opener detected ('You are a …')")
    if UTILIZING.search(text):
        r.error("LLM phrasing detected ('utilizing/leveraging your expertise')")
    if STEP_LIST.search(text):
        r.error("Step-by-step numbered instructions detected")
    if ADJECTIVE_PATTERN.search(text):
        r.error("LLM adjective pattern detected (stacked adjectives + failure list)")
    if VAGUE_SUCCESS.search(text):
        r.warn("Vague success criteria ('make it clear/accurate/comprehensive')")

    deliverable = extract_deliverable_name(text)
    if not deliverable:
        r.error("No concrete deliverable filename found (e.g. report.xlsx)")
    else:
        if re.search(r"golden|geranium|ai_output", deliverable, re.I):
            r.error(f"Deliverable filename looks synthetic: {deliverable}")

    if not re.search(r"(?i)(input files:|the following input files:)", text):
        r.error("Missing platform detection phrase: 'Input files:' or 'The following input files:'")

    file_refs = re.findall(
        r"[\w\-]+\.(?:csv|xlsx|xls|pdf|docx|pptx|txt)",
        text,
        re.I,
    )
    input_refs = [f for f in file_refs if f != deliverable]
    if len(input_refs) < 1:
        r.error("Prompt should reference at least one input file by name")

    if re.search(r"inputs\.zip|input\.zip|final submission\.zip", text, re.I):
        r.error("Prompt references zip package name instead of inner files")

    if len(text.split()) < 80:
        r.warn("Prompt may be too thin (<80 words) for a 3+ hour task")

    results.append(r)

    if task_dir:
        spec_path = task_dir / "task-spec.md"
        if spec_path.exists():
            spec_names = set(extract_filenames_from_spec(read_text(spec_path)))
            prompt_names = set(input_refs)
            align = CheckResult("prompt-spec-alignment")
            if spec_names and prompt_names and not prompt_names.intersection(spec_names):
                align.warn("Prompt input file names may not match task-spec.md")
            results.append(align)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_path", type=Path)
    parser.add_argument("--task-dir", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    prompt_path = args.prompt_path if args.prompt_path.is_absolute() else REPO_ROOT / args.prompt_path
    task_dir = args.task_dir
    if task_dir and not task_dir.is_absolute():
        task_dir = REPO_ROOT / task_dir

    results = lint_prompt(prompt_path, task_dir)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
