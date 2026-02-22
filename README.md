# agentlint — Claude Code Plugin

Real-time quality guardrails for AI coding agents. 41 rules across 7 packs covering all 17 Claude Code hook events.

## Prerequisites

Install the `agentlint` Python package:

```bash
pip install agentlint
```

## Binary resolution

The plugin automatically resolves the `agentlint` binary at runtime — no PATH configuration needed. It probes, in order: PATH lookup, `~/.local/bin` (pipx), `uv tool` install location, and `python -m agentlint`. This works regardless of how you installed the package.

If auto-resolution still fails, run `agentlint setup` to register hooks with an absolute path instead.

## Troubleshooting

**Hooks not firing?** Verify the plugin is installed: `claude plugin list`

**`agentlint: command not found`?** The binary resolver couldn't locate agentlint.
Install it (`pip install agentlint`) or run `agentlint setup` to embed an absolute
path in your hooks.

**Timeouts?** PreToolUse hooks have a 5s timeout. If your project is very large,
consider using `severity: relaxed` in `agentlint.yml`.

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

AgentLint hooks into all 17 Claude Code lifecycle events. The key events:

- **PreToolUse** — Intercepts Bash, Edit, and Write calls. Blocks secrets, `.env` commits, force-pushes, destructive commands, unsafe shell execution, SQL injection, and more. Validates commit messages. With the security pack enabled, also blocks Bash file writes and network exfiltration.
- **PostToolUse** — Checks written files for size limits, tracks edit drift, detects dead imports, warns on error handling removal, and flags unnecessary async. Tracks session token budget.
- **UserPromptSubmit** / **SubagentStop** / **Notification** — Passthrough events for future rule expansion.
- **Stop** — Generates an end-of-session quality report with debug artifact detection, TODO scanning, token budget summary, and adversarial self-review prompt.

## Rule packs

| Pack | Rules | Auto-activates when |
|------|-------|---------------------|
| **universal** | 14 | Always active |
| **quality** | 4 | Always active |
| **python** | 6 | `pyproject.toml` or `setup.py` exists |
| **frontend** | 8 | `package.json` exists |
| **react** | 3 | `react` in package.json dependencies |
| **seo** | 4 | SSR/SSG framework (Next.js, Nuxt, Gatsby, Astro, etc.) detected |
| **security** | 2 | Opt-in (add `security` to packs) |

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
- `agentlint list-rules` — List all available rules (use `--pack security` to filter)
- `agentlint status` — Show version, severity mode, active packs, rule count, and session activity
- `agentlint doctor` — Diagnose common misconfigurations

## License

MIT
