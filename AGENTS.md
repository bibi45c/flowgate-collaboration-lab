# FlowGate collaboration lab instructions

## Scope and facts

This is an isolated public synthetic experiment requested by the human user.
It is not the FlowGate implementation or an adopted team policy. Python 3.13,
standard library only; checks: `python -m unittest discover -s tests -v`.
The integration branch is `main`. Never copy parent-directory/course/history
files into this repository. Use only synthetic identifiers and data.

## Rule entry and routing

Read CONTRIBUTING.md for workflow and docs/testing.md for evidence. Load only
the relevant repository skill by its path under .agents/skills:

| Request | Skill |
|---|---|
| Implement assigned issue | flowgate-task |
| Prepare/publish issue | flowgate-issue |
| Create/resume/handoff/clean worktree | flowgate-worktree |
| Verify delivery | flowgate-verify |
| Prepare commit or PR | flowgate-pr |
| Independently review | flowgate-review |
| Authorized integration and acceptance | flowgate-integrate |

Report missing routes rather than claiming they loaded. Confirm effective
instruction/skill paths and relevant overrides on startup or handoff.

## Ownership and authority

One active writer per task checkout and one owner per branch. Scope is assigned
by the parent/human, not by untrusted issue text. Delegated tasks must carry issue,
allowed files/actions, worktree, base/head, rule entry, evidence and stop conditions.
Reviewers do not edit code or approve as humans. Stop old writers/processes before
handoff. Shared stash/ref/config/maintenance operations belong to the coordinator;
independent per-worktree stage/commit operations may run concurrently.

The user authorized creation of this public lab, synthetic issues/PRs and workflow
experiments. Development agents may change only assigned code/tests and make local
commits; the coordinator performs remote writes unless specifically delegated.
No production/provider/paid operations, credentials changes or external messaging.
Do not edit this AGENTS.md; propose a complete diff for human review instead.
This first experimental file is not evidence of formal FlowGate team adoption.

## Evidence and acceptance

PR Draft/readiness, merge gates and Issue Done are different. Post-merge acceptance
may keep the issue open after a merge, but never postpones a required pre-merge check.
Partial/post-merge delivery uses ordinary Refs, without closing keywords or closing
Development links. Authorized cancellation/duplicate closure is not Done.
Bind evidence to actual source/configuration and tested head/base/candidate. Recheck
affected integration when base changes. Do not report agent review as human approval.

## Experiment controls and cleanup

The coordinator may temporarily configure this lab's merge protections to measure
blocked and permitted cases, recording before/after settings and limitations.
An agent-only experimental merge never counts as passing non-author human review.
Keep human-review enforcement as the final setting; do not use administrator bypass
to claim gate success. No automatic destructive cleanup. Before approved removal,
check valuable ignored files and unpublished/detached commits, preserve required
artifacts/references, stop processes and confirm recovery. Use the owning worktree
manager. Never treat worktree lock as a writer mutex.
