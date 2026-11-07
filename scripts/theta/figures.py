"""Figures for data/explore/theta_estimate/FINDINGS.md. Run after run_estimate.py.

    python3 scripts/theta/figures.py
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

RES = TM.ROOT / "data" / "explore" / "theta_estimate" / "results"
FIG = TM.ROOT / "data" / "explore" / "theta_estimate" / "figures"
INK, INK2, GRID, BAND = "#0b0b0b", "#52514e", "#e4e3df", "#d9d8d3"
COLOR = dict(maintenance="#2a78d6", development="#eb6834", testing="#1baf7a",
             infrastructure="#eda100", bpo="#e87ba4", consulting="#008300")
NAME = dict(maintenance="Maintenance", development="Development", testing="Testing",
            infrastructure="Infrastructure", bpo="BPO", consulting="Consulting")
plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.fonttype": "none"})


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def fig_path():
    p = pd.read_csv(RES / "theta_path.csv", parse_dates=["month"])
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6), sharey=True)
    ax = axes[0]
    ax.fill_between(p.month, 100 * p.S_p10, 100 * p.S_p90, color=BAND, lw=0, label="10–90% of draws")
    ax.plot(p.month, 100 * p.S_p50, color=INK, lw=2, label="median")
    ax.axvline(pd.Timestamp("2026-11-07"), color=INK2, lw=0.8, ls=":")
    ax.text(pd.Timestamp("2026-11-07"), 1, " now", color=INK2, fontsize=7, va="bottom")
    ax.set_title("Sector ceiling S (share of all labor hours)", loc="left", color=INK, fontsize=9)
    ax.set_ylabel("% of labor hours saved at full adoption")
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    ax = axes[1]
    ends = {}
    for j in PR.LINES:
        ax.plot(p.month, 100 * p[f"{j}_p50"], color=COLOR[j], lw=2)
        ends[j] = 100 * p[f"{j}_p50"].iloc[-1]
    # spread end labels so none sit closer than 2.6 points
    placed = []
    for j in sorted(ends, key=ends.get):
        y = max(ends[j], placed[-1] + 2.6) if placed else ends[j]
        placed.append(y)
        ax.text(p.month.iloc[-1] + pd.Timedelta(days=20), y, NAME[j], color=INK, fontsize=7.5, va="center")
    ax.axvline(pd.Timestamp("2026-11-07"), color=INK2, lw=0.8, ls=":")
    ax.set_title("θ_j by service line (median of draws)", loc="left", color=INK, fontsize=9)
    ax.set_xlim(p.month.iloc[0], p.month.iloc[-1] + pd.Timedelta(days=330))
    for ax in axes:
        style(ax)
        ax.set_ylim(0, None)
    fig.text(0.01, 0.01, "After Apr 2026, METR's frontier is extrapolated at a ~129-day doubling. "
             "Source: scripts/theta/run_estimate.py.", fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIG / "fig1_theta_path.png", dpi=200)


def fig_decomposition():
    s = pd.read_csv(RES / "theta_by_date.csv").set_index("date")
    rows = ["FY26 end (Mar 2026)", "Now (Nov 2026)", "Nov 2027"]
    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.0), sharey=True)
    for ax, row in zip(axes, rows):
        for i, j in enumerate(PR.LINES):
            kappa = 100 * PR_central(j, "kappa")
            total = 100 * s.loc[row, f"{j}_central"]
            ax.barh(i, kappa, color=COLOR[j], height=0.6)
            ax.barh(i, total - kappa, left=kappa, color="white", edgecolor=COLOR[j], hatch="////", height=0.6, lw=0.8)
            ax.text(total + 1, i, f"{total:.0f}%", va="center", fontsize=7, color=INK)
        ax.set_title(row, loc="left", fontsize=9, color=INK)
        ax.set_xlim(0, 70)
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    axes[0].set_yticks(range(len(PR.LINES)), [NAME[j] for j in PR.LINES])
    axes[0].invert_yaxis()
    axes[1].set_xlabel("θ_j at central parameter values, % of the line's hours (solid: assist κ; hatched: extra from delegating)")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_decomposition.png", dpi=200)


def PR_central(line, key):
    kind, *a = PR.PER_LINE[line][key]
    return {"u": lambda: (a[0] + a[1]) / 2, "lu": lambda: (a[0] * a[1]) ** 0.5, "tri": lambda: a[1], "fix": lambda: a[0]}[kind]()


LABEL = {"w0": "non-task share w₀", "m": "context gap m", "k": "reviewer standards k", "R_F": "work left after failed checks R_F",
         "R_R": "work left after rejection R_R", "beta": "METR slope β", "h50_correction": "H50 correction",
         "doubling_days": "doubling time", "q0": "length-independent acceptance q₀", "tau": "rejection review share τ",
         "agent_cost_exp": "agent-cost exponent", "R_A": "work left after acceptance R_A", "rho_F": "review after failed checks ρ_F"}


def label(param):
    if "." in param:
        line, key = param.split(".", 1)
        nice = {"kappa": "assist speedup κ", "agent_cost_per_h": "agent cost per hour", "domain_divisor": "domain horizon divisor",
                "median_h": "median task length", "sigma": "task-length spread σ", "wage": "loaded wage",
                "review_fixed_h": "fixed review time", "review_prop": "proportional review time"}
        return f"{NAME[line]}: {nice.get(key, key)}"
    return LABEL.get(param, param)


def fig_sensitivity():
    s = pd.read_csv(RES / "sensitivity.csv")
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4))
    for ax, d in zip(axes, ["FY26 end (Mar 2026)", "Now (Nov 2026)"]):
        top = s[s.date == d].nlargest(10, "first_order_share").iloc[::-1]
        ax.barh(range(len(top)), 100 * top.first_order_share, color="#2a78d6", height=0.6)
        ax.set_yticks(range(len(top)), [label(x) for x in top.param], fontsize=7)
        ax.set_title(d, loc="left", fontsize=9, color=INK)
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    axes[0].set_xlabel("% of the variance of S explained (first-order)")
    axes[1].set_xlabel("% of the variance of S explained (first-order)")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_sensitivity.png", dpi=200)


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    fig_path()
    fig_decomposition()
    fig_sensitivity()
    print("wrote", *sorted(p.name for p in FIG.glob("*.png")))
