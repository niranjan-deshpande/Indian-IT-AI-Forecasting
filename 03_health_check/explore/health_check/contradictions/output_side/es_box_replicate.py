"""Approximate replication of Economic Survey 2025-26 Ch.7 Box VII.2 (AI and India's services exports).
Survey: two-way FE DiD on quarterly RBI BoP, Q1FY18-Q2FY26, treated = software, business, financial services;
control = travel, transport, insurance, government n.i.e., communication; intervention Q2FY23; log levels.
Reported: post x treated = 0.333 (=> ~39.5%); software 0.37 (~44%), business 0.51 (~67%), financial 0.12 (n.s.).
Here: IMF BOP mirror of RBI BoP (BPM6 items): software=SI2, business=SJ, financial=SG; control SD, SC, SF, SL, SI1.
Input: ../raw_output/imf/imf_bop_ind_q_allitems.csv. Output: es_box_did.csv, es_raw_growth.csv.
Run: python3 -I es_box_replicate.py
"""
import os, numpy as np, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(OUT, "..", "raw_output", "imf", "imf_bop_ind_q_allitems.csv"), low_memory=False)
d = d[d.BOP_ACCOUNTING_ENTRY == "CD_T"]
p = d.pivot_table(index="TIME_PERIOD", columns="INDICATOR", values="OBS_VALUE") / 1e9
p.index = pd.PeriodIndex([x.replace("-", "") for x in p.index], freq="Q")
TREAT = {"SI2": "software", "SJ": "business", "SG": "financial"}
CTRL = {"SD": "travel", "SC": "transport", "SF": "insurance", "SL": "government", "SI1": "telecom"}

def did(start="2017Q2", end="2025Q3", post_from="2022Q3", treat=TREAT, ctrl=CTRL, by_cat=False):
    x = p.loc[start:end, list(treat) + list(ctrl)].stack().rename("v").reset_index()
    x.columns = ["q", "cat", "v"]; x["y"] = np.log(x.v)
    x["treated"] = x.cat.isin(treat).astype(int); x["post"] = (x.q >= pd.Period(post_from)).astype(int)
    X = [pd.get_dummies(x.cat, prefix="c", drop_first=True, dtype=float), pd.get_dummies(x.q.astype(str), prefix="t", drop_first=True, dtype=float)]
    names = []
    if by_cat:
        for c in treat:
            x[f"pt_{c}"] = ((x.cat == c) & (x.post == 1)).astype(float); names.append(f"pt_{c}")
    else:
        x["pt"] = (x.treated * x.post).astype(float); names = ["pt"]
    M = pd.concat([pd.Series(1.0, index=x.index, name="const"), x[names]] + X, axis=1).values
    b, *_ = np.linalg.lstsq(M, x.y.values, rcond=None)
    resid = x.y.values - M @ b
    # cluster-robust SE by category (few clusters -> indicative only)
    XtX_inv = np.linalg.pinv(M.T @ M); meat = np.zeros((M.shape[1], M.shape[1]))
    for c in x.cat.unique():
        idx = (x.cat == c).values; s = M[idx].T @ resid[idx]; meat += np.outer(s, s)
    se = np.sqrt(np.diag(XtX_inv @ meat @ XtX_inv))
    return {n: (b[i + 1], se[i + 1]) for i, n in enumerate(names)}

rows = []
def add(spec, **kw):
    for k, (b, se) in did(**kw).items():
        rows.append(dict(spec=spec, term=k, coef=round(b, 3), cluster_se=round(se, 3), implied_pct=round((np.exp(b) - 1) * 100, 1)))
add("Survey spec: Q1FY18-Q2FY26, post from Q2FY23")
add("Survey spec, by category", by_cat=True)
add("Control excl. travel (COVID collapse/rebound)", ctrl={k: v for k, v in CTRL.items() if k != "SD"})
add("Post from ChatGPT quarter (2022Q4)", post_from="2022Q4")
# drop-COVID spec: rebuild p without 2020-2022Q2
_p = p.copy()
p = _p.drop(pd.period_range("2020Q1", "2022Q2", freq="Q"), errors="ignore")
add("Drop 2020Q1-2022Q2 (COVID) from sample")
p = _p
add("Extend sample to 2026Q2", end="2026Q2")
r = pd.DataFrame(rows); r.to_csv(os.path.join(OUT, "es_box_did.csv"), index=False); print(r.to_string(index=False))

# raw growth: 4q sums ending Q2FY23 (2022Q3) vs ending Q2FY26 (2025Q3) and latest
g = []
for c, lab in {**TREAT, **CTRL, "SJ2": "prof & mgmt consulting", "S": "total services"}.items():
    s = p[c].rolling(4).sum()
    g.append(dict(item=c, label=lab, group="treated" if c in TREAT else ("control" if c in CTRL else "memo"),
                  usd_bn_4q_to_2022Q3=round(s.loc[pd.Period("2022Q3")], 1), usd_bn_4q_to_2025Q3=round(s.loc[pd.Period("2025Q3")], 1),
                  growth_pct=round((s.loc[pd.Period("2025Q3")] / s.loc[pd.Period("2022Q3")] - 1) * 100, 1),
                  usd_bn_4q_to_2026Q2=round(s.loc[pd.Period("2026Q2")], 1)))
gt = pd.DataFrame(g)
for grp in ["treated", "control"]:
    sub = gt[gt.group == grp]
    gt = pd.concat([gt, pd.DataFrame([dict(item=grp.upper(), label=f"sum of {grp}", group=grp, usd_bn_4q_to_2022Q3=sub.usd_bn_4q_to_2022Q3.sum(),
                                            usd_bn_4q_to_2025Q3=sub.usd_bn_4q_to_2025Q3.sum(),
                                            growth_pct=round((sub.usd_bn_4q_to_2025Q3.sum() / sub.usd_bn_4q_to_2022Q3.sum() - 1) * 100, 1),
                                            usd_bn_4q_to_2026Q2=sub.usd_bn_4q_to_2026Q2.sum())])])
gt.to_csv(os.path.join(OUT, "es_raw_growth.csv"), index=False); print(gt.to_string(index=False))
