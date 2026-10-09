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
