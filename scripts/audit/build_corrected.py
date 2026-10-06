"""Corrected-data pipeline (audit). Rebuilds core_quarterly / yoy_metrics from data/raw with the audit corrections applied.

    python3 scripts/audit/build_corrected.py                 # apply every ROOT/audit/corrections_*.csv
    python3 scripts/audit/build_corrected.py --check-baseline # also rebuild with NO corrections and diff vs data/tidy
    python3 scripts/audit/build_corrected.py --only corrections_1b.csv   # apply a subset (glob in audit/, or absolute)
    python3 scripts/audit/build_corrected.py --only /abs/test_corr.csv --out /tmp/x   # test run, other output dir

Inputs : data/raw/*.csv (via the unmodified functions of scripts/01_build_tidy.py, imported with importlib)
         audit/corrections_*.csv with columns
           firm, cal_q, fiscal_q, column, dimension, old_value, new_value, action, reason, source_url, source_loc, evidence
         optional extra columns: unit, basis, period_type, doc_date (narrow a raw-metric match to one vintage);
                                 level (core | yoy | raw) to override the automatic choice below
Outputs: data/corrected/core_quarterly_corrected.csv
         data/corrected/yoy_metrics_corrected.csv
         data/corrected/CHANGELOG.csv  (one row per applied change: file, firm, cal_q, column, old, new, reason, source, ...)
         data/corrected/yoy_metrics_corrected_alt_ltimchain.csv  (ALTERNATIVE, not a correction: corrected yoy plus one
           'ltim_chain' entity = LTI-group growth-rate chain; see audit/findings_1b.md §6)

WHERE A CORRECTION APPLIES (decided from `column`, unless the optional `level` column says otherwise;
e.g. `headcount` is both a core column and a raw metric -> core by default, level=raw to fix every raw vintage):
  1. core level  - `column` is a column of core_quarterly (e.g. headcount, rev_usd, rev_cc_yoy, util0, subcon).
                   Changed after core_panel(), before yoy_metrics(), so YoY values are recomputed from it.
                   The companion <column>_src is set to the correction's source_url (replace) or emptied (set_missing).
                   If subcon / rev_inr / rev_usd(tcs) change, subcon_share is recomputed with 01_build_tidy's formula.
                   Only that one core column changes: a raw metric feeding several core columns (e.g. Infosys
                   utilization_excl_trainees -> util0 and util_excl) should be corrected at raw level instead.
  2. yoy level   - `column` is a column of yoy_metrics but not of core_quarterly (gR_usd, gL, du, gTCV, gRPE, resid ...).
                   Applied last, after yoy_metrics(); for gR/gL/du edits gRPE and resid are recomputed for that row.
                   Use only when no level series is consistent (e.g. accounting-basis mixes).
  3. raw level   - otherwise `column` is a raw `metric` name; rows of data/raw matching firm, cal_q, metric, dimension
                   (and fiscal_q / unit / basis / period_type when given) AND value == old_value are changed in every
                   vintage, then select_vintage/core_panel/yoy_metrics run as in 01_build_tidy.py.
                   set_missing drops those rows; if another vintage with a different value exists it is then
                   selected (logged in CHANGELOG as 'fallback vintage'). Use core-level set_missing to force a gap.
  `gR` is a yoy column but derived from core `rev_cc_yoy`: to change it correct rev_cc_yoy (core or raw level).
ACTIONS: replace (needs new_value) | set_missing | flag_only (no change; asserted and logged).
NOTATION: 'metric (raw, basis=reported)' in `column`, cal_q ranges 'A..B' and ';'-lists are accepted (see normalise()).
DUPLICATES: the same change listed in several files is applied once (CHANGELOG action 'duplicate'); a core/yoy
           correction whose target already equals new_value because a raw-level correction fixed it upstream is
           logged as 'duplicate' instead of failing.
ASSERTION: before any change, old_value must equal the value in the data, to the precision it is written with
           (|data - old| <= 0.5 * 10^-decimals of old_value as written; empty old_value = value must be missing).
           Any mismatch raises AssertionError and nothing is written.
"""
import argparse
import glob
import io
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_common import ROOT, SCRIPTS, AUD, CORR, load_module, ltim_chain  # noqa: E402

BT = load_module("build_tidy_01", SCRIPTS / "01_build_tidy.py")
REQ = ["firm", "cal_q", "fiscal_q", "column", "dimension", "old_value", "new_value", "action", "reason",
       "source_url", "source_loc", "evidence"]
OPT = ["unit", "basis", "period_type", "doc_date", "level"]


def tol(s):
    s = str(s).strip()
    if "." in s and "e" not in s.lower():
        return 0.5 * 10 ** -len(s.split(".")[1]) + 1e-12
    return 0.5 + 1e-12 if s.lstrip("-").isdigit() else 1e-9


def matches(val, old):
    old = "" if pd.isna(old) else str(old).strip()
    if old == "":
        return pd.isna(val)
    if pd.isna(val):
        return False
    return abs(float(val) - float(old)) <= tol(old)


def _is_num(x):
    try:
        float(str(x).strip())
        return True
    except ValueError:
        return False


def normalise(c):
    """Accept the variant notations used by the correction authors and expand them to one row per target:
    - column 'metric (raw, basis=reported)'   -> column=metric, level=raw, basis=reported (any k=v among
                                                 unit/basis/period_type/doc_date/level; bare raw|core|yoy = level)
    - cal_q 'A..B' (range) with old_value 'v1; v2; ...' (one per quarter, ';' or ',' separated) -> one row per quarter
    - several columns/dimensions separated by ';' (flag_only only)                -> one row per column
    Rows whose old_value is not numeric after expansion are allowed only for flag_only ('descriptive' = logged,
    not asserted)."""
    import re
    out = []
    for r in c.to_dict("records"):
        m = re.fullmatch(r"\s*([A-Za-z0-9_]+)\s*\((.*)\)\s*", r["column"])
        if m:
            r["column"] = m.group(1)
            for tok in [t.strip() for t in m.group(2).split(",") if t.strip()]:
                if "=" in tok:
                    k, v = [x.strip() for x in tok.split("=", 1)]
                    if not str(r.get(k, "")).strip():
                        r[k] = v
                elif tok in ("raw", "core", "yoy") and not str(r.get("level", "")).strip():
                    r["level"] = tok
        cols = [x.strip() for x in r["column"].split(";")]
        dims = [x.strip() for x in str(r["dimension"]).split(";")]
        if ".." in r["cal_q"]:
            a, b = [x.strip() for x in r["cal_q"].split("..")]
            qs = []
            q = a
            while q <= b:
                qs.append(q)
                y, n = int(q[:4]), int(q[-1])
                q = f"{y + (n == 4)}Q{n % 4 + 1}"
        else:
            qs = [r["cal_q"]]
        olds = [x.strip() for x in re.split(r"[;,]", str(r["old_value"])) if x.strip()]
        if len(qs) > 1 or len(cols) > 1:
            assert r["action"] == "flag_only", f"{r['corr_file']} line {r['corr_row']}: ranges / lists only allowed for flag_only"
        for qi, q in enumerate(qs):
            for ci, col in enumerate(cols):
                rr = dict(r)
                rr["cal_q"], rr["column"] = q, col
                rr["dimension"] = dims[ci] if len(dims) == len(cols) else dims[0]
                if len(qs) > 1:
                    rr["fiscal_q"] = ""
                    rr["old_value"] = olds[qi] if len(olds) == len(qs) and all(_is_num(o) for o in olds) else r["old_value"]
                ov = str(rr["old_value"]).strip()
                rr["descriptive"] = bool(ov) and not _is_num(ov)
                assert not rr["descriptive"] or rr["action"] == "flag_only", \
                    f"{r['corr_file']} line {r['corr_row']}: non-numeric old_value {ov!r} for {rr['action']}"
                out.append(rr)
    return pd.DataFrame(out)


def load_corrections(pattern):
    files = sorted(glob.glob(pattern if Path(pattern).is_absolute() else str(AUD / pattern)))
    frames = []
    for f in files:
        c = pd.read_csv(f, dtype=str, keep_default_na=False)
        missing = [k for k in REQ if k not in c.columns]
        assert not missing, f"{f}: missing columns {missing}"
        c["corr_file"] = Path(f).name
        c["corr_row"] = np.arange(len(c)) + 2      # spreadsheet line number
        frames.append(c)
    if not frames:
        return pd.DataFrame(columns=REQ + OPT + ["corr_file", "corr_row", "descriptive"])
    c = pd.concat(frames, ignore_index=True)
    for k in OPT:
        if k not in c.columns:
            c[k] = ""
    c = c.fillna("")
    for k in REQ + OPT:
        c[k] = c[k].astype(str).str.strip()
    bad = c[~c.action.isin(["replace", "set_missing", "flag_only"])]
    assert bad.empty, f"unknown action(s):\n{bad[['corr_file', 'corr_row', 'action']]}"
    bad = c[(c.action == "replace") & (c.new_value == "")]
    assert bad.empty, f"replace without new_value:\n{bad[['corr_file', 'corr_row']]}"
    return normalise(c)


def where(c):
    return f"{c.corr_file} line {c.corr_row} ({c.firm} {c.cal_q} {c.column})"


def build(corr, log):
    applied, removed = {}, {}             # raw rows already changed / removed: identical changes from several files apply once
    raw = BT.load_raw()
    # column sets used to classify each correction: taken from an uncorrected build (a few seconds)
    core_dry = BT.core_panel(BT.select_vintage(raw))
    core_cols = set(core_dry.columns) - {"firm", "cal_q"}
    yoy_cols = set(BT.yoy_metrics(core_dry).columns) - {"firm", "cal_q"}
    # ---------------------------------------------------------------- raw level
    corr = corr.copy()
    auto = np.where(corr.column.isin(core_cols), "core", np.where(corr.column.isin(yoy_cols - core_cols), "yoy", "raw"))
    lv = corr["level"].fillna("").astype(str).str.strip() if "level" in corr.columns else pd.Series("", index=corr.index)
    assert lv.isin(["", "core", "yoy", "raw"]).all(), "level must be core, yoy or raw"
    corr["level"] = np.where(lv != "", lv, auto)
    rawc = corr[corr.level == "raw"]
    for c in rawc.itertuples():
        m = (raw.firm == c.firm) & (raw.cal_q == c.cal_q) & (raw.metric == c.column)
        if c.dimension:
            m &= raw.dimension == c.dimension
        for k in ["fiscal_q", "unit", "basis", "period_type", "doc_date"]:
            v = getattr(c, k, "")
            if isinstance(v, str) and v.strip():
                col = raw[k].dt.strftime("%Y-%m-%d") if k == "doc_date" else raw[k]
                m &= col == v.strip()
        cand = raw[m]
        if c.descriptive:
            log.append(dict(level="raw", action="flag_only", n_rows=len(cand), old=c.old_value, new="", note="descriptive old_value, not asserted", c=c))
            continue
        hit = cand.index[[matches(v, c.old_value) for v in cand.value]]
        if not len(hit) and c.action != "flag_only":
            # identical change already applied to these raw rows by an earlier correction (e.g. listed in 1a and 1b)?
            prev = [applied[i] for i in cand.index if i in applied and applied[i][1:] == (c.action, c.new_value)]
            gone = [v for k, v in removed.items() if k[:4] == (c.firm, c.cal_q, c.column, c.dimension)] if c.action == "set_missing" else []
            if prev or gone:
                src = (prev or gone)[0][0]
                log.append(dict(level="raw", action="duplicate", n_rows=0, old=c.old_value, new=c.new_value,
                                note=f"same change already applied from {src}", c=c))
                continue
        assert len(cand), f"{where(c)}: no raw row matches firm/cal_q/metric/dimension"
        assert len(hit), f"{where(c)}: old_value {c.old_value!r} not found; raw values present: {sorted(set(cand.value.round(4)))}"
        if c.action == "replace":
            for i in hit:
                applied[i] = (f"{c.corr_file} line {c.corr_row}", c.action, c.new_value)
        elif c.action == "set_missing":
            removed[(c.firm, c.cal_q, c.column, c.dimension, c.old_value)] = (f"{c.corr_file} line {c.corr_row}",)
        if c.action == "flag_only":
            log.append(dict(level="raw", action="flag_only", n_rows=len(hit), old=c.old_value, new="", note="no change", c=c))
            continue
        if c.action == "replace":
            raw.loc[hit, "value"] = float(c.new_value)
            raw.loc[hit, "notes"] = raw.loc[hit, "notes"].fillna("").astype(str) + f" | AUDIT CORRECTION ({c.corr_file}): {c.old_value} -> {c.new_value}"
            if c.source_url:
                raw.loc[hit, "source_url"] = c.source_url
        else:
            raw = raw.drop(index=hit)
        log.append(dict(level="raw", action=c.action, n_rows=len(hit), old=c.old_value, new=c.new_value, note="all matching vintages", c=c))
    p = BT.select_vintage(raw)
    # fallback-vintage notes for raw set_missing
    for e in log:
        if e["level"] == "raw" and e["action"] == "set_missing":
            c = e["c"]
            k = (p.firm == c.firm) & (p.cal_q == c.cal_q) & (p.metric == c.column) & ((p.dimension == c.dimension) if c.dimension else True)
            if k.any():
                e["note"] = f"fallback vintage now used: {sorted(set(p[k].value.round(4)))}"
    core = BT.core_panel(p)
    # ---------------------------------------------------------------- core level
    for c in corr[corr.level == "core"].itertuples():
        i = core.index[(core.firm == c.firm) & (core.cal_q == c.cal_q)]
        assert len(i) == 1, f"{where(c)}: firm/cal_q not in core_quarterly"
        i = i[0]
        val = core.at[i, c.column]
        if c.descriptive:
            log.append(dict(level="core", action="flag_only", n_rows=1, old=c.old_value, new="", note="descriptive old_value, not asserted", c=c))
            continue
        if c.action != "flag_only" and not matches(val, c.old_value) and \
                ((c.action == "replace" and matches(val, c.new_value)) or (c.action == "set_missing" and pd.isna(val))):
            log.append(dict(level="core", action="duplicate", n_rows=0, old=c.old_value, new=c.new_value,
                            note="value already equals new_value (applied by an upstream/raw-level correction)", c=c))
            continue
        assert matches(val, c.old_value), f"{where(c)}: old_value {c.old_value!r} != core value {val!r}"
        if c.action == "flag_only":
            log.append(dict(level="core", action="flag_only", n_rows=1, old=c.old_value, new="", note="no change", c=c))
            continue
        core.at[i, c.column] = float(c.new_value) if c.action == "replace" else np.nan
        src = c.column + "_src"
        if src in core.columns:
            core.at[i, src] = (c.source_url or core.at[i, src]) if c.action == "replace" else np.nan
        note = ""
        if c.column in ("subcon", "rev_inr") or (c.column == "rev_usd" and c.firm == "tcs"):
            den = core.at[i, "rev_usd"] if c.firm == "tcs" else core.at[i, "rev_inr"]
            core.at[i, "subcon_share"] = 100 * core.at[i, "subcon"] / den
            note = "subcon_share recomputed"
        log.append(dict(level="core", action=c.action, n_rows=1, old=c.old_value, new=c.new_value, note=note, c=c))
    yoy = BT.yoy_metrics(core)
    # ---------------------------------------------------------------- yoy level
    for c in corr[corr.level == "yoy"].itertuples():
        i = yoy.index[(yoy.firm == c.firm) & (yoy.cal_q == c.cal_q)]
        assert len(i) == 1, f"{where(c)}: firm/cal_q not in yoy_metrics"
        i = i[0]
        val = yoy.at[i, c.column]
        if c.descriptive:
            log.append(dict(level="yoy", action="flag_only", n_rows=1, old=c.old_value, new="", note="descriptive old_value, not asserted", c=c))
            continue
        if c.action != "flag_only" and not matches(val, c.old_value) and \
                ((c.action == "replace" and matches(val, c.new_value)) or (c.action == "set_missing" and pd.isna(val))):
            log.append(dict(level="yoy", action="duplicate", n_rows=0, old=c.old_value, new=c.new_value,
                            note="value already equals new_value (applied by an upstream/raw-level correction)", c=c))
            continue
        assert matches(val, c.old_value), f"{where(c)}: old_value {c.old_value!r} != yoy value {val!r}"
        if c.action == "flag_only":
            log.append(dict(level="yoy", action="flag_only", n_rows=1, old=c.old_value, new="", note="no change", c=c))
            continue
        yoy.at[i, c.column] = float(c.new_value) if c.action == "replace" else np.nan
        note = ""
        if c.column in ("gR", "gL", "du"):
            yoy.at[i, "gRPE"] = yoy.at[i, "gR"] - yoy.at[i, "gL"]
            yoy.at[i, "resid"] = yoy.at[i, "gR"] - yoy.at[i, "gL"] - yoy.at[i, "du"]
            note = "gRPE/resid recomputed"
        log.append(dict(level="yoy", action=c.action, n_rows=1, old=c.old_value, new=c.new_value, note=note, c=c))
    return core, yoy


def csv_text(df):
    b = io.StringIO()
    df.to_csv(b, index=False)
    return b.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="corrections_*.csv", help="glob (inside audit/) of correction files to apply")
    ap.add_argument("--check-baseline", action="store_true", help="also rebuild with no corrections and diff vs data/tidy")
    ap.add_argument("--out", default=str(CORR), help="output directory (default data/corrected; use a scratch dir for tests)")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    if a.check_baseline:
        core0, yoy0 = build(load_corrections("__none__"), [])
        for name, df in [("core_quarterly.csv", core0), ("yoy_metrics.csv", yoy0)]:
            orig = (ROOT / "data" / "tidy" / name).read_text()
            new = csv_text(df)
            same = orig == new
            print(f"baseline check {name}: byte-identical={same} (rows {len(df)}, bytes {len(new)} vs {len(orig)})")
            if not same:
                o = pd.read_csv(io.StringIO(orig), low_memory=False)
                n = pd.read_csv(io.StringIO(new), low_memory=False)
                print("   shape", o.shape, n.shape, "frame-equal:", o.equals(n))
                raise SystemExit("baseline rebuild differs from data/tidy - investigate before trusting corrections")

    corr = load_corrections(a.only)
    print(f"{len(corr)} correction rows from {sorted(set(corr.corr_file))}")
    log = []
    core, yoy = build(corr, log)
    core.to_csv(out / "core_quarterly_corrected.csv", index=False)
    yoy.to_csv(out / "yoy_metrics_corrected.csv", index=False)
    alt = pd.concat([yoy, ltim_chain(yoy, core)], ignore_index=True)
    alt.to_csv(out / "yoy_metrics_corrected_alt_ltimchain.csv", index=False)
    ch = pd.DataFrame([dict(file=e["c"].corr_file, line=e["c"].corr_row, firm=e["c"].firm, cal_q=e["c"].cal_q,
                            fiscal_q=e["c"].fiscal_q, column=e["c"].column, dimension=e["c"].dimension,
                            level=e["level"], action=e["action"], old=e["old"], new=e["new"], n_rows=e["n_rows"],
                            reason=e["c"].reason, source=f"{e['c'].source_url} | {e['c'].source_loc}", note=e["note"])
                       for e in log],
                      columns=["file", "line", "firm", "cal_q", "fiscal_q", "column", "dimension", "level", "action",
                               "old", "new", "n_rows", "reason", "source", "note"])
    ch.to_csv(out / "CHANGELOG.csv", index=False)
    # summary of what actually differs from the pilot files
    o = pd.read_csv(ROOT / "data" / "tidy" / "yoy_metrics.csv")
    d = o.merge(yoy, on=["firm", "cal_q"], suffixes=("_o", "_c"), how="outer")
    nchg = {m: int(((d[m + "_o"] - d[m + "_c"]).abs() > 1e-9).sum() + (d[m + "_o"].isna() ^ d[m + "_c"].isna()).sum())
            for m in ["gR", "gR_usd", "gL", "du", "gTCV", "dsub", "gRPE", "resid"]}
    print("CHANGELOG rows:", len(ch), "| by action:", ch.action.value_counts().to_dict())
    print("yoy cells differing from data/tidy/yoy_metrics.csv:", nchg)


if __name__ == "__main__":
    main()
