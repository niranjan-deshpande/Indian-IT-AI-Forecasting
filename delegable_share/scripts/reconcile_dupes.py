"""Reconcile Stage 1b duplicate pairs that only one model flagged (protocol in DECISIONS.md).

  python3 scripts/reconcile_dupes.py build    <tag>  # disputed pairs; Claude brief + Terra round
  python3 scripts/reconcile_dupes.py adjudicate <tag> # settle agreements; Opus brief for the rest
  python3 scripts/reconcile_dupes.py apply    <tag>  # collapse final pairs -> units_final.csv

Working files: coding/stage1/<tag>/dedupe/reconcile/.
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402
from stage1b_duplicates import items_by_occ  # noqa: E402

RULES = pathlib.Path(ROOT / "prompts" / "stage1b_duplicates.md").read_text().split("```")[1]

ASK = """Two checkers applied the duplicate rules below to the same list of work
items and disagreed about the pairs under DISPUTED PAIRS: one checker judged
each pair a duplicate (its reasoning is shown); the other did not flag it.
Decide for each pair, using only the rules and how the work is done today.

RULES:
{rules}
For each pair output {{"a": "...", "b": "...", "reasoning": "two sentences",
"duplicate": true | false}}.
"""


def describe(r):
    return (f"[{r['task_id']}{r['part_id']}] {r['type']} — {r['work_item']} (start: {r['start']}; "
            f"end: {r['end']}) — from statement: {r['task_statement']}")


def disputed(tag):
    d = ROOT / "coding" / "stage1" / tag / "dedupe"
    out = {}
    for code, rows in items_by_occ(tag).items():
        got = {}
        for m in ("claude", "terra"):
            pairs = json.loads((d / m / f"{code}.json").read_text()).get("pairs", [])
            got[m] = {frozenset((str(p["a"]), str(p["b"]))): p["reasoning"] for p in pairs}
        both = got["claude"].keys() & got["terra"].keys()
        names = {f"{r['task_id']}{r['part_id']}": r for r in rows}
        out[code] = {"agreed": [sorted(k) for k in both], "disputed": [
            {"a": sorted(k)[0], "b": sorted(k)[1], "flagged_by": m, "reasoning": why,
             "text": describe(names[sorted(k)[0]]) + "\n" + describe(names[sorted(k)[1]])}
            for m in ("claude", "terra") for k, why in got[m].items() if k not in both]}
    return out


def body(code, pairs, rows):
    items = "\n".join(describe(r) for r in rows)
    blocks = "\n\n".join(f"PAIR {p['a']} / {p['b']}\n{p['text']}\nFlagging checker's reasoning: "
                         f"{p['reasoning']}" for p in pairs)
    return (ASK.format(rules=RULES) + f"\n=== ALL ITEMS ({rows[0]['occupation_title']}) ===\n"
            f"{items}\n\n=== DISPUTED PAIRS ===\n{blocks}\n")


def main():
    cmd, tag = sys.argv[1], sys.argv[2]
    rdir = ROOT / "coding" / "stage1" / tag / "dedupe" / "reconcile"
    occ = items_by_occ(tag)
    if cmd == "build":
        dis = disputed(tag)
        (rdir / "claude").mkdir(parents=True, exist_ok=True)
        (rdir / "terra").mkdir(exist_ok=True)
        (rdir / "disputes.json").write_text(json.dumps(dis, indent=1))
        if __import__("os").environ.get("NOROUND"):  # BPO run on: one-model flags go to Opus directly
            for code, v in dis.items():
                print(code, "agreed", v["agreed"], "| disputed", [(p["a"], p["b"]) for p in v["disputed"]])
            return
        before = spent()
        for code, v in dis.items():
            if not v["disputed"]:
                continue
            b = body(code, v["disputed"], occ[code])
            out = rdir / "claude" / f"{code}.json"
            (rdir / f"brief_{code}.md").write_text(
                "Use only this file: read no other file and do not search the web.\n"
                f"Write ONE JSON array (one element per disputed pair) to:\n  {out}\n"
                "and nothing else to that file. Then reply \"done <n> pairs\".\n\n" + b)
            parsed, _ = chat_json([{"role": "user", "content": b +
                                    '\nReturn a JSON object {"pairs": [...]}.'}],
                                  purpose=f"reconcile dupes {tag} {code}")
            (rdir / "terra" / f"{code}.json").write_text(json.dumps(parsed.get("pairs", []),
                                                                    indent=1))
            print(code, len(v["disputed"]), "disputed; terra:",
                  [(p["a"], p["b"], p["duplicate"]) for p in parsed.get("pairs", [])])
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")
    elif cmd == "adjudicate":
        dis = json.loads((rdir / "disputes.json").read_text())
        final = {}
        for code, v in dis.items():
            final[code] = {"collapse": list(v["agreed"]), "log": []}
            left = []
            for p in v["disputed"]:
                k = frozenset((p["a"], p["b"]))
                verdict = {}
                for m in ("claude", "terra"):
                    f = rdir / m / f"{code}.json"
                    for x in (json.loads(f.read_text()) if f.exists() else []):
                        if frozenset((str(x["a"]), str(x["b"]))) == k:
                            verdict[m] = x
                c, t = verdict.get("claude", {}), verdict.get("terra", {})
                if "duplicate" in c and c.get("duplicate") == t.get("duplicate"):
                    final[code]["log"].append(f"{p['a']}={p['b']}: both now say "
                                              f"{'duplicate' if c['duplicate'] else 'distinct'}")
                    if c["duplicate"]:
                        final[code]["collapse"].append([p["a"], p["b"]])
                else:
                    left.append(dict(p, verdicts=verdict))
            if left:
                out = rdir / f"adjudicated_{code}.json"
                blocks = "\n\n".join(
                    f"PAIR {p['a']} / {p['b']}\n{p['text']}\nOriginal flag reasoning: "
                    f"{p['reasoning']}" + (f"\nVerdict 1: {json.dumps(p['verdicts'].get('claude'))}\n"
                    f"Verdict 2: {json.dumps(p['verdicts'].get('terra'))}" if p['verdicts'] else "")
                    for p in left)
                (rdir / f"adjudicate_{code}.md").write_text(
                    "You are the final adjudicator. Use only this file: read no other file and "
                    "do not search the web.\nTwo independent checkers disagree (one flagged the "
                    "pair, the other did not) about whether each pair below is a duplicate under "
                    "these rules:\n"
                    f"{RULES}\nMake the final call for each pair. Write ONE JSON array of "
                    '{"a","b","reasoning","duplicate": true|false} to:\n'
                    f"  {out}\nand nothing else to that file. Then reply \"done <n> pairs\".\n\n"
                    f"=== ALL ITEMS ===\n" + "\n".join(describe(r) for r in occ[code]) +
                    f"\n\n=== PAIRS ===\n{blocks}\n")
            final[code]["to_adjudicate"] = [[p["a"], p["b"]] for p in left]
            print(code, "collapse", final[code]["collapse"], "| adjudicate",
                  final[code]["to_adjudicate"], "|", final[code]["log"])
        (rdir / "final.json").write_text(json.dumps(final, indent=1))
    elif cmd == "apply":
        final = json.loads((rdir / "final.json").read_text())
        pairs = []
        for code, v in final.items():
            pairs += v["collapse"]
            f = rdir / f"adjudicated_{code}.json"
            for x in (json.loads(f.read_text()) if f.exists() else []):
                if x["duplicate"]:
                    pairs.append(sorted([str(x["a"]), str(x["b"])]))
        src = ROOT / "coding" / "stage1" / tag / "units.csv"
        rows = list(csv.DictReader(open(src)))
        key = {f"{r['task_id']}{r['part_id']}": r for r in rows}
        # Merge whole groups (pairs can chain, e.g. a=b, a=c, b=c): keep the first member; its
        # weight is the mean of the group's weights (symmetric collapse, DECISIONS 2026-11-09).
        parent = {}

        def find(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                x = parent[x]
            return x
        for a, b in pairs:
            parent[find(b)] = find(a)
        groups = {}
        for x in list(parent):
            groups.setdefault(find(x), []).append(x)
        drop = set()
        for members in groups.values():
            members = sorted(members)
            keep = members[0]
            key[keep]["weight"] = round(sum(float(key[m]["weight"]) for m in members) / len(members), 4)
            key[keep]["collapsed_with"] = ";".join(members[1:])
            drop |= set(members[1:])
        out = [dict(r, collapsed_with=r.get("collapsed_with", "")) for r in rows
               if f"{r['task_id']}{r['part_id']}" not in drop]
        with open(src.with_name("units_final.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
        print(f"collapsed {pairs}; {len(rows)} -> {len(out)} parts")


if __name__ == "__main__":
    main()
