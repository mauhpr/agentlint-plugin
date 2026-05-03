# agentlint — Claude Code Plugin

Real-time guardrails for AI coding agents — code quality, security, infrastructure safety, file-scope governance, and CLI tool integration. 67 rules across 7 packs covering all 17 Claude Code hook events.

> **Note:** This is the Claude Code plugin wrapper. AgentLint v2.0+ now supports 10 platforms (Claude Code, Cursor, Kimi, Grok, Gemini, Codex, Continue, OpenAI Agents, MCP, and generic HTTP). See the [main repo](https://github.com/mauhpr/agentlint) for other platforms.

## Prerequisites

Install the `agentlint` Python package:

```bash
pip install agentlint
```

## Binary resolution

The plugin automatically resolves the `agentlint` binary at runtime — no PATH configuration needed. It probes, in order: PATH lookup, `~/.local/bin` (pipx), `uv tool` install location, and `python -m agentlint`. This works regardless of how you installed the package.

If auto-resolution still fails, run `agentlint setup` to register hooks with an absolute path instead.

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

AgentLint hooks into all 17 Claude Code lifecycle events via this plugin:

| Event | Behavior |
|-------|----------|
| **PreToolUse** | Blocks secrets, `.env` commits, force-pushes, destructive commands, unsafe shell execution, SQL injection. With security pack: blocks Bash file writes and network exfiltration. |
| **PostToolUse** | Checks file size, tracks edit drift, detects dead imports, warns on error handling removal. **Runs configured CLI tools** (linters, scanners, test runners) via CLI integration. |
| **SubagentStart** | Injects safety briefing into subagent context. |
| **SubagentStop** | Audits subagent transcripts for dangerous commands. |
| **Stop** | Generates quality report with debug artifacts, TODOs, token budget, circuit breaker status. |

## Rule packs

| Pack | Rules | Activates when |
|------|-------|----------------|
| **universal** | 19 | Always active |
| **quality** | 7 | Always active |
| **python** | 6 | `pyproject.toml` or `setup.py` exists |
| **frontend** | 8 | `package.json` exists |
| **react** | 3 | `react` in package.json dependencies |
| **seo** | 4 | SSR/SSG framework detected |
| **security** | 3 | Opt-in |
| **autopilot** | 18 | Opt-in |

## Monorepo Support

Different subdirectories can use different packs:

```yaml
projects:
  frontend/:
    packs: [universal, frontend, react]
  backend/:
    packs: [universal, python]
```

Files outside project prefixes fall back to global `packs:`. Longest prefix wins.

## Warning Suppression

Suppress noisy warnings for the rest of the session:

```bash
agentlint suppress drift-detector    # suppress a rule
agentlint suppress --list            # show suppressed rules
agentlint suppress --remove drift-detector  # unsuppress one rule
agentlint suppress --clear           # clear all suppressions
```

ERRORs are never suppressed (safety invariant). Auto-suppress available via `auto_suppress_after: N` config.

## Global Config Defaults

Set defaults that cascade to all rules:

```yaml
rules:
  strict_mode: true          # all rules inherit this
  auto_suppress_after: 5     # auto-suppress after 5 consecutive fires
  no-secrets:
    strict_mode: false       # per-rule override
```

## Session Summary

View cumulative session activity at any time:

```bash
agentlint report --summary              # text dashboard
agentlint report --summary --format json # structured output
```

Shows violations (blocked/warnings/info), top rules, files touched, suppressed rules, circuit breaker state, and subagent activity. The Stop report also includes cumulative totals automatically.

## MCP Server

Agents can **pre-validate code before writing**, eliminating the block-retry loop from PreToolUse hooks:

```bash
pip install agentlint[mcp]
```

**Tools:**
- `check_content(content, file_path, tool_name?, event?)` — pre-validate code or Bash commands
- `list_rules(pack?)` — discover available rules
- `get_config()` — read current configuration
- `suppress_rule(rule_id)` — suppress a warning rule for the session

**Resources:** `agentlint://rules`, `agentlint://config`

The MCP server registers automatically when the plugin is enabled (requires `agentlint[mcp]`). See the [full MCP guide](https://github.com/mauhpr/agentlint/blob/main/docs/mcp.md) for workflow recipes and troubleshooting.

## CI Mode

Run agentlint in CI pipelines — same rules, same config:

```bash
agentlint ci --diff origin/main...HEAD
```

Exit 0 = clean/warnings. Exit 1 = ERROR violations. Use `--format json` for machine-readable output.

## File-Scope Governance

Restrict which files the agent can access:

```yaml
rules:
  file-scope:
    allow: ["src/**", "tests/**", "docs/**"]
    deny: ["*.env", "credentials/**", ".github/workflows/**"]
```

Deny takes precedence over allow. Blocks Write, Edit, Read, and Bash file operations. Path traversal blocked.

## CLI Integration

Run any command-line tool as a PostToolUse check. Global defaults cascade to all commands:

```yaml
rules:
  cli-integration:
    timeout: 15           # default for all commands
    diff_only: true       # only report violations on changed lines
    commands:
      - name: ruff
        glob: "**/*.py"
        command: "ruff check {file.path} --output-format=concise"
        timeout: 30       # override for ruff only
      - name: ruff-format
        glob: "**/*.py"
        command: "ruff format {file.path}"
        mode: auto-fix    # run silently, apply fix, no warning
      - name: prettier
        glob: "**/*.{ts,tsx,js,jsx}"
        command: "prettier --write {file.path}"
        mode: auto-fix
```

**Modes:** `check` (default — report violations), `auto-fix` (run silently, warn only on failure).

**`diff_only`:** Filters CLI output to only violations on changed lines. Pre-existing violations are suppressed.

Template placeholders (`{file.path}`, `{file.stem}`, `{file.dir}`, `{project.dir}`, `{env.VARNAME}`, etc.) resolve from hook context. All values are shell-escaped for security.

## Custom packs

Custom rules are grouped by `pack` attribute. Add the pack name to `packs:` to activate:

```yaml
packs:
  - universal
  - fintech           # custom pack

custom_rules_dir: .agentlint/rules/
```

Use `agentlint doctor` to detect orphaned packs.

## Circuit Breaker

When a blocking rule fires 3+ times, it degrades from ERROR → WARNING → INFO → suppressed. Security-critical rules (`no-secrets`, `no-env-commit`) are exempt. Auto-resets after 5 clean evaluations or 30 minutes.

## Configuration

```bash
agentlint init           # Create agentlint.yml
agentlint setup          # Install hooks
agentlint doctor         # Diagnose issues
agentlint list-rules     # Show all rules
agentlint status         # Version, packs, rule count, project mappings
agentlint suppress       # Suppress/unsuppress warning rules
agentlint ci             # Scan changed files for CI
agentlint-mcp            # Run MCP server (requires agentlint[mcp])
```

See [agentlint documentation](https://github.com/mauhpr/agentlint) for full reference.

## Agents

- `/agentlint:security-audit` — Scan codebase for security vulnerabilities
- `/agentlint:doctor` — Diagnose configuration and hook issues
- `/agentlint:fix` — Auto-fix common violations with confirmation

## Commands

- `/agentlint:lint-status` — Show active rules and session violations
- `/agentlint:lint-config` — Show or edit configuration

## Troubleshooting

**Hooks not firing?** Run `claude plugin list` to verify installation.

**`agentlint: command not found`?** Install it (`pip install agentlint`) or run `agentlint setup`.

**Timeouts?** PreToolUse hooks have a 5s timeout. Use `severity: relaxed` for large projects.

## License

MIT
