# Frozen Parallel-Lane Interfaces

Schema: `spatiotemporal-video-qa/v1`
Integration branch: `feat/spatiotemporal-video-qa`
Writable remote: `fork=https://github.com/fengweit/dimos.git`

## Public stable identities

- `relation_id = relation_ + sha256(canonical_json({object_ids, predicate, schema_version}))`.
- Known relation vector: `relation_50c38f99a34ced799c3b8c8bd3417ac288a6ce9481dc9de19525042a2e4f5ea3`.
- `question_id = question_ + sha256(canonical_json({object_ids, predicate, question_kind, reference_ids, schema_version}))`.
- Known spatial vector: `question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e`.
- IDs are bundle-scoped in v1. Episode, text, sample coordinates, evidence, answers, paths, and private interval IDs never enter public preimages.
- Temporal questions reference exactly two distinct strict `RelationId` values. Private interval IDs never enter public questions.

## Frozen records

Authoritative definitions are integration-owned in `dimos/benchmark/spatiotemporal/models.py`:

- `SpatialPredicate`: `left-of`, `right-of`, `above`, `below`.
- `TemporalPredicate`: `before`, `after`.
- `QuestionKind`: `spatial`, `temporal`.
- `PredictionStatus`: `correct`, `incorrect`, `missing`, `invalid`.
- `RelationFact`: stable public relation ID plus private episode/sample identity and exactly its own evidence frame.
- `RelationInterval`: private interval ID, relation identity, inclusive frame/timestamp endpoints, and ordered evidence frames. Frame equality iff timestamp equality.
- `Question`: disjoint spatial and temporal variants; no answer/evidence fields.
- `OracleAnswer`: Boolean truth plus private frame and/or typed interval evidence.
- `BundleArtifact`, `PublicBundleManifest`, `OracleBundleManifest`: strict canonical relative paths, SHA-256 digests, derived bundle identity, and public-manifest binding.

## Frozen callable ports

Authoritative definitions are integration-owned in `dimos/benchmark/spatiotemporal/ports.py`:

```python
class ObservationDetector(Protocol):
    def detect(self, image: Image) -> Sequence[DetectedObject]: ...
    def close(self) -> None: ...

class CandidateAnswerer(Protocol):
    def ingest_video(self, video_path: Path) -> CandidateReadiness: ...
    def answer(self, question: Question) -> str | bool | None: ...
    def close(self) -> None: ...
```

`DetectedObject` contains only object ID, label, normalized box, and confidence. `CandidateReadiness` contains only readiness, ingested frame count, and an optional candidate-originated detail. No candidate-facing record may contain teacher observations, relation facts/intervals, answers, evidence, oracle manifests, or private roots.

## Frozen replay-generation seam

Authoritative integration-owned types live in `ports.py`:

```python
class ObservationBundleGenerator(Protocol):
    def generate(
        self,
        observations: Sequence[ObjectObservation],
        output_root: Path,
        source_video_sha256: str,
    ) -> ReplayBundleResult: ...
```

`ReplayBundleResult` returns matching public/oracle manifests and `logical_sha256`, defined as SHA-256 over canonical JSON containing those two manifest values; extraction-root paths never enter the preimage. The oracle manifest must bind the canonical newline-terminated public manifest bytes. Insufficiency uses `ReplayInsufficiencyError` with one of `empty_observations`, `mixed_episodes`, `no_relations`, or `no_questions`.

Authoritative concrete APIs already merged from Lane B are:

- `generation.generate_spatial_questions(facts)`
- `generation.generate_temporal_question_cases(intervals)`
- `bundles.write_bundle(...)`
- `bundles.load_bundle(root)`

D2 owns observation replay and may depend on an injected `ObservationBundleGenerator`; it must not duplicate relation/question/bundle implementations.

## Ownership and change protocol

`models.py`, `utilities.py`, `ports.py`, `test_models.py`, and `test_ports.py` are integration-owned. Lanes must stop and create `interface-change-requests/<lane>-<sequence>.md` rather than editing a shared contract or defining a duplicate type.
