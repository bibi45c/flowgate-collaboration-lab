"""Scoped Git coordinator for the lab and its own sibling worktrees."""
import argparse
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT.parent / "worktrees"
REMOTE = "https://github.com/bibi45c/flowgate-collaboration-lab.git"
COMMIT_HOOKS = ("pre-commit", "prepare-commit-msg", "commit-msg", "post-commit",
                "post-rewrite", "reference-transaction", "post-index-change")


def checkout(value=None):
    path = Path(value).resolve() if value else ROOT
    if path != ROOT and not path.is_relative_to(TASKS.resolve()):
        raise ValueError("Checkout must be the lab or its own task worktree")
    return path


def git(path, *args):
    result = subprocess.run(["git", "-c", f"safe.directory={path.as_posix()}", *args], cwd=path, text=True, encoding="utf-8", capture_output=True)
    if result.stdout:
        print(result.stdout[:10000], end="")
    if result.stderr:
        print(result.stderr[:2500], end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout if "-z" in args else result.stdout.strip()


def explicit_files(path, names):
    if not names:
        raise ValueError("Explicit files are required")
    allowed = set()
    for name in names:
        normalized = name.replace("\\", "/")
        if (not normalized or re.search(r"[:*?\[\]]", normalized)
                or normalized.startswith(("/", "-"))
                or any(part in {"", ".", ".."} for part in normalized.split("/"))):
            raise ValueError("Use explicit repository-relative file paths, not Git pathspecs")
        target = (path / normalized).resolve()
        if not target.is_relative_to(path.resolve()) or target.is_dir():
            raise ValueError("Commit scope must contain files within the assigned checkout")
        if not target.is_file():
            tracked = set(git(path, "ls-files", "-z", "--", normalized).split("\0"))
            if normalized not in tracked:
                raise ValueError(f"Commit file does not exist and is not tracked: {normalized}")
        allowed.add(normalized)
    return allowed


def check_index_scope(path, allowed):
    # Include both rename endpoints; do not clear or repair someone else's index.
    staged = {name for name in git(path, "diff", "--cached", "--name-only", "--no-renames", "-z").split("\0") if name}
    outside = staged - allowed
    if outside:
        raise ValueError("Refuse out-of-scope staged files: " + ", ".join(sorted(outside)))


def refuse_commit_hooks(path):
    configured = subprocess.run(
        ["git", "-c", f"safe.directory={path.as_posix()}", "config", "--path", "--get", "core.hooksPath"],
        cwd=path, text=True, encoding="utf-8", capture_output=True)
    if configured.returncode not in (0, 1):
        raise ValueError("Cannot inspect effective hook configuration; no files staged")
    directory = (configured.stdout.rstrip("\r\n") if configured.returncode == 0
                 else git(path, "rev-parse", "--git-path", "hooks"))
    hooks = (path / directory).resolve()
    active = [name for name in COMMIT_HOOKS
              if (hooks / name).is_file() and os.access(hooks / name, os.X_OK)]
    if active:
        raise ValueError("Refuse effective commit hooks before staging: " + ", ".join(active)
                         + "; retain the index and use a reviewed normal workflow without disabling hooks")


def verify_commit_scope(path, previous_head, allowed):
    head = git(path, "rev-parse", "HEAD")
    parents = git(path, "rev-list", "--parents", "-n", "1", head).split()[1:]
    changed = {name for name in git(path, "diff", "--name-only", "--no-renames", "-z", previous_head, head).split("\0") if name}
    if parents != [previous_head] or changed - allowed:
        raise ValueError("Commit postcondition failed; retain the actual commit and index for review. "
                         "Do not report success or push; no reset/amend performed")
    return head


def commit_files(path, names, title):
    if not title:
        raise ValueError("Explicit title is required")
    refuse_commit_hooks(path)
    allowed = explicit_files(path, names)
    previous_head = git(path, "rev-parse", "HEAD")
    check_index_scope(path, allowed)
    git(path, "add", "--", *sorted(allowed))
    check_index_scope(path, allowed)
    git(path, "diff", "--cached", "--check")
    git(path, "diff", "--cached", "--stat")
    git(path, "commit", "-m", title)
    return verify_commit_scope(path, previous_head, allowed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["bootstrap", "worktree", "commit", "fetch", "push", "update-main", "inspect"])
    parser.add_argument("--path")
    parser.add_argument("--name")
    parser.add_argument("--branch")
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--title")
    parser.add_argument("--files", nargs="+")
    args = parser.parse_args()
    path = checkout(args.path)
    if args.action == "bootstrap":
        refuse_commit_hooks(path)
        files = [".gitignore", "AGENTS.md", "README.md", "CLAUDE.md", "CONTRIBUTING.md", "lab", "tests", "scripts", "docs", ".agents", ".github"]
        git(path, "add", "--", *files)
        git(path, "diff", "--cached", "--check")
        git(path, "diff", "--cached", "--stat")
        git(path, "commit", "-m", "chore(lab): bootstrap synthetic collaboration experiment")
    elif args.action == "worktree":
        target = checkout(str(TASKS / args.name))
        TASKS.mkdir(exist_ok=True)
        if target.exists():
            raise ValueError("Refuse to replace an existing worktree directory")
        git(ROOT, "worktree", "add", "-b", args.branch, str(target), args.ref)
    elif args.action == "commit":
        commit_files(path, args.files, args.title)
    elif args.action in {"fetch", "push", "update-main"}:
        url = git(path, "remote", "get-url", "origin")
        if url.rstrip("/").removesuffix(".git") != REMOTE.removesuffix(".git"):
            raise ValueError("Refuse network action against a different repository")
        if args.action == "fetch":
            git(path, "fetch", "origin")
        elif args.action == "push":
            git(path, "push", "--set-upstream", "origin", args.branch)
        else:
            if git(path, "branch", "--show-current") != "main":
                raise ValueError("Only the main checkout may update the main branch")
            git(path, "pull", "--ff-only", "origin", "main")
    else:
        git(path, "rev-parse", "HEAD")
        git(path, "status", "--short")


if __name__ == "__main__":
    main()
