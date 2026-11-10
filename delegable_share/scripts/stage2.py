"""Stage 2 (work-item features): build briefs, run Terra, validate, combine best of three.

  python3 scripts/stage2.py build    <run> <units_csv>   # briefs for coders s1, s2 (Claude)
  python3 scripts/stage2.py terra    <run>               # coder t (GPT-6.1 Terra)
  python3 scripts/stage2.py validate <run>               # check all coders' outputs
  python3 scripts/stage2.py combine  <run>               # features.csv + SUMMARY.md

Only DISCRETE and LIVE_SERVICE parts are coded. Each coder gets all items in its own random
order, split into batches of ~17 that mix occupations. Files: coding/stage2/<run>/.
"""
import collections
import csv
import json
import math
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402

PROMPT = ROOT / "prompts" / "stage2_features.md"
CODERS = {"s1": "claude-sonnet (subagent)", "s2": "claude-sonnet (subagent)",
          "t": "gpt-6.1-terra"}
BATCH = 17
DOMAINS = {"software": 0.20, "computer_use": 0.12, "text": 0.25}  # kappa, SPEC §9 pilot values
ORD = ["low", "medium", "high"]
NUM = ["length_p10", "length_p50", "length_p90", "review_p10", "review_p50", "review_p90"]

WRAPPER = """You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  {out}
with one element per item, in the order given, each the output object
described in the instructions. Write nothing else to that file. Then reply
"done <n> items".
"""


def run_dir(run):
    return ROOT / "coding" / "stage2" / run


def prompt_parts():
    md = PROMPT.read_text()
    block = md[md.index("## Prompt"):md.index("## Worked examples")].split("```")[1].strip("\n")
    ex = md[md.index("## Worked examples"):md.index("## Changes from the spec")]
    ex = "\n".join(ex.splitlines()[1:]).strip()
    return block, ex


def item_text(r):
    return (f"[{r['item_id']}]\nOccupation: {r['occupation_title']}\n"
            f"Task statement: {r['task_statement']}\nPart: {r['part_text']}\n"
            f"Type: {r['type']}\nWork item: {r['work_item']}\nStart: {r['start']}\n"
            f"End: {r['end']}\nChecked by: {r['checked_by']}\n")


def body(items):
    block, ex = prompt_parts()
    return ("=== INSTRUCTIONS ===\n" + block +
            "\n\n=== WORKED EXAMPLES (other occupations) ===\n" + ex +
            "\n\n=== ITEMS ===\n" + "\n".join(item_text(r) for r in items))


def load_manifest(run):
    return json.loads((run_dir(run) / "manifest.json").read_text())


def main():
    cmd, run = sys.argv[1], sys.argv[2]
    d = run_dir(run)

    if cmd == "build":
        units = ROOT / sys.argv[3]
        items = [dict(r, item_id=f"{r['task_id']}{r['part_id']}")
                 for r in csv.DictReader(open(units)) if r["type"] in ("DISCRETE", "LIVE_SERVICE")]
        by_id = {r["item_id"]: r for r in items}
        n_b = math.ceil(len(items) / BATCH)
        manifest = {"run": run, "units": str(units.relative_to(ROOT)),
                    "prompt_header": PROMPT.read_text().splitlines()[0],
                    "items": list(by_id), "coders": {}}
        for i, c in enumerate(CODERS):
            ids = list(by_id)
            random.Random(1000 + i).shuffle(ids)
            batches = [ids[k::n_b] for k in range(n_b)]
            manifest["coders"][c] = {"model": CODERS[c], "batches": batches}
            (d / c).mkdir(parents=True, exist_ok=True)
            if c == "t":
                continue
            (d / "briefs").mkdir(exist_ok=True)
            for j, b in enumerate(batches):
                out = d / c / f"batch{j}.json"
                (d / "briefs" / f"{c}_batch{j}.md").write_text(
                    WRAPPER.format(out=out) + "\n" + body([by_id[x] for x in b]) + "\n")
        (d / "items.json").write_text(json.dumps(by_id, indent=1))
        (d / "manifest.json").write_text(json.dumps(manifest, indent=1))
        print(len(items), "items;", n_b, "batches per coder")

    elif cmd == "terra":
        m, by_id = load_manifest(run), json.loads((d / "items.json").read_text())
        before = spent()
        for j, b in enumerate(m["coders"]["t"]["batches"]):
            parsed, u = chat_json([{"role": "user", "content": body([by_id[x] for x in b]) +
                                    '\n\nReturn a JSON object {"items": [...]}, one element per '
                                    "item in the order given, each the output object described "
                                    "in the instructions."}],
                                  purpose=f"stage2 {run} t batch{j}")
            (d / "t" / f"batch{j}.json").write_text(json.dumps(parsed.get("items", []), indent=1))
            print("batch", j, len(parsed.get("items", [])), "items", u.get("completion_tokens"))
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")

    elif cmd == "validate":
        m, bad = load_manifest(run), []
        for c, info in m["coders"].items():
            for j, b in enumerate(info["batches"]):
                f = d / c / f"batch{j}.json"
                if not f.exists():
                    bad.append((c, j, "-", "missing"))
                    continue
                got = {str(x.get("item_id")): x for x in json.loads(f.read_text())}
                for iid in b:
                    x = got.get(iid)
                    if x is None:
                        bad.append((c, j, iid, "not coded"))
                        continue
                    try:
                        v = [float(x[k]) for k in NUM]
                    except (KeyError, TypeError, ValueError):
                        bad.append((c, j, iid, "missing or non-numeric number"))
                        continue
                    if not (0 < v[0] <= v[1] <= v[2]):
                        bad.append((c, j, iid, f"lengths not 0<p10<=p50<=p90: {v[:3]}"))
                    if min(v[3:]) < 0:
                        bad.append((c, j, iid, "negative review minutes"))
                    if x.get("domain") not in DOMAINS:
                        bad.append((c, j, iid, f"bad domain {x.get('domain')}"))
                    for k in ("stakes", "stakes_p90", "context"):
                        if x.get(k) not in ORD:
                            bad.append((c, j, iid, f"bad {k} {x.get(k)}"))
                    if x.get("stakes") in ORD and x.get("stakes_p90") in ORD and \
                            ORD.index(x["stakes_p90"]) < ORD.index(x["stakes"]):
                        bad.append((c, j, iid, "stakes_p90 below stakes"))
        for b in bad:
            print("PROBLEM", *b)
        print(len(bad), "problems")
        sys.exit(1 if bad else 0)

    elif cmd == "combine":
        m, by_id = load_manifest(run), json.loads((d / "items.json").read_text())
        codes = {c: {} for c in m["coders"]}
        for c, info in m["coders"].items():
            for j in range(len(info["batches"])):
                for x in json.loads((d / c / f"batch{j}.json").read_text()):
                    codes[c][str(x["item_id"])] = x
        rows, spread = [], collections.defaultdict(list)
        for iid, u in by_id.items():
            xs = [codes[c][iid] for c in m["coders"]]
            r = {"item_id": iid, "onetsoc_code": u["onetsoc_code"],
                 "occupation_title": u["occupation_title"], "task_id": u["task_id"],
                 "type": u["type"], "work_item": u["work_item"], "weight": u["weight"]}
            for k in NUM:
                vals = [float(x[k]) for x in xs]
                r[k] = statistics.median(vals)
                r[k + "_all"] = ";".join(f"{v:g}" for v in vals)
            # review line a + b*h through the three (median) points; a >= 0
            hs = [r["length_p10"], r["length_p50"], r["length_p90"]]
            rs = [r["review_p10"], r["review_p50"], r["review_p90"]]
            hm, rm = statistics.mean(hs), statistics.mean(rs)
            sxx = sum((h - hm) ** 2 for h in hs)
            b = sum((h - hm) * (x - rm) for h, x in zip(hs, rs)) / sxx if sxx else 0.0
            a = rm - b * hm
            if a < 0:  # refit through the origin
                a, b = 0.0, sum(h * x for h, x in zip(hs, rs)) / sum(h * h for h in hs)
            r["review_a"], r["review_b"] = round(a, 3), round(b, 4)
            lo = (rs[1] - rs[0]) / (hs[1] - hs[0]) if hs[1] > hs[0] else float("nan")
            hi = (rs[2] - rs[1]) / (hs[2] - hs[1]) if hs[2] > hs[1] else float("nan")
            r["review_slope_lo"], r["review_slope_hi"] = round(lo, 4), round(hi, 4)
            spread["review_b"].append(b)
            r["p50_ratio"] = round(max(float(x["length_p50"]) for x in xs) /
                                   min(float(x["length_p50"]) for x in xs), 2)
            spread["p50_ratio"].append(r["p50_ratio"])
            for k in ("stakes", "stakes_p90", "context"):
                idx = sorted(ORD.index(x[k]) for x in xs)
                r[k] = ORD[idx[1]]
                r[k + "_all"] = ";".join(x[k] for x in xs)
                spread[k + "_range"].append(idx[2] - idx[0])
            kap = sorted((DOMAINS[x["domain"]], x["domain"]) for x in xs)
            r["domain"], r["kappa"] = kap[1][1], kap[1][0]
            r["domain_all"] = ";".join(x["domain"] for x in xs)
            spread["domain_agree"].append(len({x["domain"] for x in xs}))
            r["two_groups_any"] = any(x.get("two_groups") for x in xs)
            r["unit_flags"] = sum(bool(x.get("unit_flag")) for x in xs)
            r["unit_flag_reasons"] = " | ".join(x.get("unit_flag_reason", "") for x in xs
                                                if x.get("unit_flag"))
            rows.append(r)
        with open(d / "features.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        # coder-level tendencies: median of log(coder p50 / combined p50)
        tend = {c: statistics.median(math.log(float(codes[c][r["item_id"]]["length_p50"]) /
                                              r["length_p50"]) for r in rows) for c in m["coders"]}
        n = len(rows)
        q = statistics.quantiles(spread["p50_ratio"], n=4)
        out = [f"# Stage 2 summary — {run}", "",
               f"{n} items × 3 coders ({', '.join(f'{c} = {v}' for c, v in CODERS.items())}). "
               "Combined: median of numbers and ordered categories; domain by median κ.", "",
               "## Spread between coders", "",
               f"- Median item length (p50), max/min across coders: median ratio "
               f"{statistics.median(spread['p50_ratio']):.2f}, quartiles {q[0]:.2f}–{q[2]:.2f}, "
               f"{sum(x > 3 for x in spread['p50_ratio'])} items above 3×.",
               f"- Stakes: all three agree on {spread['stakes_range'].count(0)}, within one step on "
               f"{spread['stakes_range'].count(1)}, two steps apart on "
               f"{spread['stakes_range'].count(2)}.",
               f"- Context: all agree {spread['context_range'].count(0)}, one step "
               f"{spread['context_range'].count(1)}, two steps {spread['context_range'].count(2)}.",
               f"- Domain: all agree {spread['domain_agree'].count(1)}, two agree "
               f"{spread['domain_agree'].count(2)}, three-way split "
               f"{spread['domain_agree'].count(3)}.",
               f"- Coder tendency in p50 length (median ratio to combined): " +
               ", ".join(f"{c} ×{math.exp(v):.2f}" for c, v in tend.items()) + ".",
               f"- Review line a + b·h (fit to the three median points): median b "
               f"{statistics.median(spread['review_b']):.3f}, quartiles "
               f"{statistics.quantiles(spread['review_b'], n=4)[0]:.3f}–"
               f"{statistics.quantiles(spread['review_b'], n=4)[2]:.3f}; median a "
               f"{statistics.median(r['review_a'] for r in rows):.1f} min. Slope short→typical vs "
               f"typical→long (medians): "
               f"{statistics.median(r['review_slope_lo'] for r in rows):.3f} vs "
               f"{statistics.median(r['review_slope_hi'] for r in rows):.3f}.",
               f"- Unit flags: {sum(r['unit_flags'] > 0 for r in rows)} items flagged by at least "
               f"one coder; {sum(r['two_groups_any'] for r in rows)} items with two groups noted.",
               "", "## Combined features by occupation (medians across items)", "",
               "| Occupation | Items | p50 min | p90 min | review p10 | stakes (L/M/H) | "
               "context (L/M/H) | domain (sw/cu/tx) |", "|---|---|---|---|---|---|---|---|"]
        by_occ = collections.defaultdict(list)
        for r in rows:
            by_occ[r["occupation_title"]].append(r)
        for o, rs in by_occ.items():
            cnt = lambda k, vals: "/".join(str(sum(r[k] == v for r in rs)) for v in vals)  # noqa
            out.append(f"| {o} | {len(rs)} | {statistics.median(r['length_p50'] for r in rs):g} | "
                       f"{statistics.median(r['length_p90'] for r in rs):g} | "
                       f"{statistics.median(r['review_p10'] for r in rs):g} | "
                       f"{cnt('stakes', ORD)} | {cnt('context', ORD)} | "
                       f"{cnt('domain', list(DOMAINS))} |")
        out += ["", "## Widest disagreements on length (p50 ratio > 3)", ""]
        for r in sorted(rows, key=lambda r: -r["p50_ratio"]):
            if r["p50_ratio"] > 3:
                out.append(f"- {r['item_id']} ({r['occupation_title']}): {r['work_item']} — "
                           f"p50 by coder {r['length_p50_all']} min")
        out += ["", "## Unit flags", ""] + [
            f"- {r['item_id']} ({r['unit_flags']}/3): {r['unit_flag_reasons']}"
            for r in rows if r["unit_flags"]]
        (d / "SUMMARY.md").write_text("\n".join(out) + "\n")
        print("\n".join(out[:22]))


if __name__ == "__main__":
    main()
