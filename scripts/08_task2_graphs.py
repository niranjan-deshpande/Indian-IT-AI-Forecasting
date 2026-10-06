"""Task 2: growth graphs from the corrected data (audit Task 1).

Regenerates every figure in figures/task2/ with one command:

    cd scripts && python 08_task2_graphs.py              # corrected data (data/corrected/)
    cd scripts && python 08_task2_graphs.py --original   # pilot data (data/tidy/), for comparison only

Inputs: data/corrected/core_quarterly_corrected.csv, data/corrected/yoy_metrics_corrected.csv
Outputs: figures/task2/*.png, figures/task2/plotted_series_*.csv (table view of every plotted line),
         figures/task2/weighting_check.csv (simple vs revenue-weighted Indian average)

Definitions (all growth rates are YoY log changes x 100):
  quarterly  revenue USD       ln(rev_usd_t / rev_usd_{t-4})                       (gR_usd)
             revenue cc        ln(1 + firm-reported YoY cc growth)                 (gR)
             headcount         ln(L_t / L_{t-4}); HCLTech base net of the Q1FY25 divestiture (gL)
             rev/employee      gR_usd - gL  (reported USD)
             utilization       ln(u_t / u_{t-4}) within one reported series        (du)
             residual          gR - gL - du  (cc revenue; the pilot's definition)  (resid)
  annual (calendar year; Accenture/Cognizant by the calendar quarter their fiscal quarter is mapped to)
             revenue USD       ln of the sum of 4 quarters vs previous year (needs all 4 quarters)
             cc, headcount, utilization, residual: mean of the 4 quarterly YoY values (needs all 4)
             rev/employee      annual revenue USD growth - annual headcount growth
Indian average: simple mean across the Indian firms reporting that quarter, and revenue-weighted
  mean (weights = USD revenue in the same quarter / year). Before 2022Q3 the pre-merger LTI and Mindtree
  form ONE entity (their revenue-weighted mean) and LTIMindtree is excluded; from 2022Q3 LTIMindtree only.
  No level splice (DECISIONS D9). This differs from the pilot, which counted LTI and Mindtree as two firms.
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from common import ROOT, FIG, INDIAN, LABEL

ap = argparse.ArgumentParser()
ap.add_argument("--original", action="store_true", help="use the pilot's data/tidy files instead of the corrected ones")
args = ap.parse_args()

if args.original:
    CORE, YOY, TAG = ROOT / "data/tidy/core_quarterly.csv", ROOT / "data/tidy/yoy_metrics.csv", "pilot data (uncorrected)"
    OUTD = FIG / "task2_original"
else:
    CORE, YOY, TAG = (ROOT / "data/corrected/core_quarterly_corrected.csv",
                      ROOT / "data/corrected/yoy_metrics_corrected.csv", "corrected data")
    OUTD = FIG / "task2"
OUTD.mkdir(parents=True, exist_ok=True)

PRE_MERGER = ["lti", "mindtree"]
COMPS = ["accenture", "cognizant"]
# categorical slots 1-8 of the validated reference palette (fixed order, never cycled)
COLOR = {"tcs": "#2a78d6", "infosys": "#eb6834", "hcltech": "#1baf7a", "wipro": "#eda100",
         "techm": "#e87ba4", "ltim": "#008300", "lti": "#008300", "mindtree": "#008300",
         "accenture": "#4a3aa7", "cognizant": "#e34948"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
UTIL_STOP_FIRMS = ["tcs", "hcltech"]

core = pd.read_csv(CORE, dtype={"cal_q": str})
yoy = pd.read_csv(YOY, dtype={"cal_q": str})
df = yoy.merge(core[["firm", "cal_q", "rev_usd", "headcount"]], on=["firm", "cal_q"], how="left")
df["gRPE_usd"] = df.gR_usd - df.gL


def qdate(q):
    """Middle of a calendar quarter, as a Timestamp (for plotting)."""
    y, n = int(q[:4]), int(q[-1])
    return pd.Timestamp(year=y, month=3 * n - 1, day=15)


def in_indian_avg(firm, q):
    if firm in PRE_MERGER:
        return q < "2022Q3"
    if firm == "ltim":
        return q >= "2022Q3"
    return firm in INDIAN


# ------------------------------------------------------------------ annual (calendar-year) panel
df["year"] = df.cal_q.str[:4].astype(int)
ann_rows = []
for (f, y), g in df.groupby(["firm", "year"]):
    full = len(g) == 4
    row = dict(firm=f, year=y, n_q=len(g), rev_usd=g.rev_usd.sum(min_count=4) if full else np.nan)
    for c in ["gR", "gL", "du", "resid"]:
        row[c] = g[c].mean() if full and g[c].notna().sum() == 4 else np.nan
    ann_rows.append(row)
ann = pd.DataFrame(ann_rows).sort_values(["firm", "year"])
ann["gR_usd"] = 100 * np.log(ann.rev_usd / ann.groupby("firm").rev_usd.shift(1))
ann.loc[ann.year.diff().ne(1) & ann.firm.eq(ann.firm.shift(1)), "gR_usd"] = np.nan
ann["gRPE_usd"] = ann.gR_usd - ann.gL
ann["cal_q"] = ann.year.astype(str) + "Q4"   # membership rule for the Indian average uses year-end


def collapse_lti_group(m, metric, period_col):
    """Pre-merger LTI and Mindtree count as ONE entity in the average (audit 1b: the pilot's two-entity treatment
    double-weights the LTI business). Its value is their USD-revenue-weighted mean (simple mean if a weight is missing)."""
    pre = m[m.firm.isin(PRE_MERGER)]
    rest = m[~m.firm.isin(PRE_MERGER)]
    rows = []
    for k, g in pre.groupby(period_col):
        w = g.rev_usd
        v = np.average(g[metric], weights=w) if w.notna().all() and w.sum() > 0 else g[metric].mean()
        rows.append({period_col: k, "firm": "lti_group", "cal_q": g.cal_q.iloc[0], metric: v,
                     "rev_usd": w.sum(min_count=len(g))})
    return pd.concat([rest, pd.DataFrame(rows)], ignore_index=True) if rows else rest


def indian_average(d, metric, period_col):
    m = d[[in_indian_avg(f, q) for f, q in zip(d.firm, d.cal_q)]]
    m = m[m[metric].notna()]
    m = collapse_lti_group(m, metric, period_col)
    out = m.groupby(period_col).apply(lambda g: pd.Series({
        "simple": g[metric].mean(),
        # weighted over the firms that also report USD revenue that period
        "weighted": np.average(g[metric][g.rev_usd.notna()], weights=g.rev_usd[g.rev_usd.notna()]) if g.rev_usd.notna().any() else np.nan,
        "n_firms": len(g), "n_firms_weighted": int(g.rev_usd.notna().sum())}), include_groups=False)
    return out


METRICS = [  # (column, title, file stem)
    ("gR_usd", "Revenue growth, reported USD", "01_revenue_usd"),
    ("gR", "Revenue growth, constant currency (as reported by each firm)", "02_revenue_cc"),
    ("gL", "Headcount growth", "03_headcount"),
    ("gRPE_usd", "Revenue per employee growth (reported USD revenue)", "04_revenue_per_employee"),
    ("du", "Utilization, YoY change (log points, within each firm's reported series)", "05_utilization"),
    ("resid", "Residual  g(R/L) − g(u)  (cc revenue; firms reporting utilization only)", "06_residual"),
]


def shade(ax):
    for a, b, lab in [("2008-01-01", "2009-12-31", "2008–09"), ("2020-04-01", "2021-06-30", "COVID")]:
        ax.axvspan(pd.Timestamp(a), pd.Timestamp(b), color="#d9d8d3", alpha=0.45, lw=0, zorder=0)
        ax.text(pd.Timestamp(a) + pd.Timedelta(days=20), 0.98, lab, transform=ax.get_xaxis_transform(),
                fontsize=7, color=INK2, va="top")
    for d, lab in [("2022-01-01", "2022"), ("2023-01-01", "2023Q1")]:
        ax.axvline(pd.Timestamp(d), color=INK2, lw=0.9, ls=(0, (4, 2)), zorder=1)
        ax.text(pd.Timestamp(d) + pd.Timedelta(days=15), 0.02, lab, transform=ax.get_xaxis_transform(),
                fontsize=7, color=INK2, rotation=90, va="bottom")


def style(ax, ylabel):
    ax.axhline(0, color=INK, lw=0.6, zorder=1)
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(INK2); ax.spines["bottom"].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.set_ylabel(ylabel, fontsize=8, color=INK2)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def util_stop_marks(ax, d, date_of):
    """Mark the last quarter/year with utilization data for TCS and HCLTech."""
    for f in UTIL_STOP_FIRMS:
        g = d[(d.firm == f) & d.du.notna()]
        if g.empty:
            continue
        last = g.iloc[-1]
        x = date_of(last)
        ax.axvline(x, color=COLOR[f], lw=1.2, ls=":", zorder=2)
        ax.text(x, 0.92 if f == "tcs" else 0.84, f" {LABEL[f]} stops reporting\n utilization (last: {last.cal_q if 'cal_q' in last else last.year})",
                transform=ax.get_xaxis_transform(), fontsize=6.5, color=INK2, va="top")


ALLQ = [f"{y}Q{n}" for y in range(2007, 2027) for n in range(1, 5)]
ALLY = list(range(2007, 2027))


def plot_panel(ax, d, metric, date_of, period_col, clip):
    """Each series is reindexed to the full period grid so missing periods show as breaks, not bridges."""
    grid = ALLQ if period_col == "cal_q" else ALLY
    xs = [date_of(pd.Series({"cal_q": k, "year": k})) for k in grid]
    wide = d.pivot_table(index=period_col, columns="firm", values=metric, aggfunc="first").reindex(grid)
    tables = []
    for f in INDIAN + PRE_MERGER:
        if f not in wide or wide[f].notna().sum() == 0:
            continue
        y = wide[f].copy()
        keys = pd.Series(grid, index=grid).astype(str)
        keys = keys if period_col == "cal_q" else keys + "Q4"
        if f == "ltim":
            y[keys < "2022Q3"] = np.nan
        if f in PRE_MERGER:
            y[keys >= "2022Q3"] = np.nan
        lab = LABEL[f] if f not in PRE_MERGER else ("LTI / Mindtree (pre-merger)" if f == "lti" else None)
        ax.plot(xs, y.clip(*clip), color=COLOR[f], lw=1.0, alpha=0.85,
                ls="-" if f not in PRE_MERGER else (0, (1, 1.5)), label=lab, zorder=3)
        tables.append(y.rename(metric).rename_axis(period_col).reset_index().dropna().assign(series=LABEL[f]))
    avg = indian_average(d, metric, period_col).reindex(grid)
    ax.plot(xs, avg.simple.clip(*clip), color=INK, lw=2.4, label="Indian average (simple mean)", zorder=5)
    ax.plot(xs, avg.weighted.clip(*clip), color=INK, lw=1.6, ls=(0, (5, 2)), label="Indian average (revenue-weighted)", zorder=5)
    tables.append(avg.simple.rename(metric).rename_axis(period_col).reset_index().dropna().assign(series="Indian average (simple)"))
    tables.append(avg.weighted.rename(metric).rename_axis(period_col).reset_index().dropna().assign(series="Indian average (revenue-weighted)"))
    for f in COMPS:
        if f not in wide or wide[f].notna().sum() == 0:
            continue
        ax.plot(xs, wide[f].clip(*clip), color=COLOR[f], lw=2.0, ls=(0, (3, 1.2)), label=LABEL[f], zorder=4)
        tables.append(wide[f].rename(metric).rename_axis(period_col).reset_index().dropna().assign(series=LABEL[f]))
    return pd.concat(tables, ignore_index=True), avg.dropna(how="all")


def qx(r):
    return qdate(r["cal_q"])


def ax_(r):
    return pd.Timestamp(year=int(r["year"]), month=7, day=1)


weight_check = []
for metric, title, stem in METRICS:
    fig, axes = plt.subplots(2, 1, figsize=(12, 8.6), sharex=True)
    clip = (-40, 60)
    tq, aq = plot_panel(axes[1], df, metric, qx, "cal_q", clip)
    ta, aa = plot_panel(axes[0], ann, metric, ax_, "year", clip)
    for ax, lab in [(axes[0], "annual (calendar year), %"), (axes[1], "quarterly YoY, %")]:
        shade(ax); style(ax, lab)
    if metric in ("du", "resid"):
        util_stop_marks(axes[1], df, qx)
        util_stop_marks(axes[0], ann.assign(cal_q=ann.year.astype(str)), ax_)
    axes[0].set_title("Annual (calendar year)", fontsize=9, loc="left", color=INK)
    axes[1].set_title("Quarterly, year-over-year", fontsize=9, loc="left", color=INK)
    axes[0].set_xlim(pd.Timestamp("2007-06-01"), pd.Timestamp("2026-12-31"))
    h, l = axes[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=6, fontsize=7.5, frameon=False)
    fig.suptitle(f"{title}\nYoY log change ×100. Breaks in lines = periods with no data (most firms: 2012Q3–2015Q1 not collected).\n"
                 f"Values clipped to {clip}. Shading: 2008–09 and COVID (YoY quarters 2020Q2–2021Q2). Source: firm filings, {TAG}.",
                 fontsize=10, color=INK)
    fig.tight_layout(rect=[0, 0.06, 1, 0.92])
    fig.savefig(OUTD / f"{stem}.png", dpi=150)
    plt.close(fig)
    pd.concat([tq.assign(freq="quarterly"), ta.assign(freq="annual")]).to_csv(OUTD / f"plotted_series_{stem}.csv", index=False)
    for freq, a in [("quarterly", aq), ("annual", aa)]:
        dlt = (a.simple - a.weighted)
        post = dlt[[str(i) >= "2023" for i in dlt.index]]
        weight_check.append(dict(metric=metric, freq=freq, mean_abs_diff_all=dlt.abs().mean(), max_abs_diff=dlt.abs().max(),
                                 mean_diff_2023on=post.mean(), n_periods=dlt.notna().sum()))
pd.DataFrame(weight_check).round(2).to_csv(OUTD / "weighting_check.csv", index=False)

# ------------------------------------------------------------------ gap and rolling correlation
avg_q = {m: indian_average(df, m, "cal_q") for m in ["gR", "gL", "gR_usd"]}
avg_a = {m: indian_average(ann, m, "year") for m in ["gR", "gL", "gR_usd"]}
acc_q = df[df.firm == "accenture"].set_index("cal_q")
cog_q = df[df.firm == "cognizant"].set_index("cal_q")
acc_a = ann[ann.firm == "accenture"].set_index("year")

fig, axes = plt.subplots(2, 2, figsize=(13, 7.6), sharex=True)
gap_tab = []
for j, (m, t) in enumerate([("gR", "Revenue growth (cc)"), ("gL", "Headcount growth")]):
    for i, (avg, cmp_, date_of, lab) in enumerate([(avg_a[m], acc_a, lambda k: pd.Timestamp(year=int(k), month=7, day=1), "annual"),
                                                   (avg_q[m], acc_q, qdate, "quarterly")]):
        ax = axes[i, j]
        for col, ls, lw, nm in [("simple", "-", 2.2, "simple mean"), ("weighted", (0, (5, 2)), 1.5, "revenue-weighted")]:
            grid = ALLY if lab == "annual" else ALLQ
            gap = (avg[col] - cmp_[m].reindex(avg.index)).reindex(grid)   # full grid: gaps show as breaks
            ax.plot([date_of(k) for k in grid], gap, color=INK, lw=lw, ls=ls, label=f"Indian average ({nm}) − Accenture")
            gap = gap.dropna()
            gap_tab.append(gap.rename("gap").reset_index().rename(columns={"index": "period", "cal_q": "period", "year": "period"})
                           .assign(metric=m, freq=lab, avg=col))
        shade(ax); style(ax, "percentage points")
        ax.set_title(f"{t}: Indian average − Accenture, {lab}", fontsize=9, loc="left", color=INK)
axes[0, 0].set_xlim(pd.Timestamp("2007-06-01"), pd.Timestamp("2026-12-31"))
h, l = axes[1, 0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=2, fontsize=8, frameon=False)
fig.suptitle(f"Growth gap, Indian firms minus Accenture (YoY log points).\nAccenture quarters end Nov/Feb/May/Aug and are mapped to the calendar quarter containing the quarter end. {TAG}.",
             fontsize=9, color=INK)
fig.tight_layout(rect=[0, 0.05, 1, 0.94])
fig.savefig(OUTD / "07_gap_vs_accenture.png", dpi=150)
plt.close(fig)
pd.concat(gap_tab).to_csv(OUTD / "plotted_series_07_gap_vs_accenture.csv", index=False)

W = 8
fig, axes = plt.subplots(1, 2, figsize=(13, 4.4), sharey=True)
roll_tab = []
for ax, (m, t) in zip(axes, [("gR", "Revenue growth (cc)"), ("gL", "Headcount growth")]):
    for cmp_name, cmp_, color in [("Accenture", acc_q, COLOR["accenture"]), ("Cognizant", cog_q, COLOR["cognizant"])]:
        for col, ls, lw in [("simple", "-", 2.0), ("weighted", (0, (5, 2)), 1.3)]:
            j = pd.concat([avg_q[m][col], cmp_[m]], axis=1, keys=["ind", "cmp"]).sort_index()
            full = pd.Index(sorted(set(j.index)))
            # rolling correlation over 8 consecutive calendar quarters; windows spanning missing quarters are dropped
            r = j.ind.rolling(W, min_periods=W).corr(j.cmp)
            consecutive = pd.Series([(pd.Period(q, "Q") - pd.Period(full[max(k - W + 1, 0)], "Q")).n == W - 1 if k >= W - 1 else False
                                     for k, q in enumerate(full)], index=full)
            r = r[consecutive.reindex(r.index).fillna(False)]
            ax.plot([qdate(q) for q in r.index], r, color=color, lw=lw, ls=ls,
                    label=f"Indian avg ({'simple' if col == 'simple' else 'rev-weighted'}) vs {cmp_name}")
            roll_tab.append(r.rename("corr").reset_index().rename(columns={"index": "cal_q"}).assign(metric=m, comparator=cmp_name, avg=col))
    shade(ax); style(ax, f"{W}-quarter rolling correlation")
    ax.set_ylim(-1.05, 1.05)
    ax.set_title(f"{t}: rolling {W}-quarter correlation (window ends at the plotted quarter)", fontsize=9, loc="left", color=INK)
axes[0].set_xlim(pd.Timestamp("2007-06-01"), pd.Timestamp("2026-12-31"))
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=4, fontsize=7.5, frameon=False)
fig.suptitle(f"Co-movement of Indian average with comparators. {TAG}.", fontsize=10, color=INK)
fig.tight_layout(rect=[0, 0.1, 1, 0.92])
fig.savefig(OUTD / "08_rolling_correlation.png", dpi=150)
plt.close(fig)
pd.concat(roll_tab).to_csv(OUTD / "plotted_series_08_rolling_correlation.csv", index=False)
print("wrote", sorted(p.name for p in OUTD.glob("*.png")))
print(pd.read_csv(OUTD / "weighting_check.csv").to_string())
