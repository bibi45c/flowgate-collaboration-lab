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
