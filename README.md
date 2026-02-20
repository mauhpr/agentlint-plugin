# agentlint — Claude Code Plugin

Real-time quality guardrails for AI coding agents. 31 rules across 5 packs that auto-activate based on your project's tech stack.

## Prerequisites

Install the `agentlint` Python package:

```bash
pip install agentlint
```

## PATH requirements

The plugin hooks use the bare `agentlint` command and require it to be on your shell's PATH. If hooks fail with `command not found` (common with venv or non-standard installs), use `agentlint setup` instead — it resolves the absolute path automatically.

See the [agentlint documentation](https://github.com/mauhpr/agentlint#quick-start) for details.

## Install from GitHub

Add the marketplace and install:

```bash
claude plugin marketplace add mauhpr/agentlint-plugin
claude plugin install agentlint@agentlint
```

## Install Locally

```bash
claude --plugin-dir /path/to/agentlint-plugin
```

## What it does

AgentLint hooks into three Claude Code lifecycle events:

- **PreToolUse** — Intercepts Bash, Edit, and Write calls. Blocks secrets, `.env` commits, force-pushes, destructive commands, unsafe shell execution, SQL injection, and more.
- **PostToolUse** — Checks written files for size limits, tracks edit drift, and flags unnecessary async.
- **Stop** — Generates an end-of-session quality report with debug artifact and TODO detection.

## Rule packs

| Pack | Rules | Auto-activates when |
|------|-------|---------------------|
| **universal** | 10 | Always active |
| **python** | 6 | `pyproject.toml` or `setup.py` exists |
| **frontend** | 8 | `package.json` exists |
| **react** | 3 | `react` in package.json dependencies |
| **seo** | 4 | SSR/SSG framework (Next.js, Nuxt, Gatsby, Astro, etc.) detected |

See [agentlint documentation](https://github.com/mauhpr/agentlint) for the full rule reference.

## Configuration

After installing, create `agentlint.yml` in your project:

```bash
agentlint init
```

See [agentlint documentation](https://github.com/mauhpr/agentlint) for full configuration options.

## Commands

- `/agentlint:lint-status` — Show active rules and session violations
- `/agentlint:lint-config` — Show or edit AgentLint configuration

## License

MIT
