# Status — uiw8P2JGbW

Current step: source-pinned, CPU-only clean-room verifier construction.

The audit found all six anchored claims in the primary TeX source: FPA/tCPA
Jensen monotonicity and optimum, VCG/tCPA 6.2% counterexample, FPA-with-budget
16.8% counterexample, and LP lifting. No author code is released, so every
numerical result must be derived from the paper's literal finite parameters and
labelled as an independent reconstruction. Another paper's heavy source job is
active; only deterministic/cheap checks may run now.

Full deterministic six-claim verifier passes: 2,000 calibrated Jensen cases
(min gap `-1.78e-15`), 500 tCPA optimum cases (zero violations), literal
VCG/tCPA `3.23 → 3.03` (6.192%), literal FPA-budget `5.5268 → 4.5977`
(16.810%), and 500 LP lifts (zero violations). The uncalibrated negative
control fails in 998/2,000 cases. One pytest check passes.

The local publication gate passes (`outputs/publication_gate.json`). Next:
complete the Trackio conclusion and source map, secret-scan, public GitHub
push, then atomically enqueue. No direct HF publication is permitted.
