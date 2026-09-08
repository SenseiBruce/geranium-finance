#!/usr/bin/env python3
"""Validate input zip packaging and name alignment."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    REPO_ROOT,
    CheckResult,
    extract_deliverable_name,
    extract_filenames_from_prompt,
    extract_filenames_from_spec,
    inspect_zip,
    print_results,
    read_text,
)


def validate_input_zip(
    zip_path: Path,
    task_dir: Path | None = None,
    prompt_path: Path | None = None,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    zip_check = inspect_zip(zip_path)
    results.append(zip_check)
    if not zip_check.ok:
        return results

    import zipfile

    with zipfile.ZipFile(zip_path, "r") as zf:
        zip_names = {info.filename.split("/")[-1] for info in zf.infolist() if not info.is_dir()}

    expected: set[str] = set()
    if prompt_path and prompt_path.exists():
        prompt_text = read_text(prompt_path)
        for name in extract_filenames_from_prompt(prompt_text):
            if name != extract_deliverable_name(prompt_text):
                expected.add(name)
        if not re.search(r"(?i)(input files:|the following input files:)", prompt_text):
            r = CheckResult("prompt-detection-phrase")
            r.warn("Prompt missing 'Input files:' or 'The following input files:' phrase")
            results.append(r)
    elif task_dir:
        spec_path = task_dir / "task-spec.md"
        meta_path = task_dir / "metadata.yaml"
        if meta_path.exists():
            import yaml

            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            for name in meta.get("input_files") or []:
                expected.add(name)
        elif spec_path.exists():
            spec_text = read_text(spec_path)
            expected.update(extract_filenames_from_spec(spec_text))
            deliverable = extract_deliverable_name(spec_text)
            if deliverable:
                expected.discard(deliverable)

    if expected:
        align = CheckResult("filename-alignment")
        missing = expected - zip_names
        extra = zip_names - expected
        for m in sorted(missing):
            align.error(f"Expected input file missing from zip: {m}")
        for e in sorted(extra):
            align.warn(f"File in zip not listed in spec/prompt: {e}")
        results.append(align)

    size_check = CheckResult("zip-size")
    total = sum(
        (REPO_ROOT / zip_path).stat().st_size if not zip_path.is_absolute() else zip_path.stat().st_size
        for _ in [0]
    )
    mb = zip_path.stat().st_size / (1024 * 1024)
    if mb > 30:
        size_check.error(f"Zip exceeds 30 MB limit: {mb:.1f} MB")
    if len(zip_names) > 20:
        size_check.error(f"More than 20 files in zip: {len(zip_names)}")
    results.append(size_check)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--task-dir", type=Path, default=None)
    parser.add_argument("--prompt", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    zip_path = args.zip_path
    if not zip_path.is_absolute():
        zip_path = REPO_ROOT / zip_path

    prompt_path = args.prompt
    if prompt_path and not prompt_path.is_absolute():
        prompt_path = REPO_ROOT / prompt_path

    task_dir = args.task_dir
    if task_dir and not task_dir.is_absolute():
        task_dir = REPO_ROOT / task_dir

    if task_dir and not prompt_path:
        candidate = task_dir / "prompt.txt"
        if candidate.exists():
            prompt_path = candidate

    results = validate_input_zip(zip_path, task_dir, prompt_path)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
