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
  # Auto-repair malformed Hugo front matter before staging.
  if FIX_OUT="$(python3 "$REPO_DIR/scripts/fix_frontmatter.py" 2>&1)" && [ -n "$FIX_OUT" ]; then
    while IFS= read -r line; do log "${YLW}fm: ${line}${RST}"; done <<< "$FIX_OUT"
  fi

  # Auto-tag code fences with the correct language (python, go, ...).
  if LANG_OUT="$(python3 "$REPO_DIR/scripts/fix_codelang.py" 2>&1)" && [ -n "$LANG_OUT" ]; then
    while IFS= read -r line; do log "${YLW}lang: ${line}${RST}"; done <<< "$LANG_OUT"
  fi

  # Strip ChatGPT oai_citation references before they reach the repo.
  if CITE_OUT="$(python3 "$REPO_DIR/scripts/fix_chatgpt.py" 2>&1)" && [ -n "$CITE_OUT" ]; then
    while IFS= read -r line; do log "${YLW}cite: ${line}${RST}"; done <<< "$CITE_OUT"
  fi

  # Normalize block-math delimiters: \[ \] → $$ $$.
  if MATH_OUT="$(python3 "$REPO_DIR/scripts/fix_mathdelim.py" 2>&1)" && [ -n "$MATH_OUT" ]; then
    while IFS= read -r line; do log "${YLW}math: ${line}${RST}"; done <<< "$MATH_OUT"
  fi

  # Fix KaTeX-invalid sequences: \* \+ \= etc. inside math.
  if KATEX_OUT="$(python3 "$REPO_DIR/scripts/fix_katex.py" 2>&1)" && [ -n "$KATEX_OUT" ]; then
    while IFS= read -r line; do log "${YLW}katex: ${line}${RST}"; done <<< "$KATEX_OUT"
  fi

  _did_something=false

  # Commit any local changes (always safe to commit locally).
  if [ -n "$(git status --porcelain)" ]; then
    git add -A
    if ! git diff --cached --quiet; then
      MSG="$(build_commit_msg)"
      git commit -q -m "$MSG"
      log "${CYN}○ ${MSG}${RST}"
    else
      log "${YLW}· nothing to commit${RST}"
    fi
    _did_something=true
  fi

  # Push only after a local hugo build passes — catches render errors
  # (KaTeX, broken shortcodes, etc.) before they break GitHub Pages.
  # If hugo fails the commit stays local; the next cycle retries.
  if git log "origin/$BRANCH..HEAD" --oneline 2>/dev/null | grep -q .; then
    if HUGO_OUT="$(hugo --renderToMemory --gc 2>&1)"; then
      if PUSH_OUT="$(git push -q origin "$BRANCH" 2>&1)"; then
        log "${GRN}✓ pushed${RST}"
        # Wait for GitHub Pages deploy and report result + duration.
        _deploy_start=$(date +%s)
        log "${GRY}  waiting for deploy…${RST}"
        _run_id=""
        for _i in $(seq 1 12); do
          sleep 10
          _run_id=$(gh run list --repo tamnd/brain --branch "$BRANCH" \
            --event push --limit 1 --json databaseId,status \
            --jq '.[0] | select(.status != "completed") | .databaseId' 2>/dev/null || true)
          [ -n "$_run_id" ] && break
          # Also accept if already completed within this window.
          _run_id=$(gh run list --repo tamnd/brain --branch "$BRANCH" \
            --event push --limit 1 --json databaseId,status,conclusion,updatedAt \
            --jq '.[0] | select(.status == "completed") | .databaseId' 2>/dev/null || true)
          [ -n "$_run_id" ] && break
        done
        if [ -n "$_run_id" ]; then
          gh run watch "$_run_id" --exit-status &>/dev/null && _conclusion="success" || _conclusion="failure"
          _deploy_end=$(date +%s)
          _elapsed=$(( _deploy_end - _deploy_start ))
          _mins=$(( _elapsed / 60 )); _secs=$(( _elapsed % 60 ))
          if [ "$_conclusion" = "success" ]; then
            log "${GRN}✓ deployed in ${_mins}m${_secs}s${RST}"
          else
            log "${YLW}✗ deploy failed after ${_mins}m${_secs}s${RST}"
          fi
        else
          log "${YLW}· deploy run not found${RST}"
        fi
      else
        while IFS= read -r line; do log "${YLW}push: ${line}${RST}"; done <<< "$PUSH_OUT"
        log "${YLW}✗ push failed — commit held locally, retry next cycle${RST}"
      fi
    else
      while IFS= read -r line; do log "${YLW}hugo: ${line}${RST}"; done <<< "$HUGO_OUT"
      errfiles=$(printf '%s\n' "$HUGO_OUT" \
        | grep -oE 'see "[^"]+"' \
        | sed 's/^see "//; s/"$//; s|'"$REPO_DIR/"'||; s/:[0-9]*$//' \
        | sort -u)
      if [ -n "$errfiles" ]; then
        log "${YLW}fix these files:${RST}"
        while IFS= read -r f; do log "  ${YLW}→ $f${RST}"; done <<< "$errfiles"
      fi
      # Auto-fix: re-run KaTeX and math fixers, then retry hugo once.
      _katex_retry="$(python3 "$REPO_DIR/scripts/fix_katex.py" 2>&1)"
      _math_retry="$(python3 "$REPO_DIR/scripts/fix_mathdelim.py" 2>&1)"
      if [ -n "$_katex_retry" ] || [ -n "$_math_retry" ]; then
        [ -n "$_katex_retry" ] && log "${YLW}katex auto-fix: ${_katex_retry}${RST}"
        [ -n "$_math_retry"  ] && log "${YLW}math auto-fix:  ${_math_retry}${RST}"
        # Amend the last commit with the fixes applied.
        if [ -n "$(git status --porcelain)" ]; then
          git add -A
          git commit -q --amend --no-edit
          log "${YLW}· amended commit with auto-fixes${RST}"
        fi
        # Retry hugo.
        if HUGO_OUT2="$(hugo --renderToMemory --gc 2>&1)"; then
          if PUSH_OUT2="$(git push -q --force-with-lease origin "$BRANCH" 2>&1)"; then
            log "${GRN}✓ pushed after auto-fix${RST}"
          else
            log "${YLW}✗ push failed after auto-fix: ${PUSH_OUT2}${RST}"
          fi
        else
          log "${YLW}✗ hugo still failing after auto-fix — held locally${RST}"
          while IFS= read -r line; do log "${YLW}hugo: ${line}${RST}"; done <<< "$HUGO_OUT2"
        fi
      else
        log "${YLW}✗ hugo error — commit held locally, retry next cycle${RST}"
      fi
    fi
    _did_something=true
  fi

  if ! $_did_something; then
    log "${GRY}· nothing to commit${RST}"
  fi

  sleep "$INTERVAL"
done
