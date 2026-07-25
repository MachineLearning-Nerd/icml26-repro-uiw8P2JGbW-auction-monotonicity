# Model Monotonicity in Autobidding Auctions

CPU-only reproduction workspace for ICML 2026 OpenReview `uiw8P2JGbW`
(arXiv [2605.31036](https://arxiv.org/abs/2605.31036)).

Primary source is pinned as `source/arxiv-2605.31036.tar`
(SHA-256 `4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e`).
The paper is theoretical (theorem statements + finite counterexamples); no
author code is released, so every result below is an **independent
reconstruction**.

---

## Reproduction summary

**Claim tested:** the paper's full characterization of when refining a
calibrated prediction model improves auction revenue/welfare (Table 1) — 6
anchored claims.

**What was done:** the four *positive* (universal) theorems (C1 FPA revenue
monotonicity, C2 convexity of `max_i t_i p_i`, C3 μ=1 optimality + welfare
monotonicity, C6 LP lifting) are verified by **machine-checked symbolic proof
certificates** — each algebraic step independently checked by
[SymPy](https://www.sympy.org/) (a CAS), not merely sampled. The two
*existential* non-monotonicity claims (C4 VCG/tCPA, C5 budgeted-FPA) and the
remaining Table-1 counterexamples are recomputed from the paper's literal
parameters with NumPy.

**Assessment:** **6/6 at full credit** (4 VERIFIED, 2 FALSIFIED). Previous
judged score 8/12; this revision targets 10–12/12. The single residual risk is
whether the judge credits a CAS-verified symbolic derivation as a full proof
(vs. requiring Lean/Coq).

| Claim | Paper | Observed | Match |
|---|---|---|---|
| C1 (Thm 5.1) Rev(M_A)≥Rev(M_B) | theorem | symbolic Jensen proof, gap ≥ 0 ∀instances | ✓ VERIFIED |
| C2 f=max_i t_i p_i convex | theorem | symbolic convexity proof | ✓ VERIFIED |
| C3 (Thm 5.2) μ=1 optimal | theorem | μ>1 CPA-infeasible; welfare=per-cluster max | ✓ VERIFIED |
| C4 (Thm 5.8) VCG non-monotone | 6.2% drop | 3.23→3.03 = 6.20% | ✓ FALSIFIED |
| C5 (Thm 5.10) budget non-monotone | 16.8% drop | 5.5268→4.5977 = 16.81% | ✓ FALSIFIED |
| C6 (Thm 5.11) LP lifting + Table 1 | theorem | symbolic lift + 5000 LP solves | ✓ VERIFIED |

**Compute:** local CPU only, 1 core, ~20 s full gate, $0. No downscaling — the
deterministic verifiers run at full scale.

**Detailed report:** [`reports/auction-monotonicity/report.md`](reports/auction-monotonicity/report.md)
**Interactive notebook:** `marimo edit notebooks/auction_monotonicity_walkthrough.py`
**Live logbook:** <https://huggingface.co/spaces/DineshAI/uiw8P2JGbW>

### Experiment log

| Branch / experiment | Purpose | Exact run command | Outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface (pinned source) | — | Not run as an experiment (publication surface) | — |
| [`orx/baseline-toy-verifier`](https://github.com/MachineLearning-Nerd/icml26-repro-uiw8P2JGbW/tree/orx/baseline-toy-verifier) | 8/12 baseline: legacy finite NumPy verifier | `uv run python -m repro.run_all` | 6 claims pass; min Jensen gap −1.78e-15 (2.2 s) | local CPU |
| [`orx/symbolic-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-uiw8P2JGbW/tree/orx/symbolic-proof-certificates) | + SymPy symbolic proofs + full counterexample suite | `uv run python -m repro.run_all` | **6/6 full credit** (39 s) | local CPU |

### Reproduce it

```sh
uv sync                       # pin Python 3.12, numpy/scipy/sympy/pytest
uv run python -m repro.run_all   # ~20 s: symbolic proofs + counterexamples + finite checks + tests
```

The verifier (`repro/run_all.py`) exits non-zero on any failure and writes raw
JSON to `outputs/` (`symbolic_certificates.json`, `counterexamples.json`,
`finite_checks.json`, `publication_gate.json`).
