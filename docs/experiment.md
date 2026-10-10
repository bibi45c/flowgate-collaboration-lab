# Collaboration experiment plan

The executed observations are recorded in [results.md](results.md) and
[observations.json](observations.json). The cases below retain their original plan
status; consult the results for what was actually exercised and its limitations.

This plan tests the collaboration contract with synthetic code, identities and
issues. It is not FlowGate production or team-adoption evidence. Case outcomes below
are planned until the coordinator records actual observations and evidence.

## Roles and controls

The coordinator owns remote writes, shared Git operations and serial integration.
Development agents own explicitly assigned code/tests in isolated worktrees.
Independent reviewers inspect the assigned head without editing the implementation.
Each assignment includes the contract described in CONTRIBUTING.md.

Only one GitHub account is available. Test that a non-author human-review gate
blocks agent-only integration; do not label an agent review human approval. Any
temporary protection relaxation is an explicit lab experiment with before/after
settings. Restore human-review enforcement at the end. A platform/plan restriction
is a reported limitation, not a successful enforcement result.

## Planned cases

| Case | Exercise | Observable result required |
|---|---|---|
| Effective rules | Each agent reads root entry and its assigned skill | Actual paths/version and relevant overrides reported; no unsupported cross-tool claim |
| Parallel work | Two independent tasks in different branches/worktrees | Each writer changes only assigned files; outputs remain isolated |
| Reviewer boundary | Independent agent reviews a pinned head | Findings cite evidence; implementation and human approval remain untouched |
| Partial delivery | Merge one scoped stage with ordinary Refs only | Unfinished issue stays open; closing associations/message checked |
| Post-merge acceptance | Leave one legitimate synthetic acceptance step outstanding | Pre-merge gates permit eligible integration; issue remains Awaiting acceptance |
| Negative PR metadata | Supply malformed title or missing/invalid fields | Applicable check rejects it; correction is observed |
| Changed integration base | Integrate A before B and recheck B against the new base | Record candidate/base change and affected revalidation; old branch pass is insufficient |
| Human gate | Attempt authorized agent-only integration under normal protections | Non-author approval remains required or platform limitation is recorded |
| Handoff/resume | Transfer a task after stopping old writer/processes | New owner confirms state; old execution cannot resume writing by agreement |
| Recovery/cleanup | Preserve valuable ignored output and detached/unpublished work | Recovery is verified before any authorized removal; clean status alone is rejected |
| Non-delivery closure | Close a synthetic duplicate/cancelled task with reason | It is closed without being marked Done |

Do not manufacture a failure to pad the report. If a case was only inspected or
partially exercised, state that limit. Run destructive cleanup only within the
explicit experiment scope after preservation and recovery checks.

## Observation format

For each executed case, record its actual issue/PR URL if created, agents/owners,
rule version, tested head/base/candidate, actions, results, evidence, limitations
and any narrowly supported policy correction. Record configured check/protection
settings, final setting restoration and any remaining blockers. Do not prefill
remote identifiers or assert completion from this plan.

## 2026-10-11: Issue/PR gate revalidation

This is a pre-integration observation snapshot for [Issue #12](https://github.com/bibi45c/flowgate-collaboration-lab/issues/12)
and [PR #13](https://github.com/bibi45c/flowgate-collaboration-lab/pull/13).
The development writer handed its isolated worktree back to the coordinator;
an independent agent reviewed the pinned test diff without publishing a human approval.
No AGENTS.md, workflow, application contract or GateFlow files changed.

Base: `ec16f4e3e1460b54dd1084dce5f68b66e069b2d5`.
Test head: `20646488d1f0a7ed41e8de026368698e88b82115`.
Python 3.13.5: targeted tests passed (3 methods, 11 subcases); full suite passed (62 tests).

| Executed case | Observed result | Evidence |
|---|---|---|
| Incomplete issue submitted by CLI | Created successfully despite malformed title/missing form fields; then repaired and assigned | Issue #12 |
| Malformed PR title | PR metadata and Quality failed; Unit tests passed | [Run 38073089565](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/38073089565) |
| Partial delivery with a closing reference | PR metadata and Quality failed; Unit tests passed | [Run 38073170340](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/38073170340) |
| Complete delivery with outstanding post-merge acceptance and closing reference | PR metadata and Quality failed; Unit tests passed | [Run 38073220181](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/38073220181) |
| Complete/post-merge with ordinary reference | All three CI jobs passed; closing associations empty | [Run 38073261935](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/38073261935) |
| Normal merge attempt after the successful run | Rejected by branch policy; PR stayed OPEN, REVIEW_REQUIRED and BLOCKED | PR #13, coordinator merge exit 1 |

Observed normal protections: strict Quality from GitHub Actions, enforced admins,
one approving review, CODEOWNERS, stale-review dismissal, conversation resolution,
and no force pushes/deletions. Only one collaborator account is available.

The issue-form probe confirms that CLI creation is not prevented by the web form.
Static/pure-function review also found that the PR guard checks linked issue identity,
not issue readiness or actual acceptance evidence. Issue edits do not trigger this
workflow; candidate workflow changes still require trusted review. These findings
do not establish an executed merge bypass or an accepted application delivery.

At this snapshot, experimental integration, protection restoration and post-merge
acceptance have not run. Subsequent actual results belong in Issue #12; a controlled
agent-only merge must retain Quality/strict/admin/conversation gates, restore the
original human-review setting, and remain labelled as an experiment.
## Deterministic issue reminders: pre-integration snapshot

Issue [#14](https://github.com/bibi45c/flowgate-collaboration-lab/issues/14) and
PR [#15](https://github.com/bibi45c/flowgate-collaboration-lab/pull/15) track the
minimal format-only experiment. The runtime adds one workflow and one Python
script; one additional test file verifies its behavior. There is no AI, label/state
automation or PR gate. Existing issue forms supply required fields, and
CONTRIBUTING.md supplies the permitted title areas.

Local evidence on implementation commit
`ab8ae60ebf3dc3dad32e300b685faaf9c7312173`, against main
`339330962692d858b7e950438ad91b86b1625649`, using Python 3.13.5:

| Check | Observed result |
|---|---|
| Focused issue-format tests | 17 passed |
| Full unittest suite | 79 passed |
| Complete task, bug and design forms | Accepted |
| Missing, empty, placeholder or duplicate required sections | Reported |
| Unknown title area | Reported after an independently reproduced correction |
| Entire verification plan set to None | Reported; only the post-merge step may be absent |
| HTML comment opener inside a code fence | Preserved as reproduction data |
| Fake API comment creation, repair and repeat | Same bot-comment ID; repeat performs no write |

This snapshot records local results, not live GitHub issue-event acceptance.
The workflow must be on the default branch before those events can run. Issue #14
will hold actual opened/edited run links, bot-comment IDs and protection readbacks.
Any single-account lab merge remains experimental, not non-author human approval.
The checker validates format, not requirement quality or implementation authority.
Its dependency-free form reader supports the current simple YAML layout and fails
visibly for unsupported layouts. Feedback is advisory, not an atomic snapshot gate.
