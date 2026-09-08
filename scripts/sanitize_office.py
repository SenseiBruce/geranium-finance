#!/usr/bin/env python3
"""Remove common LLM / tooling tells from Office files before packaging."""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from xml.etree import ElementTree as ET

from common import REPO_ROOT, CheckResult

TOOL_CREATORS = re.compile(r"\b(openpyxl|python-docx|xlsxwriter|pandas)\b", re.I)
NS = {
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}


def clear_macos_xattrs(path: Path) -> None:
    if not path.exists():
        return
    subprocess.run(["xattr", "-c", str(path)], check=False, capture_output=True)


def _patch_core_xml(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)
    changed = False
    for tag in ("creator", "lastModifiedBy"):
        for elem in root.findall(f"dc:{tag}", NS) + root.findall(f"cp:{tag}", NS):
            if elem.text and TOOL_CREATORS.search(elem.text):
                elem.text = ""
                changed = True
    if not changed:
        return xml_bytes
    ET.register_namespace("cp", NS["cp"])
    ET.register_namespace("dc", NS["dc"])
    ET.register_namespace("dcterms", NS["dcterms"])
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _clean_number(val: float) -> str:
    """Render a cached value without IEEE-754 tails.

    Platform digests read the raw <v> text, so 266744662.79999998 reads as an
    LLM/float artifact. Round to 2dp for money-scale values, keep more precision
    for small ratios, and never emit exponent notation.
    """
    if isinstance(val, bool) or isinstance(val, int):
        return str(val)
    f = float(val)
    if f != f or f in (float("inf"), float("-inf")):
        return "0"
    magnitude = abs(f)
    if magnitude >= 1000:
        digits = 2
    elif magnitude >= 1:
        digits = 4
    else:
        digits = 10
    text = f"{round(f, digits):.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cache_xlsx_formula_values(
    path: Path,
    sheet_values: dict[str, dict[str, float | int | str]],
) -> None:
    """Inject cached formula results so digests show computed values.

    Numeric values are normalized through `_clean_number` (no IEEE tails).
    String values are stored as OOXML ``t="str"`` formula results so text
    deliverables (e.g. Quote/Refer/Decline, executive rationale) appear in
    platform digests without requiring Excel recalculation.
    """
    path = path if path.is_absolute() else REPO_ROOT / path
    if not path.exists():
        return

    from openpyxl import load_workbook

    wb = load_workbook(path)
    sheet_index = {ws.title: idx + 1 for idx, ws in enumerate(wb.worksheets)}
    wb.close()

    with zipfile.ZipFile(path, "r") as zin:
        entries = {info.filename: zin.read(info.filename) for info in zin.infolist()}

    cell_re = re.compile(
        r'<c(?P<attrs>(?=[^>]*\sr="(?P<ref>[A-Z]+\d+)")[^>]*)>'
        r'(?P<body><f>[^<]+</f>(?:<v[^>]*>[^<]*</v>|<v\s*/>)?)'
        r'</c>',
        re.S,
    )

    for sheet_name, values in sheet_values.items():
        idx = sheet_index.get(sheet_name)
        if not idx:
            continue
        fname = f"xl/worksheets/sheet{idx}.xml"
        if fname not in entries:
            continue
        xml = entries[fname].decode("utf-8")

        def repl(match: re.Match[str]) -> str:
            ref = match.group("ref")
            if ref not in values:
                return match.group(0)
            body = match.group("body")
            if "<f>" not in body:
                return match.group(0)
            formula = re.search(r"<f>([^<]+)</f>", body)
            if not formula:
                return match.group(0)
            raw = values[ref]
            attrs = match.group("attrs")
            # Drop any existing type attr, then set the correct one.
            attrs = re.sub(r'\s+t="[^"]*"', "", attrs)
            # Keep r= first when present so naive digest parsers that match
            # ^<c r="..." still find the cell.
            r_match = re.search(r'\s+r="([A-Z]+\d+)"', attrs)
            if r_match:
                attrs = re.sub(r'\s+r="[A-Z]+\d+"', "", attrs)
                r_attr = f' r="{r_match.group(1)}"'
            else:
                r_attr = ""
            if isinstance(raw, str):
                type_attr = ' t="str"'
                val = _xml_escape(raw)
            else:
                type_attr = ' t="n"'
                val = _clean_number(raw)
            return f"<c{r_attr}{type_attr}{attrs}><f>{formula.group(1)}</f><v>{val}</v></c>"

        entries[fname] = cell_re.sub(repl, xml).encode("utf-8")

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp_path = Path(tmp.name)
    with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in entries.items():
            zout.writestr(name, data)
    tmp_path.replace(path)


_VALUE_TAG = re.compile(r"<v>([^<]+)</v>")


def _shorten_value(match: re.Match[str]) -> str:
    """Rewrite a stored number as its shortest round-tripping form.

    openpyxl serializes floats with "%.16g", which surfaces IEEE tails such as
    95.90000000000001 for a literal 95.9. Python's repr gives the shortest text
    that parses back to the identical double, so this is lossless.
    """
    text = match.group(1)
    if "." not in text or "e" in text.lower():
        return match.group(0)
    try:
        shortest = repr(float(text))
    except ValueError:
        return match.group(0)
    if "e" in shortest.lower() or len(shortest) >= len(text):
        return match.group(0)
    return f"<v>{shortest}</v>"


def normalize_xlsx_numbers(data: bytes) -> bytes:
    """Collapse float artifacts in a worksheet XML payload."""
    return _VALUE_TAG.sub(_shorten_value, data.decode("utf-8")).encode("utf-8")


def sanitize_xlsx(path: Path) -> bool:
    """Strip tool creator metadata and float artifacts. Returns True if modified."""
    path = path if path.is_absolute() else REPO_ROOT / path
    if not path.exists() or path.suffix.lower() != ".xlsx":
        return False

    clear_macos_xattrs(path)
    modified = False
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp_path = Path(tmp.name)

    try:
        with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename == "docProps/core.xml":
                    patched = _patch_core_xml(data)
                    if patched != data:
                        data = patched
                        modified = True
                elif info.filename.startswith("xl/worksheets/") and info.filename.endswith(".xml"):
                    patched = normalize_xlsx_numbers(data)
                    if patched != data:
                        data = patched
                        modified = True
                zout.writestr(info, data)
        if modified:
            tmp_path.replace(path)
    finally:
        if tmp_path.exists() and not modified:
            tmp_path.unlink(missing_ok=True)

    return modified


def scan_xlsx_tells(path: Path) -> list[str]:
    path = path if path.is_absolute() else REPO_ROOT / path
    issues: list[str] = []
    if not path.exists():
        return [f"File not found: {path}"]
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if "docProps/core.xml" in zf.namelist():
                core = zf.read("docProps/core.xml").decode("utf-8", errors="replace")
                if TOOL_CREATORS.search(core):
                    issues.append("docProps/core.xml lists a Python tool as creator/lastModifiedBy")
    except zipfile.BadZipFile:
        issues.append("Corrupt or invalid xlsx zip")
    return issues


def sanitize_folder(folder: Path) -> list[Path]:
    folder = folder if folder.is_absolute() else REPO_ROOT / folder
    changed: list[Path] = []
    if not folder.is_dir():
        return changed
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        clear_macos_xattrs(path)
        if path.suffix.lower() == ".xlsx" and sanitize_xlsx(path):
            changed.append(path)
    return changed


def check_office_tells(paths: list[Path]) -> list[CheckResult]:
    results: list[CheckResult] = []
    for path in paths:
        if path.suffix.lower() != ".xlsx":
            continue
        r = CheckResult(path.name)
        for issue in scan_xlsx_tells(path):
            r.warn(issue)
        results.append(r)
    return results


def main() -> None:
    import argparse

    from common import print_results

    parser = argparse.ArgumentParser(description="Sanitize Office file metadata before packaging")
    parser.add_argument("paths", nargs="+", type=Path, help="Task dir or inputs/golden folder paths")
    parser.add_argument("--check-only", action="store_true", help="Scan for tells without modifying")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if args.check_only:
        files: list[Path] = []
        for raw in args.paths:
            p = raw if raw.is_absolute() else REPO_ROOT / raw
            if p.is_dir():
                files.extend(sorted(x for x in p.iterdir() if x.suffix.lower() == ".xlsx"))
            elif p.suffix.lower() == ".xlsx":
                files.append(p)
        raise SystemExit(print_results(check_office_tells(files), strict=args.strict))

    for raw in args.paths:
        p = raw if raw.is_absolute() else REPO_ROOT / raw
        if p.is_dir():
            changed = sanitize_folder(p)
            for path in changed:
                print(f"Sanitized {path}")
        elif p.suffix.lower() == ".xlsx" and sanitize_xlsx(p):
            print(f"Sanitized {p}")


if __name__ == "__main__":
    main()
