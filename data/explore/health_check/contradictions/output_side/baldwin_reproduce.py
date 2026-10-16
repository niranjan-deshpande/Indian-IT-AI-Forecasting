"""Reproduce Baldwin (30 Jul 2026) 'The Jobs AI Was Supposed to Eliminate Are Booming' from free WTO data,
and build the computer-services equivalent from IMF BoP.

Inputs (downloaded by fetch_wto_imf.py):
  ../raw_output/wto/its_cs_qx_nine.json  WTO ITS_CS_QX via DBnomics, USD mn, partner World
  ../raw_output/imf/imf_bop_ind_q.csv    IMF BOP India quarterly credits (RBI-compiled), USD
Outputs (this folder):
  baldwin_obs_rolling4q.csv        4-quarter rolling sums, nine economies, + index 2022Q4=100
  baldwin_table_reproduced.csv     Baldwin's table recomputed next to his published numbers
  india_trend_gap.csv              actual vs 2015-22 log-linear trend, several India series and fit windows
  india_series_quarterly.csv       India quarterly: WTO SI/SJ, IMF SI/SI2/SJ, 4q rolling sums
  fig_baldwin_india_obs_trend.png, fig_india_computer_trend.png, fig_baldwin_index.png
Run: python3 -I baldwin_reproduce.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from load import dn_tidy, imf

OUT = os.path.dirname(os.path.abspath(__file__))
NAMES = {"840": "United States", "826": "United Kingdom", "356": "India", "276": "Germany", "702": "Singapore",
         "250": "France", "156": "China", "056": "Belgium", "608": "Philippines"}
PUBLISHED = {  # Baldwin's table (image cb71a76a...png): 2025 level US$bn, 2024 growth, 2025 growth, Q4 2025 index
    "United States": (286.4, 8.4, 8.6, 122), "United Kingdom": (253.8, 10.9, 9.8, 131), "India": (184.7, 14.5, 17.3, 153),
    "Germany": (144.8, 8.5, 9.4, 133), "Singapore": (128.8, 11.5, 11.2, 138), "France": (126.6, 8.7, 10.0, 129),
    "China": (122.6, 7.9, 8.8, 123), "Belgium": (59.2, 4.7, 1.4, 116), "Philippines": (25.4, 5.9, 2.8, 118)}

def qindex(p):  # '2025-Q4' -> PeriodIndex
    return pd.PeriodIndex([x.replace("-", "") for x in p], freq="Q")

# ---- 1. WTO OBS, nine economies -------------------------------------------------------------
q = dn_tidy("its_cs_qx_nine.json")
q["economy"] = q.reporter.map(NAMES)
sj = q[q.sector == "SJ"].pivot(index="period", columns="economy", values="value")
sj.index = qindex(sj.index); sj = sj.sort_index()
roll = sj.rolling(4).sum()
idx = roll / roll.loc[pd.Period("2022Q4")] * 100
long = roll.stack().rename("obs_exports_4q_usd_bn").to_frame().join(idx.stack().rename("index_2022q4_100"))
long.index.names = ["quarter", "economy"]
long.reset_index().assign(quarter=lambda d: d.quarter.astype(str), source="WTO ITS_CS_QX via DBnomics, sector SJ, partner World") \
    .to_csv(os.path.join(OUT, "baldwin_obs_rolling4q.csv"), index=False)

rows = []
for e in NAMES.values():
    a = sj[e].groupby(sj.index.year).sum(min_count=4)
    pub = PUBLISHED[e]
    rows.append(dict(economy=e, lvl2025_ours=round(a[2025], 1), lvl2025_baldwin=pub[0],
                     g2024_ours=round((a[2024] / a[2023] - 1) * 100, 1), g2024_baldwin=pub[1],
                     g2025_ours=round((a[2025] / a[2024] - 1) * 100, 1), g2025_baldwin=pub[2],
                     idx_q4_2025_ours=round(idx.loc[pd.Period("2025Q4"), e], 0), idx_q4_2025_baldwin=pub[3],
                     lvl2022_ours=round(a[2022], 1)))
tab = pd.DataFrame(rows); tab.to_csv(os.path.join(OUT, "baldwin_table_reproduced.csv"), index=False)
print(tab.to_string(index=False))

# ---- 2. India series: WTO-adjusted vs IMF/RBI as published ------------------------------------
wi = q[q.reporter == "356"].pivot(index="period", columns="sector", values="value")
wi.index = qindex(wi.index); wi = wi.add_prefix("wto_")
im = imf("imf_bop_ind_q.csv"); im = im[im.BOP_ACCOUNTING_ENTRY == "CD_T"].pivot_table(index="TIME_PERIOD", columns="INDICATOR", values="value")
im.index = qindex(im.index); im = im.add_prefix("imf_")
ind = wi.join(im, how="outer").sort_index()
ind["wto_SI_share_of_imf_SI"] = ind.wto_SI / ind.imf_SI
ind["wto_reallocated_SI_to_SJ"] = ind.imf_SI - ind.wto_SI
ind["imf_SI2_plus_SJ"] = ind.imf_SI2 + ind.imf_SJ
for c in ["wto_SJ", "wto_SI", "imf_SJ", "imf_SI2", "imf_SI2_plus_SJ", "imf_S"]:
    ind[c + "_4q"] = ind[c].rolling(4).sum()
o = ind.copy(); o.index = o.index.astype(str); o.index.name = "quarter"
o.round(3).to_csv(os.path.join(OUT, "india_series_quarterly.csv"))
print("\nWTO SI as share of IMF SI (India):", ind.wto_SI_share_of_imf_SI.loc["2015Q1":"2025Q4"].describe().round(3).to_dict())

# ---- 3. Trend gaps --------------------------------------------------------------------------
def trend_gap(s, fit_from, fit_to, at):
    s = s.dropna(); f = s.loc[fit_from:fit_to]
    t = np.array([p.ordinal for p in f.index]); b, a = np.polyfit(t, np.log(f.values), 1)
    pred = lambda p: np.exp(a + b * pd.Period(p).ordinal)
    out = {"trend_growth_pct_yr": (np.exp(4 * b) - 1) * 100}
    for p in at:
        if pd.Period(p) in s.index:
            out[f"gap_{p}_pct"] = (s.loc[pd.Period(p)] / pred(p) - 1) * 100
    return out, (a, b)

series = {"WTO OBS (Baldwin's series; incl. ~32% of India's computer line reallocated)": "wto_SJ_4q",
          "IMF/RBI OBS as published (SJ)": "imf_SJ_4q",
          "IMF/RBI computer services (SI2)": "imf_SI2_4q",
          "IMF/RBI computer + OBS (SI2+SJ)": "imf_SI2_plus_SJ_4q",
          "WTO computer/telecom/info after reallocation (SI)": "wto_SI_4q",
          "IMF/RBI total services (S)": "imf_S_4q"}
windows = [("2015Q1", "2022Q4"), ("2015Q4", "2022Q4"), ("2010Q4", "2019Q4"), ("2015Q1", "2019Q4")]
gr = []
for lab, col in series.items():
    for w in windows:
        g, _ = trend_gap(ind[col], w[0], w[1], ["2022Q4", "2025Q4", "2026Q2"])
        s = ind[col].dropna()
        cagr_pre = ((s.loc[pd.Period("2022Q4")] / s.loc[pd.Period("2015Q4")]) ** (1 / 7) - 1) * 100
        cagr_post = ((s.loc[pd.Period("2025Q4")] / s.loc[pd.Period("2022Q4")]) ** (1 / 3) - 1) * 100
        gr.append(dict(series=lab, column=col, fit_window=f"{w[0]}-{w[1]}", **{k: round(v, 1) for k, v in g.items()},
                       cagr_2015_22_pct=round(cagr_pre, 1), cagr_2022_25_pct=round(cagr_post, 1)))
gr = pd.DataFrame(gr); gr.to_csv(os.path.join(OUT, "india_trend_gap.csv"), index=False)
print(gr.to_string(index=False))

# ---- 4. Charts --------------------------------------------------------------------------------
def trend_chart(col, title, fname, last="2025Q4"):
    s = ind[col].dropna().loc["2013Q1":last]
    _, (a, b) = trend_gap(ind[col], "2015Q1", "2022Q4", [])
    t = np.array([p.ordinal for p in s.index]); x = s.index.to_timestamp(how="end")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2021-12-31"), color="#c9d6ea", alpha=.5, lw=0)
    ax.axvspan(pd.Timestamp("2022-11-30"), x[-1], color="#f3d3cf", alpha=.5, lw=0)
    ax.plot(x, s.values, color="#1f4e9c", lw=2.2, label="Actual, 4-quarter rolling sum")
    ax.plot(x, np.exp(a + b * t), "--", color="#1f4e9c", lw=1.2, label="Log-linear trend fitted 2015Q1-2022Q4")
    gap = (s.iloc[-1] / np.exp(a + b * t[-1]) - 1) * 100
    ax.set_yscale("log"); ax.set_ylabel("US$ bn (log scale)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_yticks([25, 50, 75, 100, 150, 200, 250]); ax.set_ylim(30, 260); ax.set_title(title, fontsize=11)
    p0 = pd.Period("2022Q4"); g0 = (s.loc[p0] / np.exp(a + b * p0.ordinal) - 1) * 100
    ax.scatter([p0.to_timestamp(how="end")], [s.loc[p0]], color="#b03a2e", zorder=5, s=18)
    ax.annotate(f"already {g0:+.0f}% at 2022Q4", xy=(p0.to_timestamp(how="end"), s.loc[p0]), xytext=(8, -18), textcoords="offset points", color="#b03a2e", fontsize=8)
    ax.text(0.98, 0.04, f"{gap:+.0f}% vs trend at {s.index[-1]}", transform=ax.transAxes, ha="right", color="#1f4e9c", fontsize=10)
    ax.legend(loc="upper left", frameon=False, fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=150); plt.close(fig)
trend_chart("wto_SJ_4q", "India 'other business services' exports, WTO basis (Baldwin's series)", "fig_baldwin_india_obs_trend.png")
trend_chart("imf_SI2_4q", "India computer services exports, IMF/RBI BoP (SI2), to 2026Q2", "fig_india_computer_trend.png", last="2026Q2")
trend_chart("imf_SI2_plus_SJ_4q", "India computer + other business services, IMF/RBI BoP, to 2026Q2", "fig_india_computer_plus_obs_trend.png", last="2026Q2")

fig, ax = plt.subplots(figsize=(7, 4.2))
for e in NAMES.values():
    s = idx[e].loc["2019Q1":"2025Q4"]
    ax.plot(s.index.to_timestamp(how="end"), s.values, lw=2.4 if e == "India" else 1.2, label=f"{e} ({s.iloc[-1]:.0f})")
ax.axhline(100, color="k", lw=.6, ls=":"); ax.legend(fontsize=7, frameon=False, ncol=2)
ax.set_title("Other business services exports, 4q rolling, 2022Q4 = 100 (WTO)", fontsize=11); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_baldwin_index.png"), dpi=150); plt.close(fig)
