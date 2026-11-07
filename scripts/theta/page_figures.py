"""SVG figures for the Results section of docs/theta-model.html. Run after run_estimate.py.

    python3 scripts/theta/page_figures.py

Colours and fonts follow the page's stylesheet; backgrounds are transparent so the figure panel shows through.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import priors as PR  # noqa: E402
import theta_model as TM  # noqa: E402
from figures import COLOR, NAME, PR_central, label  # noqa: E402

RES = TM.ROOT / "data" / "explore" / "theta_estimate" / "results"
OUT = TM.ROOT / "docs" / "figures" / "theta"
INK, INK2, INK3, RULE, ACCENT, CAT_A = "#2a2318", "#5e5245", "#8a7d6d", "#e6ddd0", "#235fa6", "#b0702a"
NOW = pd.Timestamp("2026-11-07")
plt.rcParams.update({
    "font.family": ["Source Sans 3", "Helvetica", "Arial", "sans-serif"], "font.size": 10,
    "axes.edgecolor": INK3, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none",
    "savefig.transparent": True, "figure.facecolor": "none", "axes.facecolor": "none",
})


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=RULE, lw=0.8)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def ceiling():
    p = pd.read_csv(RES / "theta_path.csv", parse_dates=["month"])
    u = pd.read_csv(RES / "theta_path_us_wages.csv", parse_dates=["month"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), sharey=True, gridspec_kw={"wspace": 0.12})
    ax = axes[0]
    ax.fill_between(p.month, 100 * p.S_p10, 100 * p.S_p90, color=ACCENT, alpha=0.15, lw=0)
    ax.plot(p.month, 100 * p.S_p50, color=ACCENT, lw=2.2)
    ax.plot(u.month, 100 * u.S_p50, color=CAT_A, lw=2, ls=(0, (4, 2)))
    end = p.month.iloc[-1] + pd.Timedelta(days=25)
    ax.text(end, 100 * p.S_p50.iloc[-1], "Indian wages", color=INK, fontsize=9, va="center")
    ax.text(end, 100 * u.S_p50.iloc[-1], "US-like wages", color=INK, fontsize=9, va="center")
    ax.set_title("Whole sector, S", loc="left", color=INK, fontsize=11)
    ax.set_ylabel("% of labor hours saved at full adoption")
    ends, placed = {}, []
    ax = axes[1]
    for j in PR.LINES:
        ax.plot(p.month, 100 * p[f"{j}_p50"], color=COLOR[j], lw=2)
        ends[j] = 100 * p[f"{j}_p50"].iloc[-1]
    for j in sorted(ends, key=ends.get):
        y = max(ends[j], placed[-1] + 3.2) if placed else ends[j]
        placed.append(y)
        ax.text(end, y, NAME[j], color=INK, fontsize=9, va="center")
    ax.set_title("By service line, θⱼ", loc="left", color=INK, fontsize=11)
    for ax in axes:
        grid(ax)
        ax.axvline(NOW, color=INK3, lw=0.9, ls=":")
        ax.text(NOW, 1.5, " now", color=INK2, fontsize=8.5)
        ax.set_ylim(0, 52)
        ax.set_xlim(p.month.iloc[0], p.month.iloc[-1] + pd.Timedelta(days=420))
        ax.set_xticks(pd.to_datetime([f"{y}-01-01" for y in range(2024, 2029)]), [str(y) for y in range(2024, 2029)])
    save(fig, "ceiling")


def decomposition():
    s = pd.read_csv(RES / "theta_by_date.csv").set_index("date")
    rows = [("FY26 end (Mar 2026)", "End of FY26"), ("Now (Nov 2026)", "Now"), ("Nov 2027", "Nov 2027 (extrapolated)")]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.1), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (row, title) in zip(axes, rows):
        for i, j in enumerate(PR.LINES):
            kappa = 100 * PR_central(j, "kappa")
            total = 100 * s.loc[row, f"{j}_central"]
            ax.barh(i, kappa, color=COLOR[j], height=0.62)
            if total - kappa > 0.3:
                ax.barh(i, total - kappa, left=kappa, color="none", edgecolor=COLOR[j], hatch="////", height=0.62, lw=0.9)
            ax.text(total + 1.2, i, f"{total:.0f}%", va="center", fontsize=8.5, color=INK)
        ax.set_title(title, loc="left", fontsize=11, color=INK)
        ax.set_xlim(0, 62)
        grid(ax, "x")
    axes[0].set_yticks(range(len(PR.LINES)), [NAME[j] for j in PR.LINES])
    axes[0].invert_yaxis()
    save(fig, "decomposition")


def topdown():
    bu = pd.read_csv(RES / "bottom_up_realized_fy26.csv", index_col=0)["flat adoption"]
    bk = pd.read_csv(RES / "bottom_up_kappa_plus.csv", index_col=0)["kappa +0.15"]
    rows = [("Top-down, from firm filings", 6.9, 4.5, 10.8, INK),
            ("Model, disclosed adoption", 100 * bu.p50, 100 * bu.p10, 100 * bu.p90, ACCENT),
            ("Model, disclosed adoption, κ + 0.15", 100 * bk.p50, 100 * bk.p10, 100 * bk.p90, CAT_A)]
    fig, ax = plt.subplots(figsize=(7.5, 2.1))
    for i, (name, mid, lo, hi, c) in enumerate(rows):
        ax.plot([lo, hi], [i, i], color=c, lw=6, alpha=0.3, solid_capstyle="round")
        ax.plot(mid, i, "o", color=c, ms=8, mec="white", mew=1.5)
        ax.text(hi + 0.3, i, f"{mid:.1f}", va="center", fontsize=9, color=INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 12.5)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xlabel("labor saved per unit of work, FY24–26 cumulative, %")
    grid(ax, "x")
    save(fig, "topdown")


def swings():
    s = pd.read_csv(RES / "swings.csv")
    s = s[s.date == "Now (Nov 2026)"].nlargest(9, "swing").iloc[::-1]
    base = 100 * s.S_base.iloc[0]
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    for i, r in enumerate(s.itertuples()):
        lo, hi = sorted([100 * r.S_at_lo, 100 * r.S_at_hi])
        ax.barh(i, hi - lo, left=lo, color=ACCENT, height=0.55, alpha=0.85)
    ax.axvline(base, color=INK, lw=1)
    ax.text(base, len(s) - 0.35, f" central {base:.0f}%", fontsize=8.5, color=INK2, va="bottom")
    ax.set_yticks(range(len(s)), [label(x) for x in s.param], fontsize=9)
    ax.set_xlabel("S now, % of labor hours, with one input at the low or high end of its range")
    ax.set_xlim(10, 19)
    grid(ax, "x")
    save(fig, "swings")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ceiling()
    decomposition()
    topdown()
    swings()
    print("wrote", *sorted(p.name for p in OUT.glob("*.svg")))
