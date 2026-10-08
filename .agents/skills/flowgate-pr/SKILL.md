---
name: flowgate-pr
description: Prepare or update an authorized FlowGate lab commit and PR with scoped changes, canonical metadata and current verification evidence.
---

Read [CONTRIBUTING.md](../../../CONTRIBUTING.md), Commits and PRs, and use the
[PR template](../../../.github/pull_request_template.md) as the sole body format.

Inspect the actual diff, owner, target branch and included files before committing.
Preserve unrelated work. Use the documented type/scope title; stage only the assigned
change. Verify evidence describes delivered inputs and the current head/base.

Keep all seven template headings. Fill Delivery and Acceptance phase with valid
single values. Describe the concrete problem/behavior, actual issue relationship,
checks, risk/recovery and limits. Keep partial or outstanding post-merge acceptance
issues on ordinary Refs with no closing Development link or closing commit keywords.
Do not claim complete issue acceptance merely from complete implementation.

Author preparation, review readiness and merge eligibility are different. Make a
reviewable PR when permitted; pending post-merge acceptance alone does not require
Draft. Failed/missing mandatory pre-merge checks still block merge.

Prepare before publishing; remote actions remain coordinator-owned unless delegated.
For new commits, update proof and identify any affected review. Return the artifact
or actual link, head/base, required gates and remaining acceptance. Do not merge via
this skill or count an agent review as human approval.
