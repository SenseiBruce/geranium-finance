#!/usr/bin/env python3
"""Generate golden-vs-rubric audit checklist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results, read_text


def golden_vs_rubric(task_dir: Path, force: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []
    rubric_path = task_dir / "rubric.json"
    audit_path = task_dir / "golden-rubric-audit.json"
    evidence_path = task_dir / "golden-rubric-evidence.md"

    if not rubric_path.exists():
        r = CheckResult("golden-vs-rubric")
        r.error("rubric.json not found")
        return [r]

    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    criteria = rubric["criteria"]

    if not force and evidence_path.exists():
        text = evidence_path.read_text(encoding="utf-8")
        if "- [ ]" not in text and "- [x]" in text:
            r = CheckResult("golden-vs-rubric")
            r.warn(f"Using existing completed audit: {evidence_path.name}")
            results.append(r)
            return results

    audit = {
        "task": task_dir.name,
        "criteria_count": len(criteria),
        "manual_review_required": True,
        "items": [],
    }

    unverified = 0
    for c in criteria:
        item = {
            "id": c.get("id"),
            "weight": c.get("weight"),
            "type": c.get("type"),
            "text": c.get("text"),
            "golden_passes": None,
            "notes": "Verify manually against golden solution",
        }
        audit["items"].append(item)
        unverified += 1

    audit_path.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    r = CheckResult("golden-vs-rubric")
    r.warn(
        f"Wrote {audit_path.name} with {unverified} criteria requiring manual golden verification"
    )

    if force or not evidence_path.exists():
        lines = [
            f"# Golden vs Rubric Evidence — {task_dir.name}",
            "",
            "Mark each criterion PASS/FAIL after verifying against golden solution.",
            "",
        ]
        for c in criteria:
            sign = "+" if c.get("weight", 0) > 0 else ""
            lines.append(f"- [ ] **{c.get('id')}** ({sign}{c.get('weight')}): {c.get('text')}")
        evidence_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        r.warn(f"Wrote {evidence_path.name} — complete self-audit before Step 6")

    positive = sum(c["weight"] for c in criteria if c.get("weight", 0) > 0)
    negative = sum(abs(c["weight"]) for c in criteria if c.get("weight", 0) < 0)
    if positive and negative / positive < 0.20:
        r.error("Negative weight ratio below 20% — fix rubric before submit")

    results.append(r)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir
    results = golden_vs_rubric(task_dir, force=args.force)

    evidence = task_dir / "golden-rubric-evidence.md"
    if args.strict and evidence.exists():
        text = read_text(evidence)
        if "- [ ]" in text:
            r = CheckResult("audit-complete")
            r.error("golden-rubric-evidence.md has unchecked items — complete manual audit")
            results.append(r)

    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
