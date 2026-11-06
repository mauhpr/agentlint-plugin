#!/bin/sh
# Resolve the agentlint binary across common install methods.
# Claude Code runs hooks via /bin/sh with a minimal PATH, so we
# probe well-known locations before falling back to python -m.

set -e

REQUESTED_COMMAND=${1-}

check_observer_support() {
  # A help probe never receives the native event's stdin or makes a decision.
  # Policy commands always retain their original execution and exit behavior.
  if [ "$REQUESTED_COMMAND" = observe ] && ! "$@" observe --help </dev/null >/dev/null 2>&1; then
    echo "agentlint: activity visibility unknown; upgrade AgentLint to 2.11.0 or newer for passive observation. Existing policy checks remain active." >&2
    exit 0
  fi
}

if command -v agentlint >/dev/null 2>&1; then
  check_observer_support agentlint
  exec agentlint "$@"
elif [ -x "$HOME/.local/bin/agentlint" ]; then
  check_observer_support "$HOME/.local/bin/agentlint"
  exec "$HOME/.local/bin/agentlint" "$@"
elif [ -x "$HOME/.local/share/uv/tools/agentlint/bin/agentlint" ]; then
  check_observer_support "$HOME/.local/share/uv/tools/agentlint/bin/agentlint"
  exec "$HOME/.local/share/uv/tools/agentlint/bin/agentlint" "$@"
else
  # Probe the Python sysconfig scripts dir (where pip puts console_scripts).
  # Covers Framework installs like /Library/Frameworks/Python.framework/.
  SCRIPTS_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_path('scripts'))" </dev/null 2>/dev/null) || SCRIPTS_DIR=''
  if [ -n "$SCRIPTS_DIR" ] && [ -x "$SCRIPTS_DIR/agentlint" ]; then
    check_observer_support "$SCRIPTS_DIR/agentlint"
    exec "$SCRIPTS_DIR/agentlint" "$@"
  elif python3 -m agentlint --help </dev/null >/dev/null 2>&1; then
    check_observer_support python3 -m agentlint
    exec python3 -m agentlint "$@"
  elif python -m agentlint --help </dev/null >/dev/null 2>&1; then
    check_observer_support python -m agentlint
    exec python -m agentlint "$@"
  else
    echo "agentlint: command not found. Install with: pip install agentlint" >&2
    exit 127
  fi
fi
