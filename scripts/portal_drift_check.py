#!/usr/bin/env python3
"""Portal drift card: rubric ↔ inputs ↔ golden entity sync before upload.

Helix lesson: golden/inputs renamed while portal rubric still had old names → oracle ~0.66.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import REPO_ROOT, CheckResult, print_results
from package_consistency_check import _ENTITY_HINT, _gather_corpus, check_task

_NEGATION_PREFIX = re.compile(r"\bNo\s+", re.I)


def portal_sync_card(task_dir: Path) -> str:
    lines = [
        f"# Portal sync card — {task_dir.name}",
        "",
        "Before upload: confirm the **portal** rubric/prompt match repo entities.",
        "After a rename: find/replace **delta only** — do not wipe all criteria.",
        "",
    ]
    rubric_path = task_dir / "rubric.json"
    if not rubric_path.exists():
        lines.append("_No rubric.json yet._")
        return "\n".join(lines)

    criteria = json.loads(rubric_path.read_text(encoding="utf-8")).get("criteria", [])
    rubric_ents: set[str] = set()
    for c in criteria:
        for m in _ENTITY_HINT.finditer(c.get("text") or ""):
            rubric_ents.add(m.group(1).strip())

    inputs = list((task_dir / "inputs").glob("*")) if (task_dir / "inputs").exists() else []
    golden = list((task_dir / "golden").glob("*")) if (task_dir / "golden").exists() else []
    prompt = [task_dir / "prompt.txt"]
    input_ents = {
        m.group(1).strip()
        for m in _ENTITY_HINT.finditer(_gather_corpus(inputs + prompt))
    }
    golden_ents = {m.group(1).strip() for m in _ENTITY_HINT.finditer(_gather_corpus(golden))}

    lines.append("## Entities in rubric.json")
    for e in sorted(rubric_ents) or ["_(none matched)_"]:
        lines.append(f"- {e}")
    lines.append("")
    lines.append("## In inputs/prompt but not rubric")
    missing_r = sorted(input_ents - rubric_ents)
    for e in missing_r or ["_(none)_"]:
        lines.append(f"- {e}")
    lines.append("")
    lines.append("## In rubric but not inputs/prompt (BLOCKING if true)")
    missing_i = sorted(rubric_ents - input_ents)
    for e in missing_i or ["_(none)_"]:
        lines.append(f"- {e}")
    lines.append("")
    lines.append("## In rubric but not golden text")
    missing_g = sorted(rubric_ents - golden_ents)
    for e in missing_g or ["_(none)_"]:
        lines.append(f"- {e}")
    lines.append("")
    if missing_i:
        lines.append("**Action:** fix rubric or regenerate inputs — do not upload.")
    elif missing_r:
        lines.append(
            "**Action:** if portal still shows old names for the input entities above, "
            "apply find/replace delta on those criteria only."
        )
    else:
        lines.append("**Action:** repo entity surfaces look aligned; paste prompt/criteria from submission/.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--card-only", action="store_true", help="Print sync card only (no consistency scan)")
    args = parser.parse_args()
    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir

    print(portal_sync_card(task_dir))
    print()
    if args.card_only:
        return

    results = check_task(task_dir)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
