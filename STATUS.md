# Status — ICML 2026 autobidding auction monotonicity

Paper ID: `uiw8P2JGbW`<br>
Paper: [arXiv:2605.31036](https://arxiv.org/abs/2605.31036)<br>
Target repository: `MachineLearning-Nerd/icml26-model-monotonicity-autobidding-auctions`

## Current scientific status

**Scoped gate: PASS. Paper-level reproduction: INCONCLUSIVE.**

- C1, C2, C3, and C6 have conditional source-transcribed symbolic/SMT
  certificates under the paper’s stated model conventions.
- C4 and C5 reproduce the paper’s finite non-monotonicity counterexamples at
  printed precision.
- The additional Table 1 MAX-CPA counterexamples are also reconstructed.
- No author implementation is available; finite checks corroborate the proof
  and counterexample routes but do not establish universal claims.
- The positive certificates use SymPy and Z3, not a foundational proof
  assistant. MAX-CPA FPA uses designated feasible profiles, and the LP row is a
  centralized benchmark rather than a strategic equilibrium.

## Evidence

- C1/C2 calibrated Jensen corroboration: `200,000` cases; uncalibrated control
  violations: `100,714`.
- C3 sweep: `20,000` instances and an `81`-point `μ∈[0,2]` grid.
- C6 LP corroboration: `5,000` coarse/fine HiGHS solves, zero violations.
- C4 revenue: `3.23002 → 3.02970` (`6.2018%` decrease).
- C5 revenue: `5.5267555 → 4.5977168` (`16.8098%` decrease).
- Printed-decimal residuals are retained: C4 coarse CPA is `10.00008` versus
  target `10`; C5 fine spend is `3.1850168` versus budget `3.185`.
- Historical live judged score: `8/12`; no new score is claimed.

## Reproduce

```bash
uv sync
uv run python -m repro.run_all
```

The gate writes its manifest to
[`outputs/publication_gate.json`](outputs/publication_gate.json). Evidence and
source anchors are summarized in [`README.md`](README.md) and
[`docs/PRIMARY_SOURCE_MAP.md`](docs/PRIMARY_SOURCE_MAP.md).

## Repository cleanup

- Former name: `icml26-repro-uiw8P2JGbW-auction-monotonicity`.
- Clean name: `icml26-model-monotonicity-autobidding-auctions`.
- Historical branch roles and ancestry: [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).
- Final public branch policy: `main` only.
- Final reachable commit attribution: `MachineLearning-Nerd`.
- Citation and author thank-you note: [`README.md`](README.md).
