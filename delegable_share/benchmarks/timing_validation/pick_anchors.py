"""Pick held-out anchor items (not in items.jsonl) with published times, for anchored estimation.
Terminal-Bench 2: non-security tasks with short instructions, spread over expert times.
SWE-bench Verified: one short issue per difficulty bucket."""
import json, pathlib, random, tomllib
import pandas as pd
HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"
used = {json.loads(l)["item_id"] for l in open(HERE / "items.jsonl")}
rng = random.Random(7)
out = []
tb = []
for f in sorted((RAW / "tb/repo").glob("*/task.toml")):
    m = tomllib.loads(f.read_text())["metadata"]
    name = f.parent.name
    if name in used or m.get("expert_time_estimate_min") is None or m.get("category") == "security":
        continue
    txt = (f.parent / "instruction.md").read_text().strip()
    if len(txt.split()) > 160:
        continue
    tb.append((float(m["expert_time_estimate_min"]), name, txt, m.get("category")))
for target in [5, 15, 30, 60, 120, 240, 480, 1440]:
    cand = sorted(tb, key=lambda x: (abs(__import__("math").log(x[0] / target)), x[1]))
    t, name, txt, cat = cand[0]
    tb = [x for x in tb if x[1] != name]
    out.append(dict(item_id=name, benchmark="terminal-bench-2.0", text=txt, time_min=t,
                    label=f"{t:g} minutes (task author's expert estimate)", category=cat))
d = pd.read_parquet(RAW / "swe/test.parquet")
labels = {"<15 min fix": "under 15 minutes", "15 min - 1 hour": "15 minutes to 1 hour",
          "1-4 hours": "1 to 4 hours", ">4 hours": "more than 4 hours"}
for bucket, lab in labels.items():
    c = d[(d["difficulty"] == bucket) & (~d["instance_id"].isin(used))]
    c = c[c["problem_statement"].str.split().str.len() <= 180]
    if c.empty:
        continue  # e.g. ">4 hours": all 3 items are in the test sample
    r = c.sample(1, random_state=7).iloc[0]
    out.append(dict(item_id=r.instance_id, benchmark="swe-bench-verified",
                    text=f"Repository: {r.repo}\n\n{r.problem_statement.strip()}", time_min=None,
                    label=f"{lab} (annotators' difficulty bucket)", category=None))
with open(HERE / "anchors.jsonl", "w") as fh:
    for o in out:
        fh.write(json.dumps(o) + "\n")
for o in out:
    print(o["benchmark"][:8], o["item_id"], "|", o["label"], "|", o["category"], "|", len(o["text"].split()), "words")
