# agentlint — Claude Code Plugin

Real-time guardrails for AI coding agents — code quality, security, and infrastructure safety. 63 rules across 8 packs covering all 17 Claude Code hook events.

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

## Vision

The short-term problem is code quality: secrets, broken tests, force-pushes, debug artifacts. AgentLint solves that today.

The longer-term question is harder: what does it mean for an agent to operate safely on real infrastructure? The **autopilot pack** is the first experiment in that direction — opt-in, explicitly experimental, built in the open.

## What it does

AgentLint hooks into all 17 Claude Code lifecycle events. The key events:

- **PreToolUse** — Intercepts Bash, Edit, and Write calls. Blocks secrets, `.env` commits, force-pushes, destructive commands, unsafe shell execution, SQL injection, and more. Validates commit messages. With the security pack enabled, also blocks Bash file writes and network exfiltration.
- **PostToolUse** — Checks written files for size limits, tracks edit drift, detects dead imports, warns on error handling removal, and flags unnecessary async. Tracks session token budget.
- **UserPromptSubmit** / **SubagentStop** / **Notification** — Passthrough events for future rule expansion.
- **Stop** — Generates an end-of-session quality report with debug artifact detection, TODO scanning, token budget summary, circuit breaker status, and adversarial self-review prompt.

### Circuit Breaker (Progressive Trust)

When a blocking rule fires repeatedly (3+ times), it automatically degrades from ERROR → WARNING → INFO → suppressed — preventing false-positive loops from blocking agents. Security-critical rules (`no-secrets`, `no-env-commit`) are exempt and always block. Auto-resets after 5 clean evaluations or 30 minutes. Fully configurable per-rule.

## Rule packs

| Pack | Rules | Auto-activates when |
|------|-------|---------------------|
| **universal** | 17 | Always active |
| **quality** | 4 | Always active |
| **python** | 6 | `pyproject.toml` or `setup.py` exists |
| **frontend** | 8 | `package.json` exists |
| **react** | 3 | `react` in package.json dependencies |
| **seo** | 4 | SSR/SSG framework (Next.js, Nuxt, Gatsby, Astro, etc.) detected |
| **security** | 3 | Opt-in (add `security` to packs) |
| **autopilot** | 18 | Opt-in, ⚠️ experimental (add `autopilot` to packs) |

See [agentlint documentation](https://github.com/mauhpr/agentlint) for the full rule reference.

## Configuration

After installing, create `agentlint.yml` in your project:

```bash
agentlint init
```

See [agentlint documentation](https://github.com/mauhpr/agentlint) for full configuration options.

## Agents

Specialized agents for multi-step operations:

- `/agentlint:security-audit` — Scan your codebase for security vulnerabilities, hardcoded secrets, and unsafe patterns
- `/agentlint:doctor` — Diagnose configuration issues, verify hook installation, suggest optimal pack settings
- `/agentlint:fix` — Auto-fix common violations (debug artifacts, accessibility, dead imports) with confirmation

## Commands

- `/agentlint:lint-status` — Show active rules and session violations
- `/agentlint:lint-config` — Show or edit AgentLint configuration
- `agentlint list-rules` — List all available rules (use `--pack security` to filter)
- `agentlint status` — Show version, severity mode, active packs, rule count, and session activity
- `agentlint doctor` — Diagnose common misconfigurations
- `agentlint import-agents-md` — Import conventions from AGENTS.md into AgentLint config

## License

MIT
