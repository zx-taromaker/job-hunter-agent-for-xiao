#!/usr/bin/env bash
# ==============================================================================
# Script: deploy_vercel.sh
# Purpose: One-click live deployment of Job Hunter Agent for Xiao to Vercel
# Project Name: job-hunter-agent-for-xiao
# ==============================================================================

set -e

PROJECT_NAME="job-hunter-agent-for-xiao"

echo ""
echo "================================================================="
echo "  🚀 Deploying 'Job Hunter Agent for Xiao' ($PROJECT_NAME) to Vercel"
echo "================================================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "📍 Working directory: $PROJECT_DIR"
echo "🔍 Checking Vercel CLI..."

if command -v vercel &> /dev/null; then
  VERCEL_CMD="vercel"
elif command -v npx &> /dev/null; then
  VERCEL_CMD="npx vercel"
else
  echo "⚠️  Vercel CLI is not installed globally."
  echo "👉 You can install it via: npm i -g vercel"
  echo "    Or simply run with Node.js / npx."
  exit 1
fi

echo "✨ Deploying $PROJECT_NAME with $VERCEL_CMD..."
echo "👉 Follow the interactive prompts (Project name: $PROJECT_NAME):"
echo ""

# Deploy to production
$VERCEL_CMD --prod

echo ""
echo "================================================================="
echo "  ✅ Live Deployment Complete!"
echo "  'Job Hunter Agent for Xiao' is now live on Vercel."
echo "================================================================="
echo ""
