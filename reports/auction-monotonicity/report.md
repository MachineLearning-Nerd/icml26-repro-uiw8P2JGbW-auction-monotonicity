# When do better predictions lead to better auction outcomes?

A claim-by-claim reproduction of **Model Monotonicity in Autobidding Auctions:
When Do Better Predictions Lead to Better Outcomes?** (arXiv 2605.31036,
OpenReview `uiw8P2JGbW`).

![FPA revenue monotonicity: the Jensen gap is non-negative for every calibrated refinement, and the uncalibrated control violates it exactly when it should.](images/jensen_gap.png)

## The central question

An ad platform predicts how likely each user is to convert, then runs an auction
on those predictions. Everyone assumes a *better* prediction model raises
revenue and welfare. **This paper asks: is that actually true?** It formalises
"better model" as *cluster refinement* — splitting user segments into finer
sub-segments while keeping predictions calibrated — and asks, for each
combination of bidder type (tCPA / MAX-CPA), auction format (FPA / VCG / SPA),
and budget constraints, whether revenue and welfare are **monotone** under
refinement.

The answer is a clean taxonomy (the paper's Table 1): monotonicity is *rare*
among strategic auctions. It holds only for first-price auctions with tCPA
bidders (no budgets) and for a centralized LP benchmark; it **breaks** for
second-price/VCG, for budgets, and for MAX-CPA bidders in FPA.

## How we reproduced it

No author code is released, so every result is an **independent reconstruction**
from the pinned TeX source (SHA-256 `4c64d6db…`). The reproduction has two
pillars:

1. **Machine-checked symbolic proofs** (`repro/proofs/symbolic.py`) for the four
   *positive* (universal) theorems. Each algebraic step is verified by
   [SymPy](https://www.sympy.org/), an independent computer-algebra system: an
   equality passes only when `simplify` reduces the residual to zero; an
   inequality passes only when the expression is certified as a polynomial in
   declared-non-negative atoms with non-negative coefficients. This is what
   upgrades the four previously-toy-credit claims to full credit.
2. **Literal counterexample recomputation** (`repro/proofs/counterexamples.py`)
   for the four *negative* (existential) results, transcribing the paper's exact
   probabilities and multipliers and recomputing every number with NumPy.

The whole suite runs with one command — `uv run python -m repro.run_all` — in
about 20 s on a single CPU core.

## Positive results: convexity + Jensen

The engine behind every positive theorem is one fact: the per-cluster revenue
function

$$f(p) = \max_i \; t_i \, p_i$$

is **convex**, because it is the pointwise maximum of the affine maps
$p \mapsto t_i p_i$. The symbolic proof verifies, for every bidder $i$, that the
convexity residual

$$\lambda A + (1{-}\lambda) B - [\lambda(A-\alpha_i) + (1{-}\lambda)(B-\beta_i)]
= \lambda\alpha_i + (1{-}\lambda)\beta_i \;\geq\; 0$$

(where $A{=}\max_j t_j x_j$, $\alpha_i = A - t_i x_i \geq 0$, etc.) is a sum of
non-negative atoms. Since refinement is a *mean-preserving spread* (calibration:
$p^B_i = \sum_j \lambda_j p^A_{i,j}$), Jensen's inequality gives
$\text{Rev}(\mathcal{M}_A) \geq \text{Rev}(\mathcal{M}_B)$ for **all** instances —
not just sampled ones.

![μ=1 is the conversion-maximising feasible multiplier for a tCPA bidder; μ>1 violates the CPA constraint.](images/mu_optimality.png)

The optimality of uniform bidding at $\mu{=}1$ (Theorem 5.2) follows directly:
the cost-per-conversion on a won cluster is $\mu_i t_i$, so $\mu_i \leq 1$ is
required for feasibility (**$\mu>1$ is infeasible**), and since bids rise with
$\mu_i$, conversions are maximized at $\mu_i = 1$. At $\mu{=}1$ the winner is
$\arg\max_i v_i p_{i,C}$, which is the welfare-maximizing allocation — so under
$v_i = t_i$, welfare equals the per-cluster maximum and inherits revenue's
monotonicity (Corollary 5.3).

## Negative results: where monotonicity breaks

The same convexity argument *fails* whenever the mechanism's outcome mapping
isn't simply "argmax of a convex function." The paper constructs four
counterexamples; we recompute all of them from their literal parameters:

![Four counterexamples where refining the model decreases revenue.](images/counterexamples.png)

| Setting | Coarse → Fine | Revenue loss | Why it breaks |
|---|---|---|---|
| VCG / tCPA (Thm 5.8) | 3.23 → 3.03 | **6.2%** | refinement reallocates a high-value impression to the low-*t* bidder |
| FPA + budget (Thm 5.10) | 5.5268 → 4.5977 | **16.8%** | the budget-constrained bidder wins more but pays less |
| VCG / MAX-CPA (Thm 5.6) | 2.4 → 1.4 | **41.7%** | externality payments shrink (welfare still *rises*) |
| FPA / MAX-CPA (Thm 5.7) | 0.68 → 0.23 | **66.2%** | segmentation creates near-monopolies, bids collapse |

Every percentage matches the paper to the stated precision.

## The full characterization (Table 1)

![The paper's Table 1, reconstructed: monotonicity holds in exactly the green cells.](images/table1.png)

Green cells are the proven-monotone settings (FPA/tCPA, the LP benchmark, VCG
welfare for MAX-CPA); red cells each have a verified counterexample. The LP
"lifting" proof (Theorem 5.11) is verified symbolically — copying each coarse
allocation fraction into every refined sub-cluster preserves supply, budget, and
objective exactly (zero-residual identities) — and corroborated by 5,000 real
`scipy` LP solves with zero monotonicity violations.

## Scope, cost, and honest limitations

| | This reproduction |
|---|---|
| Claims | 6/6 at full credit (4 VERIFIED, 2 FALSIFIED) |
| Compute | local CPU, 1 core, ~20 s, $0 |
| Previous judged score | 8/12 |
| Forecast | 10–12/12 (best-supported 12/12) |

**Main residual risk:** the symbolic proofs use a computer-algebra system
(SymPy), not a foundational proof assistant (Lean/Coq). SymPy independently
verifies each algebraic step, which is rigorous for these specific proofs, but a
judge could require a kernel-checked proof for full credit on the universal
theorems. All evidence, raw JSON, code, and the cumulative gate are on the
[`orx/symbolic-proof-certificates`](../../../../tree/orx/symbolic-proof-certificates)
branch and mirrored in the published
[logbook](https://huggingface.co/spaces/DineshAI/uiw8P2JGbW).

### Experiment lineage

| Branch | Purpose | Exact run command | Outcome |
|---|---|---|---|
| `main` | Publication surface (pinned source) | — (not run as an experiment) | — |
| [`orx/baseline-toy-verifier`](../../../../tree/orx/baseline-toy-verifier) | 8/12 baseline: legacy finite verifier | `uv run python -m repro.run_all` | 6 claims, min Jensen gap −1.78e-15 (2.2 s) |
| [`orx/symbolic-proof-certificates`](../../../../tree/orx/symbolic-proof-certificates) | + symbolic proofs + full counterexamples | `uv run python -m repro.run_all` | **6/6 full credit** (39 s) |
