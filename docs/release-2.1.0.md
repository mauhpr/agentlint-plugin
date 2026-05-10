# AgentLint Plugin 2.1.0 Release Plan

Goal: release the Claude Code marketplace plugin in lockstep with `agentlint` 2.1.0.

## Release Scope

- Keep this repo clearly positioned as the Claude Code marketplace wrapper.
- Point non-Claude users to the multi-agent `agentlint` package and setup docs.
- Verify binary resolution works for PATH, pipx/user installs, uv tool installs, and `python -m agentlint`.
- Verify plugin hooks call the same 2.1.0 CLI behavior used by other platforms.

## Pre-Release Checklist

1. Update versions after AgentLint 2.1.0 is ready:

   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`

2. Validate plugin metadata:

   ```bash
   python3 -m json.tool .claude-plugin/plugin.json
   python3 -m json.tool .claude-plugin/marketplace.json
   python3 -m json.tool hooks/hooks.json
   ```

3. Validate resolver shell syntax:

   ```bash
   sh -n bin/resolve-and-run.sh
   test -x bin/resolve-and-run.sh
   ```

4. Run the fake-binary smoke:

   ```bash
   tmpbin=$(mktemp -d)
   printf '#!/bin/sh\nprintf "%%s\\n" "$@"\n' > "$tmpbin/agentlint"
   chmod +x "$tmpbin/agentlint"
   PATH="$tmpbin:$PATH" HOME=$(mktemp -d) bin/resolve-and-run.sh check --event PreToolUse
   ```

5. Confirm README says this is the Claude Code wrapper and links other platforms to the main repo.

## Release Notes Draft

AgentLint Plugin 2.1.0 is the Claude Code marketplace companion for AgentLint 2.1.0. It keeps native Claude Code hooks easy to install while the core package expands the broader multi-agent setup story for Cursor, Codex, Gemini, Continue, Kimi, Grok, OpenAI Agents, MCP, and generic integrations.

## Do Not Release Until

- `agentlint` 2.1.0 is tested and ready for PyPI.
- Plugin metadata is bumped to 2.1.0.
- JSON validation and resolver smoke pass.
