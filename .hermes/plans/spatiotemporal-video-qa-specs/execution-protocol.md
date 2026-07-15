# Execution Protocol

## Ownership

The main agent owns all writes, RED/GREEN runs, git operations, interface decisions, and final acceptance. Subagents are read-only reviewers unless a separate worktree and explicit task are approved.

Never trust a subagent's success claim. Rerun every claimed check in the main worktree and inspect the resulting files or diff.

For unattended one-shot phase workers, do not use asynchronous `delegate_task`. Run each required independent review in a separate foreground, read-only Hermes subprocess and consume its result before the main worker continues.

## Per-behavior TDD loop

1. Add one focused behavioral test.
2. Run its exact pytest node ID.
3. Confirm the failure is caused by missing behavior—not syntax, import, or setup errors.
4. Implement the minimum behavior.
5. Run the exact test until green.
6. Run the current module tests.
7. Refactor only while green.
8. Run the phase gate before moving to the next behavior.

Do not write all tests first. Implement vertical slices one behavior at a time.

## Per-phase workflow

1. Read the phase spec and its prerequisite specs only.
2. Confirm the previous commit is green and the worktree is clean.
3. Dispatch the phase's pre-implementation reviewer, if listed.
4. Resolve findings in the intended test interface before production code.
5. Implement each behavior via the TDD loop.
6. Run the phase harness from `quality-gates.md`.
7. Dispatch specification-compliance review.
8. Fix accepted findings through failing regression tests.
9. Dispatch code-quality/adversarial review.
10. Fix accepted findings through failing regression tests.
11. Rerun the phase harness in the main worktree.
12. Inspect `git diff --check` and the staged diff.
13. Commit only the phase's coherent source, tests, and docs.

## Subagent assignments

### Before Phase 1

Run three independent read-only reviews. Interactive sessions may parallelize them; unattended one-shot workers run them as foreground subprocesses so every result is consumed:

- Contract reviewer: strict schema, public/oracle split, stable IDs, over-design.
- Geometry adversary: margins, equality, missing tracks, inverse relations.
- Repository reviewer: typing, test placement, imports, no `__init__.py`, dependencies.

### After every phase

Review sequentially:

1. Specification compliance.
2. Code quality and adversarial behavior.

### Specialized reviews

- Phase 2: geometry and metamorphic invariants.
- Phase 3: interval algebra and missing-evidence semantics.
- Phase 4: dataset balance and template leakage.
- Phase 5: filesystem security and oracle leakage.
- Phase 6: metric denominators and candidate/oracle isolation.
- Phase 8: detector API, stable identity, lifecycle cleanup.
- Phase 9: clean-shell documentation usability.

## Git discipline

Branch: `feat/spatiotemporal-video-qa`.

Each phase commit must be independently green. Never mix unrelated refactors, generated output, model assets, or videos into a phase commit. Push only after local gates pass because every push starts expensive CI.

## Stop policy

If a phase stop condition fails:

1. Do not continue to the next phase.
2. Add a minimal reproduction test.
3. Fix the root cause or reduce scope explicitly.
4. Update the phase spec if the approved contract changes.
5. Re-run all gates for that phase.
