#!/usr/bin/env python3
"""Seed and task uniqueness checks for batch diversity."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from common import REPO_ROOT, CheckResult, load_jsonl, print_results


def load_registry() -> list[dict]:
    seeds = load_jsonl(REPO_ROOT / "registry" / "seeds.jsonl")
    tasks = load_jsonl(REPO_ROOT / "registry" / "task-registry.jsonl")
    return seeds + tasks


def check_uniqueness(
    seed_id: str | None = None,
    topology: str | None = None,
    scaffold: str | None = None,
    file_mix: str | None = None,
    opener_pattern: str | None = None,
    input_filenames: list[str] | None = None,
    task_dir: Path | None = None,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    registry = load_registry()
    r = CheckResult("seed-uniqueness")

    if task_dir:
        meta_path = task_dir / "metadata.yaml"
        if meta_path.exists():
            import yaml

            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            seed_id = seed_id or meta.get("slug")
            input_filenames = input_filenames or meta.get("input_files", [])

    for entry in registry:
        eid = entry.get("seed_id") or entry.get("slug")

        # Allow self when validating an existing task directory
        if task_dir and eid == task_dir.name:
            continue

        if seed_id and eid == seed_id:
            r.error(f"Duplicate seed_id/slug already registered: {seed_id}")

        if topology and entry.get("topology", "").lower() == topology.lower():
            r.warn(f"Topology collision with {eid}: {topology}")

        if scaffold and entry.get("scaffold") == scaffold and seed_id != eid:
            r.warn(f"Same scaffold '{scaffold}' as {eid} — verify strip test")

        if opener_pattern and entry.get("opener_pattern") == opener_pattern:
            same_scaffold = scaffold and entry.get("scaffold") == scaffold
            if same_scaffold:
                r.error(f"Opener + scaffold combo duplicates {eid}")

        if file_mix and entry.get("file_mix") == file_mix.split(",") if isinstance(file_mix, str) else file_mix:
            if scaffold and entry.get("scaffold") == scaffold:
                r.warn(f"Identical file mix + scaffold as {eid}")

        if input_filenames:
            existing = set(entry.get("input_filenames", []))
            overlap = existing.intersection(set(input_filenames))
            if overlap and seed_id != eid:
                r.error(f"Shared input filenames with {eid}: {sorted(overlap)}")

    results.append(r)
    return results


def register_seed(args: argparse.Namespace) -> None:
    # Skeleton gate first — hard-fail reused decision structures (Pelliston Uniqueness)
    if args.scaffold:
        from skeleton_gate import check_scaffold

        sk_results = check_scaffold(
            args.scaffold,
            seed_id=args.seed_id,
            allow_reuse=bool(getattr(args, "allow_skeleton_reuse", False)),
        )
        if print_results(sk_results, strict=True) != 0:
            raise SystemExit(1)

    results = check_uniqueness(
        seed_id=args.seed_id,
        topology=args.topology,
        scaffold=args.scaffold,
        file_mix=args.file_mix,
        opener_pattern=args.opener_pattern,
        input_filenames=args.input_filenames.split(",") if args.input_filenames else None,
    )
    if print_results(results, strict=True) != 0:
        raise SystemExit(1)

    entry = {
        "seed_id": args.seed_id,
        "slug": args.seed_id,
        "topology": args.topology or "",
        "scaffold": args.scaffold or "",
        "file_mix": args.file_mix.split(",") if args.file_mix else [],
        "opener_pattern": args.opener_pattern or "",
        "input_filenames": args.input_filenames.split(",") if args.input_filenames else [],
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "status": "seed",
    }
    path = REPO_ROOT / "registry" / "seeds.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Registered seed: {args.seed_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("--seed-id")
    check.add_argument("--topology")
    check.add_argument("--scaffold")
    check.add_argument("--file-mix")
    check.add_argument("--opener-pattern")
    check.add_argument("--input-filenames")
    check.add_argument("--task-dir", type=Path)
    check.add_argument("--strict", action="store_true")
    check.add_argument("--allow-skeleton-reuse", action="store_true")

    reg = sub.add_parser("register")
    reg.add_argument("--seed-id", required=True)
    reg.add_argument("--topology")
    reg.add_argument("--scaffold")
    reg.add_argument("--file-mix")
    reg.add_argument("--opener-pattern")
    reg.add_argument("--input-filenames")
    reg.add_argument(
        "--allow-skeleton-reuse",
        action="store_true",
        help="Allow registering a scaffold whose decision skeleton is already used (not recommended)",
    )

    args = parser.parse_args()

    if args.command == "register":
        register_seed(args)
        return

    task_dir = args.task_dir
    if task_dir and not task_dir.is_absolute():
        task_dir = REPO_ROOT / task_dir

    filenames = args.input_filenames.split(",") if args.input_filenames else None
    results = check_uniqueness(
        seed_id=args.seed_id,
        topology=args.topology,
        scaffold=args.scaffold,
        file_mix=args.file_mix,
        opener_pattern=args.opener_pattern,
        input_filenames=filenames,
        task_dir=task_dir,
    )
    if args.scaffold:
        from skeleton_gate import check_scaffold

        results.extend(
            check_scaffold(
                args.scaffold,
                seed_id=args.seed_id or (task_dir.name if task_dir else None),
                allow_reuse=bool(getattr(args, "allow_skeleton_reuse", False)),
            )
        )
    raise SystemExit(print_results(results, strict=args.strict))


if __name__ == "__main__":
    main()