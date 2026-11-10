"""Build docs/delegable-share.html from delegable_share/page_text.md and the run CSVs.

    python3 delegable_share/scripts/build_page.py [pilot_run] [bpo_run]      e.g. pilot_v4c bpo_v1

pilot_run defaults to pilot_v4c. If bpo_run is given and coding/stage2/<bpo_run>/delegable/items.csv
exists, the "::: if-bpo" blocks of page_text.md are shown with the BPO charts and table; otherwise the
"::: if-no-bpo" blocks are shown instead (the "in progress" note).

Inputs (all read, never written):
  coding/stage2/<run>/delegable/items.csv   per item, every scenario (delegable.py)
  coding/stage2/<run>/features.csv          coded lengths, review lines, kappa, context
  coding/stage2/<run>/matches_final.csv     benchmark match and its rating
  benchmarks/horizons.csv                   horizons per benchmark (horizons.py)
  coding/bench_times/validation/estimates.csv   blind time estimates vs published times
  data/pilot_tasks.csv                      for the count of rated pilot statements
Model settings (beta, q, lambda, m levels) are imported from scripts/delegable.py so the page and the
numbers cannot drift apart.

Text conventions (page_text.md): as in 03_health_check/health_check_text.md, plus
  {{token}}             a number computed here (see tokens()); the build fails on an unknown token
  $...$, $$...$$        math, rendered by KaTeX
  ::: gentable NAME     a table generated here; caption lines, then optional "---" and a note line
  ::: if-bpo / ::: if-no-bpo   shown only when the BPO run is present / absent
The page reuses the stylesheet and chart/footnote/contents scripts of
03_health_check/scripts/health_check_template.html, so the tabs stay in step.
"""
import html
import json
import math
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.dont_write_bytecode = True  # leave no .pyc behind for the imported helpers
HERE = Path(__file__).resolve().parent
DS = HERE.parent
REPO = DS.parent
sys.path.insert(0, str(REPO / "01_pilot" / "scripts" / "note"))  # shared helpers, as the other builders
sys.path.insert(0, str(HERE))
from build_note import REPO_URL, inline, pipe_table  # noqa: E402
import delegable as DL  # noqa: E402  (model settings only; nothing is recomputed)

OUT = REPO / "docs" / "delegable-share.html"
TEXT = DS / "page_text.md"
TEMPLATE = REPO / "03_health_check" / "scripts" / "health_check_template.html"
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"
CRUMBS = ('<a href="index.html">Pilot note</a> · <a href="two-questions.html">Two questions (working draft)</a> · '
          '<a href="health-check.html">Health check</a> · <a href="theta-model.html">Estimating θ (working draft)</a> · '
          '<b>Delegable share</b>')

BASE, RHO5 = "base", "base, rho 0.5 (tests/state)"
SCEN_LABEL = {  # long label, short label (narrow screens)
    "base": ("Baseline: ρ = 1, aligned to today", "Baseline"),
    "base, rho 0.5 (tests/state)": ("ρ = 0.5 for test- and state-graded benchmarks", "ρ = 0.5"),
    "latest observed H (no date alignment)": ("No date alignment (latest observed horizons)", "No alignment"),
    "decompressed spread, both sides": ("Spread of times widened, both sides", "Widen, both"),
    "decompressed spread, benchmarks only": ("Spread of times widened, benchmark items only", "Widen, bench."),
    "beta 0.6": ("Slope β = 0.6 (baseline 0.84)", "β = 0.6"),
    "beta 1.0": ("Slope β = 1.0", "β = 1.0"),
    "lambda 0.25": ("Failure cost λ = 0.25 (live items)", "λ = 0.25"),
    "lambda 3": ("Failure cost λ = 3 (live items)", "λ = 3"),
    "fill from 2nd match": ("Uncovered items take their second match", "2nd match"),
    "+12 months (pooled trend)": ("One year ahead (pooled trend)", "+12 months"),
}
SHORT_OCC = {
    # more_v1 (second wave)
    "Information Security Analysts": "Info security analysts",
    "Payroll and Timekeeping Clerks": "Payroll clerks",
    "Bill and Account Collectors": "Bill collectors",
    "General and Operations Managers": "General managers",
    "Project Management Specialists": "Project managers",
    "Elementary School Teachers, Except Special Education": "Primary teachers",
    "Police and Sheriff's Patrol Officers": "Police officers",
    "Computer and Information Systems Managers": "IT managers",
    "Medical and Health Services Managers": "Health services managers",
    "Training and Development Specialists": "Training specialists",
    "Operations Research Analysts": "Operations researchers",
    "Child, Family, and School Social Workers": "Social workers",
    "Public Relations Specialists": "PR specialists",
    "Licensed Practical and Licensed Vocational Nurses": "Practical nurses",
    "Fast Food and Counter Workers": "Fast food workers",
    "Landscaping and Groundskeeping Workers": "Groundskeepers",
    "First-Line Supervisors of Retail Sales Workers": "Retail supervisors",
    "Shipping, Receiving, and Inventory Clerks": "Shipping clerks",
    "Medical Secretaries and Administrative Assistants": "Medical secretaries",
    "First-Line Supervisors of Office and Administrative Support Workers": "Office supervisors",
    "Maintenance and Repair Workers, General": "Maintenance workers",
    "Laborers and Freight, Stock, and Material Movers, Hand": "Hand movers",
    "Interpreters and Translators": "Translators",
    "Proofreaders and Copy Markers": "Proofreaders",
    "Technical Writers": "Technical writers",
    "Paralegals and Legal Assistants": "Paralegals",
    "Tax Preparers": "Tax preparers",
    "Electricians": "Electricians",
    "Registered Nurses": "Registered nurses",
    "Childcare Workers": "Childcare workers",
    "Janitors and Cleaners, Except Maids and Housekeeping Cleaners": "Janitors",
    "Heavy and Tractor-Trailer Truck Drivers": "Truck drivers",
    "Accountants and Auditors": "Accountants",
    "Lawyers": "Lawyers",
    "Credit Analysts": "Credit analysts",
    "Secondary School Teachers, Except Special and Career/Technical Education": "Secondary teachers",
    "Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products": "Wholesale sales reps",
    "Management Analysts": "Management analysts",
    "Computer User Support Specialists": "User support",
    "Customer Service Representatives": "Customer service",
    "Software Quality Assurance Analysts and Testers": "Software QA",
    "Software Developers": "Software developers",
    "Web Developers": "Web developers",
    "Network and Computer Systems Administrators": "Network/systems admins",
    "Database Administrators": "Database admins",
    "Computer Systems Analysts": "Systems analysts",
    "Bookkeeping, Accounting, and Auditing Clerks": "Bookkeeping clerks",
    "Billing and Posting Clerks": "Billing clerks",
    "Data Entry Keyers": "Data entry keyers",
    "Insurance Claims and Policy Processing Clerks": "Insurance claims clerks",
    "Medical Records Specialists": "Medical records",
}
OCC_KEY = {"Computer User Support Specialists": "us", "Customer Service Representatives": "cs",
           "Software Quality Assurance Analysts and Testers": "qa"}
BENCH = {
    "crmarena_pro": "CRMArena-Pro", "eva_bench": "EVA-Bench", "finch": "Finch", "gdpval": "GDPval",
    "itbench_sre": "ITBench SRE", "osworld_verified": "OSWorld-Verified", "sopbench": "SOPBench",
    "spreadsheetbench_2": "SpreadsheetBench 2", "starshell": "StarShell", "swe_bench_pro": "SWE-bench Pro",
    "sweeper_bench": "SWEeper-Bench", "swt_bench": "SWT-bench Verified", "tau_banking": "τ-bench banking",
    "tau_retail_airline": "τ-bench retail/airline", "tau_telecom": "τ-bench telecom", "tau_voice": "τ-Voice",
    "terminal_bench_1": "Terminal-Bench 1", "terminal_bench_2": "Terminal-Bench 2", "workarena_l1": "WorkArena L1",
    "workarena_pp": "WorkArena++", "scuba": "SCUBA", "theagentcompany": "TheAgentCompany",
}
TYPES = ["DISCRETE", "LIVE_SERVICE", "INTERPERSONAL", "PHYSICAL", "NO_DELIVERABLE"]
CODED = ("DISCRETE", "LIVE_SERVICE")
EXAMPLES = ["1282b", "14662a"]  # worked examples on the page: a ticket reply, a QA evaluation
MONTHS = ("January February March April May June July August September October November December").split()


TODAY = "2026-11-10"


BENCH.update({"apex_accounting": "APEX-Accounting", "dualentry": "DualEntry", "vals_finance_agent": "Vals Finance Agent",
              "healthadminbench": "HealthAdminBench", "ui_cube": "UI-CUBE", "theagentcompany": "TheAgentCompany",
              "swe_lancer": "SWE-Lancer", "spider2": "Spider 2.0", "terminal_bench_4": "Terminal-Bench 4",
              "dba_bench": "DBA-Bench", "swe_bench_verified": "SWE-bench Verified", "jobbench": "JobBench",
              "apex_agents": "APEX-Agents", "online_mind2web": "Online-Mind2Web", "officeval": "OfficeVal",
              "osworld_2": "OSWorld 2.0"})

def bname(b):
    b = str(b).replace(" (no horizon)", "")
    return BENCH.get(b, b)


def occ_short(o):
    return SHORT_OCC.get(o, o)


def pct(x, nd=0):
    return f"{100 * x:.{nd}f}%"


def dur(minutes):
    m = float(minutes)
    if m < 100:
        return f"{m:.0f} minutes"
    h = m / 60
    if h < 10:
        return f"{h:.1f}".rstrip("0").rstrip(".") + " hours"
    return f"{h:,.0f} hours"


def month(date):
    y, mo = str(date).split("-")[:2]
    return f"{MONTHS[int(mo) - 1]} {y}"


# ---------------------------------------------------------------- data

class Run:
    def __init__(self, name):
        self.name = name
        d = DS / "coding" / "stage2" / name
        self.items = pd.read_csv(d / "delegable" / "items.csv", dtype={"item_id": str})
        self.feats = pd.read_csv(d / "features.csv", dtype={"item_id": str}).set_index("item_id")
        self.match = pd.read_csv(d / "matches_final.csv", dtype={"item_id": str}).set_index("item_id")
        self.base = self.items[self.items.scenario == BASE].set_index("item_id")
        self.occs = list(dict.fromkeys(self.base.occupation))
        self.scenarios = list(dict.fromkeys(self.items.scenario))
        self.agg = self._aggregate()

    def _aggregate(self):
        """Occupation means exactly as delegable.py: importance-weighted over items with a D
        (zero-D types included), uncovered weight reported separately."""
        out = {}
        for (sc, occ), g in self.items.groupby(["scenario", "occupation"], sort=False):
            det = g[g.D.notna()]
            wd = det.weight.sum()
            out[(sc, occ)] = {"S": (det.weight * det.S).sum() / wd, "D": (det.weight * det.D).sum() / wd,
                              "unc": g[g.D.isna()].weight.sum() / g.weight.sum()}
        return out

    def coded(self):
        return self.base[self.base.type.isin(CODED)]


def headline_data(run):
    a = run.agg
    return {"occ": [occ_short(o) for o in run.occs],
            "S1": [round(100 * a[(BASE, o)]["S"], 3) for o in run.occs],
            "S5": [round(100 * a[(RHO5, o)]["S"], 3) for o in run.occs],
            "D1": [round(100 * a[(BASE, o)]["D"], 3) for o in run.occs],
            "D5": [round(100 * a[(RHO5, o)]["D"], 3) for o in run.occs]}


def scenarios_data(run):
    order = [s for s in SCEN_LABEL if s in run.scenarios] + [s for s in run.scenarios if s not in SCEN_LABEL]
    rows = []
    for s in order:
        lab, short = SCEN_LABEL.get(s, (s, s[:14]))
        rows.append({"lab": lab, "short": short, "base": s == BASE,
                     "S": [round(100 * run.agg[(s, o)]["S"], 3) for o in run.occs],
                     "D": [round(100 * run.agg[(s, o)]["D"], 3) for o in run.occs]})
    return {"occ": [occ_short(o) for o in run.occs], "rows": rows}


def items_data(run):
    rng = random.Random(7)
    b = run.base
    wmax = b.weight.max()
    rows = []
    for iid, r in b.iterrows():
        if pd.isna(r.D):
            continue
        coded = r.type in CODED
        lab = r.work_item if isinstance(r.work_item, str) else f"{TYPE_LAB.get(r.type, r.type)} task statement ({iid})"
        rows.append({"o": run.occs.index(r.occupation), "t": r.type, "w": round(float(r.weight / wmax), 3),
                     "S": round(100 * r.S, 1), "D": round(100 * r.D, 1), "j": round(rng.uniform(-0.3, 0.3), 3),
                     "lab": lab, "bm": bname(r.benchmark) if coded else "not coded (counts as 0)",
                     "pi": None if not coded else round(float(r.pi_at_p50), 2)})
    return {"occ": [occ_short(o) for o in run.occs], "items": rows}


def dvs_data(run):
    c = run.coded().dropna(subset=["D"])
    return {"occ": [occ_short(o) for o in run.occs],
            "pts": [{"o": run.occs.index(r.occupation), "D": round(100 * r.D, 1), "S": round(100 * r.S, 1),
                     "lab": r.work_item, "pi": round(float(r.pi_at_p50), 2)} for _, r in c.iterrows()]}


def curve(run, iid):
    """Gain and review per hour of an item, over its hours-weighted length distribution (base case)."""
    f, it = run.feats.loc[iid], run.base.loc[iid]
    mu, sd = DL.lognormal_fit(f.length_p10, f.length_p50, f.length_p90)
    mh = mu + sd * sd
    beta, H, rho = DL.BASE["beta"], float(it.H_min), float(it.rho)
    m, kap, a, bb = DL.M.get(f.context, 3.0), float(f.kappa), float(f.review_a), float(f.review_b)
    xs, gain, rev, dens = [], [], [], []
    for k in range(161):
        z = -3.2 + 6.4 * k / 160
        h = math.exp(mh + sd * z)
        pi = rho / (1 + math.exp(-beta * (math.log(H) - math.log(m * h))))
        xs.append(round(h, 3))
        gain.append(round(100 * pi * (1 - kap), 2))
        rev.append(round(100 * (a + bb * h) / h, 2))
        dens.append(math.exp(-z * z / 2))
    top = max(dens)
    dens = [round(35 * v / top, 2) for v in dens]
    polys, seg = [], []
    for x, g, r_ in zip(xs, gain, rev):
        if g > r_:
            seg.append((x, g, min(r_, 100)))
        elif seg:
            polys.append(seg)
            seg = []
    if seg:
        polys.append(seg)
    poly = {"x": [], "y": []}
    for s in polys:
        poly["x"] += [p[0] for p in s] + [p[0] for p in reversed(s)] + [None]
        poly["y"] += [p[1] for p in s] + [p[2] for p in reversed(s)] + [None]
    return {"title": f"{it.work_item[0].upper()}{it.work_item[1:]}", "bm": bname(it.benchmark), "x": xs, "gain": gain,
            "rev": rev, "dens": dens, "poly": poly, "p50": float(f.length_p50),
            "S": round(100 * float(it.S)), "D": round(100 * float(it.D))}


def mechanism_data(run):
    return {"panels": [curve(run, i) for i in EXAMPLES]}


def types_data(run):
    b = run.base
    tot = b.groupby("occupation").weight.sum()
    v = {t: [round(100 * b[(b.occupation == o) & (b.type == t)].weight.sum() / tot[o], 1) for o in run.occs] for t in TYPES}
    return {"occ": [occ_short(o) for o in run.occs], "types": TYPES, "v": v}


def coverage_data(run):
    c = run.coded()
    tot = c.weight.sum()
    bm = c.benchmark.map(lambda b: "No match or no horizon" if ("no horizon" in str(b) or b == "none" or pd.isna(b)) else bname(b))
    g = c.assign(bm=bm).groupby(["bm", "occupation"]).weight.sum().unstack(fill_value=0)
    order = [x for x in g.sum(axis=1).sort_values(ascending=False).index if x != "No match or no horizon"]
    if "No match or no horizon" in g.index:
        order.append("No match or no horizon")
    return {"occ": [occ_short(o) for o in run.occs], "bm": order,
            "v": [[round(100 * g.loc[b].get(o, 0) / tot, 1) for o in run.occs] for b in order]}


def horizons_table():
    h = pd.read_csv(DS / "benchmarks" / "horizons.csv")
    return h[h.variant == "base"].set_index("benchmark")


def horizons_data(run):
    h = horizons_table()
    c = run.coded()
    w = c.groupby("benchmark").weight.sum() / c.weight.sum()
    rows = []
    for b, r in h.sort_values("H_today_min").iterrows():
        rows.append({"name": bname(b), "grading": r.grading, "rho": r.grading in ("tests", "state"),
                     "latest": float(r.H_now_min), "today": float(r.H_today_min), "date": month(r.H_now_date),
                     "model": str(r.H_now_model), "score": round(100 * float(r.H_now_score)), "med": float(r.item_median_min),
                     "w": round(100 * float(w.get(b, 0)))})
    return {"rows": rows}


def timeline_data(runs):
    """S by occupation at monthly dates (delegable.py timeline.csv), horizons moved on the pooled trend."""
    series, dates = [], None
    for run in runs:
        tl = pd.read_csv(DS / "coding" / "stage2" / run.name / "delegable" / "timeline.csv")
        for o in run.occs:
            r1 = tl[(tl.scenario == BASE) & (tl.occupation == o)].sort_values("months_from_today")
            r5 = tl[(tl.scenario == RHO5) & (tl.occupation == o)].sort_values("months_from_today")
            dates = list(r1.date)
            series.append({"name": occ_short(o), "S1": [round(100 * v, 2) for v in r1.S],
                           "S5": [round(100 * v, 2) for v in r5.S]})
    return {"dates": dates, "series": series, "today": TODAY}


GROUP_ORDER = [("negative", "Negative controls"), ("general", "Rest of the economy"), ("white_collar", "Other white-collar"),
               ("bpo", "IT and BPO"), ("pilot", "Pilot"), ("positive", "Positive controls")]
GROUP_COL = {"negative": "#7a7268", "general": "#4fa3c7", "white_collar": "#8f68a6", "bpo": "#235fa6", "pilot": "#2f8a57",
             "positive": "#b0702a"}


def group_of(pilot, bpo, extra):
    """extra: further runs whose occupations are in comparison_tasks.csv or more_tasks.csv (control_group column)."""
    g = {o: "pilot" for o in pilot.occs}
    if bpo:
        g.update({o: "bpo" for o in bpo.occs})
    m = {}
    for f in ("comparison_tasks.csv", "more_tasks.csv"):
        if (DS / "data" / f).exists():
            ct = pd.read_csv(DS / "data" / f)
            m.update(dict(zip(ct.occupation_title, ct.control_group.replace({"bpo_extra": "bpo"}))))
    for run in extra:
        g.update({o: m[o] for o in run.occs})
    return g


def groups_data(runs, groups):
    rows = []
    for run in runs:
        for o in run.occs:
            rows.append({"g": groups[o], "occ": occ_short(o), "S1": round(100 * run.agg[(BASE, o)]["S"], 2),
                         "S5": round(100 * run.agg[(RHO5, o)]["S"], 2)})
    order = [k for k, _ in GROUP_ORDER]
    rows.sort(key=lambda r: (order.index(r["g"]), r["S1"]))
    return {"rows": rows, "labels": dict(GROUP_ORDER), "cols": GROUP_COL}


def group_timeline_data(runs, groups):
    """Unweighted mean of occupation S within each group, by month."""
    acc, dates = {}, None
    for run in runs:
        tl = pd.read_csv(DS / "coding" / "stage2" / run.name / "delegable" / "timeline.csv")
        for o in run.occs:
            for sc, key in ((BASE, "S1"), (RHO5, "S5")):
                r = tl[(tl.scenario == sc) & (tl.occupation == o)].sort_values("months_from_today")
                dates = list(r.date)
                acc.setdefault((groups[o], key), []).append(list(r.S))
    series = []
    for k, lab in GROUP_ORDER:
        if (k, "S1") not in acc:
            continue
        mean = lambda L: [round(100 * sum(x) / len(x), 2) for x in zip(*L)]  # noqa: E731
        series.append({"name": f"{lab} ({len(acc[(k, 'S1')])})", "S1": mean(acc[(k, "S1")]), "S5": mean(acc[(k, "S5")]),
                       "col": GROUP_COL[k]})
    return {"dates": dates, "series": series, "today": TODAY}


def trend_data(runs, k=8):
    """Record-setting horizon by model release date, for the k benchmarks with most matched weight."""
    f = pd.read_csv(DS / "benchmarks" / "horizons_fits.csv")
    f = f[(f.variant == "base") & f.release_date.notna()].copy()
    f["release_date"] = f.release_date.astype(str).str.slice(0, 10)
    f = f[f.release_date.str.len() == 10]
    w = pd.concat([r.coded().groupby("benchmark").weight.sum() / r.coded().weight.sum() for r in runs], axis=1).sum(axis=1)
    top = [b for b in w.sort_values(ascending=False).index if b in set(f.benchmark)][:k]
    out = []
    for b in top:
        g = f[f.benchmark == b].sort_values("release_date")
        best, xs, ys, ms = 0, [], [], []
        for _, r in g.iterrows():
            if r.H_min > best:
                best = r.H_min
                xs.append(r.release_date); ys.append(round(float(r.H_min), 2)); ms.append(str(r.model))
        out.append({"name": bname(b), "x": xs, "y": ys, "model": ms})
    return {"series": out, "today": TODAY}


def timing_raw(run="validation"):
    v = pd.read_csv(DS / "coding" / "bench_times" / run / "estimates.csv")
    tb = v[v.published_min.notna()]
    swe = v[v.benchmark == "swe-bench-verified"]
    return tb, swe


def timing_stats(run="validation"):
    tb, swe = timing_raw(run)
    lx, ly = tb.published_min.map(math.log), tb.est_median.map(math.log)
    slope = ((lx - lx.mean()) * (ly - ly.mean())).sum() / ((lx - lx.mean()) ** 2).sum()
    icpt = ly.mean() - slope * lx.mean()
    return {"slope": slope, "icpt": icpt, "rho_tb": tb.published_min.rank().corr(tb.est_median.rank()),
            "rho_swe": swe.bucket_lo.rank().corr(swe.est_median.rank()), "n_tb": len(tb), "n_swe": len(swe),
            "ratio": (tb.est_median / tb.published_min).median(),
            "within2": int(((tb.est_median / tb.published_min).between(0.5, 2)).sum()),
            "pub_lo": tb.published_min.min(), "pub_hi": tb.published_min.max(),
            "est_lo": tb.est_median.min(), "est_hi": tb.est_median.max()}


def timing_data():
    tb, swe = timing_raw()
    st = timing_stats()
    buckets = sorted({(float(r.bucket_lo), float(r.bucket_hi) if pd.notna(r.bucket_hi) else None) for _, r in swe.iterrows()})
    rng = random.Random(3)
    return {"tb": {"pub": tb.published_min.round(1).tolist(), "est": tb.est_median.round(1).tolist()},
            "slope": round(st["slope"], 3), "icpt": round(st["icpt"], 3),
            "buckets": [{"lo": lo, "hi": hi} for lo, hi in buckets],
            "swe": [{"b": [lo for lo, _ in buckets].index(float(r.bucket_lo)), "est": float(r.est_median),
                     "j": round(rng.uniform(-0.22, 0.22), 3)} for _, r in swe.iterrows()]}


# ---------------------------------------------------------------- tokens: every number quoted in the prose

def tokens(pilot):
    t = {}
    a = pilot.agg
    for occ in pilot.occs:
        k = OCC_KEY.get(occ)
        if not k:
            continue
        for sc, suf in [(BASE, ""), (RHO5, "5"), ("latest observed H (no date alignment)", "_noalign"),
                        ("decompressed spread, both sides", "_decomp"), ("decompressed spread, benchmarks only", "_decompb"),
                        ("lambda 3", "_lam3"), ("lambda 0.25", "_lam025"), ("beta 0.6", "_b06"), ("beta 1.0", "_b10"),
                        ("+12 months (pooled trend)", "_12m"), ("fill from 2nd match", "_fill")]:
            t[f"{k}_S{suf}"] = pct(a[(sc, occ)]["S"])
            t[f"{k}_D{suf}"] = pct(a[(sc, occ)]["D"])
        t[f"{k}_unc"] = pct(a[(BASE, occ)]["unc"])
        b = pilot.base[pilot.base.occupation == occ]
        for ty, nm in zip(TYPES, ["disc", "live", "inter", "phys", "nodel"]):
            t[f"{k}_{nm}"] = pct(b[b.type == ty].weight.sum() / b.weight.sum())
        c = b[b.type.isin(CODED)]
        mt = pilot.match.loc[c.index]
        nohz = c.benchmark.astype(str).str.contains("no horizon")
        t[f"{k}_good"] = pct(c[(mt.best_match == "good") & ~nohz].weight.sum() / c.weight.sum())
        t[f"{k}_partial"] = pct(c[(mt.best_match == "partial") & ~nohz].weight.sum() / c.weight.sum())
        t[f"{k}_p50"] = f"{pilot.feats.loc[c.index].length_p50.median():.0f}"
        t[f"{k}_zero"] = pct(b[~b.type.isin(CODED)].weight.sum() / b.weight.sum())
        grading = c.benchmark.map(horizons_table().grading)
        t[f"{k}_rhoshare"] = pct(c[grading.isin(["tests", "state"])].weight.sum() / c.weight.sum())
    uncs = [a[(BASE, o)]["unc"] for o in pilot.occs]
    t["unc_max"] = pct(max(uncs))
    parts = []
    for o in pilot.occs:
        c = pilot.coded()[pilot.coded().occupation == o]
        mt = pilot.match.loc[c.index]
        parts.append(c[(mt.best_match == "partial")].weight.sum() / c.weight.sum())
    t["partial_lo"], t["partial_hi"] = f"{100 * min(parts):.0f}", pct(max(parts))
    # item ranges by benchmark, and the decompression stretch
    c = pilot.coded()
    for bm in ("gdpval", "itbench_sre"):
        v = c[c.benchmark == bm].S
        t[f"{bm}_S_lo"], t[f"{bm}_S_hi"], t[f"{bm}_n"] = pct(v.min()), pct(v.max()), str(len(v))
    t["S_item_max"] = pct(c.S.max())
    ff = pilot.feats.loc[c.index]
    ratio = ((ff.length_p90.map(math.log) - ff.length_p10.map(math.log)) / DL.COMPRESSION).map(math.exp)
    t["decomp_ratio"] = f"{round(ratio.median(), -1):.0f}"
    t["compression"] = f"{DL.COMPRESSION:.2f}"
    # counts
    tasks = pd.read_csv(DS / "data" / "pilot_tasks.csv")
    t["n_statements"] = str(int(tasks.im.notna().sum()))
    t["n_items"] = str(len(pilot.base))
    t["n_coded"] = str(len(pilot.coded()))
    f = pilot.feats
    t["n_medium"] = str(int((f.context == "medium").sum()))
    t["n_high"] = str(int((f.context == "high").sum()))
    t["n_low"] = str(int((f.context == "low").sum()))
    kap = f.groupby("domain").kappa.first()
    for dom, nm in [("software", "kappa_sw"), ("computer_use", "kappa_cu"), ("text", "kappa_text")]:
        t[nm] = pct(kap[dom])
    t["review_b_med"] = pct(f.review_b.median())
    t["review_a_med"] = f"{f.review_a.median():.1f}"
    t["live_n"] = str(int((pilot.base.type == "LIVE_SERVICE").sum()))
    # model settings, from delegable.py
    t["beta"] = f"{DL.BASE['beta']:.2f}"
    t["beta_doubling"] = f"{DL.BASE['beta'] * math.log(2):.2f}"
    t["q"] = pct(DL.BASE["q"])
    t["lam"] = f"{DL.BASE['lam']:g}"
    t["m_low"], t["m_med"], t["m_high"] = (f"{DL.M[x]:g}" for x in ("low", "medium", "high"))
    # live items under rho = 0.5: the agent must succeed more often than lam / (1 - kappa + lam)
    live = f.loc[pilot.base[pilot.base.type == "LIVE_SERVICE"].index]
    th = [DL.BASE["lam"] / (1 - k + DL.BASE["lam"]) for k in live.kappa]
    t["live_thresh_lo"], t["live_thresh_hi"] = f"{100 * min(th):.0f}", pct(max(th))
    r5 = pilot.items[(pilot.items.scenario == RHO5) & (pilot.items.type == "LIVE_SERVICE")]
    t["live_r5_zero"] = "every" if (r5.D.fillna(0) == 0).all() else "most"
    # worked examples
    for n, iid in enumerate(EXAMPLES, 1):
        fe, it = f.loc[iid], pilot.base.loc[iid]
        h = float(fe.length_p50)
        pi, k = float(it.pi_at_p50), float(fe.kappa)
        gain, rev = pi * (1 - k) * h, float(fe.review_a) + float(fe.review_b) * h
        t[f"ex{n}_h"] = dur(h)
        t[f"ex{n}_hmin"] = f"{h:.0f}"
        t[f"ex{n}_eff"] = f"{h * DL.M.get(fe.context, 3.0):.0f}"
        t[f"ex{n}_pi"] = f"{pi:.2f}"
        t[f"ex{n}_pipct"] = pct(pi)
        t[f"ex{n}_kappa"] = f"{k:.2f}"
        t[f"ex{n}_gain"] = f"{gain:.1f}"
        t[f"ex{n}_rev"] = f"{rev:.1f}"
        t[f"ex{n}_net"] = f"{gain - rev:.1f}"
        t[f"ex{n}_netpct"] = pct((gain - rev) / h)
        t[f"ex{n}_S"] = pct(float(it.S))
        t[f"ex{n}_D"] = pct(float(it.D))
        t[f"ex{n}_bm"] = bname(it.benchmark)
        t[f"ex{n}_H"] = dur(float(it.H_min))
        t[f"ex{n}_thresh"] = pct((float(fe.review_a) / h + float(fe.review_b)) / (1 - k))
        t[f"ex{n}_b"] = pct(float(fe.review_b))
    # horizons
    hz = horizons_table()
    t["n_bench"] = str(len(hz))
    t["n_bench_items"] = f"{int(hz.n_items.sum()):,}"
    t["pooled"] = f"{hz.pooled_doubling_months.iloc[0]:g}"
    c = pilot.coded()
    for b, r in hz.iterrows():
        t[f"hz_{b}_today"] = dur(r.H_today_min)
        t[f"hz_{b}_latest"] = dur(r.H_now_min)
        t[f"hz_{b}_date"] = month(r.H_now_date)
        t[f"hz_{b}_score"] = pct(r.H_now_score)
        t[f"hz_{b}_med"] = dur(r.item_median_min)
        t[f"hz_{b}_ratio"] = f"{r.H_today_min / r.H_now_min:,.0f}"
        t[f"w_{b}"] = pct(c[c.benchmark == b].weight.sum() / c.weight.sum())
    st = timing_stats()
    t["tb_slope"] = f"{st['slope']:.2f}"
    t["tb_rho"] = f"{st['rho_tb']:.2f}"
    t["swe_rho"] = f"{st['rho_swe']:.2f}"
    t["tb_n"], t["swe_n"] = str(st["n_tb"]), str(st["n_swe"])
    t["tb_within2"] = str(st["within2"])
    t["tb_pub_range"] = f"{st['pub_lo']:,.0f}–{st['pub_hi']:,.0f} minutes"
    t["tb_est_range"] = f"{st['est_lo']:,.0f}–{st['est_hi']:,.0f} minutes"
    t["tb_ratio"] = f"{st['ratio']:.2f}"
    an = timing_stats("validation_anchored")
    t["anch_slope"], t["anch_ratio"] = f"{an['slope']:.2f}", f"{an['ratio']:.2f}"
    return t


# ---------------------------------------------------------------- generated tables

def table_html(head, rows, cls="items"):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def gt_summary(run):
    a = run.agg
    rows = [[html.escape(o), pct(a[(BASE, o)]["S"]), pct(a[(RHO5, o)]["S"]), pct(a[(BASE, o)]["D"]),
             pct(a[(RHO5, o)]["D"]), pct(a[(BASE, o)]["unc"])] for o in run.occs]
    return table_html(["Occupation", "S, ρ = 1", "S, ρ = 0.5", "D, ρ = 1", "D, ρ = 0.5", "Uncovered"], rows)


def gt_match(run):
    rows = []
    for o in run.occs:
        c = run.coded()[run.coded().occupation == o]
        mt = run.match.loc[c.index]
        nohz = c.benchmark.astype(str).str.contains("no horizon")
        w = c.weight.sum()
        sh = lambda m: pct(m.sum() / w)  # noqa: E731
        rows.append([html.escape(occ_short(o)), sh(c.weight[(mt.best_match == "good") & ~nohz]),
                     sh(c.weight[(mt.best_match == "partial") & ~nohz]), sh(c.weight[mt.best_match == "none"]),
                     sh(c.weight[nohz & (mt.best_match != "none")])])
    return table_html(["Occupation", "Good", "Partial", "No match", "Matched, but no horizon"], rows)


def gt_items(run):
    r5 = run.items[run.items.scenario == RHO5].set_index("item_id")
    rows = []
    for iid, r in run.coded().iterrows():
        has = pd.notna(r.D)
        f = lambda v: pct(v) if pd.notna(v) else "–"  # noqa: E731
        rows.append([html.escape(occ_short(r.occupation)), html.escape(r.work_item),
                     "live" if r.type == "LIVE_SERVICE" else "discrete", html.escape(bname(r.benchmark)),
                     f"{r.pi_at_p50:.2f}" if has else "–", f(r.D), f(r.S), f(r5.loc[iid].S)])
    return table_html(["Occupation", "Work item", "Type", "Benchmark", "π, typical item", "D", "S", "S, ρ = 0.5"], rows,
                      cls="items itemlist")


# ---------------------------------------------------------------- figure shells

def sw(color, hollow=False):
    st = f"border:1.5px solid {color};background:transparent" if hollow else f"background:{color}"
    return f'<span><span class="sw" style="{st}"></span>'


def ln(color, style="solid", w=3):
    return f'<span><i style="border-color:{color};border-top-style:{style};border-top-width:{w}px"></i>'


OCC_CSS = ["#235fa6", "#b0702a", "#2f8a57", "#8f68a6", "#c0607e", "#4d6f91", "#ae8a2c", "#5a9370", "#b8643f",
           "#7a7268", "#163d6b", "#6fb38a", "#93c9a8"]
TYPE_CSS = {"DISCRETE": "#235fa6", "LIVE_SERVICE": "#b0702a", "INTERPERSONAL": "#8f68a6", "PHYSICAL": "#7a7268",
            "NO_DELIVERABLE": "#cfc4b4"}
TYPE_LAB = {"DISCRETE": "Discrete", "LIVE_SERVICE": "Live service", "INTERPERSONAL": "Interpersonal",
            "PHYSICAL": "Physical", "NO_DELIVERABLE": "No deliverable"}


def occ_legend(occs):
    return "".join(sw(OCC_CSS[i % len(OCC_CSS)]) + html.escape(occ_short(o)) + "</span>" for i, o in enumerate(occs))


def fig(name, title="", legend="", note=""):
    t = f'<div class="fig-title">{title}</div>' if title else ""
    lg = f'<div class="legend" aria-hidden="true">{legend}</div>' if legend else ""
    top = f'<div class="fig-top">{t}{lg}</div>' if (t or lg) else ""
    return (f'<figure class="wide" id="fig-{name}"><div class="fig-panel">{top}'
            f'<div id="chart-{name}" class="chart" role="img" aria-label="{html.escape(re.sub("<[^>]+>", "", title or name))}"></div>'
            + (f'<div class="fig-note">{note}</div>' if note else "")
            + '</div><figcaption>{caption}</figcaption></figure>')


def figure_shells(pilot, bpo, comp=None):
    rho = sw("#235fa6") + "ρ = 1</span>" + sw("#9fb8d6") + "ρ = 0.5 for test- and state-graded benchmarks</span>"
    types = "".join(sw(TYPE_CSS[t]) + TYPE_LAB[t] + "</span>" for t in TYPES)
    item_types = (sw(TYPE_CSS["DISCRETE"]) + "Discrete</span>" + sw(TYPE_CSS["LIVE_SERVICE"]) + "Live service</span>"
                  + sw("#cfc4b4", True) + "Interpersonal, physical or no deliverable (0)</span>")
    shells = {
        "headline": fig("headline", "Pilot occupations, % of unassisted hours", rho),
        "mechanism": fig("mechanism", "Per hour of work, % of the item's unassisted time",
                         ln("#235fa6") + "Expected saving if delegated, π(1−κ)</span>" + ln("#b0702a") + "Review time, (a + bh)/h</span>"
                         + sw("rgba(35,95,166,0.25)") + "Net saving (counted in S)</span>" + sw("rgba(207,196,180,0.6)")
                         + "Where the item's hours are</span>"),
        "dvs": fig("dvs", "Each coded work item, baseline (ρ = 1)", occ_legend(pilot.occs)),
        "items": fig("items", "Each work item, baseline (ρ = 1); marker area ∝ importance weight", item_types),
        "scenarios": fig("scenarios", "One setting changed at a time from the baseline", occ_legend(pilot.occs)
                         + ln("#8a7d6d", "dotted", 1.5) + "Baseline value</span>"),
        "types": fig("types", "Share of each occupation's importance weight, by type of work item", types),
        "coverage": fig("coverage", "Share of the pilot's coded weight matched to each benchmark", occ_legend(pilot.occs)),
        "horizons": fig("horizons", "Horizon: item length at which the best agent succeeds half the time (log scale)",
                        sw("#235fa6") + "Today, graded by tests or state checks</span>" + sw("#b0702a")
                        + "Today, other grading</span>" + sw("#8a7d6d", True) + "Latest observed</span>"
                        + '<span><b class="mk" style="color:#8a7d6d">|</b>Median item (our estimate)</span>'),
        "timing": fig("timing", "Our coders' blind estimates against published times (log scales)",
                      ln("#8a7d6d", "dashed", 1.5) + "Estimate = published</span>" + ln("#235fa6", "solid", 2)
                      + "Fitted line</span>"),
    }
    runs_occs = pilot.occs + (bpo.occs if bpo else [])
    shells["timeline"] = fig("timeline", "S over time, % of unassisted hours (horizons moved along the pooled trend)", occ_legend(runs_occs))
    grp_leg = "".join(sw(GROUP_COL[k]) + lab + "</span>" for k, lab in GROUP_ORDER) + sw("#8a7d6d", True) + "Hollow: ρ = 0.5</span>"
    shells["groups"] = fig("groups", "S by occupation, % of unassisted hours (filled: ρ = 1; hollow: ρ = 0.5)", grp_leg)
    shells["group_timeline"] = fig("group_timeline", "S over time, average of the occupations in each group (pooled trend)",
                                   "".join(sw(GROUP_COL[k]) + lab + "</span>" for k, lab in GROUP_ORDER))
    shells["trend"] = fig("trend", "Horizon of the best model released so far, by release date (log scale)")
    if bpo:
        shells["bpo_headline"] = fig("bpo_headline", "BPO occupations, % of unassisted hours", rho)
        shells["bpo_items"] = fig("bpo_items", "Each work item, baseline (ρ = 1); marker area ∝ importance weight", item_types)
    return shells


# ---------------------------------------------------------------- text rendering (as in build_health_check.py, plus math)

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub("<[^>]+>", "", t).lower()).strip("-")


def math_span(tex, display=False):
    esc = html.escape(tex, quote=True)
    if display:
        return f'<div class="math" data-tex="{esc}"><span class="math-fallback">{html.escape(tex)}</span></div>'
    return f'<span class="imath" data-tex="{esc}">{html.escape(tex)}</span>'


class Doc:
    def __init__(self, tok, notes, figures, gentables, bpo):
        self.tok, self.notes, self.figures, self.gentables, self.bpo = tok, notes, figures, gentables, bpo
        self.order, self.toc = [], []

    def inl(self, s):
        maths = []

        def keep(m):
            maths.append(m.group(1))
            return f"\x03{len(maths) - 1}\x03"
        s = re.sub(r"\$(.+?)\$", keep, s)
        h = inline(s, self.tok)
        return re.sub(r"\x03(\d+)\x03", lambda m: math_span(maths[int(m.group(1))]), h)

    def il(self, s):
        refs = []

        def take(m):
            refs.append(m.group(1))
            return f"\x02{len(refs) - 1}\x02"
        s = re.sub(r"\[\^([\w-]+)\]", take, s)
        h = self.inl(s)

        def put(m):
            key = refs[int(m.group(1))]
            if key not in self.order:
                self.order.append(key)
            n = self.order.index(key) + 1
            body = self.inl(self.notes.get(key, f"MISSING NOTE {key}"))
            return (f'<span class="fn"><a class="fn-ref" href="#note-{key}" aria-label="Note {n}">{n}</a>'
                    f'<span class="fn-pop" role="note"><span class="fn-n">{n}</span> {body}</span></span>')
        return re.sub(r"\x02(\d+)\x02", put, h)

    def block(self, kind, arg, lines, depth):
        if kind == "figure":
            cap = " ".join(l.strip() for l in lines if l.strip())
            assert arg in self.figures, f"no figure shell for {arg}"
            return self.figures[arg].replace("{caption}", self.il(cap))
        if kind == "details":
            sid = slug(arg)
            self.toc.append((3, arg, sid, True))
            return (f'<details class="more" id="{sid}"><summary><span class="more-title">{self.il(arg)}</span>'
                    f'<span class="more-hint">Optional detail. Click to expand.</span></summary>'
                    f'<div class="more-body">{self.render(lines, depth + 1)}</div></details>')
        if kind == "if-bpo":
            return self.render(lines, depth) if self.bpo else ""
        if kind == "if-no-bpo":
            return "" if self.bpo else f'<div class="pending">{self.render(lines, depth)}</div>'
        if kind == "table":
            st = [l.strip() for l in lines]
            top, note_lines = (lines[:st.index("---")], lines[st.index("---") + 1:]) if "---" in st else (lines, [])
            cap = " ".join(l.strip() for l in top if l.strip() and not l.strip().startswith("|"))
            tbl = [l for l in top if l.strip().startswith("|")]
            note = " ".join(l.strip() for l in note_lines if l.strip())
            return ('<div class="table-wrap">' + (f'<p class="table-cap">{self.il(cap)}</p>' if cap else "")
                    + pipe_table(tbl, self.tok).replace('class="items"', 'class="items text"')
                    + (f'<p class="table-note">{self.il(note)}</p>' if note else "") + "</div>")
        assert kind == "gentable", f"unknown block kind {kind}"
        assert arg in self.gentables, f"no generated table {arg}"
        st = [l.strip() for l in lines]
        top, note_lines = (lines[:st.index("---")], lines[st.index("---") + 1:]) if "---" in st else (lines, [])
        cap = " ".join(l.strip() for l in top if l.strip())
        note = " ".join(l.strip() for l in note_lines if l.strip())
        return ('<div class="table-wrap">' + (f'<p class="table-cap">{self.il(cap)}</p>' if cap else "") + self.gentables[arg]()
                + (f'<p class="table-note">{self.il(note)}</p>' if note else "") + "</div>")

    def render(self, lines, depth=0):
        out, para, i = [], [], 0
        appendix = False

        def flush():
            if para:
                out.append(f"<p>{self.il(' '.join(para))}</p>")
                para.clear()
        while i < len(lines):
            st = lines[i].strip()
            if not st:
                flush(); i += 1; continue
            if st.startswith("<!--"):
                flush()
                while "-->" not in lines[i]:
                    i += 1
                i += 1; continue
            if st.startswith("$$"):
                flush()
                buf = [st]
                while not (buf[-1].endswith("$$") and len("\n".join(buf)) > 2):
                    i += 1
                    buf.append(lines[i].strip())
                out.append(math_span(" ".join(buf)[2:-2].strip(), display=True))
                i += 1; continue
            if st.startswith("## "):
                flush()
                title = st[3:]
                m = re.match(r"(\d+)\.\s+(.*)", title)
                num, t = (m.group(1), m.group(2)) if m else ("", title)
                sid = slug(t)
                self.toc.append((2, (f"{num}. " if num else "") + t, sid, False))
                appendix = t.lower().startswith("appendix")
                out.append(f'<h2 id="{sid}">' + (f'<span class="num">{num}</span>' if num else "") + f"{self.il(t)}</h2>")
                i += 1; continue
            if st.startswith("### "):
                flush()
                t = st[4:]
                sid = slug(t)
                if appendix:
                    out.append(f'<details class="app" id="{sid}"><summary>{self.il(t)}</summary><div>')
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith(("### ", "## ")) and not re.match(r"^\[\^[\w-]+\]:", lines[j].strip()):
                        j += 1
                    out.append(self.render(lines[i + 1:j], depth + 1))
                    out.append("</div></details>")
                    i = j; continue
                self.toc.append((3, t, sid, False))
                out.append(f'<h3 id="{sid}">{self.il(t)}</h3>')
                i += 1; continue
            if st.startswith(":::") and st != ":::":
                flush()
                parts = st[3:].strip().split(None, 1)
                kind, arg = parts[0], (parts[1] if len(parts) > 1 else None)
                j, d = i + 1, 1
                while True:
                    s2 = lines[j].strip()
                    if s2 == ":::":
                        d -= 1
                        if d == 0:
                            break
                    elif s2.startswith(":::"):
                        d += 1
                    j += 1
                out.append(self.block(kind, arg, lines[i + 1:j], depth))
                i = j + 1; continue
            if re.match(r"^\[\^[\w-]+\]:", st):
                flush(); i += 1; continue
            if re.match(r"^(- |\d+\. )", st):
                flush()
                ordered = bool(re.match(r"^\d+\. ", st))
                items = []
                while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i].strip()):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i].strip()))
                    i += 1
                    while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^(- |\d+\. )", lines[i].strip()):
                        items[-1] += " " + lines[i].strip()  # wrapped bullet
                        i += 1
                lis = "".join(f"<li>{self.il(it)}</li>" for it in items)
                out.append(f"<ol>{lis}</ol>" if ordered else f"<ul>{lis}</ul>")
                continue
            para.append(st)
            i += 1
        flush()
        return "\n".join(o for o in out if o)


def toc_html(toc, doc):
    items, open_sub = [], False
    for level, title, sid, collapsible in toc:
        label = doc.inl(title)
        if level == 2:
            if open_sub:
                items.append("</ul></li>"); open_sub = False
            items.append(f'<li><a href="#{sid}" data-target="{sid}">{label}</a><ul>')
            open_sub = True
        else:
            cls = ' class="opt"' if collapsible else ""
            items.append(f'<li{cls}><a href="#{sid}" data-target="{sid}">{label}</a></li>')
    if open_sub:
        items.append("</ul></li>")
    body = "".join(items).replace("<ul></ul>", "")
    return f'<nav class="toc" aria-label="Contents"><div class="toc-head">Contents</div><ul>{body}</ul></nav>'


# ---------------------------------------------------------------- charts (page-specific; shared helpers come from the template)

CHART_JS = r"""
const OCC_COL = ["#235fa6", "#b0702a", "#2f8a57", "#8f68a6", "#c0607e", "#4d6f91", "#ae8a2c", "#5a9370", "#b8643f", "#7a7268", "#163d6b", "#6fb38a", "#93c9a8"];
const TYPE_COL = { DISCRETE: "#235fa6", LIVE_SERVICE: "#b0702a", INTERPERSONAL: "#8f68a6", PHYSICAL: "#7a7268", NO_DELIVERABLE: "#cfc4b4" };
const TYPE_LAB = { DISCRETE: "Discrete", LIVE_SERVICE: "Live service", INTERPERSONAL: "Interpersonal", PHYSICAL: "Physical", NO_DELIVERABLE: "No deliverable" };
const P = v => v === null ? "–" : Math.round(v) + "%";
const DUR = m => m < 90 ? Math.round(m) + " min" : (m / 60 < 10 ? (m / 60).toFixed(1) : Math.round(m / 60).toLocaleString()) + " h";
const LOGTICKS = { tickvals: [1, 10, 60, 600, 6000, 60000, 600000], ticktext: ["1 min", "10 min", "1 h", "10 h", "100 h", "1,000 h", "10,000 h"] };
const stackH = (narrow, n, per, pad) => (narrow ? 2 : 1) * (pad + per * n);

/* S and D by occupation, two reliability cases */
function figHeadline(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.16 : 0.07, n = d.occ.length;
  const traces = [], ann = [];
  const lay = { barmode: "group", bargap: 0.3, bargroupgap: 0.06, hovermode: "closest", height: stackH(narrow, n, 50, 46) + 30,
    margin: { l: narrow ? 118 : 132, r: 36, t: 24, b: 28 } };
  ["S", "D"].forEach((m, i) => {
    const k = i ? "2" : "", p = twoPanels(narrow, i, gap);
    [["1", C.accent, "ρ = 1"], ["5", C.light, "ρ = 0.5"]].forEach(([r, col, nm]) => {
      const v = d[m + r];
      traces.push({ type: "bar", orientation: "h", y: d.occ, x: v, xaxis: "x" + k, yaxis: "y" + k, marker: { color: col },
        text: v.map(P), textposition: "outside", cliponaxis: false, textfont: small(11.5),
        hovertemplate: "%{y}: " + m + " = %{x:.1f}%<extra>" + nm + "</extra>" });
    });
    lay["xaxis" + k] = axis({ domain: p.x, anchor: "y" + k, range: [0, 100], ticksuffix: "%", dtick: 25 });
    lay["yaxis" + k] = axis({ domain: p.y, anchor: "x" + k, autorange: "reversed", showticklabels: i === 0 || narrow, ticks: "" });
    ann.push(ptitle(k, m === "S" ? "S: net hours saved" : "D: hours handed to an agent"));
  });
  lay.annotations = ann; draw(el, traces, lay); el.dataset.narrow = narrow;
}

/* the delegation rule for one item, over its range of lengths */
function figMechanism(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.2 : 0.08;
  const traces = [], ann = [], shapes = [], lay = { hovermode: "x unified", height: narrow ? 640 : 340, margin: { l: 46, r: 10, t: 34, b: 40 } };
  d.panels.forEach((q, i) => {
    const k = i ? "2" : "", p = twoPanels(narrow, i, gap), ax = { xaxis: "x" + k, yaxis: "y" + k };
    traces.push(Object.assign({ x: q.x, y: q.dens, type: "scatter", mode: "lines", fill: "tozeroy", line: { width: 0 }, fillcolor: "rgba(207,196,180,0.45)", hoverinfo: "skip" }, ax));
    traces.push(Object.assign({ x: q.poly.x, y: q.poly.y, type: "scatter", mode: "lines", fill: "toself", line: { width: 0 }, fillcolor: "rgba(35,95,166,0.18)", hoverinfo: "skip" }, ax));
    traces.push(Object.assign({ x: q.x, y: q.gain, type: "scatter", mode: "lines", line: { color: C.accent, width: 2.5 }, hovertemplate: "saving %{y:.0f}%<extra></extra>" }, ax));
    traces.push(Object.assign({ x: q.x, y: q.rev.map(v => Math.min(v, 140)), type: "scatter", mode: "lines", line: { color: C.a, width: 2.5 }, hovertemplate: "review %{y:.0f}%<extra></extra>" }, ax));
    lay["xaxis" + k] = axis(Object.assign({ domain: p.x, anchor: "y" + k, type: "log", title: { text: "Item length", font: small(12), standoff: 4 } }, LOGTICKS,
      { range: [Math.log10(q.x[0]), Math.log10(q.x[q.x.length - 1])], hoverformat: ".0f" }));
    lay["yaxis" + k] = axis({ domain: p.y, anchor: "x" + k, range: [0, 100], ticksuffix: "%", dtick: 25 });
    shapes.push(vline(k, q.p50));
    ann.push(ptitle(k, q.title.length > 46 && narrow ? q.title.slice(0, 44) + "…" : q.title));
    ann.push(lab(k, Math.log10(q.p50), 97, "typical item", { xanchor: "left", xshift: 4 }));
    ann.push({ xref: "x" + k + " domain", yref: "y" + k + " domain", x: 1, y: 0.86, xanchor: "right", showarrow: false, align: "right",
      text: "matched to " + q.bm + "<br><b>S = " + q.S + "%</b>, D = " + q.D + "%", font: { family: FONT, size: 12, color: C.ink2 } });
  });
  lay.annotations = ann; lay.shapes = shapes; draw(el, traces, lay); el.dataset.narrow = narrow;
}

/* D against S, per coded item */
function figDvS(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640;
  const traces = d.occ.map((o, i) => {
    const pts = d.pts.filter(p => p.o === i);
    return { x: pts.map(p => p.D), y: pts.map(p => p.S), type: "scatter", mode: "markers", name: o,
      marker: { color: OCC_COL[i % OCC_COL.length], size: 8, opacity: 0.85, line: { color: "#fffdf9", width: 0.8 } },
      customdata: pts.map(p => [p.lab, p.pi]), hovertemplate: "%{customdata[0]}<br>D %{x:.0f}%, S %{y:.0f}%, π at typical length %{customdata[1]}<extra>" + o + "</extra>" };
  });
  traces.unshift({ x: [0, 100], y: [0, 100], type: "scatter", mode: "lines", line: { color: C.rule2, width: 1, dash: "dot" }, hoverinfo: "skip" });
  draw(el, traces, { height: narrow ? 330 : 360, hovermode: "closest", margin: { l: 50, r: 10, t: 8, b: 42 },
    xaxis: axis({ range: [-3, 103], ticksuffix: "%", title: ytitle("D: share of hours handed to an agent") }),
    yaxis: axis({ range: [-3, 103], ticksuffix: "%", title: ytitle("S: net hours saved") }),
    annotations: [{ x: 70, y: 70, text: "S = D", showarrow: false, textangle: narrow ? 0 : -33, yshift: 9, font: { family: FONT, size: 11.5, color: C.ink3 } }] });
  el.dataset.narrow = narrow;
}

/* every item, S and D, by occupation and type */
function figItems(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.14 : 0.06, n = d.occ.length;
  const traces = [], ann = [];
  const lay = { hovermode: "closest", height: stackH(narrow, n, 78, 30) + 40, margin: { l: narrow ? 104 : 120, r: 10, t: 24, b: 30 } };
  ["S", "D"].forEach((m, i) => {
    const k = i ? "2" : "", p = twoPanels(narrow, i, gap);
    Object.keys(TYPE_COL).forEach(t => {
      const pts = d.items.filter(q => q.t === t); if (!pts.length) return;
      const coded = t === "DISCRETE" || t === "LIVE_SERVICE";
      traces.push({ x: pts.map(q => q[m]), y: pts.map(q => q.o + q.j), xaxis: "x" + k, yaxis: "y" + k, type: "scatter", mode: "markers",
        marker: { size: pts.map(q => 5 + 11 * Math.sqrt(q.w)), color: coded ? tint(TYPE_COL[t], 0.75) : "rgba(0,0,0,0)",
          line: { color: coded ? "#fffdf9" : "#b5a994", width: coded ? 0.8 : 1.2 } },
        customdata: pts.map(q => [q.lab, q.bm, q.pi === null ? "–" : q.pi, q.S, q.D, d.occ[q.o]]),
        hovertemplate: "<b>%{customdata[0]}</b><br>%{customdata[5]} · " + TYPE_LAB[t] + "<br>Benchmark: %{customdata[1]}<br>π at typical length: %{customdata[2]}<br>S %{customdata[3]:.0f}%, D %{customdata[4]:.0f}%<extra></extra>" });
    });
    lay["xaxis" + k] = axis({ domain: p.x, anchor: "y" + k, range: [-4, 104], ticksuffix: "%", dtick: 25 });
    lay["yaxis" + k] = axis({ domain: p.y, anchor: "x" + k, range: [n - 0.5, -0.5], tickvals: d.occ.map((_, j) => j), ticktext: d.occ,
      showticklabels: i === 0 || narrow, ticks: "", showline: false });
    ann.push(ptitle(k, m === "S" ? "S: net hours saved" : "D: hours handed to an agent"));
  });
  const shapes = [];
  ["", "2"].forEach(k => { for (let j = 0; j < n - 1; j++) shapes.push(hline(k, j + 0.5, { line: { color: C.rule, width: 1 } })); });
  lay.annotations = ann; lay.shapes = shapes; draw(el, traces, lay); el.dataset.narrow = narrow;
}

/* scenario dot plot */
function figScenarios(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.1 : 0.05, nr = d.rows.length;
  const y = d.rows.map(r => { const t = narrow ? r.short : r.lab; return r.base ? "<b>" + t + "</b>" : t; });
  const traces = [], ann = [], shapes = [];
  const lay = { hovermode: "closest", height: (narrow ? 2 : 1) * (26 * nr + 20) + 50, margin: { l: narrow ? 92 : 300, r: 12, t: 24, b: 30 } };
  ["S", "D"].forEach((m, i) => {
    const k = i ? "2" : "", p = twoPanels(narrow, i, gap);
    const sx = [], sy = [];
    d.rows.forEach((r, j) => { sx.push(Math.min(...r[m]), Math.max(...r[m]), null); sy.push(y[j], y[j], null); });
    traces.push({ x: sx, y: sy, xaxis: "x" + k, yaxis: "y" + k, type: "scatter", mode: "lines", line: { color: C.rule2, width: 2 }, hoverinfo: "skip" });
    d.occ.forEach((o, q) => {
      traces.push({ x: d.rows.map(r => r[m][q]), y, xaxis: "x" + k, yaxis: "y" + k, type: "scatter", mode: "markers", name: o,
        marker: { color: OCC_COL[q % OCC_COL.length], size: 9, line: { color: "#fffdf9", width: 1 } },
        hovertemplate: o + ": " + m + " = %{x:.0f}%<extra></extra>" });
      shapes.push(Object.assign(vline(k, d.rows[0][m][q]), { line: { color: OCC_COL[q % OCC_COL.length], width: 1, dash: "dot" } }));
    });
    lay["xaxis" + k] = axis({ domain: p.x, anchor: "y" + k, range: [0, 100], ticksuffix: "%", dtick: 25 });
    lay["yaxis" + k] = axis({ domain: p.y, anchor: "x" + k, autorange: "reversed", type: "category", showticklabels: i === 0 || narrow, ticks: "", showline: false, tickfont: small(narrow ? 11 : 12.5) });
    ann.push(ptitle(k, m === "S" ? "S: net hours saved" : "D: hours handed to an agent"));
  });
  lay.annotations = ann; lay.shapes = shapes; draw(el, traces, lay); el.dataset.narrow = narrow;
}

/* type of work item, share of weight */
function figTypes(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640;
  const traces = d.types.map(t => ({ type: "bar", orientation: "h", y: d.occ, x: d.v[t], name: TYPE_LAB[t], marker: { color: TYPE_COL[t] },
    text: d.v[t].map(v => v >= 6 ? Math.round(v) + "%" : ""), textposition: "inside", insidetextanchor: "middle",
    textfont: { family: FONT, size: 11.5, color: t === "NO_DELIVERABLE" ? C.ink : "#fff" },
    hovertemplate: "%{y}: " + TYPE_LAB[t] + " %{x:.0f}%<extra></extra>" }));
  draw(el, traces, { barmode: "stack", bargap: 0.35, height: 44 * d.occ.length + 60, hovermode: "closest",
    margin: { l: narrow ? 108 : 124, r: 10, t: 6, b: 28 },
    xaxis: axis({ range: [0, 100], ticksuffix: "%", dtick: 25 }), yaxis: axis({ autorange: "reversed", ticks: "", showline: false }) });
  el.dataset.narrow = narrow;
}

/* weight by matched benchmark */
function figCoverage(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640;
  const traces = d.occ.map((o, i) => ({ type: "bar", orientation: "h", y: d.bm, x: d.v.map(r => r[i]), name: o,
    marker: { color: OCC_COL[i % OCC_COL.length] }, hovertemplate: "%{y}: " + o + " %{x:.1f}% of coded weight<extra></extra>" }));
  const tot = d.v.map(r => r.reduce((a, b) => a + b, 0));
  traces.push({ type: "scatter", mode: "text", y: d.bm, x: tot, text: tot.map(v => Math.round(v) + "%"), textposition: "middle right",
    textfont: small(11.5), hoverinfo: "skip", cliponaxis: false });
  draw(el, traces, { barmode: "stack", bargap: 0.3, height: 22 * d.bm.length + 50, hovermode: "closest",
    margin: { l: narrow ? 128 : 160, r: 30, t: 6, b: 28 },
    xaxis: axis({ ticksuffix: "%", range: [0, Math.max(...tot) * 1.12] }), yaxis: axis({ autorange: "reversed", ticks: "", showline: false, tickfont: small(narrow ? 11 : 12.5) }) });
  el.dataset.narrow = narrow;
}

/* benchmark horizons: latest observed and aligned to today */
function figHorizons(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, r = d.rows, y = r.map(q => q.name);
  const sx = [], sy = [];
  r.forEach(q => { sx.push(q.latest, q.today, null); sy.push(q.name, q.name, null); });
  const hov = r.map(q => [q.date, q.model, q.score, DUR(q.latest), DUR(q.today), q.grading, q.w, DUR(q.med)]);
  const traces = [
    { x: sx, y: sy, type: "scatter", mode: "lines", line: { color: C.rule2, width: 2 }, hoverinfo: "skip" },
    { x: r.map(q => q.med), y, type: "scatter", mode: "markers", marker: { symbol: "line-ns", size: 12, line: { color: C.ink3, width: 2 } },
      hovertemplate: "%{y}: median item %{x:.0f} min (our estimate)<extra></extra>" },
    { x: r.map(q => q.latest), y, type: "scatter", mode: "markers", marker: { size: 8, color: "#fffdf9", line: { color: C.ink3, width: 1.5 } },
      customdata: hov, hovertemplate: "<b>%{y}</b><br>Latest observed: %{customdata[3]} (%{customdata[1]}, %{customdata[0]}, score %{customdata[2]}%)<extra></extra>" },
    { x: r.map(q => q.today), y, type: "scatter", mode: "markers", marker: { size: 10, color: r.map(q => q.rho ? C.accent : C.a) },
      customdata: hov, hovertemplate: "<b>%{y}</b><br>Today: %{customdata[4]}<br>Grading: %{customdata[5]}<br>Share of pilot coded weight: %{customdata[6]}%<extra></extra>" },
  ];
  const ann = r.map(q => ({ xref: "paper", yref: "y", x: 1, y: q.name, xanchor: "left", xshift: 6, showarrow: false,
    text: q.w ? q.w + "%" : "–", font: { family: FONT, size: 11.5, color: C.ink2 } }));
  ann.push({ xref: "paper", yref: "paper", x: 1, y: 1, xanchor: "left", yanchor: "bottom", xshift: 2, showarrow: false, text: "weight", font: { family: FONT, size: 11, color: C.ink3 } });
  draw(el, traces, { height: 24 * r.length + 70, hovermode: "closest", margin: { l: narrow ? 128 : 150, r: 44, t: 18, b: 32 },
    xaxis: axis(Object.assign({ type: "log", range: [0.3, 4.6] }, LOGTICKS)), yaxis: axis({ type: "category", ticks: "", showline: false, tickfont: small(narrow ? 11 : 12.5) }),
    annotations: ann });
  el.dataset.narrow = narrow;
}

/* blind time estimates vs published */
function figTiming(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.2 : 0.1;
  const p1 = twoPanels(narrow, 0, gap), p2 = twoPanels(narrow, 1, gap);
  const lo = 3, hi = 2000, fx = [lo, hi], fy = fx.map(x => Math.exp(d.icpt) * Math.pow(x, d.slope));
  const blabel = b => b.hi === null ? ">" + b.lo + " min" : b.lo + "–" + b.hi + " min";
  const traces = [
    { x: fx, y: fx, type: "scatter", mode: "lines", line: { color: C.ink3, width: 1.5, dash: "dash" }, hoverinfo: "skip" },
    { x: fx, y: fy, type: "scatter", mode: "lines", line: { color: C.accent, width: 2 }, hoverinfo: "skip" },
    { x: d.tb.pub, y: d.tb.est, type: "scatter", mode: "markers", marker: { color: tint(C.accent, 0.7), size: 8, line: { color: "#fffdf9", width: 0.8 } },
      hovertemplate: "published %{x:.0f} min, estimated %{y:.0f} min<extra></extra>" },
    { x: d.swe.map(q => q.b + q.j), y: d.swe.map(q => q.est), xaxis: "x2", yaxis: "y2", type: "scatter", mode: "markers",
      marker: { color: tint(C.a, 0.7), size: 8, line: { color: "#fffdf9", width: 0.8 } }, hovertemplate: "estimated %{y:.0f} min<extra></extra>" },
  ];
  const shapes = d.buckets.map((b, i) => ({ type: "rect", xref: "x2", yref: "y2", x0: i - 0.4, x1: i + 0.4, y0: Math.max(b.lo, lo), y1: b.hi === null ? hi : b.hi,
    fillcolor: C.rule, opacity: 0.6, line: { width: 0 }, layer: "below" }));
  const lt = { tickvals: [5, 15, 60, 240, 960], ticktext: ["5 min", "15 min", "1 h", "4 h", "16 h"] };
  draw(el, traces, { height: narrow ? 600 : 330, hovermode: "closest", margin: { l: 56, r: 10, t: 30, b: 46 }, shapes,
    xaxis: axis(Object.assign({ domain: p1.x, anchor: "y", type: "log", range: [Math.log10(lo), Math.log10(hi)], title: { text: "Published time", font: small(12), standoff: 4 } }, lt)),
    yaxis: axis(Object.assign({ domain: p1.y, anchor: "x", type: "log", range: [Math.log10(lo), Math.log10(hi)], title: ytitle("Our estimate") }, lt)),
    xaxis2: axis({ domain: p2.x, anchor: "y2", range: [-0.6, d.buckets.length - 0.4], tickvals: d.buckets.map((_, i) => i), ticktext: d.buckets.map(blabel),
      title: { text: "Published bucket (shaded)", font: small(12), standoff: 4 } }),
    yaxis2: axis(Object.assign({ domain: p2.y, anchor: "x2", type: "log", range: [Math.log10(lo), Math.log10(hi)] }, lt)),
    annotations: [ptitle("", "Terminal-Bench 2"), ptitle("2", "SWE-bench Verified"),
      { xref: "x domain", yref: "y domain", x: 0.97, y: 0.04, xanchor: "right", showarrow: false, text: "slope " + d.slope.toFixed(2), font: { family: FONT, size: 12, color: C.accent } }] });
  el.dataset.narrow = narrow;
}

/* S over time, one line per occupation; horizons moved along the pooled trend */
function figTimeline(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, gap = narrow ? 0.16 : 0.07;
  const traces = [], ann = [], shapes = [];
  const lay = { hovermode: "closest", height: narrow ? 620 : 380, margin: { l: 46, r: 12, t: 26, b: 36 }, showlegend: false };
  [["1", "ρ = 1"], ["5", "ρ = 0.5 for test- and state-graded benchmarks"]].forEach(([r, nm], i) => {
    const k = i ? "2" : "", p = twoPanels(narrow, i, gap);
    d.series.forEach((q, j) => traces.push({ type: "scatter", mode: "lines", x: d.dates, y: q["S" + r], xaxis: "x" + k, yaxis: "y" + k,
      line: { color: q.col || OCC_COL[j % OCC_COL.length], width: q.col ? 3 : 2 }, name: q.name,
      hovertemplate: q.name + ", %{x|%b %Y}: S = %{y:.0f}%<extra></extra>" }));
    lay["xaxis" + k] = axis({ domain: p.x, anchor: "y" + k, type: "date", tickformat: "%b %Y", nticks: narrow ? 4 : 5 });
    lay["yaxis" + k] = axis({ domain: p.y, anchor: "x" + k, range: [0, 70], ticksuffix: "%", dtick: 10 });
    shapes.push({ type: "line", xref: "x" + k, yref: "y" + k + " domain", x0: d.today, x1: d.today, y0: 0, y1: 1,
      line: { color: C.muted || "#8a7d6d", width: 1, dash: "dot" } });
    ann.push(ptitle(k, nm));
    ann.push({ xref: "x" + k, yref: "y" + k + " domain", x: d.today, y: 0.98, xanchor: "right", showarrow: false,
      text: "today ", font: { family: FONT, size: 11, color: "#8a7d6d" } });
  });
  lay.annotations = ann; lay.shapes = shapes; draw(el, traces, lay); el.dataset.narrow = narrow;
}

const TREND_COL = ["#235fa6", "#b0702a", "#2f8a57", "#c0607e", "#8f68a6", "#ae8a2c", "#4fa3c7", "#5c5c5c"];
/* S for every occupation, grouped (dot plot); filled = rho 1, hollow = rho 0.5 */
function figGroups(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640, traces = [];
  const ys = d.rows.map(r => r.occ);
  Object.keys(d.labels).forEach(g => {
    const rs = d.rows.filter(r => r.g === g);
    if (!rs.length) return;
    traces.push({ type: "scatter", mode: "markers", y: rs.map(r => r.occ), x: rs.map(r => r.S5), name: d.labels[g] + ", ρ = 0.5",
      marker: { size: 9, color: "rgba(0,0,0,0)", line: { color: d.cols[g], width: 1.8 } }, showlegend: false,
      hovertemplate: "%{y}: S = %{x:.0f}%<extra>ρ = 0.5</extra>" });
    traces.push({ type: "scatter", mode: "markers", y: rs.map(r => r.occ), x: rs.map(r => r.S1), name: d.labels[g],
      marker: { size: 10, color: d.cols[g] }, hovertemplate: "%{y}: S = %{x:.0f}%<extra>ρ = 1</extra>" });
  });
  draw(el, traces, { hovermode: "closest", height: 60 + 19 * ys.length, margin: { l: narrow ? 128 : 150, r: 12, t: 8, b: 36 },
    showlegend: false,
    xaxis: axis({ range: [0, 60], ticksuffix: "%", dtick: 10 }),
    yaxis: axis({ type: "category", categoryarray: ys, categoryorder: "array", autorange: "reversed", ticks: "", tickfont: small(11.5) }) });
  el.dataset.narrow = narrow;
}

/* record-setting horizon by model release date, per benchmark (log scale) */
function figTrend(id, d) {
  const el = document.getElementById(id), narrow = W(el) < 640;
  const traces = d.series.map((q, j) => ({ type: "scatter", mode: "lines+markers", x: q.x, y: q.y, name: q.name, text: q.model,
    line: { color: TREND_COL[j % TREND_COL.length], width: 1.8, shape: "hv" }, marker: { size: 6, color: TREND_COL[j % TREND_COL.length] },
    hovertemplate: q.name + "<br>%{text}, %{x|%b %Y}: %{y:.0f} min<extra></extra>" }));
  draw(el, traces, { hovermode: "closest", height: narrow ? 460 : 400, margin: { l: 60, r: 12, t: 10, b: 36 },
    showlegend: true, legend: { orientation: "h", y: -0.14, font: small(11.5) },
    xaxis: axis({ type: "date", tickformat: "%b %Y" }),
    yaxis: axis(Object.assign({ type: "log" }, LOGTICKS)),
    shapes: [{ type: "line", xref: "x", yref: "paper", x0: d.today, x1: d.today, y0: 0, y1: 1, line: { color: "#8a7d6d", width: 1, dash: "dot" } }] });
  el.dataset.narrow = narrow;
}

const FIGS = { groups: figGroups, group_timeline: figTimeline, timeline: figTimeline, trend: figTrend, headline: figHeadline, bpo_headline: figHeadline, mechanism: figMechanism, dvs: figDvS, items: figItems, bpo_items: figItems,
  scenarios: figScenarios, types: figTypes, coverage: figCoverage, horizons: figHorizons, timing: figTiming };
const CHARTS = {};
Object.keys(DATA).forEach(k => { CHARTS["chart-" + k] = () => FIGS[k]("chart-" + k, DATA[k]); });
"""
JS_FIGS = {"groups", "group_timeline", "timeline", "trend", "headline", "bpo_headline", "mechanism", "dvs", "items", "bpo_items", "scenarios", "types", "coverage", "horizons", "timing"}

EXTRA_CSS = """
/* this page */
.imath { white-space: nowrap; }
.math .katex-display { margin: 0; }
table.itemlist { font-size: 13px; } table.itemlist td:nth-child(2) { text-align: left; min-width: 220px; }
table.itemlist td:nth-child(3), table.itemlist td:nth-child(4) { text-align: left; white-space: nowrap; }
table.itemlist th:nth-child(2), table.itemlist th:nth-child(3), table.itemlist th:nth-child(4) { text-align: left; }
table.itemlist th[scope="row"] { white-space: nowrap; }
table.text th, table.text td { text-align: left; }
.pending p:last-child { margin-bottom: 0; }
.pending { font-family: var(--sans); font-size: 15px; color: var(--ink-2); background: var(--panel); border: 1px dashed var(--rule-2);
  border-radius: 6px; padding: 10px 14px; }
"""


# ---------------------------------------------------------------- page

def main():
    args = sys.argv[1:]
    pilot = Run(args[0] if args else "pilot_v4c")
    bpo = None
    if len(args) > 1:
        p = DS / "coding" / "stage2" / args[1] / "delegable" / "items.csv"
        if p.exists():
            bpo = Run(args[1])
        else:
            print(f"BPO run {args[1]}: {p.relative_to(REPO)} not found; showing the in-progress note")
    extra = [Run(a) for a in args[2:] if (DS / "coding" / "stage2" / a / "delegable" / "items.csv").exists()]
    comp = extra[0] if extra else None

    raw = TEXT.read_text(encoding="utf-8")
    fm, body = raw[3:].split("\n---", 1)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    front = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in fm.strip().splitlines()))
    tok = tokens(pilot)
    tok["today_long"] = "10 November 2026"
    if bpo:  # a few BPO-wide numbers for the prose
        for sc, suf in [(BASE, ""), (RHO5, "5")]:
            vals = sorted((bpo.agg[(sc, o)]["S"], o) for o in bpo.occs)
            tok[f"bpo_S{suf}_lo"], tok[f"bpo_S{suf}_hi"] = pct(vals[0][0]), pct(vals[-1][0])
            if not suf:
                tok["bpo_top"], tok["bpo_bottom"] = vals[-1][1], vals[0][1]
        tok["bpo_n_occ"] = str(len(bpo.occs))
    unknown = sorted({k for k in re.findall(r"\{\{(\w+)\}\}", body + fm) if k != "repo" and k not in tok})
    assert not unknown, f"unknown tokens in page_text.md: {unknown}"
    sub = lambda s: re.sub(r"\{\{(\w+)\}\}", lambda m: m.group(0) if m.group(1) == "repo" else tok[m.group(1)], s)  # noqa: E731
    body = sub(body)
    notes = dict(re.findall(r"^\[\^([\w-]+)\]:\s*(.+)$", body, flags=re.M))

    data = {"headline": headline_data(pilot), "mechanism": mechanism_data(pilot), "dvs": dvs_data(pilot),
            "items": items_data(pilot), "scenarios": scenarios_data(pilot), "types": types_data(pilot),
            "coverage": coverage_data(pilot), "horizons": horizons_data(pilot), "timing": timing_data()}
    gentables = {"summary": lambda: gt_summary(pilot), "match": lambda: gt_match(pilot), "items": lambda: gt_items(pilot)}
    runs_all = [pilot] + ([bpo] if bpo else []) + extra
    groups = group_of(pilot, bpo, extra)
    data["groups"] = groups_data(runs_all, groups)
    data["group_timeline"] = group_timeline_data(runs_all, groups)
    data["timeline"] = timeline_data([pilot] + ([bpo] if bpo else []))
    data["trend"] = trend_data([pilot] + ([bpo] if bpo else []))
    if bpo:
        data["bpo_headline"] = headline_data(bpo)
        data["bpo_items"] = items_data(bpo)
        gentables["bpo_summary"] = lambda: gt_summary(bpo)

    repo = f'<a href="{REPO_URL}">{REPO_URL.replace("https://", "")}</a>'
    doc = Doc({"repo": repo}, notes, figure_shells(pilot, bpo, comp), gentables, bpo is not None)
    main_html = doc.render(body.splitlines())
    missing = [k for k in doc.order if k not in notes]
    assert not missing, f"undefined footnotes: {missing}"
    unused = [k for k in notes if k not in doc.order]
    assert not unused, f"unused footnotes: {unused}"
    notes_html = "".join(f'<li id="note-{k}">{doc.inl(notes[k])}</li>' for k in doc.order)
    runs = ", ".join(f"<code>{r.name}</code>" for r in [pilot, bpo] + extra if r)
    main_html += (f'<details class="app" id="notes"><summary>All notes</summary><div><ol class="notes">{notes_html}</ol></div></details>'
                  f'<p class="footer">Built from <code>delegable_share/page_text.md</code> and the CSVs of runs {runs} by '
                  '<code>delegable_share/scripts/build_page.py</code>.</p>')

    used = re.findall(r'id="chart-(\w+)"', main_html)
    assert len(used) == len(set(used)), "a chart appears twice"
    data = {k: v for k, v in data.items() if k in used}
    assert set(used) == set(data), f"charts without data: {set(used) - set(data)}"
    assert set(used) <= JS_FIGS, f"charts without a JS function: {set(used) - JS_FIGS}"

    by = [p.strip() for p in front["byline"].split("·")]
    byline = " · ".join(html.escape(p) for p in by[:-1]) + f' · <span class="tag">{html.escape(by[-1])}</span>'
    header = (f'<header><p class="crumbs">{CRUMBS}</p><h1>{doc.inl(front["title"])}</h1>'
              f'<p class="byline">{byline}</p><p class="thanks">{doc.inl(sub(front["thanks"]))}</p></header>')
    toc = toc_html(doc.toc, doc)

    tpl = TEMPLATE.read_text(encoding="utf-8")
    css = re.search(r"<style>\n(.*?)</style>", tpl, re.S).group(1)
    js_helpers = tpl[tpl.index("const C = {"):tpl.index("/* --- Fig 1")]
    js_wiring = tpl[tpl.index("const drawn = new Set();"):tpl.rindex("</script>")]
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(front["short"])}</title>
<meta name="description" content="{html.escape(front["description"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}{EXTRA_CSS}</style>
</head>
<body>
<div class="page">
{toc}
<main>
{header}<details class="toc-mobile"><summary>Contents</summary>{toc}</details>
{main_html}
</main>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.0/plotly.min.js"></script>
<script src="{KATEX}/katex.min.js"></script>
<script>
const DATA = {data_json};
{js_helpers}{CHART_JS}
if (window.katex) {{
  document.querySelectorAll(".math[data-tex]").forEach(el => katex.render(el.dataset.tex, el, {{ displayMode: true, throwOnError: false }}));
  document.querySelectorAll(".imath[data-tex]").forEach(el => katex.render(el.dataset.tex, el, {{ displayMode: false, throwOnError: false }}));
}}
{js_wiring}</script>
</body>
</html>
"""
    assert "MISSING NOTE" not in page
    assert "{{" not in main_html, "unreplaced token"
    OUT.write_text(page, encoding="utf-8")
    words = len(re.findall(r"\b\w[\w’'-]*\b", re.sub(r"<[^>]+>", " ", re.sub(r'data-tex="[^"]*"', "", main_html))))
    print(f"wrote {OUT.relative_to(REPO)} ({len(page) / 1024:.0f} KB); {len(doc.order)} notes; charts: {used}; "
          f"BPO: {'yes, ' + bpo.name if bpo else 'in progress'}; ~{words:,} words in the page body")
    for o in pilot.occs:
        a, b = pilot.agg[(BASE, o)], pilot.agg[(RHO5, o)]
        print(f"  {occ_short(o):18s} S {a['S']:.0%}/{b['S']:.0%}  D {a['D']:.0%}/{b['D']:.0%}  unc {a['unc']:.0%}")


if __name__ == "__main__":
    main()
