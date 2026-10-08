"""Coordinator CLI for this one public synthetic repository; never handles tokens."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = "bibi45c/flowgate-collaboration-lab"
ROOT = Path(__file__).resolve().parents[1]


def run(args):
    environment = os.environ.copy()
    environment.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.directory", "GIT_CONFIG_VALUE_0": ROOT.as_posix()})
    result = subprocess.run(["gh", *args], cwd=ROOT, env=environment, text=True, capture_output=True, encoding="utf-8")
    # Only public repository output is requested. Authentication/token commands
    # are deliberately not exposed by this coordinator.
    print(result.stdout[:12000], end="")
    if result.stderr:
        print(result.stderr[:3500], file=sys.stderr, end="")
    return result.returncode


def body_file(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError("Body file must exist within the lab repository")
    return str(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "repo", "pins", "issue", "pr", "edit-pr", "checks", "view-pr", "protect", "protection", "merge", "update", "comment", "close", "view-issue", "runs"])
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
        payload = {"required_status_checks": {"strict": True, "contexts": ["Quality"]}, "enforce_admins": True, "required_pull_request_reviews": {"dismiss_stale_reviews": True, "require_code_owner_reviews": args.reviews == "on", "required_approving_review_count": 1 if args.reviews == "on" else 0}, "restrictions": None, "required_conversation_resolution": True, "allow_force_pushes": False, "allow_deletions": False}
        local = ROOT / ".lab-local"
        local.mkdir(exist_ok=True)
        path = local / "protection-input.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return run(["api", "--method", "PUT", endpoint, "--input", str(path), "--jq", '{strict:.required_status_checks.strict,contexts:.required_status_checks.contexts,enforce_admins:.enforce_admins.enabled,review_count:.required_pull_request_reviews.required_approving_review_count}'])
    if args.action == "merge":
        # Never bypass or disable checks. Settings experiments are explicit actions.
        return run(["pr", "merge", str(args.number), "--repo", REPO, "--squash", "--subject", args.title])
    if args.action == "update":
        return run(["pr", "update-branch", str(args.number), "--repo", REPO])
    if args.action == "comment":
        return run(["issue", "comment", str(args.number), "--repo", REPO, "--body-file", body_file(args.body_file)])
    if args.action == "close":
        return run(["issue", "close", str(args.number), "--repo", REPO, "--reason", args.reason])
    return run(["run", "list", "--repo", REPO, "--limit", "8", "--json", "databaseId,event,headSha,status,conclusion,url"])


if __name__ == "__main__":
    raise SystemExit(main())
