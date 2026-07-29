"""Validate AgentLint Plugin release metadata without third-party dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> object:
    """Load a repository JSON file, failing with its path in the traceback."""
    return json.loads((ROOT / relative_path).read_text())


def main() -> None:
    """Validate JSON syntax and all version-bearing release surfaces."""
    plugin = load_json(".claude-plugin/plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    load_json("hooks/hooks.json")
    load_json(".mcp.json")

    assert isinstance(plugin, dict)
    assert isinstance(marketplace, dict)
    plugins = marketplace.get("plugins")
    assert isinstance(plugins, list) and len(plugins) == 1
    marketplace_plugin = plugins[0]
    assert isinstance(marketplace_plugin, dict)

    version = plugin.get("version")
    assert isinstance(version, str) and version
    assert re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version)
    assert marketplace_plugin.get("version") == version

    changelog = (ROOT / "CHANGELOG.md").read_text()
    readme = (ROOT / "README.md").read_text()
    assert f"## v{version} " in changelog
    assert f"use AgentLint {version} or newer" in readme

    print(version)


if __name__ == "__main__":
    main()
