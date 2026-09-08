#!/usr/bin/env python3
"""Package inputs/ or golden/ folders into platform-ready zips."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from common import REPO_ROOT
from sanitize_office import sanitize_folder


def archive_zip_if_exists(zip_path: Path, task_dir: Path) -> Path | None:
    """Copy an existing zip into archives/zips/<timestamp>/ before replacing it."""
    if not zip_path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = task_dir / "archives" / "zips" / stamp
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / zip_path.name
    shutil.copy2(zip_path, dest)
    return dest


def package_folder(folder: Path, zip_path: Path, *, task_dir: Path | None = None) -> Path | None:
    """Build a fresh zip from folder contents; archive prior zip when task_dir is set."""
    if not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")

    sanitized = sanitize_folder(folder)
    if sanitized:
        print(f"Sanitized metadata on {len(sanitized)} file(s) in {folder.name}/")

    files = sorted(f for f in folder.iterdir() if f.is_file())
    if not files:
        raise SystemExit(f"No files to zip in {folder}")

    archived: Path | None = None
    if task_dir is not None:
        archived = archive_zip_if_exists(zip_path, task_dir)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)

    if archived:
        print(f"Archived previous {zip_path.name} → {archived}")
    print(f"Created {zip_path} ({len(files)} files)")
    return archived


def repackage_task_zips(
    task_dir: Path,
    *,
    inputs: bool = True,
    golden: bool = True,
) -> None:
    """Always rebuild task zips from source folders (archiving any existing zips first)."""
    if inputs:
        package_folder(task_dir / "inputs", task_dir / "inputs.zip", task_dir=task_dir)
    if golden:
        package_folder(task_dir / "golden", task_dir / "golden.zip", task_dir=task_dir)


def sync_submission_folder(task_dir: Path) -> Path:
    """Copy latest platform artifacts into submission/ (fresh zips, not copies of copies)."""
    sub = task_dir / "submission"
    sub.mkdir(exist_ok=True)
    for name in ["prompt.txt", "inputs.zip", "golden.zip", "rubric.json", "metadata.yaml", "task.toml"]:
        src = task_dir / name
        if src.exists():
            shutil.copy2(src, sub / name)
    tests_src = task_dir / "tests"
    if tests_src.is_dir():
        tests_dest = sub / "tests"
        if tests_dest.exists():
            shutil.rmtree(tests_dest)
        shutil.copytree(tests_src, tests_dest)
    report = task_dir / "pre-submit-report.md"
    if report.exists():
        shutil.copy2(report, sub / "pre-submit-report.md")
    portal = task_dir / "portal-submission.md"
    if portal.exists():
        shutil.copy2(portal, sub / "portal-submission.md")
    portal2 = task_dir / "portal-section2.md"
    if portal2.exists():
        shutil.copy2(portal2, sub / "portal-section2.md")
    return sub


def main() -> None:
    parser = argparse.ArgumentParser(description="Package task inputs or golden folders.")
    parser.add_argument("task_dir", type=Path, help="tasks/<slug>/ directory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inputs", action="store_true", help="Package inputs/ → inputs.zip")
    group.add_argument("--golden", action="store_true", help="Package golden/ → golden.zip")
    group.add_argument("--all", action="store_true", help="Package both inputs and golden")
    parser.add_argument(
        "--sync-submission",
        action="store_true",
        help="After packaging, copy latest artifacts to submission/",
    )
    args = parser.parse_args()

    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir
    if args.all:
        repackage_task_zips(task_dir)
    elif args.inputs:
        package_folder(task_dir / "inputs", task_dir / "inputs.zip", task_dir=task_dir)
    else:
        package_folder(task_dir / "golden", task_dir / "golden.zip", task_dir=task_dir)

    if args.sync_submission:
        dest = sync_submission_folder(task_dir)
        print(f"Synced submission folder: {dest}")


if __name__ == "__main__":
    main()
