# Release report — uiw8P2JGbW (arXiv 2605.31036)

**Model Monotonicity in Autobidding Auctions: When Do Better Predictions Lead
to Better Outcomes?**

## Current disposition

The repository gate passes its scoped symbolic, SMT, counterexample, finite, and
test stages. The paper-level status remains **INCONCLUSIVE** because there is no
author implementation and the positive routes are source-transcribed
reconstructions rather than foundational proofs of the complete auction model.

| Claim | Evidence status | Confidence | Limitation |
| --- | --- | --- | --- |
| C1, Theorem 5.1 | Conditional SymPy/Z3 Jensen certificate + 200,000 calibrated cases | Medium/High | Mechanism and refinement assumptions are modeled, not independently formalized in Lean/Coq |
| C2, Theorem 5.1 convexity | Conditional SymPy/Z3 pointwise-max certificate | High | Certificate covers the stated affine/nonnegative model |
| C3, Theorem 5.2/Cor. 5.3 | Conditional CPA/bid/welfare certificate + 20,000-instance sweep | Medium/High | Source equilibrium and uniform-bidding conventions are assumed |
| C4, Theorem 5.8 | Printed VCG/tCPA counterexample: `3.23002→3.02970` | High | `6.2018%` loss; CPA is `10.00008` at printed decimal precision |
| C5, Theorem 5.10 | Printed budgeted-FPA counterexample: `5.5267555→4.5977168` | High | `16.8098%` loss; fine spend exceeds printed budget by `1.68×10⁻⁵` due to rounding |
| C6, Theorem 5.11 | Conditional symbolic/SMT lifting identity + 5,000 LP solves | Medium/High | Centralized LP benchmark, not a strategic equilibrium |

Additional Table 1 counterexamples are retained in
`outputs/counterexamples.json`: MAX-CPA VCG revenue decreases while welfare
increases, and designated-profile MAX-CPA FPA revenue and welfare decrease.

## Fixed reproduction command

```bash
uv sync
uv run python -m repro.run_all
```

The gate runs the following evidence producers:

1. `repro/proofs/symbolic.py` — SymPy identities and nonnegative polynomial
   certificates;
2. `repro/proofs/smt.py` — independent Z3 LRA contradiction checks;
3. `repro/proofs/counterexamples.py` — literal printed-parameter reconstructions;
4. `repro/proofs/finite.py` — corroborative random, sweep, and LP checks;
5. `repro/src/verify_auction_claims.py` — historical finite regression; and
6. `repro/tests/` — scoped unit tests.

The gate manifest is [`outputs/publication_gate.json`](../../outputs/publication_gate.json).
The source map is [`docs/PRIMARY_SOURCE_MAP.md`](../../docs/PRIMARY_SOURCE_MAP.md),
and historical branch roles are in [`BRANCH_AUDIT.md`](../../BRANCH_AUDIT.md).

## Runtime and historical publication state

- Pinned source archive: SHA-256
  `4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e`.
- Full historical gate: approximately 17–39 seconds on one local CPU core;
  local cost `$0`.
- Previous live judged score: `8/12`.
- Historical Hugging Face revision: `db47def77ed891ac822e6bbaffe338b844e2884f`.
- No score increase is claimed until a live evaluator scores the renamed,
  cleaned repository.

## Citation and thanks

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

Thank you to Ashwinkumar Badanidiyuru for making the formal source available
and for developing this useful analysis of model refinement, auction design,
and autobidding. The source enabled this independent reconstruction to expose
its assumptions and rounding limits clearly.
