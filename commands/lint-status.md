---
name: lint-status
description: Show AgentLint status — active rules, violations this session
---

Run `agentlint status --project-dir "$CLAUDE_PROJECT_DIR"` and display:
1. Which rule packs are active (including quality pack, always active since v0.4.0)
2. How many rules are running (41 across 7 packs)
3. Current severity mode
4. Session activity: tool calls tracked, token budget usage
5. Any violations found this session

If the user reports problems, suggest running `agentlint doctor --project-dir "$CLAUDE_PROJECT_DIR"` to diagnose misconfigurations.
