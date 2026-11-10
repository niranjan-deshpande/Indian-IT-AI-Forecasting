"""Share of the weighted key-series total contributed by the largest PSUs (aggregate). Usage: python3 -I diag_influence.py WORK_DIR"""
import sys, os
import numpy as np, pandas as pd
for r in ["2021-22", "2022-23", "2023-24", "cy2024", "cy2025"]:
    d = pd.read_parquet(os.path.join(sys.argv[1], r + ".parquet"))
    sel = d.ps_status.isin([11, 12, 21, 31, 41, 51]) & d.gedu.isin([12, 13]) & d.age.between(21, 30) & d.ps_nic.str[:2].isin(["62", "63"])
    t = (d.w * sel).groupby(d.psu).sum().sort_values(ascending=False)
    tot = t.sum()
    print(r, "total(k)=%.0f" % (tot / 1e3), "top1 PSU share=%.3f top5=%.3f" % (t.iloc[0] / tot, t.iloc[:5].sum() / tot),
          "PSUs with >0:", int((t > 0).sum()), " total excl top1 (k)=%.0f" % ((tot - t.iloc[0]) / 1e3))
