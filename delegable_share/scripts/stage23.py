"""Stages 2+3 combined: features + benchmark match in one pass.

  python3 scripts/stage23.py build   <run> <units_csv>  # briefs for s1, s2 (Claude), manifest
  python3 scripts/stage23.py terra   <run>              # coder t (GPT-6.1 Terra)
  python3 scripts/stage23.py check   <run>              # validate match fields
  python3 scripts/stage23.py matches <run>              # combine matches -> matches.csv, MATCHES.md
  python3 scripts/stage23.py priming <run> <runA> <runB> # features vs two separate-stage runs

Features are validated and combined with stage2.py (validate / combine) on the same run dir:
coding/stage2/<run>/. Batches: ~34 items (2 per coder), to limit Claude subagent overhead.
"""
import collections
import csv
import json
import math
import pathlib
import random
import re
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402
from stage2 import CODERS, WRAPPER, item_text, prompt_parts  # noqa: E402

COMBINED = ROOT / "prompts" / "stage23_combined.md"
CATALOG = ROOT / "benchmarks" / "stage3_catalog_draft.md"
BATCH = int(__import__("os").environ.get("BATCH", 34))
TIER_A = {"metr_th", "swe_bench_verified", "multi_swe_bench", "terminal_bench_2",
          "vals_finance_agent", "osworld_2", "cybench"}
RATING = ["none", "partial", "good"]


def catalog(seed):
    """Catalog text without human times or internal notes; groups and entries shuffled."""
    text = CATALOG.read_text()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    groups = re.split(r"\n## ", text.split("---", 1)[1])
    rng = random.Random(seed)
    out, ids = [], []
    parsed = []
    for g in groups:
        g = g.strip()
        if not g:
            continue
        title, rest = g.split("\n", 1)
        entries = [e.strip() for e in re.split(r"\n(?=\*\*`)", rest) if e.strip().startswith("**`")]
        entries = ["\n".join(l for l in e.splitlines() if not l.startswith("*Human time"))
                   for e in entries]
        ids += re.findall(r"\*\*`([^`]+)`", rest)
        parsed.append((title.strip("# "), entries))
    rng.shuffle(parsed)
    for title, entries in parsed:
        rng.shuffle(entries)
        out.append(f"## {title}\n\n" + "\n\n".join(entries))
    return "\n\n".join(out), ids


def body(items, seed):
    block, _ = prompt_parts()
    md = COMBINED.read_text()
    match = md.split("## Match instructions")[1].split("```")[1].strip("\n")
    ex = md[md.index("## Worked examples"):]
    ex = "\n".join(ex.splitlines()[1:]).strip()
    cat, _ = catalog(seed)
    return ("=== INSTRUCTIONS ===\n" + block + "\n\n" + match +
            "\n\n=== WORKED EXAMPLES (other occupations) ===\n" + ex +
            "\n\n=== BENCHMARK LIST ===\n" + cat +
            "\n\n=== ITEMS ===\n" + "\n".join(item_text(r) for r in items))


def d(run):
    return ROOT / "coding" / "stage2" / run


def main():
    cmd, run = sys.argv[1], sys.argv[2]
    rd = d(run)
    if cmd == "build":
        units = ROOT / sys.argv[3]
        items = [dict(r, item_id=f"{r['task_id']}{r['part_id']}")
                 for r in csv.DictReader(open(units)) if r["type"] in ("DISCRETE", "LIVE_SERVICE")]
        by_id = {r["item_id"]: r for r in items}
        n_b = math.ceil(len(items) / BATCH)
        manifest = {"run": run, "units": str(units.relative_to(ROOT)), "combined": True,
                    "prompt_header": COMBINED.read_text().splitlines()[0], "items": list(by_id),
                    "coders": {}}
        for i, c in enumerate(CODERS):
            ids = list(by_id)
            random.Random(2000 + i).shuffle(ids)
            batches = [ids[k::n_b] for k in range(n_b)]
            manifest["coders"][c] = {"model": CODERS[c], "batches": batches, "catalog_seed": 3000 + i}
            (rd / c).mkdir(parents=True, exist_ok=True)
            if c == "t":
                continue
            (rd / "briefs").mkdir(exist_ok=True)
            for j, b in enumerate(batches):
                (rd / "briefs" / f"{c}_batch{j}.md").write_text(
                    WRAPPER.format(out=rd / c / f"batch{j}.json") + "\n" +
                    body([by_id[x] for x in b], 3000 + i) + "\n")
        (rd / "items.json").write_text(json.dumps(by_id, indent=1))
        (rd / "manifest.json").write_text(json.dumps(manifest, indent=1))
        print(len(items), "items;", n_b, "batches per coder")

    elif cmd == "terra":
        m, by_id = json.loads((rd / "manifest.json").read_text()), json.loads((rd / "items.json").read_text())
        info, before = m["coders"]["t"], spent()
        from concurrent.futures import ThreadPoolExecutor

        def one(jb):
            j, b = jb
            if (rd / "t" / f"batch{j}.json").exists():  # resumable
                return j, None, {}
            parsed, u = chat_json([{"role": "user", "content": body([by_id[x] for x in b],
                                                                     info["catalog_seed"]) +
                                    '\n\nReturn a JSON object {"items": [...]}, one element per '
                                    "item in the order given, each the output object described "
                                    "in the instructions (feature fields, then match fields)."}],
                                  purpose=f"stage23 {run} t batch{j}")
            (rd / "t" / f"batch{j}.json").write_text(json.dumps(parsed.get("items", []), indent=1))
            return j, len(parsed.get("items", [])), u
        with ThreadPoolExecutor(6) as ex:
            for j, n, u in ex.map(one, enumerate(info["batches"])):
                print("batch", j, n, "items", u.get("completion_tokens"))
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")

    elif cmd in ("check", "matches"):
        m = json.loads((rd / "manifest.json").read_text())
        _, ids = catalog(0)
        valid = set(ids) | {"none"}
        codes, bad = {c: {} for c in m["coders"]}, []
        for c, info in m["coders"].items():
            for j in range(len(info["batches"])):
                for x in json.loads((rd / c / f"batch{j}.json").read_text()):
                    iid = str(x["item_id"])
                    codes[c][iid] = x
                    for k in ("best", "second"):
                        if x.get(k) not in valid:
                            bad.append((c, iid, f"{k} not in catalog: {x.get(k)}"))
                        if x.get(k + "_match") not in RATING:
                            bad.append((c, iid, f"bad {k}_match {x.get(k + '_match')}"))
                        if (x.get(k) == "none") != (x.get(k + "_match") == "none"):
                            if k == "best":
                                bad.append((c, iid, "best and best_match disagree on none"))
                            else:  # tolerated: such a second choice is treated as none
                                print("WARN", c, iid, "second and second_match disagree; treated as none")
        if cmd == "check":
            for b in bad:
                print("PROBLEM", *b)
            print(len(bad), "problems")
            sys.exit(1 if bad else 0)
        by_id = json.loads((rd / "items.json").read_text())
        rows, split = [], []
        for iid, u in by_id.items():
            xs = [codes[c][iid] for c in m["coders"]]
            votes = collections.Counter(x["best"] for x in xs)
            top, n = votes.most_common(1)[0]
            if n == 1:
                split.append(iid)
                best, rating = "UNRESOLVED", "none"
            else:
                best = top
                rating = RATING[min(RATING.index(x["best_match"]) for x in xs if x["best"] == top)]
            sv = collections.Counter(x["second"] for x in xs if x["second"] != best
                                     and x["second"] != "none" and x.get("second_match") != "none")
            second = sv.most_common(1)[0][0] if sv else "none"
            rows.append({"item_id": iid, "onetsoc_code": u["onetsoc_code"],
                         "occupation_title": u["occupation_title"], "type": u["type"],
                         "work_item": u["work_item"], "weight": u["weight"],
                         "best": best, "best_match": rating, "votes": n,
                         "best_all": ";".join(f"{x['best']}:{x['best_match']}" for x in xs),
                         "second": second, "tier": "A" if best in TIER_A else
                         ("-" if best in ("none", "UNRESOLVED") else "B"),
                         "differences": " | ".join(x.get("best_difference", "") for x in xs
                                                   if x["best"] == best and x.get("best_difference"))})
        with open(rd / "matches.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        out = [f"# Benchmark matches — {run}", "",
               "Plurality of three coders; rating = lowest among coders who chose the winner. "
               "Weights are O*NET importance × time share (coded items only).", "",
               f"Agreement on best: all three {sum(r['votes'] == 3 for r in rows)}, two "
               f"{sum(r['votes'] == 2 for r in rows)}, three-way split {len(split)} "
               f"(to adjudicate: {', '.join(split) or 'none'}).", "",
               "## Coverage by occupation (share of coded weight)", "",
               "| Occupation | good | partial | none / split | of which Tier A (good+partial) |",
               "|---|---|---|---|---|"]
        by_occ = collections.defaultdict(list)
        for r in rows:
            by_occ[r["occupation_title"]].append(r)
        for o, rs in by_occ.items():
            tot = sum(float(r["weight"]) for r in rs)
            s = lambda f: 100 * sum(float(r["weight"]) for r in rs if f(r)) / tot  # noqa: E731
            out.append(f"| {o} | {s(lambda r: r['best_match'] == 'good'):.0f}% | "
                       f"{s(lambda r: r['best_match'] == 'partial'):.0f}% | "
                       f"{s(lambda r: r['best_match'] == 'none'):.0f}% | "
                       f"{s(lambda r: r['tier'] == 'A' and r['best_match'] != 'none'):.0f}% |")
        out += ["", "## Matched weight by benchmark (good + partial)", "",
                "| Benchmark | Tier | Items | Share of all coded weight |", "|---|---|---|---|"]
        allw = sum(float(r["weight"]) for r in rows)
        bw = collections.defaultdict(lambda: [0, 0.0])
        for r in rows:
            if r["best_match"] != "none":
                bw[r["best"]][0] += 1
                bw[r["best"]][1] += float(r["weight"])
        for b, (n, w) in sorted(bw.items(), key=lambda x: -x[1][1]):
            out.append(f"| {b} | {'A' if b in TIER_A else 'B'} | {n} | {100 * w / allw:.0f}% |")
        (rd / "MATCHES.md").write_text("\n".join(out) + "\n")
        print("\n".join(out))

    elif cmd == "adjudicate":
        # Opus brief for three-way splits on best match (the only adjudicated case).
        m = json.loads((rd / "manifest.json").read_text())
        by_id = json.loads((rd / "items.json").read_text())
        rows = list(csv.DictReader(open(rd / "matches.csv")))
        split = [r["item_id"] for r in rows if r["best"] == "UNRESOLVED"]
        codes = {}
        for c, info in m["coders"].items():
            for j in range(len(info["batches"])):
                for x in json.loads((rd / c / f"batch{j}.json").read_text()):
                    codes.setdefault(str(x["item_id"]), []).append(x)
        md = COMBINED.read_text()
        match = md.split("## Match instructions")[1].split("```")[1].strip("\n")
        cat, _ = catalog(0)
        out = rd / "adjudicated.json"
        blocks = []
        for iid in split:
            v = "\n".join(f"  Coder {n + 1}: best {x['best']} ({x['best_match']}); second "
                          f"{x['second']} ({x['second_match']}). Reasoning: {x['match_reasoning']}"
                          for n, x in enumerate(codes[iid]))
            blocks.append(item_text(by_id[iid]) + "Three coders' verdicts:\n" + v + "\n")
        (rd / "adjudicate.md").write_text(
            "You are the final adjudicator in a research pipeline. Use only this file: read no "
            "other file and do not search the web.\nThree coders matched each work item below to "
            "a benchmark, following the instructions below, and all three chose differently. "
            "Make the final call for each item.\n"
            f"Write ONE JSON array to:\n  {out}\nwith one element per item: "
            '{"item_id", "reasoning", "best", "best_match", "best_difference"}. Write nothing '
            'else to that file. Then reply "done <n> items".\n\n=== INSTRUCTIONS ===\n' + match +
            "\n\n=== BENCHMARK LIST ===\n" + cat + "\n\n=== ITEMS ===\n" + "\n".join(blocks))
        print(len(split), "items to adjudicate ->", rd / "adjudicate.md")

    elif cmd == "apply_adj":
        rows = list(csv.DictReader(open(rd / "matches.csv")))
        adj = {str(x["item_id"]): x for x in json.loads((rd / "adjudicated.json").read_text())}
        for r in rows:
            if r["item_id"] in adj:
                a = adj[r["item_id"]]
                r["best"], r["best_match"] = a["best"], a["best_match"]
                r["tier"] = "A" if a["best"] in TIER_A else ("-" if a["best"] == "none" else "B")
                r["differences"] = "adjudicated: " + a.get("best_difference", "")
        with open(rd / "matches_final.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(len(adj), "adjudicated ->", rd / "matches_final.csv")

    elif cmd == "priming":
        A, B = sys.argv[3], sys.argv[4]
        load = lambda r: {x["item_id"]: x for x in csv.DictReader(open(d(r) / "features.csv"))}  # noqa
        F, FA, FB = load(run), load(A), load(B)
        out = [f"# Priming check: {run} (combined) vs {A}, {B} (separate stages)", "",
               "Signed shift = median log ratio (positive: combined run gives larger values). "
               "Spread = median |log ratio|. The A-vs-B column is the noise between two "
               "separate-stage runs.", "",
               f"| Feature | {run} vs {B}: shift | spread | {run} vs {A}: shift | spread | "
               f"{B} vs {A}: shift | spread |", "|---|---|---|---|---|---|---|"]
        for k in ["length_p10", "length_p50", "length_p90", "review_p10", "review_p50"]:
            cells = []
            for X, Y in ((F, FB), (F, FA), (FB, FA)):
                lr = [math.log(float(X[i][k]) / float(Y[i][k])) for i in X
                      if i in Y and k in Y[i] and float(X[i][k]) > 0 and float(Y[i][k]) > 0]
                cells += [f"×{math.exp(statistics.median(lr)):.2f}",
                          f"×{math.exp(statistics.median(abs(v) for v in lr)):.2f}"]
            out.append(f"| {k} | " + " | ".join(cells) + " |")
        for k in ["stakes", "context", "domain"]:
            cells = []
            for X, Y in ((F, FB), (F, FA), (FB, FA)):
                same = sum(X[i][k] == Y[i][k] for i in X if i in Y)
                cells += [f"{same}/{len(X)} same", ""]
            out.append(f"| {k} | " + " | ".join(cells) + " |")
        (d(run) / "PRIMING.md").write_text("\n".join(out) + "\n")
        print("\n".join(out))


if __name__ == "__main__":
    main()
