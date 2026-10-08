---
name: flowgate-worktree
description: Obtain, resume, hand off or safely close an assigned FlowGate lab worktree with explicit writer ownership and recoverable state.
---

Read [CONTRIBUTING.md](../../../CONTRIBUTING.md), Ownership and Worktrees.
Inspect current worktree inventory, owner, branch/head and changes before mutation.

- Reuse a suitable owned checkout; otherwise create the assigned task branch and
  isolated worktree from the recorded main or agreed dependency base. Use the owning
  manager, and do not switch an active checkout or force a branch into two checkouts.
- Confirm one active writer, allowed paths and effective rules. Separate mutable
  test outputs, ports and data namespaces. Read-only review can inspect a pinned
  diff; review builds/tests that write need an isolated checkout/resources.
- Shared stash/ref/config/maintenance operations belong to the coordinator.
  Independent stage/commit in separate worktrees is allowed; worktree lock does not
  establish writer ownership.
- On handoff, stop old execution/processes, inspect changes and evidence, then
  confirm transfer. On resume, recheck ownership before writing.
- Before authorized cleanup, inspect valuable ignored/untracked files and
  unpublished/detached commits. Preserve needed artifacts and durable refs or a
  verified recoverable archive, stop processes, and confirm disposition/recovery.
  Clean status alone is insufficient; unknown or cancelled work remains recoverable.

Return local worktree/branch mapping, head/base, owner and preserved/remaining
state. Keep machine paths local; shared issue/PR status uses portable identifiers.
