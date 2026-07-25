"""Unit tests for the counterexample recomputations (claims 4,5 + Table 1)."""
from repro.proofs import counterexamples as ce


def test_c4_vcg_tcpa_matches_six_point_two_pct():
    r = ce.c4_vcg_tcpa_nonmonotonicity()
    assert abs(r["revenue_loss_pct"] - 6.2) < 0.05
    assert abs(r["coarse_revenue"] - 3.23) < 1e-3   # paper rounds multipliers
    assert abs(r["fine_revenue"] - 3.03) < 1e-3
    assert abs(r["coarse_cpa_A"] - 10.0) < 1e-3
    assert abs(r["coarse_cpa_B"] - 1.0) < 1e-3


def test_c5_budgeted_fpa_matches_16_8_pct():
    r = ce.c5_budgeted_fpa_nonmonotonicity()
    assert abs(r["revenue_loss_pct"] - 16.8) < 0.05
    assert abs(r["coarse_revenue"] - 5.5268) < 1e-3
    assert abs(r["fine_revenue"] - 4.5977) < 1e-3
    assert abs(r["adv1_spend_coarse"] - 3.185) < 1e-3
    assert abs(r["adv1_spend_fine"] - 3.185) < 1e-3


def test_c5_liquid_welfare_matches_revenue_loss():
    r = ce.c5_budgeted_fpa_nonmonotonicity()
    assert abs(r["liquid_loss_pct"] - r["revenue_loss_pct"]) < 0.05


def test_vcg_maxcpa_revenue_drops_welfare_rises():
    r = ce.vcg_maxcpa_revenue_nonmonotonicity()
    assert abs(r["revenue_loss_pct"] - 41.7) < 0.1
    assert r["welfare_monotone"] is True
    assert r["fine_welfare"] > r["coarse_welfare"]


def test_maxcpa_fpa_revenue_and_welfare_drop():
    r = ce.maxcpa_fpa_nonmonotonicity()
    assert abs(r["revenue_loss_pct"] - 66.2) < 0.1
    assert abs(r["welfare_loss_pct"] - 0.09) < 0.01
