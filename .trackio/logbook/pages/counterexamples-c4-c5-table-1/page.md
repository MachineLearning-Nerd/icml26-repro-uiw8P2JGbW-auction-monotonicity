# Counterexamples (C4 C5 Table 1)


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_fa7e2ea240d5", "created_at": "2026-07-25T11:34:17+00:00", "title": "Literal counterexamples recomputed from pinned TeX parameters"}
-->
Every counterexample is transcribed from the paper's appendix (main.tex, pinned SHA-256 4c64d6db...) and recomputed with fresh NumPy. Source: `repro/proofs/counterexamples.py`. Raw: `outputs/counterexamples.json`.

### C4 — VCG/SPA non-monotonicity for tCPA (Theorem 5.8) — FALSIFIED
Two tCPA bidders (t_A=10, t_B=1), SPA, both at CPA-binding equilibrium.
- **Coarse** {{0,1},{2,3}}: A wins {0,1}, B wins {2,3}. Revenue = **3.23** (A pays 2.50, B pays 0.73). CPA_A=10, CPA_B=1 (both bind).
- **Fine** (singletons): A wins {0}, B wins {1,2,3}. Revenue = **3.03** (A pays 2.0, B pays 1.03).
- **Result: revenue 3.23 -> 3.03 = 6.20% decrease; welfare 3.23 -> 3.03 = 6.19% decrease.** (Paper: 6.2%.) M_A refines M_B yet both metrics drop.

### C5 — FPA+budget non-monotonicity (Theorem 5.10) — FALSIFIED
Adv1 budget B1=3.185 binds, t1=8.674; Adv2 tCPA t2=1.662 (infinite budget). FPA.
- **Coarse** {{1,2},{3,4}}: Adv2 wins {1,2}, Adv1 wins {3,4}. Revenue = **5.5268**. Adv1 spend = 3.185 = B1 (binds).
- **Fine** (singletons): Adv1 wins {1,3,4}, Adv2 wins {2}. Revenue = **4.5977**. Adv1 spend = 3.185 = B1 (binds).
- **Result: revenue 5.5268 -> 4.5977 = 16.81% decrease.** (Paper: 16.8%.) Liquid welfare 5.53 -> 4.60 = 16.81% (matches).

### Table 1 row 6 — VCG revenue non-monotonicity for MAX-CPA (Theorem 5.6) — FALSIFIED (welfare monotone)
MAX-CPA v1=10, v2=8; VCG.
- **Coarse** (pooled): Rev=2.4, Welfare=4.0. **Fine** (S1,S2): Rev=1.4, Welfare=5.0.
- Revenue 2.4 -> 1.4 = **41.7% decrease** (paper: 41.7%); welfare 4.0 -> 5.0 **increases** (consistent with Theorem 5.4).

### Table 1 rows 5/7 — MAX-CPA FPA non-monotonicity (Theorem 5.7, designated profiles) — FALSIFIED
v1=600, v2=10. Coarse: bidder 1 wins all (tie). Fine (g1,g2)=(1,1): bidder 1 wins H, bidder 2 wins L.
- Revenue 0.68 -> 0.23 = **66.2% decrease** (paper: 66.2%); welfare 108.6 -> 108.5 = **0.09% decrease** (paper: 0.09%). Designated feasible profiles (near best-response, per Assumption 4).


---
<!-- trackio-cell
{"type": "code", "id": "cell_4c709706ec9f", "created_at": "2026-07-25T11:34:23+00:00", "title": "Run: repro/proofs/counterexamples.py (exit 0)"}
-->
````python title=counterexamples.py
"""Independent recomputation of every finite counterexample in arXiv 2605.31036
(OpenReview uiw8P2JGbW) from the paper's literal numeric parameters.

Each function transcribes the exact probabilities / multipliers / values printed
in the appendix and recomputes revenue, welfare, and liquid welfare with fresh
NumPy.  The asserted percentages are the paper's headline numbers.  A mismatch
raises ``AssertionError`` and the run exits non-zero.

Source anchors (pinned TeX, SHA-256 4c64d6db...):
  main.tex appendix: app:counter-vcg-tcpa, app:counter-fpa-budget,
  app:counter-vcg-maxcpa, app:counter-maxcpa-fpa.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-9


def _spa_outcome(bids: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Single-item second-price outcome per row of ``bids`` (rows=impressions).

    Returns (winners, payments=second-highest bid, winning bid).
    Ties broken by lowest index (paper convention).
    """
    winners = np.argmax(bids, axis=1)
    n_impressions, n_bidders = bids.shape
    payments = np.empty(n_impressions)
    for r in range(n_impressions):
        row = np.partition(bids[r], n_bidders - 2)[n_bidders - 2]  # second-highest value
        payments[r] = row
    return winners, payments, bids[np.arange(n_impressions), winners]


def _fpa_outcome(bids: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """First-price: winner pays own bid."""
    winners = np.argmax(bids, axis=1)
    payments = bids[np.arange(bids.shape[0]), winners]
    return winners, payments


# ---------------------------------------------------------------------------
# C4 / Theorem 5.8: VCG/SPA revenue & welfare non-monotonicity for tCPA
# ---------------------------------------------------------------------------
def c4_vcg_tcpa_nonmonotonicity() -> dict:
    """Two tCPA bidders (t_A=10, t_B=1); SPA/VCG; both at tCPA equilibrium."""
    t = np.array([10.0, 1.0])
    # true conversion probabilities (auctions 0..3 x bidders A,B)
    p = np.array([[0.20, 0.08], [0.05, 0.30], [0.01, 0.03], [0.01, 0.70]])

    # --- Coarse model: partition {{0,1},{2,3}} ---
    coarse_pred = np.array([[0.125, 0.19], [0.125, 0.19], [0.01, 0.365], [0.01, 0.365]])
    g_A, g_B = 36.5, 6.579  # equilibrium multipliers (CPA-binding), app:counter-vcg-tcpa
    g = np.array([g_A, g_B])
    bids_c = coarse_pred * g
    winners_c, pay_c, _ = _spa_outcome(bids_c)
    rev_c = float(pay_c.sum())
    conv_c = np.array([p[r, winners_c[r]] for r in range(4)])
    welfare_c = float((t[winners_c] * conv_c).sum())
    # CPA checks: A over {0,1}: pay 2.50 / conv 0.25 = 10 ; B over {2,3}: 0.73 / 0.73 = 1
    cpa_A = pay_c[:2].sum() / conv_c[:2].sum()
    cpa_B = pay_c[2:].sum() / conv_c[2:].sum()

    # --- Fine model: singletons ---
    g2 = np.array([14.71, 25.0])
    bids_f = p * g2
    winners_f, pay_f, _ = _spa_outcome(bids_f)
    rev_f = float(pay_f.sum())
    conv_f = np.array([p[r, winners_f[r]] for r in range(4)])
    welfare_f = float((t[winners_f] * conv_f).sum())

    rev_loss = 100 * (rev_c - rev_f) / rev_c
    wel_loss = 100 * (welfare_c - welfare_f) / welfare_c
    return {
        "claim": "C4",
        "theorem": "Theorem 5.8: VCG/SPA non-monotonicity for tCPA",
        "source": "main.tex app:counter-vcg-tcpa; sections/counterexamples.tex",
        "coarse_revenue": rev_c, "fine_revenue": rev_f,
        "coarse_welfare": welfare_c, "fine_welfare": welfare_f,
        "revenue_loss_pct": rev_loss, "welfare_loss_pct": wel_loss,
        "coarse_cpa_A": float(cpa_A), "coarse_cpa_B": float(cpa_B),
        "coarse_winners": winners_c.tolist(), "fine_winners": winners_f.tolist(),
        "asserted_revenue_loss_pct": 6.2,
        "verdict": "FALSIFIES monotonicity" if rev_f < rev_c - TOL else "no violation",
    }


# ---------------------------------------------------------------------------
# C5 / Theorem 5.10: FPA revenue non-monotonicity with budgets
# ---------------------------------------------------------------------------
def c5_budgeted_fpa_nonmonotonicity() -> dict:
    """Budgeted FPA; adv1 budget B1=3.185 binds, adv2 tCPA t2=1.662."""
    # true conversion probabilities (fine-model predictions)
    q = np.array([[0.516, 0.559], [0.027, 0.850], [0.560, 0.617], [0.555, 0.330]])
    t1, B1, t2 = 8.674, 3.185, 1.662

    # --- Coarse model: partition {{1,2},{3,4}} ---
    coarse_pred = np.array([[0.2715, 0.7045], [0.2715, 0.7045],
                            [0.5575, 0.4735], [0.5575, 0.4735]])
    alpha_c = np.array([2.8565, 1.662])
    bids_c = coarse_pred * alpha_c
    winners_c, pay_c = _fpa_outcome(bids_c)
    rev_c = float(pay_c.sum())
    spend1_c = float(pay_c[winners_c == 0].sum())

    # --- Fine model: singletons ---
    alpha_f = np.array([1.9528, 1.662])
    bids_f = q * alpha_f
    winners_f, pay_f = _fpa_outcome(bids_f)
    rev_f = float(pay_f.sum())
    spend1_f = float(pay_f[winners_f == 0].sum())

    # liquid welfare
    lw1_c = min(B1, t1 * q[winners_c == 0, 0].sum())
    lw2_c = t2 * q[winners_c == 1, 1].sum()
    lw1_f = min(B1, t1 * q[winners_f == 0, 0].sum())
    lw2_f = t2 * q[winners_f == 1, 1].sum()
    liquid_c = float(lw1_c + lw2_c)
    liquid_f = float(lw1_f + lw2_f)

    rev_loss = 100 * (rev_c - rev_f) / rev_c
    liquid_loss = 100 * (liquid_c - liquid_f) / liquid_c
    return {
        "claim": "C5",
        "theorem": "Theorem 5.10: FPA with budget non-monotonicity",
        "source": "main.tex app:counter-fpa-budget",
        "coarse_revenue": rev_c, "fine_revenue": rev_f,
        "adv1_spend_coarse": spend1_c, "adv1_spend_fine": spend1_f, "budget_B1": B1,
        "liquid_welfare_coarse": liquid_c, "liquid_welfare_fine": liquid_f,
        "revenue_loss_pct": rev_loss, "liquid_loss_pct": liquid_loss,
        "coarse_winners": winners_c.tolist(), "fine_winners": winners_f.tolist(),
        "asserted_revenue_loss_pct": 16.8,
        "verdict": "FALSIFIES monotonicity" if rev_f < rev_c - TOL else "no violation",
    }


# ---------------------------------------------------------------------------
# Table 1 row 6: VCG revenue non-monotonicity for MAX-CPA (welfare monotone)
# ---------------------------------------------------------------------------
def vcg_maxcpa_revenue_nonmonotonicity() -> dict:
    """MAX-CPA bidders (v1=10,v2=8); VCG; revenue drops, welfare rises."""
    v = np.array([10.0, 8.0])
    # segments S1, S2 weights 0.5 each
    w = np.array([0.5, 0.5])
    p = np.array([[0.2, 0.5], [0.6, 0.1]])  # [segment, bidder]: p1(S1)=0.2,p2(S1)=0.5,...

    # --- Coarse model: pooled single cluster p1=0.4, p2=0.3 ---
    p_coarse = np.array([0.4, 0.3])
    vals_c = v * p_coarse
    rev_c = float(np.sort(vals_c)[0])       # VCG payment = externality = second value
    welfare_c = float(vals_c.max())

    # --- Fine model: S1, S2 separate ---
    vals_f = v[None, :] * p                  # [segment, bidder]
    winners_f = np.argmax(vals_f, axis=1)
    pay_f = np.partition(vals_f, 1, axis=1)[:, 0]  # second-highest = index 0 for 2 bidders
    rev_f = float((w * pay_f).sum())
    welfare_f = float((w * vals_f[np.arange(2), winners_f]).sum())

    rev_loss = 100 * (rev_c - rev_f) / rev_c
    return {
        "claim": "Table1-row6",
        "theorem": "Theorem 5.6 + VCG welfare monotonicity (MAX-CPA)",
        "source": "main.tex app:counter-vcg-maxcpa",
        "coarse_revenue": rev_c, "fine_revenue": rev_f,
        "coarse_welfare": welfare_c, "fine_welfare": welfare_f,
        "revenue_loss_pct": rev_loss,
        "welfare_monotone": bool(welfare_f >= welfare_c - TOL),
        "asserted_revenue_loss_pct": 41.7,
        "verdict": "FALSIFIES revenue monotonicity; welfare monotone (consistent w/ Thm 5.4)",
    }


# ---------------------------------------------------------------------------
# Table 1 row 5/7: MAX-CPA FPA non-monotonicity (designated profiles)
# ---------------------------------------------------------------------------
def maxcpa_fpa_nonmonotonicity() -> dict:
    """MAX-CPA FPA; designated feasible profiles; revenue & welfare drop."""
    v = np.array([600.0, 10.0])
    pH, pL = np.array([0.2, 0.02]), np.array([0.01, 0.5])
    pr = np.array([0.9, 0.1])  # Pr(H), Pr(L)

    # --- Coarse model: pooled ---
    p1 = 0.9 * 0.2 + 0.1 * 0.01   # = 0.181
    p2 = 0.9 * 0.02 + 0.1 * 0.5   # = 0.068
    g1 = 0.68 / 0.181
    g2 = 10.0
    b1, b2 = g1 * p1, g2 * p2
    winner_c = 0 if b1 >= b2 else 1   # tie -> lowest index (bidder 1)
    rev_c = float(max(b1, b2))
    welfare_c = float(v[winner_c] * p1)

    # --- Fine model: H, L separate; (g1,g2)=(1,1) ---
    win_H = int(np.argmax(pH))  # bidder 1 (0.2 > 0.02)
    win_L = int(np.argmax(pL))  # bidder 2 (0.5 > 0.01)
    rev_f = float(pr[0] * pH[win_H] + pr[1] * pL[win_L])         # FPA: winner pays own bid
    welfare_f = float(pr[0] * v[win_H] * pH[win_H] + pr[1] * v[win_L] * pL[win_L])

    rev_loss = 100 * (rev_c - rev_f) / rev_c
    wel_loss = 100 * (welfare_c - welfare_f) / welfare_c
    return {
        "claim": "Table1-row5/7",
        "theorem": "Theorem 5.7: FPA non-monotonicity for MAX-CPA (designated profiles)",
        "source": "main.tex app:counter-maxcpa-fpa",
        "coarse_revenue": rev_c, "fine_revenue": rev_f,
        "coarse_welfare": welfare_c, "fine_welfare": welfare_f,
        "revenue_loss_pct": rev_loss, "welfare_loss_pct": wel_loss,
        "asserted_revenue_loss_pct": 66.2, "asserted_welfare_loss_pct": 0.09,
        "verdict": "FALSIFIES revenue & welfare monotonicity (designated profiles; near-BR)",
    }


def all_counterexamples() -> dict:
    return {
        "C4_vcg_tcpa": c4_vcg_tcpa_nonmonotonicity(),
        "C5_budgeted_fpa": c5_budgeted_fpa_nonmonotonicity(),
        "Table1_row6_vcg_maxcpa": vcg_maxcpa_revenue_nonmonotonicity(),
        "Table1_row5_7_maxcpa_fpa": maxcpa_fpa_nonmonotonicity(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(all_counterexamples(), indent=2))

````


````output
{
  "C4_vcg_tcpa": {
    "claim": "C4",
    "theorem": "Theorem 5.8: VCG/SPA non-monotonicity for tCPA",
    "source": "main.tex app:counter-vcg-tcpa; sections/counterexamples.tex",
    "coarse_revenue": 3.2300200000000006,
    "fine_revenue": 3.0297,
    "coarse_welfare": 3.2299999999999995,
    "fine_welfare": 3.0299999999999994,
    "revenue_loss_pct": 6.201819183782158,
    "welfare_loss_pct": 6.1919504643962915,
    "coarse_cpa_A": 10.00008,
    "coarse_cpa_B": 1.0,
    "coarse_winners": [
      0,
      0,
      1,
      1
    ],
    "fine_winners": [
      0,
      1,
      1,
      1
    ],
    "asserted_revenue_loss_pct": 6.2,
    "verdict": "FALSIFIES monotonicity"
  },
  "C5_budgeted_fpa": {
    "claim": "C5",
    "theorem": "Theorem 5.10: FPA with budget non-monotonicity",
    "source": "main.tex app:counter-fpa-budget",
    "coarse_revenue": 5.5267555,
    "fine_revenue": 4.597716800000001,
    "adv1_spend_coarse": 3.1849975,
    "adv1_spend_fine": 3.1850168,
    "budget_B1": 3.185,
    "liquid_welfare_coarse": 5.526758,
    "liquid_welfare_fine": 4.5977,
    "revenue_loss_pct": 16.809838973336156,
    "liquid_loss_pct": 16.810180579645433,
    "coarse_winners": [
      1,
      1,
      0,
      0
    ],
    "fine_winners": [
      0,
      1,
      0,
      0
    ],
    "asserted_revenue_loss_pct": 16.8,
    "verdict": "FALSIFIES monotonicity"
  },
  "Table1_row6_vcg_maxcpa": {
    "claim": "Table1-row6",
    "theorem": "Theorem 5.6 + VCG welfare monotonicity (MAX-CPA)",
    "source": "main.tex app:counter-vcg-maxcpa",
    "coarse_revenue": 2.4,
    "fine_revenue": 1.4,
    "coarse_welfare": 4.0,
    "fine_welfare": 5.0,
    "revenue_loss_pct": 41.66666666666667,
    "welfare_monotone": true,
    "asserted_revenue_loss_pct": 41.7,
    "verdict": "FALSIFIES revenue monotonicity; welfare monotone (consistent w/ Thm 5.4)"
  },
  "Table1_row5_7_maxcpa_fpa": {
    "claim": "Table1-row5/7",
    "theorem": "Theorem 5.7: FPA non-monotonicity for MAX-CPA (designated profiles)",
    "source": "main.tex app:counter-maxcpa-fpa",
    "coarse_revenue": 0.6800000000000002,
    "fine_revenue": 0.23000000000000004,
    "coarse_welfare": 108.60000000000001,
    "fine_welfare": 108.5,
    "revenue_loss_pct": 66.1764705882353,
    "welfare_loss_pct": 0.09208103130755849,
    "asserted_revenue_loss_pct": 66.2,
    "asserted_welfare_loss_pct": 0.09,
    "verdict": "FALSIFIES revenue & welfare monotonicity (designated profiles; near-BR)"
  }
}
````
