"""Chart + compact results table from aggregate CSVs.
Usage: python3 -I make_chart.py PLFS_OUT_DIR"""
import sys, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1]
ROUNDS = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "cy2024", "cy2025"]
LABELS = ["17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-24", "CY24", "CY25"]
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

k = pd.read_csv(os.path.join(D, "key_series_grads_21_30.csv"))
o = pd.read_csv(os.path.join(D, "occupation_split.csv"))
x = np.arange(len(ROUNDS))

plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False})
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), facecolor="#fcfcfb")


def style(ax, title):
    ax.set_facecolor("#fcfcfb")
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_xticks(x); ax.set_xticklabels(LABELS)
    ax.set_title(title, loc="left", color=INK, fontsize=10)
    ax.axvline(7.5, color=INK2, lw=0.8, ls="--")
    ax.text(7.55, ax.get_ylim()[1] * 0.97, "2025 design\nbreak", fontsize=7, color=INK2, va="top")


def series(ax, sub, col, lo, hi, color, label, scale, off):
    sub = sub.set_index("round").reindex(ROUNDS)
    y = sub[col] * scale
    ax.errorbar(x + off, y, yerr=[y - sub[lo] * scale, sub[hi] * scale - y], fmt="-o", color=color,
                lw=2, ms=4, capsize=2, elinewidth=1, label=label)
    return y


ax = axes[0]
for g, c, lab, off in [("nic62_63", BLUE, "NIC 62+63", -0.08), ("it_ites", ORANGE, "IT+ITeS (62+63+822)", 0.08)]:
    series(ax, k[k.series == g], "estimate", "ci90_lo", "ci90_hi", c, lab, 1e-6, off)
ax.set_ylabel("millions"); ax.set_ylim(0, 4)
style(ax, "(b) Employed graduates aged 21-30 in IT\n(usual principal status, 90% CI)")
ax.legend(frameon=False, loc="upper left")

ax = axes[1]
for g, c, lab, off in [("nic62_63", BLUE, "NIC 62+63", -0.08), ("it_ites", ORANGE, "IT+ITeS", 0.08)]:
    series(ax, k[k.series == g], "share", "share_ci90_lo", "share_ci90_hi", c, lab, 100, off)
ax.set_ylabel("% of all employed graduates aged 21-30"); ax.set_ylim(0, 16)
style(ax, "(c) Share of all employed graduates 21-30")
ax.legend(frameon=False, loc="upper left")

ax = axes[2]
for p, c, lab, off in [("all_ages", BLUE, "all ages", -0.08), ("grads_21_30", ORANGE, "graduates 21-30", 0.08)]:
    series(ax, o[o.population == p], "share_outside", "share_ci90_lo", "share_ci90_hi", c, lab, 100, off)
ax.set_ylabel("% of ICT-occupation workers"); ax.set_ylim(0, 40)
ax.axvline(3.5, color=INK2, lw=0.8, ls=":")
ax.text(3.45, 1, "NCO-2004 | NCO-2015", fontsize=7, color=INK2, va="bottom", ha="center")
style(ax, "Step 4: ICT-occupation workers employed\noutside NIC 62-63 (share, 90% CI)")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.62, 1.0))

fig.text(0.01, 0.01, "Source: PLFS unit-level data, first-visit person files; official multipliers. CIs: Taylor linearisation, "
         "FSU clusters within strata. CY24 shares Jan-Jun 2024 records with 2023-24.", fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(os.path.join(D, "plfs_it_young_graduates.png"), dpi=160)

# ---- compact results table ----
rows = []
for r, lab in zip(ROUNDS, LABELS):
    a = k[(k["round"] == r)].set_index("series")
    oo = o[(o["round"] == r) & (o.population == "all_ages")].iloc[0]
    rows.append({
        "round": r,
        "grads21_30_nic62_63_k": round(a.loc["nic62_63", "estimate"] / 1e3),
        "ci90_k": f"{a.loc['nic62_63', 'ci90_lo'] / 1e3:.0f}-{a.loc['nic62_63', 'ci90_hi'] / 1e3:.0f}",
        "n": int(a.loc["nic62_63", "n_unweighted"]),
        "grads21_30_it_ites_k": round(a.loc["it_ites", "estimate"] / 1e3),
        "ci90_k_itites": f"{a.loc['it_ites', 'ci90_lo'] / 1e3:.0f}-{a.loc['it_ites', 'ci90_hi'] / 1e3:.0f}",
        "n_itites": int(a.loc["it_ites", "n_unweighted"]),
        "all_employed_grads21_30_k": round(a.loc["all_employed_grads_21_30", "estimate"] / 1e3),
        "share_nic62_63_pct": round(100 * a.loc["nic62_63", "share"], 1),
        "share_ci90": f"{100 * a.loc['nic62_63', 'share_ci90_lo']:.1f}-{100 * a.loc['nic62_63', 'share_ci90_hi']:.1f}",
        "share_it_ites_pct": round(100 * a.loc["it_ites", "share"], 1),
        "ict_occ_all_ages_k": round(oo.ict_occ_total / 1e3),
        "ict_occ_outside_it_k": round(oo.ict_occ_outside_it / 1e3),
        "share_outside_pct": round(100 * oo.share_outside, 1),
        "share_outside_ci90": f"{100 * oo.share_ci90_lo:.1f}-{100 * oo.share_ci90_hi:.1f}",
        "n_outside": int(oo.n_outside),
        "nco_version": oo.nco_version,
    })
t = pd.DataFrame(rows)
t.to_csv(os.path.join(D, "results_compact.csv"), index=False)
print(t.to_string())
