# ICML 2026 — Model Monotonicity in Autobidding Auctions

Independent reproduction and evidence audit for **“Model Monotonicity in
Autobidding Auctions: When Do Better Predictions Lead to Better Outcomes?”**

> **Current assessment: SCOPED GATE PASS; paper-level status INCONCLUSIVE.**
> The positive claims have source-transcribed symbolic/SMT certificates under
> the paper’s stated mechanism conventions. The negative claims have literal
> printed-parameter counterexamples. No author implementation or foundational
> proof-assistant development is included, so the repository does not claim to
> have independently re-proved every paper theorem from first principles.

## Paper

- **Author:** Ashwinkumar Badanidiyuru
- **Paper:** [arXiv:2605.31036](https://arxiv.org/abs/2605.31036)
- **OpenReview record:** [uiw8P2JGbW](https://openreview.net/forum?id=uiw8P2JGbW)
- **Venue:** ICML 2026
- **Source snapshot:** [`source/arxiv-2605.31036.tar`](source/arxiv-2605.31036.tar)
- **Live logbook:** [DineshAI/uiw8P2JGbW](https://huggingface.co/spaces/DineshAI/uiw8P2JGbW)

The paper studies whether refining a calibrated prediction model—splitting user
clusters into more informative sub-clusters—must improve auction revenue,
welfare, or liquid welfare. It analyzes target-CPA (tCPA) and maximum-CPA
(MAX-CPA) bidders across first-price, second-price/VCG, and budget-constrained
settings, plus a centralized LP benchmark.

## Claim-to-evidence ledger

| Claim | Paper result | Producer and evidence path | Current assessment | Scope and caveat |
| --- | --- | --- | --- | --- |
| **C1 — Theorem 5.1** | FPA revenue is monotone for calibrated refinement with tCPA bidders and uniform `μ=1` bidding | [`repro/proofs/symbolic.py`](repro/proofs/symbolic.py) proves the Jensen gap; [`repro/proofs/smt.py`](repro/proofs/smt.py) finds no LRA counterexample; [`repro/proofs/finite.py`](repro/proofs/finite.py) runs 200,000 calibrated cases | **VERIFIED CONDITIONALLY · MEDIUM/HIGH** | Depends on the paper’s calibrated-refinement and equilibrium conventions. SymPy/Z3 certify the reconstructed algebra, not a Lean/Coq formalization of the full paper. |
| **C2 — Theorem 5.1 mechanism** | `f(p)=max_i t_i p_i` is convex | `symbolic.py` checks every per-bidder residual; `smt.py` returns `unsat` for the modeled LRA counterexample search; the uncalibrated negative control fails | **VERIFIED CONDITIONALLY · HIGH** | The certificate covers the stated nonnegative-weight/affine model and its explicit convexity reduction. |
| **C3 — Theorem 5.2 + Corollary 5.3** | `μ=1` is optimal/feasible for tCPA FPA and gives welfare monotonicity when `v=t` | `symbolic.py` checks CPA, bid monotonicity, revenue-maximality, and welfare identities; `smt.py` checks the corresponding contradictions; `finite.py` tests 20,000 instances with an 81-point `μ∈[0,2]` grid | **VERIFIED CONDITIONALLY · MEDIUM/HIGH** | Uses the source’s uniform-bidding and equilibrium conventions; finite sweeps corroborate but do not establish the universal theorem. |
| **C4 — Theorem 5.8** | VCG/SPA revenue and welfare need not be monotone for tCPA bidders | [`repro/proofs/counterexamples.py`](repro/proofs/counterexamples.py) recomputes the printed four-auction construction: revenue `3.23002→3.02970` and welfare `3.23000→3.03000` | **COUNTEREXAMPLE REPRODUCED · HIGH** | Revenue loss is `6.2018%` (reported as `6.2%`). Printed decimals leave coarse bidder-A CPA at `10.00008` rather than exactly `10`; the residual is disclosed, not silently corrected. |
| **C5 — Theorem 5.10** | FPA revenue need not be monotone with a budget constraint | `counterexamples.py` recomputes the source parameters: revenue `5.5267555→4.5977168` and liquid welfare `5.526758→4.59770` | **COUNTEREXAMPLE REPRODUCED · HIGH** | Revenue loss is `16.8098%` (reported as `16.8%`). Printed decimals produce bidder-1 fine spend `3.1850168` against `B₁=3.185`; this `1.68×10⁻⁵` rounding residual is retained and disclosed. |
| **C6 — Theorem 5.11 + Table 1 LP row** | A coarse feasible LP solution lifts to every refined sub-cluster, so the LP optimum is monotone | `symbolic.py` and `smt.py` verify supply/budget/objective identities; `finite.py` solves 5,000 coarse/fine LP pairs with HiGHS | **VERIFIED CONDITIONALLY · MEDIUM/HIGH** | This is a centralized fractional LP benchmark, not a strategic auction equilibrium. LP solves are corroboration; the symbolic lifting identity is the primary evidence. |

The same counterexample producer also reconstructs the Table 1 MAX-CPA rows:
VCG revenue falls `2.4→1.4` while welfare rises `4.0→5.0`, and designated-profile
FPA revenue falls `0.68→0.23` with a `0.09%` welfare decrease. The latter is
explicitly a designated feasible-profile result, not a full MAX-CPA FPA
equilibrium characterization.

### What “verified” means here

`VERIFIED CONDITIONALLY` means that the repository’s source anchors, algebraic
identities, modeled quantifiers, and stated assumptions pass the committed
symbolic/SMT certificate. It does not mean that the external auction-theory
assumptions, every equilibrium-selection convention, or every universal paper
statement has been independently formalized in a foundational proof assistant.
`COUNTEREXAMPLE REPRODUCED` means that the source’s displayed finite
construction produces the claimed direction and percentage at printed
precision; it does not turn an existential result into a universal theorem.

## Reproduce

```bash
uv sync
uv run python -m repro.run_all
```

The one-command gate runs, in order:

1. SymPy symbolic certificates for C1, C2, C3, C6, and the MAX-CPA VCG
   welfare theorem;
2. a second Z3 linear-real-arithmetic checker for C1, C2, C3, and C6;
3. literal NumPy counterexamples for C4, C5, and the additional Table 1 rows;
4. finite NumPy/SciPy corroboration and negative controls;
5. the historical six-claim regression verifier; and
6. the scoped `pytest` suite.

The orchestrator is [`repro/run_all.py`](repro/run_all.py). It exits non-zero
when any stage fails and writes the machine-readable gate to
[`outputs/publication_gate.json`](outputs/publication_gate.json).

## Evidence map

| Artifact | Purpose |
| --- | --- |
| [`outputs/symbolic_certificates.json`](outputs/symbolic_certificates.json) | SymPy identities and non-negativity certificates |
| [`outputs/smt_certificates.json`](outputs/smt_certificates.json) | Independent Z3 contradiction checks |
| [`outputs/counterexamples.json`](outputs/counterexamples.json) | Printed-parameter C4/C5 and Table 1 reconstructions |
| [`outputs/finite_checks.json`](outputs/finite_checks.json) | Randomized, sweep, and LP corroboration |
| [`outputs/publication_gate.json`](outputs/publication_gate.json) | Aggregate status and evidence paths |
| [`reports/auction-monotonicity/report.md`](reports/auction-monotonicity/report.md) | Claim-by-claim narrative report |
| [`docs/PRIMARY_SOURCE_MAP.md`](docs/PRIMARY_SOURCE_MAP.md) | Source anchors and reconstruction boundaries |
| [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md) | Historical branch roles and final cleanup decision |

## Source provenance and limitations

The pinned source archive has SHA-256:

```text
source/arxiv-2605.31036.tar  4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e
source/main.tex              aa6cdd42fa29a78804cdca8b1e93e2ab34454d17261f83797bab60a451fb06e8
```

The paper source is accepted ICML TeX with one listed author and no released
author implementation. The positive certificates are independent CAS/SMT
reconstructions, while the finite checks are explicitly corroborative. The
auction model uses source-specific conventions: tCPA settings use binding
constraints and equilibrium multipliers; MAX-CPA FPA rows use designated
feasible profiles rather than a full equilibrium theorem; and the LP row is a
centralized benchmark. These distinctions are part of the result, not hidden
implementation details.

## Repository and branch policy

The clean public name for this repository is
`icml26-model-monotonicity-autobidding-auctions`. The former generated name was
`icml26-repro-uiw8P2JGbW-auction-monotonicity`. The historical `orx/*` branches
are documented in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md); both are ancestors of
the final `main`, with the symbolic-proof branch carrying the current
publication surface. After cleanup, `main` is the sole public branch and
reachable commits are attributed to `MachineLearning-Nerd`.

## Citation

```bibtex
@inproceedings{badanidiyuru2026model,
  title     = {Model Monotonicity in Autobidding Auctions: When Do Better Predictions Lead to Better Outcomes?},
  author    = {Ashwinkumar Badanidiyuru},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year      = {2026},
  eprint    = {2605.31036},
  archivePrefix = {arXiv},
  note      = {ICML 2026}
}
```

## Thank you

Thank you to Ashwinkumar Badanidiyuru for developing this careful analysis of
the interaction between prediction refinement, auction mechanisms, and
autobidding, and for making the formal paper source available. That source made
it possible to reconstruct the symbolic identities and the literal
counterexamples while keeping the mechanism conventions visible. This
repository is an independent reproduction and evidence audit; it does not
claim authorship of the paper’s work.
