from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE_ARCHIVE=ROOT/'source/arxiv-2605.31036.tar'
SOURCE_ARCHIVE_SHA256='4c64d6db633bb1028e267c95abd0944611b7b07e91745f7456a7b0886e6aa07e'

def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    data=json.loads((ROOT/'outputs/auction_claims.json').read_text()); failures=[]
    checks=[data['C1_refinement_revenue']['min_jensen_gap']>=-1e-12,data['C2_calibration_necessity_negative_control']['negative_cases']>0,data['C3_t_cpa_mu_one_optimality']['violations']==0,data['C4_vcg_t_cpa_nonmonotonicity']['fine']<data['C4_vcg_t_cpa_nonmonotonicity']['coarse'],data['C5_budgeted_fpa_nonmonotonicity']['fine']<data['C5_budgeted_fpa_nonmonotonicity']['coarse'],data['C6_lp_lifting']['violations']==0]
    if not all(checks): failures.append('one or more anchored checks failed')
    tests=subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pytest','-q','repro/tests'],cwd=ROOT,capture_output=True).returncode==0
    if not tests: failures.append('tests failed')
    archive_sha256=sha256(SOURCE_ARCHIVE)
    if archive_sha256 != SOURCE_ARCHIVE_SHA256: failures.append('source archive hash changed')
    report={
        'paper':'uiw8P2JGbW',
        'overall_status':'INCONCLUSIVE',
        'paper_claims_total':6,
        'paper_claims_verified':0,
        'current_claim_status':{
            'C1':'VERIFIED_CONDITIONAL',
            'C2':'VERIFIED_CONDITIONAL',
            'C3':'VERIFIED_CONDITIONAL',
            'C4':'COUNTEREXAMPLE_REPRODUCED',
            'C5':'COUNTEREXAMPLE_REPRODUCED',
            'C6':'VERIFIED_CONDITIONAL',
        },
        'pass':not failures,
        'tests_passed':tests,
        'publication_gate_passed':not failures,
        'claims_passed':6 if not failures else 0,
        'source_archive_sha256':archive_sha256,
        'failures':failures,
        'evidence':data,
    }
    (ROOT/'outputs/publication_gate.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps(report,indent=2,sort_keys=True))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
