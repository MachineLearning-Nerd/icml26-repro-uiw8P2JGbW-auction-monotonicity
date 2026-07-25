"""Baseline verifier for uiw8P2JGbW (arXiv 2605.31036).

Runs the legacy 6-claim finite NumPy verifier and the pytest suite.  This is the
reproduction baseline (finite-instance sanity checks).  A child branch adds
rigorous symbolic proof certificates on top.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main() -> int:
    failures = []
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    print("=" * 60 + "\nBASELINE: legacy 6-claim finite verifier\n" + "=" * 60)
    sys.path.insert(0, str(ROOT))
    try:
        from repro.src import verify_auction_claims as legacy
        legacy.main()
        report = json.loads((OUT / "auction_claims.json").read_text())
        print(f"  baseline: {len(report)} claims, min_jensen_gap="
              f"{report['C1_refinement_revenue']['min_jensen_gap']:.2e}")
    except Exception as e:
        failures.append(f"legacy_verifier: {e}")
        print(f"  FAILED: {e}")
    print("\n" + "=" * 60 + "\nPYTEST\n" + "=" * 60)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(ROOT / "repro" / "tests")],
        capture_output=True, text=True)
    print(proc.stdout.strip()[-500:])
    if proc.returncode != 0:
        failures.append("pytest")
    elapsed = time.time() - t0
    gate = {"paper": "uiw8P2JGbW", "baseline": True, "pass": not failures,
            "failures": failures, "elapsed_s": round(elapsed, 3)}
    (OUT / "publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    print(json.dumps(gate, indent=2))
    return 0 if gate["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
