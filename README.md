# AgentLint for Claude Code

**Local guardrails, hook diagnostics, and guided fixes inside Claude Code.**

This plugin connects [AgentLint](https://github.com/mauhpr/agentlint) to Claude Code's supported Bash, Write, and Edit hooks. It also adds three specialist agents, two slash commands, and an optional MCP connection.

AgentLint checks proposed actions, returns findings to Claude, and can deny pre-tool actions with ERROR findings. Many risky operations warn by default; stricter security and infrastructure packs are opt-in. [See exactly what is covered](https://mauhpr.github.io/agentlint/coverage/).

[Quickstart](https://mauhpr.github.io/agentlint/quickstart/) · [Claude Code guide](https://mauhpr.github.io/agentlint/agents/claude/) · [Rules](https://mauhpr.github.io/agentlint/rules/) · [Plugin changelog](CHANGELOG.md)

## Install

Requires Python 3.11+ and Claude Code.

1. Install the Python package with [uv](https://docs.astral.sh/uv/getting-started/installation/) or pipx:

   ```bash
   uv tool install agentlint
   ```

   Or use `pipx install agentlint`. For the bundled MCP tools as well as hooks, install `"agentlint[mcp]"` instead of `agentlint`.

2. Add the marketplace and install the plugin:

   ```bash
   claude plugin marketplace add mauhpr/agentlint-plugin
   claude plugin install agentlint@agentlint
   ```

3. Restart Claude Code in your project. Make one harmless tool call, then check:

   ```bash
   agentlint status
   ```

   Look for a recent **observed** Claude hook call from this project. If it is missing, start with `agentlint doctor` and the [diagnostic guide](https://mauhpr.github.io/agentlint/diagnostics/).

Use the plugin **or** `agentlint setup claude`. Both install the same checks, so installing both can duplicate hook calls.

For a local checkout: `claude --plugin-dir /path/to/agentlint-plugin`.

## See the correction loop

A supported pre-tool hook sends a proposed write to AgentLint. If the content matches a credential pattern, the write is denied and Claude receives a correction such as:

```text
[no-secrets] Secret assignment detected: api_key=...
  -> Use environment variables instead of hard-coded secrets.
```

Claude can revise the proposal to read from the environment. AgentLint checks it again; any other active rules still apply. The [first-use walkthrough](https://mauhpr.github.io/agentlint/quickstart/#4-see-a-block) demonstrates this using synthetic data.

AgentLint provides feedback. It does not automatically rewrite your code.

## Agents and commands

| You want to… | Use |
|--------------|-----|
| Investigate codebase security issues | `/agentlint:security-audit` |
| Diagnose configuration and hooks | `/agentlint:doctor` |
| Propose fixes for common findings, then apply with your confirmation | `/agentlint:fix` |
| Inspect coverage, effective policy, and session activity | `/agentlint:lint-status` |
| Inspect or adjust project policy | `/agentlint:lint-config` |

The first three are agent definitions; the last two are slash commands. Review proposed fixes before approving them. The plugin's agent definitions include their own pre-tool hooks.

The plugin also registers the `agentlint-mcp` server when its optional dependencies are installed. MCP checks are on demand and advisory; native hooks supply enforcement. [MCP setup and tools](https://mauhpr.github.io/agentlint/agents/mcp-hosts/)

## Version compatibility

This plugin release is **2.10.1** and requires **AgentLint 2.10.1 or newer**. The plugin packages integration files; the installed Python package supplies all rules and their behavior. Upgrading one does not upgrade the other.

See the [plugin changelog](CHANGELOG.md) for packaging changes and the [core changelog](https://github.com/mauhpr/agentlint/blob/main/CHANGELOG.md) for rule, adapter, and CLI changes.

## What the plugin registers

| Event | Matcher | Timeout | Purpose |
|-------|---------|---------|---------|
| PreToolUse | `Bash\|Edit\|Write` | 5s | Deny matched actions with ERROR findings; return advisory findings |
| PostToolUse | `Bash\|Edit\|Write` | 10s | Inspect results, record qualifying test evidence, run configured CLI checks |
| UserPromptSubmit | all | 5s | Prompt-level rules |
| SubagentStart | all | 5s | Optional autopilot safety briefing |
| SubagentStop | all | 10s | Optional retrospective transcript audit |
| Notification | all | 5s | Notification rules |
| Stop | all | 30s | Session report |

After-tool and session-end checks cannot prevent an action that has already happened. Subagent hook behavior depends on the host's version and configuration; the briefing and transcript audit do not prove real-time coverage. [Subagent safety](https://mauhpr.github.io/agentlint/subagent-safety/)

## Make it fit your project

The policy lives in `agentlint.yml`. Start with core defaults, then enable the packs and conventions you need.

- [Protect main](https://mauhpr.github.io/agentlint/guides/protect-main/) — distinguish warnings, blocking rules, and branch protection.
- [Fix a false positive](https://mauhpr.github.io/agentlint/guides/fix-a-false-positive/) — use the narrowest adjustment.
- [Run linters and formatters](https://mauhpr.github.io/agentlint/guides/run-linters/) — return existing tool feedback after edits.
- [Share required rules](https://mauhpr.github.io/agentlint/guides/shared-policy/) — apply a baseline across repositories.
- [Configuration reference](https://mauhpr.github.io/agentlint/configuration/) — every policy layer and option.

## How the binary is found

Hooks call `bin/resolve-and-run.sh`. It looks for `agentlint` on `PATH`, in `~/.local/bin`, in the uv tool location, then tries `python -m agentlint`. If resolution fails, install the package and check the environment that launches Claude Code.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Never observed or stale observation | Check `claude plugin list`, restart Claude, and make a tool call in this project |
| Checks run twice | Use the marketplace plugin or native setup, rather than both |
| Binary not found | Confirm the package is installed and reachable in Claude's environment |
| MCP server fails to start | Install the optional `agentlint[mcp]` dependencies |
| A rule repeatedly flags legitimate work | Follow the false-positive guide before changing broad policy |
| A hook times out | Use diagnostics to identify the slow rule or external CLI; inspect the event timeouts above |

AgentLint is a rule and heuristic layer, not a sandbox. Keep review, tests, branch protection, and scoped credentials in place. Cloud event delivery is optional; see [privacy and optional AgentChute](https://mauhpr.github.io/agentlint/agentchute/).

## Community and security

[Code of Conduct](CODE_OF_CONDUCT.md) · [Report a vulnerability privately](SECURITY.md) · [MIT license](LICENSE)

The rules, adapters, and canonical documentation live in [AgentLint core](https://github.com/mauhpr/agentlint). For other coding agents, start with the [integration guides](https://mauhpr.github.io/agentlint/#agents).
