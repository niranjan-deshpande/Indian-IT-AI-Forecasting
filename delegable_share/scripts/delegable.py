"""Delegable share D per work item and per occupation (SPEC §2 with DECISIONS changes).

  python3 scripts/delegable.py <stage2_run> [units_csv]

Per coded item (DISCRETE or LIVE_SERVICE):
  item lengths ~ lognormal fitted to the coded p10/p50/p90 (percentiles across items, so the
  hours-weighted density g(h) is lognormal(mu + sigma^2, sigma));
  pi(h) = rho_b * sigma(beta * [ln H_b - ln(m h)]), H_b from benchmarks/horizons.csv;
  DISCRETE:      delegate if pi (1-kappa) h > a + b h                       (a, b: item's review line)
  LIVE_SERVICE:  delegate if pi (1-kappa) h > q (a + b h) + (1 - pi) lambda h
  D = share of g's hours where the rule holds.
INTERPERSONAL, PHYSICAL, NO_DELIVERABLE: D = 0. Best match "none", or a benchmark without a
horizon: D undetermined (reported as uncovered weight, not filled).

Outputs in coding/stage2/<run>/delegable/: items.csv (every scenario), RESULTS.md.
"""
import csv
import math
import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
M = {"low": 1.0, "medium": 3.0, "high": 10.0}
COMPRESSION = 0.37          # must match horizons.py; decompression widens spread, keeps p50
BASE = dict(hcol="H_today_min", months_ahead=0, variant="base", beta=0.84, rho_tests=1.0, q=0.03, lam=1.0, fallback=False, decomp=False)
SCENARIOS = {
    "base": {},
    "base, rho 0.5 (tests/state)": dict(rho_tests=0.5),
    "beta 0.6": dict(variant="beta_lo", beta=0.60),
    "beta 1.0": dict(variant="beta_hi", beta=1.00),
    "decompressed spread, both sides": dict(variant="base_decomp", decomp=True),
    "decompressed spread, benchmarks only": dict(variant="base_decomp"),
    "lambda 0.25": dict(lam=0.25),
    "lambda 3": dict(lam=3.0),
    "fill from 2nd match": dict(fallback=True),
    "latest observed H (no date alignment)": dict(hcol="H_now_min"),
    "+12 months (pooled trend)": dict(months_ahead=12),
}
NGRID = 401


def lognormal_fit(p10, p50, p90):
    mu = math.log(p50)
    sd = (math.log(p90) - math.log(p10)) / (2 * 1.2815516)
    return mu, max(sd, 0.05)


def item_D(f, H, rho, p):
    mu, sd = lognormal_fit(float(f["length_p10"]), float(f["length_p50"]), float(f["length_p90"]))
    if p["decomp"]:
        sd /= COMPRESSION
    mh = mu + sd * sd                      # hours-weighted
    a, b = float(f["review_a"]), float(f["review_b"])
    kap, m = float(f["kappa"]), M.get(f["context"], 3.0)
    live = f["type"] == "LIVE_SERVICE"
    lnH = math.log(H)
    tot = dsum = ssum = 0.0
    band = []
    for k in range(NGRID):
        z = -4 + 8 * k / (NGRID - 1)
        w = math.exp(-z * z / 2)
        lnh = mh + sd * z
        h = math.exp(lnh)
        x = p["beta"] * (lnH - lnh - math.log(m))
        pi = rho / (1 + math.exp(-x))
        gain = pi * (1 - kap) * h
        cost = p["q"] * (a + b * h) + (1 - pi) * p["lam"] * h if live else a + b * h
        tot += w
        if gain > cost:
            dsum += w
            ssum += w * (gain - cost) / h
            band.append(h)
    p50 = float(f["length_p50"])
    x50 = p["beta"] * (lnH - math.log(m * p50))
    return (dsum / tot, (round(min(band), 1), round(max(band), 1)) if band else ("", ""),
            rho / (1 + math.exp(-x50)), ssum / tot)


def main():
    run = sys.argv[1]
    units = ROOT / (sys.argv[2] if len(sys.argv) > 2 else "coding/stage1/v2_final/units_final.csv")
    d = ROOT / "coding" / "stage2" / run
    feats = {r["item_id"]: r for r in csv.DictReader(open(d / "features.csv"))}
    match = {r["item_id"]: r for r in csv.DictReader(open(d / "matches_final.csv"))}
    hz = defaultdict(dict)
    for r in csv.DictReader(open(ROOT / "benchmarks" / "horizons.csv")):
        hz[r["variant"]][r["benchmark"]] = r
    items = list(csv.DictReader(open(units)))
    out, agg = [], defaultdict(lambda: defaultdict(float))
    for sname, over in SCENARIOS.items():
        p = {**BASE, **over}
        for u in items:
            iid = u["task_id"] + u["part_id"]
            w, ts = float(u["weight"]), float(u["time_share"])
            row = {"scenario": sname, "item_id": iid, "occupation": u["occupation_title"],
                   "type": u["type"], "work_item": u["work_item"], "weight": w, "benchmark": "",
                   "H_min": "", "rho": "", "pi_at_p50": "", "D": "", "S": "", "band_lo_min": "", "band_hi_min": ""}
            if u["type"] in ("DISCRETE", "LIVE_SERVICE"):
                f, mt = feats[iid], match[iid]
                cands = [mt["best"]] + ([mt["second"]] if p["fallback"] else [])
                bm = next((c for c in cands if c and c != "none" and c in hz[p["variant"]]), None)
                if bm:
                    h = hz[p["variant"]][bm]
                    rho = p["rho_tests"] if h["grading"] in ("tests", "state") else 1.0
                    Hval = float(h[p["hcol"]]) * 2 ** (p["months_ahead"] / float(h["pooled_doubling_months"]))
                    D, band, pi50, S = item_D(f, Hval, rho, p)
                    row.update(benchmark=bm, H_min=round(Hval, 1), rho=rho, pi_at_p50=round(pi50, 3),
                               D=round(D, 4), S=round(S, 4), band_lo_min=band[0], band_hi_min=band[1])
                else:
                    row.update(benchmark=mt["best"] + " (no horizon)")
            else:
                row["D"] = row["S"] = 0.0
            out.append(row)
            g = agg[(sname, u["occupation_title"])]
            g["w"] += w
            g["eq"] += ts
            if row["D"] == "":
                g["w_unc"] += w
            else:
                g["wD"] += w * row["D"]
                g["wS"] += w * row["S"]
                g["w_det"] += w
                g["eqD"] += ts * row["D"]
                g["eq_det"] += ts
                if u["type"] == "LIVE_SERVICE":
                    g["wD_live"] += w * row["D"]
    od = d / "delegable"
    od.mkdir(exist_ok=True)
    with open(od / "items.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(out[0]))
        wr.writeheader()
        wr.writerows(out)
    occs = sorted({u["occupation_title"] for u in items})
    md = [f"# Delegable shares — {run}", "",
          "D̄ = importance-weighted mean of D over items with a horizon (interpersonal, physical and "
          "no-deliverable items count as 0). Uncovered = share of weight whose matched benchmark has "
          "no horizon (or no match); it is excluded, not filled. S = expected net hours saved by "
          "delegating (gain minus review, and minus failure cost for live items), as a share of the "
          "item's unassisted hours, over the hours where delegation pays.", "",
          "Headline measure: S; D alongside. Headline rows: the first two (ρ = 1, and ρ = 0.5 for benchmarks graded by tests or state "
          "checks). Other rows vary one setting from the first row.", "",
          "| Scenario | " + " | ".join(occs) + " |", "|---|" + "---|" * len(occs)]
    for sname in SCENARIOS:
        cells = []
        for o in occs:
            g = agg[(sname, o)]
            dbar = g["wD"] / g["w_det"] if g["w_det"] else float("nan")
            cells.append(f"S {g['wS'] / g['w_det']:.0%} · D {dbar:.0%} (eq D {g['eqD'] / g['eq_det']:.0%}; "
                         f"unc {g['w_unc'] / g['w']:.0%})" if g["w_det"] else "n/a")
        md.append(f"| {sname} | " + " | ".join(cells) + " |")
    md += ["", "## Items (base scenario)", "",
           "| item | type | work item | w | benchmark | H (min) | π at p50 | D | S | delegated lengths (min) |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in out:
        if r["scenario"] == "base" and r["type"] in ("DISCRETE", "LIVE_SERVICE"):
            md.append(f"| {r['item_id']} | {r['type'][:4]} | {r['work_item'][:60]} | {r['weight']:.2f} | "
                      f"{r['benchmark']} | {r['H_min']} | {r['pi_at_p50']} | {r['D']} | {r['S']} | "
                      f"{r['band_lo_min']}–{r['band_hi_min']} |")
    (od / "RESULTS.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:6 + len(SCENARIOS)]))


if __name__ == "__main__":
    main()
