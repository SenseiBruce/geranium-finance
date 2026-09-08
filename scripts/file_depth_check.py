#!/usr/bin/env python3
"""Check input file depth floors."""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results


def count_xlsx_cells(path: Path) -> int:
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        return -1

    count = 0
    with zipfile.ZipFile(path, "r") as zf:
        sheets = [n for n in zf.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
        for sheet in sheets:
            root = ET.fromstring(zf.read(sheet))
            for cell in root.iter():
                if cell.tag.endswith("}v") or cell.tag.endswith("}t"):
                    if cell.text and cell.text.strip():
                        count += 1
    return count


def count_csv_cells(path: Path) -> int:
    count = 0
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            count += sum(1 for c in row if c.strip())
    return count


def word_count_text(path: Path) -> int:
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b\w+\b", text))


def file_depth_check(inputs_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    if not inputs_dir.is_dir():
        r = CheckResult("inputs-dir")
        r.error(f"Inputs directory not found: {inputs_dir}")
        return [r]

    files = [f for f in inputs_dir.iterdir() if f.is_file()]
    if not files:
        r = CheckResult("inputs-nonempty")
        r.error("No input files found")
        return [r]

    total_cells = 0
    for f in files:
        r = CheckResult(f.name)
        ext = f.suffix.lower()
        if ext == ".xlsx":
            cells = count_xlsx_cells(f)
            if cells >= 0 and cells < 100:
                r.warn(f"Spreadsheet may be below 100 populated cells (estimated {cells})")
            total_cells += max(cells, 0)
        elif ext == ".csv":
            cells = count_csv_cells(f)
            if cells < 30:
                r.warn(f"CSV may be thin ({cells} populated cells)")
            total_cells += cells
        elif ext in {".txt", ".md"}:
            words = word_count_text(f)
            if words < 200:
                r.warn(f"Text file may be below 200 words ({words} words)")
        elif ext == ".pdf":
            words = word_count_text(f)
            if words < 100:
                r.warn(f"PDF text extract thin ({words} words) — verify substantive content")
        elif ext == ".docx":
            words = word_count_text(f)
            if words < 200:
                r.warn(f"DOCX may be below depth floor ({words} words extracted)")

        if f.stat().st_size == 0:
            r.error("File is empty")

        results.append(r)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    inputs_dir = args.inputs_dir if args.inputs_dir.is_absolute() else REPO_ROOT / args.inputs_dir
    results = file_depth_check(inputs_dir)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
