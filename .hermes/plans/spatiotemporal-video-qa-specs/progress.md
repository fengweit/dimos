# Spatiotemporal Video QA Implementation Progress

AUTOMATION_STATUS: READY
CURRENT_PHASE: 2
CURRENT_STEP: 02a
LAST_COMPLETED_STEP: 01d

> Append-only execution ledger. Every micro-spec or blocker commit must update this file with real evidence and be pushed to the remote feature branch.

## Required entry format

```text
## Step NNx — <name>
State: COMPLETE | BLOCKED
Commit subject: <subject>
Changed files: <focused file list>
Delivered: <one replayable behavior>
Harness evidence:
- `<exact command>` → <actual result>
Reviews:
- Focused review: <result>
Blockers: none | <one actionable blocker>
Remote: origin/feat/spatiotemporal-video-qa at local HEAD
Next: Step NNx | stopped
```

## Micro-step status

| Step | Feature | State |
|---|---|---|
| 00 | Foundation and frozen contracts | COMPLETE |
| 01a | Strict contracts and canonical IDs | COMPLETE |
| 01b | One left-of relation | COMPLETE |
| 01c | One public question and private answer | COMPLETE |
| 01d | Exact score and tracer | COMPLETE |
| 02a | Inverse and vertical predicates | PENDING |
| 02b | Ambiguity and metamorphic harness | PENDING |
| 03a | Relation intervals and gaps | PENDING |
| 03b | Strict before and after | PENDING |
| 04a | Spatial-at question generation | PENDING |
| 04b | Temporal questions and balance | PENDING |
| 05a | Bundle writer and loader | PENDING |
| 05b | Hashes, leakage, and path safety | PENDING |
| 06a | Prediction parsing and statuses | PENDING |
| 06b | Evidence-linked report and candidate protocol | PENDING |
| 07a | Canonical teacher-observation JSONL | PENDING |
| 07b | Observation replay entry point | PENDING |
| 08a | Video sampler and fake detector seam | PENDING |
| 08b | YOLO-E adapter and identity contract | PENDING |
| 08c | Real video to eval bundle | PENDING |
| 09a | TemporalMemory candidate adapter | PENDING |
| 09b | Real candidate smoke and evidence report | PENDING |
| 09c | One-command demo and final package | PENDING |

## Execution entries

## Automation update — micro-specs and remote progress
State: COMPLETE
Commit subject: `docs(benchmark): split implementation into micro-specs`
Changed files: plan index, automation runner, progress ledger, and `steps/*.md`.
Delivered: Twenty-two independently reviewable checklists; each green unit has one focused harness, one progress update, one commit, and one verified remote push.
Harness evidence:
- Local Markdown link validation and `git diff --check` are required before this commit.
Reviews:
- Scope adjustment: explicitly requested by the user to prevent phase-sized implementation blobs.
Blockers: none
Remote: push and remote-HEAD verification required immediately after commit
Next: Step 01a — Strict contracts and canonical IDs

## Automation recovery — unattended review handoff
State: COMPLETE
Commit subject: `fix(benchmark): keep phase reviews synchronous`
Delivered: The detached phase worker now executes independent read-only reviews in foreground subprocesses instead of losing asynchronous delegation results when one-shot mode exits.
Harness evidence:
- `bash -n ~/.hermes/scripts/dimos_spatiotemporal_worker.sh` → passed before restart.
- First worker → stopped cleanly on unattended command-approval timeout; no files changed.
- Second worker → baseline tests and strict mypy passed, but exited after asynchronous review dispatch; no files changed.
Reviews:
- Automation behavior: root cause identified from two persisted worker logs.
- Repository integrity: branch remained clean and Phase 0 remained READY.
Blockers: none
Next: Phase 0 — Foundation and frozen contracts

## Phase 0 — Foundation and frozen contracts
State: COMPLETE
Commit subject: `chore(benchmark): record spatiotemporal QA baseline`
Delivered: A replayable repository/environment baseline and frozen v1 semantics for canonical observation ordering, duplicate rejection, strict temporal boundaries, stable IDs, and normalized uncertainty margins.
Baseline:
- Branch HEAD before this phase: `912874b6cdba6151397294889dc77744da716ece`.
- `origin/main`: `ce2c71a68b14f35a9e930e3c3821768587ea4c85`.
- Merge base with `origin/main`: `ce2c71a68b14f35a9e930e3c3821768587ea4c85`.
- Environment: macOS 26.5.2 (25F84), arm64, Python 3.12.13 at `.venv/bin/python`, uv 0.11.28 at `~/.local/bin/uv` satisfying repository requirement `>=0.9.17`.
- The tracked `uv.lock` is lock format version 1, revision 3. Git LFS is not installed, as required before Phase 8.
Harness evidence:
- `git status --short --branch` → clean `## feat/spatiotemporal-video-qa` before editing.
- `git fetch origin && git rev-parse origin/main && git rev-parse HEAD && git merge-base origin/main HEAD` → fetch passed; returned the SHAs recorded above.
- `sw_vers; uname -m; .venv/bin/python --version` → macOS 26.5.2 (25F84), arm64, Python 3.12.13.
- `uv --version` → `uv 0.11.28 (ebf0f43d7 2026-07-07 aarch64-apple-darwin)`, compatible with `pyproject.toml` requirement `>=0.9.17`.
- `uv sync --locked --group lint` → failed while building pre-existing transitive `pyaudio==0.2.14` because `portaudio.h` is unavailable; no repository files changed.
- `uv sync --locked --no-default-groups --group lint` → passed, resolved 471 packages, and synchronized the lint group.
- `uv pip install 'coverage==7.15.0' 'execnet==2.1.2' 'pytest-asyncio==0.26.0' 'pytest-cov==7.1.0' 'pytest-env==1.1.5' 'pytest-error-for-skips==2.0.2' 'pytest-mock==3.15.0' 'pytest-timeout==2.4.0' 'pytest-xdist==3.8.0'` → restored the 9 test-only packages removed by the lint-only sync at their locked versions.
- `./configure --prefix="$HOME/.local" --disable-mac-universal CFLAGS='-O2 -Wno-error=implicit-const-int-float-conversion' && make -j4 && make install` in PortAudio 19.7.0 source → installed the missing local PortAudio headers/library after the unmodified build exposed a new-clang warning-as-error.
- `install -m 644 /tmp/portaudio-19.7.0/include/pa_mac_core.h "$HOME/.local/include/pa_mac_core.h" && CFLAGS="-I$HOME/.local/include" LDFLAGS="-L$HOME/.local/lib -Wl,-rpath,$HOME/.local/lib" uv pip install 'pyaudio==0.2.14'` → built and installed the locked PyAudio package; import reported version 0.2.14.
- `uv sync --locked && uv sync --locked --group lint` → both passed; the exact default test and lint environments now synchronize from the lock.
- `uv run pytest dimos/perception/experimental/temporal_memory/test_temporal_memory_module.py -v` → final post-review run: 30 passed, 1 skipped in 4.05s; the skipped integration test requires `OPENAI_API_KEY`. The run emitted one pre-existing Python `ResourceWarning` for a still-running subprocess.
- `uv run mypy` → `Success: no issues found in 858 source files`.
- `command -v git-lfs` → unavailable, confirming Git LFS remains uninstalled.
Reviews:
- Every review below ran sequentially from the repository root as a separate foreground command of the form `$HOME/.local/bin/hermes --yolo chat --quiet -q '<role-specific read-only prompt>'`; each prompt prohibited file modification, commits, agent launches, and later-phase spec reads. The recorded Hermes session ID identifies the complete prompt and output.
- Contract pre-review (`20260715_110946_863d6c`): accepted the findings that duplicate keys, validation-before-sort, tri-state unknown filtering, canonical ID preimages, and exact normalized-margin formulas needed to be explicit. Accepted separate public/oracle artifacts and rejected additional encryption/service infrastructure as over-design.
- Geometry pre-review (`20260715_111058_dbb52e`): accepted strict edge-gap formulas, inverse-by-argument-swap, missing-evidence-as-unknown, and strict before/after tri-state semantics. Reconciled its one-frame-per-timestamp recommendation with object-level records by allowing multiple objects at one timestamp only when they share one `frame_id`.
- Repository pre-review (`20260715_111232_df0d97`): accepted exact command/environment evidence, namespace-package test placement, no new dependency, and explicit status-field updates. No `__init__.py` will be added under the new benchmark directories.
- Specification initial review (`20260715_111537_2d763e`) → FAIL. Accepted exact reviewer/tool evidence, canonical numeric-ID input, and chronological append findings. Its pending-review/completion-state finding was procedural and is resolved by recording both completed review cycles before commit. Repository-compatible uv is now available and its exact checks are recorded.
- Quality/adversarial initial review (`20260715_111805_4eed03`) → FAIL. Accepted one-to-one frame/timestamp identity, explicit spatial false semantics, explicit sample schedule, opaque public IDs, and stable-ID canonicalization findings. Its pending-review and missing-commit findings describe the expected pre-commit review state and are resolved by this review cycle and final commit.
- Specification follow-up (`20260715_112255_c1e50d`) → FAIL. Accepted its fixed-width floating-point representation, narrowed ID scope, exact review invocation, and package-restoration evidence findings. Its completion-state finding is resolved by returning the uncommitted ledger to Phase 0 `REVIEWING` until both follow-ups pass.
- Specification second follow-up (`20260715_112734_f2fdd0`) → FAIL. Accepted its exact JSON shape, Unicode, escaping, and omitted-versus-empty findings; the frozen question-ID preimage now uses a mandatory RFC 8785 object with no numeric fields.
- Specification third follow-up (`20260715_112930_cb38bf`) → PASS with non-blocking recommendations for a known-answer hash vector and exact per-kind vocabulary; both are now frozen below.
- Quality/adversarial follow-up (`20260715_113207_bed4d9`) → FAIL. Accepted malformed-box rejection, exact predicate/kind vocabulary and list roles, removal of private-derived temporal IDs, and an exact ordinary-`uv run` environment. Rejected capability restriction as unavailable to the mandated subprocess form; verified read-only worktree integrity instead.
- Quality/adversarial second follow-up (`20260715_114011_cf244b`) → FAIL. Accepted rejection of payloads on missing samples and exact relation-ID vocabulary/vector findings; both are frozen below.
- Quality/adversarial third follow-up (`20260715_114310_93e5b4`) → PASS with no blocking or non-blocking findings; both known-answer hashes were independently reproduced.
Frozen decisions:
- Out-of-order input: validate records and dataset-level conflicts first, then canonical-sort samples by `(timestamp_s, frame_id)` and object observations within each sample by `object_id` before processing or serialization. `timestamp_s` must be finite and `frame_id` a non-negative deterministic source-frame index. Each timestamp maps to exactly one frame ID and each frame ID to exactly one timestamp.
- Duplicate timestamps and identities: multiple objects may share a timestamp only within that single canonical sample. Reject the whole input on conflicting frame/timestamp mappings or any duplicate object ID within a sample, even if records are identical; duplicate artifact IDs are also rejected rather than resolved first/last-write-wins.
- Sampling and missing evidence: the canonical input explicitly enumerates the ordered sample schedule, including empty or explicitly missing samples; sparse object records alone never imply a schedule. Relation continuity is defined only across consecutive schedule entries. An entry where either object is absent or the sample is missing yields unknown and breaks continuity; no box carry-forward, interpolation, timestamp-gap heuristic, or false inverse is allowed.
- Strict temporal boundaries: `before(A, B)` is true only when `A.end_s < B.start_s`, and `after(A, B)` is exactly `before(B, A)`. The strict inverse proves false. Touching endpoints, overlap, containment, missing evidence, or unresolved interval identity are unknown; unknown cases are ineligible for generated Boolean questions and never encoded as false.
- Stable IDs: public object IDs are opaque NFC strings. Public relation-proposition IDs are `relation_<64 lowercase SHA-256 hex characters>` over RFC 8785 bytes of exactly `{"object_ids":[subject_id,object_id],"predicate":"...","schema_version":"spatiotemporal-video-qa/v1"}`, where `predicate` is exactly one of `left-of`, `right-of`, `above`, or `below`. Public question IDs are `question_<64 lowercase SHA-256 hex characters>` over RFC 8785 bytes of exactly `{"object_ids":[...],"predicate":"...","question_kind":"...","reference_ids":[...],"schema_version":"spatiotemporal-video-qa/v1"}`. All members are mandatory; arrays are never omitted or null. Strings must contain valid Unicode scalar values in NFC form; reject non-NFC input. For `spatial`, `predicate` is one of `left-of`, `right-of`, `above`, `below`, `object_ids` is exactly `[subject_id, object_id]`, and `reference_ids` is empty. For `temporal`, `predicate` is `before` or `after`, `object_ids` is empty, and `reference_ids` is exactly `[first_public_relation_id, second_public_relation_id]` in question-text order. No interval/evidence ID enters any public preimage. Exclude question text formatting, answers, evidence, coordinates/boxes, confidence, detector/tracker provenance, generation time, and paths; oracle records reference but never influence public IDs. Known relation vector: canonical bytes `{"object_ids":["obj_red","obj_blue"],"predicate":"left-of","schema_version":"spatiotemporal-video-qa/v1"}` produce `relation_50c38f99a34ced799c3b8c8bd3417ac288a6ce9481dc9de19525042a2e4f5ea3`. Known spatial-question vector: canonical bytes `{"object_ids":["obj_red","obj_blue"],"predicate":"left-of","question_kind":"spatial","reference_ids":[],"schema_version":"spatiotemporal-video-qa/v1"}` produce `question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e`. Before any later phase introduces another stable ID kind, it must freeze an equally exact public or private preimage and prefix.
- Normalized geometry and margins: boxes use top-left-origin `(x_min, y_min, x_max, y_max)`, with x divided by image width and y by image height. A present sample's box is malformed when it has wrong arity/type, a non-finite coordinate, or fails `0 <= x_min < x_max <= 1` and `0 <= y_min < y_max <= 1`; reject the whole input rather than converting malformed data to unknown. An explicitly missing sample must contain no object observations or boxes, and any payload on it is rejected. A single finite dimensionless margin `m` with `0 <= m <= 1` is applied axis-locally: `left-of(A,B)` iff `A.x_max + m < B.x_min`, and `above(A,B)` iff `A.y_max + m < B.y_min`; `right-of` and `below` swap arguments. A predicate is false only when its strict inverse is true. Equality at the margin, valid overlap/containment, self-relations, or missing objects are unknown and ineligible for Boolean question generation.
Blockers: none
Next: Phase 1 — Contracts and spatial tracer bullet

## Phase 1 — Tracer and contracts
State: COMPLETE
Commit subject: `feat(benchmark): add typed spatial QA tracer`
Changed files: `dimos/benchmark/spatiotemporal/{models,relations,questions,scoring,utilities}.py`, six colocated `test_*.py` files, and this progress ledger. No dependency, lockfile, `__init__.py`, generated output, video, weight, secret, or absolute source-artifact path was added.
Delivered: Strict immutable Pydantic observation/question/oracle/prediction/result contracts; canonical SHA-256 question IDs; normalized strict-margin `left-of`; answer-free public question/private oracle separation; exact Boolean scoring; and a replayable observation → relation → question → oracle → prediction → score tracer.
TDD evidence:
- Focused RED runs failed for missing strict bounds, observation constraints, strict-margin relation derivation, stable question construction, private oracle separation, exact scoring, canonical serialization, invalid margin/sample alignment, score-record ID alignment, self-relation filtering, finite timestamp translation, canonical question validation, candidate revalidation, and question/relation oracle alignment. Each corresponding focused test then passed after the minimal production change.
- `uv run pytest dimos/benchmark/spatiotemporal/test_questions.py::test_rejects_forged_relation_candidate_during_question_construction -v` → RED: failed because a forged threshold-equality candidate was accepted; GREEN: passed after downstream candidate revalidation.
- `uv run pytest dimos/benchmark/spatiotemporal/test_questions.py::test_rejects_private_oracle_for_an_unrelated_relation -v` → RED: failed because unrelated relation truth was accepted; GREEN: passed after executable-contract and episode alignment checks.
Harness evidence:
- `uv run pytest -q dimos/benchmark/spatiotemporal/test_utilities.py::test_serializes_strict_records_to_identical_canonical_json dimos/benchmark/spatiotemporal/test_relations.py::test_accepts_left_of_relation_only_above_strict_margin dimos/benchmark/spatiotemporal/test_tracer.py::test_observations_flow_to_public_question_private_oracle_and_score` → H0/H1/H2 passed: 3 passed in 0.01s.
- `uv run pytest dimos/benchmark/spatiotemporal -q` → 16 passed in 0.02s. The command emitted the same pre-existing uv/Python subprocess `ResourceWarning` recorded in the Phase 0 baseline; the Phase 1 tests emitted no package warning.
- `uv run ruff format --check dimos/benchmark/spatiotemporal && uv run ruff check dimos/benchmark/spatiotemporal` → 11 files already formatted; all checks passed.
- `uv run mypy` → `Success: no issues found in 863 source files`.
- `git diff --check` → passed with no output.
Replayable artifact:
- `dimos/benchmark/spatiotemporal/test_tracer.py::test_observations_flow_to_public_question_private_oracle_and_score`; replay with `uv run pytest dimos/benchmark/spatiotemporal/test_tracer.py -v`.
Reviews:
- Every completed review ran sequentially from the repository root as a separate foreground `$HOME/.local/bin/hermes --yolo chat --quiet -q '<read-only prompt>'` command. Prompts prohibited modifications, commits, tests where requested, agent launches, and later-phase spec reads.
- Specification follow-up (`20260715_122152_4226a6`) → FAIL. Accepted finite margin and same-sample validation, valid Unicode scalar enforcement, same-object filtering, and a full end-to-end tracer. The scalar rejection was already provided by Pydantic and proved by regression test, then made explicit at the contract boundary.
- Specification follow-up (`20260715_122508_c18e51`) → FAIL. Accepted finite negative timestamp translation and immediately-below/at/above threshold coverage.
- Specification follow-up (`20260715_123330_7e6bc6`) → FAIL. Accepted explicit Unicode-scalar validation. Rejected missing ledger evidence as procedural before final harness execution and ledger update.
- Quality/adversarial initial review (`20260715_123606_b8bf42`) → FAIL. Accepted canonical Question ID/self-relation validation, forged-candidate revalidation, question/relation oracle alignment, scoring-ID alignment, and always-yes false-truth coverage. Rejected a durable public relation-proposition model as outside Phase 1 because the phase explicitly permits a temporary relation candidate; deferred non-blocking evidence/result hardening.
- Quality/adversarial follow-up (`20260715_125327_39ceee`) → PASS with no blockers. Non-blocking suggestions were evidence-frame constraints and direct `QuestionResult.correct` consistency; scorer/builder outputs are valid and those broader contract refinements are deferred.
- Specification final (`20260715_125607_6deb28`) → PASS with no blockers and confirmed the complete tracer, strict contracts, canonical IDs, relation boundary semantics, candidate/oracle revalidation, and separate-oracle exact scoring.
Blockers: none
Remote: not pushed; the one-run contract explicitly forbids remote push.
Next: Phase 2 — Spatial predicates and ambiguity, beginning with Step 02a.
