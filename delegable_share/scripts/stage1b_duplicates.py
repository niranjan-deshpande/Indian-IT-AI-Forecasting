"""Stage 1b: find duplicate work items within an occupation, with two independent models.

  python3 scripts/stage1b_duplicates.py build  <tag>   # briefs for Claude subagents
  python3 scripts/stage1b_duplicates.py terra  <tag>   # same items through GPT-6.1 Terra
  python3 scripts/stage1b_duplicates.py report <tag>   # agreement; writes DUPLICATES.md

Inputs: coding/stage1/<tag>/units.csv. Items with type DISCRETE or LIVE_SERVICE are compared
(the others get D = 0, so duplicates among them don't change anything).
Outputs: coding/stage1/<tag>/dedupe/{briefs,claude,terra}/<onetsoc>.json and DUPLICATES.md.
"""
import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402

PROMPT = ROOT / "prompts" / "stage1b_duplicates.md"


def items_by_occ(tag):
    occ = collections.defaultdict(list)
    for r in csv.DictReader(open(ROOT / "coding" / "stage1" / tag / "units.csv")):
        if r["type"] in ("DISCRETE", "LIVE_SERVICE"):
            occ[r["onetsoc_code"]].append(r)
    return occ


def body(rows):
    prompt = PROMPT.read_text().split("```")[1].strip("\n")
    lines = [f"[{r['task_id']}{r['part_id']}] {r['type']} — {r['work_item']} "
             f"(start: {r['start']}; end: {r['end']}) — from statement: {r['task_statement']}"
             for r in rows]
    return (f"{prompt}\n\n=== OCCUPATION ===\n{rows[0]['occupation_title']}\n\n"
            "=== ITEMS ===\n" + "\n".join(lines))


def main():
    cmd, tag = sys.argv[1], sys.argv[2]
    d = ROOT / "coding" / "stage1" / tag / "dedupe"
    occ = items_by_occ(tag)
    if cmd == "build":
        (d / "briefs").mkdir(parents=True, exist_ok=True)
        (d / "claude").mkdir(exist_ok=True)
        for code, rows in occ.items():
            out = d / "claude" / f"{code}.json"
            (d / "briefs" / f"{code}.md").write_text(
                "You are a checker in a research pipeline. Use only this file: read no other "
                "file and do not search the web.\n"
                f"Write the JSON object described below to:\n  {out}\n"
                "and nothing else to that file. Then reply \"done <n> pairs\".\n\n" + body(rows))
            print(code, len(rows), "items")
    elif cmd == "terra":
        (d / "terra").mkdir(parents=True, exist_ok=True)
        before = spent()
        from concurrent.futures import ThreadPoolExecutor

        def one(kv):
            code, rows = kv
            parsed, _ = chat_json([{"role": "user", "content": body(rows)}],
                                  purpose=f"stage1b {tag} {code}")
            (d / "terra" / f"{code}.json").write_text(json.dumps(parsed, indent=1))
            return code, len(parsed.get("pairs", []))
        with ThreadPoolExecutor(6) as ex:
            for code, n in ex.map(one, occ.items()):
                print(code, n, "pairs")
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")
    elif cmd == "report":
        out = [f"# Stage 1b duplicates — {tag}", "",
               "Collapsed = flagged by both models (weight becomes the mean of the two). "
               "One-model pairs are listed for the hand-check and NOT collapsed.", ""]
        names = {f"{r['task_id']}{r['part_id']}": r for rows in occ.values() for r in rows}
        for code, rows in occ.items():
            got = {}
            for m in ("claude", "terra"):
                f = d / m / f"{code}.json"
                pairs = json.loads(f.read_text()).get("pairs", []) if f.exists() else []
                got[m] = {frozenset((str(p["a"]), str(p["b"]))): p["reasoning"] for p in pairs}
            both = got["claude"].keys() & got["terra"].keys()
            out += [f"## {rows[0]['occupation_title']}", ""]
            for label, keys in (("Both models (collapse)", both),
                                ("Claude only", got["claude"].keys() - both),
                                ("Terra only", got["terra"].keys() - both)):
                out.append(f"**{label}:** {len(keys)}")
                for k in sorted(keys, key=sorted):
                    a, b = sorted(k)
                    why = got["claude"].get(k) or got["terra"].get(k)
                    out.append(f"- {a} = {b}: “{names.get(a, {}).get('work_item', '?')}” / "
                               f"“{names.get(b, {}).get('work_item', '?')}” — {why}")
                out.append("")
        (ROOT / "coding" / "stage1" / tag / "DUPLICATES.md").write_text("\n".join(out))
        print("\n".join(out))
    elif cmd == "apply":
        # Collapse pairs flagged by both models: keep the first ID, weight = mean of the two.
        agreed = []
        for code in occ:
            sets = []
            for m in ("claude", "terra"):
                pairs = json.loads((d / m / f"{code}.json").read_text()).get("pairs", [])
                sets.append({frozenset((str(p["a"]), str(p["b"]))) for p in pairs})
            agreed += [sorted(k) for k in sets[0] & sets[1]]
        src = ROOT / "coding" / "stage1" / tag / "units.csv"
        rows = list(csv.DictReader(open(src)))
        key = {f"{r['task_id']}{r['part_id']}": r for r in rows}
        drop = set()
        for a, b in agreed:
            ra, rb = key[a], key[b]
            ra["weight"] = round((float(ra["weight"]) + float(rb["weight"])) / 2, 4)
            ra["collapsed_with"] = b
            drop.add(b)
        final = [dict(r, collapsed_with=r.get("collapsed_with", "")) for r in rows
                 if f"{r['task_id']}{r['part_id']}" not in drop]
        with open(src.with_name("units_final.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(final[0]))
            w.writeheader()
            w.writerows(final)
        print(f"collapsed {agreed}; {len(rows)} -> {len(final)} parts in units_final.csv")


if __name__ == "__main__":
    main()
