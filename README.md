# agentlint — Claude Code Plugin

Real-time quality guardrails for AI coding agents. Blocks secrets, force-pushes, and destructive commands before they happen.

## Prerequisites

Install the `agentlint` Python package:

```bash
pip install agentlint
```

## Install from Plugin Directory

If available in the Claude Code plugin directory:

```
/plugin install agentlint
```

## Install from Marketplace

```
/plugin marketplace add maupr92/agentlint
/plugin install agentlint@agentlint
```

## Install Locally

```bash
claude --plugin-dir /path/to/agentlint-plugin
```

## What it does

AgentLint hooks into three Claude Code lifecycle events:

- **PreToolUse** — Intercepts Bash, Edit, and Write calls. Blocks secrets, `.env` commits, force-pushes, and destructive commands.
- **PostToolUse** — Checks written files for size limits and tracks edit drift.
- **Stop** — Generates an end-of-session quality report with debug artifact and TODO detection.

## Configuration

After installing, create `agentlint.yml` in your project:

```bash
agentlint init
```

See [agentlint documentation](https://github.com/maupr92/agentlint) for full configuration options.

## Commands

- `/agentlint:lint-status` — Show active rules and session violations
- `/agentlint:lint-config` — Show or edit AgentLint configuration

## License

MIT
