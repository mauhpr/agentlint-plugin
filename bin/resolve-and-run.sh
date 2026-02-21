#!/bin/sh
# Resolve the agentlint binary across common install methods.
# Claude Code runs hooks via /bin/sh with a minimal PATH, so we
# probe well-known locations before falling back to python -m.

set -e

if command -v agentlint >/dev/null 2>&1; then
  exec agentlint "$@"
elif [ -x "$HOME/.local/bin/agentlint" ]; then
  exec "$HOME/.local/bin/agentlint" "$@"
elif [ -x "$HOME/.local/share/uv/tools/agentlint/bin/agentlint" ]; then
  exec "$HOME/.local/share/uv/tools/agentlint/bin/agentlint" "$@"
elif python3 -m agentlint --version >/dev/null 2>&1; then
  exec python3 -m agentlint "$@"
elif python -m agentlint --version >/dev/null 2>&1; then
  exec python -m agentlint "$@"
else
  echo "agentlint: command not found. Install with: pip install agentlint" >&2
  exit 127
fi
