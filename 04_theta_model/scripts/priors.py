"""Priors for the theta_j model. Each entry is (distribution, *args):

    ("u", lo, hi)        uniform              central = midpoint
    ("lu", lo, hi)       log-uniform          central = geometric midpoint
    ("tri", lo, mode, hi) triangular          central = mode
    ("fix", v)           fixed

Sources are in 04_theta_model/theta_j_literature.md and 04_theta_model/explore/theta_estimate/research/*.md.
"""

LINES = ["maintenance", "development", "testing", "infrastructure", "bpo", "consulting"]

# Hours weights of the six lines among task hours (sum to 1); multiplied by (1 - w0) in the model.
# Revenue shares: mean of the latest service-line splits of Infosys (Q4 FY18), TCS (FY17), Wipro (Q3 FY21)
# and HCLTech (Q4 FY19) in data/tidy/panel_long.csv, mapped to the six lines (ADM split 55/45 between
# maintenance and development, Wipro/HCL "applications" split 45/40/15 maintenance/development/testing,
# ER&D and engineering counted as development). Hours shares divide by an assumed relative billing rate
# (consulting 1.4, development 1.0, maintenance 0.95, testing 0.85, infrastructure 0.9, BPO 0.5).
REVENUE_WEIGHTS = dict(maintenance=0.181, development=0.280, testing=0.078, infrastructure=0.227, bpo=0.095, consulting=0.139)
BILLING_RATE = dict(maintenance=0.95, development=1.0, testing=0.85, infrastructure=0.9, bpo=0.5, consulting=1.4)

GLOBAL = {
    # capability curve (METR Time Horizon 1.1)
    "beta": ("u", 0.6, 1.0),                 # slope per natural-log unit; recent models 0.6-1.0
    "doubling_days": ("tri", 104, 129, 158),  # 95% CI and point estimate since 2023
    "h50_correction": ("u", 0.5, 1.0),        # Barry (METR 2026): alternative fits and private tasks cut H50 up to ~40%
    # translating METR to firm work
    "m": ("lu", 1, 10),                       # context gap: METR contractor hours per firm-employee hour (prior 1-18)
    "k": ("lu", 2, 10),                       # reviewer standards as a horizon shift (Whitfill et al. one-shot ~7)
    "q0": ("u", 0.85, 1.0),                   # length-independent acceptance
    # outcome table
    "tau": ("u", 0.3, 1.0),                   # review time on rejected vs accepted output
    "rho_F": ("u", 0.0, 0.05),                # review time when checks fail
    "R_A": ("u", 0.0, 0.15),                  # work left after acceptance
    "R_R": ("u", 0.33, 1.0),                  # work left after a reviewer rejects (Rein: ~1/3-1/2)
    "R_F": ("u", 0.8, 1.1),                   # work left after failing checks
    # inference cost: c_D(h) = agent_cost_per_h (per line) * h ** agent_cost_exp dollars per attempt
    "agent_cost_exp": ("u", 0.9, 1.2),        # roughly linear in h (Redwood, MirrorCode, Ord)
    # non-task time (bench, training, sales, coordination), theta_0 = 0
    "w0": ("u", 0.15, 0.35),
}

# Line-specific priors. median_h and sigma describe the COUNT-weighted lognormal of task touch time
# (04_theta_model/explore/theta_estimate/research/f_j_task_lengths.md). The task unit should match one autonomous AI run.
PER_LINE = {
    "maintenance": dict(
        median_h=("lu", 0.5, 2), sigma=("tri", 1.1, 1.35, 1.6),     # Jira worklogs (SiP, MariaDB, Atlassian, Red Hat), MetricNet
        domain_divisor=("fix", 1), kappa=("u", 0.10, 0.30), agent_cost_per_h=("lu", 0.7, 10),
        review_fixed_h=("u", 0.03, 0.25), review_prop=("u", 0.05, 0.25), wage=("lu", 8, 17)),
    "development": dict(
        median_h=("lu", 4, 16), sigma=("tri", 1.3, 1.5, 1.8),       # SiP enhancements, Rubin stories, MariaDB/Red Hat tasks
        domain_divisor=("fix", 1), kappa=("u", 0.15, 0.30), agent_cost_per_h=("lu", 0.7, 10),
        review_fixed_h=("u", 0.03, 0.25), review_prop=("u", 0.05, 0.25), wage=("lu", 8, 17)),
    "testing": dict(
        median_h=("lu", 0.25, 1), sigma=("tri", 1.0, 1.3, 1.6),     # per-test-case benchmarks (QA Wolf, Inflectra); low confidence
        domain_divisor=("fix", 1), kappa=("u", 0.15, 0.35), agent_cost_per_h=("lu", 0.7, 10),
        review_fixed_h=("u", 0.03, 0.25), review_prop=("u", 0.05, 0.25), wage=("lu", 7, 14)),
    "infrastructure": dict(
        median_h=("lu", 0.25, 1), sigma=("tri", 1.0, 1.2, 1.5),     # MetricNet incident/request work time, SOC alert survey
        domain_divisor=("lu", 3, 40), kappa=("u", 0.05, 0.20),   # ITBench-AA; assumes 0.5-2 h incidents
        agent_cost_per_h=("lu", 1, 20),
        review_fixed_h=("u", 0.05, 0.3), review_prop=("u", 0.1, 0.3), wage=("lu", 7, 14)),
    "bpo": dict(
        median_h=("lu", 0.08, 0.3), sigma=("tri", 0.95, 1.1, 1.4),  # MetricNet AHT, Brown et al. call data, APQC invoices
        domain_divisor=("lu", 10, 100), kappa=("u", 0.04, 0.15),  # support /10-/50 (tau-bench), back office /30 (OSWorld 2.0, RLI)
        agent_cost_per_h=("lu", 1, 30),                          # chat cheap; computer use ~$15/human-hour
        review_fixed_h=("u", 0.0, 0.05), review_prop=("u", 0.03, 0.25), wage=("lu", 2.5, 5)),
    "consulting": dict(
        median_h=("lu", 4, 20), sigma=("tri", 1.2, 1.5, 1.8),       # SiP spec tasks, QSM ERP sizing; largely a guess
        domain_divisor=("lu", 2, 20), kappa=("u", 0.10, 0.30),   # no direct evidence
        agent_cost_per_h=("lu", 2, 30),
        review_fixed_h=("u", 0.1, 0.5), review_prop=("u", 0.15, 0.4), wage=("lu", 12, 30)),
}

# Rank (Spearman) correlations between priors, for the correlated draw (run_estimate.py --correlated).
# These describe shared *uncertainty*: if we are wrong about one input, we are likely wrong about the others
# in the same direction. Each entry: (parameters, rho, reason). A group means every pair within it.
SOFTWARE = ["maintenance", "development", "testing"]
CORRELATIONS = [
    ([f"{j}.kappa" for j in LINES], 0.7, "one unknown: how much current tools help, versus 2022-24 studies"),
    ([f"{j}.agent_cost_per_h" for j in LINES], 0.8, "same models and prices on every line"),
    ([f"{j}.wage" for j in LINES], 0.8, "same labor market and the same filings-based conversion"),
    ([f"{j}.review_fixed_h" for j in LINES], 0.6, "same review practice and the same thin evidence"),
    ([f"{j}.review_prop" for j in LINES], 0.6, "same review practice and the same thin evidence"),
    ([f"{j}.median_h" for j in LINES], 0.4, "one choice of task granularity applies to every line"),
    (["infrastructure.domain_divisor", "bpo.domain_divisor", "consulting.domain_divisor"], 0.5,
     "one unknown: how far agents trail coding outside software"),
    (["R_R", "R_F"], 0.5, "one unknown: how reusable a failed attempt is"),
    (["m", "k"], 0.3, "both measure how much harder firm work is than METR's tasks"),
    (["beta", "h50_correction"], -0.5, "Barry (METR 2026): fits that cut H50 raise H80, i.e. a steeper slope"),
] + [(["m", f"{j}.kappa"], -0.3, "high-context staff gain less from assistance (METR 2025 RCT)") for j in SOFTWARE]
