# One-Run Integration Worker Contract

Complete at most one integration action and exit.

1. Verify `/Users/tian/dimos`, branch `feat/spatiotemporal-video-qa`, clean status, and synchronization with `fork/feat/spatiotemporal-video-qa`.
2. Verify no `dimos-stqa-*` lane worker is active.
3. Read the global board and all lane ledgers. Select only the first dependency-ordered lane in `READY_FOR_INTEGRATION`: A, B, D, E, C.
4. Fetch `fork`; record the source lane head; merge using `git merge --no-ff --no-edit fork/<lane-branch>`. Never guess through conflicts.
5. Run that lane's focused tests, `uv run pytest dimos/benchmark/spatiotemporal -q`, `uv run ruff check dimos/benchmark/spatiotemporal`, and `uv run mypy`.
6. Update only the global board with source and resulting integration heads, commit if needed, push `fork/feat/spatiotemporal-video-qa`, and verify local/remote SHA equality.
7. Never modify lane ledgers or lane-owned implementation while merging. A conflict outside a lane-local ledger is a stop condition.
8. Heavy real video and real `TemporalMemory` gates are reserved for explicit I2/I3 execution after all five lane heads merge; do not run them from a merge tick.
9. Do not force-push, amend, rebase, reset, stash, broad-add, install dependencies, or launch another worker.
