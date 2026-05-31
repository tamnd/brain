#!/usr/bin/env bash
# Generate missing HSK vocabulary pages using chatgpt-tool
# Usage: ./scripts/generate_vocab_pages.sh [level]
# If level is given (4-9), only process that level. Otherwise process all.
#
# Each missing word is extracted from hsk/N/vocabulary.md and a full
# vocabulary page is generated via chatgpt-tool and written to
# hsk/N/vocabulary/<word>.md

set -euo pipefail

BRAIN="$(cd "$(dirname "$0")/.." && pwd)/content/en/languages/chinese/hsk"
CHATGPT_TOOL="$HOME/bin/chatgpt-tool"
FILTER_LEVEL="${1:-}"

LEVEL_INFO=(
  [4]="B1|hsk-4"
  [5]="B2|hsk-5"
  [6]="C1|hsk-6"
  [7]="C1+|hsk-7"
  [8]="C2|hsk-8"
  [9]="C2+|hsk-9"
)

CEFR_TAG=(
  [4]="b1"
  [5]="b2"
  [6]="c1"
  [7]="c1"
  [8]="c2"
  [9]="c2"
)

CEFR_LABEL=(
  [4]="B1"
  [5]="B2"
  [6]="C1"
  [7]="C1 academic"
  [8]="C2"
  [9]="C2 classical"
)

generate_page() {
  local level="$1"
  local chinese="$2"
  local pinyin="$3"
  local english="$4"
  local pos="$5"
  local outfile="$BRAIN/$level/vocabulary/$chinese.md"
  local cefr="${CEFR_LABEL[$level]}"
  local tag="${CEFR_TAG[$level]}"

  if [ -f "$outfile" ]; then
    echo "  [skip] $chinese already exists"
    return 0
  fi

  echo "  [gen] HSK $level: $chinese ($pinyin) — $english"

  local prompt="Write a complete Chinese vocabulary reference page for the word $chinese ($pinyin), meaning \"$english\", part-of-speech: $pos, at HSK $level / $cefr level.

Output ONLY the Hugo markdown content with this exact structure:

---
title: \"$chinese ($pinyin) — $english\"
description: \"HSK $level | $pos | $english\"
tags: [\"hsk-$level\", \"vocabulary\", \"$tag\"]
date: 2026-05-31T00:00:00+07:00
---

## $chinese ($pinyin)

[One paragraph introduction: what the word means, its register/tone, how commonly it's used, what makes it worth knowing at this level]

## Meanings

1. **[$pos]** [primary meaning with nuance]
2. (if applicable) **[$pos2]** [secondary meaning]

## Example Sentences

[6 example sentences. Each on its own lines:
**Chinese sentence in bold**
Pinyin romanization in italic
English translation]

## Collocations

| Collocation | Meaning |
|-------------|---------|
[4-6 rows of common collocations]

## Usage Notes

[1-2 paragraphs: register, common mistakes, how to distinguish from similar words, formal vs informal contexts]

## Memory Hook

[One sentence mnemonic or character breakdown to remember the word]"

  local content
  content=$("$CHATGPT_TOOL" search "$prompt" --no-verbose 2>/dev/null) || {
    echo "  [error] chatgpt-tool failed for $chinese"
    return 1
  }

  if [ -z "$content" ]; then
    echo "  [error] empty response for $chinese"
    return 1
  fi

  # Strip any leading/trailing prose that isn't the markdown
  # The response should start with --- frontmatter
  echo "$content" > "$outfile"
  echo "  [done] wrote $outfile"
}

# Process each level
for level in 4 5 6 7 8 9; do
  if [ -n "$FILTER_LEVEL" ] && [ "$level" != "$FILTER_LEVEL" ]; then
    continue
  fi

  vocabmd="$BRAIN/$level/vocabulary.md"
  vocab_dir="$BRAIN/$level/vocabulary"

  if [ ! -f "$vocabmd" ]; then
    echo "Skipping HSK $level: no vocabulary.md"
    continue
  fi

  # Count missing
  total=0
  missing=0
  while IFS='|' read -r _ chinese pinyin english pos _; do
    chinese=$(echo "$chinese" | sed 's/^ *//;s/ *$//')
    [ -z "$chinese" ] && continue
    total=$((total + 1))
    [ ! -f "$vocab_dir/$chinese.md" ] && missing=$((missing + 1))
  done < <(grep "^|" "$vocabmd" | grep -v "^| Word\|^|---\|^| Chinese\|^| HSK\|^| \*\*")

  echo ""
  echo "=== HSK $level: $missing/$total words need pages ==="

  if [ "$missing" -eq 0 ]; then
    echo "  All pages exist, skipping."
    continue
  fi

  # Generate missing pages
  count=0
  while IFS='|' read -r _ chinese pinyin english pos _; do
    chinese=$(echo "$chinese" | sed 's/^ *//;s/ *$//')
    pinyin=$(echo "$pinyin" | sed 's/^ *//;s/ *$//')
    english=$(echo "$english" | sed 's/^ *//;s/ *$//')
    pos=$(echo "$pos" | sed 's/^ *//;s/ *$//')
    [ -z "$chinese" ] && continue
    [ -f "$vocab_dir/$chinese.md" ] && continue

    generate_page "$level" "$chinese" "$pinyin" "$english" "$pos"
    count=$((count + 1))

    # Brief pause to avoid rate limiting
    sleep 2
  done < <(grep "^|" "$vocabmd" | grep -v "^| Word\|^|---\|^| Chinese\|^| HSK\|^| \*\*")

  echo "  Generated $count pages for HSK $level"
done

echo ""
echo "Done."
