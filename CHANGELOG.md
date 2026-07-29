# Changelog

## v2.5.4 (2026-07-29) — AgentLint 2.5.4 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.4.
- Updates plugin and marketplace metadata to v2.5.4.
- No hook payload or resolver changes.
- Users get the Ruff quality baseline, stronger branch-coverage enforcement,
  expanded MCP tests, and hardened release automation through the installed
  `agentlint` Python package.

---

## v2.5.3 (2026-05-25) — AgentLint 2.5.3 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.3.
- Updates plugin and marketplace metadata to v2.5.3.
- No hook payload or resolver changes.
- Users get AgentChute queue baselining, the `agentlint queue
  discard-pending` recovery command, the `agentlint queue flush` fix, and
  clearer policy diagnostics through the installed `agentlint` Python package.

---

## v2.5.2 (2026-05-25) — AgentLint 2.5.2 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.2.
- No hook payload or resolver changes.
- Users get AgentChute credential persistence through the installed
  `agentlint` Python package, so `agentlint login`, `agentlint onboard --yes`,
  and `agentlint test --flush` can run in the same terminal without manually
  sourcing shell profile changes.

---

## v2.5.1 (2026-05-24) — AgentLint 2.5.1 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.1.
- No hook payload or resolver changes.
- Users get the Stop hook session report formatting fix through the installed
  `agentlint` Python package.

---

## v2.5.0 (2026-05-23) — AgentLint 2.5 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.0.
- No hook payload or resolver changes.
- Users get the new local-first `no-nvd-critical-cve-install` universal rule
  through the installed `agentlint` Python package. The rule consumes the
  cached AgentChute `nvd-cves` feed and blocks exact critical/CISA KEV CPE
  product+version matches without requiring network access in the hook path.

---

## v2.4.0 (2026-05-19) — AgentLint 2.4 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.4.0.
- No hook payload or resolver changes.
- Users get AgentChute local-first onboarding, dashboard pairing, automatic
  background event upload, policy cache diagnostics, and the new `agentlint
  onboard`, `login`, `setup-agent`, `status`, `doctor --fix`, `test`,
  `test-policy`, `queue`, `env`, and `policy` command families through the
  installed `agentlint` Python package.

---

## v2.3.1 (2026-05-15) — AgentChute Onboarding Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.3.1.
- No hook payload or resolver changes.
- Users get clearer AgentChute local setup output, safer AgentChute dry-run
  diagnostics, and improved Codex setup guidance through the installed
  `agentlint` Python package.

---

## v2.3.0 (2026-05-14) — AgentLint 2.3 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.3.0.
- No hook payload or resolver changes.
- Users get FastAPI-aware async findings, grouped text CI output, and
  accepted-pattern config support through the installed `agentlint` Python
  package.

---

## v2.2.0 (2026-05-10) — Public Docs Cleanup

- Removed the internal 2.1.0 release plan from the public plugin repo.
- Clarified plugin metadata and README copy so this repo reads as the Claude
  Code marketplace wrapper, while non-Claude setup lives in the main AgentLint
  package.
- No runtime hook behavior changes.
