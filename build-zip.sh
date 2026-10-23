#!/usr/bin/env bash
# Gera dist/google-ads.zip para enviar ao app do Claude.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/google-ads.zip
zip -rq dist/google-ads.zip .claude-plugin .mcp.json server skills README.md LICENSE -x '*/__pycache__/*' '*.DS_Store'
echo "dist/google-ads.zip"
