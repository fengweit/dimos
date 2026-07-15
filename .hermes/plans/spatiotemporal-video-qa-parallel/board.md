# Parallel Spatiotemporal Video-QA Board

AUTOMATION_STATUS: COMPLETE
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
| I — integration | `feat/spatiotemporal-video-qa` | COMPLETE | `1b9f7dae6` | `1b9f7dae6` |

Only integration may update this board, merge lanes, resolve conflicts, or run real video/TemporalMemory gates.

## Completed real gates

- Demo implementation: `1b9f7dae68e2023867dc20e90b4e7dfd122a6e14`.
- Real input: 25-second, 750-frame clip derived from the LFS-backed `assets/simple_demo.mp4`.
- Real YOLO-E 11s: two independent runs matched exactly; 5 sampled frames, 8 detections, 4 native IDs, no fallback IDs.
- Teacher output: 6 facts, 6 intervals, 54 questions (6 spatial, 48 temporal), isolated public/oracle bundles.
- Root-independent logical SHA-256: `ba4be04df7ed376925551bf998b6dce3fa08678665644ec0337c6eda6f9d62a9`.
- Real TemporalMemory plumbing: ready after 25 public frames, 5 windows, 3 state entities; timestamp-scripted fixture explicitly does not claim visual VLM quality.
- Candidate boundary: public questions/video only; evaluator owns oracle; 54 valid answers, 26 correct, 0 invalid/missing.
- Two complete command runs produced identical summary SHA-256 `610c4bba46705d2ba61240e904faed732199c2fe75d8bb8be86d36a7463bf491`.
- Final gates: 108 spatiotemporal tests passed; Ruff passed; mypy passed across 874 files; independent review passed.
