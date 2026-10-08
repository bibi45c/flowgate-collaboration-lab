import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts import lab_git, lab_remote


class CommitScopeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="synthetic-git-scope-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        global_config = self.repo / "empty-global-config"
        global_config.write_text("", encoding="utf-8")
        self.environment = mock.patch.dict(os.environ, {
            "GIT_CONFIG_GLOBAL": str(global_config), "GIT_CONFIG_NOSYSTEM": "1"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)
        lab_git.git(self.repo, "init", "-q")
        lab_git.git(self.repo, "config", "user.name", "Synthetic Lab")
        lab_git.git(self.repo, "config", "user.email", "lab@example.invalid")
        for name in ("inside.txt", "outside.txt", " leading.txt"):
            (self.repo / name).write_text("baseline\n", encoding="utf-8", newline="\n")
        lab_git.git(self.repo, "add", "--", "inside.txt", "outside.txt", " leading.txt")
        lab_git.git(self.repo, "commit", "-qm", "chore(lab): seed isolated scope fixture")
        self.real_index = (self.repo / ".git" / "index").read_bytes()
        self.original_head = lab_git.git(self.repo, "rev-parse", "HEAD")
        self.alternate = self.repo / "alternate-index"
        self.index_environment = mock.patch.dict(os.environ, {"GIT_INDEX_FILE": str(self.alternate)})
        self.index_environment.start()
        self.addCleanup(self.index_environment.stop)
        lab_git.git(self.repo, "read-tree", "HEAD")

    def assert_real_index_unchanged(self):
        self.assertEqual((self.repo / ".git" / "index").read_bytes(), self.real_index)

    def change(self, name):
        (self.repo / name).write_text("changed\n", encoding="utf-8", newline="\n")

    def test_existing_out_of_scope_stage_is_refused_and_preserved(self):
        self.change("inside.txt")
        self.change("outside.txt")
        lab_git.git(self.repo, "add", "--", "outside.txt")
        before = self.alternate.read_bytes()
        with self.assertRaisesRegex(ValueError, "out-of-scope"):
            lab_git.commit_files(self.repo, ["inside.txt"], "fix(lab): scoped change")
        self.assertEqual(self.alternate.read_bytes(), before)
        self.assertEqual(lab_git.git(self.repo, "rev-parse", "HEAD"), self.original_head)
        self.assert_real_index_unchanged()

    def test_out_of_scope_stage_added_during_add_is_refused(self):
        self.change("inside.txt")
        self.change("outside.txt")
        original = lab_git.git
        def racing_git(path, *args):
            result = original(path, *args)
            if args[0] == "add":
                original(path, "add", "--", "outside.txt")
            return result
        with mock.patch.object(lab_git, "git", side_effect=racing_git):
            with self.assertRaisesRegex(ValueError, "out-of-scope"):
                lab_git.commit_files(self.repo, ["inside.txt"], "fix(lab): scoped change")
        staged = original(self.repo, "diff", "--cached", "--name-only", "-z")
        self.assertIn("outside.txt\0", staged)
        self.assertEqual(original(self.repo, "rev-parse", "HEAD"), self.original_head)
        self.assert_real_index_unchanged()

    def test_directory_glob_pathspec_and_escape_are_refused(self):
        (self.repo / "nested").mkdir()
        (self.repo / "nested" / "file.txt").write_text("synthetic\n", encoding="utf-8", newline="\n")
        before = self.alternate.read_bytes()
        for name in ("nested", "*.txt", ":(top)inside.txt", "../outside.txt", "C:/outside.txt", "."):
            with self.subTest(name=name), self.assertRaises(ValueError):
                lab_git.commit_files(self.repo, [name], "fix(lab): scoped change")
        self.assertEqual(self.alternate.read_bytes(), before)
        self.assert_real_index_unchanged()

    def test_success_commits_only_explicit_file(self):
        self.change("inside.txt")
        self.change("outside.txt")
        head = lab_git.commit_files(self.repo, ["inside.txt"], "fix(lab): scoped change")
        self.assertNotEqual(head, self.original_head)
        self.assertEqual(lab_git.git(self.repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"), "inside.txt")
        self.assert_real_index_unchanged()

    def test_explicit_tracked_deletion_is_supported(self):
        (self.repo / "inside.txt").unlink()
        lab_git.commit_files(self.repo, ["inside.txt"], "fix(lab): remove scoped fixture")
        self.assertEqual(lab_git.git(self.repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD"), "D\tinside.txt")
        self.assert_real_index_unchanged()

    def test_leading_space_path_does_not_hide_staged_content(self):
        self.change(" leading.txt")
        lab_git.git(self.repo, "add", "--", " leading.txt")
        with self.assertRaisesRegex(ValueError, " leading.txt"):
            lab_git.commit_files(self.repo, ["inside.txt"], "fix(lab): scoped change")
        self.assert_real_index_unchanged()


class RemoteCommandTests(unittest.TestCase):
    def invoke(self, *args):
        with mock.patch("sys.argv", ["lab_remote", *args]):
            return lab_remote.main()

    def test_merge_without_reviewed_sha_is_refused(self):
        with mock.patch.object(lab_remote, "run") as run, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.invoke("merge", "--number", "6", "--title", "fix(governance): pin reviewed head")
            run.assert_not_called()

    def test_merge_passes_exact_reviewed_sha(self):
        sha = "a" * 40
        with mock.patch.object(lab_remote, "run", return_value=0) as run:
            self.assertEqual(self.invoke("merge", "--number", "6", "--title", "fix(governance): pin reviewed head", "--head", sha), 0)
        command = run.call_args.args[0]
        self.assertEqual(command[command.index("--match-head-commit") + 1], sha)
        self.assertNotIn("--admin", command)

    def test_read_only_run_evidence_commands(self):
        for action, expected in (("run-detail", "--json"), ("run-log-failed", "--log-failed")):
            with self.subTest(action=action), mock.patch.object(lab_remote, "run", return_value=0) as run:
                self.assertEqual(self.invoke(action, "--number", "123"), 0)
                command = run.call_args.args[0]
                self.assertEqual(command[:3], ["run", "view", "123"])
                self.assertIn(expected, command)

    def test_ref_evidence_targets_only_repository_branch(self):
        with mock.patch.object(lab_remote, "run", return_value=0) as run:
            self.assertEqual(self.invoke("view-ref", "--head", "fix/synthetic"), 0)
        self.assertEqual(run.call_args.args[0][1], f"repos/{lab_remote.REPO}/git/ref/heads/fix/synthetic")
        with mock.patch.object(lab_remote, "run") as run, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.invoke("view-ref", "--head", "../other")
            run.assert_not_called()
