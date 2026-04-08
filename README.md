# agentlint — Claude Code Plugin

Real-time guardrails for AI coding agents — code quality, security, infrastructure safety, file-scope governance, and CLI tool integration. 68 rules across 8 packs covering all 17 Claude Code hook events.

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

AgentLint hooks into all 17 Claude Code lifecycle events:

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

## MCP Server

Agents can query rules and pre-validate code programmatically:

```bash
pip install agentlint[mcp]
```

**Tools:**
- `check_content(content, file_path, tool_name?, event?)` — pre-validate code or Bash commands
- `list_rules(pack?)` — discover available rules
- `get_config()` — read current configuration

**Resources:** `agentlint://rules`, `agentlint://config`

The MCP server registers automatically when the plugin is enabled (requires `agentlint[mcp]`).

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

Run any command-line tool as a PostToolUse check:

```yaml
rules:
  cli-integration:
    commands:
      - name: ruff
        on: ["Write", "Edit"]
        glob: "**/*.py"
        command: "ruff check {file.path} --output-format=concise"
        timeout: 10
        severity: warning
```

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
agentlint status         # Version, packs, rule count
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
