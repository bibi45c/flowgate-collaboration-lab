"""Read-only PR metadata guard. Body structure is not proof of test success."""
import argparse
import json
import os
import re
import urllib.request

TITLE = re.compile(r"^(feat|fix|docs|test|refactor|perf|build|ci|chore|revert)\((lab|access|accounting|governance|ci|docs|test)\)!?: \S.+$")
HEADINGS = ("Summary", "Linked issues", "Delivery", "Acceptance phase", "Verification", "Risk and recovery", "Known limitations")
KEYWORD = re.compile(r"\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s*:?\s+(?:(?:[\w.-]+/[\w.-]+)?#\d+|https://github\.com/[^\s]+/issues/\d+)", re.I)


def sections(body):
    body = re.sub(r"<!--[\s\S]*?-->", "", body or "")
    parts = re.split(r"^## ([^\n]+)\s*$", body, flags=re.M)
    result = {}
    for index in range(1, len(parts), 2):
        name = parts[index].strip()
        if name in result:
            raise ValueError(f"Duplicate section: {name}")
        result[name] = parts[index + 1].strip()
    return result


def validate(pr, closing_issue_numbers=(), commit_messages=(), linked_issues=None):
    errors = []
    if not TITLE.fullmatch(pr.get("title", "")):
        errors.append("PR title must use a supported type(scope): concrete change")
    try:
        fields = sections(pr.get("body", ""))
    except ValueError as error:
        return errors + [str(error)]
    for name in HEADINGS:
        if not fields.get(name):
            errors.append(f"Missing/empty section: {name}")
    delivery = fields.get("Delivery")
    phase = fields.get("Acceptance phase")
    if delivery not in {"complete", "partial"}:
        errors.append("Delivery must be complete or partial")
    if phase not in {"pre-merge", "post-merge"}:
        errors.append("Acceptance phase must be pre-merge or post-merge")
    issue_numbers = {int(item) for item in re.findall(r"(?<![\w/])#(\d+)\b", fields.get("Linked issues", ""))}
    if not issue_numbers:
        errors.append("Linked issues must reference a real lab issue")
    if linked_issues is not None:
        for number in issue_numbers:
            issue = linked_issues.get(number)
            if not issue or "pull_request" in issue:
                errors.append(f"#{number} is not an issue in this repository")
    if delivery == "partial" or phase == "post-merge":
        if KEYWORD.search(pr.get("body", "")):
            errors.append("Partial/post-merge delivery cannot use closing keywords")
        if closing_issue_numbers:
            errors.append("Partial/post-merge delivery cannot have closing Development links")
        if any(KEYWORD.search(message) for message in commit_messages):
            errors.append("Partial/post-merge delivery cannot have closing keywords in commits")
    return errors


def api(path, payload=None):
    token = os.environ["GH_TOKEN"]
    request = urllib.request.Request("https://api.github.com/" + path, data=json.dumps(payload).encode() if payload else None, headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "flowgate-collaboration-lab"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--number", type=int, required=True)
    args = parser.parse_args()
    if args.repo != "bibi45c/flowgate-collaboration-lab":
        parser.error("This experimental guard is restricted to its own repository")
    pr = api(f"repos/{args.repo}/pulls/{args.number}")
    query = "query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){closingIssuesReferences(first:100){nodes{number} pageInfo{hasNextPage}}}}}"
    owner, name = args.repo.split("/")
    graph = api("graphql", {"query": query, "variables": {"owner": owner, "name": name, "number": args.number}})
    if graph.get("errors"):
        raise RuntimeError("Cannot verify closing relationships")
    closing = graph["data"]["repository"]["pullRequest"]["closingIssuesReferences"]
    if closing["pageInfo"]["hasNextPage"]:
        raise RuntimeError("Closing references exceed the lab guard's inspected range")
    commits = []
    page = 1
    while True:
        batch = api(f"repos/{args.repo}/pulls/{args.number}/commits?per_page=100&page={page}")
        commits.extend(item["commit"]["message"] for item in batch)
        if len(batch) < 100:
            break
        page += 1
    fields = sections(pr.get("body", ""))
    issue_numbers = {int(item) for item in re.findall(r"(?<![\w/])#(\d+)\b", fields.get("Linked issues", ""))}
    issues = {number: api(f"repos/{args.repo}/issues/{number}") for number in issue_numbers}
    errors = validate(pr, [item["number"] for item in closing["nodes"]], commits, issues)
    print(json.dumps({"pr": args.number, "head": pr["head"]["sha"], "base": pr["base"]["sha"], "closing_issues": [item["number"] for item in closing["nodes"]], "errors": errors}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
