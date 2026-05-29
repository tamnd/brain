#!/usr/bin/env bash
# setup_repos.sh — create and initialize tamnd/brain-vi, brain-zh-cn, brain-ja
#
# Usage:
#   bash scripts/translate/setup_repos.sh             # create all three repos
#   bash scripts/translate/setup_repos.sh vi           # create only brain-vi
#   DRY_RUN=1 bash scripts/translate/setup_repos.sh   # preview without making changes
#
# Prerequisites:
#   - gh CLI (github.com/cli/gh) authenticated as tamnd
#   - git configured with ssh access to github.com

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN_REPO="$(cd "$SCRIPT_DIR/../.." && pwd)"
DRY_RUN="${DRY_RUN:-0}"
FILTER="${1:-all}"

HUGO_BRAINY_VERSION="v0.3.5"
HUGO_BRAINY_HASH="h1:gMMA+zI+UmtSjXfK9hxWCaASUFXX8bQPNfKyBFkE1Hk="
HUGO_BRAINY_MOD_HASH="h1:F1gqu18e6d7P7RCVp3zINvBwTiBwKX2WciQfyjgs6vo="
HUGO_VERSION="0.147.9"

run() {
    if [[ "$DRY_RUN" == "1" ]]; then
        echo "[dry-run] $*"
    else
        "$@"
    fi
}

# ── Language definitions ──────────────────────────────────────────────────────

declare -A REPO_NAME LANG_CODE BASE_URL CF_PROJECT TITLE DESCRIPTION INDEX_BODY

REPO_NAME[vi]="brain-vi"
LANG_CODE[vi]="vi"
BASE_URL[vi]="https://brain-vi.tamnd.com/"
CF_PROJECT[vi]="brain-vi"
TITLE[vi]="brain (Tiếng Việt)"
DESCRIPTION[vi]="Ghi chú cá nhân của tamnd"
INDEX_BODY[vi]="Bản dịch tự động của [tamnd's brain](https://brain.tamnd.com).\nNội dung đang được cập nhật dần dần."

REPO_NAME[zh_CN]="brain-zh-cn"
LANG_CODE[zh_CN]="zh-CN"
BASE_URL[zh_CN]="https://brain-zh-cn.tamnd.com/"
CF_PROJECT[zh_CN]="brain-zh-cn"
TITLE[zh_CN]="brain (中文)"
DESCRIPTION[zh_CN]="tamnd 的个人知识库"
INDEX_BODY[zh_CN]="[tamnd's brain](https://brain.tamnd.com) 的自动翻译版本。\n内容正在逐步更新中。"

REPO_NAME[ja]="brain-ja"
LANG_CODE[ja]="ja"
BASE_URL[ja]="https://brain-ja.tamnd.com/"
CF_PROJECT[ja]="brain-ja"
TITLE[ja]="brain (日本語)"
DESCRIPTION[ja]="tamnd の個人知識ベース"
INDEX_BODY[ja]="[tamnd's brain](https://brain.tamnd.com) の自動翻訳版です。\nコンテンツは順次更新されています。"

LANGS=("vi" "zh_CN" "ja")

# ── Helper: create one repo ──────────────────────────────────────────────────

create_repo() {
    local lang="$1"
    local repo="${REPO_NAME[$lang]}"
    local base_url="${BASE_URL[$lang]}"
    local cf_project="${CF_PROJECT[$lang]}"
    local title="${TITLE[$lang]}"
    local desc="${DESCRIPTION[$lang]}"
    local lc="${LANG_CODE[$lang]}"
    local index_body="${INDEX_BODY[$lang]}"

    echo ""
    echo "══════════════════════════════════════════════"
    echo "  Setting up tamnd/$repo"
    echo "══════════════════════════════════════════════"

    local tmpdir
    tmpdir="$(mktemp -d)"
    trap "rm -rf '$tmpdir'" RETURN

    # ── Create GitHub repo ──────────────────────────────────────────────
    if gh repo view "tamnd/$repo" &>/dev/null; then
        echo "  GitHub repo tamnd/$repo already exists — skipping creation"
    else
        run gh repo create "tamnd/$repo" \
            --public \
            --description "$title — auto-translated from tamnd/brain" \
            --clone=false
        echo "  Created: tamnd/$repo"
    fi

    # ── Init local dir ──────────────────────────────────────────────────
    pushd "$tmpdir" > /dev/null
    run git init -b main
    run git remote add origin "git@github.com:tamnd/$repo.git"

    # hugo.toml
    cat > hugo.toml << HUGO
baseURL = "${base_url}"
title = "${title}"

enableGitInfo = true
enableRobotsTXT = true
enableEmoji = true

[frontmatter]
  date    = ["date", "publishDate"]
  lastmod = ["lastmod", "date", "publishDate"]

defaultContentLanguage = "${lc}"
defaultContentLanguageInSubdir = false

[module]
  [[module.imports]]
    path = "github.com/tamnd/hugo-brainy"

[languages]
  [languages.${lc//-/_}]
    label = "${title}"
    locale = "${lc}"
    contentDir = "content"
    weight = 1

[markup]
  [markup.highlight]
    noClasses = false
  [markup.goldmark.renderer]
    unsafe = true
  [markup.goldmark.extensions.passthrough]
    enable = true
    [markup.goldmark.extensions.passthrough.delimiters]
      block  = [["$$", "$$"], ["\\\\[", "\\\\]"]]
      inline = [["$", "$"],   ["\\\\(", "\\\\)"]]

[params]
  description = "${desc}"
  math = true

  [params.navbar]
    displayTitle = true
    displayLogo = false
    width = "full"

  [params.theme]
    default = "system"
    displayToggle = true

  [params.search]
    enable = true
    type = "flexsearch"
    [params.search.flexsearch]
      index = "summary"

  [params.editURL]
    enable = false

  [params.footer]
    enable = true
    displayCopyright = false
    displayPoweredBy = false
HUGO

    # go.mod
    cat > go.mod << GOMOD
module github.com/tamnd/${repo}

go 1.23.0

require github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION} // indirect
GOMOD

    # go.sum (copy exact hashes from brain)
    cat > go.sum << GOSUM
github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION} ${HUGO_BRAINY_HASH}
github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION}/go.mod ${HUGO_BRAINY_MOD_HASH}
GOSUM

    # .gitignore
    cat > .gitignore << 'GITIGNORE'
public/
resources/_gen/
.hugo_build.lock
GITIGNORE

    # Initial content
    mkdir -p content
    cat > content/_index.md << IDXMD
---
title: "${title}"
tags: ["mathematics", "programming", "knowledge"]
type: docs
cascade:
  type: docs
date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

$(echo -e "$index_body")
IDXMD

    # GitHub Actions deploy workflow
    mkdir -p .github/workflows
    cat > .github/workflows/deploy.yml << WORKFLOW
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  BASE_URL: "${base_url}"
  CF_PROJECT: "${cf_project}"
  HUGO_VERSION: "${HUGO_VERSION}"

permissions:
  contents: read
  deployments: write

concurrency:
  group: cloudflare-pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6.0.2
        with:
          fetch-depth: 0

      - name: Setup Go
        uses: actions/setup-go@v6.4.0
        with:
          go-version: "1.23"
          cache: false

      - name: Cache Hugo modules
        uses: actions/cache@v5.0.5
        with:
          path: /home/runner/.cache/hugo_cache
          key: hugo-mods-\${{ runner.os }}-\${{ hashFiles('go.sum') }}
          restore-keys: hugo-mods-\${{ runner.os }}-

      - name: Install Hugo extended
        run: |
          curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v\${HUGO_VERSION}/hugo_extended_\${HUGO_VERSION}_linux-amd64.tar.gz" \\
            | tar -xz -C /usr/local/bin hugo

      - name: Build site
        env:
          HUGO_CACHEDIR: /home/runner/.cache/hugo_cache
        run: hugo --baseURL "\${{ env.BASE_URL }}" --minify

      - name: Remove oversized files
        run: find public -size +24M -print -delete

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v4.0.0
        with:
          apiToken: \${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: \${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy public --project-name=\${{ env.CF_PROJECT }} --branch=main
WORKFLOW

    # Commit and push
    run git add --all
    run git commit -m "chore: initial Hugo site for ${title}

Auto-translated from tamnd/brain.
Theme: github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION}
Deploy: Cloudflare Pages -> ${base_url}"

    # Push (may fail if repo was just created — retry once)
    if ! run git push -u origin main 2>/dev/null; then
        echo "  Retrying push..."
        sleep 3
        run git push -u origin main
    fi

    popd > /dev/null
    echo "  Pushed: tamnd/$repo"
    echo ""
    echo "  ⚡ Next steps for tamnd/$repo:"
    echo "     1. Add secrets in https://github.com/tamnd/$repo/settings/secrets/actions:"
    echo "        CLOUDFLARE_API_TOKEN"
    echo "        CLOUDFLARE_ACCOUNT_ID"
    echo "     2. Create Cloudflare Pages project '$cf_project':"
    echo "        wrangler pages project create $cf_project"
    echo "     3. Add custom domain in Cloudflare Pages dashboard:"
    echo "        ${base_url%/} -> $cf_project"
}

# ── Main ─────────────────────────────────────────────────────────────────────

echo "brain-translate: setup_repos.sh"
echo "Source repo: $BRAIN_REPO"
[[ "$DRY_RUN" == "1" ]] && echo "DRY RUN — no changes will be made"

for lang in "${LANGS[@]}"; do
    if [[ "$FILTER" == "all" || "$FILTER" == "$lang" ]]; then
        create_repo "$lang"
    fi
done

echo ""
echo "Done."
echo ""
echo "After adding secrets, trigger the first deploy with:"
for lang in "${LANGS[@]}"; do
    if [[ "$FILTER" == "all" || "$FILTER" == "$lang" ]]; then
        echo "  gh workflow run deploy.yml --repo tamnd/${REPO_NAME[$lang]}"
    fi
done
