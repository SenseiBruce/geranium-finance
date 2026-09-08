#!/usr/bin/env python3
"""Fetch O*NET task/skill dropdown strings for a Finance & Insurance occupation code."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

from common import REPO_ROOT

CACHE_DIR = REPO_ROOT / "registry" / "onet-cache"
TASK_CHOOSE_URL = "https://www.onetonline.org/search/task/choose/{code}"
DETAILS_URL = "https://www.onetonline.org/link/details/{code}"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "geranium-finance-onet-lookup/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_tasks(html: str) -> list[str]:
    tasks: list[str] = []
    if "Job Duties Custom List" in html:
        block = html.split("Job Duties Custom List", 1)[-1]
        block = block.split("Go Please select", 1)[0]
        for line in block.split("\n"):
            line = line.strip()
            if line.endswith(".") and len(line) > 40 and "http" not in line:
                if not line.startswith(("Review the", "Occupation", "Type a")):
                    tasks.append(line)
    return tasks


def parse_essential_skills(html: str) -> list[str]:
    skills: list[str] = []
    in_section = False
    for line in html.split("\n"):
        if "Essential Skills" in line:
            in_section = True
            continue
        if in_section and line.startswith("## ") and "Essential Skills" not in line:
            break
        m = re.search(r"\|\s*\d+\s*\|\s*([^|]+?)\s*—", line)
        if m:
            skills.append(m.group(1).strip())
    return skills


def lookup(code: str, *, refresh: bool = False) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{code}.json"
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    task_html = fetch(TASK_CHOOSE_URL.format(code=code))
    detail_html = fetch(DETAILS_URL.format(code=code))
    tasks = parse_tasks(task_html)
    skills = parse_essential_skills(detail_html)
    data = {
        "code": code,
        "tasks": tasks,
        "essential_skills": skills,
        "task_choose_url": TASK_CHOOSE_URL.format(code=code),
        "details_url": DETAILS_URL.format(code=code),
    }
    if tasks:
        cache_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    elif cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    return data


def portal_suggestions(data: dict) -> dict:
    if "suggested_portal" in data:
        return data["suggested_portal"]
    return {
        "tasks": data.get("tasks", [])[:3],
        "skills": data.get("essential_skills", [])[:3],
    }


def validate_metadata(onet_meta: dict) -> list[str]:
    """Return errors if metadata tasks/skills are not exact dropdown strings."""
    code = onet_meta.get("code", "")
    if not code:
        return ["metadata.yaml missing onet.code"]
    data = lookup(code)
    errors: list[str] = []
    valid_tasks = set(data.get("tasks", []))
    valid_skills = set(data.get("essential_skills", []))
    for t in onet_meta.get("tasks", []):
        if t not in valid_tasks:
            errors.append(f"O*NET task not in portal dropdown: {t[:80]}...")
    for s in onet_meta.get("skills", []):
        if s not in valid_skills:
            errors.append(f"O*NET skill not in Essential Skills dropdown: {s}")
    return errors


def format_portal_block(data: dict, *, meta_tasks: list[str] | None = None, meta_skills: list[str] | None = None) -> str:
    """Markdown block for pre-submit report / step 7 copy-paste."""
    occ = data.get("occupation", "")
    code = data.get("code", "")
    lines = [
        f"## Portal O*NET ({code} {occ})".strip(),
        "",
        "Select occupation **first**, then pick tasks/skills from these exact strings:",
        "",
        "### Tasks (all available in dropdown)",
    ]
    for i, t in enumerate(data.get("tasks", []), 1):
        mark = " ← use" if meta_tasks and t in meta_tasks else ""
        lines.append(f"{i}. {t}{mark}")
    lines += ["", "### Essential Skills (dropdown)"]
    for i, s in enumerate(data.get("essential_skills", []), 1):
        mark = " ← use" if meta_skills and s in meta_skills else ""
        lines.append(f"{i}. {s}{mark}")
    lines += [
        "",
        f"Source: {data.get('task_choose_url', '')}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="O*NET dropdown strings for portal forms")
    parser.add_argument("code", help="O*NET-SOC code, e.g. 13-2053.00")
    parser.add_argument("--refresh", action="store_true", help="Re-fetch from onetonline.org")
    parser.add_argument("--suggest", action="store_true", help="Print suggested portal selections")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    args = parser.parse_args()

    data = lookup(args.code, refresh=args.refresh)
    if args.json:
        print(json.dumps(data, indent=2))
        return

    occ = data.get("occupation", "")
    print(f"O*NET {args.code} {occ}".strip())
    print(f"Source: {data.get('task_choose_url', '')}\n")
    print("TASKS (exact portal dropdown text):")
    for i, t in enumerate(data.get("tasks", []), 1):
        print(f"  {i}. {t}")
    print("\nESSENTIAL SKILLS (portal dropdown):")
    for i, s in enumerate(data.get("essential_skills", []), 1):
        print(f"  {i}. {s}")

    if args.suggest:
        sug = portal_suggestions(data)
        print("\n>>> SUGGESTED FOR PORTAL:")
        for t in sug.get("tasks", []):
            print(f"TASK: {t}")
        for s in sug.get("skills", []):
            print(f"SKILL: {s}")


if __name__ == "__main__":
    main()
