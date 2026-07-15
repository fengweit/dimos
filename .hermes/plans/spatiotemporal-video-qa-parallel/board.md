# Parallel Spatiotemporal Video-QA Board

AUTOMATION_STATUS: BOOTSTRAPPING
PARALLEL_BASE_SHA: MACHINE_LOCAL_AFTER_CONTROL_PLANE_COMMIT
SHARED_CONTRACT_SHA: bd63c75357b291836ea8a51a208bb1968f8944c4
REMOTE: fork
INTEGRATION_BRANCH: feat/spatiotemporal-video-qa

> A commit cannot contain its own SHA. After this control-plane commit, the exact immutable lane base is written to `~/.hermes/run/dimos-spatiotemporal-control/PARALLEL_BASE_SHA`, used to create every branch/worktree, and verified against every lane HEAD before jobs can be resumed.

| Lane | Branch | State | Source head | Merged head |
|---|---|---|---|---|
| A — semantics | `feat/stqa-semantics` | BOOTSTRAPPING | — | — |
| B — dataset | `feat/stqa-dataset` | BOOTSTRAPPING | — | — |
| C — evaluation | `feat/stqa-evaluation` | BOOTSTRAPPING | — | — |
| D — replay | `feat/stqa-replay` | BOOTSTRAPPING | — | — |
| E — video | `feat/stqa-video` | BOOTSTRAPPING | — | — |
| I — integration | `feat/spatiotemporal-video-qa` | BOOTSTRAPPING | — | — |

Only integration may update this board, merge lanes, resolve conflicts, or run real video/TemporalMemory gates.
