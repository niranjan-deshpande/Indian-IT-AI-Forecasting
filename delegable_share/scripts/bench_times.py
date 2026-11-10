"""Estimate human times for benchmark items (blind), and score against published times.

  python3 scripts/bench_times.py build <run> <items.jsonl> [anchors.jsonl]  # briefs for s1, s2
  python3 scripts/bench_times.py terra <run>                # coder t (GPT-6.1 Terra)
  python3 scripts/bench_times.py score <run>                # SCORE.md + estimates.csv
  python3 scripts/bench_times.py collect <run>              # estimates.csv only (no published times)
Env N_BATCH (default 2) sets batches per coder at build time.

Files: coding/bench_times/<run>/. Prompt: prompts/benchmark_times.md.
"""
import csv
import json
import math
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402

PROMPT = ROOT / "prompts" / "benchmark_times.md"
CODERS = {"s1": "claude-sonnet (subagent)", "s2": "claude-sonnet (subagent)",
          "t": "gpt-6.1-terra"}
N_BATCH = int(__import__('os').environ.get('N_BATCH', 2))
WRAPPER = """You are a coder in a research pipeline. Follow the instructions below exactly.
Use only the information in this file. Do not read any other files and do not
search the web. Estimate each ITEM independently, in the order given.

Write ONE JSON array to:
  {out}
with one element per item, in the order given. Write nothing else to that
file. Then reply "done <n> items".
"""


def prompt_and_descr():
    md = PROMPT.read_text()
    block = md.split("## Prompt")[1].split("```")[1].strip("\n")
    descr, key = {}, None
    for line in md.split("## Benchmark descriptions shown to coders")[1].split("##")[0].splitlines():
        if line.startswith("- `"):
            key, v = line[3:].split("`: ", 1)
            descr[key] = v.strip()
        elif key and line.startswith("  ") and line.strip():
            descr[key] += " " + line.strip()  # continuation of a wrapped bullet
        else:
            key = None
    return block, descr


ANCHOR_INTRO = """=== REFERENCE ITEMS (already timed; do not estimate these) ===
These items from the same kinds of benchmark have known times. Use them to
calibrate your scale: work like this ranges from a few minutes to more than
a day, and long items can take many hours. Compare each item you estimate
with the reference items before giving a number.
"""


def anchor_block(anchors):
    _, descr = prompt_and_descr()
    return ANCHOR_INTRO + "\n".join(
        f"[reference] Benchmark: {descr[a['benchmark'].replace('-', '_').replace('terminal_bench_2.0', 'terminal_bench_2')]}\n"
        f"Item text:\n{a['text']}\nKnown time: {a['label']}\n" for a in anchors)


def body(items, anchors=None):
    block, descr = prompt_and_descr()
    parts = [f"[{it['item_id']}]\nBenchmark: {descr[it['benchmark'].replace('-', '_').replace('terminal_bench_2.0', 'terminal_bench_2')]}\n"
             f"Item text:\n{it['text']}\n" for it in items]
    ref = ("\n\n" + anchor_block(anchors)) if anchors else ""
    return "=== INSTRUCTIONS ===\n" + block + ref + "\n\n=== ITEMS ===\n" + "\n".join(parts)


def main():
    cmd, run = sys.argv[1], sys.argv[2]
    d = ROOT / "coding" / "bench_times" / run
    if cmd == "build":
        items = [json.loads(l) for l in open(ROOT / sys.argv[3]) if l.strip()]
        by_id = {it["item_id"]: it for it in items}
        anchors = ([json.loads(l) for l in open(ROOT / sys.argv[4]) if l.strip()]
                   if len(sys.argv) > 4 else None)
        manifest = {"run": run, "items_file": sys.argv[3],
                    "anchors_file": sys.argv[4] if anchors else None, "coders": {}}
        for i, c in enumerate(CODERS):
            ids = list(by_id)
            random.Random(4000 + i).shuffle(ids)
            batches = [ids[k::N_BATCH] for k in range(N_BATCH)]
            manifest["coders"][c] = {"model": CODERS[c], "batches": batches}
            (d / c).mkdir(parents=True, exist_ok=True)
            if c == "t":
                continue
            (d / "briefs").mkdir(exist_ok=True)
            for j, b in enumerate(batches):
                (d / "briefs" / f"{c}_batch{j}.md").write_text(
                    WRAPPER.format(out=d / c / f"batch{j}.json") + "\n" +
                    body([by_id[x] for x in b], anchors) + "\n")
        (d / "items.json").write_text(json.dumps(by_id, indent=1))
        (d / "manifest.json").write_text(json.dumps(manifest, indent=1))
        print(len(items), "items;", N_BATCH, "batches per coder")
    elif cmd == "terra":
        m, by_id = json.loads((d / "manifest.json").read_text()), json.loads((d / "items.json").read_text())
        anchors = ([json.loads(l) for l in open(ROOT / m["anchors_file"]) if l.strip()]
                   if m.get("anchors_file") else None)
        before = spent()
        from concurrent.futures import ThreadPoolExecutor

        def one(jb):
            j, b = jb
            parsed, u = chat_json([{"role": "user", "content": body([by_id[x] for x in b], anchors) +
                                    '\n\nReturn a JSON object {"items": [...]}, one element per '
                                    "item in the order given."}], purpose=f"bench_times {run} t{j}")
            (d / "t" / f"batch{j}.json").write_text(json.dumps(parsed.get("items", []), indent=1))
            return j, len(parsed.get("items", [])), u
        with ThreadPoolExecutor(6) as ex:
            for j, n, u in ex.map(one, enumerate(m["coders"]["t"]["batches"])):
                print("batch", j, n, u.get("completion_tokens"))
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")
    elif cmd == "collect":
        m, by_id = json.loads((d / "manifest.json").read_text()), json.loads((d / "items.json").read_text())
        est = {c: {} for c in m["coders"]}
        for c, info in m["coders"].items():
            for j in range(len(info["batches"])):
                fp = d / c / f"batch{j}.json"
                for x in (json.loads(fp.read_text()) if fp.exists() else []):
                    est[c][str(x["item_id"])] = float(x["estimate_min"])
        rows, missing = [], []
        for iid, it in by_id.items():
            vals = [est[c].get(iid) for c in m["coders"]]
            ok = [v for v in vals if v and v > 0]
            if len(ok) < len(vals):
                missing.append((iid, [c for c, v in zip(m["coders"], vals) if not v or v <= 0]))
            if len(ok) >= 2:
                rows.append({"item_id": iid, "benchmark": it["benchmark"], "est_median": statistics.median(ok),
                             "est_all": ";".join(f"{v:g}" for v in vals if v)})
        with open(d / "estimates.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(len(rows), "items with >=2 estimates; missing:", missing)
    elif cmd == "score":
        m, by_id = json.loads((d / "manifest.json").read_text()), json.loads((d / "items.json").read_text())
        est = {c: {} for c in m["coders"]}
        for c, info in m["coders"].items():
            for j in range(len(info["batches"])):
                for x in json.loads((d / c / f"batch{j}.json").read_text()):
                    est[c][str(x["item_id"])] = float(x["estimate_min"])
        rows = []
        excl = set(json.loads((d / "exclude.json").read_text())["ids"]) if (d / "exclude.json").exists() else set()
        for iid, it in by_id.items():
            if iid in excl:
                continue
            vals = [est[c].get(iid) for c in m["coders"]]
            if any(v is None or v <= 0 for v in vals):
                continue
            r = {"item_id": iid, "benchmark": it["benchmark"], "time_kind": it["time_kind"],
                 "published_min": it.get("time_min"), "bucket_lo": it.get("bucket_lo_min"),
                 "bucket_hi": it.get("bucket_hi_min"), "est_median": statistics.median(vals),
                 "est_all": ";".join(f"{v:g}" for v in vals)}
            rows.append(r)
        with open(d / "estimates.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

        def spearman(x, y):
            def rank(v):
                s = sorted(range(len(v)), key=lambda i: v[i])
                r = [0.0] * len(v)
                i = 0
                while i < len(s):
                    j = i
                    while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]:
                        j += 1
                    for k in range(i, j + 1):
                        r[s[k]] = (i + j) / 2
                    i = j + 1
                return r
            rx, ry = rank(x), rank(y)
            mx, my = statistics.mean(rx), statistics.mean(ry)
            num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
            return num / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))

        out = [f"# Blind time estimates vs published times — {run}", "",
               "Estimate = median of three coders (two Sonnet, one Terra). Ratio = estimate / "
               "published.", ""]
        for bm in sorted({r["benchmark"] for r in rows}):
            rs = [r for r in rows if r["benchmark"] == bm]
            pts = [r for r in rs if r["time_kind"] == "point" and r["published_min"]]
            bks = [r for r in rs if r["time_kind"] == "bucket"]
            out.append(f"## {bm} ({len(rs)} items)")
            if pts:
                e = [r["est_median"] for r in pts]
                p = [float(r["published_min"]) for r in pts]
                lr = [math.log(a / b) for a, b in zip(e, p)]
                out += [f"- Spearman rank correlation: {spearman(e, p):.2f}",
                        f"- Median ratio (bias): ×{math.exp(statistics.median(lr)):.2f}; "
                        f"middle half ×{math.exp(statistics.quantiles(lr, n=4)[0]):.2f}–"
                        f"×{math.exp(statistics.quantiles(lr, n=4)[2]):.2f}",
                        f"- Within 2× of published: {sum(abs(x) <= math.log(2) for x in lr)}/"
                        f"{len(lr)}; within 3×: {sum(abs(x) <= math.log(3) for x in lr)}/{len(lr)}"]
                for c in m["coders"]:
                    lc = [math.log(est[c][r["item_id"]] / float(r["published_min"])) for r in pts]
                    out.append(f"  - coder {c}: median ratio ×{math.exp(statistics.median(lc)):.2f}, "
                               f"Spearman {spearman([est[c][r['item_id']] for r in pts], p):.2f}")
            if bks:
                order = sorted({(r["bucket_lo"] or 0) for r in bks})
                ordv = [order.index(r["bucket_lo"] or 0) for r in bks]
                e = [r["est_median"] for r in bks]
                inside = sum((r["est_median"] >= (r["bucket_lo"] or 0)) and
                             (r["bucket_hi"] is None or r["est_median"] <= r["bucket_hi"])
                             for r in bks)
                out += [f"- Spearman with bucket order: {spearman(e, ordv):.2f}",
                        f"- Estimate inside the published bucket: {inside}/{len(bks)}"]
                for k, lo in enumerate(order):
                    sub = [r["est_median"] for r in bks if (r["bucket_lo"] or 0) == lo]
                    hi = next(r["bucket_hi"] for r in bks if (r["bucket_lo"] or 0) == lo)
                    out.append(f"  - bucket {lo:g}–{hi if hi else '∞'} min: n {len(sub)}, median "
                               f"estimate {statistics.median(sub):g} min "
                               f"(range {min(sub):g}–{max(sub):g})")
            out.append("")
        (d / "SCORE.md").write_text("\n".join(out))
        print("\n".join(out))


if __name__ == "__main__":
    main()
