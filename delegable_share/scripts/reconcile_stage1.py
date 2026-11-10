"""Reconcile Stage 1 disagreements between two coders (Claude subagent vs GPT-6.1 Terra).

Protocol (DECISIONS.md): each side sees both codings and both sets of reasoning, labelled X/Y in
random order, and picks one or writes a revision. If both pick the same coding, it is settled.
Otherwise an Opus subagent adjudicates. Every round is kept.

  python3 scripts/reconcile_stage1.py build      <tag>  # find disputes, write briefs + key
  python3 scripts/reconcile_stage1.py terra      <tag>  # Terra's round
  python3 scripts/reconcile_stage1.py adjudicate <tag>  # settle what agrees; briefs for the rest
  python3 scripts/reconcile_stage1.py finalize   <tag>  # coding/stage1/<tag>_final/ + RECONCILE.md

Inputs: coding/stage1/<tag>/<onetsoc>.json (Claude) and coding/stage1/<tag>_terra/<onetsoc>.json.
Working files: coding/stage1/<tag>/reconcile/.
"""
import collections
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import ROOT, chat_json, spent  # noqa: E402

TYPES = ["DISCRETE", "LIVE_SERVICE", "INTERPERSONAL", "PHYSICAL", "NO_DELIVERABLE"]

ROUND = """Two coders independently coded the same task statements, following the
instructions above. For each statement under DISPUTES their codings
disagree. Each coding is shown in full, with the coder's reasoning, as
coding X and coding Y (the labels are assigned at random).

For each disputed statement, decide which coding follows the instructions
better, judged only by the instructions and by how this work is done today
without AI. Don't prefer a coding for being longer or more finely split. If
both are wrong in a way neither fixes, write a revised coding instead.

For each disputed statement, output:
  {"task_id": "...", "reasoning": "two or three sentences",
   "choice": "X" | "Y" | "revised",
   "coding": <full coding object in the instructions' format; only if revised>}
"""

ADJ = """You are the final adjudicator. Two coders independently coded each statement
under DISPUTES, following the instructions above, and disagreed. Each was
then shown both codings (X and Y, labels random) and asked to pick one or
revise; their verdicts did not agree, and both verdicts are shown.

For each statement, make the final call: pick X or Y, or write the coding
that best follows the instructions. Judge only by the instructions and by
how this work is done today without AI.

For each statement, output:
  {"task_id": "...", "reasoning": "two or three sentences",
   "choice": "X" | "Y" | "revised",
   "coding": <full coding object; only if revised>}
"""


def mix(item):
    m = collections.Counter()
    for p in item.get("parts", []):
        m[p["type"]] += float(p["time_share"])
    return m


def disputed(a, b):
    dist = 0.5 * sum(abs(mix(a)[t] - mix(b)[t]) for t in TYPES)
    return dist >= 0.25 or len(a.get("parts", [])) != len(b.get("parts", []))


def paths(tag):
    s1 = ROOT / "coding" / "stage1"
    return s1 / tag, s1 / f"{tag}_terra", s1 / tag / "reconcile"


def brief_body(tag, code, disputes, key, header, extra=None):
    """Stage 1 brief body (instructions, examples, occupation, task list) + disputes."""
    src = (ROOT / "coding" / "stage1" / tag / "briefs" / f"{code}.md").read_text()
    body = src[src.index("=== INSTRUCTIONS ==="):src.index("=== TARGETS ===")]
    blocks = []
    for tid in disputes:
        x, y = key[code][tid]["X"], key[code][tid]["Y"]
        blk = (f"--- task {tid} ---\n"
               f"CODING X:\n{json.dumps(x['coding'], indent=1)}\n\n"
               f"CODING Y:\n{json.dumps(y['coding'], indent=1)}\n")
        if extra:
            blk += extra(code, tid)
        blocks.append(blk)
    return body + "=== DISPUTES ===\n" + header + "\n" + "\n".join(blocks)


def load_items(d, code):
    return {str(it["task_id"]): it for it in json.loads((d / f"{code}.json").read_text())}


def main():
    cmd, tag = sys.argv[1], sys.argv[2]
    cdir, tdir, rdir = paths(tag)
    manifest = json.loads((cdir / "manifest.json").read_text())
    codes = [b["onetsoc"] for b in manifest["batches"]]

    if cmd == "build":
        rng = random.Random(20261109)
        key = {}
        for code in codes:
            A, B = load_items(cdir, code), load_items(tdir, code)
            key[code] = {}
            for tid in A:
                if disputed(A[tid], B[tid]):
                    pair = [("claude", A[tid]), ("terra", B[tid])]
                    rng.shuffle(pair)
                    key[code][tid] = {lab: {"source": s, "coding": c}
                                      for lab, (s, c) in zip("XY", pair)}
        (rdir / "briefs").mkdir(parents=True, exist_ok=True)
        (rdir / "claude").mkdir(exist_ok=True)
        (rdir / "key.json").write_text(json.dumps(key, indent=1))
        for code in codes:
            if not key[code]:
                continue
            out = rdir / "claude" / f"{code}.json"
            wrapper = ("You are a reviewer in a research pipeline. Use only this file: read no "
                       "other file and do not search the web.\n"
                       f"Write ONE JSON array (one element per disputed statement) to:\n  {out}\n"
                       "and nothing else to that file. Then reply \"done <n> items\".\n\n")
            (rdir / "briefs" / f"{code}.md").write_text(
                wrapper + brief_body(tag, code, key[code], key, ROUND))
            print(code, len(key[code]), "disputes")

    elif cmd == "terra":
        key = json.loads((rdir / "key.json").read_text())
        (rdir / "terra").mkdir(exist_ok=True)
        before = spent()
        for code in codes:
            if not key[code]:
                continue
            body = brief_body(tag, code, key[code], key, ROUND)
            parsed, _ = chat_json([{"role": "user", "content": body +
                                    '\nReturn a JSON object {"items": [...]}.'}],
                                  purpose=f"reconcile stage1 {tag} {code}")
            (rdir / "terra" / f"{code}.json").write_text(json.dumps(parsed.get("items", []),
                                                                    indent=1))
            print(code, len(parsed.get("items", [])))
        print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")

    elif cmd == "adjudicate":
        key = json.loads((rdir / "key.json").read_text())
        (rdir / "adjudicate" / "out").mkdir(parents=True, exist_ok=True)
        settled = {}
        for code in codes:
            if not key[code]:
                continue
            v = {m: {str(x["task_id"]): x for x in
                     json.loads((rdir / m / f"{code}.json").read_text())}
                 for m in ("claude", "terra")}
            left = []
            for tid in key[code]:
                c, t = v["claude"].get(tid, {}), v["terra"].get(tid, {})
                if c.get("choice") in ("X", "Y") and c.get("choice") == t.get("choice"):
                    settled.setdefault(code, {})[tid] = {"how": "both picked " + c["choice"],
                                                         "choice": c["choice"]}
                else:
                    left.append(tid)

            def verdicts(code_, tid, v=v):
                return "".join(
                    f"VERDICT {n}: {json.dumps(v[m].get(tid, {}), indent=1)}\n"
                    for n, m in (("1", "claude"), ("2", "terra")))
            if left:
                out = rdir / "adjudicate" / "out" / f"{code}.json"
                wrapper = ("You are the final adjudicator in a research pipeline. Use only this "
                           "file: read no other file and do not search the web.\n"
                           f"Write ONE JSON array (one element per disputed statement) to:\n"
                           f"  {out}\nand nothing else to that file. Then reply "
                           "\"done <n> items\".\n\n")
                sub = {tid: key[code][tid] for tid in left}
                (rdir / "adjudicate" / f"{code}.md").write_text(
                    wrapper + brief_body(tag, code, sub, {code: sub}, ADJ, verdicts))
            print(code, f"settled {len(key[code]) - len(left)}, to adjudicate {len(left)}")
        (rdir / "settled.json").write_text(json.dumps(settled, indent=1))

    elif cmd == "finalize":
        key = json.loads((rdir / "key.json").read_text())
        settled = json.loads((rdir / "settled.json").read_text())
        fdir = ROOT / "coding" / "stage1" / f"{tag}_final"
        fdir.mkdir(exist_ok=True)
        log = [f"# Stage 1 reconciliation log — {tag}", "",
               "Base coding: Claude (Opus subagent). Disputed statements replaced by the outcome "
               "of reconciliation (both picked the same coding) or adjudication (Opus).", ""]
        counts = collections.Counter()
        for code in codes:
            items = load_items(cdir, code)
            adj_f = rdir / "adjudicate" / "out" / f"{code}.json"
            adj = ({str(x["task_id"]): x for x in json.loads(adj_f.read_text())}
                   if adj_f.exists() else {})
            log.append(f"## {code}")
            for tid in key[code]:
                if tid in settled.get(code, {}):
                    ch, how = settled[code][tid]["choice"], settled[code][tid]["how"]
                    final = key[code][tid][ch]["coding"]
                    src = key[code][tid][ch]["source"]
                else:
                    a = adj[tid]
                    how = "adjudicated: " + a["choice"]
                    if a["choice"] in ("X", "Y"):
                        final = key[code][tid][a["choice"]]["coding"]
                        src = key[code][tid][a["choice"]]["source"]
                    else:
                        final, src = dict(a["coding"], task_id=tid), "adjudicator revision"
                    how += f" — {a['reasoning']}"
                items[tid] = dict(final, task_id=tid)
                counts[src] += 1
                log.append(f"- **{tid}**: {how} → {src}")
            log.append("")
            (fdir / f"{code}.json").write_text(json.dumps(list(items.values()), indent=1))
        log.insert(4, "Outcomes: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + "\n")
        (fdir / "RECONCILE.md").write_text("\n".join(log))
        print("\n".join(log[:6]))


if __name__ == "__main__":
    main()
