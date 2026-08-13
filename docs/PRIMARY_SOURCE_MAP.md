# Primary-source map

Pinned arXiv source: `2605.31036`, SHA-256
`4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e`.
The extracted `source/main.tex` SHA-256 is
`aa6cdd42fa29a78804cdca8b1e93e2ab34454d17261f83797bab60a451fb06e8`.

- C1/C2: Theorems 5.1–5.2 and Jensen proof, `sections/main_results.tex`.
- C3: tCPA FPA welfare corollary and uniform-multiplier argument.
- C4: VCG/tCPA finite construction, Appendix counterexample (`3.23 → 3.03`).
- C5: budgeted FPA finite construction (`5.5268 → 4.5977`).
- C6: LP lifting theorem and feasibility-preserving proof.

Claim producers:

- C1/C2/C3/C6: `repro/proofs/symbolic.py` plus the independent modeled Z3 checks
  in `repro/proofs/smt.py`; `repro/proofs/finite.py` is corroboration only.
- C4/C5 and the additional Table 1 rows: literal printed-parameter
  reconstructions in `repro/proofs/counterexamples.py`.
- Aggregate orchestration: `repro/run_all.py`.

The verifier is an independent source-transcribed reconstruction. The symbolic
and SMT artifacts audit the stated algebra and modeled constraints, but do not
substitute a foundational proof of every paper theorem or a new equilibrium
existence theorem. The MAX-CPA FPA rows use designated feasible profiles, and
the LP row is a centralized benchmark rather than a strategic equilibrium.
