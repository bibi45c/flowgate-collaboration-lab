import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import lab_remote


class RemoteOutputTests(unittest.TestCase):
    def test_gbk_stdout_stderr_preserve_remote_return_code(self):
        for returncode in (0, 7):
            with self.subTest(returncode=returncode):
                stdout_bytes, stderr_bytes = io.BytesIO(), io.BytesIO()
                stdout = io.TextIOWrapper(stdout_bytes, encoding="gbk", errors="strict")
                stderr = io.TextIOWrapper(stderr_bytes, encoding="gbk", errors="strict")
                result = subprocess.CompletedProcess(["gh"], returncode, "\ufeffsuccess ✓\n", "\ufeffwarning ✓\n")
                try:
                    with mock.patch.object(lab_remote.subprocess, "run", return_value=result):
                        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                            self.assertEqual(lab_remote.run(["repo", "view", lab_remote.REPO]), returncode)
                    stdout.flush()
                    stderr.flush()
                    for data in (stdout_bytes.getvalue(), stderr_bytes.getvalue()):
                        decoded = data.decode("gbk")
                        self.assertIn("\\ufeff", decoded)
                        self.assertIn("\\u2713", decoded)
                finally:
                    stdout.detach()
                    stderr.detach()

    def test_utf8_output_keeps_unicode_and_limits(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        result = subprocess.CompletedProcess(["gh"], 0, "\ufeff✓" + "x" * 13000, "\ufeff✓" + "x" * 4000)
        with mock.patch.object(lab_remote.subprocess, "run", return_value=result):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(lab_remote.run(["repo", "view", lab_remote.REPO]), 0)
        self.assertTrue(stdout.getvalue().startswith("\ufeff✓"))
        self.assertEqual(len(stdout.getvalue()), 12000)
        self.assertEqual(len(stderr.getvalue()), 3500)

    def test_protection_experiments_define_off_as_null_and_default_as_on(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-protection-") as temporary:
            with mock.patch.object(lab_remote, "ROOT", Path(temporary)), mock.patch.object(lab_remote, "run", return_value=0):
                for mode in ("off", "on"):
                    with self.subTest(mode=mode), mock.patch("sys.argv", ["lab_remote", "protect", "--reviews", mode]):
                        self.assertEqual(lab_remote.main(), 0)
                        payload = json.loads((Path(temporary) / ".lab-local" / "protection-input.json").read_text(encoding="utf-8"))
                        if mode == "off":
                            self.assertIsNone(payload["required_pull_request_reviews"])
                        else:
                            self.assertEqual(payload["required_pull_request_reviews"]["required_approving_review_count"], 1)
                            self.assertTrue(payload["required_pull_request_reviews"]["require_code_owner_reviews"])
                        self.assertTrue(payload["required_conversation_resolution"])
