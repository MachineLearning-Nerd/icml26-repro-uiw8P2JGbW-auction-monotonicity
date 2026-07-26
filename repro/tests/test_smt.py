"""Unit tests for the Z3 SMT proofs (second independent checker)."""
from repro.proofs import smt


def test_c2_convexity_smt_unsat():
    assert smt.c2_convexity(n=3)["result"].startswith("unsat")


def test_c1_jensen_smt_unsat():
    assert "unsat" in smt.c1_jensen(n_bidders=2, n_sub=3)["result"]


def test_c3_smt_covers_all_three_parts():
    c = smt.c3_mu_one_optimality()
    assert "feasibility" in c["facts"]
    assert "bid_monotone" in c["facts"]
    assert "revenue_max" in c["facts"]


def test_c6_lp_identity_smt_unsat():
    assert "unsat" in smt.c6_lp_identity(n_bidders=2, n_sub=2)["result"]
