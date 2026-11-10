"""Linear-Gaussian generative model of firm-quarter metrics under scenarios S1-S4.

Identity (all in quarterly log changes, deviations from each firm's pre-2023 baseline):
    R = p * Q                  ->  gR   = pi + q
    L = a * Q / u              ->  gL   = alpha + q - du      (u = utilization)
Headcount adjusts to *surprise* volume changes with partial-adjustment speed lam,
so a surprise drift x in q gives
    gL_t = x * (1 - (1-lam)^t),   du_t = x * (1-lam)^t
while *anticipated* labor-need changes (alpha, S2/S3) pass straight into gL and leave u unchanged.
    gTCV = pi + q              (deal value; noisy)
    gSub = change in subcontracting share (S4 only, not used by default)
    SLc  = revenue growth of high-AI-exposure service lines minus low-exposure lines
           (only for firms with service-line data): S3 -> -kappa * d * dexp, else 0.

Scenario effect d (>0, % per year) enters as:
    S1 demand drop          : q     -= d          (all firms, surprise)
    S2 labor need, p holds  : alpha -= d * e_f    (anticipated), pi = 0
    S3 labor need, p passed : alpha -= d * e_f, pi -= kappa * d * e_f
    S4 work moves (GCC)     : q     -= d * india_f (Indian vendors only, surprise)
Nuisance parameters present under every scenario (integrated out analytically):
    b   : common demand drift (all firms, surprise)          ~ N(0, tau_b^2)
    h_f : firm-specific demand drift                          ~ N(0, tau_h^2)
Noise: per metric AR(1) with coefficient rho_m; innovations = common (across firms) + idiosyncratic,
       cross-metric correlated. Calibrated from pre-2023 residuals (see 04_noise_calibration.py).

Because y is linear in theta = [d, b, h_1..h_F] with Gaussian prior and Gaussian noise,
the marginal likelihood under each scenario is Gaussian: y ~ N(X m, X P X' + Sigma).
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field

SCENARIOS = ["S1", "S2", "S3", "S4"]
METRICS = ["gR", "gL", "du", "gTCV", "SLc"]


@dataclass
class NoiseParams:
    metrics: list                    # metric names, order used in the matrices below
    rho: np.ndarray                  # (M,) AR(1) coefficients
    omega_common: np.ndarray         # (M,M) innovation covariance of the common component
    omega_idio: dict                 # firm -> (M,M) innovation covariance of the idiosyncratic component

    def scaled(self, k: float) -> "NoiseParams":
        """Noise scaled by k in standard deviation (variance by k^2)."""
        return NoiseParams(self.metrics, self.rho.copy(), self.omega_common * k**2,
                           {f: v * k**2 for f, v in self.omega_idio.items()})


@dataclass
class ModelSpec:
    firms: list                      # firm ids
    india: dict                      # firm -> 1 if Indian vendor else 0
    exposure: dict                   # firm -> AI-exposure loading e_f (1 = Indian average)
    avail: dict                      # (firm, metric) -> bool  : metric observed for that firm
    lam: float = 0.5                 # partial adjustment speed of headcount to surprise volume
    lam_labor: float = 1.0           # adjustment speed for anticipated labor-need change (S2/S3)
    kappa: float = 1.0               # price pass-through in S3
    dexp: float = 0.5                # exposure gap between high- and low-AI service lines
    prior_d_mean: float = 4.0        # analyst prior on effect size, % per year
    prior_d_sd: float = 2.0
    tau_b: float = 2.0               # % per year
    tau_h: float = 2.0               # % per year
    per_year: float = 4.0            # quarters per year (drifts are specified per year)
    # --- hypothetical new-data metrics (value-of-information analysis, see voi.py) ---
    eta: float = 0.2                 # cyclical output-price response to a demand drift (S1 and nuisance b)
    omega: float = 0.5               # share of vendors' output-price change visible in an industry price index
    dexp_occ: float = 1.0            # labor-need gap between high- and low-exposure occupations (per unit d)
    zeta: float = 0.0                # S1: demand shock loading on occupation contrast (demand correlated w/ exposure)
    xi: float = 0.0                  # S4: GCC shift loading on occupation contrast
    phi: float = 0.5                 # S4: effect on affiliated share of India's computer-services exports
    window: int = 4                  # observation = change over `window` quarters (4 = YoY)
    t_offset: int = 0                # first observed quarter = onset + 1 + t_offset


def _obs_index(spec: ModelSpec, metrics: list, T: int):
    """List of (metric, firm, t) for observed cells, t = 1..T."""
    idx = []
    for m in metrics:
        for f in spec.firms:
            if spec.avail.get((f, m), False):
                for t in range(1, T + 1):
                    idx.append((m, f, t))
    return idx


def _level_paths(n: int, lam: float):
    """Cumulative log-level responses (t = -8..n) to a unit per-quarter drift starting at t=1.
    target(t) = t for t>=1; actual follows partial adjustment actual_t = actual_{t-1} + lam*(target_t - actual_{t-1})."""
    ts = np.arange(-8, n + 1)
    target = np.clip(ts, 0, None).astype(float)
    actual = np.zeros_like(target)
    for i in range(1, len(ts)):
        actual[i] = actual[i - 1] + lam * (target[i] - actual[i - 1])
    return ts, target, actual, target - actual


def design(spec: ModelSpec, scen: str, idx: list) -> np.ndarray:
    """Design matrix X (n_obs x (2+F)) mapping theta=[d, b, h_1..h_F] (% per year) to observations.
    Observation (m, f, t) is the change in the relevant log level between quarters t-w and t (w = spec.window;
    w=4 -> year-on-year), with t counted from the scenario onset (t=1 is the first affected quarter;
    spec.t_offset shifts the first observed quarter)."""
    F = len(spec.firms)
    fpos = {f: i for i, f in enumerate(spec.firms)}
    X = np.zeros((len(idx), 2 + F))
    qy = 1.0 / spec.per_year
    tmax = max(t for _, _, t in idx) + spec.t_offset + 1 if idx else 1
    ts, tgt, act_s, gap_s = _level_paths(tmax, spec.lam)
    _, _, act_l, gap_l = _level_paths(tmax, spec.lam_labor)
    pos = {t: i for i, t in enumerate(ts)}
    w = spec.window

    def ch(arr, t):  # change over the observation window
        return arr[pos[t]] - arr[pos[t - w]]

    for r, (m, f, t0) in enumerate(idx):
        t = t0 + spec.t_offset
        e = spec.exposure[f]
        ind = spec.india[f]
        if scen == "S1":
            dq, dal, dpi = -1.0, 0.0, 0.0
        elif scen == "S2":
            dq, dal, dpi = 0.0, -e, 0.0
        elif scen == "S3":
            dq, dal, dpi = 0.0, -e, -spec.kappa * e
        elif scen == "S4":
            dq, dal, dpi = -float(ind), 0.0, 0.0
        else:
            raise ValueError(scen)
        if m in ("gR", "gTCV"):
            coef_d = (dpi + dq) * ch(tgt, t)
            coef_n = ch(tgt, t)                      # nuisance demand (surprise q) on revenue
        elif m == "gL":
            coef_d = dal * ch(act_l, t) + dq * ch(act_s, t)
            coef_n = ch(act_s, t)
        elif m == "du":
            coef_d = dal * ch(gap_l, t) + dq * ch(gap_s, t)
            coef_n = ch(gap_s, t)
        elif m == "SLc":
            coef_d = (-spec.kappa * spec.dexp * e if scen == "S3" else 0.0) * ch(tgt, t)
            coef_n = 0.0
        elif m == "gPout":      # industry output-price index (pseudo-firm)
            load = {"S1": -spec.eta, "S2": 0.0, "S3": -spec.kappa * spec.omega * e, "S4": 0.0}[scen]
            coef_d = load * ch(tgt, t)
            coef_n = spec.eta * ch(tgt, t)
        elif m == "OCc":        # occupation contrast in headcount/hiring: high- minus low-exposure occupations
            if scen in ("S2", "S3"):
                coef_d = -spec.dexp_occ * e * ch(act_l, t)
            elif scen == "S1":
                coef_d = -spec.zeta * ch(act_s, t)
            else:
                coef_d = -spec.xi * ind * ch(act_s, t)
            coef_n = 0.0
        elif m == "gAff":       # affiliated share of India's computer-services exports (country pseudo-firm)
            coef_d = (spec.phi if scen == "S4" else 0.0) * ch(tgt, t)
            coef_n = 0.0
        elif m == "gRate":      # revenue per billed hour = p/a
            coef_d = {"S1": 0.0, "S2": e, "S3": (1 - spec.kappa) * e, "S4": 0.0}[scen] * ch(tgt, t)
            coef_n = 0.0
        else:
            raise ValueError(m)
        X[r, 0] = coef_d * qy
        X[r, 1] = coef_n * qy
        if f not in ("industry", "country"):
            X[r, 2 + fpos[f]] = coef_n * qy
    return X


def prior(spec: ModelSpec):
    F = len(spec.firms)
    mean = np.zeros(2 + F)
    mean[0] = spec.prior_d_mean
    var = np.r_[spec.prior_d_sd**2, spec.tau_b**2, np.full(F, spec.tau_h**2)]
    return mean, np.diag(var)


def noise_cov(spec: ModelSpec, noise: NoiseParams, idx: list) -> np.ndarray:
    mpos = {m: i for i, m in enumerate(noise.metrics)}
    n = len(idx)
    S = np.zeros((n, n))
    mi = np.array([mpos[m] for m, _, _ in idx])
    fi = np.array([f for _, f, _ in idx])
    ti = np.array([t for _, _, t in idx])
    rho = noise.rho
    for a in range(n):
        ma, fa, ta = mi[a], fi[a], ti[a]
        mb, fb, tb = mi, fi, ti
        om = noise.omega_common[ma, mb].copy()
        same = fb == fa
        if same.any():
            om[same] += noise.omega_idio[fa][ma, mb[same]]
        ra, rb = rho[ma], rho[mb]
        lag = ta - tb
        fac = np.where(lag >= 0, ra ** np.abs(lag), rb ** np.abs(lag)) / (1 - ra * rb)
        S[a] = om * fac
    return 0.5 * (S + S.T)


class ScenarioModels:
    """Pre-computes marginal means/covariances of y under each scenario for a given metric set and T."""

    def __init__(self, spec: ModelSpec, noise: NoiseParams, metrics: list, T: int, scenarios=SCENARIOS, idx=None):
        self.spec, self.noise, self.metrics, self.T = spec, noise, metrics, T
        self.idx = _obs_index(spec, metrics, T) if idx is None else idx
        self.n = len(self.idx)
        self.scenarios = scenarios
        self.Sigma = noise_cov(spec, noise, self.idx) if self.n else None
        m0, P = prior(spec)
        self.X, self.mu, self.chol, self.logdet = {}, {}, {}, {}
        for s in scenarios:
            X = design(spec, s, self.idx)
            V = X @ P @ X.T + self.Sigma
            L = np.linalg.cholesky(V + 1e-10 * np.eye(self.n))
            self.X[s], self.mu[s], self.chol[s] = X, X @ m0, L
            self.logdet[s] = 2 * np.log(np.diag(L)).sum()

    def loglik(self, Y: np.ndarray) -> dict:
        """Y: (n_draws, n). Returns scenario -> (n_draws,) marginal log-likelihoods."""
        out = {}
        for s in self.scenarios:
            Z = np.linalg.solve(self.chol[s], (Y - self.mu[s]).T)
            out[s] = -0.5 * (Z**2).sum(0) - 0.5 * self.logdet[s] - 0.5 * self.n * np.log(2 * np.pi)
        return out

    def simulate(self, scen: str, d_true: float, n_draws: int, rng: np.random.Generator) -> np.ndarray:
        """Draw y under scenario `scen` with effect size fixed at d_true; nuisances drawn from prior."""
        spec = self.spec
        F = len(spec.firms)
        theta = np.zeros((n_draws, 2 + F))
        theta[:, 0] = d_true
        theta[:, 1] = rng.normal(0, spec.tau_b, n_draws)
        theta[:, 2:] = rng.normal(0, spec.tau_h, (n_draws, F))
        Ls = np.linalg.cholesky(self.Sigma + 1e-12 * np.eye(self.n))
        eps = rng.standard_normal((n_draws, self.n)) @ Ls.T
        return theta @ self.X[scen].T + eps


def detection_table(spec, noise, metric_sets: dict, T_values, d_true, n_draws=2000, seed=0,
                    scenarios=SCENARIOS):
    """For each metric set, T, and ordered scenario pair (truth A vs alternative B):
    expected log BF_{A:B} under A, and pairwise accuracy (mean of P(correct|A) and P(correct|B)).
    Also 4-way classification accuracy (argmax marginal likelihood, equal priors)."""
    rng = np.random.default_rng(seed)
    rows = []
    for name, mets in metric_sets.items():
        for T in T_values:
            sm = ScenarioModels(spec, noise, mets, T, scenarios)
            if sm.n == 0:
                continue
            ll = {}
            for a in scenarios:
                Y = sm.simulate(a, d_true, n_draws, rng)
                ll[a] = sm.loglik(Y)
            # 4-way accuracy
            # ties (observationally identical scenarios for this metric set) are split evenly
            def _acc4(a):
                M = np.vstack([ll[a][s] for s in scenarios])
                best = M.max(0)
                tied = np.isclose(M, best, rtol=0, atol=1e-8)
                return np.mean(tied[scenarios.index(a)] / tied.sum(0))
            acc4 = np.mean([_acc4(a) for a in scenarios])
            for i, a in enumerate(scenarios):
                for b in scenarios[i + 1:]:
                    lbf_a = ll[a][a] - ll[a][b]         # under truth a
                    lbf_b = ll[b][b] - ll[b][a]         # under truth b
                    def _win(x):
                        return np.mean(x > 1e-8) + 0.5 * np.mean(np.abs(x) <= 1e-8)
                    acc = 0.5 * (_win(lbf_a) + _win(lbf_b))
                    rows.append(dict(metric_set=name, T=T, pair=f"{a}-{b}",
                                     E_logBF_true_first=np.mean(lbf_a),
                                     E_logBF_true_second=np.mean(lbf_b),
                                     pair_accuracy=acc, P_strong=0.5 * (np.mean(lbf_a > np.log(10)) +
                                                                         np.mean(lbf_b > np.log(10))),
                                     acc4=acc4, n_obs=sm.n))
    return rows
