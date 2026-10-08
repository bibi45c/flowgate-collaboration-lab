---
name: flowgate-review
description: Independently review a pinned FlowGate lab PR or change against its scope, contracts and evidence without editing the implementation.
---

Read [CONTRIBUTING.md](../../../CONTRIBUTING.md), Independent review, and
[docs/testing.md](../../../docs/testing.md). Inspect the assigned current diff,
issue and approved contract before reading another reviewer's conclusions.

Pin head/base or integration candidate. Keep implementation read-only; authorized
test execution with file/service side effects uses isolated checkout/resources.
Initialize unexecuted checks as `not run`, not passed.

For each actionable finding, provide location, triggering scenario, observable
failure/impact and supporting evidence. Distinguish confirmed behavior from a
counterexample hypothesis or missing proof. Check issue closing relations,
pre/post-merge separation, ownership, delivered test inputs and changed-base evidence
when they affect the assignment. Do not add speculative governance requirements.

If cross-questioning is requested, compare independently produced findings, verify
disputed evidence and retain material dissent. Do not modify code, approve as a
human, post a remote review or expand the assignment without authorization.

Return reviewed identifiers, findings, checks and remaining uncertainty. A new head
or affected base invalidates unsupported reuse of the old report; agent review is
supporting evidence and does not satisfy the normal human-review gate.
