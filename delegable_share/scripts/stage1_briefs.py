"""Build Stage 1 (unit schema) briefs for subagent coders: one brief per occupation.

Reads prompts/stage1_unit_schema.md (instructions + worked examples) and a task CSV, and writes
coding/stage1/<tag>/briefs/<onetsoc>.md plus coding/stage1/<tag>/manifest.json.

Usage: python3 scripts/stage1_briefs.py <tag> [data/pilot_tasks.csv]
Env: NONPILOT=1 drops statements with in_pilot == True; GROUP=k also writes briefs/group<j>.md
for subagents, each covering k occupations (instructions and examples once, one output file
per occupation). Per-occupation briefs are still written (Terra and validation use them).
"""
import os
import csv
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROMPT = ROOT / "prompts" / "stage1_unit_schema.md"

WRAPPER = """You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each TARGET independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  {out_path}
with one element per target, in the order given. Each element is the output
object described in the instructions, with "task_id" added as its first key.
Write nothing else to that file. Then reply "done <n> items", plus at most
three sentences on anything you found ambiguous.
"""

BODY_MARKER = "=== INSTRUCTIONS ==="  # everything from here on is model-agnostic


def section(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]


def main():
    tag = sys.argv[1]
    tasks_csv = ROOT / (sys.argv[2] if len(sys.argv) > 2 else "data/pilot_tasks.csv")
    out = ROOT / "coding" / "stage1" / tag
    md = PROMPT.read_text()
    prompt_block = section(md, "## Prompt", "## Worked examples").split("```")[1].strip("\n")
    examples = section(md, "## Worked examples", "## Changes from the spec")
    examples = "\n".join(
        l for l in examples.splitlines()[1:] if not l.startswith("Drawn from BPO")
    ).strip()

    rows = [r for r in csv.DictReader(open(tasks_csv)) if r["has_ratings"] == "True"
            and not (os.environ.get("NONPILOT") and r.get("in_pilot") == "True")]
    occs = {}
    for r in rows:
        occs.setdefault(r["onetsoc_code"], []).append(r)

    (out / "briefs").mkdir(parents=True, exist_ok=True)
    manifest = {"stage": 1, "tag": tag, "prompt_header": md.splitlines()[0],
                "built": datetime.date.today().isoformat(),
                "source": str(tasks_csv.relative_to(ROOT)), "batches": []}
    for code, rs in occs.items():
        out_path = out / f"{code}.json"
        task_list = "\n".join(f"[{r['task_id']}] {r['task_statement']}" for r in rs)
        brief = "\n\n".join([
            WRAPPER.format(out_path=out_path),
            BODY_MARKER + "\n" + prompt_block,
            "=== WORKED EXAMPLES (other occupations) ===\n" + examples,
            f"=== OCCUPATION ===\n{rs[0]['occupation_title']} ({code})\n\n"
            f"{rs[0]['occupation_description']}",
            "=== TASK LIST (context; every statement below is also a TARGET) ===\n" + task_list,
            f"=== TARGETS ===\nCode all {len(rs)} statements above, in that order.",
        ])
        bpath = out / "briefs" / f"{code}.md"
        bpath.write_text(brief + "\n")
        manifest["batches"].append({"onetsoc": code, "title": rs[0]["occupation_title"],
                                    "n": len(rs), "task_ids": [r["task_id"] for r in rs],
                                    "brief": str(bpath.relative_to(ROOT)),
                                    "output": str(out_path.relative_to(ROOT))})
        print(code, len(rs), bpath)
    k = int(os.environ.get("GROUP", 0))
    if k:
        codes = list(occs)
        manifest["groups"] = []
        for j in range(0, len(codes), k):
            grp = codes[j:j + k]
            paths = "\n".join(f"  {occs[c][0]['occupation_title']} ({c}) -> {out / f'{c}.json'}" for c in grp)
            head = f"""You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are {len(grp)} occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
{paths}
with one element per target, in the order given. Each element is the output
object described in the instructions, with "task_id" added as its first key.
Write nothing else to those files. Then reply "done <n> items" per occupation,
plus at most three sentences on anything you found ambiguous.
"""
            secs = []
            for c in grp:
                rs = occs[c]
                secs.append(f"=== OCCUPATION: {rs[0]['occupation_title']} ({c}) ===\n"
                            f"{rs[0]['occupation_description']}\n\n"
                            "TASK LIST (context; every statement below is also a TARGET):\n" +
                            "\n".join(f"[{r['task_id']}] {r['task_statement']}" for r in rs) +
                            f"\n\nTARGETS: code all {len(rs)} statements above, in that order, "
                            f"and write them to {out / f'{c}.json'}.")
            g = "\n\n".join([head, BODY_MARKER + "\n" + prompt_block,
                              "=== WORKED EXAMPLES (other occupations) ===\n" + examples] + secs)
            gp = out / "briefs" / f"group{j // k}.md"
            gp.write_text(g + "\n")
            manifest["groups"].append({"brief": str(gp.relative_to(ROOT)), "onetsoc": grp,
                                       "n": sum(len(occs[c]) for c in grp)})
            print("group", j // k, grp, sum(len(occs[c]) for c in grp))
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
