"""Monte Carlo estimate of theta_j(t) and S(t), plus sensitivity and the top-down check.

    python3 04_theta_model/scripts/run_estimate.py                # independent priors -> results/
    python3 04_theta_model/scripts/run_estimate.py --correlated   # correlated priors (priors.CORRELATIONS) -> results_correlated/
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import ndtr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import priors as PR  # noqa: E402
import theta_model as TM  # noqa: E402

CORRELATED = "--correlated" in sys.argv
OUT = TM.ROOT / "04_theta_model" / "explore" / "theta_estimate" / ("results_correlated" if CORRELATED else "results")
N = 6000
SEED = 20261107

DATES = {
    "FY24 start (Apr 2023)": "2023-04-01",
    "FY25 start (Apr 2024)": "2024-04-01",
    "FY26 start (Apr 2025)": "2025-04-01",
    "FY26 end (Mar 2026)": "2026-03-31",
    "Last METR point (Apr 2026)": "2026-04-07",
    "Now (Nov 2026)": "2026-11-07",
    "Nov 2027": "2027-11-07",
}


def draw(spec, n, rng, central=False):
    kind, *a = spec
    if kind == "fix":
        return np.full(n, float(a[0]))
    if central:
        v = {"u": lambda: (a[0] + a[1]) / 2, "lu": lambda: math.sqrt(a[0] * a[1]), "tri": lambda: a[1]}[kind]()
        return np.full(n, float(v))
    if kind == "u":
        return rng.uniform(a[0], a[1], n)
    if kind == "lu":
        return np.exp(rng.uniform(math.log(a[0]), math.log(a[1]), n))
    if kind == "tri":
        return rng.triangular(a[0], a[1], a[2], n)
    raise ValueError(kind)


def all_specs():
    specs = dict(PR.GLOBAL)
    specs.update({f"{j}.{k}": v for j in PR.LINES for k, v in PR.PER_LINE[j].items()})
    return specs


def quantile(spec, u):
    """Inverse CDF of a prior at probabilities u."""
    kind, *a = spec
    if kind == "u":
        return a[0] + u * (a[1] - a[0])
    if kind == "lu":
        return np.exp(math.log(a[0]) + u * (math.log(a[1]) - math.log(a[0])))
    if kind == "tri":
        lo, mode, hi = a
        cut = (mode - lo) / (hi - lo)
        return np.where(u < cut, lo + np.sqrt(u * (hi - lo) * (mode - lo)),
                        hi - np.sqrt((1 - u) * (hi - lo) * (hi - mode)))
    raise ValueError(kind)


def correlation_matrix(keys):
    """Pearson correlation of the normal scores implied by PR.CORRELATIONS (Spearman), made positive definite."""
    idx = {k: i for i, k in enumerate(keys)}
    C = np.eye(len(keys))
    for params, rho, _ in PR.CORRELATIONS:
        r = 2 * math.sin(math.pi * rho / 6)  # Spearman -> Pearson for a Gaussian copula
        for a in params:
            for b in params:
                if a != b and a in idx and b in idx:
                    C[idx[a], idx[b]] = r
    vals, vecs = np.linalg.eigh(C)
    if vals.min() < 1e-6:
        print(f"correlation matrix not positive definite (min eigenvalue {vals.min():.3f}); clipping")
        C = vecs @ np.diag(np.clip(vals, 1e-6, None)) @ vecs.T
        d = np.sqrt(np.diag(C))
        C = C / np.outer(d, d)
    return C


def sample(n, central=False, seed=SEED, correlated=None):
    correlated = CORRELATED if correlated is None else correlated
    rng = np.random.default_rng(seed)
    specs = all_specs()
    if central or not correlated:
        return {k: draw(v, n, rng, central) for k, v in specs.items()}
    keys = [k for k, v in specs.items() if v[0] != "fix"]
    L = np.linalg.cholesky(correlation_matrix(keys))
    u = ndtr(rng.standard_normal((n, len(keys))) @ L.T)
    P = {k: quantile(specs[k], u[:, i]) for i, k in enumerate(keys)}
    P.update({k: draw(v, n, rng) for k, v in specs.items() if v[0] == "fix"})
    return P


def line_weights(kind="hours"):
    if kind == "revenue":
        w = dict(PR.REVENUE_WEIGHTS)
    else:
        w = {j: PR.REVENUE_WEIGHTS[j] / PR.BILLING_RATE[j] for j in PR.LINES}
    tot = sum(w.values())
    return {j: v / tot for j, v in w.items()}


def run(P, t_year, trend, weights="hours"):
    h50 = np.array([TM.h50_hours(t_year, trend, dd, c)
                    for dd, c in zip(P["doubling_days"], P["h50_correction"])])
    w = line_weights(weights)
    out = {"h50_hours": h50}
    S = np.zeros_like(h50)
    for line in PR.LINES:
        r = TM.theta_line(P, line, h50)
        for k, v in r.items():
            out[f"{line}.{k}"] = v
        S += w[line] * r["theta"]
    out["S"] = (1 - P["w0"]) * S
    return out


def q(x, ps=(10, 50, 90)):
    return [float(np.percentile(x, p)) for p in ps]


def first_order_share(x, y, bins=20):
    """Binned first-order Sobol index: Var(E[y | x]) / Var(y)."""
    if np.ptp(x) == 0:
        return 0.0
    edges = np.quantile(x, np.linspace(0, 1, bins + 1))
    idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, bins - 1)
    means = np.array([y[idx == b].mean() for b in range(bins)])
    counts = np.array([(idx == b).sum() for b in range(bins)])
    return float(np.sum(counts * (means - y.mean()) ** 2) / counts.sum() / y.var())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    trend = TM.frontier_trend()
    anchor, ln_anchor, dd_fit, rows = trend
    print(f"frontier trend: anchor {anchor:.2f}, H50 {math.exp(ln_anchor)/60:.1f} h, fitted doubling {dd_fit:.0f} days, n={len(rows)}")

    P = sample(N)
    Pc = sample(1, central=True)
    summary = []
    for label, d in DATES.items():
        ty = TM.year_frac(d)
        r, rc = run(P, ty, trend), run(Pc, ty, trend)
        row = {"date": label, "H50_h_central": rc["h50_hours"][0], "S_central": rc["S"][0]}
        row.update(zip(["S_p10", "S_p50", "S_p90"], q(r["S"])))
        for line in PR.LINES:
            row[f"{line}_central"] = rc[f"{line}.theta"][0]
            row[f"{line}_p10"], row[f"{line}_p50"], row[f"{line}_p90"] = q(r[f"{line}.theta"])
            row[f"{line}_deleg_central"] = rc[f"{line}.delegated_hours_share"][0]
        summary.append(row)
    summary = pd.DataFrame(summary)
    summary.to_csv(OUT / "theta_by_date.csv", index=False)
    pd.set_option("display.width", 200)
    cols = ["date", "H50_h_central", "S_central", "S_p10", "S_p50", "S_p90"]
    print(summary[cols].round(3).to_string(index=False))
    print(summary[["date"] + [f"{j}_central" for j in PR.LINES]].round(3).to_string(index=False))
    print(summary[["date"] + [f"{j}_deleg_central" for j in PR.LINES]].round(3).to_string(index=False))

    # monthly path, Apr 2023 to Mar 2028
    path = []
    Pp = sample(2000, seed=SEED + 1)
    for d in pd.date_range("2023-04-01", "2028-03-01", freq="MS"):
        ty = TM.year_frac(d.date())
        r, rc = run(Pp, ty, trend), run(Pc, ty, trend)
        row = {"month": d.date().isoformat(), "H50_h_central": rc["h50_hours"][0], "S_central": rc["S"][0]}
        row.update(zip(["S_p10", "S_p50", "S_p90"], q(r["S"])))
        for line in PR.LINES:
            row[f"{line}_central"] = rc[f"{line}.theta"][0]
            row[f"{line}_p50"] = float(np.median(r[f"{line}.theta"]))
            row[f"{line}_kappa_central"] = Pc[f"{line}.kappa"][0]
        path.append(row)
    pd.DataFrame(path).to_csv(OUT / "theta_path.csv", index=False)

    # top-down check: adoption needed for S(FY26 end) to deliver the realized FY24-26 replacement
    r = run(P, TM.year_frac(DATES["FY26 end (Mar 2026)"]), trend)
    realized = {"central": 0.069, "low": 0.045, "high": 0.108}  # 2.3 pp/yr x 3 (range 1.5-3.6)
    chk = pd.DataFrame({k: q(v / r["S"]) for k, v in realized.items()}, index=["p10", "p50", "p90"])
    chk.to_csv(OUT / "implied_adoption.csv")
    print("adoption needed at FY26 end to match top-down (rows: quantiles over model draws):")
    print(chk.round(2).to_string())

    # bottom-up realized replacement by FY26 end, using disclosed adoption
    # (research/adoption_delegation.md: active use ~22% of headcount at FY26 end, range 15-30%;
    #  developers at roughly twice the firm-wide rate)
    rng = np.random.default_rng(SEED + 2)
    a_all = rng.triangular(0.15, 0.22, 0.30, N)
    w = line_weights()
    flat = (1 - P["w0"]) * sum(w[j] * a_all * r[f"{j}.theta"] for j in PR.LINES)
    soft = {"maintenance", "development", "testing"}
    # same firm-wide headcount share, but software lines at 2x the rate of the others
    share_soft = sum(w[j] for j in soft)
    a_other = a_all / (2 * share_soft + (1 - share_soft))
    tilted = (1 - P["w0"]) * sum(w[j] * (2 * a_other if j in soft else a_other) * r[f"{j}.theta"] for j in PR.LINES)
    bu = pd.DataFrame({"flat adoption": q(flat), "software-tilted adoption": q(tilted)}, index=["p10", "p50", "p90"])
    bu.to_csv(OUT / "bottom_up_realized_fy26.csv")
    print("bottom-up realized replacement by FY26 end (share of labor), vs top-down 0.069 (0.045-0.108):")
    print(bu.round(3).to_string())

    # what-ifs: kappa +0.15 on every line (bottom-up check) and US-like wages (x6) over time
    Pk = {k: v.copy() for k, v in P.items()}
    for j in PR.LINES:
        Pk[f"{j}.kappa"] += 0.15
    rk = run(Pk, TM.year_frac(DATES["FY26 end (Mar 2026)"]), trend)
    flat_k = (1 - Pk["w0"]) * sum(w[j] * a_all * rk[f"{j}.theta"] for j in PR.LINES)
    pd.DataFrame({"kappa +0.15": q(flat_k)}, index=["p10", "p50", "p90"]).to_csv(OUT / "bottom_up_kappa_plus.csv")
    Pu = {k: v.copy() for k, v in Pp.items()}
    for j in PR.LINES:
        Pu[f"{j}.wage"] *= 6
    us = []
    for d in pd.date_range("2023-04-01", "2028-03-01", freq="MS"):
        r = run(Pu, TM.year_frac(d.date()), trend)
        us.append(dict(zip(["month", "S_p10", "S_p50", "S_p90"], [d.date().isoformat(), *q(r["S"])])))
    pd.DataFrame(us).to_csv(OUT / "theta_path_us_wages.csv", index=False)

    # one-at-a-time swings: each prior at its low and high end, everything else central
    swings = []
    for label in ["FY26 end (Mar 2026)", "Now (Nov 2026)"]:
        ty = TM.year_frac(DATES[label])
        base = run(Pc, ty, trend)["S"][0]
        specs = dict(PR.GLOBAL)
        specs.update({f"{j}.{k}": v for j in PR.LINES for k, v in PR.PER_LINE[j].items()})
        for k, (kind, *a) in specs.items():
            if kind == "fix":
                continue
            lo, hi = (a[0], a[-1])
            vals = []
            for v in (lo, hi):
                Px = {kk: vv.copy() for kk, vv in Pc.items()}
                Px[k][:] = v
                vals.append(run(Px, ty, trend)["S"][0])
            swings.append({"date": label, "param": k, "lo": lo, "hi": hi, "S_base": base,
                           "S_at_lo": vals[0], "S_at_hi": vals[1], "swing": abs(vals[1] - vals[0])})
    swings = pd.DataFrame(swings).sort_values(["date", "swing"], ascending=[True, False])
    swings.to_csv(OUT / "swings.csv", index=False)
    print(swings.groupby("date").head(8).round(3).to_string(index=False))

    # sensitivity of S now and at FY26 end
    sens = []
    for label in ["FY26 end (Mar 2026)", "Now (Nov 2026)"]:
        r = run(P, TM.year_frac(DATES[label]), trend)
        for k, v in P.items():
            sens.append({"date": label, "param": k, "first_order_share": first_order_share(v, r["S"]),
                         "spearman": float(pd.Series(v).corr(pd.Series(r["S"]), method="spearman"))})
    sens = pd.DataFrame(sens).sort_values(["date", "first_order_share"], ascending=[True, False])
    sens.to_csv(OUT / "sensitivity.csv", index=False)
    print(sens.groupby("date").head(10).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
