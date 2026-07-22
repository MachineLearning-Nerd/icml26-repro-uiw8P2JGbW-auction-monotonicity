from repro.src.verify_auction_claims import fpa_value
import numpy as np

def test_refining_a_calibrated_cluster_is_non_decreasing():
    targets=np.array([10.,1.]); fine=np.array([[.2,.08],[.05,.3]]); w=np.array([.5,.5])
    assert sum(x*fpa_value(p,targets) for x,p in zip(w,fine)) >= fpa_value(w@fine,targets)
