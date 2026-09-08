"""Shared utilities for geranium-finance validation scripts."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent


class CheckResult:
    def __init__(self, name: str):
        self.name = name
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_filenames_from_spec(spec_text: str) -> list[str]:
    """Pull filenames from Input File Plan table or bullet lists."""
    names: list[str] = []
    for match in re.finditer(
        r"[\w\-./]+\.(?:csv|xlsx|xls|pdf|docx|pptx|txt|json|yaml|md|jpeg|jpg|png)",
        spec_text,
        re.IGNORECASE,
    ):
        name = match.group(0).split("/")[-1]
        if name not in names:
            names.append(name)
    return names


def extract_filenames_from_prompt(prompt_text: str) -> list[str]:
    names: list[str] = []
    for match in re.finditer(
        r"[\w\-]+\.(?:csv|xlsx|xls|pdf|docx|pptx|txt|json|yaml|md|jpeg|jpg|png)",
        prompt_text,
        re.IGNORECASE,
    ):
        name = match.group(0)
        if name not in names:
            names.append(name)
    return names


def extract_deliverable_name(text: str) -> str | None:
    patterns = [
        r"(?:named|name(?:d)?|save(?:d)? as|create)\s+[`\"']?([\w\-]+\.(?:xlsx|docx|pptx|pdf))[`\"']?",
        r"([\w\-]+\.(?:xlsx|docx|pptx|pdf))\s*(?:—|--|-|\.)",
        r"\|\s*Filename\s*\|\s*([\w\-]+\.(?:xlsx|docx|pptx|pdf))\s*\|",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1)
    m = re.search(r"([\w\-]+\.(?:xlsx|docx|pptx|pdf))", text, re.IGNORECASE)
    return m.group(1) if m else None


def inspect_zip(zip_path: Path) -> CheckResult:
    result = CheckResult(f"zip:{zip_path.name}")
    if not zip_path.exists():
        result.error(f"Zip not found: {zip_path}")
        return result

    if " " in zip_path.name:
        result.error(f"Zip filename contains spaces: {zip_path.name}")

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                name = info.filename
                if name.endswith("/"):
                    result.error(f"Subfolder or directory entry in zip: {name}")
                    continue
                if "/" in name or "\\" in name:
                    result.error(f"Nested path in zip (no subfolders): {name}")
                base = name.split("/")[-1]
                if " " in base:
                    result.error(f"Filename contains spaces: {base}")
                if re.search(r"\.(xlsx|docx|pdf|pptx|csv|txt)\.\1$", base, re.I):
                    result.error(f"Double extension detected: {base}")
                if info.file_size == 0:
                    result.error(f"Empty file in zip: {base}")
    except zipfile.BadZipFile:
        result.error(f"Corrupt or invalid zip: {zip_path}")

    return result


def print_results(results: list[CheckResult], strict: bool = False) -> int:
    exit_code = 0
    for r in results:
        prefix = "PASS" if r.ok else "FAIL"
        print(f"[{prefix}] {r.name}")
        for w in r.warnings:
            print(f"  WARN: {w}")
        for e in r.errors:
            print(f"  ERROR: {e}")
        if not r.ok:
            exit_code = 1
    if strict and any(not r.ok for r in results):
        exit_code = 1
    return exit_code


def task_dir_from_arg(arg: str | None) -> Path | None:
    if not arg:
        return None
    p = Path(arg)
    if p.is_dir():
        return p
    return None
