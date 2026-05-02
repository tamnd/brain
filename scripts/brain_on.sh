#!/bin/bash
set -euo pipefail

REPO_DIR="$HOME/github/tamnd/brain"
BRANCH="main"
INTERVAL=60

cd "$REPO_DIR"

echo "brain is on -- watching $REPO_DIR every ${INTERVAL}s"

while true; do
  TS="$(date '+%Y-%m-%d %H:%M:%S')"

  if [ -n "$(git status --porcelain)" ]; then
    git add -A

    if ! git diff --cached --quiet; then
      MSG="note: $TS"
      git commit -m "$MSG"
      git push origin "$BRANCH"
      echo "[$TS] saved and pushed"
    fi
  fi

  sleep "$INTERVAL"
done
