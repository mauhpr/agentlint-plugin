# AgentLint for Claude Code

Claude Code marketplace plugin for [AgentLint](https://github.com/mauhpr/agentlint):
guardrails that check every file write, edit and shell command your agent makes,
and block the dangerous ones (secrets, force-pushes to `main`, destructive
commands, CI/CD edits, risky cloud operations) before they happen.

This repository only packages AgentLint for Claude Code: hook definitions, a
binary resolver, three agents and two slash commands. The rules, configuration
and documentation live in the [main repository](https://github.com/mauhpr/agentlint).
For other agents (Codex, Cursor, Gemini, ...) use the Python package directly.

## Install

1. Install the AgentLint package (Python 3.11+):

   ```bash
   pipx install agentlint        # or: uv tool install agentlint / pip install agentlint
   ```

2. Add the plugin:

   ```bash
   claude plugin marketplace add mauhpr/agentlint-plugin
   claude plugin install agentlint@agentlint
   ```

3. Restart Claude Code, make any tool call, and check that hooks are reaching
   AgentLint:

   ```bash
   agentlint status
   ```

   Look for `claude ... observed: <time> ago`.

Use the plugin **or** `agentlint setup claude`, not both — both install the same
hooks, and every call would be checked twice.

To try a local checkout: `claude --plugin-dir /path/to/agentlint-plugin`.

## Version compatibility

For this 2.9.1 plugin release, use AgentLint 2.9.1 or newer.

AgentLint 2.9.1 fixes setup output for the OpenAI Agents SDK, MCP and generic
integrations, uses Gemini's own event names, and refuses to overwrite an agent
settings file it can't parse. AgentLint 2.9.0 also applies built-in rules to
Gemini, Kimi, Grok and Cursor tool names, which earlier versions missed.

AgentLint 2.9.0 checks shell commands per parsed operation, so quoted text
passed to read-only commands and later operations in the same command (such as
`gh pr create --base main` after a feature-branch push) no longer cause false
matches; unsupported syntax keeps the conservative raw checks. It reports
configuration drift (explicit packs that omit code the repository contains),
adds typed, expiring, human-only approvals (`agentlint approve grant <class>`),
and records test-run evidence (`agentlint evidence`). This plugin now sends
Bash post-tool events so completed test runs are recognized.

AgentLint 2.8.0 made coverage and denials easy to verify: `agentlint status`
shows each agent as configured, enabled and observed, and denials name the
file, line, operation and policy layer.

To compose a shared policy with repository settings, configure
`AGENTLINT_WORKSPACE_CONFIG` in the environment that starts Claude Code; see the
[workspace configuration reference](https://github.com/mauhpr/agentlint/blob/main/docs/configuration.md#workspace-policy).
This release widens the PostToolUse matcher to `Bash|Edit|Write`; the binary resolver is unchanged.
Codex file-patch support is delivered by AgentLint core's separate Codex adapter.
These improvements are delivered by the installed AgentLint core package.

## What the plugin registers

| Event | Matcher | Timeout | Purpose |
|-------|---------|---------|---------|
| PreToolUse | `Bash\|Edit\|Write` | 5s | Block dangerous writes and commands before they run |
| PostToolUse | `Bash\|Edit\|Write` | 10s | Check the result; record completed test runs; run configured CLI tools |
| UserPromptSubmit | all | 5s | Prompt-level rules |
| SubagentStart | all | 5s | Safety briefing for subagents |
| SubagentStop | all | 10s | Audit subagent transcripts |
| Notification | all | 5s | Notification rules |
| Stop | all | 30s | End-of-session report |

Rules, packs and options: [Rules](https://github.com/mauhpr/agentlint/blob/main/docs/rules.md).
Configuration (`agentlint.yml`): [Configuration](https://github.com/mauhpr/agentlint/blob/main/docs/configuration.md).

## Agents and commands

| Name | Purpose |
|------|---------|
| `/agentlint:security-audit` | Scan the codebase for security issues |
| `/agentlint:doctor` | Diagnose configuration and hook problems |
| `/agentlint:fix` | Fix common findings, with confirmation |
| `/agentlint:lint-status` | Coverage, effective policy and session activity |
| `/agentlint:lint-config` | Show or edit `agentlint.yml` |

The plugin's agents carry their own PreToolUse hooks, because Claude Code
subagents don't trigger the parent session's hooks. See
[Subagent safety](https://github.com/mauhpr/agentlint/blob/main/docs/subagent-safety.md).

The plugin also registers the AgentLint MCP server (`agentlint-mcp`, needs
`pip install "agentlint[mcp]"`). Tools: [MCP server](https://github.com/mauhpr/agentlint/blob/main/docs/mcp.md).

## How the binary is found

The hooks call `bin/resolve-and-run.sh`, which looks for `agentlint` on `PATH`,
in `~/.local/bin` (pipx), in the `uv tool` location, and finally tries
`python -m agentlint`. If none work, install the package or run
`agentlint doctor`.

## Troubleshooting

- **`agentlint status` says "never observed"**: check `claude plugin list`,
  restart Claude Code, and make a tool call.
- **`agentlint: command not found`**: install the package (step 1).
- **Hook timeouts on very large files**: raise limits or disable the slow rule;
  see [Diagnostics](https://github.com/mauhpr/agentlint/blob/main/docs/diagnostics.md).

## Community and security

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report
vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

MIT
