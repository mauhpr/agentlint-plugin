---
name: lint-status
description: Show AgentLint status — coverage, effective policy, session activity
---

Run `agentlint status --project-dir "$CLAUDE_PROJECT_DIR"` and summarize:
1. Coverage: for Claude, whether hooks are configured, and when AgentLint last
   observed a hook call (if "never observed", say so plainly).
2. Effective policy: policy files in effect (workspace / repository), active
   packs, rule count, severity mode, required rules, and any pack drift warnings.
3. AgentChute (optional cloud): off, healthy or degraded, and what is still
   enforced locally.
4. Session activity and findings this session, if reported.

Use `agentlint status --json` if you need exact fields. If anything looks wrong,
suggest `agentlint doctor --project-dir "$CLAUDE_PROJECT_DIR"` (read-only;
`--fix` repairs).
