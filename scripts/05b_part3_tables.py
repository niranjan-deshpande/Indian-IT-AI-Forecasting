"""Part 3 outputs: key detection table and figures from output/sim_results.csv."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import OUT, FIG

sim = pd.read_csv(OUT / "sim_results.csv")
PAIRS = ["S1-S2", "S1-S3", "S1-S4", "S2-S3", "S2-S4", "S3-S4"]
PAIR_LABEL = {"S1-S2": "S1 demand vs S2 labor-need (p holds)", "S1-S3": "S1 demand vs S3 AI deflation (p falls)",
              "S1-S4": "S1 demand vs S4 work moves (GCC)", "S2-S3": "S2 vs S3 (price pass-through?)",
              "S2-S4": "S2 vs S4", "S3-S4": "S3 vs S4"}
THRESH = 0.8


def t_to(sub, thr=THRESH):
    s = sub.sort_values("T")
    hit = s[s.pair_accuracy >= thr]
    return int(hit["T"].iloc[0]) if len(hit) else None


def fmt_t(t):
    return f"{t}q" if t is not None else "never (≤12q)"


# ---- key table: baseline, per pair and metric set
b = sim[sim.config == "baseline"]
rows = []
for pair in PAIRS:
    for ms, g in b[b.pair == pair].groupby("metric_set"):
        a12 = g[g["T"] == 12].pair_accuracy.iloc[0]
        a4 = g[g["T"] == 4].pair_accuracy.iloc[0]
        lbf = 0.5 * (g[g["T"] == 12].E_logBF_true_first.iloc[0] + g[g["T"] == 12].E_logBF_true_second.iloc[0])
        rows.append(dict(pair=pair, metric_set=ms, acc_T4=a4, acc_T12=a12, E_logBF_T12=lbf,
                         quarters_to_80pct=fmt_t(t_to(g))))
kt = pd.DataFrame(rows)
kt.to_csv(OUT / "key_table_full.csv", index=False)

# compact: columns = metric sets, rows = pairs, cell = "acc@12 (T80)"
order = ["revenue only", "headcount only", "utilization only", "TCV only", "service-line contrast only",
         "revenue + headcount", "rev + heads + util", "rev + heads + util + TCV", "all incl. service-line"]
kt["cell"] = kt.apply(lambda r: f"{r.acc_T12:.2f} ({r.quarters_to_80pct.replace(' (≤12q)', '')})", axis=1)
compact = kt.pivot(index="pair", columns="metric_set", values="cell").reindex(index=PAIRS, columns=order)
compact.index = [PAIR_LABEL[p] for p in compact.index]
compact.to_markdown(OUT / "key_table_compact.md")

# ---- robustness: 'all incl. service-line' and 'rev + heads + util + TCV' across configs
rob = []
for cfg, g0 in sim.groupby("config"):
    for ms in ["revenue + headcount", "rev + heads + util + TCV", "all incl. service-line"]:
        g1 = g0[g0.metric_set == ms]
        for pair in PAIRS:
            g = g1[g1.pair == pair]
            if len(g) == 0:
                continue
            rob.append(dict(config=cfg, metric_set=ms, pair=pair, acc_T12=g[g["T"] == 12].pair_accuracy.iloc[0],
                            T80=t_to(g)))
rob = pd.DataFrame(rob)
rob.to_csv(OUT / "robustness.csv", index=False)
cfg_order = ["baseline", "noise x0.5", "noise x2.0", "effect 2.0%/yr", "effect 6.0%/yr",
             "labor cut also sluggish (lam_labor=0.5)", "partial pass-through (kappa=0.5)",
             "no nuisance drifts (tau=0)", "wide common-drift prior (tau_b=4)",
             "Part-4 timing: observe from quarter 6 after onset", "AR(1) persistence +0.07 (small-sample bias)",
             "pre-COVID calibration"]
rb = rob[rob.metric_set == "all incl. service-line"].copy()
rb["cell"] = rb.apply(lambda r: f"{r.acc_T12:.2f} ({fmt_t(None if pd.isna(r.T80) else int(r.T80)).replace(' (≤12q)', '')})", axis=1)
rbt = rb.pivot(index="config", columns="pair", values="cell").reindex(index=cfg_order, columns=PAIRS)
rbt.to_markdown(OUT / "robustness_compact.md")

# 4-way accuracy
acc4 = b.drop_duplicates(["metric_set", "T"]).pivot(index="metric_set", columns="T", values="acc4").reindex(order)
acc4.round(2).to_csv(OUT / "acc4_baseline.csv")

# ---- Fig 6: accuracy vs T by pair, three metric sets
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
cols = {"S1-S2": "#1f4e79", "S1-S3": "#c0392b", "S1-S4": "#e39b2d", "S2-S3": "#2e8b57", "S2-S4": "#7b3294", "S3-S4": "#888888"}
for ax, ms in zip(axes, ["revenue + headcount", "rev + heads + util + TCV", "all incl. service-line"]):
    for pair in PAIRS:
        g = b[(b.metric_set == ms) & (b.pair == pair)].sort_values("T")
        ax.plot(g["T"], g.pair_accuracy, color=cols[pair], lw=2 if pair == "S1-S3" else 1.3, label=PAIR_LABEL[pair])
    ax.axhline(0.8, color="k", ls=":", lw=0.8)
    ax.axhline(0.5, color="k", lw=0.5)
    ax.set_ylim(0.45, 1.0)
    ax.set_xlabel("quarters observed after onset")
    ax.set_title(ms, fontsize=9)
axes[0].set_ylabel("pairwise classification accuracy")
axes[2].legend(fontsize=6.5, loc="lower right")
fig.suptitle("Fig 6. Detection power (baseline calibration, effect 4%/yr, 8 firms): which scenario pairs separate, and how fast", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FIG / "fig6_detection_power.png", dpi=150)
plt.close(fig)

# ---- Fig 7: robustness of S1-S3 and S2-S3 separation
fig, axes = plt.subplots(1, 2, figsize=(12, 3.8), sharey=True)
for ax, pair in zip(axes, ["S1-S3", "S2-S3"]):
    for cfg in cfg_order:
        g = sim[(sim.config == cfg) & (sim.metric_set == "all incl. service-line") & (sim.pair == pair)].sort_values("T")
        if len(g):
            ax.plot(g["T"], g.pair_accuracy, lw=2.2 if cfg == "baseline" else 1.1,
                    color="k" if cfg == "baseline" else None, label=cfg)
    ax.axhline(0.8, color="k", ls=":", lw=0.8)
    ax.set_title(PAIR_LABEL[pair] + " — all metrics", fontsize=9)
    ax.set_xlabel("quarters observed")
    ax.set_ylim(0.45, 1.0)
axes[0].set_ylabel("pairwise accuracy")
axes[1].legend(fontsize=6.5, loc="lower right")
fig.suptitle("Fig 7. Sensitivity of detection power to noise, effect size and modelling assumptions", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(FIG / "fig7_sensitivity.png", dpi=150)
plt.close(fig)
print(compact.to_string())
print(rbt.to_string())
print(acc4.round(2).to_string())
