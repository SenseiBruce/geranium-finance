#!/usr/bin/env python3
"""Validate golden solution zip packaging."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    REPO_ROOT,
    CheckResult,
    extract_deliverable_name,
    inspect_zip,
    print_results,
    read_text,
)


def validate_golden_zip(zip_path: Path, task_dir: Path | None = None) -> list[CheckResult]:
    results: list[CheckResult] = []
    zip_check = inspect_zip(zip_path)
    results.append(zip_check)
    if not zip_check.ok:
        return results

    import zipfile

    with zipfile.ZipFile(zip_path, "r") as zf:
        zip_names = [info.filename.split("/")[-1] for info in zf.infolist() if not info.is_dir()]

    if len(zip_names) == 0:
        r = CheckResult("golden-nonempty")
        r.error("Golden zip contains no files")
        results.append(r)
        return results

    expected_name: str | None = None
    if task_dir:
        for src in [task_dir / "prompt.txt", task_dir / "task-spec.md"]:
            if src.exists():
                expected_name = extract_deliverable_name(read_text(src))
                if expected_name:
                    break

    name_check = CheckResult("deliverable-filename")
    if expected_name:
        if expected_name not in zip_names:
            name_check.error(
                f"Deliverable '{expected_name}' not found in golden zip. Found: {zip_names}"
            )
    else:
        name_check.warn("Could not determine expected deliverable filename from prompt/spec")
    results.append(name_check)

    tell_check = CheckResult("golden-tells")
    for name in zip_names:
        if re.search(r"golden|geranium|ai_output|model_response", name, re.I):
            tell_check.error(f"Filename looks like AI/platform artifact: {name}")
    results.append(tell_check)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--task-dir", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    zip_path = args.zip_path if args.zip_path.is_absolute() else REPO_ROOT / args.zip_path
    task_dir = args.task_dir
    if task_dir and not task_dir.is_absolute():
        task_dir = REPO_ROOT / task_dir

    results = validate_golden_zip(zip_path, task_dir)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
