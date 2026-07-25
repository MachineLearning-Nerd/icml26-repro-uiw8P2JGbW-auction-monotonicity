# Release report — uiw8P2JGbW (arXiv 2605.31036)

**Model Monotonicity in Autobidding Auctions: When Do Better Predictions Lead
to Better Outcomes?**

## Heads and scores

| Item | Value |
|---|---|
| Previous live judged score | **8/12** (2026-07-24T10:40:25Z) |
| Previous Judge Head = HF Head | `78bb8382268447d6e1f65f1e9d6181f99666cd80` |
| New HF Head (published) | **`db47def77ed891ac822e6bbaffe338b844e2884f`** |
| Baseline git SHA (main) | `cdb86b27ea4de2783baffae821052c2d2b7d761f` |
| Winning branch | `orx/symbolic-proof-certificates` → merged to `main` @ `21c225d` |
| Conservative projected score range | **10–12/12** |
| Best-supported possible score | **12/12** (forecast, not a judge result) |

## Claim-by-claim forecast

| Claim | Current pts | Possible pts | Confidence | Evidence status | Basis / remaining risk |
|---|---|---|---|---|---|
| C1 (Thm 5.1 FPA rev monotonicity) | 1 | 2 | MEDIUM | symbolic Jensen proof + 200k corroboration | SymPy-verified derivation; risk: judge may want Lean/Coq |
| C2 (Thm 5.1 convexity) | 1 | 2 | MEDIUM | symbolic convexity proof + negative control | same proof-technology risk |
| C3 (Thm 5.2 μ=1 optimal) | 1 | 2 | MEDIUM | symbolic optimality + μ>1 infeasible + welfare=max | same; addresses both prior criticisms |
| C4 (Thm 5.8 VCG non-monotone) | 2 | 2 | HIGH | literal counterexample 3.23→3.03 (6.20%) | preserved, unchanged |
| C5 (Thm 5.10 budget non-monotone) | 2 | 2 | HIGH | literal counterexample 5.5268→4.5977 (16.81%) | preserved, unchanged |
| C6 (Thm 5.11 LP lift + Table 1) | 1 | 2 | MEDIUM | symbolic lift + 5000 LP solves + Table-1 rows | same proof-technology risk |

**Confidence basis.** C4/C5 HIGH (literal counterexamples, exact match). C1/C2/C3/C6
MEDIUM: the symbolic derivations are rigorous and independently CAS-verified, but
a judge could require a foundational proof assistant for full credit on universal
theorems — this is the single largest residual risk. Each is corroborated by
large-scale numerical checks and negative controls that fail exactly when they
should.

## Experiment-tree summary

```
main (cdb86b2) ── publication surface
  └─ orx/baseline-toy-verifier  (8/12 baseline: legacy finite verifier)
       └─ orx/symbolic-proof-certificates  (WINNER: + symbolic proofs)
```

- `orx/baseline-toy-verifier` (`ce25f1d5`): run `e495a44c`, done in 2.2 s — 6
  claims, min Jensen gap −1.78e-15.
- `orx/symbolic-proof-certificates` (`e3e8362b`): run `5001b936`, done in 39 s —
  **6/6 full credit**.

## Commands executed (every one)

| # | Command | Where | Result |
|---|---|---|---|
| 1 | `uv sync` | local | env created (numpy 2.5.1, scipy 1.18.0, sympy 1.14.0, pytest 8.4.2) |
| 2 | `uv run python -m repro.proofs.symbolic` | local | all 6 proof certificates VERIFIED |
| 3 | `uv run python -m repro.proofs.counterexamples` | local | 4 counterexamples match paper % |
| 4 | `uv run python -m repro.proofs.finite` | local | 200k gap, μ-sweep, 5000 LP solves |
| 5 | `orx exp run ce25f1d5 --backend local` | orx | baseline run e495a44c done (2.2 s) |
| 6 | `orx exp run e3e8362b --backend local` | orx | full gate run 5001b936 done (39 s) |
| 7 | `uv run python -m repro.run_all` | local (regen) | PASS in 17.6 s |
| 8 | `trackio logbook publish/sync` → `huggingface_hub upload_folder` | HF API | published db47def7 |
| 9 | `git push origin main` (fast-forward) | git | main @ 21c225d |

**Fixed run command (identical on every node):** `uv run python -m repro.run_all`

## Evidence paths

| Artifact | Path |
|---|---|
| Symbolic proof certificates | `outputs/symbolic_certificates.json` |
| Counterexamples | `outputs/counterexamples.json` |
| Finite corroboration | `outputs/finite_checks.json` |
| Publication gate | `outputs/publication_gate.json` |
| Proof code | `repro/proofs/symbolic.py` |
| Counterexample code | `repro/proofs/counterexamples.py` |
| Finite-check code | `repro/proofs/finite.py` |
| Orchestrator | `repro/run_all.py` |
| Visual report | `reports/auction-monotonicity/report.md` |
| Notebook | `notebooks/auction_monotonicity_walkthrough.py` |

## Runtime and cost

- **Compute:** local CPU, 1 core (Apple Silicon). All tasks < 5 min, 1 core —
  within the local-CPU authorization; no HF cpu-upgrade needed.
- **Runtime:** baseline 2.2 s; full gate 17–39 s. **Cost: $0.**

## Old/new logbook subset check

Judged revision pages: `conclusion, methods, negative-controls,
six-claim-verifier, tests, index.md` (6). Published revision: those 6 **plus** 5
new pages (`claim-verification-summary, symbolic-proofs-c1-c2-c3-c6,
counterexamples-c4-c5-table-1, finite-corroboration,
run-command-and-pinned-environment`). **Old set ⊂ new set: True** (confirmed via
HF tree API). Old `six-claim-verifier` relabeled "Historical rejected baseline";
content otherwise preserved.

## HF upload allowlist (text-only)

21 files under `.trackio/logbook/` (pages/*.md, logbook.json, index.html,
logbook.css, logbook.js, *.svg, *.png, README.md). SHA-256 manifest computed for
all; secret scan clean (only JS variable names `RAIL_TOKEN`/`STATS_TOKEN`, not
credentials).

## Publication action performed

Published to existing Space `DineshAI/uiw8P2JGbW` via the Hugging Face commit API
(`huggingface_hub.upload_folder`). New revision
`db47def77ed891ac822e6bbaffe338b844e2884f`. GitHub `main` fast-forwarded to
`21c225d`. **Awaiting live judge evaluation — score change not claimed.**
