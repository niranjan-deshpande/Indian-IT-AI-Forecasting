"""Assemble timing-validation items. Run: python3 -I build_items.py  (from this dir). No estimates made here."""
import json, random, tomllib, pathlib, pandas as pd
HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"
SEED = 20261109
MAXW = 1500
out = []

# ---- SWE-bench Verified
d = pd.read_parquet(RAW / "swe/test.parquet")
bk = {"<15 min fix": (0, 15), "15 min - 1 hour": (15, 60), "1-4 hours": (60, 240), ">4 hours": (240, None)}
rng = random.Random(SEED)
sel = []
for b in bk:
    ids = sorted(d[d.difficulty == b].instance_id)
    sel += ids if b == ">4 hours" else rng.sample(ids, 15)
for iid in sel:
    r = d[d.instance_id == iid].iloc[0]
    w = r.problem_statement.split(); trunc = len(w) > MAXW
    ps = " ".join(w[:MAXW]) + " [truncated]" if trunc else r.problem_statement
    lo, hi = bk[r.difficulty]
    out.append(dict(item_id=iid, benchmark="swe-bench-verified",
        text=f"Repository: {r.repo}\nInstance: {iid}\n\n{ps}", truncated=trunc,
        time_kind="bucket", time_min=None, bucket_lo_min=lo, bucket_hi_min=hi,
        time_note=f"OpenAI annotator difficulty bucket: {r.difficulty}"))

# ---- Terminal-Bench 2.0
rows = []
for f in sorted((RAW / "tb/repo").glob("*/task.toml")):
    m = tomllib.loads(f.read_text())["metadata"]
    if m.get("expert_time_estimate_min") is None: continue
    rows.append((f.parent.name, float(m["expert_time_estimate_min"]), m.get("junior_time_estimate_min"), m.get("category"), m.get("difficulty")))
rows.sort(key=lambda x: (x[1], x[0]))
q = len(rows) // 4; rng = random.Random(SEED); pick = []
for i in range(4):
    chunk = rows[i*q:(i+1)*q if i < 3 else len(rows)]
    pick += rng.sample(chunk, 10)
for name, e, j, cat, diff in sorted(pick, key=lambda x: (x[1], x[0])):
    txt = (RAW / "tb/repo" / name / "instruction.md").read_text().strip()
    out.append(dict(item_id=name, benchmark="terminal-bench-2.0", text=txt, truncated=False,
        time_kind="point", time_min=e, bucket_lo_min=None, bucket_hi_min=None,
        time_note=f"expert estimate {e:g} min; junior estimate {j} min; category={cat}; author difficulty={diff}"))
with open(HERE / "items.jsonl", "w") as fh:
    for o in out: fh.write(json.dumps(o) + "\n")
print(len(out), sum(o["truncated"] for o in out), len(rows))
