"""Unit tests for the symbolic proof certificates (claims 1,2,3,6)."""
import numpy as np

from repro.proofs import symbolic


def test_lemma_pointwise_max_convex_verifies():
    cert = symbolic.lemma_pointwise_max_convex(n=4)
    assert "non-negative" in cert["verdict"]


def test_claim2_convexity_verifies():
    cert = symbolic.claim2_convexity(n=3)
    assert cert["verdict"].startswith("VERIFIED")
    assert len(cert["per_i_residual"]) == 3


def test_claim1_revenue_monotonicity_verifies():
    cert = symbolic.claim1_revenue_monotonicity(n_bidders=3, n_subclusters=4)
    assert cert["verdict"].startswith("VERIFIED")


def test_claim3_mu_one_optimality_covers_mu_gt_one():
    cert = symbolic.claim3_mu_one_optimality()
    assert cert["verdict"].startswith("VERIFIED")
    assert "mu <= 1" in cert["parts"]["feasibility"]
    assert "mu>1 infeasible" in cert["parts"]["feasibility"]


def test_claim3_mu_one_is_welfare_max():
    cert = symbolic.claim3_mu_one_optimality()
    assert "welfare" in cert["parts"]["welfare_argmax"].lower()


def test_claim6_lp_lifting_verifies():
    cert = symbolic.claim6_lp_lifting(n_bidders=2, n_sub=3)
    assert cert["verdict"].startswith("VERIFIED")


def test_symbolic_proofs_exit_nonzero_on_bogus_identity():
    """Negative control: a deliberately false identity must raise ProofError."""
    import sympy as sp
    with __import__("pytest").raises(symbolic.ProofError):
        symbolic._check_zero(sp.Symbol("x"), "bogus")
