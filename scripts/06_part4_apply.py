"""Part 4 (ILLUSTRATIVE): likelihood ratios across scenarios for FY2025-27 data (calendar 2024Q2-2026Q2).

y_{m,f,t} = observed YoY metric minus the firm's pre-2023 mean (same window as noise calibration).
Scenario onset: 2023Q1 (headcount peak / start of FY24 slowdown), so 2024Q2 is quarter 6 after onset (t_offset = 5).
Marginal likelihood under each scenario is Gaussian (see sim_model.py); equal prior odds.
Outputs: output/part4_results.csv, output/part4_table.md, figures/fig8_part4.png
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import OUT, FIG
from sim_model import ScenarioModels, SCENARIOS, prior
import importlib
P3 = importlib.import_module("05_part3_simulation")

panel = P3.build_panel()
EXCL = P3.EXCL
METRICS = P3.METRICS


def baseline_means(panel, window=("2015Q2", "2022Q4"), exclude=EXCL, min_obs=8):
    """Firm pre-window mean of each metric; cells with < min_obs quarters are dropped (left missing).
    LTIMindtree (no pre-window data) gets the average of LTI and Mindtree means where both are available."""
    d = panel[(panel.cal_q >= window[0]) & (panel.cal_q <= window[1]) & (~panel.cal_q.isin(exclude))]
    g = d.groupby("firm")[METRICS]
    mu = g.mean().where(g.count() >= min_obs)
    parts = mu.reindex(["lti", "mindtree"])
    mu.loc["ltim"] = parts.mean(skipna=True)
    return mu


def observed(panel, mu, q0="2024Q2", q1="2026Q2", onset="2023Q1", metrics=METRICS):
    qs = sorted(q for q in set(panel.cal_q) if q0 <= q <= q1)
    def qn(q): return int(q[:4]) * 4 + int(q[-1])
    idx, y = [], []
    for m in metrics:
        for f in P3.SIM_FIRMS:
            g = panel[panel.firm == f].set_index("cal_q")
            for q in qs:
                v = g[m].get(q, np.nan) if m in g else np.nan
                b = mu.loc[f, m] if f in mu.index else np.nan
                if pd.notna(v) and pd.notna(b):
                    t0 = qn(q) - qn(q0) + 1
                    idx.append((m, f, t0))
                    y.append(v - b)
    t_offset = qn(q0) - qn(onset)
    return idx, np.array(y), t_offset


def evaluate(spec_kw, cal, mu, metrics=METRICS, onset="2023Q1", noise_scale=1.0, label="", data=None):
    idx, y, toff = observed(panel if data is None else data, mu, onset=onset, metrics=metrics)
    av = {(f, m): True for m in METRICS for f in P3.SIM_FIRMS}
    spec = P3.make_spec(av, cal["tau_h"], cal["tau_b"], t_offset=toff, **spec_kw)
    noise = P3.noise_obj(cal).scaled(noise_scale)
    sm = ScenarioModels(spec, noise, metrics, T=0, idx=idx)
    ll = sm.loglik(y[None, :])
    ll = {s: float(v[0]) for s, v in ll.items()}
    mx = max(ll.values())
    post = {s: np.exp(v - mx) for s, v in ll.items()}
    z = sum(post.values())
    m0, P = prior(spec)
    out = dict(spec=label, n_obs=len(y), t_offset=toff)
    for s in SCENARIOS:
        X = sm.X[s]
        V = X @ P @ X.T + sm.Sigma
        th = m0 + P @ X.T @ np.linalg.solve(V, y - X @ m0)
        out[f"P({s})"] = post[s] / z
        out[f"logL_{s}"] = ll[s]
        out[f"d_hat_{s}"] = th[0]
        out[f"b_hat_{s}"] = th[1]
    out["logBF_S3_vs_S1"] = ll["S3"] - ll["S1"]
    out["logBF_S3_vs_S2"] = ll["S3"] - ll["S2"]
    out["logBF_S1_vs_S4"] = ll["S1"] - ll["S4"]
    return out


if __name__ == "__main__":
    cal = P3.get_noise(panel)
    taus = json.load(open(OUT / "taus.json"))
    cal["tau_h"], cal["tau_b"] = taus["tau_h"], taus["tau_b"]
    cal_pre = P3.get_noise(panel, window=("2015Q2", "2020Q1"), exclude=[], fallback=cal)
    cal_pre["tau_h"], cal_pre["tau_b"] = taus["tau_h_precovid"], taus["tau_b_precovid"]
    mu = baseline_means(panel)
    mu_pre = baseline_means(panel, ("2015Q2", "2020Q1"), [])
    mu.round(2).to_csv(OUT / "part4_baseline_means.csv")

    runs = [
        evaluate({}, cal, mu, label="baseline (all metrics, onset 2023Q1)"),
        evaluate({}, cal, mu, metrics=["gR", "gL"], label="revenue + headcount only"),
        evaluate({}, cal, mu, metrics=["gR", "gL", "du", "gTCV"], label="no service-line contrast"),
        evaluate({}, cal, mu, onset="2024Q2", label="onset 2024Q2"),
        evaluate({}, cal, mu, noise_scale=2.0, label="noise x2"),
        evaluate({"lam_labor": 0.5}, cal, mu, label="labor cut also sluggish"),
        evaluate({"kappa": 0.5}, cal, mu, label="partial pass-through (kappa=0.5)"),
        evaluate({"prior_d_mean": 2.0, "prior_d_sd": 1.0}, cal, mu, label="small effect prior (2±1 %/yr)"),
        evaluate({"tau_b": 4.0}, cal, mu, label="wide common-drift prior (tau_b=4)"),
        evaluate({}, cal_pre, mu_pre, label="pre-COVID baseline & noise"),
    ]
    # AI-exposure classification of service lines (affects only the SLc metric)
    for cls, lab in [("alt_ERD_high", "AI class: ER&D high (HCL dropped)"),
                     ("alt_consulting_high", "AI class: consulting high (ACN/CTSH flipped)"),
                     ("alt_BPS_neutral", "AI class: BPS neutral (TechM dropped)")]:
        pan = P3.build_panel(cls)
        runs.append(evaluate({}, cal, baseline_means(pan), label=lab, data=pan))
    res = pd.DataFrame(runs)
    res.to_csv(OUT / "part4_results.csv", index=False)
    cols = ["spec", "n_obs", "P(S1)", "P(S2)", "P(S3)", "P(S4)", "logBF_S3_vs_S1", "d_hat_S1", "d_hat_S3", "b_hat_S3"]
    res[cols].round(2).to_markdown(OUT / "part4_table.md", index=False)
    print(res[cols].round(2).to_string())

    fig, ax = plt.subplots(figsize=(10, 4.2))
    colors = {"S1": "#1f4e79", "S2": "#2e8b57", "S3": "#c0392b", "S4": "#e39b2d"}
    left = np.zeros(len(res))
    for s in SCENARIOS:
        ax.barh(range(len(res)), res[f"P({s})"], left=left, color=colors[s], label=s)
        left += res[f"P({s})"].values
    ax.set_yticks(range(len(res)))
    ax.set_yticklabels(res.spec, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("posterior probability (equal prior odds)")
    ax.legend(ncol=4, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    ax.set_title("Fig 8. ILLUSTRATIVE: scenario posteriors for FY2025-27 data under alternative modelling choices", fontsize=9.5, pad=24)
    fig.tight_layout()
    fig.savefig(FIG / "fig8_part4.png", dpi=150)
