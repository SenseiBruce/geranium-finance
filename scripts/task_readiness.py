#!/usr/bin/env python3
"""Final task readiness gate — all steps and validators."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import REPO_ROOT, CheckResult, load_jsonl, print_results


STEP_MARKERS = [
    ".step2b-complete",
    ".step3-complete",
    ".step4-complete",
    ".step5-complete",
]


def run_script(script: str, args: list[str]) -> tuple[int, str]:
    python = REPO_ROOT / ".venv" / "bin" / "python"
    if not python.exists():
        python = Path(sys.executable)
    cmd = [str(python), str(REPO_ROOT / "scripts" / script)] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    return proc.returncode, output


def task_readiness(task_dir: Path, strict: bool = False, package: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []

    if not task_dir.is_dir():
        r = CheckResult("task-dir")
        r.error(f"Task directory not found: {task_dir}")
        return [r]

    if package:
        from package_zips import repackage_task_zips, sync_submission_folder

        repackage_task_zips(task_dir)
        m = CheckResult("repackage-zips")
        m.warn(
            "Rebuilt inputs.zip and golden.zip from source folders "
            "(previous zips archived under archives/zips/)"
        )
        results.append(m)

    for marker in STEP_MARKERS:
        m = CheckResult(marker)
        if not (task_dir / marker).exists():
            m.error(f"Missing completion marker: {marker}")
        results.append(m)

    required = ["task-spec.md", "metadata.yaml", "prompt.txt", "rubric.json", "inputs.zip", "golden.zip"]
    for name in required:
        m = CheckResult(f"file:{name}")
        if not (task_dir / name).exists():
            m.error(f"Missing required file: {name}")
        results.append(m)

    checks = [
        ("lint_task_spec.py", [str(task_dir / "task-spec.md"), "--strict"]),
        ("validate_input_zip.py", [str(task_dir / "inputs.zip"), "--task-dir", str(task_dir), "--strict"]),
        ("lint_prompt.py", [str(task_dir / "prompt.txt"), "--task-dir", str(task_dir), "--strict"]),
        ("validate_golden_zip.py", [str(task_dir / "golden.zip"), "--task-dir", str(task_dir), "--strict"]),
        ("lint_rubric.py", [str(task_dir / "rubric.json"), "--strict"]),
        ("package_consistency_check.py", [str(task_dir), "--strict"]),
        ("golden_vs_rubric.py", [str(task_dir)]),
        ("seed_uniqueness_check.py", ["check", "--task-dir", str(task_dir)]),
    ]

    for script, args in checks:
        code, output = run_script(script, args)
        m = CheckResult(script)
        if code != 0:
            m.error(f"Gate failed — run manually for details")
            for line in output.strip().splitlines()[-5:]:
                m.warn(line)
        results.append(m)

    if package and all(r.ok for r in results):
        from package_zips import sync_submission_folder

        sub = sync_submission_folder(task_dir)
        report = task_dir / "pre-submit-report.md"

        registry_path = REPO_ROOT / "registry" / "task-registry.jsonl"
        meta: dict = {"slug": task_dir.name}
        metadata_file = task_dir / "metadata.yaml"
        if metadata_file.exists():
            try:
                import yaml

                meta = yaml.safe_load(metadata_file.read_text(encoding="utf-8")) or meta
            except ImportError:
                meta["slug"] = task_dir.name
            except Exception:
                meta = {"slug": task_dir.name}

        onet_block = ""
        onet_code = meta.get("onet", {}).get("code", "")
        if onet_code:
            sys.path.insert(0, str(REPO_ROOT / "scripts"))
            from onet_lookup import format_portal_block, lookup, validate_metadata

            onet_data = lookup(onet_code)
            onet_errors = validate_metadata(meta.get("onet", {}))
            onet_block = "\n\n" + format_portal_block(
                onet_data,
                meta_tasks=meta.get("onet", {}).get("tasks"),
                meta_skills=meta.get("onet", {}).get("skills"),
            )
            if onet_errors:
                onet_block += "\n\n**Fix metadata.yaml before portal submit:**\n"
                for e in onet_errors:
                    onet_block += f"- {e}\n"

        if not report.exists():
            report.write_text(
                f"# Pre-Submit Report — {task_dir.name}\n\n"
                f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n"
                f"All local gates passed.\n"
                f"{onet_block}",
                encoding="utf-8",
            )
            shutil.copy2(report, sub / "pre-submit-report.md")
        elif onet_block:
            body = report.read_text(encoding="utf-8")
            if "## Portal O*NET" not in body:
                report.write_text(body.rstrip() + "\n" + onet_block + "\n", encoding="utf-8")
                shutil.copy2(report, sub / "pre-submit-report.md")

        entry = {
            "slug": task_dir.name,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "occupation": meta.get("onet", {}).get("occupation", ""),
            "onet_code": meta.get("onet", {}).get("code", ""),
            "deliverable": meta.get("deliverable", {}).get("filename", ""),
            "status": "ready_to_submit",
        }
        existing = {r.get("slug") for r in load_jsonl(registry_path)}
        if task_dir.name not in existing:
            with registry_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")

        m = CheckResult("package")
        m.warn(f"Submission folder populated at {sub}")
        results.append(m)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--package", action="store_true")
    args = parser.parse_args()

    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir
    results = task_readiness(task_dir, strict=args.strict, package=args.package)

    if args.strict and all(r.ok for r in results):
        (task_dir / ".step6-complete").touch()

    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
