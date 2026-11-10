#!/usr/bin/env bash
# ==============================================================================
# Script: publish_to_github.sh
# Purpose: Initialize local git repository and push to GitHub repository
# Required Repo Name: job-hunter-agent-for-xiao
# ==============================================================================

set -e

REPO_NAME="job-hunter-agent-for-xiao"

echo ""
echo "================================================================="
echo "  🐙 Publishing 'Job Hunter Agent for Xiao' to GitHub"
echo "  Target Repository Name: $REPO_NAME"
echo "================================================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Ensure .gitignore exists
if [ ! -f .gitignore ]; then
  cat << 'EOF' > .gitignore
# Dependencies & caches
node_modules/
.vercel/
.env.local
.env*.local

# System & OS
.DS_Store
Thumbs.db

# Logs
npm-debug.log*
yarn-debug.log*
EOF
  echo "📄 Created .gitignore"
fi

# Check if git is available
if ! command -v git &> /dev/null; then
  echo "⚠️  Git is not yet installed or Xcode developer tools are pending."
  echo "👉 On macOS, run: xcode-select --install"
  exit 1
fi

# Initialize git if needed
if [ ! -d .git ]; then
  echo "📦 Initializing local git repository for $REPO_NAME..."
  git init
  git branch -M main
fi

# Add all project files
echo "📝 Staging files..."
git add .

# Commit
git commit -m "feat: complete Job Hunter Agent for Xiao dashboard, 4x/day scheduler, and recruitment suite" || echo "No changes to commit."

# Remote repository handling
echo ""
echo "🔗 Current remotes:"
git remote -v || true
echo ""

if ! git remote | grep -q "origin"; then
  echo "👉 Enter your GitHub username (or full repo URL):"
  read -r GH_INPUT

  if [[ "$GH_INPUT" =~ ^https?:// ]] || [[ "$GH_INPUT" =~ ^git@ ]]; then
    REPO_URL="$GH_INPUT"
  elif [ -n "$GH_INPUT" ]; then
    REPO_URL="https://github.com/$GH_INPUT/$REPO_NAME.git"
  else
    REPO_URL=""
  fi

  if [ -n "$REPO_URL" ]; then
    git remote add origin "$REPO_URL"
    echo "✅ Remote 'origin' added: $REPO_URL"
  else
    echo "⚠️ No URL provided. You can run manually: git remote add origin https://github.com/<username>/$REPO_NAME.git"
    exit 0
  fi
fi

echo "🚀 Pushing main branch to GitHub ($REPO_NAME)..."
git push -u origin main

echo ""
echo "================================================================="
echo "  🎉 Successfully published to GitHub: $REPO_NAME!"
echo "================================================================="
echo ""
