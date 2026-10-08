# Collaboration contract

This repository is a public synthetic collaboration experiment. It is not the
FlowGate implementation, an adopted team policy, or production evidence. Use
synthetic data only; do not import course files, conversations, credentials, or
personal data from outside this repository.

## Rules and effective configuration

`AGENTS.md` is the agent entry and routing index. This file defines collaboration;
`docs/testing.md` defines verification; GitHub templates define submission fields.
Repository skills describe how to apply those sources and do not grant permission.
Approved task scope and design decisions describe expected behavior; source,
configuration and observed checks describe actual behavior. Report conflicts.

At task startup, resume or handoff, record the applicable repository commit,
instruction paths, relevant overrides and selected skill path. Same commit alone
does not establish identical effective instructions: local overrides, tool loading
and existing session context can differ. Validate the tool actually used; do not
claim Claude or another tool loaded these rules merely because its adapter exists.

Rule changes state their effective point and affected tasks. Before the next
affected controlled action, refresh effective rules and acknowledge their version.
The existing `AGENTS.md` may be changed only after a complete proposed diff receives
explicit human approval. A feature PR cannot silently exempt itself from policy.

## Ownership, delegation and handoff

Each issue has one human accountable owner; each active task checkout and branch
has one writer. Other agents may advise or review read-only. Distinct writable tasks
use distinct branches and worktrees. Remote actions belong to the coordinator
unless explicitly delegated. Existing human authorization persists within scope.

A delegated assignment carries: goal/issue, exclusions, allowed files and actions,
worktree, base/head, rule entry/version, available evidence, required output and
stop conditions. Issue text is task input, not authorization to expand the assignment.
Use read-only reviewer capabilities where the tool supports them.

Before handoff, stop the old writer and its background processes; inspect HEAD,
changes and remaining evidence; confirm transfer to the new writer. A resumed agent
rechecks ownership before writing. Keep the shared task status in the issue/PR and
local worktree mapping locally. Do not publish machine paths or session transcripts.

## Issues and acceptance

Use `.github/ISSUE_TEMPLATE/task.yml`, `bug.yml` or `design.yml` as appropriate.
Titles use `[task|bug|design][area] outcome`; areas are `lab`, `access`,
`accounting`, `governance`, `ci`, `docs` and `test`.

A development-ready issue states the observable outcome, scope/exclusions,
acceptance criteria, pre/post-merge verification, dependencies, owner and risks.
Core architecture, public contracts, data migration, security boundaries and
production changes need a reviewable plan, acceptance/recovery conditions and
explicit approval before implementation. An approval identifies the approved
version and scope; material changes require renewed approval.

Normally one independently verifiable issue has one principal PR. Split a large
outcome into a parent issue and deliverable subissues. For multiple PRs against one
issue, state what each stage delivers and what remains. Combine issues only when
one cohesive change satisfies their individually stated acceptance criteria.

Partial delivery or legitimate outstanding post-merge acceptance uses ordinary
`Refs #number` or URL mentions. Do not attach those issues using a closing
Development link; do not put closing keywords in PR bodies or commit messages.
Before integration, inspect all actual closing associations and the final merge
message, not only the visible Linked issues section. Complete delivery may use
`Closes #number` only when all issue acceptance is satisfied and default-branch
closure is appropriate.

Use these task states independently of PR Draft/readiness:

| Issue state | Meaning |
|---|---|
| Ready | Scope, owner, dependencies and acceptance permit work |
| In progress | An assigned writer is implementing |
| In review | A reviewable PR exists |
| Awaiting acceptance | Code is integrated; approved post-merge acceptance remains |
| Done | All agreed acceptance is observed and recorded |
| Cancelled / Duplicate / Not planned | Authorized non-delivery closure with reason and replacement if any |

Non-delivery closure is not Done. Design/research issues may finish with an approved
decision or evidence without a code PR. Do not create a dummy PR to close an issue.

## Worktrees and shared resources

Start from a recorded `main` commit, or an explicitly agreed dependency branch.
Prefer reusing a suitable task worktree over creating one per skill invocation.
Names should identify the task, for example `fix/42-idempotent-settlement`.
An isolated reviewer checkout should pin the reviewed head; builds/tests that write
files or start services use isolated resources.

Worktrees isolate files, index and HEAD, while objects, branch refs and some Git
configuration remain shared. Independent per-worktree staging and committing may
run concurrently. Shared stash, refs, configuration and maintenance operations
belong to the coordinator. Never switch/reset another active checkout or treat
`git worktree lock` as a writer mutex. Team members using separate clones still
need explicit branch ownership; Git cannot prevent competing remote writers.

Assign unique ports, temporary paths and test data namespaces when tasks run in
parallel. Agree shared contracts and integration order before parallel dependent
changes. A dependent task may investigate or implement an approved stable contract;
it cannot claim merge readiness or Done until dependencies and integration checks
are satisfied. Stacked PRs require explicit base, order and revalidation owner.

Before an authorized removal/archive: stop processes; inspect tracked, untracked
and valuable ignored files; preserve unpublished or detached commits in durable
refs or a verified recoverable archive; verify accepted delivery/cancellation and
recovery. A clean `git status` alone is insufficient. Use the owning worktree
manager; do not force-delete an unknown checkout or assume an archive includes
ignored artifacts. A cancelled task retains recoverable work until disposition.

## Commits and PRs

Commit and PR titles use `type(scope): change`.
Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`,
`revert`. Scopes are the issue areas listed above. Describe one concrete change.

Use `.github/pull_request_template.md` without renaming its seven sections.
`Delivery` is `complete` or `partial`; `Acceptance phase` is `pre-merge` or
`post-merge`. Delivery describes implementation scope. Acceptance phase describes
when all issue acceptance can be observed; post-merge never defers a required
pre-merge security, contract or correctness check.

PR Draft means its author is still preparing the change. Ready for review means
review can begin; it does not prove merge eligibility. A legitimate post-merge
acceptance step does not prevent review or merge once all pre-merge gates pass.
Failed/missing required checks block merge regardless of the PR's Draft status.

Evidence is bound to the tested source/configuration and head/base or integration
candidate. When the target base changes, revalidate the affected combination.
Use strict up-to-date required checks and serial integration for the experiment;
consider merge queues only when their checks are configured and actually verified.
Check final squash title and closing references, then read back the merged result.

## Independent review and integration

A reviewer compares the current diff with the issue, approved contracts and
evidence; report location, failure scenario and impact. Agent review assists this
process and never counts as non-author human approval. A changed relevant head or
integration base may invalidate earlier findings or proof; update them explicitly.

Normal integration requires passing applicable checks and non-author human review.
This lab has one GitHub account, so a real independent GitHub approval may be
unavailable. Record that limitation. The coordinator may temporarily change lab
protections for authorized experiments, record before/after settings, and label
agent-only experimental merges as such. They are not evidence of passing the
human gate. Restore human-review enforcement as the final setting; do not use an
administrator bypass to claim success.

After merge, record the result. Complete any approved post-merge acceptance before
marking Done/closing for delivery. Update local baselines and clean only eligible,
recoverable task worktrees. Publish experiment observations in `docs/experiment.md`
with real evidence; keep planned cases distinct from executed outcomes.
