#!/bin/sh
# Resolve the agentlint binary across common install methods.
# Claude Code runs hooks via /bin/sh with a minimal PATH, so we
# probe well-known locations before falling back to bare `agentlint`.

set -e

if command -v agentlint >/dev/null 2>&1; then
  AGENTLINT=agentlint
elif [ -x "$HOME/.local/bin/agentlint" ]; then
  AGENTLINT="$HOME/.local/bin/agentlint"
elif [ -x "$HOME/.local/share/uv/tools/agentlint/bin/agentlint" ]; then
  AGENTLINT="$HOME/.local/share/uv/tools/agentlint/bin/agentlint"
elif python3 -m agentlint --version >/dev/null 2>&1; then
  AGENTLINT="python3 -m agentlint"
elif python -m agentlint --version >/dev/null 2>&1; then
  AGENTLINT="python -m agentlint"
else
  AGENTLINT=agentlint
fi

exec $AGENTLINT "$@"
