#!/usr/bin/env python3
"""
Geranium Finance chat orchestrator.

Run everything from Cursor chat via one entry point:

  .venv/bin/python scripts/gf.py status
  .venv/bin/python scripts/gf.py seed register --seed-id my-task ...
  .venv/bin/python scripts/gf.py init my-task
  .venv/bin/python scripts/gf.py gate 2a my-task
  .venv/bin/python scripts/gf.py next my-task
  .venv/bin/python scripts/gf.py validate my-task --strict --package
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PYTHON = REPO / ".venv" / "bin" / "python"
if not PYTHON.exists():
    PYTHON = Path(sys.executable)

STEP_MARKERS = {
    "2b": ".step2b-complete",
    "3": ".step3-complete",
    "4": ".step4-complete",
    "5": ".step5-complete",
    "6": ".step6-complete",
    "7a": ".step7a-complete",
    "7b": ".step7b-complete",
}

STEP_PROMPTS = {
    "1": "prompts/step1-ideation.md",
    "2a": "prompts/step2a-task-spec.md",
    "2b": "prompts/step2b-input-files.md",
    "3": "prompts/step3-prompt.md",
    "4": "prompts/step4-golden-solution.md",
    "5": "prompts/step5-rubric.md",
    "6": "prompts/step6-quality-gates.md",
    "7a": "prompts/step7a-portal-form.md",
    "7b": "prompts/step7b-portal-section2.md",
    "7": "prompts/step7-submit.md",
}

ARCHETYPES = {
    "consolidation": {
        "occupation": "Treasurers and Controllers",
        "onet_code": "11-3031.01",
        "scaffold": "multi_entity_consolidation_with_fx_and_acquisition",
        "skeleton": "fx_acquisition_consolidation",
        "file_mix": "csv,txt,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "consolidated_review_{entity}.xlsx",
        "input_pattern": [
            "{entity}_brand_ledger.csv",
            "{entity_short}_acquisition_memo.txt",
            "{entity_short}_fx_and_period_reference.txt",
        ],
        "topology_hint": "Q1 board close with FX label and mid-period acquisition",
    },
    "renewal_desk": {
        "occupation": "Insurance Underwriters",
        "onet_code": "13-2053.00",
        "scaffold": "renewal_desk_multi_file_routing",
        "skeleton": "renewal_path_routing",
        "file_mix": "csv,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "renewal_underwriting_review.xlsx",
        "input_pattern": [
            "renewal_account_list.csv",
            "policy_location_schedule.csv",
            "underwriting_rules_notes.txt",
        ],
        "topology_hint": "Renewal desk with account vs location-loss path conflicts",
    },
    "valuation": {
        "occupation": "Financial Analysts",
        "onet_code": "13-2051.00",
        "scaffold": "live_formula_valuation_model",
        "skeleton": "live_formula_valuation",
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "valuation_draft.xlsx",
        "input_pattern": [
            "cohort_summary.xlsx",
            "cap_table.csv",
            "investor_brief.txt",
        ],
        "topology_hint": "Series B prep with cohort assumptions and cap table",
    },
    # CLOSED skeleton (trueup_reconcile) — kept for reference; gf new will refuse
    "reconciliation": {
        "occupation": "Treasurers and Controllers",
        "onet_code": "11-3031.01",
        "scaffold": "cam_annual_trueup_reconciliation",
        "skeleton": "trueup_reconcile",
        "blocked": True,
        "file_mix": "csv,xlsx,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "cam_trueup_{entity}.xlsx",
        "input_pattern": [
            "expense_ledger.csv",
            "tenant_lease_abstracts.xlsx",
            "prior_cam_billing_register.txt",
        ],
        "topology_hint": "Year-end CAM true-up with lease caps, vacancy absorption, and mid-year share change",
    },
    "covenant_pack": {
        "occupation": "Credit Analysts",
        "onet_code": "13-2041.00",
        "scaffold": "covenant_headroom_credit_pack",
        "skeleton": "covenant_headroom_pack",
        "blocked": True,
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "covenant_headroom_{entity}.xlsx",
        "input_pattern": [
            "{entity}_debt_schedule.xlsx",
            "{entity}_ebitda_bridge.csv",
            "credit_agreement_covenant_excerpts.txt",
        ],
        "topology_hint": "Quarter-end covenant headroom with EBITDA add-backs and basket exceptions",
    },
    "intercompany": {
        "occupation": "Treasurers and Controllers",
        "onet_code": "11-3031.01",
        "scaffold": "intercompany_fx_cutoff_settlement",
        "skeleton": "intercompany_settlement",
        "file_mix": "csv,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "intercompany_settlement_{entity}.xlsx",
        "input_pattern": [
            "{entity}_ar_subledger.csv",
            "{entity}_ap_mirror.csv",
            "intercompany_cutoff_and_fx_memo.txt",
        ],
        "topology_hint": "Month-end intercompany settlement with FX and cut-off disputes",
    },
    "claims_triangle": {
        "occupation": "Insurance Underwriters",
        "onet_code": "13-2053.00",
        "scaffold": "claims_triangle_case_ibnr_opinion",
        "skeleton": "claims_reserve_triangle",
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "claims_reserve_opinion_{entity}.xlsx",
        "input_pattern": [
            "{entity}_loss_triangle.xlsx",
            "{entity}_open_claims.csv",
            "actuarial_factor_memo.txt",
        ],
        "topology_hint": "Year-end claims triangle with case vs IBNR (insured program, not SI retention)",
    },
    "claims_coverage": {
        "occupation": "Claims Adjusters, Examiners, and Investigators",
        "onet_code": "13-1031.00",
        "scaffold": "single_claim_coverage_reserve_opinion",
        "skeleton": "claims_coverage_determination",
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "claim_coverage_opinion_{entity}.xlsx",
        "input_pattern": [
            "{entity}_claim_file.xlsx",
            "{entity}_policy_schedule.csv",
            "coverage_investigation_memo.txt",
        ],
        "topology_hint": "Single large commercial claim: coverage vs exclusion fight plus case reserve recommendation",
    },
    "loan_underwriting": {
        "occupation": "Loan Officers",
        "onet_code": "13-2072.00",
        "scaffold": "commercial_loan_credit_decision_pack",
        "skeleton": "commercial_loan_underwriting",
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "loan_underwriting_decision_{entity}.xlsx",
        "input_pattern": [
            "{entity}_borrower_financials.xlsx",
            "{entity}_collateral_schedule.csv",
            "credit_policy_and_exception_memo.txt",
        ],
        "topology_hint": "Commercial equipment term loan: DSCR/LTV conflicts vs credit policy with collateral exception path",
    },
    "gl_flux_close": {
        "occupation": "Treasurers and Controllers",
        "onet_code": "11-3031.01",
        "scaffold": "month_end_gl_flux_aje_close_pack",
        "skeleton": "gl_flux_close_pack",
        "file_mix": "xlsx,csv,txt",
        "deliverable_type": "xlsx",
        "deliverable_pattern": "flux_close_pack_{entity}.xlsx",
        "input_pattern": [
            "{entity}_trial_balance.xlsx",
            "{entity}_support_schedules.csv",
            "flux_threshold_and_aje_memo.txt",
        ],
        "topology_hint": "Month-end GL flux close: material variance thresholds + support schedule conflicts → AJE pack and close readiness",
    },
}


def run_script(script: str, args: list[str], *, check: bool = True) -> int:
    cmd = [str(PYTHON), str(REPO / "scripts" / script)] + args
    print(f"$ {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, cwd=REPO)
    if check and proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc.returncode


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "new-task"


def task_dir(slug: str) -> Path:
    return REPO / "tasks" / slug


def cmd_status(args: argparse.Namespace) -> None:
    if args.slug:
        td = task_dir(args.slug)
        if not td.exists():
            print(f"Task not found: {args.slug}")
            raise SystemExit(1)
        print(f"Task: {args.slug}")
        for step, marker in STEP_MARKERS.items():
            done = (td / marker).exists()
            print(f"  Step {step}: {'DONE' if done else 'pending'}")
        for name in ["task-spec.md", "metadata.yaml", "prompt.txt", "inputs.zip", "golden.zip", "rubric.json"]:
            p = td / name
            print(f"  {name}: {'yes' if p.exists() else 'no'}")
        nxt = infer_next_step(td)
        print(f"\nNext step: {nxt}")
        print(f"Prompt file: {STEP_PROMPTS.get(nxt, 'n/a')}")
        return

    seeds = load_jsonl(REPO / "registry" / "seeds.jsonl")
    tasks = load_jsonl(REPO / "registry" / "task-registry.jsonl")
    task_dirs = sorted(p.name for p in (REPO / "tasks").glob("*") if p.is_dir())

    print("Seeds:")
    for s in seeds:
        print(f"  - {s.get('seed_id')} ({s.get('scaffold')})")

    print("\nRegistered tasks:")
    for t in tasks:
        print(f"  - {t.get('slug')} [{t.get('status')}]")

    print("\nTask folders:")
    for slug in task_dirs:
        td = task_dir(slug)
        nxt = infer_next_step(td)
        print(f"  - {slug} → next: {nxt}")


def infer_next_step(td: Path) -> str:
    if not (td / "task-spec.md").exists():
        return "2a"
    if not (td / ".step2b-complete").exists():
        return "2b"
    if not (td / ".step3-complete").exists():
        return "3"
    if not (td / ".step4-complete").exists():
        return "4"
    if not (td / ".step5-complete").exists():
        return "5"
    if not (td / ".step6-complete").exists():
        return "6"
    if not (td / ".step7a-complete").exists():
        return "7a"
    if not (td / ".step7b-complete").exists():
        return "7b"
    return "7"


def cmd_next(args: argparse.Namespace) -> None:
    td = task_dir(args.slug)
    step = infer_next_step(td)
    prompt = REPO / STEP_PROMPTS.get(step, "")
    print(f"slug: {args.slug}")
    print(f"next_step: {step}")
    print(f"prompt: {prompt.relative_to(REPO) if prompt.exists() else 'n/a'}")
    print(f"gate: gf gate {step} {args.slug}")


def cmd_init(args: argparse.Namespace) -> None:
    slug = args.slug
    td = task_dir(slug)
    if td.exists() and not args.force:
        print(f"Task folder already exists: {td}")
        print("Use --force to re-init templates.")
        raise SystemExit(1)

    td.mkdir(parents=True, exist_ok=True)
    (td / "inputs").mkdir(exist_ok=True)
    (td / "golden").mkdir(exist_ok=True)

    spec_tpl = REPO / "templates" / "task-spec.md"
    meta_tpl = REPO / "templates" / "metadata.yaml"
    if spec_tpl.exists() and not (td / "task-spec.md").exists():
        text = spec_tpl.read_text(encoding="utf-8").replace("<slug>", slug)
        (td / "task-spec.md").write_text(text, encoding="utf-8")
    if meta_tpl.exists() and not (td / "metadata.yaml").exists():
        text = meta_tpl.read_text(encoding="utf-8").replace('slug: ""', f'slug: {slug}').replace(
            'seed_id: ""', f'seed_id: {slug}'
        )
        (td / "metadata.yaml").write_text(text, encoding="utf-8")

    print(f"Initialized {td}")
    print(f"Next: gf gate 2a {slug}  (after filling task-spec.md)")


def cmd_seed_register(args: argparse.Namespace) -> None:
    reg_args = ["register", "--seed-id", args.seed_id]
    if args.topology:
        reg_args += ["--topology", args.topology]
    if args.scaffold:
        reg_args += ["--scaffold", args.scaffold]
    if args.file_mix:
        reg_args += ["--file-mix", args.file_mix]
    if args.opener_pattern:
        reg_args += ["--opener-pattern", args.opener_pattern]
    if args.input_filenames:
        reg_args += ["--input-filenames", args.input_filenames]
    if getattr(args, "allow_skeleton_reuse", False):
        reg_args += ["--allow-skeleton-reuse"]
    run_script("seed_uniqueness_check.py", reg_args)
    print(f"Seed registered: {args.seed_id}")
    print(f"Next: gf init {args.seed_id}")


def cmd_seed_check(args: argparse.Namespace) -> None:
    check_args = ["check", "--seed-id", args.seed_id]
    if args.topology:
        check_args += ["--topology", args.topology]
    if args.scaffold:
        check_args += ["--scaffold", args.scaffold]
    if args.file_mix:
        check_args += ["--file-mix", args.file_mix]
    if args.opener_pattern:
        check_args += ["--opener-pattern", args.opener_pattern]
    if args.task_dir:
        check_args += ["--task-dir", args.task_dir]
    if getattr(args, "allow_skeleton_reuse", False):
        check_args += ["--allow-skeleton-reuse"]
    run_script("seed_uniqueness_check.py", check_args + (["--strict"] if args.strict else []))


def cmd_seed_suggest(args: argparse.Namespace) -> None:
    arch = ARCHETYPES.get(args.archetype)
    if not arch:
        print(f"Unknown archetype: {args.archetype}")
        print(f"Available: {', '.join(ARCHETYPES)}")
        raise SystemExit(1)

    if arch.get("blocked") and not getattr(args, "allow_skeleton_reuse", False):
        print(
            f"Archetype '{args.archetype}' maps to CLOSED skeleton '{arch.get('skeleton')}' "
            f"(scaffold {arch['scaffold']}). Pick covenant_pack / intercompany / claims_triangle, "
            f"or run: gf skeleton status"
        )
        raise SystemExit(1)

    entity = slugify(args.entity or "acme-media-group")
    entity_short = entity.split("-")[0] if "-" in entity else entity

    deliverable = arch["deliverable_pattern"].format(
        entity=entity, entity_short=entity_short, slug_entity=entity
    )
    inputs = [
        p.format(entity=entity, entity_short=entity_short, slug_entity=entity)
        for p in arch["input_pattern"]
    ]
    seed_id = args.seed_id or slugify(f"{entity}-{args.archetype}")

    seed = {
        "seed_id": seed_id,
        "slug": seed_id,
        "occupation": arch["occupation"],
        "onet_code": arch["onet_code"],
        "opener_pattern": "situation_first",
        "file_mix": arch["file_mix"].split(","),
        "deliverable_type": arch["deliverable_type"],
        "deliverable_name": deliverable,
        "scaffold": arch["scaffold"],
        "skeleton": arch.get("skeleton"),
        "topology": args.topology or arch["topology_hint"],
        "input_filenames": inputs,
        "time_estimate_hours": 5,
        "status": "seed",
    }
    print(json.dumps(seed, indent=2))
    print("\nRegister with:")
    print(
        f"  gf seed register --seed-id {seed_id} "
        f'--topology "{seed["topology"]}" '
        f"--scaffold {arch['scaffold']} "
        f'--file-mix {arch["file_mix"]} '
        f"--opener-pattern situation_first "
        f'--input-filenames {",".join(inputs)}'
    )
    if args.register:
        # Ensure scaffold is listed under its skeleton before register
        _ensure_scaffold_in_catalog(arch["scaffold"], arch.get("skeleton"))
        cmd_seed_register(
            argparse.Namespace(
                seed_id=seed_id,
                topology=seed["topology"],
                scaffold=arch["scaffold"],
                file_mix=arch["file_mix"],
                opener_pattern="situation_first",
                input_filenames=",".join(inputs),
                allow_skeleton_reuse=bool(getattr(args, "allow_skeleton_reuse", False)),
            )
        )
        if args.init:
            cmd_init(argparse.Namespace(slug=seed_id, force=False))


def _ensure_scaffold_in_catalog(scaffold: str, skeleton: str | None) -> None:
    if not skeleton:
        return
    path = REPO / "registry" / "skeletons.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    meta = (catalog.get("skeletons") or {}).get(skeleton)
    if not meta:
        return
    scaffolds = meta.setdefault("scaffolds", [])
    if scaffold not in scaffolds:
        scaffolds.append(scaffold)
        path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
        print(f"Added scaffold '{scaffold}' under skeleton '{skeleton}' in registry/skeletons.json")


def _pick_auto_archetype() -> str:
    """Prefer archetypes whose skeleton is FREE in the catalog."""
    sys.path.insert(0, str(REPO / "scripts"))
    from skeleton_gate import load_catalog, skeletons_in_use

    catalog = load_catalog()
    in_use = skeletons_in_use(catalog)
    preferred = [
        "gl_flux_close",
        "loan_underwriting",
        "claims_coverage",
        "covenant_pack",
        "intercompany",
        "claims_triangle",
    ]
    for name in preferred:
        arch = ARCHETYPES[name]
        sk = arch.get("skeleton")
        if sk and sk not in in_use and not arch.get("blocked"):
            return name
    for name, arch in ARCHETYPES.items():
        if arch.get("blocked"):
            continue
        sk = arch.get("skeleton")
        if sk and sk not in in_use:
            return name
    # Fall back to least-used non-blocked
    scored = []
    for name, arch in ARCHETYPES.items():
        if arch.get("blocked"):
            continue
        sk = arch.get("skeleton")
        scored.append((len(in_use.get(sk or "", [])), name))
    scored.sort()
    return scored[0][1] if scored else "covenant_pack"

def cmd_gate(args: argparse.Namespace) -> None:
    slug = args.slug
    td = task_dir(slug)
    step = args.step.lower()

    if step == "2a":
        run_script("lint_task_spec.py", [str(td / "task-spec.md"), "--strict"])
        run_script("spec_satisfiability.py", [str(td / "task-spec.md")])
        print("Step 2a gates passed. Fill task-spec.md then run: gf init if needed, gf gate 2b")
        return

    if step == "2b":
        run_script("file_depth_check.py", [str(td / "inputs/")])
        run_script("package_zips.py", [str(td), "--inputs"])
        run_script(
            "validate_input_zip.py",
            [str(td / "inputs.zip"), "--task-dir", str(td), "--strict"],
        )
        (td / ".step2b-complete").touch()
        print("Step 2b complete.")
        return

    if step == "3":
        run_script("lint_prompt.py", [str(td / "prompt.txt"), "--task-dir", str(td), "--strict"])
        run_script(
            "validate_input_zip.py",
            [str(td / "inputs.zip"), "--task-dir", str(td), "--prompt", str(td / "prompt.txt"), "--strict"],
        )
        (td / ".step3-complete").touch()
        print("Step 3 complete.")
        return

    if step == "4":
        run_script("package_zips.py", [str(td), "--golden"])
        run_script(
            "validate_golden_zip.py",
            [str(td / "golden.zip"), "--task-dir", str(td), "--strict"],
        )
        run_script("open_check.py", [str(td / "golden/")])
        run_script("package_consistency_check.py", [str(td), "--strict"])
        (td / ".step4-complete").touch()
        print("Step 4 complete.")
        return

    if step == "5":
        run_script("lint_rubric.py", [str(td / "rubric.json"), "--strict"])
        run_script("package_consistency_check.py", [str(td), "--strict"])
        run_script("golden_vs_rubric.py", [str(td)])
        print("Complete golden-rubric-evidence.md checkmarks, then: gf gate 5 --confirm-audit")
        if args.confirm_audit:
            run_script("golden_vs_rubric.py", [str(td), "--strict"])
            (td / ".step5-complete").touch()
            print("Step 5 complete.")
        return

    if step == "6":
        run_script("seed_uniqueness_check.py", ["check", "--task-dir", str(td), "--strict"])
        val_args = [str(td), "--strict"]
        if args.package:
            val_args.append("--package")
        run_script("task_readiness.py", val_args)
        (td / ".step6-complete").touch()
        run_script("portal_form.py", [str(td), "--all", "--sync-submission"])
        (td / ".step7a-complete").touch()
        (td / ".step7b-complete").touch()
        print("Step 6 complete. Portal forms written (Section 1 + Section 2).")
        print("Next: upload using portal-submission.md then portal-section2.md (Step 7).")
        return

    if step == "7a":
        run_script("portal_form.py", [str(td), "--sync-submission"])
        (td / ".step7a-complete").touch()
        print("Step 7a complete. Open portal-submission.md for Section 1 copy-paste.")
        return

    if step == "7b":
        run_script("portal_form.py", [str(td), "--section2", "--sync-submission"])
        (td / ".step7b-complete").touch()
        print("Step 7b complete. Open portal-section2.md for golden upload + rubric criteria.")
        return

    print(f"Unknown step: {step}")
    raise SystemExit(1)


def cmd_validate(args: argparse.Namespace) -> None:
    val_args = [str(task_dir(args.slug))]
    if args.strict:
        val_args.append("--strict")
    if args.package:
        val_args.append("--package")
    run_script("task_readiness.py", val_args)


def cmd_portal2(args: argparse.Namespace) -> None:
    """Generate portal-section2.md with golden upload + rubric copy-paste fields."""
    td = task_dir(args.slug)
    if not td.is_dir():
        print(f"Task not found: {args.slug}")
        raise SystemExit(1)
    run_script("portal_form.py", [str(td), "--section2", "--sync-submission"])
    (td / ".step7b-complete").touch()
    out = td / "portal-section2.md"
    print(f"\nSection 2 form: {out}")
    print(f"Submission copy: {td / 'submission' / 'portal-section2.md'}")


def cmd_portal(args: argparse.Namespace) -> None:
    """Generate portal-submission.md with Snorkel form copy-paste answers."""
    td = task_dir(args.slug)
    if not td.is_dir():
        print(f"Task not found: {args.slug}")
        raise SystemExit(1)
    run_script("portal_form.py", [str(td), "--sync-submission"])
    (td / ".step7a-complete").touch()
    out = td / "portal-submission.md"
    print(f"\nPortal form: {out}")
    print(f"Submission copy: {td / 'submission' / 'portal-submission.md'}")


def cmd_repackage(args: argparse.Namespace) -> None:
    """Rebuild both zips from source folders, archive superseded copies, sync submission/."""
    td = task_dir(args.slug)
    if not td.is_dir():
        print(f"Task not found: {args.slug}")
        raise SystemExit(1)
    run_script(
        "package_zips.py",
        [str(td), "--all", "--sync-submission"],
    )
    if (td / "prompt.txt").exists() and (td / "metadata.yaml").exists():
        run_script("portal_form.py", [str(td), "--all", "--sync-submission"])
        (td / ".step7a-complete").touch()
        if (td / "golden.zip").exists() and (td / "rubric.json").exists():
            (td / ".step7b-complete").touch()
    print(f"\nResubmit-ready folder: {td / 'submission'}")
    print("Section 1: submission/portal-submission.md")
    print("Section 2: submission/portal-section2.md")


def cmd_preflight(args: argparse.Namespace) -> None:
    """One command before every portal upload or resubmit.

    Rebuilds zips from source, then runs the drift checks that historically only
    surfaced after a 30-minute platform auto-eval round trip.
    """
    td = task_dir(args.slug)
    if not td.is_dir():
        print(f"Task not found: {args.slug}")
        raise SystemExit(1)

    run_script("package_zips.py", [str(td), "--all", "--sync-submission"])
    run_script("package_consistency_check.py", [str(td), "--strict"])
    run_script("lint_rubric.py", [str(td / "rubric.json"), "--strict"])
    run_script("portal_drift_check.py", [str(td), "--card-only"])
    run_script("portal_form.py", [str(td), "--all", "--sync-submission"])

    log = td / "submission-log.md"
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    line = f"\n## {stamp} — preflight\n\n- Ran `gf preflight {args.slug}` (zips rebuilt, drift + rubric lint, portal forms refreshed).\n"
    if log.exists():
        log.write_text(log.read_text(encoding="utf-8") + line, encoding="utf-8")
    else:
        log.write_text(f"# Submission log — {args.slug}\n{line}", encoding="utf-8")

    print(f"\nUpload from: {td / 'submission'}")
    print("  inputs.zip / golden.zip  (freshly rebuilt)")
    print("  Section 1: portal-submission.md")
    print("  Section 2: portal-section2.md")
    print("\nIf entity names changed, apply find/replace DELTA on portal criteria — do not re-enter all.")


def cmd_skeleton(args: argparse.Namespace) -> None:
    sk_args = [args.skeleton_cmd]
    if args.skeleton_cmd == "check":
        if not args.scaffold:
            print("Usage: gf skeleton check --scaffold <scaffold_id>")
            raise SystemExit(1)
        sk_args += ["--scaffold", args.scaffold, "--strict"]
    if getattr(args, "json", False):
        sk_args += ["--json"]
    run_script("skeleton_gate.py", sk_args)

def cmd_portal_drift(args: argparse.Namespace) -> None:
    td = task_dir(args.slug)
    run_script(
        "portal_drift_check.py",
        [str(td)] + (["--strict"] if args.strict else []) + (["--card-only"] if args.card_only else []),
    )


def cmd_new(args: argparse.Namespace) -> None:
    """One-shot: suggest seed → register → init."""
    archetype = args.archetype
    if getattr(args, "auto", False) or not archetype:
        archetype = _pick_auto_archetype()
        print(f"Auto-picked archetype: {archetype} (free skeleton preferred)")
    cmd_seed_suggest(
        argparse.Namespace(
            archetype=archetype,
            entity=args.entity,
            seed_id=args.seed_id,
            topology=args.topology,
            register=True,
            init=True,
            allow_skeleton_reuse=bool(getattr(args, "allow_skeleton_reuse", False)),
        )
    )
    slug = args.seed_id or slugify(f"{slugify(args.entity or 'acme')}-{archetype}")
    print(f"\nNew task scaffold ready: tasks/{slug}/")
    print(f"Next in chat: 'Run step 2a for {slug}'")
    print("Reminder: strip-test against registry/skeletons.json before Step 2b.")


def cmd_onet(args: argparse.Namespace) -> None:
    """Print exact O*NET portal dropdown strings for an occupation code or task slug."""
    sys.path.insert(0, str(REPO / "scripts"))
    from onet_lookup import format_portal_block, lookup, portal_suggestions, validate_metadata

    code = args.code
    meta_tasks: list[str] | None = None
    meta_skills: list[str] | None = None
    slug = args.slug

    if not code:
        if not slug:
            print("Usage: gf onet <slug>  OR  gf onet --code 13-2053.00")
            raise SystemExit(1)
        td = task_dir(slug)
        meta_file = td / "metadata.yaml"
        if not meta_file.exists():
            print(f"No metadata.yaml in {td}")
            raise SystemExit(1)
        import yaml

        meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        onet = meta.get("onet", {})
        code = onet.get("code")
        meta_tasks = onet.get("tasks")
        meta_skills = onet.get("skills")
        if not code:
            print(f"metadata.yaml missing onet.code for {slug}")
            raise SystemExit(1)

    data = lookup(code, refresh=args.refresh)
    if slug and not args.code:
        errors = validate_metadata({"code": code, "tasks": meta_tasks or [], "skills": meta_skills or []})
        if errors:
            print("WARN: metadata.yaml has strings not in portal dropdown:")
            for e in errors:
                print(f"  - {e}")
            print()

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(format_portal_block(data, meta_tasks=meta_tasks, meta_skills=meta_skills))

    if args.suggest:
        sug = portal_suggestions(data)
        print("\n### Suggested selections")
        for t in sug.get("tasks", []):
            print(f"TASK: {t}")
        for s in sug.get("skills", []):
            print(f"SKILL: {s}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Geranium Finance chat orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Show pipeline status")
    p_status.add_argument("slug", nargs="?", help="Task slug (optional)")
    p_status.set_defaults(func=cmd_status)

    p_next = sub.add_parser("next", help="Print next step for a task")
    p_next.add_argument("slug")
    p_next.set_defaults(func=cmd_next)

    p_init = sub.add_parser("init", help="Create task folder from templates")
    p_init.add_argument("slug")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_gate = sub.add_parser("gate", help="Run gates for a pipeline step")
    p_gate.add_argument("step", help="2a, 2b, 3, 4, 5, 6, 7a, 7b")
    p_gate.add_argument("slug")
    p_gate.add_argument("--package", action="store_true")
    p_gate.add_argument("--confirm-audit", action="store_true", help="Step 5: require completed audit")
    p_gate.set_defaults(func=cmd_gate)

    p_val = sub.add_parser("validate", help="Full task readiness check")
    p_val.add_argument("slug")
    p_val.add_argument("--strict", action="store_true")
    p_val.add_argument("--package", action="store_true")
    p_val.set_defaults(func=cmd_validate)

    p_repack = sub.add_parser(
        "repackage",
        help="Rebuild both zips (archive old), sync submission/ for portal resubmit",
    )
    p_repack.add_argument("slug")
    p_repack.set_defaults(func=cmd_repackage)

    p_pre = sub.add_parser(
        "preflight",
        help="Run before every portal upload: repackage + drift checks + portal forms",
    )
    p_pre.add_argument("slug")
    p_pre.set_defaults(func=cmd_preflight)

    p_onet = sub.add_parser("onet", help="O*NET portal dropdown strings (by code or task slug)")
    p_onet.add_argument("slug", nargs="?", help="Task slug — reads onet.code from metadata.yaml")
    p_onet.add_argument("--code", help="O*NET-SOC code, e.g. 13-2053.00 (overrides slug lookup)")
    p_onet.add_argument("--refresh", action="store_true", help="Re-fetch from onetonline.org")
    p_onet.add_argument("--suggest", action="store_true", help="Print suggested portal picks")
    p_onet.add_argument("--json", action="store_true", help="Output full cached JSON")
    p_onet.set_defaults(func=cmd_onet)

    p_portal = sub.add_parser("portal", help="Generate portal-submission.md form answers")
    p_portal.add_argument("slug")
    p_portal.set_defaults(func=cmd_portal)

    p_portal2 = sub.add_parser("portal2", help="Section 2 form: golden upload + rubric criteria")
    p_portal2.add_argument("slug")
    p_portal2.set_defaults(func=cmd_portal2)

    seed = sub.add_parser("seed", help="Seed registry commands")
    seed_sub = seed.add_subparsers(dest="seed_cmd", required=True)

    p_sr = seed_sub.add_parser("register", help="Register a seed")
    p_sr.add_argument("--seed-id", required=True)
    p_sr.add_argument("--topology")
    p_sr.add_argument("--scaffold")
    p_sr.add_argument("--file-mix")
    p_sr.add_argument("--opener-pattern", default="situation_first")
    p_sr.add_argument("--input-filenames")
    p_sr.add_argument("--allow-skeleton-reuse", action="store_true")
    p_sr.set_defaults(func=cmd_seed_register)

    p_sc = seed_sub.add_parser("check", help="Check seed uniqueness")
    p_sc.add_argument("--seed-id", required=True)
    p_sc.add_argument("--topology")
    p_sc.add_argument("--scaffold")
    p_sc.add_argument("--file-mix")
    p_sc.add_argument("--opener-pattern")
    p_sc.add_argument("--task-dir")
    p_sc.add_argument("--strict", action="store_true")
    p_sc.add_argument("--allow-skeleton-reuse", action="store_true")
    p_sc.set_defaults(func=cmd_seed_check)

    p_ss = seed_sub.add_parser("suggest", help="Suggest seed JSON from archetype")
    p_ss.add_argument("--archetype", required=True, choices=list(ARCHETYPES))
    p_ss.add_argument("--entity", help="Entity name for filenames")
    p_ss.add_argument("--seed-id")
    p_ss.add_argument("--topology")
    p_ss.add_argument("--register", action="store_true")
    p_ss.add_argument("--init", action="store_true")
    p_ss.add_argument("--allow-skeleton-reuse", action="store_true")
    p_ss.set_defaults(func=cmd_seed_suggest)

    p_new = sub.add_parser("new", help="Suggest + register + init in one shot")
    p_new.add_argument(
        "--archetype",
        nargs="?",
        default=None,
        choices=list(ARCHETYPES),
        help="Omit or pass --auto to pick a FREE skeleton archetype",
    )
    p_new.add_argument("--auto", action="store_true", help="Pick archetype from free skeletons")
    p_new.add_argument("--entity", help="Entity name")
    p_new.add_argument("--seed-id")
    p_new.add_argument("--topology")
    p_new.add_argument("--allow-skeleton-reuse", action="store_true")
    p_new.set_defaults(func=cmd_new)

    p_sk = sub.add_parser("skeleton", help="Decision-structure skeleton catalog (uniqueness)")
    p_sk.add_argument("skeleton_cmd", choices=["status", "pick", "check"])
    p_sk.add_argument("--scaffold", help="For check: scaffold id")
    p_sk.add_argument("--json", action="store_true")
    p_sk.set_defaults(func=cmd_skeleton)

    p_pd = sub.add_parser("portal-drift", help="Rubric ↔ inputs ↔ golden entity sync card")
    p_pd.add_argument("slug")
    p_pd.add_argument("--strict", action="store_true")
    p_pd.add_argument("--card-only", action="store_true")
    p_pd.set_defaults(func=cmd_portal_drift)

    args = parser.parse_args()
    if args.command == "seed":
        args.func(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
