"""Value of information: how much would hypothetical new data raise detection power?

Adds candidate series to the calibrated Part 3 model (all current public metrics) and reports pairwise accuracy.
Candidate series (see sim_model.design):
  gRate  revenue per billed hour (= p/a)               per firm      control: should add nothing for S1-S3
  gPout  industry output-price index (price per deliverable)  one series  S3: -kappa*omega*d ; S1: -eta*d (cyclical)
  OCc    occupation contrast (high- minus low-AI-exposure headcount/hiring growth) per firm
         S2/S3: -dexp_occ*d ; S1: -zeta*d ; S4: -xi*d
  gAff   affiliated share of India's computer-services exports, annual, one series   S4: +phi*d
  +firms extra Indian firms with heterogeneous AI exposure (0.6..1.4), same noise as median Indian firm
New-series noise: stationary YoY s.d. sigma (grid), AR(1) rho=0.7, uncorrelated with existing noise (assumption).
Outputs: output/voi_results.csv, output/voi_table.md, figures/fig9_voi.png
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib
from common import OUT, FIG
from sim_model import ModelSpec, NoiseParams, ScenarioModels, SCENARIOS, _obs_index

P3 = importlib.import_module("05_part3_simulation")
BASE_M = P3.METRICS
NEW_M = ["gPout", "OCc", "gAff", "gRate"]
ALL_M = BASE_M + NEW_M
RHO_NEW = 0.7
PAIRS = [("S1", "S3"), ("S1", "S4"), ("S3", "S4"), ("S1", "S2"), ("S2", "S3")]


def base_noise():
    panel = P3.build_panel()
    cal = P3.get_noise(panel)
    taus = json.load(open(OUT / "taus.json"))
    return cal, taus["tau_h"], taus["tau_b"], P3.availability(panel)


def extend_noise(cal, firms, sig):
    """sig: dict metric -> stationary s.d. for new metrics."""
    M0 = len(BASE_M)
    M = len(ALL_M)
    rho = np.r_[np.asarray(cal["rho"]), np.full(len(NEW_M), RHO_NEW)]
    oc = np.zeros((M, M))
    oc[:M0, :M0] = cal["omega_common"]
    med = np.median(np.array([cal["omega_idio"][f] for f in P3.SIM_FIRMS if f not in ("cognizant", "accenture")]), axis=0)
    oi = {}
    for f in firms:
        O = np.zeros((M, M))
        O[:M0, :M0] = cal["omega_idio"].get(f, med)
        for j, m in enumerate(NEW_M):
            s = sig.get(m, 1.0)
            if isinstance(s, dict):          # per-firm noise (measured); firms not listed get the median
                s = s.get(f, float(np.median(list(s.values()))))
            O[M0 + j, M0 + j] = s ** 2 * (1 - RHO_NEW ** 2)
        if f in ("industry", "country"):
            O[:M0, :M0] = np.eye(M0) * 1.0   # pseudo-firms carry no base metrics; placeholder variance
        oi[f] = O
    return NoiseParams(ALL_M, rho, oc, oi)


def make(av_base, th, tb, add, n_extra_firms=0, occ_firms=None, **kw):
    firms = list(P3.SIM_FIRMS)
    extra = [f"hyp{i + 1}" for i in range(n_extra_firms)]
    firms += extra + ["industry", "country"]
    india = {f: int(f not in ("cognizant", "accenture", "industry", "country")) for f in firms}
    expo = {f: (0.7 if f == "accenture" else 1.0) for f in firms}
    for i, f in enumerate(extra):
        expo[f] = 0.6 + 0.8 * i / max(n_extra_firms - 1, 1)
    av = {k: v for k, v in av_base.items()}
    for f in extra:
        for m in ["gR", "gL", "du", "gTCV"]:
            av[(f, m)] = True
        av[(f, "SLc")] = (int(f[3:]) % 2 == 0)
    if "gRate" in add:
        for f in P3.SIM_FIRMS:
            av[(f, "gRate")] = True
    if "OCc" in add:
        for f in (occ_firms or P3.SIM_FIRMS):
            av[(f, "OCc")] = True
    if "gPout" in add:
        av[("industry", "gPout")] = True
    if "gAff" in add:
        av[("country", "gAff")] = True
    base = dict(lam=0.5, lam_labor=1.0, kappa=1.0, dexp=0.5, prior_d_mean=4.0, prior_d_sd=2.0,
                tau_b=tb, tau_h=th, window=4, t_offset=5)
    base.update(kw)
    return ModelSpec(firms, india, expo, av, **base), firms


def accuracy(spec, noise, metrics, T, n_draws=1500, seed=3):
    idx = _obs_index(spec, metrics, T)
    # annual-only observation for the trade series (published once a year)
    idx = [(m, f, t) for (m, f, t) in idx if not (m == "gAff" and (t + spec.t_offset) % 4 != 0)]
    sm = ScenarioModels(spec, noise, metrics, T, SCENARIOS, idx=idx)
    rng = np.random.default_rng(seed)
    ll = {a: sm.loglik(sm.simulate(a, 4.0, n_draws, rng)) for a in SCENARIOS}
    out = {}
    for a, b in PAIRS:
        la, lb = ll[a][a] - ll[a][b], ll[b][b] - ll[b][a]
        win = lambda x: np.mean(x > 1e-8) + 0.5 * np.mean(np.abs(x) <= 1e-8)
        out[f"{a}-{b}"] = 0.5 * (win(la) + win(lb))
    return out, sm.n


if __name__ == "__main__":
    cal, th, tb, av = base_noise()
    rows = []

    def run(label, add=(), sig=None, n_extra=0, occ_firms=None, T=12, t_offset=5, **kw):
        spec, firms = make(av, th, tb, add, n_extra, occ_firms, t_offset=t_offset, **kw)
        noise = extend_noise(cal, firms, sig or {})
        acc, n = accuracy(spec, noise, BASE_M + list(add), T)
        rows.append(dict(label=label, T=T, t_offset=t_offset, n_obs=n, **acc))
        print(label, T, t_offset, {k: round(v, 2) for k, v in acc.items()})

    for toff in (5, 0):
        run("current public data (baseline)", t_offset=toff)
        run("+ hourly rate p/a (control), sd 1", ("gRate",), {"gRate": 1.0}, t_offset=toff)
        for s in (0.5, 1, 2, 4):
            run(f"+ output-price index, sd {s}", ("gPout",), {"gPout": s}, t_offset=toff)
        run("+ output-price index, sd 1, cyclical eta=0.5", ("gPout",), {"gPout": 1.0}, t_offset=toff, eta=0.5)
        run("+ output-price index, sd 1, visibility omega=0.25", ("gPout",), {"gPout": 1.0}, t_offset=toff, omega=0.25)
        for s in (2, 4, 8, 16):
            run(f"+ occupation contrast (8 firms), sd {s}", ("OCc",), {"OCc": s}, t_offset=toff)
        run("+ occupation contrast sd 4, demand confound zeta=0.3", ("OCc",), {"OCc": 4}, t_offset=toff, zeta=0.3)
        run("+ occupation contrast sd 4, GCC confound xi=0.5", ("OCc",), {"OCc": 4}, t_offset=toff, xi=0.5)
        for s in (2, 5, 10):
            run(f"+ affiliated trade share (annual), sd {s}", ("gAff",), {"gAff": s}, t_offset=toff)
        for m in (4, 8):
            run(f"+ {m} more Indian firms (exposure 0.6-1.4)", n_extra=m, t_offset=toff)
        run("combined: price sd 2 + occupation sd 8 + trade sd 5", ("gPout", "OCc", "gAff"),
            {"gPout": 2, "OCc": 8, "gAff": 5}, t_offset=toff)
    for T in (4, 8):
        run("current public data (baseline)", T=T)
        run(f"+ occupation contrast (8 firms), sd 8", ("OCc",), {"OCc": 8}, T=T)
        run(f"+ output-price index, sd 2", ("gPout",), {"gPout": 2}, T=T)
    # measured LCA occupation-contrast noise (Eloundou GPT-4 terciles, trailing-4q YoY, per firm; data/explore/lca)
    lca = pd.read_csv(OUT.parent / "data/explore/lca/lca_noise_stats_cases.csv")
    lca = lca[(lca.series == "contrast_gpt4") & (~lca.firm.str.startswith("pooled"))]
    meas = dict(zip(lca.firm, lca.sd_resid))
    run("+ LCA occupation contrast, MEASURED per-firm noise", ("OCc",), {"OCc": meas})
    run("+ LCA occupation contrast, measured noise, attenuation 0.3 (validation r)", ("OCc",), {"OCc": meas},
        dexp_occ=0.3)
    run("+ LCA occupation contrast, 2 best-coded firms only (HCL, TechM)", ("OCc",), {"OCc": meas},
        occ_firms=["hcltech", "techm"])
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "voi_results.csv", index=False)
    t12 = res[(res["T"] == 12)]
    tab = t12.pivot_table(index="label", columns="t_offset", values=["S1-S3", "S1-S4", "S3-S4"], sort=False).round(2)
    tab.to_markdown(OUT / "voi_table.md")
    print(tab.to_string())
