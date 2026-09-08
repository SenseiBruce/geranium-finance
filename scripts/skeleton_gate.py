#!/usr/bin/env python3
"""Skeleton (decision-structure) uniqueness gate for Geranium batch diversity.

Portal Uniqueness fails when two tasks share the same strip-test skeleton
even if scaffolds/filenames differ (Pelliston premium-audit true-up vs Meridian CAM).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import REPO_ROOT, CheckResult, load_jsonl, print_results

CATALOG_PATH = REPO_ROOT / "registry" / "skeletons.json"


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        return {"skeletons": {}, "available_for_new_tasks": []}
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def skeleton_for_scaffold(scaffold: str, catalog: dict | None = None) -> tuple[str | None, dict | None]:
    catalog = catalog or load_catalog()
    for sk_id, meta in (catalog.get("skeletons") or {}).items():
        if scaffold in (meta.get("scaffolds") or []):
            return sk_id, meta
    return None, None


def scaffolds_in_use() -> dict[str, list[str]]:
    """scaffold -> list of seed_ids using it."""
    used: dict[str, list[str]] = {}
    for entry in load_jsonl(REPO_ROOT / "registry" / "seeds.jsonl"):
        sc = entry.get("scaffold") or ""
        sid = entry.get("seed_id") or entry.get("slug") or "?"
        if sc:
            used.setdefault(sc, []).append(sid)
    return used


def skeletons_in_use(catalog: dict | None = None) -> dict[str, list[str]]:
    """skeleton_id -> list of seed_ids."""
    catalog = catalog or load_catalog()
    sc_used = scaffolds_in_use()
    out: dict[str, list[str]] = {}
    for sk_id, meta in (catalog.get("skeletons") or {}).items():
        seeds: list[str] = []
        for sc in meta.get("scaffolds") or []:
            seeds.extend(sc_used.get(sc, []))
        if seeds:
            out[sk_id] = sorted(set(seeds))
    return out


def check_scaffold(
    scaffold: str,
    *,
    seed_id: str | None = None,
    allow_reuse: bool = False,
) -> list[CheckResult]:
    r = CheckResult("skeleton-gate")
    catalog = load_catalog()
    sk_id, meta = skeleton_for_scaffold(scaffold, catalog)

    if not sk_id:
        r.error(
            f"Scaffold '{scaffold}' is not mapped in registry/skeletons.json. "
            f"Add it under an existing skeleton or create a new skeleton id BEFORE registering. "
            f"Strip-test: if decision_shape matches an existing skeleton, reuse that id (and expect a hard fail if already used)."
        )
        return [r]

    in_use = skeletons_in_use(catalog)
    all_holders = in_use.get(sk_id, [])
    holders = [s for s in all_holders if s != seed_id]
    blocked = meta.get("blocked_reason")

    if blocked and holders:
        r.error(
            f"Skeleton '{sk_id}' is CLOSED for new tasks ({blocked}). "
            f"Already used by: {holders}. Pick a different decision structure."
        )
    elif blocked and not holders and not (seed_id and seed_id in all_holders):
        r.error(
            f"Skeleton '{sk_id}' is CLOSED for new tasks ({blocked}). "
            f"Pick a different decision structure."
        )
    elif holders and not allow_reuse:
        r.error(
            f"Skeleton '{sk_id}' ({meta.get('label')}) already used by {holders}. "
            f"Decision shape: {meta.get('decision_shape')}. "
            f"Portal Uniqueness will likely FAIL. Use a free skeleton or pass --allow-reuse only for intentional twins."
        )
    elif holders and allow_reuse:
        r.warn(f"Skeleton '{sk_id}' reused with --allow-reuse (holders: {holders})")
    elif seed_id and seed_id in all_holders:
        pass  # existing task re-check — OK
    else:
        r.warn(f"Skeleton '{sk_id}' free — {meta.get('label')}")

    return [r]


def pick_free_skeleton(catalog: dict | None = None) -> str | None:
    catalog = catalog or load_catalog()
    preferred = catalog.get("available_for_new_tasks") or []
    in_use = skeletons_in_use(catalog)
    for sk in preferred:
        if sk not in in_use:
            return sk
    for sk_id, meta in (catalog.get("skeletons") or {}).items():
        if sk_id in in_use:
            continue
        if meta.get("blocked_reason") and sk_id in in_use:
            continue
        if meta.get("blocked_reason"):
            # closed even if somehow empty
            continue
        return sk_id
    # Prefer least-used non-closed
    candidates = [
        (len(in_use.get(sk, [])), sk)
        for sk, meta in (catalog.get("skeletons") or {}).items()
        if not meta.get("blocked_reason")
    ]
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def status_report() -> str:
    catalog = load_catalog()
    in_use = skeletons_in_use(catalog)
    lines = ["Skeleton catalog status:", ""]
    for sk_id, meta in (catalog.get("skeletons") or {}).items():
        holders = in_use.get(sk_id, [])
        flag = "CLOSED" if meta.get("blocked_reason") else ("IN USE" if holders else "FREE")
        lines.append(f"  [{flag}] {sk_id}")
        lines.append(f"           {meta.get('label')}")
        if holders:
            lines.append(f"           used by: {', '.join(holders)}")
        if meta.get("blocked_reason"):
            lines.append(f"           note: {meta['blocked_reason']}")
        lines.append("")
    free = pick_free_skeleton(catalog)
    lines.append(f"Suggested for /new: {free or '(none free — add a new skeleton)'}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Check a scaffold against the skeleton catalog")
    p_check.add_argument("--scaffold", required=True)
    p_check.add_argument("--seed-id")
    p_check.add_argument("--allow-reuse", action="store_true")
    p_check.add_argument("--strict", action="store_true")

    sub.add_parser("status", help="Print skeleton usage across the batch")

    p_pick = sub.add_parser("pick", help="Print a free skeleton id for /new")
    p_pick.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "status":
        print(status_report())
        return
    if args.command == "pick":
        catalog = load_catalog()
        sk = pick_free_skeleton(catalog)
        if args.json:
            meta = (catalog.get("skeletons") or {}).get(sk or "", {})
            print(json.dumps({"skeleton": sk, "meta": meta}, indent=2))
        else:
            print(sk or "")
        raise SystemExit(0 if sk else 1)
    results = check_scaffold(args.scaffold, seed_id=args.seed_id, allow_reuse=args.allow_reuse)
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()
