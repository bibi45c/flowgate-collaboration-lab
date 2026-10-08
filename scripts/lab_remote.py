"""Coordinator CLI for this one public synthetic repository; never handles tokens."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = "bibi45c/flowgate-collaboration-lab"
ROOT = Path(__file__).resolve().parents[1]


def emit_output(value, stream, limit):
    """Keep remote exit status authoritative even on a strict legacy console."""
    value = value[:limit]
    try:
        stream.write(value)
    except UnicodeEncodeError:
        encoding = getattr(stream, "encoding", None) or "utf-8"
        escaped = value.encode(encoding, errors="backslashreplace").decode(encoding)
        stream.write(escaped[:limit])


def run(args):
    environment = os.environ.copy()
    environment.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.directory", "GIT_CONFIG_VALUE_0": ROOT.as_posix()})
    result = subprocess.run(["gh", *args], cwd=ROOT, env=environment, text=True, capture_output=True, encoding="utf-8")
    # Only public repository output is requested. Authentication/token commands
    # are deliberately not exposed by this coordinator.
    emit_output(result.stdout, sys.stdout, 12000)
    if result.stderr:
        emit_output(result.stderr, sys.stderr, 3500)
    return result.returncode


def body_file(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError("Body file must exist within the lab repository")
    return str(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "repo", "pins", "issue", "pr", "edit-pr", "checks", "view-pr", "protect", "protection", "merge", "update", "comment", "close", "view-issue", "runs", "run-detail", "run-log-failed", "view-ref"])
    parser.add_argument("--number", type=int)
    parser.add_argument("--title")
    parser.add_argument("--body-file")
    parser.add_argument("--head")
    parser.add_argument("--reviews", choices=["on", "off"], default="on")
    parser.add_argument("--reason", choices=["completed", "not planned"], default="completed")
    args = parser.parse_args()
    if args.action == "create":
        return run(["repo", "create", REPO, "--public", "--description", "Synthetic FlowGate multi-agent collaboration/worktree/CI validation lab; not application code", "--source", str(ROOT), "--remote", "origin", "--push"])
    if args.action == "repo":
        return run(["repo", "view", REPO, "--json", "nameWithOwner,url,isPrivate,defaultBranchRef"])
    if args.action == "pins":
        for action, version in [("checkout", "v7"), ("setup-python", "v6")]:
            code = run(["api", f"repos/actions/{action}/commits/{version}", "--jq", f'"{action}=" + .sha'])
            if code:
                return code
        return 0
    if args.action == "issue":
        return run(["issue", "create", "--repo", REPO, "--title", args.title, "--body-file", body_file(args.body_file)])
    if args.action == "pr":
        return run(["pr", "create", "--repo", REPO, "--base", "main", "--head", args.head, "--title", args.title, "--body-file", body_file(args.body_file)])
    if args.action == "edit-pr":
        command = ["pr", "edit", str(args.number), "--repo", REPO]
        if args.title:
            command += ["--title", args.title]
        if args.body_file:
            command += ["--body-file", body_file(args.body_file)]
        return run(command)
    if args.action == "checks":
        return run(["pr", "checks", str(args.number), "--repo", REPO])
    if args.action == "view-pr":
        return run(["pr", "view", str(args.number), "--repo", REPO, "--json", "url,state,isDraft,headRefName,headRefOid,baseRefName,mergeStateStatus,reviewDecision,statusCheckRollup,closingIssuesReferences,mergeCommit"])
    if args.action == "view-issue":
        return run(["api", f"repos/{REPO}/issues/{args.number}", "--jq", '{number,state,state_reason,html_url,title}'])
    if args.action in {"protect", "protection"}:
        endpoint = f"repos/{REPO}/branches/main/protection"
        if args.action == "protection":
            return run(["api", endpoint, "--jq", '{strict:.required_status_checks.strict,contexts:.required_status_checks.contexts,enforce_admins:.enforce_admins.enabled,review_count:.required_pull_request_reviews.required_approving_review_count}'])
        reviews = ({"dismiss_stale_reviews": True, "require_code_owner_reviews": True,
                    "required_approving_review_count": 1} if args.reviews == "on" else None)
        payload = {"required_status_checks": {"strict": True, "contexts": ["Quality"]}, "enforce_admins": True, "required_pull_request_reviews": reviews, "restrictions": None, "required_conversation_resolution": True, "allow_force_pushes": False, "allow_deletions": False}
        local = ROOT / ".lab-local"
        local.mkdir(exist_ok=True)
        path = local / "protection-input.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return run(["api", "--method", "PUT", endpoint, "--input", str(path), "--jq", '{strict:.required_status_checks.strict,contexts:.required_status_checks.contexts,enforce_admins:.enforce_admins.enabled,review_count:.required_pull_request_reviews.required_approving_review_count}'])
    if args.action == "merge":
        # Never bypass or disable checks. Settings experiments are explicit actions.
        if not args.head or not re.fullmatch(r"[0-9a-fA-F]{40}", args.head):
            parser.error("Merge requires --head with the full reviewed commit SHA")
        if not args.number or not args.title:
            parser.error("Merge requires --number and the reviewed final --title")
        return run(["pr", "merge", str(args.number), "--repo", REPO, "--squash", "--subject", args.title, "--match-head-commit", args.head])
    if args.action == "update":
        return run(["pr", "update-branch", str(args.number), "--repo", REPO])
    if args.action == "comment":
        return run(["issue", "comment", str(args.number), "--repo", REPO, "--body-file", body_file(args.body_file)])
    if args.action == "close":
        return run(["issue", "close", str(args.number), "--repo", REPO, "--reason", args.reason])
    if args.action in {"run-detail", "run-log-failed"}:
        if not args.number or args.number < 1:
            parser.error("Run evidence requires a positive --number run ID")
        command = ["run", "view", str(args.number), "--repo", REPO]
        command += ["--json", "jobs,url,headSha,conclusion"] if args.action == "run-detail" else ["--log-failed"]
        return run(command)
    if args.action == "view-ref":
        if not args.head or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./-]*", args.head) or ".." in args.head:
            parser.error("View-ref requires a concrete branch in --head")
        return run(["api", f"repos/{REPO}/git/ref/heads/{args.head}", "--jq", ".object.sha"])
    return run(["run", "list", "--repo", REPO, "--limit", "8", "--json", "databaseId,event,headSha,status,conclusion,url"])


if __name__ == "__main__":
    raise SystemExit(main())
