"""Scoped Git coordinator for the lab and its own sibling worktrees."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT.parent / "worktrees"
REMOTE = "https://github.com/bibi45c/flowgate-collaboration-lab.git"


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
    return result.stdout.strip()


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
        for name in args.files or []:
            target = (path / name).resolve()
            if not target.is_relative_to(path):
                raise ValueError("Commit file lies outside assigned checkout")
        if not args.files or not args.title:
            raise ValueError("Explicit files and title are required")
        git(path, "add", "--", *args.files)
        git(path, "diff", "--cached", "--check")
        git(path, "diff", "--cached", "--stat")
        git(path, "commit", "-m", args.title)
        git(path, "rev-parse", "HEAD")
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
