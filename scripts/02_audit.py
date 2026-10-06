"""Part 1: coverage matrix (firm x metric x quarter) from data/tidy/panel_long.csv and core_quarterly.csv.

Outputs:
  output/coverage_matrix.csv   - firm x metric: first/last quarter, # quarters, coverage share in FY16+ and recent window
  figures/fig1_coverage.png    - heatmap of core-variable availability by firm and quarter
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from common import TIDY, FIG, OUT, LABEL, RECENT_START

p = pd.read_csv(TIDY / "panel_long.csv", low_memory=False)
core = pd.read_csv(TIDY / "core_quarterly.csv")
yoy = pd.read_csv(TIDY / "yoy_metrics.csv")

FIRM_ORDER = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim", "lti", "mindtree", "cognizant", "accenture"]
FIRM_ORDER = [f for f in FIRM_ORDER if f in set(p.firm)]
QS = [f"{y}Q{q}" for y in range(2015, 2027) for q in range(1, 5)]
QS = [q for q in QS if "2015Q2" <= q <= "2026Q2"]
RECENT = [q for q in QS if q >= RECENT_START]

# ---- metric families for the matrix ----
FAMILIES = {
    "Revenue USD (total)": lambda d: d[(d.metric == "revenue") & (d.unit == "USD_mn") & (d.dim_type.isin(["total", "other"]))],
    "Revenue growth cc (YoY)": lambda d: d[(d.metric == "revenue_growth_yoy") & (d.basis == "cc")],
    "Revenue growth cc (QoQ)": lambda d: d[(d.metric == "revenue_growth_qoq") & (d.basis == "cc")],
    "Revenue by vertical": lambda d: d[(d.dim_type == "vertical") & d.metric.isin(["revenue_share", "segment_revenue", "segment_growth_yoy"])],
    "Revenue by geography": lambda d: d[(d.dim_type == "geography") & d.metric.isin(["revenue_share", "segment_revenue", "segment_growth_yoy"])],
    "Revenue by service line": lambda d: d[(d.dim_type == "service_line") & d.metric.isin(["revenue_share", "segment_revenue", "segment_growth_yoy"])],
    "Headcount": lambda d: d[(d.metric == "headcount") & (d.dimension == "total")],
    "Net additions": lambda d: d[d.metric == "net_additions"],
    "Fresher hires": lambda d: d[d.metric == "fresher_hires"],
    "Attrition": lambda d: d[d.metric == "attrition"],
    "Utilization excl. trainees": lambda d: d[d.metric == "utilization_excl_trainees"],
    "Utilization incl. trainees": lambda d: d[d.metric.isin(["utilization_incl_trainees", "utilization_offshore"])],
    "Subcontracting cost": lambda d: d[d.metric.isin(["subcontracting_cost", "subcontracting_pct_rev"])],
    "TCV / bookings": lambda d: d[d.metric.isin(["tcv", "bookings"])],
    "Client buckets": lambda d: d[d.metric == "clients_bucket"],
    "Onsite/offshore mix": lambda d: d[d.metric.isin(["effort_share_offshore", "revenue_share_offshore", "revenue_share_onsite", "headcount_share_offshore"])],
    "AI disclosure": lambda d: d[d.metric == "ai_disclosure"],
}

rows = []
cov = {}
for fam, fn in FAMILIES.items():
    sub = fn(p)
    for f in FIRM_ORDER:
        qs = sorted(set(sub[(sub.firm == f)].cal_q.dropna()))
        qs_in = [q for q in qs if q in QS]
        cov[(fam, f)] = set(qs_in)
        rel = [q for q in QS if (f not in ("lti", "mindtree")) or q <= "2022Q3"]
        rel = [q for q in rel if (f != "ltim") or q >= "2021Q2"]
        rows.append(dict(metric=fam, firm=f, first=qs[0] if qs else "", last=qs[-1] if qs else "",
                         n_quarters_FY16on=len(qs_in),
                         share_FY16on=round(len(qs_in) / len(rel), 2) if rel else np.nan,
                         share_recent=round(len([q for q in qs_in if q in RECENT]) / len(RECENT), 2)
                         if f not in ("lti", "mindtree") else np.nan))
cm = pd.DataFrame(rows)
cm.to_csv(OUT / "coverage_matrix.csv", index=False)

# compact matrix for AUDIT.md: share of FY16+ quarters / share of recent quarters
def cell(r):
    if r.n_quarters_FY16on == 0:
        return "—"
    if np.isnan(r.share_recent):
        return f"{r.share_FY16on:.0%}"
    return f"{r.share_FY16on:.0%} / {r.share_recent:.0%}"
tab = cm.assign(cell=cm.apply(cell, axis=1)).pivot(index="metric", columns="firm", values="cell")
tab = tab.reindex(index=list(FAMILIES), columns=FIRM_ORDER)
tab.columns = [LABEL.get(c, c) for c in tab.columns]
tab.to_markdown(OUT / "coverage_table.md")

# ---- heatmap figure: core families ----
core_fams = ["Revenue growth cc (YoY)", "Headcount", "Utilization excl. trainees", "Utilization incl. trainees",
             "Attrition", "Revenue by service line", "Subcontracting cost", "TCV / bookings"]
firms_plot = [f for f in FIRM_ORDER]
fig, axes = plt.subplots(len(core_fams), 1, figsize=(11, 1.0 + 0.32 * len(firms_plot) * len(core_fams) / 2.2), sharex=True)
cmap = ListedColormap(["#eeeeee", "#2a6f97"])
for ax, fam in zip(axes, core_fams):
    M = np.array([[1 if q in cov[(fam, f)] else 0 for q in QS] for f in firms_plot])
    ax.imshow(M, aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_yticks(range(len(firms_plot)))
    ax.set_yticklabels([LABEL.get(f, f) for f in firms_plot], fontsize=6.5)
    ax.set_title(fam, fontsize=8.5, loc="left", pad=2)
    ax.axvline(QS.index(RECENT_START) - 0.5, color="#c0392b", lw=1)
    ax.tick_params(axis="x", length=0)
ticks = [i for i, q in enumerate(QS) if q.endswith("Q1")]
axes[-1].set_xticks(ticks)
axes[-1].set_xticklabels([QS[i][:4] for i in ticks], fontsize=7)
fig.suptitle("Fig 1. Data availability by firm and calendar quarter (blue = reported; red line = start of FY2025)", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.98])
fig.savefig(FIG / "fig1_coverage.png", dpi=150)
print(tab.to_string())

# usable YoY metric counts (after differencing) for Parts 2-4
use = yoy.groupby("firm")[["gR", "gL", "du", "gTCV", "dsub"]].agg(lambda s: s.notna().sum())
rec = yoy[yoy.cal_q >= RECENT_START].groupby("firm")[["gR", "gL", "du", "gTCV", "dsub"]].agg(lambda s: s.notna().sum())
use.join(rec, rsuffix="_recent").to_csv(OUT / "usable_yoy_counts.csv")
print(use.join(rec, rsuffix="_recent"))
