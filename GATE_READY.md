# Publication gate readiness

**Paper:** arXiv:2605.31036 (`uiw8P2JGbW`)<br>
**Repository target:** `MachineLearning-Nerd/icml26-model-monotonicity-autobidding-auctions`<br>
**Overall paper-level status:** `INCONCLUSIVE`

## Claim disposition

| Claim | Disposition | Confidence | Evidence |
| --- | --- | --- | --- |
| C1 | `VERIFIED_CONDITIONAL` | Medium/High | SymPy Jensen certificate, Z3 no-counterexample check, 200,000 calibrated corroboration |
| C2 | `VERIFIED_CONDITIONAL` | High | Pointwise-max convexity certificate, Z3 check, and negative control |
| C3 | `VERIFIED_CONDITIONAL` | Medium/High | CPA feasibility, bid/revenue/welfare identities, Z3 checks, and 20,000-instance sweep |
| C4 | `COUNTEREXAMPLE_REPRODUCED` | High | Printed VCG/tCPA construction gives `3.23002→3.02970` revenue |
| C5 | `COUNTEREXAMPLE_REPRODUCED` | High | Printed budgeted-FPA construction gives `5.5267555→4.5977168` revenue |
| C6 | `VERIFIED_CONDITIONAL` | Medium/High | Symbolic/SMT LP lifting identity and 5,000 LP corroboration |

The counterexample verdicts support the paper’s existential non-monotonicity
claims. The conditional verification labels describe the repository’s
source-transcribed proof objects, not a foundational re-proof of every paper
assumption or external theorem.

## Source pin

```text
source/arxiv-2605.31036.tar  4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e
source/main.tex              aa6cdd42fa29a78804cdca8b1e93e2ab34454d17261f83797bab60a451fb06e8
```

## Fixed command

```bash
uv sync
uv run python -m repro.run_all
```

The gate output is [`outputs/publication_gate.json`](outputs/publication_gate.json).
The full branch lineage is recorded in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).
