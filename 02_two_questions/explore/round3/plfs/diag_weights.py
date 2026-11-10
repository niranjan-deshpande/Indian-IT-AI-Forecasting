"""Diagnostics on weighting alternatives (aggregates only). Usage: python3 -I diag_weights.py WORK_DIR ROUND"""
import sys, os
import numpy as np, pandas as pd
d = pd.read_parquet(os.path.join(sys.argv[1], sys.argv[2] + ".parquet"))
W = [11, 12, 21, 31, 41, 51]
wk = d.ps_status.isin(W) | d.ss_status.isin(W)
un = (d.ps_status == 81) & ~d.ss_status.isin(W)
a15 = d.age >= 15
def stats(w, m=slice(None)):
    w = w[m] if not isinstance(m, slice) else w
    dd = d[m] if not isinstance(m, slice) else d
    a = dd.age >= 15
    wkk = wk[m] if not isinstance(m, slice) else wk
    unn = un[m] if not isinstance(m, slice) else un
    lf = (w * ((wkk | unn) & a)).sum(); p = (w * a).sum()
    return dict(lfpr=round(100 * lf / p, 2), wpr=round(100 * (w * (wkk & a)).sum() / p, 2),
                ur=round(100 * (w * (unn & a)).sum() / lf, 2), ur_allages=round(100 * (w * unn).sum() / (w * (wk | un)).sum(), 2))
print("official:", stats(d.w))
alt = d.mult / np.where(d.nss == d.nsc, 100, 200) / 4
print("divide by 4 instead of no_qtr:", stats(alt))
print("no_qtr distribution:", d.no_qtr.value_counts().to_dict())
for q in sorted(d.quarter.unique()):
    m = (d.quarter == q).to_numpy()
    print(q, "n=", m.sum(), stats(d.w * 4, m) if True else "", "pop(m)", round((d.w[m] * d.no_qtr[m]).sum() / 1e6, 1))
for s in [1, 2]:
    print("sector", s, stats(d.w, (d.sector == s).to_numpy()))
ws = d.ps_status.isin(W)
st = pd.Series(np.select([d.ps_status.isin([11, 12, 21]), d.ps_status == 31, d.ps_status.isin([41, 51])], ["se", "reg", "cas"], "x"))
print("ps status shares (PS workers, all ages):", (d.w[ws].groupby(st[ws]).sum() / d.w[ws].sum()).round(3).to_dict())
