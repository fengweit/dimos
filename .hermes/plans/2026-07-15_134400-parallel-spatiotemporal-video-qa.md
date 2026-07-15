# Parallel Spatiotemporal Video QA Implementation Plan

> **For Hermes:** After explicit scope approval, implement this plan through isolated worktrees and lane-specific durable micro-spec workers. Do not restart the existing serial cron.

**Goal:** Complete the spatiotemporal video-QA POC through five parallel, independently reviewable implementation lanes and one controlled integration lane.

**Architecture:** Freeze shared records and callable ports once on the integration branch, branch five isolated worktrees from that exact SHA, and assign disjoint file ownership. Each lane runs one micro-spec per worker invocation, commits and pushes only its branch, and records evidence in a lane-local ledger. A separate integration lane merges only green lane heads, runs cross-lane contract gates, and owns all real end-to-end demonstrations.

**Tech stack:** Python 3.12, Pydantic v2, pytest, Ruff, mypy, Git worktrees, Hermes detached workers, native Hermes cron watchdogs, OpenCV, existing DimOS YOLO-E and `TemporalMemory` APIs.

---

## 1. Current Baseline

- Integration repository: `/Users/tian/dimos`
- Writable remote: `fork=https://github.com/fengweit/dimos.git`
- Integration branch: `feat/spatiotemporal-video-qa`
- Current synchronized HEAD: `ba24dafe6e01711b145888ca4b9af42a1f4ca6ea`
- Complete through step `02a`; next serial step was `02b`.
- Existing serial cron `baab7a3d48e7` is paused and must be removed after the replacement jobs are verified.
- No detached worker is active.
- Hermes context configuration is `1,050,000` tokens with compression at `0.80` (~840,000 tokens).

## 2. Non-Negotiable Parallel-Safety Rules

1. Never run two editing workers in the same Git worktree.
2. Each lane has a dedicated branch, worktree, screen name, runtime directory, ledger, and cron job.
3. Lane workers may edit only their ownership globs plus their own ledger.
4. Shared contracts are integration-owned after the freeze commit. A lane may not modify them.
5. Each worker completes exactly one micro-spec, one focused review, one commit, one push, and one remote-SHA verification.
6. A lane with an interface problem writes an interface-change request and sets itself `BLOCKED`; it does not improvise a new shared API.
7. Only the integration lane merges branches, resolves cross-lane conflicts, modifies the global progress board, or runs real end-to-end gates.
8. No force push, amend, rebase, reset, stash, or broad `git add` in autonomous workers.
9. Default tests remain hermetic: no network, model weights, LFS assets, credentials, hardware, or real video.
10. Real video and real `TemporalMemory` execution remain mandatory integration gates.

## 3. Shared Interface Freeze (Bootstrap, Sequential)

This is the only prerequisite before parallel lanes start. It is performed on `feat/spatiotemporal-video-qa`, reviewed, committed, pushed, and recorded as `PARALLEL_BASE_SHA`.

### Bootstrap B1 — Freeze shared records

**Integration-owned files:**

- Modify: `dimos/benchmark/spatiotemporal/models.py`
- Modify: `dimos/benchmark/spatiotemporal/utilities.py`
- Create: `dimos/benchmark/spatiotemporal/ports.py`
- Modify: `dimos/benchmark/spatiotemporal/test_models.py`
- Create: `dimos/benchmark/spatiotemporal/test_ports.py`

**Freeze these public contracts:**

- `SpatialPredicate`: existing four values, unchanged.
- `TemporalPredicate`: exactly `before`, `after`.
- `QuestionKind`: exactly `spatial`, `temporal`.
- `RelationFact`: stable relation ID, episode/sample identity, subject/object IDs, spatial predicate, private evidence frame IDs.
- `RelationInterval`: stable private interval ID, relation ID, strict start/end frame and timestamp bounds.
- `Question`: spatial variant uses two object IDs and no references; temporal variant uses two relation references and no object IDs.
- `OracleAnswer`: expected Boolean plus private evidence references.
- `PredictionStatus`: `correct`, `incorrect`, `missing`, `invalid`.
- Public/oracle bundle manifest records and canonical schema version.

**Freeze these callable ports in `ports.py`:**

```python
class ObservationDetector(Protocol):
    def detect(self, image: Image) -> Sequence[DetectedObject]: ...
    def close(self) -> None: ...

class CandidateAnswerer(Protocol):
    def ingest_video(self, video_path: Path) -> CandidateReadiness: ...
    def answer(self, question: Question) -> str | bool | None: ...
    def close(self) -> None: ...
```

The exact `DetectedObject` and `CandidateReadiness` frozen records must contain only candidate/perception seam data; they must not expose oracle observations, intervals, answers, or evidence.

**Focused gate:**

```bash
uv run pytest \
  dimos/benchmark/spatiotemporal/test_models.py \
  dimos/benchmark/spatiotemporal/test_ports.py -v
uv run ruff check dimos/benchmark/spatiotemporal
uv run mypy
```

**Commit:**

```text
feat(benchmark): freeze parallel QA lane interfaces
```

### Bootstrap B2 — Materialize lane control plane

Create under `.hermes/plans/spatiotemporal-video-qa-parallel/`:

- `interfaces.md` — exact frozen fields, serialization examples, callable signatures, ownership rule.
- `board.md` — global lane state, base SHA, source/merged heads, integration status.
- `lanes/<lane>/steps/*.md` — short one-screen micro-specs.
- `lanes/<lane>/progress.md` — lane-local append-only ledger.
- `interface-change-requests/` — one file per blocked request.

Create lane scripts under `~/.hermes/scripts/` and runtime roots under `~/.hermes/run/dimos-spatiotemporal-<lane>/`. Scripts are machine-local and are not committed.

**Commit:**

```text
chore(benchmark): add parallel QA lane control plane
```

## 4. Lane Topology and Ownership

All lane branches start from the exact `PARALLEL_BASE_SHA` produced by B2.

| Lane | Branch | Worktree | Owned production files | Steps |
|---|---|---|---|---|
| A — Semantics | `feat/stqa-semantics` | `/Users/tian/dimos-worktrees/stqa-semantics` | `relations.py`, `intervals.py` | A1–A3 |
| B — Generation/bundles | `feat/stqa-dataset` | `/Users/tian/dimos-worktrees/stqa-dataset` | `questions.py`, `generation.py`, `bundles.py` | B1–B4 |
| C — Evaluation/candidate | `feat/stqa-evaluation` | `/Users/tian/dimos-worktrees/stqa-evaluation` | `scoring.py`, `runner.py`, `temporal_memory_answerer.py` | C1–C3 |
| D — Observation/replay | `feat/stqa-replay` | `/Users/tian/dimos-worktrees/stqa-replay` | `observation_io.py`, `replay.py` | D1–D2 |
| E — Video adapter | `feat/stqa-video` | `/Users/tian/dimos-worktrees/stqa-video` | `video_adapter.py`, `yoloe_adapter.py` | E1–E2 |
| I — Integration | `feat/spatiotemporal-video-qa` | `/Users/tian/dimos` | shared contracts, global board, demo/docs, merge conflict resolution | I1–I4 |

Each lane also exclusively owns matching `test_<module>.py` files and `.hermes/plans/spatiotemporal-video-qa-parallel/lanes/<lane>/progress.md`.

### Explicit shared-file denylist for lanes A–E

- `models.py`
- `utilities.py`
- `ports.py`
- `test_models.py`
- `test_ports.py`
- global `board.md`
- integration/demo documentation
- any other lane's files or progress ledger

A watchdog must reject a commit whose changed paths violate ownership.

## 5. Lane A — Spatial/Temporal Semantics

### A1 — Ambiguity and metamorphic spatial harness

- Harden equality-at-margin, overlap, containment, malformed margin, missing evidence, and input-order behavior.
- Add deterministic translation and mirror invariants.
- Files: `relations.py`, `test_relations.py`.
- Gate: `uv run pytest dimos/benchmark/spatiotemporal/test_relations.py -v`.
- Commit: `test(benchmark): harden spatial relation invariants`.

### A2 — Relation interval construction

- Coalesce consecutive accepted relation samples.
- Split on missing samples, identity changes, or relation changes.
- Reject conflicting frame/timestamp schedules.
- Files: `intervals.py`, `test_intervals.py`.
- Commit: `feat(benchmark): build replayable relation intervals`.

### A3 — Strict before/after

- Prove strict non-overlap only.
- Treat touching, overlap, containment, missing identity, and contradictory intervals as unknown.
- Add time-shift and input-order invariants.
- Commit: `feat(benchmark): derive strict temporal ordering`.
- Lane terminal state: `READY_FOR_INTEGRATION`.

## 6. Lane B — Deterministic Questions and Bundles

### B1 — Spatial-at questions

- Generate stable public spatial questions only from accepted relation facts.
- Keep answer/evidence/provenance private.
- Files: `questions.py`, `generation.py`, `test_generation.py`.
- Commit: `feat(benchmark): generate spatial-at questions`.

### B2 — Temporal questions and deterministic balance

- Consume frozen `RelationInterval`/`TemporalPredicate` contracts.
- Generate before/after positive and inverse cases without inventing labels.
- Produce deterministic family/polarity counts and byte-stable ordering.
- Commit: `feat(benchmark): generate balanced temporal questions`.

### B3 — Bundle writer and strict loader

- Public: metadata and questions only.
- Oracle: teacher observations, intervals, evidence, answers.
- Reject duplicate/foreign references.
- Files: `bundles.py`, `test_bundles.py`.
- Commit: `feat(benchmark): write replayable evaluation bundles`.

### B4 — Integrity, leakage, and path safety

- Verify hashes, corruption detection, path traversal rejection, public leakage scan, and root-independent canonical output.
- Commit: `test(benchmark): enforce bundle integrity and isolation`.
- Lane terminal state: `READY_FOR_INTEGRATION`.

## 7. Lane C — Scoring, Runner, and Candidate Adapter

### C1 — Typed prediction parsing

- Parse Boolean and explicit yes/no only.
- Preserve `correct`, `incorrect`, `missing`, and `invalid` statuses.
- Files: `runner.py`, `test_runner.py`.
- Commit: `feat(benchmark): parse typed candidate predictions`.

### C2 — Evidence-linked aggregate report

- Join public question, separately loaded oracle, prediction status, predicate/family, private evidence references, and source hash.
- Add always-yes, final-frame, and oracle diagnostic controls.
- Never expose oracle records to `CandidateAnswerer`.
- Files: `scoring.py`, `runner.py`, tests.
- Commit: `feat(benchmark): report evidence-linked candidate scores`.

### C3 — `TemporalMemory` candidate adapter seam

- Implement against frozen `CandidateAnswerer` only.
- Fake default tests verify video ingestion precedes questions and no teacher artifacts cross the boundary.
- Real implementation uses existing `TemporalMemory.color_image`, `get_state()`, and `query(question: str) -> str`; cleanup is mandatory.
- Files: `temporal_memory_answerer.py`, `test_temporal_memory_answerer.py`.
- Commit: `feat(benchmark): add a TemporalMemory candidate adapter`.
- Lane terminal state: `READY_FOR_INTEGRATION`.

## 8. Lane D — Canonical Observation IO and Replay

### D1 — Observation JSONL

- Canonical order and byte-stable strict round trip.
- Reject duplicate/conflicting IDs, NaN, malformed boxes, invalid timestamps, and non-NFC strings.
- Files: `observation_io.py`, `test_observation_io.py`.
- Commit: `feat(benchmark): persist canonical teacher observations`.

### D2 — Replay API/entry point

- Consume saved observations and call only the frozen generation/bundle API.
- Emit actionable insufficiency diagnostics.
- Prove separate roots yield identical logical bytes and hashes.
- Files: `replay.py`, `test_replay.py`.
- Commit: `feat(benchmark): replay observations into evaluation bundles`.
- Lane terminal state: `READY_FOR_INTEGRATION`.

## 9. Lane E — Video Sampling and YOLO-E Adaptation

### E1 — OpenCV sampler and fake detector seam

- Deterministic sampling timestamps and normalized coordinates.
- Fake detector produces canonical `ObjectObservation` records.
- Decode failure, invalid stride/dimensions, and cleanup are explicit.
- No model/network/LFS access in default tests.
- Files: `video_adapter.py`, `test_video_adapter.py`.
- Commit: `feat(benchmark): sample video into detector frames`.

### E2 — YOLO-E identity adapter

- Use existing `Yoloe2DDetector(prompt_mode=YoloePromptMode.PROMPT)`.
- Use `process_image()` for persisted tracking, and preserve `Detection2DBBox.track_id` populated by `result.boxes.id`.
- Permit the one-instance-per-prompt-class fallback only when native ID is `-1`; duplicate fallback labels fail.
- Keep heavy imports inside execution and call `stop()`/`close()` in `finally`.
- Record continuity/drop statistics.
- Files: `yoloe_adapter.py`, `test_yoloe_adapter.py`, adapter tests with fakes.
- Commit: `feat(benchmark): adapt YOLO-E video detections`.
- Lane terminal state: `READY_FOR_INTEGRATION`.

## 10. Interface Change Protocol

When a lane cannot proceed against the frozen contract:

1. Stop without changing shared files.
2. Create `interface-change-requests/<lane>-<sequence>.md` in the lane branch.
3. Include failing test, exact missing/incorrect contract, proposed minimal change, compatibility impact, and affected lanes.
4. Commit/push only the request and set lane state `BLOCKED_INTERFACE`.
5. Integration worker reviews the request, adds a shared-contract regression test, and either rejects it or lands a dedicated contract commit.
6. All lane workers stop at their next preflight until their branch contains the new contract SHA.
7. Rebase/merge-base updates are performed manually by the integration owner, never autonomously by lane workers.

No “temporary” duplicate type definitions are allowed in lane modules.

## 11. Cron and Worker Strategy

### Lane schedules

Use five staggered recurring watchdogs so startup and GitHub traffic do not spike simultaneously:

| Lane | Cron schedule | Screen name |
|---|---|---|
| A | `*/5 * * * *` | `dimos-stqa-semantics` |
| B | `1-59/5 * * * *` | `dimos-stqa-dataset` |
| C | `2-59/5 * * * *` | `dimos-stqa-evaluation` |
| D | `3-59/5 * * * *` | `dimos-stqa-replay` |
| E | `4-59/5 * * * *` | `dimos-stqa-video` |

Each cron is `no_agent=True`; its script is a lightweight watchdog that starts a durable detached Hermes worker only when that lane has no active screen and its ledger is runnable.

### Global resource guard

- At most four lane worker screens may be active simultaneously.
- A fifth watchdog exits silently and retries on its next tick.
- Each worktree shares the repository `.venv` read-only for dependencies; workers must not run `uv sync` concurrently.
- Heavy real model/video execution is forbidden in lanes and reserved for integration.

### Lane worker preflight

1. Verify exact worktree and branch.
2. Verify branch is synchronized with `fork/<lane-branch>`.
3. Verify `PARALLEL_BASE_SHA` and shared-contract hash match the board.
4. Verify changed paths are empty or owned by this lane.
5. Select exactly the earliest incomplete lane micro-spec.
6. Run RED-GREEN-REFACTOR, focused review, focused gate.
7. Update lane ledger, commit explicit files, push, verify remote SHA, exit.

### Integration watchdog

Create one separate integration watchdog on `*/10 * * * *`, initially paused. It may run only when no lane worker is editing and at least one lane head is `READY_FOR_INTEGRATION`. It never guesses through conflicts.

All six replacement cron jobs remain paused until bootstrap, worktree, branch, remote dry-run, and script verification gates pass.

## 12. Integration and Aggregation

### I1 — Merge lane heads

Merge in dependency order:

1. Lane A — semantics
2. Lane B — generation/bundles
3. Lane D — observation/replay
4. Lane E — video adapters
5. Lane C — scoring/candidate

For each lane:

```bash
git fetch fork
git merge --no-ff --no-edit fork/<lane-branch>
uv run pytest <lane focused tests> -v
uv run pytest dimos/benchmark/spatiotemporal -q
uv run ruff check dimos/benchmark/spatiotemporal
uv run mypy
git push fork feat/spatiotemporal-video-qa
```

Record source lane head and resulting integration head in `board.md`. If a merge conflicts outside lane-local ledgers, stop for root-cause review; do not auto-resolve.

### I2 — Real video to bundle

- Materialize an approved 15–30 second constrained video under repository artifact policy.
- Execute video sampler + YOLO-E + observation JSONL + replay + bundle generation.
- Require three consistent identities, one relation transition, both question families, at least 12 questions, and continuity/drop statistics.
- Replay saved observations in a separate root and compare canonical hashes.
- Commit: `feat(benchmark): generate an evaluation bundle from video`.

### I3 — Real `TemporalMemory` candidate

- Stream the same source video into actual `TemporalMemory`.
- Verify readiness using `get_state()` frame count/buffer/recent-window signals.
- Ask only public questions through `query()`.
- Persist normalized predictions and score with the separately loaded oracle.
- Inspect one correct and one non-correct trace; label any injected mutation as a harness diagnostic.
- Commit: `test(benchmark): verify a real TemporalMemory candidate`.

### I4 — One-command demo and final package

- Add `demo_spatiotemporal_qa.py` and `docs/development/spatiotemporal_video_qa.md`.
- Run every documented command from clean roots.
- Run full repository gates, secret/binary/path scan, replay determinism, and three-way final review.
- Set global board and ledger `COMPLETE`, push, verify remote HEAD, and prepare the upstream PR evidence.
- Commit: `docs(benchmark): add the spatiotemporal video QA demo`.

## 13. Validation Before Enabling Any Replacement Cron

- [ ] Bootstrap B1/B2 committed and pushed.
- [ ] `PARALLEL_BASE_SHA` recorded and remote verified.
- [ ] Five lane branches and worktrees exist at exactly that SHA.
- [ ] Every branch has a successful push dry-run to `fork`.
- [ ] File ownership globs are machine-validated and disjoint.
- [ ] Every lane spec references only frozen interfaces.
- [ ] Every watchdog and worker script passes `bash -n`.
- [ ] Each watchdog starts only its named worktree/branch.
- [ ] Global active-worker cap is tested.
- [ ] A dry-run worker exits without edits when no step is runnable.
- [ ] Existing serial cron is removed, not merely left enabled alongside new jobs.
- [ ] Replacement jobs are created paused; explicit approval is obtained before resume.

## 14. Risks and Controls

- **Shared API drift:** frozen integration-owned contracts and blocking RFC protocol.
- **Git corruption:** one worktree/branch per lane; no shared checkout; ownership enforcement.
- **Merge explosion:** disjoint production/test ownership and lane-complete merges.
- **Resource contention:** staggered schedules, four-worker cap, no concurrent dependency sync or heavy inference.
- **False progress:** lane-local real harness output, remote SHA verification, global board updated only by integration.
- **Long blocked dependency:** lanes implement against frozen interfaces; integration-only real gates are explicitly separated.
- **Private-oracle leakage:** candidate ports never contain teacher records; bundle and runner lanes have independent leakage tests.
- **Model/asset failure late:** E2 validates adapter semantics with fakes; I2/I3 remain hard real-world stop conditions.

## 15. Approval Boundary

This document is the proposed replacement strategy. In this turn:

- Context configuration was updated and verified.
- The serial cron was paused.
- No replacement branches, worktrees, scripts, commits, pushes, or cron jobs were created.

After explicit approval, execute Bootstrap B1/B2 first, present the frozen interface diff and control-plane verification, then create the paused lane jobs. Resume parallel implementation only after that bootstrap handoff is accepted.
