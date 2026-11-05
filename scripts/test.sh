#!/usr/bin/env bash
# irskills test runner. Dev-only (not part of shipped skills). Deps: claude CLI, bash 3.2+, jq.
# Usage: scripts/test.sh [all|static|eval|pairs] [--runs N] [--case GLOB] [--save-baseline] [--max-cost USD]
# Env:   AGENT_MODEL (default claude-sonnet-5-5)  JUDGE_MODEL (default claude-opus-5-5)
#        JUDGE_VOTES (default 3)  THRESHOLD (default 0.8)  CONCURRENCY (default 2)
# See TESTING.md for the flow diagram.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODE="all"; RUNS=3; CASE=""; SAVE_BASELINE=0; MAX_COST=10
AGENT_MODEL="${AGENT_MODEL:-claude-sonnet-5-5}"
JUDGE_MODEL="${JUDGE_MODEL:-claude-opus-5-5}"
JUDGE_VOTES="${JUDGE_VOTES:-3}"
THRESHOLD="${THRESHOLD:-0.8}"
CONCURRENCY="${CONCURRENCY:-2}"

while [ $# -gt 0 ]; do
  case "$1" in
    all|static|eval|pairs) MODE="$1" ;;
    --runs) RUNS="$2"; shift ;;
    --case) CASE="$2"; shift ;;
    --save-baseline) SAVE_BASELINE=1 ;;
    --max-cost) MAX_COST="$2"; shift ;;
    -h|--help) sed -n 2,6p "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 64 ;;
  esac
  shift
done

command -v jq >/dev/null || { echo "jq required" >&2; exit 69; }
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
OUT="$REPO/evals/results/$TS"; mkdir -p "$OUT"
FAILS=0
log() { printf '%s\n' "$*" | tee -a "$OUT/run.log"; }
fail() { FAILS=$((FAILS+1)); log "  FAIL $*"; }

# ---------- helpers ----------
# frontmatter keys (top-level, between first two --- lines)
fm_keys() { awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f&&/^[A-Za-z_-]+:/{sub(/:.*/,"");print}' "$1"; }
fm_val() { awk -v k="$2" 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f{sub(/^[ \t]+/,""); if(index($0,k": ")==1){v=substr($0,length(k)+3); gsub(/^"|"$/,"",v); print v; exit}}' "$1"; }
kv() { grep -E "^$2=" "$1" | tail -1 | cut -d= -f2-; }   # flat key=value (same format as irskills config)
semver() { printf '%s' "$1" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; }
words() { wc -w | tr -d ' '; }
PLUGIN_VER="$(jq -r .version "$REPO/.claude-plugin/plugin.json" 2>/dev/null)"

# ---------- 0. sync rubrics into llm graders (single source: evals/rubrics/*.md) ----------
sync_rubrics() {
  for g in "$REPO"/evals/*/*/graders/rubric-*.md; do
    [ -f "$g" ] || continue
    name="$(basename "$g" .md)"; name="${name#rubric-}"
    src="$REPO/evals/rubrics/$name.md"
    [ -f "$src" ] || { fail "missing rubric $src for $g"; continue; }
    head="$(awk 'NR==1{print;next} {print} /^---$/{exit}' "$g")"
    { printf '%s\n' "$head"; echo "<!-- body synced from evals/rubrics/$name.md by scripts/test.sh; edit the rubric, not this -->"; cat "$src"; } > "$g.tmp" && mv "$g.tmp" "$g"
  done
}

# ---------- 1. static (free, deterministic) ----------
run_static() {
  log "== static"
  semver "$PLUGIN_VER" || fail "plugin.json version not semver: $PLUGIN_VER"
  grep -q "^## irskills $PLUGIN_VER" "$REPO/CHANGELOG.md" || fail "CHANGELOG missing '## irskills $PLUGIN_VER'"
  [ -f "$REPO/skills/_shared/SKILL.md" ] && fail "_shared must not contain SKILL.md"
  allowed=" name description license compatibility metadata allowed-tools argument-hint "
  for s in "$REPO"/skills/*/SKILL.md; do
    dir="$(basename "$(dirname "$s")")"
    for k in $(fm_keys "$s"); do case "$allowed" in *" $k "*) ;; *) fail "$dir: non-portable frontmatter key '$k'";; esac; done
    [ "$(fm_val "$s" name)" = "$dir" ] || fail "$dir: name != dir"
    v="$(awk '/^metadata:/{m=1;next} m&&/^[ \t]+version:/{gsub(/.*version:[ \t]*|"/,"");print;exit} m&&/^[^ \t]/{exit}' "$s")"
    semver "$v" || fail "$dir: metadata.version missing/not semver"
    grep -q "^## $dir $v" "$REPO/CHANGELOG.md" || fail "$dir: CHANGELOG missing '## $dir $v'"
    grep -q '\.\./_shared/config-rules\.md' "$s" || fail "$dir: does not reference shared config rules"
    printf '%s=%s\n' "$dir" "$v" >> "$OUT/versions.txt"
  done
  for c in "$REPO"/evals/*/*/prompt.md; do
    d="$(dirname "$c")"; ls "$d"/graders/*.md >/dev/null 2>&1 || fail "$(basename "$d"): no graders"
  done
  log "  static done"
}

# ---------- 2. plugin eval (single-run cases; regex/file/llm graders) ----------
run_eval() {
  log "== eval (claude plugin eval, runs=$RUNS, agent=$AGENT_MODEL, judge=$JUDGE_MODEL)"
  args=(plugin eval "$REPO" --trust-plugin --scaffold --no-publish --ablation none
        --allow-tools Write --runs "$RUNS" --threshold "$THRESHOLD" -j "$CONCURRENCY"
        --model "$AGENT_MODEL" --judge-model "$JUDGE_MODEL" --max-cost-usd "$MAX_COST"
        --json "$OUT/eval.json" --output-dir "$OUT/eval")
  [ -n "$CASE" ] && args+=(--case "$CASE")
  claude "${args[@]}" 2>&1 | tee -a "$OUT/run.log"
  rc=${PIPESTATUS[0]}
  [ "$rc" -eq 0 ] || fail "plugin eval exit $rc (1=case below threshold, 2=partial)"
}

# ---------- 3. pairs (cross-run comparisons via claude -p + judge) ----------
judge() { # $1 rubric name, $2 input file -> prints judge JSON (majority of votes)
  schema="$(cat "$REPO/evals/rubrics/_judge-schema.json")"
  passes=0; last=""
  for i in $(seq 1 "$JUDGE_VOTES"); do
    r="$( { cat "$REPO/evals/rubrics/$1.md"; echo; cat "$2"; } | claude -p --model "$JUDGE_MODEL" --setting-sources project,local \
          --output-format json --json-schema "$schema" --no-session-persistence --allowedTools "" 2>/dev/null)"
    so="$(printf '%s' "$r" | jq -c '.structured_output // empty' 2>/dev/null)"
    [ -n "$so" ] || continue
    last="$so"; [ "$(printf '%s' "$so" | jq -r .pass)" = "true" ] && passes=$((passes+1))
  done
  need=$(( JUDGE_VOTES / 2 + 1 ))
  printf '%s' "${last:-{\}}" | jq -c --argjson p "$passes" --argjson n "$need" '. + {votes_pass:$p, majority_pass:($p>=$n)}'
}

run_side() { # $1 prompt, $2 fixture, $3 outdir -> writes reply.json, workspace copy
  ws="$(mktemp -d "${TMPDIR:-/tmp}/irskills-pair.XXXXXX")" || return 1
  ( cd "$ws" && git init -q . && { [ -z "$2" ] || bash "$REPO/evals/fixtures/$2.sh"; } )
  iso=(); [ -n "${ANTHROPIC_API_KEY:-}" ] && iso=(--bare)   # extra isolation if API key set
  # --setting-sources project,local: excludes user CLAUDE.md + ~/.claude/skills (avoids bias + name clash w/ plugin skills)
  ( cd "$ws" && claude -p "$1" ${iso[@]+"${iso[@]}"} --setting-sources project,local --plugin-dir "$REPO" --model "$AGENT_MODEL" --output-format json \
      --allowedTools Read Glob Grep Skill Write --permission-mode acceptEdits --no-session-persistence ) > "$3/reply.json" 2>"$3/stderr.txt"
  cp -R "$ws" "$3/workspace"
  case "$ws" in */irskills-pair.*) rm -rf -- "$ws" ;; esac   # only ever delete our own mktemp dir
}

run_pairs() {
  log "== pairs (agent=$AGENT_MODEL, judge=$JUDGE_MODEL x$JUDGE_VOTES)"
  echo '[]' > "$OUT/pairs.json"
  for p in "$REPO"/evals/pairs/*.pair; do
    n="$(basename "$p" .pair)"
    [ -n "$CASE" ] && case "$n" in $CASE) ;; *) continue;; esac
    d="$OUT/pairs/$n"; mkdir -p "$d/a" "$d/b"
    fx="$(kv "$p" fixture)"; cmp="$(kv "$p" compare)"
    run_side "$(kv "$p" a)" "$fx" "$d/a"; run_side "$(kv "$p" b)" "$fx" "$d/b"
    for s in a b; do
      if [ "$cmp" = reply ]; then jq -r '.result // ""' "$d/$s/reply.json" > "$d/$s/text.md"
      else f="${cmp#file:}"; cat "$d/$s/workspace/$f" > "$d/$s/text.md" 2>/dev/null || : > "$d/$s/text.md"; fi
    done
    wa=$(words < "$d/a/text.md"); wb=$(words < "$d/b/text.md"); det=true; why=""
    [ "$wa" -gt 0 ] && [ "$wb" -gt 0 ] || { det=false; why="empty output"; }
    if $det && [ "$cmp" = reply ]; then   # skill must have run: echo line is first line of both replies
      for s in a b; do head -1 "$d/$s/text.md" | grep -Eq '^\s*\[[a-z-]+·[a-z]+·[a-z]+·[a-z]+\]' || { det=false; why="$s: no echo line on line 1 (skill not invoked?)"; }; done
    fi
    rmin="$(kv "$p" words_ratio_min)"; rmax="$(kv "$p" words_ratio_max)"
    if $det && [ -n "$rmin" ]; then awk -v a="$wa" -v b="$wb" -v m="$rmin" 'BEGIN{exit !(b>=a*m)}' || { det=false; why="words b/a < $rmin ($wb/$wa)"; }; fi
    if $det && [ -n "$rmax" ]; then awk -v a="$wa" -v b="$wb" -v m="$rmax" 'BEGIN{r=(a>b?a/b:b/a); exit !(r<=m)}' || { det=false; why="word ratio > $rmax ($wa vs $wb)"; }; fi
    if $det && [ "$(kv "$p" same_headers)" = 1 ]; then
      diff <(grep -E '^#+ ' "$d/a/text.md" | tr 'A-Z' 'a-z') <(grep -E '^#+ ' "$d/b/text.md" | tr 'A-Z' 'a-z') >/dev/null || { det=false; why="header sets differ"; }
    fi
    { echo "## A"; cat "$d/a/text.md"; echo; echo "## B"; cat "$d/b/text.md"; } > "$d/judge-input.md"
    j="$(judge "$(kv "$p" rubric)" "$d/judge-input.md")"; printf '%s\n' "$j" > "$d/judge.json"
    jp="$(printf '%s' "$j" | jq -r '.majority_pass // false')"
    cost="$(jq -s '[.[].total_cost_usd // 0] | add' "$d/a/reply.json" "$d/b/reply.json" 2>/dev/null || echo 0)"
    ok=false; $det && [ "$jp" = true ] && ok=true
    $ok && log "  pass $n" || fail "$n: det=$det ${why:+($why)} judge=$jp"
    jq --arg n "$n" --argjson ok "$ok" --argjson det "$det" --arg why "$why" --argjson j "${j:-{\}}" --argjson c "${cost:-0}" \
       '. + [{name:$n, pass:$ok, deterministic:$det, why:$why, judge:$j, agentCostUsd:$c}]' "$OUT/pairs.json" > "$OUT/pairs.tmp" && mv "$OUT/pairs.tmp" "$OUT/pairs.json"
  done
}

# ---------- 4. summary + baseline/regression ----------
summarize() {
  S="$OUT/SUMMARY.md"; sha="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null)"
  git -C "$REPO" diff --quiet 2>/dev/null || sha="$sha+dirty"
  {
    echo "# Test summary $TS"
    echo "- plugin irskills $PLUGIN_VER · skills: $(tr '\n' ' ' < "$OUT/versions.txt" 2>/dev/null)· git $sha"
    echo "- agent $AGENT_MODEL · judge $JUDGE_MODEL · runs $RUNS · threshold $THRESHOLD · mode $MODE"
    echo "- result: $([ $FAILS -eq 0 ] && echo PASS || echo "FAIL ($FAILS)")"
  } > "$S"
  scores="{}"
  if [ -f "$OUT/eval.json" ]; then
    scores="$(jq -c '[.cases[] | {key:.name, value:(.aggregates.score // 0)}] | from_entries' "$OUT/eval.json")"
    { echo; echo "## Cases (plugin eval)"; echo "| case | score | |"; echo "|---|---|---|"
      jq -r --argjson t "$THRESHOLD" '.cases[] | "| \(.name) | \(.aggregates.score // 0 | .*100|round/100) | \(if (.aggregates.score // 0) >= $t then "ok" else "FAIL" end) |"' "$OUT/eval.json"
      echo; echo "cost \$$(jq -r '(.costUsd // 0)*100|round/100' "$OUT/eval.json") · report: eval/*/report.html"; } >> "$S"
  fi
  if [ -f "$OUT/pairs.json" ]; then
    { echo; echo "## Pairs"; echo "| pair | pass | deterministic | judge votes | suggested edit |"; echo "|---|---|---|---|---|"
      jq -r '.[] | "| \(.name) | \(.pass) | \(.deterministic) \(.why) | \(.judge.votes_pass // 0) | \(.judge.suggested_skill_edit // "" | gsub("\n";" ")) |"' "$OUT/pairs.json"; } >> "$S"
    scores="$(jq -c --argjson s "$scores" '$s + ([.[] | {key:("pair:"+.name), value:(if .pass then 1 else 0 end)}] | from_entries)' "$OUT/pairs.json")"
  fi
  printf '%s\n' "$scores" > "$OUT/scores.json"
  base="$(ls -1 "$REPO"/evals/baselines/irskills@*.json 2>/dev/null | sort -V | tail -1)"
  if [ -n "$base" ]; then
    { echo; echo "## Regression vs $(basename "$base")"
      jq -r -n --slurpfile b "$base" --argjson c "$scores" '$b[0].scores as $o | [$c|to_entries[] | select($o[.key] != null and .value < $o[.key]-0.1) | "- REGRESSION \(.key): \($o[.key]) -> \(.value)"] | if length==0 then "- none" else .[] end'; } >> "$S"
    grep -q REGRESSION "$S" && FAILS=$((FAILS+1))
  fi
  if [ "$SAVE_BASELINE" = 1 ]; then
    mkdir -p "$REPO/evals/baselines"
    jq -n --arg v "$PLUGIN_VER" --arg sha "$sha" --arg ts "$TS" --arg am "$AGENT_MODEL" --arg jm "$JUDGE_MODEL" --argjson s "$scores" \
      '{plugin:$v, git:$sha, date:$ts, agentModel:$am, judgeModel:$jm, scores:$s}' > "$REPO/evals/baselines/irskills@$PLUGIN_VER.json"
    echo "- baseline saved: evals/baselines/irskills@$PLUGIN_VER.json" >> "$S"
  fi
  echo; cat "$S"
}

sync_rubrics
run_static
case "$MODE" in
  all)   run_eval; run_pairs ;;
  eval)  run_eval ;;
  pairs) run_pairs ;;
esac
summarize
[ $FAILS -eq 0 ]
