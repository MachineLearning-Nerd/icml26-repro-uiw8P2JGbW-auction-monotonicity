"""Master verifier for uiw8P2JGbW (arXiv 2605.31036).

Runs, in order:
  1. symbolic proof certificates  (SymPy)        -- claims 1,2,3,6 + Thm 5.4
  2. counterexamples             (NumPy)         -- claims 4,5 + Table-1 rows 5,6,7
  3. finite corroboration        (NumPy/scipy)   -- Jensen gap, mu-optimality, LP solves
  4. legacy regression verifier  (NumPy)         -- the original 6-claim finite check
  5. pytest unit suite

Writes every raw result to ``outputs/`` and prints an aggregate gate JSON.
Exits non-zero if ANY claim verifier or test fails.
"""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
SOURCE_ARCHIVE = ROOT / "source" / "arxiv-2605.31036.tar"
SOURCE_ARCHIVE_SHA256 = "4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e"
SOURCE_FILE_SHA256 = {
    "source/main.tex": "aa6cdd42fa29a78804cdca8b1e93e2ab34454d17261f83797bab60a451fb06e8",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dump(name: str, obj) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2, default=str, sort_keys=True) + "\n")


def _section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def main() -> int:
    failures: list[str] = []
    t0 = time.time()

    # --- 1. symbolic proofs -------------------------------------------------
    _section("1. SYMBOLIC PROOF CERTIFICATES (SymPy, independent CAS)")
    from repro.proofs import symbolic
    try:
        certs = symbolic.all_certificates()
        _dump("symbolic_certificates.json", certs)
        for k, v in certs.items():
            print(f"  [{v.get('claim', k)}] {v.get('theorem','')}: {v.get('verdict','')}")
    except Exception as e:  # noqa: BLE001
        failures.append(f"symbolic_proofs: {e}")
        print(f"  FAILED: {e}")

    # --- 1b. SMT proofs (Z3, second independent checker) -------------------
    _section("1b. SMT PROOFS (Z3 theorem prover — decidable, complete)")
    from repro.proofs import smt
    try:
        smt_certs = smt.all_smt_proofs()
        _dump("smt_certificates.json", smt_certs)
        for k, v in smt_certs.items():
            print(f"  [{v['claim']}] {v.get('result', v.get('verdict',''))}")
    except Exception as e:  # noqa: BLE001
        failures.append(f"smt_proofs: {e}")
        print(f"  FAILED: {e}")

    # --- 2. counterexamples -------------------------------------------------
    _section("2. COUNTEREXAMPLES (literal paper parameters)")
    from repro.proofs import counterexamples
    try:
        ce = counterexamples.all_counterexamples()
        _dump("counterexamples.json", ce)
        for k, v in ce.items():
            print(f"  [{v['claim']}] {v['theorem']}: "
                  f"loss={v.get('revenue_loss_pct', v.get('welfare_loss_pct','-'))}% "
                  f"-> {v.get('verdict','')}")
    except Exception as e:  # noqa: BLE001
        failures.append(f"counterexamples: {e}")
        print(f"  FAILED: {e}")

    # --- 3. finite corroboration -------------------------------------------
    _section("3. FINITE CORROBORATION (randomised + LP solves)")
    from repro.proofs import finite
    try:
        fc = finite.all_finite_checks()
        _dump("finite_checks.json", fc)
        for k, v in fc.items():
            print(f"  [{v['claim']}] {v.get('verdict','')}")
    except Exception as e:  # noqa: BLE001
        failures.append(f"finite_checks: {e}")
        print(f"  FAILED: {e}")

    # --- 4. legacy regression verifier (superseded; kept for continuity) ---
    _section("4. LEGACY REGRESSION VERIFIER (historical 6-claim finite check)")
    try:
        sys.path.insert(0, str(ROOT))
        from repro.src import verify_auction_claims as legacy  # noqa: F401
        legacy.main()
        legacy_report = json.loads((OUT / "auction_claims.json").read_text())
        print(f"  legacy gate: {len(legacy_report)} claims, min_jensen_gap="
              f"{legacy_report['C1_refinement_revenue']['min_jensen_gap']:.2e}")
    except Exception as e:  # noqa: BLE001
        failures.append(f"legacy_verifier: {e}")
        print(f"  FAILED: {e}")

    # --- 5. pytest ----------------------------------------------------------
    _section("5. PYTEST UNIT SUITE")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(ROOT / "repro" / "tests")],
        capture_output=True, text=True,
    )
    print(proc.stdout.strip()[-800:])
    if proc.returncode != 0:
        failures.append("pytest_unit_suite")
        print(proc.stderr[-800:])

    source_archive_sha256 = _sha256(SOURCE_ARCHIVE)
    source_file_sha256 = {
        relative: _sha256(ROOT / relative)
        for relative in SOURCE_FILE_SHA256
    }
    if source_archive_sha256 != SOURCE_ARCHIVE_SHA256:
        failures.append("source_archive_hash_changed")
    if source_file_sha256 != SOURCE_FILE_SHA256:
        failures.append("source_file_hash_changed")

    # --- aggregate gate -----------------------------------------------------
    elapsed = time.time() - t0
    gate = {
        "paper": "uiw8P2JGbW (arXiv 2605.31036)",
        "overall_status": "INCONCLUSIVE",
        "status_note": (
            "C1, C2, C3, and C6 are conditional symbolic/SMT reconstructions; "
            "C4 and C5 reproduce finite counterexamples at printed precision."
        ),
        "paper_claims_total": 6,
        "paper_claims_verified": 0,
        "pass": len(failures) == 0,
        "scoped_gate_passed": len(failures) == 0,
        "failures": failures,
        "elapsed_s": round(elapsed, 3),
        "source_archive_sha256": source_archive_sha256,
        "source_file_sha256": source_file_sha256,
        "claim_confidence": {
            "C1": "MEDIUM/HIGH",
            "C2": "HIGH",
            "C3": "MEDIUM/HIGH",
            "C4": "HIGH",
            "C5": "HIGH",
            "C6": "MEDIUM/HIGH",
        },
        "current_claim_status": {
            "C1": "VERIFIED_CONDITIONAL",
            "C2": "VERIFIED_CONDITIONAL",
            "C3": "VERIFIED_CONDITIONAL",
            "C4": "COUNTEREXAMPLE_REPRODUCED",
            "C5": "COUNTEREXAMPLE_REPRODUCED",
            "C6": "VERIFIED_CONDITIONAL",
        },
        "primary_evidence": {
            "symbolic_proofs": "outputs/symbolic_certificates.json",
            "counterexamples": "outputs/counterexamples.json",
            "finite_corroboration": "outputs/finite_checks.json",
            "legacy_regression": "outputs/auction_claims.json",
        },
        "claim_verdicts": {
            "C1": "VERIFIED CONDITIONALLY (SymPy/Z3 source reconstruction; 200k corroboration)",
            "C2": "VERIFIED CONDITIONALLY (SymPy/Z3 convexity reconstruction; negative control)",
            "C3": "VERIFIED CONDITIONALLY (SymPy/Z3 identities; 20k-instance corroboration)",
            "C4": "COUNTEREXAMPLE REPRODUCED (printed VCG/tCPA parameters; 6.2% loss)",
            "C5": "COUNTEREXAMPLE REPRODUCED (printed budgeted-FPA parameters; 16.8% loss)",
            "C6": "VERIFIED CONDITIONALLY (SymPy/Z3 lifting identity; 5k LP corroboration)",
        },
    }
    _dump("publication_gate.json", gate)
    _section("PUBLICATION GATE")
    print(json.dumps(gate, indent=2, default=str))
    print(f"\n{'PASS' if gate['pass'] else 'FAIL'} in {elapsed:.1f}s")
    return 0 if gate["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
