"""Final-pass tables and figures for the research note (built from data/corrected/*_final.csv; nothing hand-computed).

    python3 scripts/final/tables_figures.py        (or scripts/final/make_all.py to rebuild the data first)

Outputs (output/final/ and figures/final/):
  table_A.csv / table_A.md   fiscal-year growth FY16-FY26 + "FY27 Q1 (one quarter)"
  table_A_firms.csv          the same metrics per Indian entity (inputs to the averages)
  table_B.csv / table_B.md   residual and utilization change, FY16-FY23 vs FY24-FY26
  fig1_india_vs_comparators.{png,svg}, fig2_subcontracting_share.{png,svg}

Definitions (all growth = log change x 100, so revenue-per-employee growth = revenue growth - headcount growth exactly):
  Indian fiscal year t = calendar quarters (t-1)Q2 .. tQ1 (Apr-Mar). Comparators use the audit's calendar mapping
  (each fiscal quarter -> calendar quarter containing its end): Cognizant aligns exactly; Accenture's quarters end
  May/Aug/Nov/Feb, so an "Indian FY" for Accenture covers Mar-Feb (11 of 12 months overlap).
  revenue (USD, cc): ln( sum_q R_{q-4} * exp(g_q) / sum_q R_{q-4} ), g_q = quarterly YoY log growth (USD: gR_usd;
      cc: ln(1 + firm-reported cc YoY)), R_{q-4} = USD revenue a year earlier. For USD this equals the log change of
      fiscal-year revenue; for cc it aggregates firm-reported cc growth with prior-year revenue weights.
  headcount: mean of the four quarterly YoY log changes of quarter-end headcount (~ growth of average headcount).
      Year-end headcount growth (Q4 vs Q4) is reported separately.
  revenue per employee: revenue growth (cc, and USD) - headcount growth.
  utilization change: mean of the four quarterly YoY log changes, within each firm's reported series.
  residual: revenue-per-employee growth (cc) - utilization change; only for firms reporting utilization.
  A fiscal-year value needs all four quarters; otherwise it is missing.
  LTI counted once: FY16-FY22 = LTI + Mindtree combined (summed USD revenue and headcount; utilization change =
      headcount-weighted mean of the two firms' within-series changes; cc missing because Mindtree reports no cc YoY);
      FY23 on = LTIMindtree (its restated combined history covers FY22, so FY23 growth is one entity in both years).
  Indian averages: simple mean over the six entities with data; revenue-weighted by fiscal-year USD revenue.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "final"
FIG = ROOT / "figures" / "final"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams["svg.fonttype"] = "none"

core = pd.read_csv(ROOT / "data/corrected/core_quarterly_final.csv", dtype={"cal_q": str})
yoy = pd.read_csv(ROOT / "data/corrected/yoy_metrics_final.csv", dtype={"cal_q": str})
d = yoy.merge(core[["firm", "cal_q", "rev_usd", "headcount"]], on=["firm", "cal_q"], how="left")

INDIAN5 = ["tcs", "infosys", "hcltech", "wipro", "techm"]
NAME = {"tcs": "TCS", "infosys": "Infosys", "hcltech": "HCLTech", "wipro": "Wipro", "techm": "Tech Mahindra",
        "lti_group": "LTI group (LTI+Mindtree to FY22, LTIMindtree from FY23)", "accenture": "Accenture",
        "cognizant": "Cognizant"}


def qadd(q, k):
    y, n = int(q[:4]), int(q[-1])
    t = y * 4 + n - 1 + k
    return f"{t // 4}Q{t % 4 + 1}"


def fy_quarters(fy):           # FY2024 -> 2023Q2..2024Q1
    return [f"{fy - 1}Q2", f"{fy - 1}Q3", f"{fy - 1}Q4", f"{fy}Q1"]


def lti_group_quarterly():
    """Quarterly series for the LTI business counted once (see module docstring)."""
    rows = []
    c = core.set_index(["firm", "cal_q"])
    y = yoy.set_index(["firm", "cal_q"])
    for q in sorted(set(core.cal_q)):
        if q < "2015Q1":
            continue
        fy = int(q[:4]) + (1 if q[-1] != "1" else 0)
        r = dict(firm="lti_group", cal_q=q)
        if fy <= 2022:   # LTI + Mindtree
            def lv(f, col, qq):
                return c[col].get((f, qq), np.nan)
            R = lv("lti", "rev_usd", q) + lv("mindtree", "rev_usd", q)
            R0 = lv("lti", "rev_usd", qadd(q, -4)) + lv("mindtree", "rev_usd", qadd(q, -4))
            L = lv("lti", "headcount", q) + lv("mindtree", "headcount", q)
            L0 = lv("lti", "headcount", qadd(q, -4)) + lv("mindtree", "headcount", qadd(q, -4))
            r.update(rev_usd=R, headcount=L, gR_usd=100 * np.log(R / R0), gL=100 * np.log(L / L0), gR=np.nan)
            du = [(y["du"].get((f, q), np.nan), lv(f, "headcount", q)) for f in ("lti", "mindtree")]
            du = [(a, w) for a, w in du if pd.notna(a) and pd.notna(w)]
            r["du"] = np.average([a for a, _ in du], weights=[w for _, w in du]) if len(du) == 2 else np.nan
        else:            # LTIMindtree
            for col in ["rev_usd", "headcount"]:
                r[col] = c[col].get(("ltim", q), np.nan)
            for col in ["gR_usd", "gL", "gR", "du"]:
                r[col] = y[col].get(("ltim", q), np.nan)
        rows.append(r)
    return pd.DataFrame(rows)


q = pd.concat([d[d.firm.isin(INDIAN5 + ["accenture", "cognizant"])], lti_group_quarterly()], ignore_index=True)
q = q.set_index(["firm", "cal_q"]).sort_index()
ENTITIES = INDIAN5 + ["lti_group"]


def fy_metrics(firm, quarters):
    """Aggregate quarterly YoY observations over the given quarters (all must be present)."""
    out = {}
    def get(col, qq):
        return q[col].get((firm, qq), np.nan) if col in q else np.nan
    base = np.array([get("rev_usd", qadd(qq, -4)) for qq in quarters], dtype=float)
    cur = np.array([get("rev_usd", qq) for qq in quarters], dtype=float)
    for lab, col in [("rev_usd", "gR_usd"), ("rev_cc", "gR")]:
        g = np.array([get(col, qq) for qq in quarters], dtype=float)
        ok = np.isfinite(g).all() and np.isfinite(base).all()
        out[lab] = 100 * np.log((base * np.exp(g / 100)).sum() / base.sum()) if ok else np.nan
    for lab, col in [("headcount", "gL"), ("util_change", "du")]:
        g = np.array([get(col, qq) for qq in quarters], dtype=float)
        out[lab] = g.mean() if np.isfinite(g).all() else np.nan
    out["headcount_yearend"] = get("gL", quarters[-1])
    out["rpe_cc"] = out["rev_cc"] - out["headcount"]
    out["rpe_usd"] = out["rev_usd"] - out["headcount"]
    out["residual"] = out["rpe_cc"] - out["util_change"]
    out["weight_rev_usd"] = cur.sum() if np.isfinite(cur).all() else np.nan
    return out


PERIODS = [(f"FY{fy % 100:02d}", fy_quarters(fy)) for fy in range(2016, 2027)] + [("FY27 Q1 (one quarter)", ["2026Q2"])]
METRICS = ["rev_usd", "rev_cc", "headcount", "headcount_yearend", "rpe_usd", "rpe_cc", "util_change", "residual"]
LABEL = {"rev_usd": "Revenue, USD", "rev_cc": "Revenue, constant currency", "headcount": "Headcount (avg-based)",
         "headcount_yearend": "Headcount, year-end", "rpe_usd": "Rev/employee, USD", "rpe_cc": "Rev/employee, cc",
         "util_change": "Utilization change", "residual": "Residual g(R/L)-g(u)"}

firm_rows = []
for per, qs in PERIODS:
    for f in ENTITIES + ["accenture", "cognizant"]:
        firm_rows.append(dict(period=per, firm=f, **fy_metrics(f, qs)))
F = pd.DataFrame(firm_rows)
F.round(3).to_csv(OUT / "table_A_firms.csv", index=False)

agg = []
for per, g in F[F.firm.isin(ENTITIES)].groupby("period", sort=False):
    for m in METRICS:
        x = g[g[m].notna()]
        w = x[x.weight_rev_usd.notna()]
        agg.append(dict(period=per, group="Indian simple average", metric=m,
                        value=x[m].mean() if len(x) else np.nan, n_firms=len(x),
                        firms=";".join(NAME[f].split(" (")[0] for f in x.firm)))
        agg.append(dict(period=per, group="Indian revenue-weighted average", metric=m,
                        value=np.average(w[m], weights=w.weight_rev_usd) if len(w) else np.nan, n_firms=len(w),
                        firms=";".join(NAME[f].split(" (")[0] for f in w.firm)))
for f in ["accenture", "cognizant"]:
    for _, r in F[F.firm == f].iterrows():
        for m in METRICS:
            agg.append(dict(period=r.period, group=NAME[f], metric=m, value=r[m], n_firms=int(pd.notna(r[m])), firms=NAME[f]))
A = pd.DataFrame(agg)
A.round(3).to_csv(OUT / "table_A.csv", index=False)

# ---------------------------------------------------------------- Table B
B = []
for lab, years in [("FY16-FY23", [f"FY{y:02d}" for y in range(16, 24)]), ("FY24-FY26", ["FY24", "FY25", "FY26"])]:
    for excl21 in (False, True):
        ys = [y for y in years if not (excl21 and y == "FY21")]
        x = F[F.firm.isin(ENTITIES) & F.period.isin(ys)]
        for m in ["residual", "util_change"]:
            v = x[x[m].notna()]
            B.append(dict(window=lab + (" excl. FY21 (COVID)" if excl21 else ""), metric=m,
                          mean_firm_years=v[m].mean(), n_firm_years=len(v), n_firms=v.firm.nunique(),
                          firms=";".join(sorted(NAME[f].split(" (")[0] for f in v.firm.unique())),
                          mean_of_yearly_simple_avg=v.groupby("period")[m].mean().mean()))
    if lab == "FY24-FY26":
        B = [b for b in B if not (b["window"].startswith("FY24-FY26 excl"))]
# same firms in both windows (firms with at least one residual observation in each window)
pre = set(F[F.firm.isin(ENTITIES) & F.period.isin([f"FY{y:02d}" for y in range(16, 24)]) & F.residual.notna()].firm)
post = set(F[F.firm.isin(ENTITIES) & F.period.isin(["FY24", "FY25", "FY26"]) & F.residual.notna()].firm)
both = sorted(pre & post)
for lab, years in [("FY16-FY23, same firms", [f"FY{y:02d}" for y in range(16, 24)]),
                   ("FY16-FY23 excl. FY21, same firms", [f"FY{y:02d}" for y in range(16, 24) if y != 21]),
                   ("FY24-FY26, same firms", ["FY24", "FY25", "FY26"])]:
    x = F[F.firm.isin(both) & F.period.isin(years)]
    for m in ["residual", "util_change"]:
        v = x[x[m].notna() & x.residual.notna()]
        B.append(dict(window=lab, metric=m, mean_firm_years=v[m].mean(), n_firm_years=len(v), n_firms=v.firm.nunique(),
                      firms=";".join(sorted(NAME[f].split(" (")[0] for f in v.firm.unique())),
                      mean_of_yearly_simple_avg=v.groupby("period")[m].mean().mean()))
TB = pd.DataFrame(B)
TB.round(3).to_csv(OUT / "table_B.csv", index=False)

# ---------------------------------------------------------------- markdown versions
def fmt(v):
    return "–" if pd.isna(v) else f"{v:+.1f}"


lines = ["# Table A. Fiscal-year growth (log change × 100), Indian fiscal years (Apr–Mar)", "",
         "Generated by `scripts/final/tables_figures.py` from `data/corrected/*_final.csv`; definitions in the script docstring.",
         "The last row (FY27 Q1) is **one quarter** (Apr–Jun 2026 vs Apr–Jun 2025), not a fiscal year.",
         "Accenture: its fiscal quarters ending May/Aug/Nov/Feb are placed in the calendar quarter containing the quarter end, "
         "so its 'Indian fiscal year' covers Mar–Feb (11 of 12 months overlap); FY27 Q1 for Accenture is its quarter ending 31 May 2026. "
         "Accenture's Q4FY26 (Jun–Aug 2026, added in this pass) falls in Indian Q2FY27 and is therefore not in this table.", ""]
for grp in ["Indian simple average", "Indian revenue-weighted average", "Accenture", "Cognizant"]:
    lines += [f"## {grp}", "", "| period | " + " | ".join(LABEL[m] for m in METRICS) + " | n firms (rev USD, rev cc, util, residual) |",
              "|" + "---|" * (len(METRICS) + 2)]
    for per, _ in PERIODS:
        x = A[(A.group == grp) & (A.period == per)].set_index("metric")
        n = (f"{int(x.loc['rev_usd','n_firms'])}, {int(x.loc['rev_cc','n_firms'])}, {int(x.loc['util_change','n_firms'])}, {int(x.loc['residual','n_firms'])}"
             if grp.startswith("Indian") else "")
        lines.append(f"| {per} | " + " | ".join(fmt(x.loc[m, "value"]) for m in METRICS) + f" | {n} |")
    lines.append("")
lines += ["## Indian firms in the utilization-change and residual columns, by year", "",
          "Utilization change needs four quarters of a firm's own utilization series; the residual also needs cc revenue "
          "and headcount growth (Wipro FY18-FY20 headcount growth is excluded by decision 3).", "",
          "| period | utilization change (firms reporting utilization) | residual |", "|---|---|---|"]
for per, _ in PERIODS:
    u = A[(A.group == "Indian simple average") & (A.period == per) & (A.metric == "util_change")].firms.iloc[0]
    x = A[(A.group == "Indian simple average") & (A.period == per) & (A.metric == "residual")].firms.iloc[0]
    lines.append(f"| {per} | {u or 'none'} | {x or 'none'} |")
lines += ["", "Firms with constant-currency revenue, by year (the cc and residual columns use only these):", "",
          "| period | firms |", "|---|---|"]
for per, _ in PERIODS:
    x = A[(A.group == "Indian simple average") & (A.period == per) & (A.metric == "rev_cc")]
    lines.append(f"| {per} | {x.firms.iloc[0]} |")
(OUT / "table_A.md").write_text("\n".join(lines) + "\n")

lb = ["# Table B. Residual and utilization change before and after FY24 (Indian entities, firm-year means)", "",
      "Residual = revenue-per-employee growth (cc) − utilization change; only firm-years with utilization data and cc revenue. "
      "Generated by `scripts/final/tables_figures.py`.", "",
      "| window | metric | mean over firm-years | firm-years | firms | mean of yearly averages | firms included |",
      "|---|---|---|---|---|---|---|"]
for _, r in TB.iterrows():
    lb.append(f"| {r.window} | {r.metric} | {fmt(r.mean_firm_years)} | {r.n_firm_years} | {r.n_firms} | "
              f"{fmt(r.mean_of_yearly_simple_avg)} | {r.firms} |")
(OUT / "table_B.md").write_text("\n".join(lb) + "\n")

# ---------------------------------------------------------------- figures (validated reference palette, light mode)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C3 = {"Indian revenue-weighted average": "#2a78d6", "Accenture": "#eb6834", "Cognizant": "#1baf7a"}
fys = [p for p, _ in PERIODS if p.startswith("FY") and "Q1" not in p]
xi = np.arange(len(fys))


def style(ax):
    ax.axhline(0, color=INK, lw=0.6)
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.set_xticks(xi)
    ax.set_xticklabels(fys, fontsize=8)


fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=False)
for ax, m, t in zip(axes, ["rev_cc", "headcount", "rpe_cc"],
                    ["Revenue growth (constant currency)", "Headcount growth", "Revenue per employee growth (cc)"]):
    ax.axvspan(fys.index("FY24") - 0.5, fys.index("FY24") + 0.5, color="#d9d8d3", alpha=0.5, lw=0)
    ax.text(fys.index("FY24"), 0.97, "FY24", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=8, color=INK2)
    for grp, col in C3.items():
        v = A[(A.group == grp) & (A.metric == m)].set_index("period").value.reindex(fys)
        ax.plot(xi, v, color=col, lw=2.2 if grp.startswith("Indian") else 1.8, marker="o", ms=4,
                label=grp.replace("Indian revenue-weighted average", "Indian six (revenue-weighted)"))
    style(ax)
    ax.set_title(t, fontsize=9.5, loc="left", color=INK)
axes[0].set_ylabel("% (log change × 100), Indian fiscal year (Apr–Mar)", fontsize=8, color=INK2)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, fontsize=8.5, frameon=False)
fig.suptitle("Figure 1. Indian IT six vs Accenture and Cognizant, FY16–FY26", fontsize=11, color=INK, x=0.01, ha="left")
fig.text(0.01, 0.005, "Indian average = firms with data that year: cc revenue covers 4 firms in FY16-FY20, 5 in FY21-FY23, all 6 from FY24 "
         "(LTI group and, before FY21, Tech Mahindra lack cc); headcount covers 5-6. Comparators aggregated to Indian fiscal years; "
         "Accenture's year is offset by one month.\nHeadcount = growth of average headcount. Source: firm filings; output/final/table_A.csv.",
         fontsize=7, color=INK2)
fig.tight_layout(rect=[0, 0.1, 1, 0.93])
for ext in ("png", "svg"):
    fig.savefig(FIG / f"fig1_india_vs_comparators.{ext}", dpi=170)
plt.close(fig)

# Figure 2: subcontracting share (audit/subcontracting_series.csv, primary definition per firm)
S = pd.read_csv(ROOT / "audit/subcontracting_series.csv")
S = S[(S.period_type == "fiscal_year") & (S.primary == True)]
S = S[S.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"])]
years = [f"FY{y}" for y in range(20, 27)]
C6 = {"tcs": "#2a78d6", "infosys": "#eb6834", "hcltech": "#1baf7a", "wipro": "#eda100", "techm": "#e87ba4", "ltim": "#008300"}
fig, ax = plt.subplots(figsize=(8.5, 4.8))
xs = np.arange(len(years))
ax.axvspan(years.index("FY24") - 0.5, years.index("FY24") + 0.5, color="#d9d8d3", alpha=0.5, lw=0)
ax.text(years.index("FY24"), 0.97, "FY24", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=8, color=INK2)
fig2_tab = []
for f, col in C6.items():
    v = S[S.firm == f].set_index("fiscal_year").subcon_pct_rev.reindex(years)
    fig2_tab.append(v.rename(f))
    ax.plot(xs, v, color=col, lw=2, marker="o", ms=4, label="LTIMindtree" if f == "ltim" else NAME[f])
    last = v.last_valid_index()
    ax.text(years.index(last) + 0.12, v[last], "LTIMindtree" if f == "ltim" else NAME[f], fontsize=8, color=INK, va="center")
ax.grid(axis="y", color=GRID, lw=0.6)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_xticks(xs); ax.set_xticklabels(years, fontsize=8); ax.tick_params(colors=INK2, labelsize=8)
ax.set_xlim(-0.4, len(years) - 0.2)
ax.set_ylabel("subcontracting cost, % of revenue", fontsize=8, color=INK2)
ax.legend(fontsize=8, frameon=False, ncol=3, loc="lower left")
ax.set_title("Figure 2. Subcontracting cost as a share of revenue, six Indian firms, FY20–FY26", fontsize=10.5, color=INK, loc="left")
fig.text(0.01, 0.005, "Firm-reported subcontracting / external-consultant cost over revenue, same currency (INR). "
         "LTIMindtree from FY22 (annual reports; pre-merger LTI not collected). TCS FY27 definition break not shown. "
         "Source: audit/subcontracting_series.csv.", fontsize=6.5, color=INK2, wrap=True)
fig.tight_layout(rect=[0, 0.05, 1, 1])
for ext in ("png", "svg"):
    fig.savefig(FIG / f"fig2_subcontracting_share.{ext}", dpi=170)
plt.close(fig)
pd.concat(fig2_tab, axis=1).round(2).to_csv(OUT / "fig2_data.csv")
print((OUT / "table_A.md").read_text()[:200])
print(TB.round(2).to_string())
