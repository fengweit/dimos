# Parallel Spatiotemporal Video-QA Board

AUTOMATION_STATUS: REAL_GATES_PENDING
PARALLEL_BASE_SHA: 59b45f77ae8704f2602edebb091da4b6fd46c1cb
SHARED_CONTRACT_SHA: bd63c75357b291836ea8a51a208bb1968f8944c4
REMOTE: fork
INTEGRATION_BRANCH: feat/spatiotemporal-video-qa

> A commit cannot contain its own SHA. After this control-plane commit, the exact immutable lane base is written to `~/.hermes/run/dimos-spatiotemporal-control/PARALLEL_BASE_SHA`, used to create every branch/worktree, and verified against every lane HEAD before jobs can be resumed.

| Lane | Branch | State | Source head | Merged head |
|---|---|---|---|---|
| A — semantics | `feat/stqa-semantics` | MERGED | `d6a4cb57c` | `9a10721b2` |
| B — dataset | `feat/stqa-dataset` | MERGED | `7e32dc11d` | `3b3626401` |
| C — evaluation | `feat/stqa-evaluation` | MERGED | `8f23f1c62` | `42ed2baaa` |
| D — replay | `feat/stqa-replay` | MERGED | `236589dce` | `40028af68` |
| E — video | `feat/stqa-video` | MERGED | `48ca5c7af` | `5075d9026` |
| I — integration | `feat/spatiotemporal-video-qa` | REAL_GATES_PENDING | `42ed2baaa` | `42ed2baaa` |

Only integration may update this board, merge lanes, resolve conflicts, or run real video/TemporalMemory gates.
