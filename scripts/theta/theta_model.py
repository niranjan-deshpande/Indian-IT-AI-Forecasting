"""Bottom-up estimate of theta_j(t) and S(t), following theta_model_text.md.

For a task that takes a firm employee h hours, in service line j, with the frontier AI at date t:

    p_METR(h, t) = sigmoid(beta * (ln H50(t) - ln h))
    p_j  = p_METR(m * d_j * h, t)              passes automated checks
    pi_j = q0 * p_METR(m * k * d_j * h, t)     passes and a reviewer accepts
    rho_bar = pi*rho_A + (p - pi)*rho_R + (1 - p)*rho_F,   rho_A(h) = a/h + b,  rho_R = tau*rho_A
    R_bar   = pi*R_A   + (p - pi)*R_R   + (1 - p)*R_F
    Delta   = (1 - kappa) - rho_bar - R_bar*(1 - kappa)
    delegate if omega*h*Delta > c_D(h)
    theta_j = integral of [kappa + delegate*Delta] over the hours-weighted task-length density

d_j is a domain divisor on the horizon (1 for software work; larger for IT ops, BPO and consulting,
where agent horizons are shorter than METR's software horizons). Priors live in priors.py.
"""
import datetime as dt
import math
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
METR_YAML = ROOT / "data" / "explore" / "theta_lit" / "metr_benchmark_results_1_1.yaml"

# log-spaced grid of task lengths in hours: 1 minute to 400 hours
LOG_H = np.linspace(math.log(1 / 60), math.log(400), 360)
H = np.exp(LOG_H)


def year_frac(d):
    d = d if isinstance(d, dt.date) else dt.date.fromisoformat(str(d))
    return d.year + (d.timetuple().tm_yday - 0.5) / 365.25


def frontier_trend(since="2023-01-01"):
    """Least-squares fit of ln H50 (minutes) on date for METR's state-of-the-art models since `since`.

    Returns (anchor_year, ln_H50_at_anchor, fitted_doubling_days, rows); the anchor is the last SOTA release.
    """
    d = yaml.safe_load(open(METR_YAML))
    rows = []
    for name, r in d["results"].items():
        m = r["metrics"]
        # Mythos Preview was never generally released, so firms could not use it
        if m.get("is_sota") and str(r["release_date"]) >= since and "mythos" not in name:
            rows.append((year_frac(r["release_date"]), math.log(m["p50_horizon_length"]["estimate"]), name))
    rows.sort()
    x = np.array([r[0] for r in rows])
    y = np.array([r[1] for r in rows])
    slope, icept = np.polyfit(x, y, 1)
    anchor = x.max()
    return anchor, icept + slope * anchor, 365.25 * math.log(2) / slope, rows


def h50_hours(t_year, trend, doubling_days, correction):
    """Frontier 50% horizon (hours) at date t_year.

    Up to the last METR release this is the measured frontier (best SOTA model released by t_year);
    after it, the fitted trend value at the last release, extrapolated at `doubling_days`.
    """
    anchor, ln_anchor_min, _, rows = trend
    if t_year <= anchor:
        past = [r[1] for r in rows if r[0] <= t_year] or [rows[0][1]]
        return correction * math.exp(max(past)) / 60
    return correction * math.exp(ln_anchor_min) / 60 * 2 ** ((t_year - anchor) * 365.25 / doubling_days)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def hours_weighted_density(median_count_h, sigma):
    """Weights on LOG_H for the hours-weighted version of a count-lognormal(ln median, sigma).

    If task counts are lognormal(mu, sigma), hours are lognormal(mu + sigma^2, sigma).
    Shapes: median, sigma are (N,) -> returns (N, len(LOG_H)) rows summing to 1.
    """
    mu = np.log(median_count_h)[:, None] + sigma[:, None] ** 2
    w = np.exp(-0.5 * ((LOG_H[None, :] - mu) / sigma[:, None]) ** 2)
    return w / w.sum(axis=1, keepdims=True)


def theta_line(P, line, h50):
    """theta_j for one line, vectorised over N parameter draws.

    P: dict of (N,) arrays (global and line-specific draws). h50: (N,) frontier H50 in hours.
    Returns dict with theta, the hours-share delegated, and the delegate-mode saving share.
    """
    g = lambda k: P[k][:, None]
    L = lambda k: P[f"{line}.{k}"][:, None]
    h = H[None, :]
    ln_h50 = np.log(h50)[:, None]
    beta = g("beta")
    d = L("domain_divisor")
    p = sigmoid(beta * (ln_h50 - np.log(g("m") * d * h)))
    pi = g("q0") * sigmoid(beta * (ln_h50 - np.log(g("m") * g("k") * d * h)))
    rho_a = L("review_fixed_h") / h + L("review_prop")
    rho_bar = pi * rho_a + (p - pi) * g("tau") * rho_a + (1 - p) * g("rho_F")
    r_bar = pi * g("R_A") + (p - pi) * g("R_R") + (1 - p) * g("R_F")
    kappa = L("kappa")
    delta = (1 - kappa) - rho_bar - r_bar * (1 - kappa)
    agent_cost = L("agent_cost_per_h") * h ** g("agent_cost_exp")
    delegate = (L("wage") * h * delta > agent_cost) & (delta > 0)
    f = hours_weighted_density(P[f"{line}.median_h"], P[f"{line}.sigma"])
    saving = kappa + delegate * delta
    return {
        "theta": (saving * f).sum(axis=1),
        "delegated_hours_share": (delegate * f).sum(axis=1),
        "accept_rate_hours_weighted": (pi * f).sum(axis=1),
    }
