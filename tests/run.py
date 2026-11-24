#!/usr/bin/env python3
"""Run skill test cases live. Every run: fresh temp workspace built from the case's fixture,
fresh `claude -p` session (never resumed, never saved), then a judge grades the output
against expected.md. No cached inputs, no baselines.

Usage: python3 tests/run.py [skill] [--case NAME] [--runs N]
Env:   AGENT_MODEL (default claude-sonnet-5-5), JUDGE_MODEL (default claude-opus-5-5)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASES = REPO / "tests" / "cases"
AGENT_MODEL = os.environ.get("AGENT_MODEL", "claude-sonnet-5-5")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-opus-5-5")
FRESH = ["--no-session-persistence", "--strict-mcp-config"]
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"items": {"type": "array", "items": {
        "type": "object",
        "properties": {"expect": {"type": "string"}, "pass": {"type": "boolean"}, "why": {"type": "string"}},
        "required": ["expect", "pass", "why"]}}},
    "required": ["items"],
}


def skill_version(path: Path) -> str:
    m = re.search(r'version:\s*"([^"]+)"', path.read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


def snapshot(ws: Path) -> dict[str, str]:
    out = {}
    for p in ws.rglob("*"):
        if p.is_file() and ".git" not in p.relative_to(ws).parts:
            out[str(p.relative_to(ws))] = hashlib.sha1(p.read_bytes()).hexdigest()
    return out


def claude(prompt: str, model: str, cwd: Path, extra: list[str]) -> dict:
    r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json", *FRESH, *extra],
                       input=prompt, cwd=cwd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise RuntimeError(f"claude exited {r.returncode}: {r.stderr[-2000:]}")
    return json.loads(r.stdout)


def run_case(case: Path, run: int, out_dir: Path) -> dict:
    meta = tomllib.loads((case / "case.toml").read_text(encoding="utf-8"))
    skill_file = REPO / "skills" / meta["skill"]
    ws = Path(tempfile.mkdtemp(prefix=f"skilltest-{case.name}-"))
    try:
        if (case / "files").is_dir():
            shutil.copytree(case / "files", ws, dirs_exist_ok=True)
        if (case / "setup.sh").is_file():
            subprocess.run(["bash", str(case / "setup.sh")], cwd=ws, check=True, capture_output=True)
        before = snapshot(ws)
        prompt = (case / "prompt.md").read_text(encoding="utf-8").replace("{skill}", str(skill_file))
        agent = claude(prompt, AGENT_MODEL, ws, ["--dangerously-skip-permissions",
                                                 "--disallowedTools", "Bash(gh:*)", "Bash(git push:*)"])
        after = snapshot(ws)
        changed = [p for p in after if before.get(p) != after[p]]
        files = "\n\n".join(f"--- {p}\n{(ws / p).read_text(encoding='utf-8', errors='replace')[:20000]}"
                            for p in sorted(changed))
        judge_prompt = (
            "You grade one test run of a Claude skill. Use no tools. For each bullet in EXPECTED, decide pass/fail "
            "strictly from the AGENT OUTPUT and CHANGED FILES. `must not` bullets pass only if the thing is absent.\n\n"
            f"EXPECTED:\n{(case / 'expected.md').read_text(encoding='utf-8')}\n\n"
            f"AGENT OUTPUT:\n{agent.get('result', '')}\n\nCHANGED FILES:\n{files or '(none)'}\n")
        judged = claude(judge_prompt, JUDGE_MODEL, ws, ["--json-schema", json.dumps(JUDGE_SCHEMA)])
        verdict = judged.get("structured_output") or json.loads(judged.get("result", "{}"))
        items = verdict.get("items", [])
        result = {"case": f"{meta['skill']}/{case.name}", "run": run, "skill_version": skill_version(skill_file),
                  "agent_model": AGENT_MODEL, "judge_model": JUDGE_MODEL,
                  "pass": bool(items) and all(i["pass"] for i in items), "items": items,
                  "cost_usd": round(agent.get("total_cost_usd", 0) + judged.get("total_cost_usd", 0), 4),
                  "agent_output": agent.get("result", ""), "changed_files": changed}
    finally:
        shutil.rmtree(ws, ignore_errors=True)
    (out_dir / f"{case.parent.name}__{case.name}__{run}.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill", nargs="?", help="skill folder name, e.g. shipit")
    ap.add_argument("--case", help="case folder name")
    ap.add_argument("--runs", type=int, default=1)
    a = ap.parse_args()
    cases = sorted(p for p in CASES.glob("*/*") if (p / "case.toml").is_file()
                   and (not a.skill or p.parent.name == a.skill) and (not a.case or p.name == a.case))
    if not cases:
        print("no cases match", file=sys.stderr)
        return 2
    out_dir = REPO / "tests" / "results" / time.strftime("%Y-%m-%dT%H-%M-%S")
    out_dir.mkdir(parents=True)
    fails = 0
    for case in cases:
        for run in range(1, a.runs + 1):
            try:
                r = run_case(case, run, out_dir)
            except Exception as e:  # report and keep going; a crash counts as a fail
                r = {"case": f"{case.parent.name}/{case.name}", "run": run, "pass": False, "error": str(e), "items": []}
            fails += not r["pass"]
            print(f"{'PASS' if r['pass'] else 'FAIL'}  {r['case']} run {run}  v{r.get('skill_version', '?')}  ${r.get('cost_usd', 0)}")
            for i in r["items"]:
                if not i["pass"]:
                    print(f"      x {i['expect']}: {i['why']}")
            if "error" in r:
                print(f"      error: {r['error']}")
    print(f"\n{fails} failed. Results: {out_dir}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
