"""Part 3: detection-power simulation.

Steps
 1. Build the calibration panel: YoY metrics gR, gL, du, gTCV (from yoy_metrics.csv) and SLc (service-line
    contrast, baseline AI classification, from 03_part2 output).
 2. Calibrate noise on the pre-2023 window (2015Q2-2022Q4) excluding COVID-affected YoY quarters (2020Q2-2021Q2).
    Sensitivity: pre-COVID window only (2015Q2-2020Q1).
 3. tau_h (firm-specific persistent drift) from sub-window changes in firm-relative mean gR;
    tau_b (common drift) from dispersion of cross-firm mean gR across non-overlapping years.
 4. Monte Carlo: for each scenario pair, metric set, T = 1..12 quarters observed, effect size and noise scale:
    expected log Bayes factor and classification accuracy.
Outputs: output/noise_params*.json, output/sim_results.csv, output/key_table.csv/.md, figures/fig6_*.png
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import TIDY, OUT, FIG, LABEL
from noise_calibration import calibrate, tau_h, to_json
from sim_model import ModelSpec, NoiseParams, detection_table, SCENARIOS

EXCL = ["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]
METRICS = ["gR", "gL", "du", "gTCV", "SLc"]
CAL_FIRMS = ["tcs", "infosys", "hcltech", "wipro", "techm", "lti", "mindtree", "cognizant", "accenture"]
SIM_FIRMS = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim", "cognizant", "accenture"]


def build_panel(classification="baseline"):
    y = pd.read_csv(TIDY / "yoy_metrics.csv")
    slc = pd.read_csv(OUT / "cross_section_service_line_contrast.csv")
    slc = slc[slc.classification == classification][["firm", "cal_q", "SLc"]]
    y = y.merge(slc, on=["firm", "cal_q"], how="left")
    y = y[y.firm.isin(CAL_FIRMS + ["ltim"])]
    # LTIMindtree enters only after the calibration window (pre-2023 its 1-3 quarters overlap LTI/Mindtree)
    return y[~((y.firm == "ltim") & (y.cal_q <= "2022Q4"))]


def get_noise(panel, window=("2015Q2", "2022Q4"), exclude=EXCL, fallback=None, min_innov=40):
    firms = [f for f in CAL_FIRMS if f in set(panel.firm)]
    cal = calibrate(panel, METRICS, firms, window=window, exclude=exclude)
    if fallback is not None:   # metrics with too few innovations in this window borrow the main calibration
        for i, m in enumerate(METRICS):
            if cal["n_innov"][m] < min_innov:
                cal["rho"][i] = fallback["rho"][i]
                cal["omega_common"][i, :] = fallback["omega_common"][i, :]
                cal["omega_common"][:, i] = fallback["omega_common"][:, i]
                for f in cal["omega_idio"]:
                    fb = fallback["omega_idio"].get(f, np.median(np.array(list(fallback["omega_idio"].values())), axis=0))
                    cal["omega_idio"][f][i, :] = fb[i, :]
                    cal["omega_idio"][f][:, i] = fb[:, i]
                cal.setdefault("borrowed", []).append(m)
        from noise_calibration import psd
        cal["omega_common"] = psd(cal["omega_common"])
        cal["omega_idio"] = {f: psd(v) for f, v in cal["omega_idio"].items()}
    # The service-line contrast is a within-firm difference: give it no common (cross-firm) component and no
    # common-component correlation with other metrics; its common variance is moved to the idiosyncratic part.
    # (A common SLc component estimated from 3-4 firms was spuriously 0.8-correlated with common revenue shocks
    # in the pre-COVID window and dominated Part 4 results; see DECISIONS.)
    k = METRICS.index("SLc")
    v_c = cal["omega_common"][k, k]
    cal["omega_common"][k, :] = 0.0
    cal["omega_common"][:, k] = 0.0
    for f in cal["omega_idio"]:
        cal["omega_idio"][f][k, k] += v_c
    # LTIMindtree post-merger: average of LTI and Mindtree idiosyncratic noise
    oi = cal["omega_idio"]
    parts = [oi[f] for f in ("lti", "mindtree") if f in oi]
    oi["ltim"] = np.mean(parts, axis=0) if parts else np.median(np.array(list(oi.values())), axis=0)
    for f in SIM_FIRMS:
        if f not in oi:
            oi[f] = np.median(np.array([oi[g] for g in firms]), axis=0)
    return cal


def taus(panel, rho_gR, window_end="2022Q4"):
    th, j = tau_h(panel[panel.firm.isin(CAL_FIRMS)], "gR", ("2015Q2", "2018Q4"), ("2019Q1", window_end), EXCL)
    # correct sampling variance for serial correlation of overlapping YoY obs: n_eff = n (1-rho)/(1+rho)
    if len(j) >= 3:
        k = (1 + rho_gR) / (1 - rho_gR)
        rel = (j.mean2 - j.mean1) - (j.mean2 - j.mean1).mean()
        samp = (j.var1 * k / j.count1 + j.var2 * k / j.count2).mean()
        th = float(np.sqrt(max(rel.var(ddof=1) - samp, 0.0)))
    # tau_b: s.d. across calendar years of cross-firm median Q4 YoY gR, pre-2023 excluding 2020-21
    d = panel[panel.firm.isin(CAL_FIRMS) & panel.cal_q.str.endswith("Q4")]
    d = d[(d.cal_q >= "2015Q4") & (d.cal_q <= window_end) & (~d.cal_q.str[:4].isin(["2020", "2021"]))]
    ann = d.groupby("cal_q").gR.median()
    tb = float(ann.std(ddof=1))
    return th, tb, j, ann


def availability(panel, min_recent=6):
    rec = panel[(panel.cal_q >= "2024Q2") & (panel.cal_q <= "2026Q2")]
    av = {}
    for f in SIM_FIRMS:
        for m in METRICS:
            av[(f, m)] = bool(rec[rec.firm == f][m].notna().sum() >= min_recent)
    return av


def make_spec(av, th, tb, **kw):
    india = {f: int(f not in ("cognizant", "accenture")) for f in SIM_FIRMS}
    expo = {f: (0.7 if f == "accenture" else 1.0) for f in SIM_FIRMS}
    base = dict(lam=0.5, lam_labor=1.0, kappa=1.0, dexp=0.5, prior_d_mean=4.0, prior_d_sd=2.0,
                tau_b=tb, tau_h=th, window=4, t_offset=0)
    base.update(kw)
    return ModelSpec(SIM_FIRMS, india, expo, av, **base)


def noise_obj(cal):
    return NoiseParams(cal["metrics"], np.asarray(cal["rho"]), np.asarray(cal["omega_common"]),
                       {f: np.asarray(v) for f, v in cal["omega_idio"].items()})


METRIC_SETS = {
    "revenue only": ["gR"], "headcount only": ["gL"], "utilization only": ["du"], "TCV only": ["gTCV"],
    "service-line contrast only": ["SLc"],
    "revenue + headcount": ["gR", "gL"], "rev + heads + util": ["gR", "gL", "du"],
    "rev + heads + util + TCV": ["gR", "gL", "du", "gTCV"], "all incl. service-line": METRICS,
}

if __name__ == "__main__":
    panel = build_panel()
    cal = get_noise(panel)
    th_est, tb, j, ann = taus(panel, float(cal["rho"][0]))
    # tau_h is not identified from the data (sampling-corrected estimate ~0; uncorrected s.d. of firm-relative
    # drift changes ~3%/yr). Judgment call: 2%/yr (DECISIONS D5); sensitivity with tau=0 below.
    th = 2.0
    cal["tau_h"], cal["tau_b"] = th, tb
    cal_pre = get_noise(panel, window=("2015Q2", "2020Q1"), exclude=[], fallback=cal)
    _, tb2, _, _ = taus(panel, float(cal_pre["rho"][0]), window_end="2020Q1")
    th2 = th
    to_json(cal, OUT / "noise_params.json")
    to_json(cal_pre, OUT / "noise_params_precovid.json")
    json.dump(dict(tau_h=th, tau_h_estimate_corrected=th_est,
                   tau_h_uncorrected_sd=float(((j.mean2 - j.mean1) - (j.mean2 - j.mean1).mean()).std()), tau_b=tb, tau_h_precovid=th2, tau_b_precovid=tb2,
                   annual_median_gR=ann.round(2).to_dict()), open(OUT / "taus.json", "w"), indent=1)

    # human-readable noise table
    rows = []
    for i, m in enumerate(METRICS):
        idio = [np.sqrt(v[i, i]) for f, v in cal["omega_idio"].items() if f in CAL_FIRMS]
        r = dict(metric=m, rho=cal["rho"][i], sd_common_innov=np.sqrt(cal["omega_common"][i, i]),
                 sd_idio_innov_median=np.median(idio), n_innov=cal["n_innov"][m],
                 rho_precovid=cal_pre["rho"][i], sd_common_precovid=np.sqrt(cal_pre["omega_common"][i, i]),
                 sd_idio_precovid=np.median([np.sqrt(v[i, i]) for f, v in cal_pre["omega_idio"].items() if f in CAL_FIRMS]))
        r["sd_total_stationary"] = np.sqrt((r["sd_common_innov"] ** 2 + r["sd_idio_innov_median"] ** 2) / (1 - r["rho"] ** 2))
        rows.append(r)
    nt = pd.DataFrame(rows)
    nt.to_csv(OUT / "noise_table.csv", index=False)
    print(nt.round(2).to_string())
    print("tau_h", round(th, 2), "tau_b", round(tb, 2), "| precovid", round(th2, 2), round(tb2, 2))
    corr_i = np.median(np.array([v for f, v in cal["omega_idio"].items() if f in CAL_FIRMS]), axis=0)
    dd = np.sqrt(np.diag(corr_i))
    print("median idio innovation corr\n", pd.DataFrame(corr_i / np.outer(dd, dd), index=METRICS, columns=METRICS).round(2))

    av = availability(panel)
    json.dump({f"{k[0]}|{k[1]}": v for k, v in av.items()}, open(OUT / "sim_availability.json", "w"), indent=1)
    print("available:", {m: [f for f in SIM_FIRMS if av[(f, m)]] for m in METRICS})

    noise = noise_obj(cal)
    Ts = list(range(1, 13))
    runs = []
    configs = [("baseline", dict(), 1.0, 4.0)]
    configs += [(f"noise x{k}", dict(), k, 4.0) for k in (0.5, 2.0)]
    configs += [(f"effect {d}%/yr", dict(), 1.0, d) for d in (2.0, 6.0)]
    configs += [("labor cut also sluggish (lam_labor=0.5)", dict(lam_labor=0.5), 1.0, 4.0),
                ("partial pass-through (kappa=0.5)", dict(kappa=0.5), 1.0, 4.0),
                ("no nuisance drifts (tau=0)", dict(tau_b=1e-3, tau_h=1e-3), 1.0, 4.0),
                ("wide common-drift prior (tau_b=4)", dict(tau_b=4.0), 1.0, 4.0),
                ("Part-4 timing: observe from quarter 6 after onset", dict(t_offset=5), 1.0, 4.0),
                ("AR(1) persistence +0.07 (small-sample bias)", dict(), "rho+", 4.0)]
    for name, kw, k, d in configs:
        spec = make_spec(av, th, tb, **kw)
        if k == "rho+":
            nz = NoiseParams(noise.metrics, np.clip(noise.rho + 0.07, None, 0.95), noise.omega_common, noise.omega_idio)
        else:
            nz = noise.scaled(k)
        sets = METRIC_SETS if name == "baseline" else {kk: METRIC_SETS[kk] for kk in
                ["revenue + headcount", "rev + heads + util + TCV", "all incl. service-line"]}
        res = detection_table(spec, nz, sets, Ts, d_true=d, n_draws=2000, seed=1)
        for r in res:
            r["config"] = name
        runs += res
        print("done", name)
    # pre-COVID noise calibration sensitivity
    spec = make_spec(av, th2, tb2)
    res = detection_table(spec, noise_obj(cal_pre), {kk: METRIC_SETS[kk] for kk in
                          ["revenue + headcount", "rev + heads + util + TCV", "all incl. service-line"]}, Ts, 4.0, 2000, 1)
    for r in res:
        r["config"] = "pre-COVID calibration"
    runs += res
    sim = pd.DataFrame(runs)
    sim.to_csv(OUT / "sim_results.csv", index=False)
