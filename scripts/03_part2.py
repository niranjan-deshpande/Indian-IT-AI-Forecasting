"""Part 2: historical decomposition, episode signatures, cross-sectional tests, Indian vs comparators.

Identity (YoY log changes, x100):   gR = gL + gRPE,   gRPE = du + resid
  gR    constant-currency revenue growth (as reported, log-transformed)
  gL    headcount growth (end-of-period)
  du    utilization change (log, within one consistent series per firm)
  resid = gR - gL - du  : mixes price (p) and labor per unit of volume (a); p and Q are NOT separately observed.

Outputs: figures/fig2_decomposition.png, fig3_episodes.png, fig4_cross_section.png, fig5_india_vs_comparators.png,
         output/episode_signatures.csv, output/cross_section_*.csv
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import TIDY, FIG, OUT, LABEL, INDIAN, COMPARATORS, EPISODES

yoy = pd.read_csv(TIDY / "yoy_metrics.csv")
p = pd.read_csv(TIDY / "panel_long.csv", low_memory=False)
MAIN = [f for f in INDIAN + COMPARATORS if f in set(yoy.firm)]

# LTIMindtree pre-merger: for plots only, show LTI and Mindtree separately (no splice) - see DECISIONS
C = {"gR": "#1f4e79", "gL": "#c0392b", "gRPE": "#2e8b57", "du": "#999999", "resid": "#e39b2d"}

# ---------------------------------------------------------------- Fig 2: decomposition small multiples
fig, axes = plt.subplots(2, 4, figsize=(13, 6.2), sharex=True, sharey=True)
QS = [f"{y}Q{q}" for y in range(2016, 2027) for q in range(1, 5) if f"{y}Q{q}" <= "2026Q2"]
QX = {q: i for i, q in enumerate(QS)}
for ax, f in zip(axes.flat, MAIN):
    g = yoy[(yoy.firm == f)].set_index("cal_q").reindex(QS)
    if f == "ltim":   # LTI (pre-merger) until 2022Q3, LTIMindtree afterwards: no splice, shown as separate segments
        lti = yoy[yoy.firm == "lti"].set_index("cal_q").reindex(QS)
        g = g.where(pd.Series(QS, index=QS) >= "2022Q4", lti, axis=0)
    x = np.arange(len(QS))
    ax.bar(x, g.du, color=C["du"], width=0.8, label="Δ utilization", alpha=0.6)
    ax.plot(x, g.gR, color=C["gR"], lw=1.6, label="revenue (cc)")
    ax.plot(x, g.gL, color=C["gL"], lw=1.6, label="headcount")
    ax.plot(x, g.gRPE, color=C["gRPE"], lw=1.2, ls="--", label="revenue/employee")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_title(LABEL[f] + (" (LTI until 2022Q3)" if f == "ltim" else ""), fontsize=9)
    ax.axvspan(QX["2024Q2"] - 0.5, len(QS) - 0.5, color="#f4e3c1", alpha=0.5, lw=0)
    ax.set_ylim(-25, 40)
for ax in axes.flat[len(MAIN):]:
    ax.set_visible(False)
ticks = [i for i, q in enumerate(QS) if q.endswith("Q1") and int(q[:4]) % 2 == 0]
for ax in axes[-1]:
    ax.set_xticks(ticks)
    ax.set_xticklabels([QS[i][:4] for i in ticks], fontsize=7)
axes[0, 0].legend(fontsize=7, loc="upper left")
fig.suptitle("Fig 2. YoY growth decomposition: revenue (cc) = headcount + revenue per employee; shaded = FY2025 onward", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(FIG / "fig2_decomposition.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- Episode signatures
def episode_table(yoy):
    rows = []
    for ep, (a, b) in EPISODES.items():
        for f in sorted(set(yoy.firm)):
            g = yoy[(yoy.firm == f) & (yoy.cal_q >= a) & (yoy.cal_q <= b)]
            pre_a = f"{int(a[:4]) - 1}{a[4:]}"
            pre = yoy[(yoy.firm == f) & (yoy.cal_q >= pre_a) & (yoy.cal_q < a)]
            if g["gL"].notna().sum() == 0 or g[["gR", "gR_usd"]].notna().sum().max() == 0:
                continue
            row = dict(episode=ep, firm=f, n_q=len(g))
            for m in ["gR", "gR_usd", "gL", "gRPE", "du", "resid", "gTCV", "dsub"]:
                row[m] = g[m].mean()
                row[m + "_pre4"] = pre[m].mean()
                row[m + "_min"] = g[m].min()
            rows.append(row)
    return pd.DataFrame(rows)

ep = episode_table(yoy)
ep.to_csv(OUT / "episode_signatures.csv", index=False)

def grp(f):
    return "Indian" if f in INDIAN + ["lti", "mindtree"] else LABEL.get(f, f)

ep["group"] = ep.firm.map(grp)
ep["gRPE_usd"] = ep.gR_usd - ep.gL
summ = ep.groupby(["episode", "group"])[["gR", "gR_usd", "gL", "gRPE", "gRPE_usd", "du", "resid", "gTCV"]].mean().round(1)
summ["n_firms_gR"] = ep.groupby(["episode", "group"]).gR.count()
summ["n_firms_du"] = ep.groupby(["episode", "group"]).du.count()
summ.to_csv(OUT / "episode_summary.csv")

fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
eps = [e for e in EPISODES if e in set(ep.episode)]
for ax, grp_name in zip(axes, ["Indian", "Cognizant", "Accenture"]):
    s = summ.xs(grp_name, level="group") if grp_name in summ.index.get_level_values("group") else None
    if s is None:
        ax.set_visible(False); continue
    s = s.reindex(eps)
    w = 0.18
    x = np.arange(len(eps))
    rev = s["gR"].where(s["gR"].notna() & ~s.index.str.startswith("GFC"), s["gR_usd"])
    ax.bar(x - 1.5 * w, rev, w, color=C["gR"], label="revenue (cc; USD for GFC)")
    for i, m in enumerate(["gL", "du"], start=1):
        ax.bar(x + (i - 1.5) * w, s[m], w, color=C[m], label={"gL": "headcount", "du": "Δ utilization"}[m])
    gfc = s.index.str.startswith("GFC")
    res = s["resid"].where(~gfc, rev - s["gL"] - s["du"].fillna(0))
    ax.bar(x + 1.5 * w, res, w, color=C["resid"], label="residual (p/a; GFC: USD-based)")
    ax.set_xticks(x)
    ax.set_xticklabels([e.replace(" (", "\n(") for e in eps], fontsize=7)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_title(grp_name + (" (mean of firms with data)" if grp_name == "Indian" else ""), fontsize=9)
axes[0].set_ylabel("mean YoY log change over episode, %")
axes[0].legend(fontsize=7)
fig.suptitle("Fig 3. Episode signatures: mean YoY growth of each component during each episode", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(FIG / "fig3_episodes.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- Cross-section: verticals
VGROUP_RULES = [  # order matters
    ("FS", ["financ", "bfs", "bank", "insur"]),
    ("TMT", ["tech", "communic", "media", "telecom", "hi-tech", "high-tech", "cme"]),
    ("HEALTH_PUB", ["health", "life", "public", "pharma"]),
    ("OTHER_IND", ["manufact", "retail", "consumer", "cpg", "energy", "resource", "utilit", "product",
                   "travel", "transport", "logist"]),
]

def vgroup(name):
    n = name.lower()
    for g, keys in VGROUP_RULES:
        if any(k in n for k in keys):
            return g
    return "OTHER"

def segment_growth(p, dim_type, grouper):
    """Firm x group x quarter YoY growth (cc if reported, else reported), share-weighted within group."""
    x = p[(p.dim_type == dim_type) & (p.metric == "segment_growth_yoy") & (p.period_type == "quarter")].copy()
    x = x.sort_values("basis").drop_duplicates(["firm", "cal_q", "dimension"], keep="first")  # 'cc' < 'reported'
    sh = p[(p.dim_type == dim_type) & (p.metric == "revenue_share")][["firm", "cal_q", "dimension", "value"]]
    sh = sh.rename(columns={"value": "share"}).drop_duplicates(["firm", "cal_q", "dimension"])
    lev = p[(p.dim_type == dim_type) & (p.metric == "segment_revenue")][["firm", "cal_q", "dimension", "value"]]
    lev = lev.rename(columns={"value": "lev"}).drop_duplicates(["firm", "cal_q", "dimension"])
    x = x.merge(sh, how="left", on=["firm", "cal_q", "dimension"]).merge(lev, how="left", on=["firm", "cal_q", "dimension"])
    x["w"] = x.share.fillna(x.lev).fillna(1.0)
    x["grp"] = x.dimension.map(grouper)
    x = x[x.grp != "OTHER"]
    x["wg"] = x.w * x.value
    out = x.groupby(["firm", "grp", "cal_q"]).agg(wg=("wg", "sum"), w=("w", "sum"), basis=("basis", "first")).reset_index()
    out["g"] = out.wg / out.w
    return out[["firm", "grp", "cal_q", "g", "basis"]]

def decel(sg, recent=("2024Q2", "2026Q2"), base=("2017Q1", "2019Q4")):
    r = sg[(sg.cal_q >= recent[0]) & (sg.cal_q <= recent[1])].groupby(["firm", "grp"]).g.mean()
    b = sg[(sg.cal_q >= base[0]) & (sg.cal_q <= base[1])].groupby(["firm", "grp"]).g.mean()
    d = pd.concat([r.rename("recent"), b.rename("base")], axis=1)
    d["decel"] = d.recent - d.base
    return d.reset_index()

def two_way_share(d, val="recent"):
    """Share of cross-sectional variance of `val` explained by group effects vs firm effects (sequential SS)."""
    d = d.dropna(subset=[val])
    tot = ((d[val] - d[val].mean()) ** 2).sum()
    g_ss = (d.groupby("grp")[val].transform("mean") - d[val].mean()).pow(2).sum()
    f_ss = (d.groupby("firm")[val].transform("mean") - d[val].mean()).pow(2).sum()
    return dict(n=len(d), share_group=g_ss / tot if tot else np.nan, share_firm=f_ss / tot if tot else np.nan)

vg = segment_growth(p, "vertical", vgroup)
vd = decel(vg)
vd.to_csv(OUT / "cross_section_verticals.csv", index=False)

GEO_RULES = [("NA", ["north america", "americas", "america", "usa", "us"]), ("EUROPE", ["europe", "uk", "emea"]),
             ("ROW", ["rest", "row", "asia", "apac", "india", "growth", "apmea", "middle east", "latin"])]

def ggroup(name):
    n = name.lower()
    if "continental europe" in n or "europe" in n or "uk" == n or "united kingdom" in n or "emea" in n:
        return "EUROPE"
    for g, keys in GEO_RULES:
        if any(n == k or n.startswith(k) for k in keys):
            return g
    return "OTHER"

gg = segment_growth(p, "geography", ggroup)
gd = decel(gg)
gd.to_csv(OUT / "cross_section_geographies.csv", index=False)

# ---------------------------------------------------------------- Cross-section: service lines & AI exposure
# Baseline classification (see DECISIONS): high = run/maintain/BPO work; low = consulting, engineering R&D; products excluded
AI_CLASS = {
    "baseline": {
        ("accenture", "Managed Services"): "high", ("accenture", "Outsourcing"): "high", ("accenture", "Consulting"): "low",
        ("cognizant", "Outsourcing services"): "high", ("cognizant", "Consulting and technology services"): "low",
        ("hcltech", "IT and Business Services"): "high", ("hcltech", "Engineering and R&D Services"): "low",
        ("techm", "BPO"): "high", ("techm", "BPS"): "high", ("techm", "IT"): "low",
    },
}
# Alternative A: ER&D is software-engineering heavy -> high; HCL contrast becomes 0 (both high) -> dropped
AI_CLASS["alt_ERD_high"] = {k: v for k, v in AI_CLASS["baseline"].items() if k[0] != "hcltech"}
# Alternative B: consulting is knowledge work highly exposed to GenAI -> Accenture/Cognizant contrasts flip sign
AI_CLASS["alt_consulting_high"] = {k: ({"high": "low", "low": "high"}[v] if k[0] in ("accenture", "cognizant") else v)
                                   for k, v in AI_CLASS["baseline"].items()}
# Alternative C: BPO/BPS already automated / voice-heavy -> TechM dropped
AI_CLASS["alt_BPS_neutral"] = {k: v for k, v in AI_CLASS["baseline"].items() if k[0] != "techm"}

def sl_growth(p):
    """Service-line YoY growth: reported segment_growth_yoy (cc preferred). Where the firm reports only levels
    (Cognizant 2018+, TechM IT/BPS in INR, HCL/Accenture gaps), YoY log change of the level in reported currency
    (noted as a limitation: includes FX)."""
    x = p[(p.dim_type == "service_line") & (p.metric == "segment_growth_yoy") & (p.period_type == "quarter")]
    x = x.sort_values("basis").drop_duplicates(["firm", "cal_q", "dimension"])
    g = x[["firm", "cal_q", "dimension", "value", "basis"]].rename(columns={"value": "g"})
    g["g"] = 100 * np.log1p(g.g / 100)
    lev = p[(p.dim_type == "service_line") & (p.metric == "segment_revenue") & (p.period_type == "quarter")].copy()
    lev["dimension"] = lev.dimension.replace({("BPO"): "BPS"}) if True else lev.dimension
    lev = lev.sort_values(["unit", "doc_date"], ascending=[True, False]).drop_duplicates(["firm", "cal_q", "dimension"])
    out = []
    for (f, dim), s in lev.groupby(["firm", "dimension"]):
        s = s.set_index("cal_q").value.sort_index()
        for q in s.index:
            ql = f"{int(q[:4]) - 1}Q{q[-1]}"
            if ql in s.index and s[ql] > 0:
                out.append(dict(firm=f, cal_q=q, dimension=dim, g=100 * np.log(s[q] / s[ql]), basis="level_reported_ccy"))
    lv = pd.DataFrame(out)
    g["dimension"] = np.where((g.firm == "techm") & (g.dimension == "BPO"), "BPS", g.dimension)
    both = pd.concat([g, lv], ignore_index=True)
    both["pri"] = both.basis.map({"cc": 0, "reported": 1}).fillna(2)
    return both.sort_values("pri").drop_duplicates(["firm", "cal_q", "dimension"]).drop(columns="pri")


slg = sl_growth(p)

def sl_contrast(slg, cls):
    rows = []
    for (f, q), g in slg.groupby(["firm", "cal_q"]):
        hi = [r.g for r in g.itertuples() if cls.get((f, r.dimension)) == "high"]
        lo = [r.g for r in g.itertuples() if cls.get((f, r.dimension)) == "low"]
        if hi and lo:
            rows.append(dict(firm=f, cal_q=q, SLc=np.mean(hi) - np.mean(lo)))
    return pd.DataFrame(rows)

sl_rows = []
for name, cls in AI_CLASS.items():
    c = sl_contrast(slg, cls)
    c["classification"] = name
    sl_rows.append(c)
slc = pd.concat(sl_rows)
slc.to_csv(OUT / "cross_section_service_line_contrast.csv", index=False)

slsum = []
for (name, f), g in slc.groupby(["classification", "firm"]):
    for per, (a, b) in {"pre (2016-2022)": ("2016Q1", "2022Q4"), "FY24 (2023Q1-2024Q1)": ("2023Q1", "2024Q1"),
                        "recent (2024Q2-2026Q2)": ("2024Q2", "2026Q2")}.items():
        s = g[(g.cal_q >= a) & (g.cal_q <= b) & (~g.cal_q.isin(["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]))].SLc
        slsum.append(dict(classification=name, firm=f, period=per, mean_SLc=s.mean(), sd=s.std(), n=s.count()))
slsum = pd.DataFrame(slsum)
slsum.to_csv(OUT / "cross_section_service_line_summary.csv", index=False)

# ---------------------------------------------------------------- Fig 4: cross-section panels
fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
ax = axes[0]
pv = vd.pivot(index="grp", columns="firm", values="recent").reindex(columns=[f for f in MAIN if f in set(vd.firm)])
im = ax.imshow(pv.values, cmap="RdBu", vmin=-10, vmax=10, aspect="auto")
ax.set_yticks(range(len(pv.index))); ax.set_yticklabels(pv.index, fontsize=8)
ax.set_xticks(range(len(pv.columns))); ax.set_xticklabels([LABEL[c] for c in pv.columns], rotation=45, ha="right", fontsize=7)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        v = pv.values[i, j]
        if not np.isnan(v):
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7)
tw = two_way_share(vd, "recent")
ax.set_title(f"Vertical YoY growth, FY25+ mean (%)\nvariance share: vertical {tw['share_group']:.0%}, firm {tw['share_firm']:.0%}", fontsize=8.5)
ax = axes[1]
pv = gd.pivot(index="grp", columns="firm", values="recent").reindex(columns=[f for f in MAIN if f in set(gd.firm)])
ax.imshow(pv.values, cmap="RdBu", vmin=-10, vmax=10, aspect="auto")
ax.set_yticks(range(len(pv.index))); ax.set_yticklabels(pv.index, fontsize=8)
ax.set_xticks(range(len(pv.columns))); ax.set_xticklabels([LABEL[c] for c in pv.columns], rotation=45, ha="right", fontsize=7)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        v = pv.values[i, j]
        if not np.isnan(v):
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7)
tw2 = two_way_share(gd, "recent")
ax.set_title(f"Geography YoY growth, FY25+ mean (%)\nvariance share: geography {tw2['share_group']:.0%}, firm {tw2['share_firm']:.0%}", fontsize=8.5)
ax = axes[2]
b = slsum[slsum.classification == "baseline"].pivot(index="firm", columns="period", values="mean_SLc")
b = b[["pre (2016-2022)", "FY24 (2023Q1-2024Q1)", "recent (2024Q2-2026Q2)"]]
b.index = [LABEL[i] for i in b.index]
b.plot.bar(ax=ax, color=["#bbbbbb", "#e39b2d", "#1f4e79"], width=0.8)
ax.axhline(0, color="k", lw=0.5)
ax.set_title("Service-line contrast: YoY growth of high-AI-exposure\nminus low-exposure lines (baseline classification)", fontsize=8.5)
ax.legend(fontsize=7); ax.tick_params(axis="x", rotation=0, labelsize=7.5)
fig.suptitle("Fig 4. Cross-section of the recent period: demand-side segments vs AI-exposed service lines", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(FIG / "fig4_cross_section.png", dpi=150)
plt.close(fig)
pd.DataFrame([dict(dim="vertical", **tw), dict(dim="geography", **tw2),
              dict(dim="vertical_decel", **two_way_share(vd, "decel")), dict(dim="geography_decel", **two_way_share(gd, "decel"))]
             ).to_csv(OUT / "cross_section_variance_shares.csv", index=False)

# ---------------------------------------------------------------- Fig 5: Indian vs comparators
ind = yoy[yoy.firm.isin(INDIAN + ["lti", "mindtree"])]
ind = ind[~((ind.firm == "ltim") & (ind.cal_q < "2022Q3"))]
agg = ind.groupby("cal_q")[["gR", "gL", "gRPE"]].median()
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), sharex=True)
qs = sorted(q for q in set(yoy.cal_q) if "2016Q1" <= q <= "2026Q2")
x = np.arange(len(qs))
for ax, m, t in zip(axes, ["gR", "gL", "gRPE"], ["Revenue growth (cc, YoY %)", "Headcount growth (YoY %)", "Revenue per employee growth (YoY %)"]):
    ax.plot(x, agg[m].reindex(qs), color="#1f4e79", lw=2, label="Indian firms (median)")
    for f, c in [("cognizant", "#e39b2d"), ("accenture", "#7b3294")]:
        ax.plot(x, yoy[yoy.firm == f].set_index("cal_q")[m].reindex(qs), color=c, lw=1.3, label=LABEL[f])
    ax.axhline(0, color="k", lw=0.5)
    ax.axvspan(qs.index("2024Q2") - 0.5, len(qs) - 0.5, color="#f4e3c1", alpha=0.5, lw=0)
    ax.set_title(t, fontsize=9)
    ticks = [i for i, q in enumerate(qs) if q.endswith("Q1") and int(q[:4]) % 2 == 0]
    ax.set_xticks(ticks); ax.set_xticklabels([qs[i][:4] for i in ticks], fontsize=7)
axes[0].legend(fontsize=7)
fig.suptitle("Fig 5. Indian vendors vs comparators", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FIG / "fig5_india_vs_comparators.png", dpi=150)
plt.close(fig)

# comovement stats
cm = []
for per, (a, b) in {"pre (2016-2022, ex-COVID)": ("2016Q1", "2022Q4"), "2023Q1-2026Q2": ("2023Q1", "2026Q2")}.items():
    for f in COMPARATORS:
        s = yoy[yoy.firm == f].set_index("cal_q")
        for m in ["gR", "gL"]:
            j = pd.concat([agg[m], s[m]], axis=1, keys=["ind", "cmp"]).dropna()
            j = j[(j.index >= a) & (j.index <= b) & (~j.index.isin(["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]))]
            cm.append(dict(period=per, comparator=f, metric=m, corr=j.ind.corr(j.cmp), mean_gap=(j.ind - j.cmp).mean(), n=len(j)))
pd.DataFrame(cm).to_csv(OUT / "india_vs_comparators.csv", index=False)
print(summ.to_string())
print(pd.DataFrame(cm).round(2).to_string())
print(slsum[slsum.classification == "baseline"].round(2).to_string())
print(pd.read_csv(OUT / "cross_section_variance_shares.csv").round(2))
