#!/bin/bash
set -euo pipefail

REPO_DIR="$HOME/github/tamnd/brain"
BRANCH="main"
INTERVAL=300

# colors
GRN='\033[0;32m'; CYN='\033[0;36m'; YLW='\033[0;33m'; GRY='\033[0;90m'; RST='\033[0m'
ts()  { date '+%H:%M:%S'; }
log() { echo -e "${GRY}[$(ts)]${RST} $*"; }

cd "$REPO_DIR"
echo -e "${CYN}brain is on${RST} — ${GRY}$REPO_DIR, every ${INTERVAL}s${RST}"

build_commit_msg() {
  local added modified deleted renamed
  added=$(git diff --cached --name-only --diff-filter=A | wc -l | tr -d ' ')
  modified=$(git diff --cached --name-only --diff-filter=M | wc -l | tr -d ' ')
  deleted=$(git diff --cached --name-only --diff-filter=D | wc -l | tr -d ' ')
  renamed=$(git diff --cached --name-only --diff-filter=R | wc -l | tr -d ' ')

  local parts=()
  [ "$added" -gt 0 ]    && parts+=("$added new")
  [ "$modified" -gt 0 ] && parts+=("$modified updated")
  [ "$deleted" -gt 0 ]  && parts+=("$deleted removed")
  [ "$renamed" -gt 0 ]  && parts+=("$renamed renamed")

  local summary
  summary=$(IFS=', '; echo "${parts[*]}")

  local first section
  first=$(git diff --cached --name-only | head -1)
  section=$(dirname "$first" | sed 's|^content/[a-z]*/||; s|^\.$||; s|^content||')
  [ -n "$section" ] && section=" [$section]" || section=""

  echo "note${section}: ${summary} ($(date '+%Y-%m-%d %H:%M'))"
}

while true; do
  if [ -n "$(git status --porcelain)" ]; then
    git add -A
    if ! git diff --cached --quiet; then
      MSG="$(build_commit_msg)"
      git commit -q -m "$MSG"
      git push -q origin "$BRANCH"
      log "${GRN}✓ $MSG${RST}"
    else
      log "${YLW}· nothing to commit${RST}"
    fi
  else
    log "${GRY}· nothing to commit${RST}"
  fi

  sleep "$INTERVAL"
done
