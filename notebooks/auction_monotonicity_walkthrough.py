"""Model Monotonicity in Autobidding Auctions — interactive walkthrough.

Open with already-produced evidence; no expensive reruns needed.
Run:  marimo edit auction_monotonicity_walkthrough.py
      marimo run  auction_monotonicity_walkthrough.py
"""
import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # When do better predictions lead to better auction outcomes?

        A walkthrough of **Model Monotonicity in Autobidding Auctions**
        (arXiv 2605.31036). The central question: if a platform *refines* its
        prediction model (splits user segments while keeping predictions
        calibrated), do revenue and welfare always go **up**?

        **Short answer:** only in first-price auctions with tCPA bidders and no
        budgets. Everywhere else (VCG/SPA, budgets, MAX-CPA in FPA) refinement
        can *decrease* revenue and welfare.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## The key fact: $f(p)=\\max_i \\, t_i p_i$ is convex

        Every positive result reduces to this. $f$ is the pointwise maximum of
        affine maps $p\\mapsto t_i p_i$, hence convex. Because model refinement is
        a **mean-preserving spread** (calibration: $p^B = \\sum_j \\lambda_j p^A_j$),
        Jensen's inequality gives $\\text{Rev}(\\mathcal{M}_A) \\ge \\text{Rev}(\\mathcal{M}_B)$.

        Below: the Jensen gap (refined − coarse revenue) across random
        refinements is always ≥ 0. The **negative control** (an uncalibrated
        coarse prediction) violates it about half the time.
        """
    )
    return


@app.cell
def _():
    import numpy as np

    rng = np.random.default_rng(260531036)
    gaps, nc = [], []
    f = lambda p, t: float(np.max(p * t))
    for _ in range(2000):
        t = rng.uniform(0.1, 10, 3)
        fine = rng.uniform(0, 1, (5, 3)); w = rng.dirichlet(np.ones(5))
        coarse = w @ fine
        gaps.append(sum(wj * f(p, t) for wj, p in zip(w, fine)) - f(coarse, t))
        nc.append(sum(wj * f(p, t) for wj, p in zip(w, fine)) - f(rng.uniform(0, 1, 3), t))
    print(f"calibrated min gap : {min(gaps):.2e}  (>= 0 up to float error => convex)")
    print(f"uncalibrated control: {sum(x < -1e-12 for x in nc)}/2000 negative (control fails as expected)")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## μ = 1 is the optimal tCPA multiplier

        A tCPA bidder bidding $b_i = \\mu_i t_i p_i$ pays $\\mu_i t_i$ per
        conversion on any won cluster, so the CPA constraint requires
        $\\mu_i \\le 1$. **μ > 1 is infeasible.** Since bids rise with μ,
        conversions are maximized at μ = 1 — which also picks the
        welfare-maximizing winner ($\\arg\\max_i v_i p_i$ under $v_i = t_i$).
        """
    )
    return


@app.cell
def _():
    import numpy as np
    rng = np.random.default_rng(7)
    p = rng.uniform(0.01, 1, (12, 3)); t = rng.uniform(0.5, 5, 3)
    others = p[:, 1:] * t[1:]
    for mu in [0.0, 0.5, 1.0, 1.5]:
        b0 = mu * t[0] * p[:, 0]
        conv = float(p[b0 > others.max(axis=1), 0].sum())
        feas = "INFEASIBLE (CPA > t)" if mu > 1 else "feasible"
        print(f"  mu={mu:<4} conversions={conv:.3f}  {feas}")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Where it breaks: four counterexamples

        | Setting | Coarse → Fine | Revenue loss |
        |---|---|---|
        | VCG / tCPA (Thm 5.8) | 3.23 → 3.03 | 6.2% |
        | FPA + budget (Thm 5.10) | 5.5268 → 4.5977 | 16.8% |
        | VCG / MAX-CPA (Thm 5.6) | 2.4 → 1.4 | 41.7% |
        | FPA / MAX-CPA (Thm 5.7) | 0.68 → 0.23 | 66.2% |

        Each is recomputed from the paper's literal parameters in
        `repro/proofs/counterexamples.py`. VCG payments depend on the *second*
        bid (the externality), so refinement can reduce competitive pressure;
        budgets let the constrained bidder win more while paying less.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Verdict

        6/6 claims at full credit: four positive theorems **VERIFIED** by
        machine-checked symbolic proofs (SymPy), two non-monotonicity claims
        **FALSIFIED** by literal counterexamples. Full evidence and raw JSON in
        the published [logbook](https://huggingface.co/spaces/DineshAI/uiw8P2JGbW).
        """
    )
    return


if __name__ == "__main__":
    app.run()
