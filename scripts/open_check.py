#!/usr/bin/env python3
"""Verify golden files exist and are non-empty."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results


def open_check(golden_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    if not golden_dir.is_dir():
        r = CheckResult("golden-dir")
        r.error(f"Golden directory not found: {golden_dir}")
        return [r]

    files = [f for f in golden_dir.iterdir() if f.is_file()]
    if not files:
        r = CheckResult("golden-nonempty")
        r.error("No golden deliverable files found")
        return [r]

    for f in files:
        r = CheckResult(f.name)
        if f.stat().st_size == 0:
            r.error("File is empty")
        if f.stat().st_size < 1024:
            r.warn("File is very small (<1 KB) — verify substantive content")
        results.append(r)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("golden_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    golden_dir = args.golden_dir if args.golden_dir.is_absolute() else REPO_ROOT / args.golden_dir
    results = open_check(golden_dir)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
