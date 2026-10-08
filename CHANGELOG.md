# Changelog

## v2.8.0 (2026-10-08) — AgentLint 2.8.0 Compatibility

- Updates plugin and marketplace metadata to v2.8.0 and requires AgentLint
  2.8.0 or newer for this release's documented behavior.
- Documents core coverage reporting: `agentlint status` recognizes user-scope
  and wrapper hook installations and shows configured -> enabled -> observed
  per agent, so this plugin's hooks are reported as observed once they run.
- Documents actionable denials (file, line, operation and the policy layer that
  made a rule active), read-only `doctor`, and AgentChute degraded-mode reporting.
- The MCP server bundled by core adds `check_patch`; no plugin wiring changes.
- Release after AgentLint 2.8.0 is published and verified on PyPI; CI verifies
  the exact package version before this plugin release can merge.

---

## v2.7.1 (2026-10-06) — AgentLint 2.7.1 Compatibility

- Updates plugin and marketplace metadata to v2.7.1 and requires AgentLint
  2.7.1 or newer for this release's documented behavior.
- Includes core read-only Python file-check improvements and conservative
  write detection through the installed Python package.
- Documents the core Codex advisory-feedback correction: warnings stay
  visible without blocking, while effective errors retain blocking decisions.
- Release after AgentLint 2.7.1 is published and verified on PyPI; CI verifies
  the exact package version before this plugin release can merge.

---

## v2.7.0 (2026-10-03) — AgentLint 2.7.0 Compatibility

- Updates plugin and marketplace metadata to v2.7.0 and requires AgentLint
  2.7.0 or newer for this release's documented behavior.
- Includes core Codex post-tool feedback, recording redaction, read-only command
  matching, scoped exceptions, and policy diagnostics through the installed
  Python package. Claude hook payloads and the binary resolver are unchanged.

---

## v2.6.1 (2026-10-01) — AgentLint 2.6.1 Compatibility

- Updates plugin and marketplace metadata to v2.6.1 and documents AgentLint
  2.6.1 as the minimum version for this plugin release.
- Includes the core Codex `PostToolUse` hook-output fix through the installed
  Python package. Claude hook payloads and the binary resolver are unchanged.

---

## v2.6.0 (2026-10-01) — AgentLint 2.6.0 Compatibility

- Updates plugin and marketplace metadata to v2.6.0 and requires AgentLint 2.6.0
  or newer for this release's documented functionality.
- Documents opt-in workspace policy composition and required safety rules.
- Includes the core engine's conservative literal-command and cloud-read matching
  improvements through the installed Python package.
- Keeps Claude hook payloads and the binary resolver unchanged. Codex patch support
  belongs to the core Codex adapter, not this Claude marketplace wrapper.
- Release after AgentLint 2.6.0 is published and verified on PyPI; CI verifies the
  exact package version before this plugin release can merge.

---

## v2.5.5 (2026-07-29) — AgentLint 2.5.5 Compatibility

- Aligns the Claude Code plugin release with AgentLint 2.5.5.
- Updates plugin and marketplace metadata to v2.5.5.
- Adds repository CI that validates JSON and version consistency, release
  notes, compatibility documentation, resolver integrity, and exact AgentLint
  availability and runtime resolution from PyPI.
- Adds Contributor Covenant 2.1, private vulnerability reporting guidance,
  Dependabot configuration, and a repeatable local release validator.
- No hook payload or resolver changes.

---

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
