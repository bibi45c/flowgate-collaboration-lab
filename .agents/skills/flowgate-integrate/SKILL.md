---
name: flowgate-integrate
description: Perform coordinator-authorized FlowGate lab integration, acceptance and closeout with current gates and explicit experimental limitations.
---

Read [CONTRIBUTING.md](../../../CONTRIBUTING.md), Commits/PRs and Integration,
and [docs/testing.md](../../../docs/testing.md). Confirm coordinator ownership and
the existing authorization for each remote or cleanup action.

1. Read current PR head, target base, checks, review and actual closing associations.
   Revalidate affected integration when base changes. Do not rely on branch-only
   passes or an outdated review. Merge serially under the configured gates.
2. Verify the final squash title/message and issue closure behavior. Partial or
   outstanding post-merge acceptance must remain ordinary Refs without closing links.
3. Require normal non-author human approval. For an explicitly authorized lab gate
   experiment, record settings before/after and the observed block or relaxation.
   Agent-only merges are experimental and not human-approved; restore human-review
   enforcement as the final setting. Never use admin bypass as proof of success.
4. Read back actual merge/issue state. Complete approved post-merge acceptance before
   Done; authorized cancellation/duplicate closure records its reason instead.
5. Use `../flowgate-worktree/SKILL.md` for any authorized cleanup after preservation
   and recovery, and record actual experiment observations in docs/experiment.md.

Stop dependent integration on an unsatisfied required gate; report platform or
single-account limitations honestly. Return actual identifiers, evidence, final
protection settings, outstanding acceptance and retained work. No production or
provider action is authorized by this synthetic workflow.
