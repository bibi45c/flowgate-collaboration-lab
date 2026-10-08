# Verification contract

## Confirmed local facts

The synthetic code uses Python 3.13 and the standard library. The baseline contains
three tests. The development check is:

```text
python -m unittest discover -s tests -v
```

This baseline is not evidence for later commits. Record each actual result.

## Select checks by change

Run the nearest meaningful check, then the full development check for code/test
changes. Use repository CI for its configured mandatory checks. Governance/template
changes also need the applicable deterministic validation and a realistic use case;
valid headings or skill frontmatter alone do not prove good agent decisions.

| Changed behavior | Relevant evidence |
|---|---|
| Access decision | Allowed and denied synthetic identities, revocation/expiry if changed |
| Accounting settlement | Repeated requests, unchanged totals, failure/retry behavior |
| Cross-module behavior | The combined access/accounting result against the current base |
| PR metadata/checking | A valid case plus malformed/partial/post-merge counterexamples |
| Ownership/worktree workflow | Observed writer ownership, handoff and recoverable isolated outputs |

Choose cases supported by the implemented contract; do not invent production,
provider, streaming or load-test coverage for this small synthetic lab.

## Evidence record

For each check record: purpose, command/scenario, environment, tested head and base
or integration candidate, source/configuration state, result, and a concise evidence
pointer/output. Results are `passed`, `failed`, `not run`, or `blocked`; explain the
last three. Missing evidence is unavailable, not zero and not a pass.

If local tests used uncommitted inputs, verify those inputs are included in the
delivered change. Re-run affected checks when content changes or equivalence cannot
be established. Testing before commit is valid when the delivered inputs match.
Final-commit CI can provide committed delivery evidence.

Independent branch passes do not establish their combination passes. Record the
latest integration base/candidate and rerun affected checks when it changes.
Concurrent tests must use distinct mutable outputs/resources.

## Acceptance and gates

List required pre-merge checks separately from approved post-merge acceptance.
Required pre-merge failures or unavailable checks block integration. An approved
post-merge scenario may leave an integrated issue Awaiting acceptance without
keeping an otherwise reviewable PR in Draft. Mark Done only after all agreed
acceptance is observed. Synthetic tests, GitHub CI, human approval, merge and
deployment are separate evidence layers.

The coordinator must record actual configured required checks and protection
settings when running experiments. The document does not assert any remote gate
is active. Agent-only review cannot satisfy the normal human-review gate.

## Guard version and controlled integration

The metadata job executes the base commit's guard. The workflow supplies
`LAB_EXPECTED_HEAD` and `LAB_EXPECTED_BASE`; the updated guard requires both full
SHAs, compares the initial live PR, and rereads relevant metadata at the end.
It rejects a changed head/base/title/body/state/version instead of attaching mixed
evidence to an old event. Direct guard invocations must supply those environment
values or `--expected-head` and `--expected-base`.

During bootstrap, an older base guard ignores the new environment values and still
performs its original checks. It does not provide the new version-consistency
guarantee until the updated guard is on the base. No failure is skipped or converted
to success. This compatibility path is not evidence that workflow self-modification
is trusted: CODEOWNERS, non-author human review and their single-account limitations
remain necessary and must be reported.

The commit helper accepts only explicit files, checks existing staged scope before
adding and again afterward, and refuses out-of-scope staged content without clearing
it. Tests use an isolated repository and alternate index; they do not alter the lab
index. The merge helper requires the full reviewed SHA and passes
`--match-head-commit` to GitHub CLI. Pinning a head does not replace human approval,
current-base checks or required protection settings.
