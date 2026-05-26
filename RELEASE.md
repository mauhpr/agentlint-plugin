# AgentLint plugin release process

This repo releases the Claude Code plugin metadata for AgentLint. It does not
publish a PyPI package.

## Release owner checklist

1. Release AgentLint first when the plugin release points at a new AgentLint
   version.
   - Wait for the AgentLint GitHub Release workflow to publish to PyPI.
   - Verify `agentlint --version` reports the new version from a fresh install.

2. Prepare a plugin release PR from a branch like
   `release/vX.Y.Z-agentlint-compat`.
   Update these files together:
   - `README.md`
   - `CHANGELOG.md`
   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`

3. Validate plugin metadata locally.

   ```bash
   python3 -m json.tool .claude-plugin/plugin.json >/dev/null
   python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
   python3 -m json.tool hooks/hooks.json >/dev/null
   python3 -m json.tool .mcp.json >/dev/null
   sh -n bin/resolve-and-run.sh
   test -x bin/resolve-and-run.sh
   ```

4. Open the PR and wait for repository checks.
   - The workflow is `.github/workflows/ci.yml`.
   - It validates JSON, shell syntax, executable bit, and binary resolution.

5. Merge the PR into `main`.

6. Create the GitHub Release from the final `main` commit.

   ```bash
   git fetch origin main --tags
   TARGET_SHA="$(git rev-parse origin/main)"
   gh release create vX.Y.Z \
     --target "$TARGET_SHA" \
     --title "AgentLint Plugin vX.Y.Z" \
     --notes-file /path/to/release-notes.md
   ```

   `gh-personal` can be used instead of `gh` on machines configured with that
   wrapper.

7. Verify the release metadata.

   ```bash
   gh release view vX.Y.Z
   git show origin/main:.claude-plugin/plugin.json | rg '"version"'
   git show origin/main:.claude-plugin/marketplace.json | rg '"version"'
   ```

## Important rules

- Do not publish this repo to PyPI.
- Do not create the plugin GitHub Release until `.claude-plugin/plugin.json`
  and `.claude-plugin/marketplace.json` both contain the release version.
- Keep hook payload and resolver changes separate from compatibility-only
  releases unless the release intentionally changes runtime behavior.
- If a GitHub Release was created with stale metadata, merge a metadata fix
  first and create a corrected patch release rather than moving a published tag.
