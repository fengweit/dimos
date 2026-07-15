# Parallel Spatiotemporal Video-QA Board

AUTOMATION_STATUS: READY_PAUSED
PARALLEL_BASE_SHA: 59b45f77ae8704f2602edebb091da4b6fd46c1cb
SHARED_CONTRACT_SHA: bd63c75357b291836ea8a51a208bb1968f8944c4
REMOTE: fork
INTEGRATION_BRANCH: feat/spatiotemporal-video-qa

> A commit cannot contain its own SHA. After this control-plane commit, the exact immutable lane base is written to `~/.hermes/run/dimos-spatiotemporal-control/PARALLEL_BASE_SHA`, used to create every branch/worktree, and verified against every lane HEAD before jobs can be resumed.

| Lane | Branch | State | Source head | Merged head |
|---|---|---|---|---|
| A — semantics | `feat/stqa-semantics` | READY_PAUSED | `59b45f77a` | — |
| B — dataset | `feat/stqa-dataset` | READY_PAUSED | `59b45f77a` | — |
| C — evaluation | `feat/stqa-evaluation` | READY_PAUSED | `59b45f77a` | — |
| D — replay | `feat/stqa-replay` | READY_PAUSED | `59b45f77a` | — |
| E — video | `feat/stqa-video` | READY_PAUSED | `59b45f77a` | — |
| I — integration | `feat/spatiotemporal-video-qa` | READY_PAUSED | `59b45f77a` | — |

Only integration may update this board, merge lanes, resolve conflicts, or run real video/TemporalMemory gates.
