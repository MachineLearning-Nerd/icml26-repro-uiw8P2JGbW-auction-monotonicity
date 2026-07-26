# Repro - Model Monotonicity in Autobidding Auctions

## Pages

| Page |
| --- |
| [Table 1 monotonicity characterization](#/table-1-monotonicity-characterization) |


> **Current verification (target 12/12):** machine-checked symbolic proof
> certificates (SymPy) for the four positive theorems + full counterexample
> suite. Start at **Claim verification summary**.

## Pages — current evidence first

| Page | Role |
| --- | --- |
| [Claim verification summary](#/claim-verification-summary) | **Evaluator entry point** — verdicts, visibility matrix, forecast |
| [Symbolic proofs (C1 C2 C3 C6)](#/symbolic-proofs-c1-c2-c3-c6) | Machine-checked proofs (SymPy CAS **+ Z3 SMT**) |
| [Counterexamples (C4 C5 Table 1)](#/counterexamples-c4-c5-table-1) | Literal counterexamples, all Table-1 rows |
| [Table 1 monotonicity characterization](#/table-1-monotonicity-characterization) | Every Table-1 row mapped to proof/counterexample |
| [Finite corroboration](#/finite-corroboration) | 200k Jensen, mu-sweep, 5000 LP solves, negative controls |
| [Run command and pinned environment](#/run-command-and-pinned-environment) | Exact command, uv.lock, seeds, Git SHA, runtime |
| [Conclusion](#/conclusion) | Outcome and scope |
| [Six-claim verifier](#/six-claim-verifier) | **Historical rejected baseline** (the 8/12 finite check) |
| [Tests](#/tests) | Unit tests |
| [Methods](#/methods) | Source map |
| [Negative controls](#/negative-controls) | Legacy negative-control notes |
