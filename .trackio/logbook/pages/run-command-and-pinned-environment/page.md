# Run command and pinned environment


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ae869fa6b217", "created_at": "2026-07-25T11:35:02+00:00", "title": "Exact command, pinned environment, seeds, runtime"}
-->
### Fixed run command (identical on every node)
```
uv run python -m repro.run_all
```
`uv run` auto-syncs the environment from the committed `uv.lock`. The command is a fixed contract; children vary only committed code.

### Pinned environment (`pyproject.toml` + `uv.lock`)
- Python 3.12.11 (requires-python >=3.11,<3.14)
- numpy 2.5.1, scipy 1.18.0, sympy 1.14.0, pytest 8.4.2, mpmath 1.3.0
- Environment manager: **uv** (no conda). One repo-level `.venv`.

### Deterministic seeds
- C1/C2 Jensen: `np.random.default_rng(260531036)`
- C3 mu-optimality: `default_rng(260531037)`
- C6 LP solves: `default_rng(260531038)`
- Counterexamples: literal constants (no randomness).

### Compute and runtime
- Backend: **local CPU** (1 core, Apple Silicon). All tasks < 5 min, 1 core.
- Baseline run (legacy verifier): **2.2 s**. Full gate (symbolic + counterexamples + finite + tests): **~39 s**.
- Cost: $0.

### Git provenance
- Baseline root branch: `orx/baseline-toy-verifier` @ ${BASELINE_SHA:0:12} (8/12 reference)
- Winning child branch: `orx/symbolic-proof-certificates` @ ${CHILD_SHA:0:12}
- Experiment tree: root (baseline-toy-verifier) -> child (symbolic-proof-certificates).

### Source pin
arXiv 2605.31036 source tar, SHA-256 `4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e`.
