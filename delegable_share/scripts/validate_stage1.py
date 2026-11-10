"""Validate Stage 1 outputs against a manifest and flatten them into units.csv.

Usage: python3 scripts/validate_stage1.py <tag> [<output_dir>]
  <tag>         which brief set (coding/stage1/<tag>/manifest.json)
  <output_dir>  where the coder outputs are (default coding/stage1/<tag>); e.g. a
                cross-check run in coding/stage1/<tag>_terra
Exit code 1 if any batch fails; problems are printed per task_id so items can be re-run.
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TYPES = {"DISCRETE", "LIVE_SERVICE", "INTERPERSONAL", "PHYSICAL", "NO_DELIVERABLE"}
CODED = {"DISCRETE", "LIVE_SERVICE"}
UNIT_FIELDS = ["unit_reasoning", "work_item", "start", "end", "checked_by"]


def ids(x):
    return [str(i) for i in (x or [])]


def main():
    tag = sys.argv[1]
    mdir = ROOT / "coding" / "stage1" / tag
    odir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else mdir
    if not odir.is_absolute():
        odir = ROOT / odir
    manifest = json.loads((mdir / "manifest.json").read_text())
    tasks = {r["task_id"]: r for r in csv.DictReader(open(ROOT / manifest["source"]))}
    problems, out_rows = [], []
    for b in manifest["batches"]:
        code = b["onetsoc"]
        path = odir / f"{code}.json"
        if not path.exists():
            problems.append((code, "-", "output file missing"))
            continue
        try:
            items = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            problems.append((code, "-", f"bad JSON: {e}"))
            continue
        got = [str(it.get("task_id")) for it in items]
        expected = set(b["task_ids"])
        for missing in expected - set(got):
            problems.append((code, missing, "not coded"))
        for extra in set(got) - expected:
            problems.append((code, extra, "unexpected task_id"))
        for it in items:
            tid = str(it.get("task_id"))
            parts = it.get("parts") or []
            if not parts:
                problems.append((code, tid, "no parts"))
                continue
            total = sum(float(p.get("time_share", 0)) for p in parts)
            if abs(total - 1) > 0.011:
                problems.append((code, tid, f"time shares sum to {total:.3f}"))
            for p in parts:
                pid, t = p.get("part_id"), p.get("type")
                if t not in TYPES:
                    problems.append((code, tid, f"part {pid}: bad type {t}"))
                if t in CODED:
                    for f in UNIT_FIELDS:
                        if not str(p.get(f, "")).strip():
                            problems.append((code, tid, f"part {pid}: missing {f}"))
                dup, ov = ids(p.get("duplicates")), ids(p.get("overlaps_with"))
                bad = [x for x in dup + ov if x not in expected or x == tid]
                if bad:
                    problems.append((code, tid, f"part {pid}: bad overlap/duplicate ids {bad}"))
                im = float(tasks[tid]["im"]) if tid in tasks and tasks[tid]["im"] else None
                out_rows.append({
                    "onetsoc_code": code, "occupation_title": b["title"], "task_id": tid,
                    "task_statement": tasks.get(tid, {}).get("task_statement", ""),
                    "im": im, "part_id": pid, "part_text": p.get("text"),
                    "time_share": p.get("time_share"),
                    "weight": round(im * float(p.get("time_share", 0)), 4) if im else None,
                    "type": t, "work_item": p.get("work_item", ""), "start": p.get("start", ""),
                    "end": p.get("end", ""), "checked_by": p.get("checked_by", ""),
                    "duplicates": ";".join(dup), "overlaps_with": ";".join(ov),
                    "split_reasoning": it.get("split_reasoning", ""),
                    "type_reasoning": p.get("type_reasoning", ""),
                    "unit_reasoning": p.get("unit_reasoning", ""), "notes": it.get("notes", ""),
                })
    if out_rows:
        with open(odir / "units.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
            w.writeheader()
            w.writerows(out_rows)
    for p in problems:
        print("PROBLEM", *p)
    print(f"{len(out_rows)} parts written to {odir.relative_to(ROOT)}/units.csv; "
          f"{len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
