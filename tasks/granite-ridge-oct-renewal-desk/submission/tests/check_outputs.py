#!/usr/bin/env python3
"""
Output and input-integrity checks for Granite Ridge October renewal desk.

Fail closed:
- Required deliverable must exist, use the exact filename, open as .xlsx, and
  contain expected underwriting sheets.
- Grading inputs must come from an immutable snapshot; snapshot failure does not
  fall back to a writable live inputs directory.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

REQUIRED_DELIVERABLE = "renewal_underwriting_review.xlsx"
XLSX_MAGIC = b"PK"  # OOXML is a zip package
MIN_BYTES = 2_000  # sanity floor; not a substitute for name/type checks

REQUIRED_INPUTS = (
    "granite_ridge_renewal_accounts.csv",
    "granite_ridge_location_schedule.csv",
    "granite_ridge_loss_run_36mo.csv",
    "granite_ridge_routing_notes.txt",
)

REQUIRED_SHEETS = (
    "Account_Routing",
    "Location_Exceptions",
    "Loss_Reconciliation",
    "Rules_Citations",
    "Summary",
)


class CheckError(Exception):
    """Hard verification failure — do not continue grading."""


def _die(msg: str) -> None:
    raise CheckError(msg)


def find_deliverable(output_dir: Path) -> Path:
    """Locate the required workbook; reject size-only or wrong-name passes."""
    if not output_dir.is_dir():
        _die(f"Output directory missing: {output_dir}")

    exact = output_dir / REQUIRED_DELIVERABLE
    if exact.is_file():
        return exact

    matches = sorted(output_dir.rglob(REQUIRED_DELIVERABLE))
    if len(matches) == 1 and matches[0].is_file():
        return matches[0]
    if len(matches) > 1:
        _die(
            f"Multiple copies of {REQUIRED_DELIVERABLE} found under {output_dir}; "
            "submit exactly one workbook with the required filename."
        )

    others = [p for p in output_dir.rglob("*") if p.is_file()]
    names = ", ".join(sorted(p.name for p in others)[:12]) or "(none)"
    _die(
        f"Required deliverable {REQUIRED_DELIVERABLE!r} not found under {output_dir}. "
        f"Files present: {names}"
    )


def validate_xlsx(path: Path) -> None:
    if path.suffix.lower() != ".xlsx":
        _die(f"Deliverable must be an Excel workbook (.xlsx); got {path.name}")
    size = path.stat().st_size
    if size < MIN_BYTES:
        _die(f"{path.name} is too small ({size} bytes) to be a valid workbook")
    head = path.read_bytes()[:2]
    if head != XLSX_MAGIC:
        _die(f"{path.name} is not a valid OOXML/xlsx package (bad magic)")
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
    except zipfile.BadZipFile as exc:
        _die(f"{path.name} is not a readable zip/xlsx: {exc}")
    required_parts = {"[Content_Types].xml", "xl/workbook.xml"}
    missing = required_parts - names
    if missing:
        _die(f"{path.name} is missing xlsx parts: {sorted(missing)}")

    try:
        from openpyxl import load_workbook
    except ImportError:
        return

    try:
        wb = load_workbook(path, read_only=True, data_only=False)
    except Exception as exc:  # noqa: BLE001
        _die(f"{path.name} could not be opened as a workbook: {exc}")
    try:
        present = set(wb.sheetnames)
    finally:
        wb.close()
    missing_sheets = [s for s in REQUIRED_SHEETS if s not in present]
    if missing_sheets:
        _die(
            f"{path.name} missing required sheet(s): {missing_sheets}. "
            f"Found: {sorted(present)}"
        )


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_input_snapshot(snapshot_path: Path) -> dict:
    """
    Load immutable input snapshot manifest.

    Expected JSON shape:
      {
        "inputs_dir": "/path/to/snapshot/inputs",
        "files": {"granite_ridge_renewal_accounts.csv": "<sha256>", ...}
      }
    """
    if not snapshot_path.is_file():
        _die(
            f"Input snapshot missing at {snapshot_path}. "
            "HARD FAILURE — refusing to grade against a live/writable inputs directory."
        )
    try:
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _die(f"Input snapshot unreadable ({snapshot_path}): {exc}")
    if not isinstance(data, dict) or "files" not in data or "inputs_dir" not in data:
        _die(f"Input snapshot schema invalid: {snapshot_path}")
    return data


def _is_writable_dir(path: Path) -> bool:
    """True if the directory itself is writable by this process."""
    try:
        return path.is_dir() and os.access(path, os.W_OK)
    except OSError:
        return True  # treat probe failure as untrusted


def verify_input_integrity(snapshot_path: Path) -> Path:
    """
    Resolve grading inputs from snapshot only.

    Fail closed: any hash mismatch, missing file, absent snapshot,
    declared live fallback, or writable/untrusted snapshot tree aborts.
    Never silently resumes against a mutable live inputs directory.
    """
    if os.environ.get("ALLOW_LIVE_INPUT_FALLBACK", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        _die(
            "ALLOW_LIVE_INPUT_FALLBACK is set. HARD FAILURE — "
            "this verifier never grades against a live/writable fallback."
        )

    snap = load_input_snapshot(snapshot_path)

    for banned_key in ("fallback_inputs_dir", "live_inputs_dir", "writable_inputs_dir"):
        if banned_key in snap:
            _die(
                f"Snapshot declares {banned_key!r}. HARD FAILURE — "
                "live/writable input fallback is not permitted."
            )

    inputs_dir = Path(snap["inputs_dir"]).resolve()
    if not inputs_dir.is_dir():
        _die(
            f"Snapshot inputs_dir does not exist: {inputs_dir}. "
            "HARD FAILURE — refusing live-directory fallback."
        )

    if _is_writable_dir(inputs_dir):
        _die(
            f"Snapshot inputs_dir is writable/untrusted: {inputs_dir}. "
            "HARD FAILURE — grading requires an immutable input snapshot."
        )

    files = snap["files"]
    if not isinstance(files, dict):
        _die("Snapshot 'files' must be a filename→sha256 map")

    for name in REQUIRED_INPUTS:
        if name not in files:
            _die(f"Snapshot missing required input {name!r}")
        path = inputs_dir / name
        if not path.is_file():
            _die(f"Snapshotted input missing on disk: {path}")
        if os.access(path, os.W_OK):
            _die(
                f"Snapshotted input is writable/untrusted: {path}. "
                "HARD FAILURE — not falling back to live inputs."
            )
        digest = _sha256_file(path)
        expected = files[name]
        if digest != expected:
            _die(
                f"Input integrity failure for {name}: "
                f"sha256 {digest} != snapshot {expected}. "
                "HARD FAILURE — not falling back to live inputs."
            )
    return inputs_dir


def check_outputs(
    output_dir: Path,
    *,
    snapshot_path: Path | None = None,
    require_snapshot: bool = True,
) -> Path:
    """
    Validate deliverable and required input snapshot.

    Returns path to the validated workbook.
    """
    if require_snapshot:
        if snapshot_path is None:
            _die(
                "snapshot_path is required (require_snapshot=True). "
                "Grading will not use an unverified live inputs directory."
            )
        verify_input_integrity(snapshot_path)

    deliverable = find_deliverable(output_dir)
    validate_xlsx(deliverable)
    return deliverable


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 1 or "--snapshot" not in argv:
        print(
            "Usage: check_outputs.py <output_dir> --snapshot PATH\n"
            "Snapshot is required (fail closed). No live-input fallback.",
            file=sys.stderr,
        )
        return 2

    output_dir = Path(argv[0])
    i = argv.index("--snapshot")
    if i + 1 >= len(argv):
        print("--snapshot requires a path", file=sys.stderr)
        return 2
    snapshot_path = Path(argv[i + 1])

    try:
        path = check_outputs(
            output_dir,
            snapshot_path=snapshot_path,
            require_snapshot=True,
        )
    except CheckError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"PASS: deliverable ok → {path}")
    print(f"PASS: input snapshot integrity ok → {snapshot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
