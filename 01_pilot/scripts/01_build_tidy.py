"""Build tidy datasets from data/raw/*.csv.

Outputs (data/tidy/):
  panel_long.csv   - one row per (firm, cal_q, metric, dimension, dim_type, unit, basis, period_type), latest vintage,
                     with source_url of the chosen vintage, n_vintages and a restatement flag.
  core_quarterly.csv - firm x cal_q levels of core variables (each column has a companion *_src column).
  yoy_metrics.csv  - firm x cal_q year-on-year metrics used in Parts 2-4 (gR, gL, du, gTCV, dsub, SLc...).
No value is interpolated or imputed. Missing stays missing.
"""
import glob
import numpy as np
import pandas as pd
from common import RAW, TIDY, RAW_COLS

KEY = ["firm", "cal_q", "metric", "dimension", "dim_type", "unit", "basis", "period_type"]


def load_raw():
    frames = []
    for f in sorted(glob.glob(str(RAW / "*.csv"))):
        d = pd.read_csv(f, low_memory=False, dtype={"cal_q": str})
        d["raw_file"] = f.split("/")[-1]
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    for c in ["dimension", "dim_type", "basis", "period_type", "unit"]:
        d[c] = d[c].fillna("na").astype(str).str.strip()
    d["doc_date"] = pd.to_datetime(d["doc_date"], errors="coerce")
    d["is_gfc_file"] = d.raw_file.eq("gfc.csv")
    return d


def select_vintage(d):
    """Latest doc_date per KEY; firm-specific files take precedence over the GFC file."""
    d = d[d.value.notna() & d.source_url.notna()].copy()
    d = d.sort_values(["is_gfc_file", "doc_date"], ascending=[True, False])
    stats = d.groupby(KEY)["value"].agg(n_vintages="size", vmin="min", vmax="max").reset_index()
    best = d.drop_duplicates(KEY, keep="first")
    best = best.merge(stats, on=KEY)
    rel = (best.vmax - best.vmin).abs() / best.value.abs().replace(0, np.nan)
    best["restated"] = (best.n_vintages > 1) & (rel.fillna(0) > 0.005)
    return best.drop(columns=["vmin", "vmax"])


def pick(p, firm, metric, dims, unit=None, basis=None, ptype=None):
    """Return Series indexed by cal_q (value) and source (src) for the first matching dimension in `dims` list.
    Dims are tried in order per quarter (first available wins)."""
    x = p[(p.firm == firm) & (p.metric == metric)]
    if unit is not None:
        x = x[x.unit.isin(unit if isinstance(unit, list) else [unit])]
    if basis is not None:
        x = x[x.basis.isin(basis if isinstance(basis, list) else [basis])]
    if ptype is not None:
        x = x[x.period_type.isin(ptype if isinstance(ptype, list) else [ptype])]
    out = []
    for rank, dim in enumerate(dims):
        y = x[x.dimension == dim].copy()
        y["rank"] = rank
        out.append(y)
    if not out:
        return pd.DataFrame(columns=["cal_q", "value", "src", "unit"])
    # within a dimension, period types are preferred in the order listed in `ptype` (e.g. ltm before quarter for
    # attrition); a stable sort makes the choice deterministic (audit 2026-10: Cognizant 2021Q2-Q3 mixed definitions)
    y = pd.concat(out)
    order = ptype if isinstance(ptype, list) else [ptype]
    y["prank"] = y.period_type.map({p: i for i, p in enumerate(order)}).fillna(len(order))
    y = y.sort_values(["rank", "prank"], kind="stable").drop_duplicates("cal_q")
    return y[["cal_q", "value", "source_url", "unit"]].rename(columns={"source_url": "src"})


# ---- per-firm specification of core variables -------------------------------------------------------------
FIRMS_ALL = ["tcs", "infosys", "hcltech", "wipro", "techm", "lti", "mindtree", "ltim", "cognizant", "accenture"]
REV_DIM = {"wipro": ["IT Services"]}
# preferred utilization series per firm (one consistent series; YoY change computed within series)
UTIL = {
    "tcs": [("utilization_excl_trainees", ["total"])],
    "infosys": [("utilization_excl_trainees", ["total", "IT Services"])],
    "hcltech": [("utilization_incl_trainees", ["total"])],
    "wipro": [("utilization_excl_trainees", ["total"])],
    "techm": [("utilization_incl_trainees", ["total"])],
    "lti": [("utilization_excl_trainees", ["total"])],
    "mindtree": [("utilization_incl_trainees", ["total"])],
    "ltim": [("utilization_excl_trainees", ["total"])],
    # Cognizant: offshore utilization through 2023Q4, blended (excl trainees) afterwards; YoY changes spliced
    "cognizant": [("utilization_offshore", ["total", "Offshore", "offshore"]), ("utilization_excl_trainees", ["total"])],
    "accenture": [("utilization_incl_trainees", ["total"])],
}
ATTR_DIM = {"tcs": ["IT Services"], "infosys": ["Voluntary Attrition % (LTM - IT Services)", "Attrition % (LTM)", "Attrition % (Annualized Consolidated)"], "wipro": ["Voluntary TTM"], "cognizant": ["Tech Services", "total"],
            "hcltech": ["total", "IT Services"]}
HEAD_DIM = {"accenture": ["total"], "wipro": ["total"]}
# Reported divestitures that mechanically cut headcount (added back to the base of YoY windows spanning them)
DIVEST = {("hcltech", "2024Q2"): 7398}


def qadd(q, k):
    y, n = int(q[:4]), int(q[-1])
    t = y * 4 + n - 1 + k
    return f"{t // 4}Q{t % 4 + 1}"


def core_panel(p):
    rows = []
    for f in FIRMS_ALL:
        if f not in set(p.firm):
            continue
        rd = REV_DIM.get(f, ["total"])
        cols = {}
        cols["rev_usd"] = pick(p, f, "revenue", rd, unit="USD_mn", ptype="quarter")
        cols["rev_inr"] = pick(p, f, "revenue", ["total"], unit=["INR_mn", "INR_cr"], ptype="quarter")
        cols["rev_cc_yoy"] = pick(p, f, "revenue_growth_yoy", rd, basis="cc", ptype="quarter")
        cols["rev_rep_yoy"] = pick(p, f, "revenue_growth_yoy", rd, basis="reported", ptype="quarter")
        cols["rev_cc_qoq"] = pick(p, f, "revenue_growth_qoq", rd, basis="cc", ptype="quarter")
        cols["headcount"] = pick(p, f, "headcount", HEAD_DIM.get(f, ["total"]), ptype="point")
        cols["attrition"] = pick(p, f, "attrition", ATTR_DIM.get(f, ["total"]), ptype=["ltm", "quarter"])
        for i, (m, dims) in enumerate(UTIL.get(f, [])):
            cols[f"util{i}"] = pick(p, f, m, dims, ptype="quarter")
        cols["util_incl"] = pick(p, f, "utilization_incl_trainees", ["total"], ptype="quarter")
        cols["util_excl"] = pick(p, f, "utilization_excl_trainees", ["total", "IT Services"], ptype="quarter")
        # subcontracting (level, same currency as revenue where possible)
        if f == "tcs":
            a = pick(p, f, "subcontracting_cost", ["Fees to external consultants (in cost of revenue)"], unit="USD_mn", ptype="quarter")
            b = pick(p, f, "subcontracting_cost", ["Fees to external consultants (in SG&A)"], unit="USD_mn", ptype="quarter")
            s = a.merge(b, on="cal_q", suffixes=("", "_b"))
            s["value"] = s.value + s.value_b
            cols["subcon"] = s[["cal_q", "value", "src", "unit"]]
            cols["subcon_denom"] = cols["rev_usd"]
        else:
            cols["subcon"] = pick(p, f, "subcontracting_cost", ["total"], unit=["INR_mn", "INR_cr"], ptype="quarter")
            cols["subcon_denom"] = cols["rev_inr"]
        # deal value
        if f == "accenture":
            cols["tcv_q"] = pick(p, f, "bookings", ["total"], unit="USD_mn", ptype="quarter")
        elif f == "cognizant":
            cols["tcv_ttm"] = pick(p, f, "bookings", ["total"], unit="USD_bn", ptype="ltm")
        elif f == "wipro":
            cols["tcv_q"] = pick(p, f, "tcv", ["Large deals (>=USD30mn TCV)"], unit="USD_mn", ptype="quarter")
        else:
            cols["tcv_q"] = pick(p, f, "tcv", ["total"], unit=["USD_mn", "USD_bn"], ptype="quarter")
        base = None
        for name, s in cols.items():
            s = s.copy()
            if name in ("tcv_q", "tcv_ttm") and len(s):
                s.loc[s.unit == "USD_bn", "value"] *= 1000
            if name in ("rev_inr", "subcon", "subcon_denom") and len(s):
                s.loc[s.unit == "INR_cr", "value"] *= 10          # crore -> million
            s = s.rename(columns={"value": name, "src": name + "_src"}).drop(columns="unit")
            base = s if base is None else base.merge(s, on="cal_q", how="outer")
        base["firm"] = f
        rows.append(base)
    core = pd.concat(rows, ignore_index=True)
    core["subcon_share"] = 100 * core.subcon / core.subcon_denom
    core = core.drop(columns=["subcon_denom", "subcon_denom_src"])
    core = core.sort_values(["firm", "cal_q"]).reset_index(drop=True)
    front = ["firm", "cal_q"]
    return core[front + [c for c in core.columns if c not in front]]


def yoy_metrics(core):
    out = []
    for f, g in core.groupby("firm"):
        g = g.set_index("cal_q").sort_index()
        allq = pd.Index(sorted(set(g.index)))
        r = pd.DataFrame(index=allq)
        lag = {q: qadd(q, -4) for q in allq}

        def lagged(col):
            return pd.Series([g[col].get(lag[q], np.nan) if col in g else np.nan for q in allq], index=allq)

        r["gR"] = 100 * np.log1p(g["rev_cc_yoy"].reindex(allq) / 100)
        r["gR_usd"] = 100 * np.log(g["rev_usd"].reindex(allq) / lagged("rev_usd"))
        base = lagged("headcount")
        for (ff, qq), n in DIVEST.items():
            if ff == f:
                span = [q for q in allq if lag[q] < qq <= q]
                base.loc[span] = base.loc[span] - n
        r["gL"] = 100 * np.log(g["headcount"].reindex(allq) / base)
        # utilization: YoY log change within each series; first series wins, later series fill quarters it lacks
        du = pd.Series(np.nan, index=allq)
        for i in range(3):
            c = f"util{i}"
            if c in g and g[c].notna().any():
                d_i = 100 * np.log(g[c].reindex(allq) / lagged(c))
                du = du.fillna(d_i) if i else d_i
        r["du"] = du
        r["util_level"] = g.get("util0", pd.Series(dtype=float)).reindex(allq)
        # deal value: TTM sum of quarterly (needs 4 consecutive quarters) or reported TTM
        if "tcv_ttm" in g and g["tcv_ttm"].notna().any():
            ttm = g["tcv_ttm"].reindex(allq)
        elif "tcv_q" in g:
            v = g["tcv_q"].reindex(allq)
            ttm = pd.Series([v.loc[[qadd(q, -k) for k in range(4)]].sum(min_count=4)
                             if all(qadd(q, -k) in v.index for k in range(4)) else np.nan for q in allq], index=allq)
        else:
            ttm = pd.Series(np.nan, index=allq)
        r["tcv_ttm"] = ttm
        r["gTCV"] = 100 * np.log(ttm / pd.Series([ttm.get(lag[q], np.nan) for q in allq], index=allq))
        r["dsub"] = g["subcon_share"].reindex(allq) - lagged("subcon_share")
        r["subcon_share"] = g["subcon_share"].reindex(allq)
        r["attrition"] = g["attrition"].reindex(allq)
        r["gRPE"] = r.gR - r.gL                       # revenue per employee (cc, end-period heads)
        r["resid"] = r.gR - r.gL - r.du               # residual: price/productivity mix
        r["firm"] = f
        out.append(r.reset_index().rename(columns={"index": "cal_q"}))
    y = pd.concat(out, ignore_index=True)
    return y[["firm", "cal_q"] + [c for c in y.columns if c not in ("firm", "cal_q")]]


if __name__ == "__main__":
    raw = load_raw()
    print("raw rows", len(raw), "missing source_url:", raw.source_url.isna().sum(), "empty values:", raw.value.isna().sum())
    p = select_vintage(raw)
    p.drop(columns=["is_gfc_file"]).to_csv(TIDY / "panel_long.csv", index=False)
    print("panel_long rows", len(p), "restated keys", int(p.restated.sum()))
    core = core_panel(p)
    core.to_csv(TIDY / "core_quarterly.csv", index=False)
    y = yoy_metrics(core)
    y.to_csv(TIDY / "yoy_metrics.csv", index=False)
    print(y.groupby("firm")[["gR", "gL", "du", "gTCV", "dsub"]].count())
