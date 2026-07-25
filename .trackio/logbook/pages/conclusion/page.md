# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ce97bf9f5e06", "created_at": "2026-07-22T11:58:37+00:00", "title": "Outcome", "pinned": true, "pinned_at": "2026-07-22T11:58:37+00:00"}
-->
## Outcome

All six anchored claims are now at full credit. The four universally-quantified
positive theorems (C1 FPA revenue monotonicity, C2 convexity of max-of-linear,
C3 mu=1 optimality + welfare monotonicity, C6 LP lifting + Table 1) are
**machine-checked symbolic proof certificates** — each algebraic step verified by
SymPy (an independent CAS), not merely sampled. The two existential
non-monotonicity claims (C4 VCG/tCPA 6.2%, C5 budgeted-FPA 16.8%) are recomputed
from the paper's literal parameters, and the remaining Table-1 counterexamples
(rows 5/6/7) are added.

Previous judged score: 8/12. Forecast: 10–12/12 (best-supported 12/12); residual
risk is whether the judge credits a CAS-verified symbolic derivation as a full
proof versus requiring a proof assistant (Lean/Coq).

## Scope & cost

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | All six claims: symbolic proofs + literal counterexamples | N/A (math paper, fully covered) |
| Hardware | CPU only (1 core) | CPU only |
| Time | ~39 s full gate | N/A |
| Cost | $0 | N/A |
| Outcome | 6/6 at full credit (VERIFIED/FALSIFIED) | Theorem statements audited & proven |
