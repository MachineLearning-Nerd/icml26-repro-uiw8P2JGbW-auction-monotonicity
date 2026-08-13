# Branch audit — uiw8P2JGbW

Audited against the pre-cleanup `main` tip `f2667df` on 2026-08-13.
Both historical `orx/*` branches are ancestors of `main`; the symbolic-proof
branch is exactly the current publication tip and the baseline branch is its
ancestor. No branch contains an unreviewed divergent implementation.

| Historical branch | Tip | Role | Disposition |
| --- | --- | --- | --- |
| `orx/baseline-toy-verifier` | `61bad71` | Initial finite NumPy verifier and pinned uv environment | Integrated in `main`; ancestor |
| `orx/symbolic-proof-certificates` | `f2667df` | SymPy/Z3 certificates, literal counterexamples, Table 1 page, and final publication surface | Integrated in `main`; current tip |

## Final cleanup policy

The final public history keeps the cumulative path on `main`, removes both
obsolete `orx/*` remote refs, and normalizes all reachable author and committer
identities to:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```

The old branch tips and their roles are recorded above before deletion. The
README and root inventory link to the renamed repository after GitHub metadata
verification.
