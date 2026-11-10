"""Compare two Stage 1 runs (e.g. Claude subagents vs an OpenAI model) statement by statement.

Usage: python3 scripts/compare_stage1.py coding/stage1/v2 coding/stage1/v2_terra
Both directories need a units.csv (run validate_stage1.py first). Prints importance shares by
type for each run, and the statements where the runs disagree on the split or on the
importance-weighted type mix. Writes <dir_b>/COMPARE.md.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TYPES = ["DISCRETE", "LIVE_SERVICE", "INTERPERSONAL", "PHYSICAL", "NO_DELIVERABLE"]


def load(d):
    by = collections.defaultdict(list)
    for r in csv.DictReader(open(ROOT / d / "units.csv")):
        by[(r["occupation_title"], r["task_id"])].append(r)
    return by


def mix(parts):
    m = collections.Counter()
    for p in parts:
        m[p["type"]] += float(p["time_share"])
    return m


def main():
    a_dir, b_dir = sys.argv[1], sys.argv[2]
    A, B = load(a_dir), load(b_dir)
    out = [f"# Stage 1 comparison: `{a_dir}` (A) vs `{b_dir}` (B)", ""]
    occs = sorted({k[0] for k in A})
    out += ["## Share of importance by type", "",
            "| Occupation | Run | " + " | ".join(TYPES) + " | Parts |",
            "|---|---|" + "---|" * (len(TYPES) + 1)]
    for o in occs:
        for name, R in (("A", A), ("B", B)):
            tot, c, n = 0.0, collections.Counter(), 0
            for (oo, _), parts in R.items():
                if oo != o:
                    continue
                for p in parts:
                    w = float(p["weight"] or 0)
                    c[p["type"]] += w
                    tot += w
                    n += 1
            out.append(f"| {o} | {name} | " + " | ".join(
                f"{100 * c[t] / tot:.0f}%" if tot else "-" for t in TYPES) + f" | {n} |")
    # distance = half L1 between type mixes (0 = same mix, 1 = disjoint)
    rows, agree = [], 0
    for k in sorted(A):
        ma, mb = mix(A[k]), mix(B.get(k, []))
        dist = 0.5 * sum(abs(ma[t] - mb[t]) for t in TYPES)
        same_split = len(A[k]) == len(B.get(k, []))
        if dist < 0.25 and same_split:
            agree += 1
        else:
            rows.append((dist, k, A[k], B.get(k, [])))
    out += ["", f"## Agreement: {agree} of {len(A)} statements have the same number of parts "
            "and a type mix within 0.25 (half-L1).", "",
            "## Disagreements (largest type-mix difference first)", ""]
    for dist, k, pa, pb in sorted(rows, key=lambda x: -x[0]):
        out.append(f"### {k[1]} — {pa[0]['task_statement']}  (type-mix distance {dist:.2f})")
        for name, ps in (("A", pa), ("B", pb)):
            for p in ps:
                out.append(f"- {name}{p['part_id']} {p['type']} {float(p['time_share']):.2f}: "
                           f"{p['work_item'] or p['part_text']}")
        out.append("")
    (ROOT / b_dir / "COMPARE.md").write_text("\n".join(out))
    print("\n".join(out[:4 + 2 * len(occs) + 4]))


if __name__ == "__main__":
    main()
