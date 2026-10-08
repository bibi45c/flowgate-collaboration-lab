---
name: flowgate-verify
description: Verify a FlowGate lab change and record source-bound test and acceptance evidence without inventing unavailable results.
---

Read [docs/testing.md](../../../docs/testing.md) for actual checks, evidence fields
and acceptance gates. Read the issue's accepted scope and affected contract.

Choose the nearest meaningful behavior check, then the documented full check and
applicable CI gates. Test failure/retry cases affected by the change; keep mutable
outputs isolated. Do not expand a test-only assignment into implementation or remote
publication without authorization.

Record purpose, actual command/scenario, environment, head/base or integration
candidate, inputs/configuration, result and concise evidence. Use `passed`, `failed`,
`not run` or `blocked`, explaining the latter three. Confirm local uncommitted test
inputs are delivered; rerun affected checks after input changes or uncertain equivalence.

When base changes, verify the affected combined behavior; a previous independent
branch pass is insufficient. Distinguish local, CI, agent review, human approval,
merge and post-merge acceptance evidence. Never move a required pre-merge check into
the post-merge list to permit integration.

Return the evidence and unsatisfied gates. A syntactically valid template or skill
does not establish correct execution; exercise a relevant behavioral case when needed.
