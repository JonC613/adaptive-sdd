#!/usr/bin/env python3
"""Track resumable Adaptive SDD delivery state and evidence.

This is an audit aid, not a security boundary. It never executes artifact content.
"""
from __future__ import annotations

import argparse, hashlib, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
MODES = ("guided", "collaborative", "delegated")
TIERS = ("tiny", "lite", "speckit")
LIFECYCLES = ("planned", "implementing", "implemented", "verified", "released")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr); raise SystemExit(1)


def path_for(project: Path, feature: str) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", feature): die("feature must be a lowercase kebab-case slug")
    return project / ".sdd" / "features" / feature / "state.json"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(path: Path) -> str | None:
    if path.is_file(): return digest(path)
    if path.is_dir():
        values = [(p.relative_to(path).as_posix(), digest(p)) for p in sorted(path.rglob("*")) if p.is_file()]
        return "sha256-tree:" + hashlib.sha256(json.dumps(values, separators=(",", ":")).encode()).hexdigest()
    return None


def relative(project: Path, raw: str) -> tuple[str, Path]:
    path = (project / raw).resolve()
    try: rel = path.relative_to(project.resolve()).as_posix()
    except ValueError: die(f"path escapes project: {raw}")
    return rel, path


def read_state(project: Path, feature: str) -> tuple[Path, dict[str, Any]]:
    path = path_for(project, feature)
    try: state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError: die(f"feature state does not exist: {feature}")
    except json.JSONDecodeError as exc: die(f"invalid feature state: {exc}")
    if state.get("schema_version") != SCHEMA_VERSION: die("unsupported feature-state schema")
    return path, state


def write(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git(project: Path, *args: str) -> str | None:
    try: result = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True)
    except FileNotFoundError: return None
    return result.stdout.strip() if result.returncode == 0 else None


def snapshot(project: Path) -> str:
    listed = git(project, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if listed is None:
        candidates = [p for p in project.rglob("*") if p.is_file() and ".git" not in p.parts]
    else:
        candidates = [project / raw for raw in listed.split("\0") if raw]
    values = []
    for path in candidates:
        try: raw = path.relative_to(project).as_posix()
        except ValueError: continue
        if raw.startswith(".sdd/features/") or raw == ".sdd/memory-state.json": continue
        values.append((raw, digest(path) if path.is_file() else "missing"))
    payload = json.dumps(sorted(values), separators=(",", ":")).encode()
    return "content:" + hashlib.sha256(payload).hexdigest()


def artifact_paths(project: Path, feature: str, tier: str, supplied: list[str]) -> list[str]:
    if supplied: return [relative(project, item)[0] for item in supplied]
    if tier == "tiny": return [f".tinyspec/{feature}.md"]
    if tier == "lite": return [f".litespec/{feature}/{name}.md" for name in ("spec", "plan", "tests")]
    return [f"specs/{feature}"]


def parse_ids(project: Path, artifacts: list[str]) -> tuple[list[str], list[str]]:
    acceptance, requirements, tasks = set(), set(), set()
    for item in artifacts:
        path = project / item
        candidates = [path] if path.is_file() else sorted(path.rglob("*.md")) if path.is_dir() else []
        for candidate in candidates:
            text = candidate.read_text(encoding="utf-8")
            acceptance.update(re.findall(r"\bAC-\d{2}\.\d+\b", text))
            requirements.update(re.findall(r"\bR-\d{2}\b", text))
            tasks.update(re.findall(r"\*\*(P\d+-T\d+)\s+—", text))
    return sorted(acceptance or requirements), sorted(tasks)


def stale_artifacts(project: Path, state: dict[str, Any]) -> list[str]:
    stale = []
    for artifact in state["artifacts"]:
        path = project / artifact["path"]
        current = fingerprint(path)
        if artifact.get("approved_fingerprint") != current: stale.append(artifact["path"])
    return stale


def blockers(project: Path, state: dict[str, Any]) -> list[str]:
    problems = [f"stale or unapproved artifact: {p}" for p in stale_artifacts(project, state)]
    problems += [f"unfinished task: {t['id']}" for t in state["tasks"] if t["status"] != "done"]
    current = snapshot(project)
    for criterion in state["criteria"]:
        matches = [e for e in state["evidence"] if e["criterion"] == criterion and e["result"] == "pass" and e["snapshot"] == current]
        if not matches: problems.append(f"missing current passing evidence: {criterion}")
    problems += [f"blocking condition: {b}" for b in state.get("blockers", [])]
    return problems


def command_init(args: argparse.Namespace) -> None:
    project = args.project.resolve(); path = path_for(project, args.feature)
    if path.exists(): die("feature state already exists; refusing to overwrite")
    artifacts = artifact_paths(project, args.feature, args.tier, args.artifact)
    for item in artifacts:
        if not (project / item).exists(): die(f"artifact does not exist: {item}")
    criteria, tasks = parse_ids(project, artifacts)
    state = {"schema_version": 1, "feature": args.feature, "tier": args.tier,
             "interaction_mode": args.mode, "lifecycle": "planned", "updated_at": now(),
             "artifacts": [{"path": p, "approved_fingerprint": None, "approval": None} for p in artifacts],
             "criteria": criteria, "tasks": [{"id": t, "status": "pending"} for t in tasks],
             "evidence": [], "blockers": [],
             "authorization": {"allowed": args.allow, "excluded": args.exclude}, "release": None}
    write(path, state); print(f"Initialized delivery state for {args.feature}")


def command_approve(args: argparse.Namespace) -> None:
    project = args.project.resolve(); path, state = read_state(project, args.feature)
    if not re.fullmatch(r"(?:human:|process:)[^\s]+", args.by): die("approval actor must be human:<id> or process:<id>")
    for artifact in state["artifacts"]:
        source = project / artifact["path"]
        current = fingerprint(source)
        if not current: die(f"approval requires existing artifact: {artifact['path']}")
        artifact["approved_fingerprint"] = current
        artifact["approval"] = {"by": args.by, "at": now(), "actions": args.action}
    criteria, tasks = parse_ids(project, [a["path"] for a in state["artifacts"]])
    prior = {item["id"]: item["status"] for item in state["tasks"]}
    state["criteria"] = criteria
    state["tasks"] = [{"id": item, "status": prior.get(item, "pending")} for item in tasks]
    state["updated_at"] = now(); write(path, state); print("Recorded artifact fingerprints and stated approval")


def command_task(args: argparse.Namespace) -> None:
    path, state = read_state(args.project.resolve(), args.feature)
    task = next((t for t in state["tasks"] if t["id"] == args.task), None)
    if not task: die(f"unknown task: {args.task}")
    actions = {a for artifact in state["artifacts"] for a in (artifact.get("approval") or {}).get("actions", [])}
    if "implementation" not in actions and not (state["interaction_mode"] == "delegated" and "implementation" in state["authorization"]["allowed"]):
        die("implementation is outside recorded authorization")
    task["status"] = args.status
    if args.status == "doing" and state["lifecycle"] == "planned": state["lifecycle"] = "implementing"
    if state["tasks"] and all(t["status"] == "done" for t in state["tasks"]): state["lifecycle"] = "implemented"
    state["updated_at"] = now(); write(path, state); print(f"{args.task}: {args.status}")


def command_evidence(args: argparse.Namespace) -> None:
    project = args.project.resolve(); path, state = read_state(project, args.feature)
    if args.criterion not in state["criteria"]: die(f"unknown criterion: {args.criterion}")
    if not re.fullmatch(r"(?:human:|process:)[^\s]+", args.by): die("evidence actor must be human:<id> or process:<id>")
    if args.method == "manual" and not args.by.startswith("human:"): die("manual evidence requires a human actor")
    if args.method == "automated":
        if not args.command or args.exit_code is None: die("automated evidence requires --command and --exit-code")
        if (args.exit_code == 0) != (args.result == "pass"): die("automated result conflicts with exit code")
    source, source_path = relative(project, args.source)
    if not source_path.exists(): die(f"evidence source does not exist: {source}")
    state["evidence"].append({"id": f"E-{len(state['evidence'])+1:03}", "criterion": args.criterion,
        "method": args.method, "result": args.result, "source": source,
        "recorded_by": args.by, "at": now(), "snapshot": snapshot(project),
        "command": args.command, "exit_code": args.exit_code, "detail": args.detail})
    state["updated_at"] = now(); write(path, state); print(f"Recorded {args.result} evidence for {args.criterion}")


def command_status(args: argparse.Namespace) -> None:
    project = args.project.resolve(); _, state = read_state(project, args.feature)
    found = blockers(project, state)
    output = {"feature": state["feature"], "status": "blocked" if found else state["lifecycle"],
              "recorded_lifecycle": state["lifecycle"], "interaction_mode": state["interaction_mode"],
              "blockers": found, "next_action": "resolve blockers" if found else "verify"}
    print(json.dumps(output, indent=2) if args.json else f"Feature: {output['feature']}\nStatus: {output['status']}\nRecorded lifecycle: {output['recorded_lifecycle']}\nMode: {output['interaction_mode']}\nNext: {output['next_action']}" + "".join(f"\nBLOCKED: {b}" for b in output["blockers"]))


def command_verify(args: argparse.Namespace) -> None:
    project = args.project.resolve(); path, state = read_state(project, args.feature); problems = blockers(project, state)
    if problems:
        if args.json: print(json.dumps({"schema_version":1,"verified":False,"blockers":problems}))
        else:
            for problem in problems: print(f"BLOCKED: {problem}")
        raise SystemExit(1)
    state["lifecycle"] = "verified"; state["verified_at"] = now(); state["verified_snapshot"] = snapshot(project)
    state["updated_at"] = now(); write(path, state)
    print(json.dumps({"schema_version":1,"verified":True,"blockers":[]}) if args.json else "VERIFIED: completion gate passed")


def command_release(args: argparse.Namespace) -> None:
    project = args.project.resolve(); path, state = read_state(project, args.feature)
    if state["lifecycle"] != "verified" or state.get("verified_snapshot") != snapshot(project): die("current snapshot is not verified")
    actions = {a for artifact in state["artifacts"] for a in (artifact.get("approval") or {}).get("actions", [])}
    delegated = state["interaction_mode"] == "delegated" and "deployment" in state["authorization"]["allowed"] and "deployment" not in state["authorization"]["excluded"]
    if "release" not in actions and not delegated: die("release is outside recorded authorization")
    state["lifecycle"] = "released"; state["release"] = {"reference": args.reference, "at": now()}; state["updated_at"] = now()
    write(path, state); print(f"RELEASED: {args.reference}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--project", type=Path, default=Path.cwd())
    subs = parser.add_subparsers(required=True)
    p = subs.add_parser("init"); p.add_argument("--feature", required=True); p.add_argument("--tier", choices=TIERS, required=True); p.add_argument("--mode", choices=MODES, default="collaborative"); p.add_argument("--artifact", action="append", default=[]); p.add_argument("--allow", action="append", default=[]); p.add_argument("--exclude", action="append", default=[]); p.set_defaults(run=command_init)
    p = subs.add_parser("approve"); p.add_argument("--feature", required=True); p.add_argument("--by", required=True); p.add_argument("--action", action="append", choices=("implementation", "release", "memory"), default=[]); p.set_defaults(run=command_approve)
    p = subs.add_parser("task"); p.add_argument("--feature", required=True); p.add_argument("--task", required=True); p.add_argument("--status", choices=("pending", "doing", "done", "blocked"), required=True); p.set_defaults(run=command_task)
    p = subs.add_parser("evidence"); p.add_argument("--feature", required=True); p.add_argument("--criterion", required=True); p.add_argument("--method", choices=("automated", "manual", "experiment", "contract"), required=True); p.add_argument("--result", choices=("pass", "fail"), required=True); p.add_argument("--source", required=True); p.add_argument("--by", required=True); p.add_argument("--command"); p.add_argument("--exit-code", type=int); p.add_argument("--detail"); p.set_defaults(run=command_evidence)
    for name, run in (("status", command_status), ("verify", command_verify)):
        p = subs.add_parser(name); p.add_argument("--feature", required=True); p.add_argument("--json", action="store_true"); p.set_defaults(run=run)
    p = subs.add_parser("release"); p.add_argument("--feature", required=True); p.add_argument("--reference", required=True); p.set_defaults(run=command_release)
    args = parser.parse_args(); args.run(args)


if __name__ == "__main__": main()
