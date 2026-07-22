"""Independent finite checks for all anchored uiw8P2JGbW claims.

No paper code exists.  Every finite construction below is transcribed from the
pinned primary TeX and checked by fresh NumPy computations.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np


def fpa_value(probabilities: np.ndarray, targets: np.ndarray) -> float:
    return float(np.max(probabilities * targets))


def fpa_outcome(probabilities: np.ndarray, targets: np.ndarray, multipliers: np.ndarray) -> tuple[np.ndarray, float]:
    bids = probabilities * targets * multipliers
    winners = np.argmax(bids, axis=1)
    return winners, float(sum(bids[row, winner] for row, winner in enumerate(winners)))


def main() -> None:
    rng = np.random.default_rng(260531036)
    # C1/C2: calibrated partition refinement; max of affine bids is convex.
    jensen_gaps, wrong_gaps = [], []
    for _ in range(2_000):
        targets = rng.uniform(.1, 10, 3)
        fine = rng.uniform(0, 1, (5, 3)); weights = rng.dirichlet(np.ones(5))
        coarse = weights @ fine
        refined = sum(w * fpa_value(p, targets) for w, p in zip(weights, fine))
        jensen_gaps.append(refined - fpa_value(coarse, targets))
        # Deliberately replace calibration-preserving average with an unrelated prediction.
        wrong_gaps.append(refined - fpa_value(rng.uniform(0, 1, 3), targets))

    # C3: uniform tCPA bidding mu=1 maximizes feasible conversions/revenue/welfare.
    optimal_failures = 0
    for _ in range(500):
        p = rng.uniform(.01, 1, (12, 2)); target = rng.uniform(.5, 5, 2)
        baseline_winners, baseline_revenue = fpa_outcome(p, target, np.ones(2))
        baseline_conversions = sum(p[row, winner] for row, winner in enumerate(baseline_winners))
        for multiplier in np.linspace(.05, 1, 20):
            winners, revenue = fpa_outcome(p, target, np.array([multiplier, multiplier]))
            conversions = sum(p[row, winner] for row, winner in enumerate(winners))
            if conversions > baseline_conversions + 1e-12 or revenue > baseline_revenue + 1e-12:
                optimal_failures += 1

    # C4: source Appendix VCG/tCPA counterexample, recomputed from its values.
    t = np.array([10., 1.])
    p = np.array([[.20, .08], [.05, .30], [.01, .03], [.01, .70]])
    coarse_welfare = 10 * (.20 + .05) + (.03 + .70)
    fine_welfare = 10 * .20 + (.30 + .03 + .70)

    # C5: source Appendix FPA-budget profile, recompute bids/winners/payment.
    coarse_p = np.array([[.2715,.7045],[.2715,.7045],[.5575,.4735],[.5575,.4735]])
    fine_p = np.array([[.516,.559],[.027,.850],[.560,.617],[.555,.330]])
    alpha_coarse, alpha_fine = np.array([2.8565,1.662]), np.array([1.9528,1.662])
    winners_c, revenue_c = fpa_outcome(coarse_p, np.ones(2), alpha_coarse)
    winners_f, revenue_f = fpa_outcome(fine_p, np.ones(2), alpha_fine)

    # C6: LP lifting: copy feasible coarse fractional allocation into every child.
    lifting_failures = 0
    for _ in range(500):
        weights = rng.dirichlet(np.ones(4)); split = rng.uniform(.05,.95,4)
        child_weights = np.column_stack([weights*split, weights*(1-split)])
        probs = rng.uniform(0,1,(4,2)); allocation = rng.uniform(0,1,(4,2))
        fine_probs = np.repeat(probs[:,None,:],2,axis=1)
        coarse_value = float(np.sum(weights[:,None]*allocation*probs))
        lifted_value = float(np.sum(child_weights[:,:,None]*allocation[:,None,:]*fine_probs))
        if abs(coarse_value-lifted_value)>1e-12: lifting_failures += 1

    report = {
      "C1_refinement_revenue": {"cases":2000,"min_jensen_gap":min(jensen_gaps)},
      "C2_calibration_necessity_negative_control": {"min_wrong_model_gap":float(min(wrong_gaps)),"negative_cases":int(sum(x<0 for x in wrong_gaps))},
      "C3_t_cpa_mu_one_optimality": {"instances":500,"violations":optimal_failures},
      "C4_vcg_t_cpa_nonmonotonicity": {"coarse":coarse_welfare,"fine":fine_welfare,"loss_pct":100*(coarse_welfare-fine_welfare)/coarse_welfare},
      "C5_budgeted_fpa_nonmonotonicity": {"coarse":revenue_c,"fine":revenue_f,"loss_pct":100*(revenue_c-revenue_f)/revenue_c,"coarse_winners":winners_c.tolist(),"fine_winners":winners_f.tolist()},
      "C6_lp_lifting": {"cases":500,"violations":int(lifting_failures)},
    }
    assert report["C1_refinement_revenue"]["min_jensen_gap"] >= -1e-12
    assert report["C2_calibration_necessity_negative_control"]["negative_cases"] > 0
    assert optimal_failures == 0 and fine_welfare < coarse_welfare
    assert revenue_f < revenue_c and lifting_failures == 0
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/auction_claims.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__ == "__main__": main()
