#!/bin/bash
# Publish gallery changes to GitHub (called by Update Gallery.command).

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo ""
echo "Step 4/4: Publishing to GitHub..."

if ! command -v git >/dev/null 2>&1; then
  echo ""
  echo "Error: git is not installed."
  echo "Install Xcode Command Line Tools: xcode-select --install"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo ""
  echo "Error: this folder is not a git repository."
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "main" ]; then
  echo ""
  echo "Warning: current branch is '$BRANCH', not 'main'."
  echo "Push target will still be origin main."
fi

git add images/

if git diff --cached --quiet; then
  echo ""
  echo "No gallery changes to commit."
  echo "The site is already up to date on GitHub."
  exit 0
fi

echo ""
echo "Changes to publish:"
git diff --cached --stat

COMMIT_MSG="Update gallery ($(date '+%Y-%m-%d %H:%M'))."
if ! git commit -m "$COMMIT_MSG"; then
  echo ""
  echo "Error: git commit failed."
  exit 1
fi

COMMIT_HASH="$(git rev-parse HEAD)"
SHORT_HASH="$(git rev-parse --short HEAD)"
echo ""
echo "Committed: $COMMIT_HASH"

PUSH_OUTPUT="$(git push origin main 2>&1)"
PUSH_STATUS=$?

if [ $PUSH_STATUS -ne 0 ]; then
  echo ""
  echo "Error: git push failed."
  echo ""
  echo "$PUSH_OUTPUT"
  echo ""
  echo "Common causes:"
  echo "  - GitHub login expired"
  echo "    → Terminal에서: gh auth login"
  echo "    → 또는 GitHub Desktop으로 한 번 로그인"
  echo "  - 인ternet 연결 문제"
  echo "  - 원격 저장소 권한 없음"
  exit 1
fi

echo ""
echo "GitHub push successful."
echo "Commit hash: $COMMIT_HASH ($SHORT_HASH)"
echo "Branch: main"
echo ""
echo "Cloudflare Pages will deploy automatically in about 1-2 minutes."
echo "Site: https://kimjaehyunv.com"

exit 0
