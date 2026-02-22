---
name: lint-config
description: Show or edit AgentLint configuration
---

Read the `agentlint.yml` file in the project root and display:
1. Current severity mode (standard/strict/relaxed)
2. Active packs
3. Rule overrides
4. Custom rules directory

If the user wants to change settings, edit the agentlint.yml file.

Note: The `security` pack is opt-in — add it to the `packs` list to enable it. Use `agentlint list-rules` to see all available rules, or `agentlint list-rules --pack security` to see security-specific rules.
