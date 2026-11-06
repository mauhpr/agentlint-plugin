"""Compare packaged hooks with the installed core and exercise native payloads."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]


class HookTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            shutil.which("agentlint"), "Install the matching AgentLint release first"
        )
        self.temp = tempfile.TemporaryDirectory(prefix="agentlint plugin project ")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        (self.project / "agentlint.yml").write_text("packs: [security]\n")
        self.env = {
            **os.environ,
            "CLAUDE_PLUGIN_ROOT": str(ROOT),
            "CLAUDE_PROJECT_DIR": str(self.project),
            "AGENTLINT_CACHE_DIR": str(self.project / "cache"),
        }

    def hook(self, event, data, passive=False):
        commands = [
            hook["command"] for entry in HOOKS[event] for hook in entry["hooks"]
        ]
        command = next(
            command for command in commands if (" observe " in command) == passive
        )
        result = subprocess.run(
            ["/bin/sh", "-c", command],
            input=json.dumps(data),
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_manifest_matches_core_generated_claude_hooks(self):
        result = subprocess.run(
            [
                "agentlint",
                "setup",
                "claude",
                "--dry-run",
                "--project-dir",
                str(self.project),
            ],
            text=True,
            capture_output=True,
            env=self.env,
            check=True,
        )
        core, _ = json.JSONDecoder().raw_decode(
            result.stdout[result.stdout.index("{") :]
        )

        def normalize(hooks):
            normalized = {}
            for event, entries in hooks.items():
                normalized[event] = []
                for entry in entries:
                    clean = {
                        key: value for key, value in entry.items() if key != "hooks"
                    }
                    clean["hooks"] = []
                    for hook in entry["hooks"]:
                        command = shlex.split(hook["command"])[1:]
                        if "--project-dir" in command:
                            index = command.index("--project-dir")
                            del command[index : index + 2]
                        clean["hooks"].append(
                            {
                                "type": hook["type"],
                                "command": command,
                                "timeout": hook["timeout"],
                            }
                        )
                    normalized[event].append(clean)
            return normalized

        self.assertEqual(normalize(HOOKS), normalize(core["hooks"]))

    def test_actual_write_policy_remains_a_denial(self):
        output = self.hook(
            "PreToolUse",
            {
                "session_id": "parent",
                "tool_name": "Bash",
                "tool_input": {"command": "cp input maintained.py"},
            },
        )
        self.assertEqual(
            json.loads(output)["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_plugin_installation_path_with_spaces_keeps_policy_enforced(self):
        plugin = self.project / "plugin with spaces"
        shutil.copytree(ROOT / "bin", plugin / "bin")
        self.env["CLAUDE_PLUGIN_ROOT"] = str(plugin)
        output = self.hook(
            "PreToolUse",
            {"tool_name": "Bash", "tool_input": {"command": "cp input maintained.py"}},
        )
        self.assertEqual(
            json.loads(output)["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_specialist_agent_hooks_enforce_policy_from_paths_with_spaces(self):
        plugin = self.project / "plugin with spaces"
        shutil.copytree(ROOT / "bin", plugin / "bin")
        self.env["CLAUDE_PLUGIN_ROOT"] = str(plugin)
        for agent in (ROOT / "agents").glob("*.md"):
            with self.subTest(agent=agent.name):
                command = next(
                    json.loads(line.strip().removeprefix("command: "))
                    for line in agent.read_text().splitlines()
                    if line.strip().startswith("command: ")
                )
                result = subprocess.run(
                    ["/bin/sh", "-c", command],
                    input=json.dumps(
                        {
                            "tool_name": "Bash",
                            "session_id": agent.stem,
                            "tool_input": {"command": "cp input maintained.py"},
                        }
                    ),
                    text=True,
                    capture_output=True,
                    env={
                        **self.env,
                        "AGENTLINT_CACHE_DIR": str(self.project / "cache" / agent.stem),
                    },
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    json.loads(result.stdout)["hookSpecificOutput"][
                        "permissionDecision"
                    ],
                    "deny",
                )

    def test_approval_wait_resume_and_failure_are_passive(self):
        payload = {
            "session_id": "parent",
            "agent_id": "child",
            "tool_use_id": "call",
            "tool_name": "Bash",
            "tool_input": {"command": "printf confidential-value"},
        }
        self.assertEqual(self.hook("PermissionRequest", payload, passive=True), "")
        resume = json.loads(
            self.hook("SessionStart", {"session_id": "parent", "source": "resume"})
        )
        context = resume["hookSpecificOutput"]["additionalContext"]
        self.assertIn("awaiting_approval", context)
        self.assertIn("do not interrupt or resubmit", context)
        self.assertNotIn("confidential-value", context)
        self.assertNotIn("permissionDecision", json.dumps(resume))
        self.hook(
            "PostToolUseFailure",
            {**payload, "tool_response": {"status": "cancelled"}},
            passive=True,
        )
        status = subprocess.run(
            ["agentlint", "status", "--json", "--project-dir", str(self.project)],
            text=True,
            capture_output=True,
            env=self.env,
            check=True,
        )
        activity = json.loads(status.stdout)["activity"]
        self.assertEqual(activity["actions"][0]["state"], "cancelled")
        self.assertNotIn("confidential-value", json.dumps(activity))


if __name__ == "__main__":
    unittest.main()
