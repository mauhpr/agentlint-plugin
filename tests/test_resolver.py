"""Exercise resolver entry points with isolated install locations and stdin."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "bin/resolve-and-run.sh"
FAKE_ENGINE = r"""
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
if Path(sys.argv[0]).name in {"python", "python3"}:
    if args[:1] == ["-c"]:
        print(os.environ.get("FAKE_SCRIPTS", ""))
        sys.exit(0)
    if args == ["-m", "agentlint", "--help"]:
        sys.exit(0 if os.environ.get("FAKE_MODULE") == "1" else 1)
    args = args[2:]
data = sys.stdin.read()
with open(os.environ["FAKE_CALLS"], "a") as log:
    log.write(json.dumps({"args": args, "stdin": data}) + "\n")
if args == ["observe", "--help"]:
    sys.exit(0 if os.environ.get("FAKE_OBSERVER") == "1" else 2)
if args[:1] == ["observe"] and os.environ.get("FAKE_OBSERVER") != "1":
    print("unsupported observe", file=sys.stderr)
    sys.exit(2)
print(json.dumps({"args": args, "stdin": data}))
sys.exit(int(os.environ.get("FAKE_EXIT", "0")))
"""


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agentlint resolver ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.home = self.root / "home"
        self.home.mkdir()
        self.log = self.root / "calls.jsonl"
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "PATH": str(self.bin),
            "FAKE_CALLS": str(self.log),
            "FAKE_SCRIPTS": "",
            "FAKE_MODULE": "0",
            "FAKE_OBSERVER": "1",
            "FAKE_EXIT": "0",
        }

    def install(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!{sys.executable}\n" + FAKE_ENGINE)
        path.chmod(0o700)

    def run_resolver(self, *args):
        return subprocess.run(
            ["/bin/sh", str(RESOLVER), *args],
            input="native payload",
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_all_install_locations_forward_policy_arguments_stdin_and_exit(self):
        for location in ("path", "local", "uv", "sysconfig", "python3", "python"):
            with self.subTest(location=location):
                # Each subtest gets a fresh resolver environment.
                self.setUp()
                if location == "path":
                    self.install(self.bin / "agentlint")
                elif location == "local":
                    self.install(self.home / ".local/bin/agentlint")
                elif location == "uv":
                    self.install(
                        self.home / ".local/share/uv/tools/agentlint/bin/agentlint"
                    )
                elif location == "sysconfig":
                    self.install(self.bin / "python3")
                    scripts = self.root / "scripts with spaces"
                    self.install(scripts / "agentlint")
                    self.env["FAKE_SCRIPTS"] = str(scripts)
                else:
                    self.install(self.bin / location)
                    self.env["FAKE_MODULE"] = "1"
                self.env["FAKE_EXIT"] = "7"
                args = ("check", "--project-dir", "project with spaces")
                result = self.run_resolver(*args)
                self.assertEqual(result.returncode, 7, result.stderr)
                self.assertEqual(
                    json.loads(result.stdout),
                    {"args": list(args), "stdin": "native payload"},
                )
                self.assertEqual(len(self.calls()), 1)

    def test_supported_observer_probe_does_not_consume_payload(self):
        self.install(self.bin / "agentlint")
        result = self.run_resolver("observe", "--event", "PermissionRequest")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.calls(),
            [
                {"args": ["observe", "--help"], "stdin": ""},
                {
                    "args": ["observe", "--event", "PermissionRequest"],
                    "stdin": "native payload",
                },
            ],
        )

    def test_old_engine_abstains_for_observer_only(self):
        self.install(self.bin / "agentlint")
        self.env["FAKE_OBSERVER"] = "0"
        result = self.run_resolver("observe", "--event", "PermissionRequest")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("upgrade", result.stderr.lower())
        self.assertIn("unknown", result.stderr.lower())
        self.assertNotIn("native payload", result.stderr)
        self.assertEqual(self.calls(), [{"args": ["observe", "--help"], "stdin": ""}])
        self.env["FAKE_EXIT"] = "9"
        policy = self.run_resolver("check", "--event", "PreToolUse")
        self.assertEqual(policy.returncode, 9)
        self.assertEqual(json.loads(policy.stdout)["stdin"], "native payload")

    def test_python_module_observer_uses_the_same_capability_check(self):
        self.install(self.bin / "python")
        self.env["FAKE_MODULE"] = "1"
        result = self.run_resolver("observe", "--event", "PermissionRequest")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls()[0]["stdin"], "")
        self.assertEqual(self.calls()[1]["stdin"], "native payload")

    def test_missing_engine_retains_installation_error(self):
        result = self.run_resolver("check")
        self.assertEqual(result.returncode, 127)
        self.assertIn("Install", result.stderr)


if __name__ == "__main__":
    unittest.main()
