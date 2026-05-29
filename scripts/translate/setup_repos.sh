#!/usr/bin/env bash
# setup_repos.sh — create and initialize tamnd/brain-vi, brain-zh-cn, brain-ja
#
# Usage:
#   bash scripts/translate/setup_repos.sh             # create all three repos
#   bash scripts/translate/setup_repos.sh vi           # create only brain-vi
#   DRY_RUN=1 bash scripts/translate/setup_repos.sh   # preview without changes
#
# Prerequisites: gh CLI authenticated as tamnd, git with ssh access

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

# ── Single-repo creation function ────────────────────────────────────────────

create_repo() {
    local lang="$1"
    local repo="$2"
    local lc="$3"
    local base_url="$4"
    local cf_project="$5"
    local title="$6"
    local desc="$7"
    local index_body="$8"

    echo ""
    echo "══════════════════════════════════════════════"
    echo "  Setting up tamnd/$repo  ($lang)"
    echo "══════════════════════════════════════════════"

    # ── Create GitHub repo ──────────────────────────────────────────────
    if gh repo view "tamnd/$repo" &>/dev/null 2>&1; then
        echo "  GitHub repo tamnd/$repo already exists — skipping creation"
    else
        run gh repo create "tamnd/$repo" \
            --public \
            --description "$title — auto-translated from tamnd/brain" \
            --clone=false
        echo "  Created: tamnd/$repo"
    fi

    if [[ "$DRY_RUN" == "1" ]]; then
        echo "  [dry-run] would init local repo and push"
        return
    fi

    local tmpdir
    tmpdir="$(mktemp -d)"
    # shellcheck disable=SC2064
    trap "rm -rf '$tmpdir'" RETURN

    pushd "$tmpdir" > /dev/null

    git init -b main
    git remote add origin "git@github.com:tamnd/$repo.git"

    # ── hugo.toml ──────────────────────────────────────────────────────
    # Note: lc may contain hyphen (zh-CN) — Hugo lang key uses underscore
    local lc_key="${lc//-/_}"
    cat > hugo.toml << EOF
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
  [languages.${lc_key}]
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
      block  = [["\\$\\$", "\\$\\$"], ["\\\\[", "\\\\]"]]
      inline = [["\\$", "\\$"],       ["\\\\(", "\\\\)"]]

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
EOF

    # ── go.mod ─────────────────────────────────────────────────────────
    cat > go.mod << EOF
module github.com/tamnd/${repo}

go 1.23.0

require github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION} // indirect
EOF

    # ── go.sum ─────────────────────────────────────────────────────────
    cat > go.sum << EOF
github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION} ${HUGO_BRAINY_HASH}
github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION}/go.mod ${HUGO_BRAINY_MOD_HASH}
EOF

    # ── .gitignore ─────────────────────────────────────────────────────
    cat > .gitignore << 'EOF'
public/
resources/_gen/
.hugo_build.lock
EOF

    # ── Initial content/_index.md ──────────────────────────────────────
    mkdir -p content
    local now
    now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    cat > content/_index.md << EOF
---
title: "${title}"
tags: ["mathematics", "programming", "knowledge"]
type: docs
cascade:
  type: docs
date: ${now}
---

${index_body}
EOF

    # ── GitHub Actions deploy workflow ─────────────────────────────────
    mkdir -p .github/workflows
    # Use printf to avoid shell expanding $ in workflow YAML
    printf '%s\n' \
'name: Deploy' \
'' \
'on:' \
'  push:' \
'    branches: [main]' \
'  workflow_dispatch:' \
'' \
'env:' \
"  BASE_URL: \"${base_url}\"" \
"  CF_PROJECT: \"${cf_project}\"" \
"  HUGO_VERSION: \"${HUGO_VERSION}\"" \
'' \
'permissions:' \
'  contents: read' \
'  deployments: write' \
'' \
'concurrency:' \
'  group: cloudflare-pages' \
'  cancel-in-progress: true' \
'' \
'jobs:' \
'  deploy:' \
'    runs-on: ubuntu-latest' \
'    steps:' \
'      - uses: actions/checkout@v6.0.2' \
'        with:' \
'          fetch-depth: 0' \
'' \
'      - name: Setup Go' \
'        uses: actions/setup-go@v6.4.0' \
'        with:' \
'          go-version: "1.23"' \
'          cache: false' \
'' \
'      - name: Cache Hugo modules' \
'        uses: actions/cache@v5.0.5' \
'        with:' \
'          path: /home/runner/.cache/hugo_cache' \
'          key: hugo-mods-${{ runner.os }}-${{ hashFiles('"'"'go.sum'"'"') }}' \
'          restore-keys: hugo-mods-${{ runner.os }}-' \
'' \
'      - name: Install Hugo extended' \
'        run: |' \
'          curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \' \
'            | tar -xz -C /usr/local/bin hugo' \
'' \
'      - name: Build site' \
'        env:' \
'          HUGO_CACHEDIR: /home/runner/.cache/hugo_cache' \
'        run: hugo --baseURL "${{ env.BASE_URL }}" --minify' \
'' \
'      - name: Remove oversized files' \
'        run: find public -size +24M -print -delete' \
'' \
'      - name: Deploy to Cloudflare Pages' \
'        uses: cloudflare/wrangler-action@v4.0.0' \
'        with:' \
"          apiToken: \${{ secrets.CLOUDFLARE_API_TOKEN }}" \
"          accountId: \${{ secrets.CLOUDFLARE_ACCOUNT_ID }}" \
"          command: pages deploy public --project-name=\${{ env.CF_PROJECT }} --branch=main" \
    > .github/workflows/deploy.yml

    # ── Commit and push ────────────────────────────────────────────────
    git add --all
    git commit -m "chore: initial Hugo site for ${title}

Auto-translated from tamnd/brain.
Theme: github.com/tamnd/hugo-brainy ${HUGO_BRAINY_VERSION}
Deploy: Cloudflare Pages -> ${base_url}"

    if ! git push -u origin main 2>/dev/null; then
        echo "  Retrying push in 3s..."
        sleep 3
        git push -u origin main
    fi

    popd > /dev/null
    echo "  Pushed: tamnd/$repo"

    echo ""
    echo "  Next steps for tamnd/$repo:"
    echo "  1. Add GitHub secrets (Settings → Secrets → Actions):"
    echo "       CLOUDFLARE_API_TOKEN"
    echo "       CLOUDFLARE_ACCOUNT_ID"
    echo "  2. Create Cloudflare Pages project:"
    echo "       wrangler pages project create ${cf_project}"
    echo "  3. Add custom domain in Cloudflare Pages dashboard:"
    echo "       ${base_url%/}  →  ${cf_project}"
}

# ── Main ─────────────────────────────────────────────────────────────────────

echo "brain-translate: setup_repos.sh"
echo "Source repo: $BRAIN_REPO"
[[ "$DRY_RUN" == "1" ]] && echo "DRY RUN — no changes will be made"

if [[ "$FILTER" == "all" || "$FILTER" == "vi" ]]; then
    create_repo "vi" "brain-vi" "vi" \
        "https://brain-vi.tamnd.com/" "brain-vi" \
        "brain (Tiếng Việt)" "Ghi chú cá nhân của tamnd" \
        "Bản dịch tự động của [tamnd's brain](https://brain.tamnd.com).\nNội dung đang được cập nhật dần dần."
fi

if [[ "$FILTER" == "all" || "$FILTER" == "zh_CN" ]]; then
    create_repo "zh_CN" "brain-zh-cn" "zh-CN" \
        "https://brain-zh-cn.tamnd.com/" "brain-zh-cn" \
        "brain (中文)" "tamnd 的个人知识库" \
        "[tamnd's brain](https://brain.tamnd.com) 的自动翻译版本。\n内容正在逐步更新中。"
fi

if [[ "$FILTER" == "all" || "$FILTER" == "ja" ]]; then
    create_repo "ja" "brain-ja" "ja" \
        "https://brain-ja.tamnd.com/" "brain-ja" \
        "brain (日本語)" "tamnd の個人知識ベース" \
        "[tamnd's brain](https://brain.tamnd.com) の自動翻訳版です。\nコンテンツは順次更新されています。"
fi

echo ""
echo "Done."
echo ""
echo "After adding secrets, trigger the first deploy:"
if [[ "$FILTER" == "all" || "$FILTER" == "vi" ]];    then echo "  gh workflow run deploy.yml --repo tamnd/brain-vi"; fi
if [[ "$FILTER" == "all" || "$FILTER" == "zh_CN" ]]; then echo "  gh workflow run deploy.yml --repo tamnd/brain-zh-cn"; fi
if [[ "$FILTER" == "all" || "$FILTER" == "ja" ]];    then echo "  gh workflow run deploy.yml --repo tamnd/brain-ja"; fi
