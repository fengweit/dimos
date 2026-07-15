# One-Run Parallel Lane Worker Contract

The worker invocation prepends the lane name, exact worktree, branch, ownership globs, and progress path. Complete exactly one earliest PENDING micro-spec and exit.

1. Read `interfaces.md`, this lane's `progress.md`, and only its earliest PENDING step.
2. Verify exact worktree and branch, clean/owned status, `fork/<branch>` synchronization, and the machine-local `PARALLEL_BASE_SHA` contract.
3. Never edit integration-owned shared contracts, another lane's files/ledger, the global board, demo/docs, or unowned paths.
4. If the interface is insufficient, create only `interface-change-requests/<lane>-<sequence>.md`, mark `BLOCKED_INTERFACE`, commit/push that request, and exit.
5. Use RED-GREEN-REFACTOR: one failing test, expected failure, minimal implementation, focused green gate, refactor while green.
6. Run one focused independent review and at most one correction/re-review cycle.
7. Run `~/.hermes/scripts/dimos_stqa_lane_guard.sh <lane> --working-tree` before staging and again with `--cached` before committing.
8. Update only this lane's append-only ledger, stage explicit files, make one specified commit, push only `fork/<branch>`, and verify local/remote SHA equality.
9. Never force-push, amend, rebase, reset, stash, broad-add, merge, install/sync dependencies, access model/network/LFS assets, or run real video/model/TemporalMemory gates.
10. Exit after one micro-spec whether complete or blocked.
