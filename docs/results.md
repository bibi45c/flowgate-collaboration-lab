# Multi-agent collaboration experiment results

This public lab tested the contribution rules with synthetic data and real GitHub
Issues, PRs, Actions and branch protection. The execution crossed 8-9 October 2026
in Singapore. It is an experiment, not formal FlowGate policy or production proof.

The final delivered code baseline before this report is
`2604ff57aa9b06f27d5d8957a55fd0ccb9dbd9b9`: **59 local tests passed**.
[Structured observations](observations.json) record actual heads, merged flags,
merge SHAs, issue closure reasons and check URLs. Final protection restoration and
readback are pending at this report snapshot. After integration, the coordinator
will attach the actual readback to this report PR's timeline; that dated attestation
establishes the observed closing settings, not an immutable guarantee.

## What was actually run

The coordinator assigned four local subagents: Accounting, Access, Governance and
an independent Reviewer. Roles were reused for separate tasks after stopping the
previous writer. An already configured remote Codex review bot also reviewed PRs.
Agent reviews and bot reviews were never counted as independent human approvals.

Each delegated task named its repository instruction/skill paths, scope, worktree,
base/head, permitted actions, evidence and stop conditions. Agents explicitly read
the canonical files; this does **not** prove automatic discovery in a fresh tool
session. The Claude adapter exists, but Claude/OpenCode execution was not tested.

| Case | Observed result | Evidence |
|---|---|---|
| Parallel development | Accounting and Access wrote separate branches/worktrees and only assigned module/tests | [PR 4](https://github.com/bibi45c/flowgate-collaboration-lab/pull/4), [PR 5](https://github.com/bibi45c/flowgate-collaboration-lab/pull/5) |
| Bad title | `fix stuff` failed metadata and required Quality, despite passing unit tests | [Failing run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37797729699) |
| Partial closing reference | `Closes #1` established an actual closing association; the partial PR failed metadata/Quality | [Failing run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37798049407) |
| Corrected metadata | Restoring the scoped title and ordinary Refs passed the latest checks | [Passing run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37798191155) |
| Human gate | Green CI plus local agent review could not merge with one required approval; no admin bypass was used | PR 5 timeline and recorded CLI policy rejection |
| Changed base | After PR 4 merged, old Access checks were green but merge was rejected as not up to date; its branch was updated and revalidated | [Updated-base run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37802232864) |
| Partial delivery | PR 4 merged with Refs only; Issue 1 remained open | [Issue 1](https://github.com/bibi45c/flowgate-collaboration-lab/issues/1), PR 4 |
| Post-merge acceptance | Issue 2 stayed open after merge; actual main smoke and 28 local tests were recorded before completed closure | [Acceptance comment](https://github.com/bibi45c/flowgate-collaboration-lab/issues/2#issuecomment-6064187654) |
| Complete staged delivery | PR 9 completed the agreed interleaved replay regression and automatically closed Issue 1 | [PR 9](https://github.com/bibi45c/flowgate-collaboration-lab/pull/9) |
| Updated guard in trusted base | PR 9 used the repaired base, a canonical Issue URL and mandatory event/live head/base binding; all three jobs passed | [Passing run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37809030604) |
| Non-delivery closure | Duplicate fixture 3 and malformed intake fixture 10 closed as `not_planned`, not Done | [Issue 3](https://github.com/bibi45c/flowgate-collaboration-lab/issues/3), [Issue 10](https://github.com/bibi45c/flowgate-collaboration-lab/issues/10) |
| Handoff | Developers explicitly stopped writing/background work; coordinator then updated branches; independent reviewers pinned current heads | PR 4/5/8/9 and structured version records |
| Recovery | Clean status hid an ignored artifact and an unpublished detached commit; coordinator preserved both and verified recovery in another worktree | Local recovery record below; no worktree removal was exercised |

## Defects found and repaired

[PR 8](https://github.com/bibi45c/flowgate-collaboration-lab/pull/8) repairs:
repository Issue URL parsing; fenced examples masquerading as template headings;
out-of-scope staged entries; expected event head/base and final live metadata
snapshot checks; reviewed-head merge matching; and Windows GBK stdout/stderr
handling that preserves the remote return code.

The first repairs were independently reviewed with 34 tests. A second review
repeated 48 tests and a real isolated old-helper hook reproduction. Updated
integration after Access passed 58 tests; Stage 2 produced the 59-test final suite.

The remote bot found two additional real boundary cases that earlier local reviews
had missed:

- **Tenant subclasses:** a custom `str.__eq__` could authorize the wrong tenant.
  Old code failed three new regressions. Exact built-in dict/str guards now reject
  the malformed subclasses before overridden methods run; independent final Access
  review repeated 10 focused / 28 full tests.
  [Finding and repair reply](https://github.com/bibi45c/flowgate-collaboration-lab/pull/5#discussion_r4220666149).
- **Commit hooks:** a real `pre-commit` hook ran `git add outside.txt` after
  the staged-path check, and the old helper committed both inside/outside files.
  The lab helper now refuses effective commit/ref/index hooks before staging,
  retains the original index, and never disables hooks. It also checks the actual
  committed parent/tree; an unexpected result remains recoverable and is rejected
  without reset/amend or a success claim.
  [Finding and repair reply](https://github.com/bibi45c/flowgate-collaboration-lab/pull/8#discussion_r4221057053).

These helpers assume one writer per checkout. They are not a permission sandbox or
a concurrency lock. A team using hooks needs a reviewed hook-aware commit workflow;
silently disabling its hooks is not an acceptable adaptation.

A coordinator update also produced a readback mismatch between the immediate PR
snapshot and the fetched branch head. The runner stopped, then reconciled the
actual branch ref and PR snapshot before continuing. Short-lived API propagation
lag is an inference; the observed mismatch is the verified fact. A successful
request or CLI line alone is insufficient evidence of the resulting version.

## Trust boundaries that remain

**Candidate workflow self-edit remains a real risk.** The deliberately unmerged
[PR 7](https://github.com/bibi45c/flowgate-collaboration-lab/pull/7) changed Quality
to ignore failed prerequisites. Its metadata job failed while the required Quality
job passed. Human review blocked integration; the PR was closed without merging.
[Actual counterexample run](https://github.com/bibi45c/flowgate-collaboration-lab/actions/runs/37801801548).

Checking out the base version of the guard protects the script source, not the
candidate workflow definition. Keep CODEOWNERS and independent human review for
AGENTS, skills, workflows, contribution rules and helper scripts. Agent-only
automatic integration would need a separately trusted mandatory check source
whose definition the candidate cannot replace; that mechanism was not implemented
or tested here.

**Issue forms are not an API enforcement boundary.** The coordinator created
Issue 10 without owner, scope or acceptance through the API. Intake review correctly
reported it as not development-ready. Retain a Ready/needs-information triage gate;
automated missing-field feedback could assist it, but semantic acceptance still
needs review. An Issue merely existing is not enough for implementation readiness.

Only one GitHub account was available. Temporary laboratory integration removed
the human review subrule while retaining strict Quality, admin enforcement and
conversation resolution. Unresolved remote review threads blocked otherwise green
PRs until actual fixes were independently verified, replied to and resolved.
Changing reviewer count to zero was not the demonstrated cause of that blockage.
No `--admin` bypass, fabricated human approval or production operation occurred.

## Recoverable worktree evidence

The fixture had detached commit
`e4915f80af87e9a14219c5cdffd241ce8802608d` and clean porcelain status, yet an
ignored `.lab-local/valuable-synthetic.txt` remained. The coordinator saved
`archive/recovery-fixture`, separately backed up the ignored artifact and working
document, then restored the same Git blob and file bytes in another checkout.

| Restored file | SHA256 |
|---|---|
| Ignored synthetic artifact | `9bfb452b5f9107d4ed0d53276443ee3cb0e4e92bdc7fba1425b69dc8d41a45ba` |
| Recovery fixture document | `4a4e537cb41295b194de8a9d3745fba9025678932d8613e702e973c82bde7525` |

Git's Windows checkout changed line endings on the first document restore. Git blob
identity was checked, and original working bytes were separately restored and
hashed. Original and recovered worktrees were retained. No destructive cleanup,
Codex-managed archive, or restore-after-deletion was claimed.

## Recommended FlowGate adoption

Keep `AGENTS.md` as the short entry and router. Keep canonical shared rules in
CONTRIBUTING/testing documents, reusable procedures in seven repository skills,
submission fields in GitHub templates, and deterministic gates in tools/CI.
Skills select and apply the rules; they do not grant extra authority.

Normally one independently verifiable Issue has one main PR. A larger outcome can
have staged PRs or deliverable subissues: partial stages use Refs; complete accepted
delivery may close; legitimate post-merge acceptance keeps the Issue open after
merge. Cancelled/duplicate closure remains distinct from Done. Design issues can
finish with an approved decision rather than a dummy code PR.

Assign one branch/worktree writer, one accountable human per Issue, and serial
integration against current base/head/candidate. Permit independent per-worktree
stage/commit, while the coordinator owns shared refs, stash and maintenance.
Stop the old writer before handoff; preserve ignored and unpublished work before
any approved cleanup.

For formal team adoption, name at least two eligible human maintainers so an author
can obtain independent CODEOWNERS review. Verify each member's actual tool loading,
overrides and rule version. Use the real project's proven commands and risks.
Review the concrete AGENTS diff under the user's existing approval rule before
adopting or modifying it. This lab did not establish production, real-provider,
multi-account human approval, cross-tool loading or merge-queue behavior.
