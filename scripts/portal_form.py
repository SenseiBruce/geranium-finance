#!/usr/bin/env python3
"""Generate Snorkel portal Section 1 and Section 2 form answers from task artifacts."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from common import REPO_ROOT, extract_deliverable_name
from rubric_portal_checks import portal_rubric_findings

PORTAL_CRITERION_MAX = 500
GERANIUM_NAME = re.compile(r"\bgeranium\b", re.I)


def load_yaml(path: Path) -> dict:
    try:
        import yaml

        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except ImportError:
        return {}
    except Exception:
        return {}


def count_input_files(task_dir: Path, meta: dict) -> int:
    listed = meta.get("input_files") or []
    if listed:
        return len(listed)
    inputs_zip = task_dir / "inputs.zip"
    if inputs_zip.exists():
        with zipfile.ZipFile(inputs_zip) as zf:
            return len([n for n in zf.namelist() if not n.endswith("/")])
    inputs_dir = task_dir / "inputs"
    if inputs_dir.is_dir():
        return len([f for f in inputs_dir.iterdir() if f.is_file()])
    return 0


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def occupation_portal_value(onet: dict, onet_data: dict) -> str:
    code = onet.get("code", "")
    name = onet.get("occupation") or onet_data.get("occupation", "")
    return f"{code}|{name}"


def rubric_summary(task_dir: Path) -> dict:
    rubric_path = task_dir / "rubric.json"
    if not rubric_path.exists():
        return {}
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    criteria = rubric.get("criteria", [])
    positives = [c for c in criteria if c.get("weight", 0) > 0]
    negatives = [c for c in criteria if c.get("weight", 0) < 0]
    pos_weight = sum(c.get("weight", 0) for c in positives)
    neg_weight = sum(abs(c.get("weight", 0)) for c in negatives)
    return {
        "count": len(criteria),
        "positive_count": len(positives),
        "negative_count": len(negatives),
        "positive_weight": pos_weight,
        "negative_weight": neg_weight,
        "criteria": criteria,
    }


def build_portal_form(task_dir: Path) -> str:
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    slug = task_dir.name
    meta = load_yaml(task_dir / "metadata.yaml")
    onet = meta.get("onet", {})
    platform = meta.get("platform", {})
    deliverable = meta.get("deliverable", {})

    prompt_path = task_dir / "prompt.txt"
    prompt_text = prompt_path.read_text(encoding="utf-8").strip() if prompt_path.exists() else ""

    sys_path = REPO_ROOT / "scripts"
    import sys

    sys.path.insert(0, str(sys_path))
    from onet_lookup import lookup, validate_metadata

    onet_code = onet.get("code", "")
    onet_data = lookup(onet_code) if onet_code else {}
    onet_errors = validate_metadata(onet) if onet_code else ["metadata.yaml missing onet.code"]

    tasks = onet.get("tasks") or []
    skills = onet.get("skills") or []
    input_count = count_input_files(task_dir, meta)
    multimodal = bool(platform.get("multimodal", False))
    web_search = bool(platform.get("web_search_allowed", False))
    hours = platform.get("time_estimate_hours", 5)
    deliverable_name = deliverable.get("filename", "")

    rubric = rubric_summary(task_dir)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Portal Submission Form — {slug}",
        "",
        f"Generated: {generated}",
        "",
        "Copy each block into the Snorkel Expert Platform. Run checks in the order listed at the bottom.",
        "",
        "---",
        "",
        "## Section 1 — Prompt and Input Files",
        "",
        "### User Prompt",
        "",
        "Paste into **User Prompt** (max 3000 characters):",
        "",
        "```",
        prompt_text,
        "```",
        "",
        f"Character count: {len(prompt_text)} / 3000",
        "",
        "### O*NET Occupation",
        "",
        "Select **one** occupation from the dropdown (select this before tasks/skills):",
        "",
        f"`{occupation_portal_value(onet, onet_data)}`",
        "",
        "### O*NET Tasks",
        "",
        "Select from dropdown (minimum 2, maximum 10). Copy exact strings:",
        "",
    ]
    for i, task in enumerate(tasks, 1):
        lines.append(f"{i}. {task}")
    if not tasks:
        lines.append("_No tasks in metadata.yaml — run `gf onet <slug>` and update metadata._")

    lines += [
        "",
        "### O*NET Skills",
        "",
        "Select from **Essential Skills** dropdown only (NOT technology skills). Minimum 2:",
        "",
    ]
    for skill in skills:
        lines.append(f"- {skill}")
    if not skills:
        lines.append("_No skills in metadata.yaml — run `gf onet <slug>` and update metadata._")

    if onet_errors:
        lines += ["", "### O*NET validation warnings", ""]
        for err in onet_errors:
            lines.append(f"- {err}")

    lines += [
        "",
        "### Input File Uploader",
        "",
        f"Upload: `tasks/{slug}/submission/inputs.zip`",
        "",
        "### How many input files are tied to your prompt?",
        "",
        str(input_count),
        "",
        "### Are any input files in the task multi-modal?",
        "",
        yes_no(multimodal),
        "",
        "_Check Yes only if input files contain video, audio, or images in addition to text._",
        "",
        "### Is web search required for your task?",
        "",
        yes_no(web_search),
        "",
        "### If you were to complete this prompt manually without the help of any LLM's, how long would this task take?",
        "",
        str(hours),
        "",
        "---",
        "",
        "## Section 2 — Golden Solution & Rubric",
        "",
        "_Section 1 must pass first. Then run `gf portal2 <slug>` for full Section 2 copy-paste fields._",
        "",
        f"Quick ref — upload golden: `tasks/{slug}/submission/golden.zip`",
        f"Expected deliverable: `{deliverable_name}`",
        "",
    ]

    if rubric:
        lines += [
            f"Rubric criteria: **{rubric['count']}** "
            f"({rubric['positive_count']} positive, {rubric['negative_count']} negative)",
            "",
        ]

    lines += [
        "---",
        "",
        "## Section 3 — AHT",
        "",
        "Report honest minutes from task start through submit.",
        "",
        "---",
        "",
        "## Portal check order",
        "",
        "1. Paste **User Prompt**",
        "2. Select **O*NET Occupation** (one only)",
        "3. Run **O*NET Compliance Check**",
        "4. Select **O*NET Tasks** and **O*NET Skills**",
        "5. Run **O*NET Tasks & Skills Compliance Check**",
        "6. Run **Prompt Quality Check**",
        "7. Upload **inputs.zip** and set input count / multimodal",
        "8. Run **Input Files Quality Check**",
        "9. Set **web search** and **hours**",
        "10. Continue to Section 2 — run `gf portal2 <slug>`",
        "",
        "## Regenerate Section 1",
        "",
        f"```bash",
        f"cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal {slug}",
        f"```",
        "",
    ]

    return "\n".join(lines)


def golden_zip_contents(task_dir: Path) -> list[str]:
    golden_zip = task_dir / "golden.zip"
    if not golden_zip.exists():
        return []
    with zipfile.ZipFile(golden_zip) as zf:
        return sorted(n for n in zf.namelist() if not n.endswith("/"))


def weight_label(weight: int) -> str:
    w = abs(weight)
    if weight < 0:
        if w >= 5:
            return "Failure mode (critical)"
        return "Failure mode (important)"
    if w >= 4:
        return "Critical"
    if w >= 2:
        return "Important"
    return "Minor"


def build_portal_section2(task_dir: Path) -> str:
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    slug = task_dir.name
    meta = load_yaml(task_dir / "metadata.yaml")
    deliverable_name = meta.get("deliverable", {}).get("filename", "")
    prompt_text = (task_dir / "prompt.txt").read_text(encoding="utf-8") if (task_dir / "prompt.txt").exists() else ""
    prompt_deliverable = extract_deliverable_name(prompt_text) or deliverable_name

    rubric = rubric_summary(task_dir)
    criteria = rubric.get("criteria", [])
    golden_files = golden_zip_contents(task_dir)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Portal Section 2 — {slug}",
        "",
        f"Generated: {generated}",
        "",
        "Use after **Section 1 passes**. Copy each criterion into the portal rubric fields.",
        "Put **weight only** in the Weight field — never in the criterion text.",
        "",
        "---",
        "",
        "## Golden Solution File Uploader",
        "",
        f"**Upload:** `tasks/{slug}/submission/golden.zip`",
        "",
        f"**Expected deliverable in prompt:** `{prompt_deliverable}`",
        "",
        "**Files inside golden.zip:**",
        "",
    ]
    if golden_files:
        for name in golden_files:
            lines.append(f"- `{name}`")
    else:
        lines.append("_golden.zip not found — run `gf repackage <slug>` first._")

    lines += [
        "",
        "### Before upload",
        "",
        "- Human-reviewed golden (not raw LLM output with surface edits only)",
        "- Client-ready formatting; spreadsheets use live formulas where the prompt requires them",
        "- Flat zip at root level (no subfolders)",
        "- Filename matches prompt exactly",
        "",
        "---",
        "",
        "## Rubric criteria",
        "",
        f"Enter **{len(criteria)}** criteria in order. Portal limit: **{PORTAL_CRITERION_MAX}** characters per criterion text.",
        "",
    ]

    if rubric:
        lines += [
            f"| Stat | Value |",
            f"|------|-------|",
            f"| Total criteria | {rubric['count']} |",
            f"| Positive | {rubric['positive_count']} (+{rubric['positive_weight']}) |",
            f"| Negative | {rubric['negative_count']} (-{rubric['negative_weight']}) |",
            "",
        ]

    warnings: list[str] = []
    for finding in portal_rubric_findings(
        criteria, deliverable_filename=prompt_deliverable or deliverable_name
    ):
        prefix = "ERROR" if finding.severity == "error" else "WARN"
        warnings.append(
            f"[{prefix}] Criterion {finding.index} ({finding.criterion_id}): {finding.message}"
        )

    for i, c in enumerate(criteria, 1):
        text = c.get("text", "").strip()
        weight = c.get("weight", 0)
        cid = c.get("id", f"criterion_{i}")
        ctype = c.get("type", "")
        category = c.get("category", "")

        if len(text) > PORTAL_CRITERION_MAX:
            warnings.append(f"Criterion {i} ({cid}) is {len(text)} chars — shorten before portal entry")
        if GERANIUM_NAME.search(text):
            warnings.append(f"Criterion {i} ({cid}) contains 'Geranium' — Name Check will fail")

        sign = "+" if weight > 0 else ""
        lines += [
            f"### Criterion {i} — `{cid}`",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| **Weight** | **{sign}{weight}** |",
            f"| Importance | {weight_label(weight)} |",
            f"| Type | {ctype} |",
            f"| Category | {category} |",
            f"| Characters | {len(text)} / {PORTAL_CRITERION_MAX} |",
            "",
            "**Criterion** (paste into text field):",
            "",
            "```",
            text,
            "```",
            "",
        ]

    if warnings:
        lines += ["---", "", "## Warnings", ""]
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Section 2 check order",
        "",
        "1. Upload **golden.zip**",
        "2. Run **Golden Solution Files Quality Check**",
        "3. Enter all rubric criteria (text + weight separately)",
        "4. Run **Rubric Quality Check**",
        "5. Run **Name Check**",
        "6. Wait for auto-eval feedback boxes (~15–30 min) if submission needs revision",
        "",
        "---",
        "",
        "## Regenerate",
        "",
        "```bash",
        f"cd ~/Projects/geranium-finance && .venv/bin/python scripts/gf.py portal2 {slug}",
        "```",
        "",
    ]

    return "\n".join(lines)


def validate_portal_section2(task_dir: Path) -> list[str]:
    errors: list[str] = []
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    for name in ("prompt.txt", "rubric.json", "golden.zip"):
        if not (task_dir / name).exists():
            errors.append(f"Missing {name}")

    rubric_path = task_dir / "rubric.json"
    if rubric_path.exists():
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        criteria = rubric.get("criteria", [])
        if len(criteria) < 15:
            errors.append(f"Rubric has {len(criteria)} criteria — portal expects 15+")
        for i, c in enumerate(criteria, 1):
            text = c.get("text", "")
            if len(text) > PORTAL_CRITERION_MAX:
                errors.append(f"Criterion {i} exceeds {PORTAL_CRITERION_MAX} chars ({len(text)})")
            if GERANIUM_NAME.search(text):
                errors.append(f"Criterion {i} contains 'Geranium'")

    prompt = task_dir / "prompt.txt"
    meta = load_yaml(task_dir / "metadata.yaml")
    deliverable = meta.get("deliverable", {}).get("filename", "")
    if prompt.exists() and deliverable:
        if deliverable not in prompt.read_text(encoding="utf-8"):
            errors.append(f"prompt.txt does not mention deliverable {deliverable}")

    golden_files = golden_zip_contents(task_dir)
    if deliverable and golden_files and deliverable not in golden_files:
        errors.append(f"golden.zip missing {deliverable}")

    return errors


def validate_portal_form(task_dir: Path) -> list[str]:
    """Return errors that block portal form generation."""
    errors: list[str] = []
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    for name in ("prompt.txt", "metadata.yaml"):
        if not (task_dir / name).exists():
            errors.append(f"Missing {name}")
    meta = load_yaml(task_dir / "metadata.yaml")
    onet = meta.get("onet", {})
    if not onet.get("code"):
        errors.append("metadata.yaml missing onet.code")
    if not onet.get("tasks"):
        errors.append("metadata.yaml missing onet.tasks")
    if not onet.get("skills"):
        errors.append("metadata.yaml missing onet.skills")
    if not (task_dir / "inputs.zip").exists():
        errors.append("Missing inputs.zip — run gf gate 2b or repackage first")

    if onet.get("code"):
        import sys

        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from onet_lookup import validate_metadata

        errors.extend(validate_metadata(onet))

    prompt = task_dir / "prompt.txt"
    if prompt.exists():
        text = prompt.read_text(encoding="utf-8")
        if len(text) > 3000:
            errors.append(f"prompt.txt is {len(text)} chars — portal limit is 3000")
    return errors


def write_portal_form(task_dir: Path, *, sync_submission: bool = False) -> Path:
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    errors = validate_portal_form(task_dir)
    if errors:
        raise SystemExit("Portal form validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    content = build_portal_form(task_dir)
    out = task_dir / "portal-submission.md"
    out.write_text(content, encoding="utf-8")
    if sync_submission:
        _sync_portal_file(task_dir, "portal-submission.md", content)
    return out


def write_portal_section2(task_dir: Path, *, sync_submission: bool = False) -> Path:
    task_dir = task_dir if task_dir.is_absolute() else REPO_ROOT / task_dir
    errors = validate_portal_section2(task_dir)
    if errors:
        raise SystemExit("Portal Section 2 validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    content = build_portal_section2(task_dir)
    out = task_dir / "portal-section2.md"
    out.write_text(content, encoding="utf-8")
    if sync_submission:
        _sync_portal_file(task_dir, "portal-section2.md", content)
    return out


def _sync_portal_file(task_dir: Path, name: str, content: str) -> None:
    sub = task_dir / "submission"
    sub.mkdir(exist_ok=True)
    (sub / name).write_text(content, encoding="utf-8")


def write_all_portal_forms(task_dir: Path, *, sync_submission: bool = False) -> tuple[Path, Path | None]:
    s1 = write_portal_form(task_dir, sync_submission=sync_submission)
    s2: Path | None = None
    try:
        s2 = write_portal_section2(task_dir, sync_submission=sync_submission)
    except SystemExit:
        pass
    return s1, s2


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate portal submission form answers")
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--section2", action="store_true", help="Generate Section 2 only (portal-section2.md)")
    parser.add_argument("--all", action="store_true", help="Generate Section 1 and Section 2")
    parser.add_argument("--sync-submission", action="store_true")
    parser.add_argument("--print", action="store_true", help="Print to stdout")
    args = parser.parse_args()

    task_dir = args.task_dir if args.task_dir.is_absolute() else REPO_ROOT / args.task_dir
    if args.section2:
        out = write_portal_section2(task_dir, sync_submission=args.sync_submission)
    elif args.all:
        out, out2 = write_all_portal_forms(task_dir, sync_submission=args.sync_submission)
        print(f"Wrote {out}")
        if out2:
            print(f"Wrote {out2}")
        if args.print and out2:
            print()
            print(out2.read_text(encoding="utf-8"))
        return
    else:
        out = write_portal_form(task_dir, sync_submission=args.sync_submission)

    print(f"Wrote {out}")
    if args.print:
        print()
        print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
