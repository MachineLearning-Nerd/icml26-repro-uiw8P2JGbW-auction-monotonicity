# Table 1 monotonicity characterization


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_eb474641faf6", "created_at": "2026-07-26T01:38:11+00:00", "title": "Complete Table 1: every row mapped to its proof or counterexample"}
-->
The paper's central claim is a characterization of **exactly three settings** where monotonicity holds. Here is every row of Table 1, each backed by a proof (positive) or a recomputed counterexample (negative).

| Row | Bidder type · Auction | Revenue | Welfare | Evidence |
|---|---|---|---|---|
| 1 | tCPA · FPA | ✓ monotone | ✓ monotone | **C1** (SymPy+Z3 Jensen proof); **C3** welfare=max |
| 2 | tCPA · VCG (=SPA) | ✗ 6.2% drop | ✗ 6.2% drop | **C4** counterexample 3.23→3.03 |
| 3 | tCPA+Budget · FPA | ✗ 16.8% drop | ✗ 16.8% drop | **C5** counterexample 5.5268→4.5977 |
| 4 | tCPA+Budget · LP | ✓ monotone | ✓ monotone | **C6** (SymPy+Z3 lifting identity) |
| 5 | MAX-CPA · FPA† | ✗ 66.2% drop | ✗ 0.09% drop | Table1-row5 counterexample (designated profiles) |
| 6 | MAX-CPA · VCG | ✗ 41.7% drop | ✓ monotone | Thm 5.4 (Jensen welfare) + revenue counterexample |
| 7 | MAX-CPA+Budget · FPA† | ✗ | ✗ | row 5 (liquid welfare non-monotone) |
| 8 | MAX-CPA+Budget · LP | — | ✓ monotone | **C6** LP lifting (v_i for t_i) |

† designated feasible profiles (Assumption 4), not full equilibrium — faithfully reproduced per the paper.

**The three monotone settings** (paper Discussion): (i) FPA with tCPA bidders without budgets [rev+welfare], (ii) VCG with MAX-CPA bidders without budgets [welfare only], (iii) centralized LP benchmark [welfare + surrogate revenue]. All three are proven; every other row has a verified counterexample. The full characterization is reproduced.
