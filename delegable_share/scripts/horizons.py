"""Fit benchmark horizons with a fixed slope: location only, from overall scores.

  python3 scripts/horizons.py <bench_times_run> [--today YYYY-MM-DD]

For each benchmark b and model j with overall score s_j, solve for H_bj in

    mean_i  sigma(beta * (ln H - ln t_i)) = s_j

where t_i are our coders' estimated human times for a random sample of b's items (median of the
three coders, coding/bench_times/<run>/estimates.csv). beta is fixed (DECISIONS 2026-11-09).
Variants: beta in BETAS, and "decompressed" times: log times stretched by 1/COMPRESSION around the
benchmark's own median (spread widened, level kept), the sensitivity for the coders' compression.

Snapshot horizon H_b(today) = the largest H among models released on or before today (frontier).
Trend: OLS of ln H on release date over frontier models (models that beat every earlier H).

Inputs:  benchmarks/data/<b>/scores.csv, benchmarks/data/grading.json
Outputs: benchmarks/horizons_fits.csv (every model x variant), benchmarks/horizons.csv
         (snapshot + trend per benchmark x variant), benchmarks/HORIZONS.md
"""
import csv
import datetime as dt
import json
import math
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BETAS = {"base": 0.84, "beta_lo": 0.60, "beta_hi": 1.00}
COMPRESSION = 0.37   # slope of log(estimate) on log(published), validation run


def stretch(t, on, centre):
    if not on:
        return t
    c = math.log(centre)
    return math.exp(c + (math.log(t) - c) / COMPRESSION)


def solve_lnH(lt, s, beta):
    s = min(max(s, 0.005), 0.995)
    f = lambda x: statistics.fmean(1 / (1 + math.exp(-beta * (x - l))) for l in lt) - s
    lo, hi = min(lt) - 40 / beta, max(lt) + 40 / beta
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return (lo + hi) / 2


def ordinal(d):
    return dt.date.fromisoformat(d).toordinal()


def main():
    run = sys.argv[1]
    today = sys.argv[sys.argv.index("--today") + 1] if "--today" in sys.argv else "2026-11-09"
    est = ROOT / "coding" / "bench_times" / run / "estimates.csv"
    times = {}
    for r in csv.DictReader(open(est)):
        times.setdefault(r["benchmark"].replace("-", "_"), []).append(float(r["est_median"]))
    grading = json.loads((ROOT / "benchmarks" / "data" / "grading.json").read_text())
    fits, snap = [], []
    for b, ts in sorted(times.items()):
        sc = ROOT / "benchmarks" / "data" / b / "scores.csv"
        if not sc.exists():
            continue
        rows = [r for r in csv.DictReader(open(sc)) if r.get("score") not in (None, "")]
        for vname, beta in BETAS.items():
            for dec in (False, True):
                v = vname + ("_decomp" if dec else "")
                lt = [math.log(stretch(t, dec, statistics.median(ts))) for t in ts]
                pts = []
                for r in rows:
                    s = float(r["score"])
                    s = s / 100 if s > 1 else s
                    lnH = solve_lnH(lt, s, beta)
                    d = ((r.get("release_date") or "").strip() or (r.get("eval_date") or "").strip())[:10]
                    d = d if len(d) == 10 else (d + "-15" if len(d) == 7 else "")
                    fits.append({"benchmark": b, "variant": v, "model": r["model"], "release_date": d,
                                 "score": round(s, 4), "H_min": round(math.exp(lnH), 2)})
                    if d:
                        pts.append((d, lnH, r["model"], s))
                pts = [p for p in pts if p[0] <= today]
                if not pts:
                    continue
                pts.sort()
                front, best = [], -1e9
                for p in pts:
                    if p[1] > best:
                        front.append(p)
                        best = p[1]
                top = max(pts, key=lambda p: p[1])
                dbl = ""
                if len(front) >= 3:
                    xs = [ordinal(p[0]) for p in front]
                    ys = [p[1] for p in front]
                    mx, my = statistics.fmean(xs), statistics.fmean(ys)
                    sxx = sum((x - mx) ** 2 for x in xs)
                    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0
                    if slope > 0:
                        dbl = round(math.log(2) / slope / 30.44, 1)
                snap.append({"benchmark": b, "variant": v, "beta": beta, "n_items": len(ts),
                             "item_median_min": round(statistics.median(ts), 1),
                             "H_now_min": round(math.exp(top[1]), 2), "H_now_model": top[2],
                             "H_now_date": top[0], "H_now_score": round(top[3], 3),
                             "n_models": len(pts), "n_frontier": len(front),
                             "doubling_months": dbl, "grading": grading.get(b, "")})
    # Align to a common date: move each benchmark's latest frontier H forward to `today` with the
    # pooled doubling time (median over benchmarks with >= 4 frontier points and 1-36 months).
    for v in {r["variant"] for r in snap}:
        dbls = [r["doubling_months"] for r in snap if r["variant"] == v and r["n_frontier"] >= 4
                and r["doubling_months"] and 1 <= r["doubling_months"] <= 36]
        pooled = statistics.median(dbls) if dbls else 7.0
        for r in snap:
            if r["variant"] == v:
                age = (ordinal(today) - ordinal(r["H_now_date"])) / 30.44
                r["pooled_doubling_months"] = round(pooled, 1)
                r["age_months"] = round(age, 1)
                r["H_today_min"] = round(r["H_now_min"] * 2 ** (age / pooled), 2)
    out = ROOT / "benchmarks"
    for name, rows in (("horizons_fits.csv", fits), ("horizons.csv", snap)):
        with open(out / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    base = [r for r in snap if r["variant"] == "base"]
    md = ["# Benchmark horizons (fixed β = 0.84/ln; location from overall scores)", "",
          f"Item times: coders' median estimates, run `{run}`. Snapshot = best model released by {today}.",
          "Doubling = OLS on frontier models (blank if fewer than 3 frontier points or no growth).",
          f"H today = H latest moved forward to {today} at the pooled doubling time "
          f"({base[0]['pooled_doubling_months'] if base else ''} months; median over benchmarks with >= 4 frontier points).", "",
          "| Benchmark | grading | items | median item (min) | H latest (min) | model (date, score) | models | own doubling (months) | H today (min) | β 0.6 / 1.0 (today) | decompressed (today) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in base:
        alt = {x["variant"]: x["H_today_min"] for x in snap if x["benchmark"] == r["benchmark"]}
        md.append(f"| {r['benchmark']} | {r['grading']} | {r['n_items']} | {r['item_median_min']} | "
                  f"{r['H_now_min']} | {r['H_now_model']} ({r['H_now_date']}, {r['H_now_score']}) | "
                  f"{r['n_models']} | {r['doubling_months']} | {r['H_today_min']} | {alt.get('beta_lo')} / {alt.get('beta_hi')} | "
                  f"{alt.get('base_decomp')} |")
    (out / "HORIZONS.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
