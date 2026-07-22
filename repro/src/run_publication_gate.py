from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def main():
    data=json.loads((ROOT/'outputs/auction_claims.json').read_text()); failures=[]
    checks=[data['C1_refinement_revenue']['min_jensen_gap']>=-1e-12,data['C2_calibration_necessity_negative_control']['negative_cases']>0,data['C3_t_cpa_mu_one_optimality']['violations']==0,data['C4_vcg_t_cpa_nonmonotonicity']['fine']<data['C4_vcg_t_cpa_nonmonotonicity']['coarse'],data['C5_budgeted_fpa_nonmonotonicity']['fine']<data['C5_budgeted_fpa_nonmonotonicity']['coarse'],data['C6_lp_lifting']['violations']==0]
    if not all(checks): failures.append('one or more anchored checks failed')
    tests=subprocess.run([str(ROOT/'.venv/bin/python'),'-m','pytest','-q','repro/tests'],cwd=ROOT,capture_output=True).returncode==0
    if not tests: failures.append('tests failed')
    report={'paper':'uiw8P2JGbW','pass':not failures,'tests_passed':tests,'publication_gate_passed':not failures,'claims_passed':6 if not failures else 0,'failures':failures,'evidence':data}
    (ROOT/'outputs/publication_gate.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps(report,indent=2,sort_keys=True))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
