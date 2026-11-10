#!/usr/bin/env bash
# ==============================================================================
# Script: install_sidecar.sh
# Purpose: Installs the 4x/day scheduled automation sidecar into Antigravity config
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$HOME/.gemini/config/sidecars/job-hunter-agent-for-xiao"

echo ""
echo "================================================================="
echo "  ⏰ Installing 'Job Hunter Agent for Xiao' 4x/Day Sidecar"
echo "================================================================="
echo ""

mkdir -p "$TARGET_DIR"
cp "$PROJECT_DIR/sidecar.json" "$TARGET_DIR/sidecar.json"

echo "✅ Installed sidecar.json to: $TARGET_DIR/sidecar.json"
echo ""
echo "👉 You can now enable 'Job Hunter Agent for Xiao' in your"
echo "   Automations dashboard: [Open Automations Dashboard](sidecar://dashboard)"
echo ""
