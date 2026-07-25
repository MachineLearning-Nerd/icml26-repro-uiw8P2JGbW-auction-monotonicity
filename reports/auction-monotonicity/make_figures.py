"""Generate the figures used in the visual report (reports/auction-monotonicity/images/)."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "reports" / "auction-monotonicity" / "images"
IMG.mkdir(parents=True, exist_ok=True)


def fig_jensen_gap():
    """Headline: Jensen gap >= 0 across 2000 calibrated refinements vs negative control."""
    rng = np.random.default_rng(260531036)
    gaps, nc = [], []
    for _ in range(2000):
        t = rng.uniform(0.1, 10, 3)
        fine = rng.uniform(0, 1, (5, 3)); w = rng.dirichlet(np.ones(5))
        coarse = w @ fine
        f = lambda p: float(np.max(p * t))
        gaps.append(sum(wj * f(p) for wj, p in zip(w, fine)) - f(coarse))
        nc.append(sum(wj * f(p) for wj, p in zip(w, fine)) - f(rng.uniform(0, 1, 3)))
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.hist(gaps, bins=60, alpha=0.8, label="calibrated refinement (Jensen gap)", color="#2a7fff")
    ax.hist(nc, bins=60, alpha=0.55, label="uncalibrated control", color="#d62728")
    ax.axvline(0, color="k", lw=1, ls="--")
    ax.set_xlabel("refined − coarse revenue gap")
    ax.set_ylabel("instances")
    ax.set_title("FPA revenue monotonicity: Jensen gap is non-negative\n(calibration is necessary — control violates it)")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(IMG / "jensen_gap.png", dpi=150); plt.close(fig)


def fig_counterexamples():
    """Counterexample headline: revenue/welfare drop under refinement for the 4 settings."""
    ce = json.loads((ROOT / "outputs" / "counterexamples.json").read_text())
    rows = [
        ("VCG/tCPA\n(Thm 5.8)", ce["C4_vcg_tcpa"]["revenue_loss_pct"]),
        ("FPA+budget\n(Thm 5.10)", ce["C5_budgeted_fpa"]["revenue_loss_pct"]),
        ("VCG/MAX-CPA\n(Thm 5.6)", ce["Table1_row6_vcg_maxcpa"]["revenue_loss_pct"]),
        ("FPA/MAX-CPA\n(Thm 5.7)", ce["Table1_row5_7_maxcpa_fpa"]["revenue_loss_pct"]),
    ]
    labels = [r[0] for r in rows]; vals = [r[1] for r in rows]
    colors = ["#ff7f0e", "#d62728", "#9467bd", "#8c564b"]
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    bars = ax.bar(labels, vals, color=colors)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("revenue loss under refinement (%)")
    ax.set_title("Where monotonicity breaks: four counterexamples\n(refinement decreases revenue despite better predictions)")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1, f"{v:.1f}%", ha="center", fontsize=8)
    fig.tight_layout(); fig.savefig(IMG / "counterexamples.png", dpi=150); plt.close(fig)


def fig_mu_optimality():
    """mu=1 optimality: conversions vs mu (single bidder), with mu>1 infeasible."""
    rng = np.random.default_rng(7)
    p = rng.uniform(0.01, 1, (12, 3)); t = rng.uniform(0.5, 5, 3)
    others = p[:, 1:] * t[1:]
    mus = np.linspace(0, 1.5, 151)
    convs = []
    for mu in mus:
        b0 = mu * t[0] * p[:, 0]
        win = b0 > others.max(axis=1)
        convs.append(p[win, 0].sum())
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(mus, convs, color="#2ca02c", lw=2)
    ax.axvline(1, color="k", ls="--", lw=1)
    ax.axvspan(1, 1.5, color="#d62728", alpha=0.12, label="μ > 1: CPA-infeasible")
    ax.set_xlabel("uniform multiplier μ (bidder 0, others at μ=1)")
    ax.set_ylabel("conversions won")
    ax.set_title("tCPA bidder: μ=1 maximises feasible conversions\n(μ > 1 violates the CPA constraint)")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(IMG / "mu_optimality.png", dpi=150); plt.close(fig)


def fig_table1():
    """Table 1 characterization: monotone (green) vs non-monotone (red) settings."""
    import matplotlib.patches as mpatches
    settings = [
        ("tCPA · FPA", True, True),
        ("tCPA · VCG", False, False),
        ("tCPA+Bud · FPA", False, False),
        ("tCPA+Bud · LP", True, True),
        ("MAX-CPA · FPA", False, False),
        ("MAX-CPA · VCG", False, True),
        ("MAX-CPA+Bud · LP", None, True),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    for i, (name, rev, wel) in enumerate(settings):
        for j, (val, lab) in enumerate([(rev, "Revenue"), (wel, "Welfare")]):
            if val is None:
                ax.text(j, i, "—", ha="center", va="center", fontsize=12, color="gray")
            else:
                c = "#2ca02c" if val else "#d62728"
                mk = "✓" if val else "✗"
                ax.text(j, i, mk, ha="center", va="center", fontsize=16, color=c, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Revenue", "Welfare"])
    ax.set_yticks(range(len(settings))); ax.set_yticklabels([s[0] for s in settings])
    ax.set_xlim(-0.5, 1.5); ax.set_ylim(-0.5, len(settings) - 0.5)
    ax.set_title("Table 1: monotonicity under model refinement\n(green = proven monotone; red = counterexample exists)")
    ax.invert_yaxis()
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout(); fig.savefig(IMG / "table1.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    fig_jensen_gap(); fig_counterexamples(); fig_mu_optimality(); fig_table1()
    print("figures written to", IMG)
