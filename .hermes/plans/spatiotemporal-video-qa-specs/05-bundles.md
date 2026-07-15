# Phase 5 — Replayable Public/Oracle Bundles

## Objective

Persist generated episodes as immutable, inspectable, leak-resistant bundles.

## Prerequisite

Phase 4 generates at least 12 stable cases.

## Files

- Create `dimos/benchmark/spatiotemporal/bundles.py`
- Create `dimos/benchmark/spatiotemporal/test_bundles.py`
- Modify contracts/utilities only when required by a failing test.

## Bundle contract

```text
<release>/
├── manifest.json
├── public/
│   ├── episode.json
│   └── questions.jsonl
└── oracle/
    ├── observations.jsonl
    ├── relation_intervals.jsonl
    └── answers.jsonl
```

## TDD behaviors

1. Atomic write to a fresh root.
2. Refuse overwrite.
3. Canonical JSON/JSONL.
4. Relative paths only.
5. SHA-256 manifest hashes.
6. Strict round-trip load.
7. Foreign-reference validation.
8. Duplicate/missing answers rejected.
9. Public-only load succeeds and exposes only source-video metadata/hash plus questions.
10. Leakage scanner catches teacher observations/boxes, answer/evidence/confidence/oracle/private paths.
11. Separate output roots produce identical logical bytes/hashes.
12. Traversal, symlink escape where applicable, and corrupted hashes fail.

## Hard harness

H0–H4.

## Reviews

Filesystem security/oracle-leakage review, then code-quality review.

## Deliverable

A temporary public/oracle release whose public half loads independently.

## Stop condition

Any oracle leakage, path escape, hash drift, or non-deterministic canonical artifact blocks Phase 6.

## Commit

```text
feat(benchmark): write replayable spatiotemporal bundles
```
