#!/bin/bash
set -euo pipefail

REPO_DIR="$HOME/github/tamnd/brain"
BRANCH="main"
INTERVAL=300

cd "$REPO_DIR"

echo "brain is on -- watching $REPO_DIR every ${INTERVAL}s"

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

  # Get the first changed file as a hint
  local first
  first=$(git diff --cached --name-only | head -1)
  local section
  section=$(dirname "$first" | sed 's|^content/[a-z]*/||; s|^\.$||; s|^content||')
  [ -n "$section" ] && section=" [$section]" || section=""

  echo "note${section}: ${summary} ($(date '+%Y-%m-%d %H:%M'))"
}

while true; do
  TS="$(date '+%Y-%m-%d %H:%M:%S')"

  if [ -n "$(git status --porcelain)" ]; then
    git add -A

    if ! git diff --cached --quiet; then
      MSG="$(build_commit_msg)"
      git commit -m "$MSG"
      git push origin "$BRANCH"
      echo "[$TS] $MSG"
    fi
  fi

  sleep "$INTERVAL"
done
