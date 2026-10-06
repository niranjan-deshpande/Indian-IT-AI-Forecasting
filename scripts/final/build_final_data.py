"""Final-pass data build: applies the audit decisions (final pass, 2026-10) on top of the source-fixed pipeline.

    python3 scripts/final/build_final_data.py

Steps
  1. Raw data = data/raw/*.csv, except ltim.csv, which is rebuilt with the fixed parser into data/rebuilt/raw/ltim.csv
     (run `LTIM_OUT=data/rebuilt/raw/ltim.csv python3 scripts/extract/ltim_build.py` to regenerate it),
     plus audit/new_raw_accenture_q4fy26.csv (decision 5).
  2. Build functions = scripts/01_build_tidy.py with the fixed pick() (attrition: ltm ranked before quarter).
  3. REPRODUCTION CHECK: fixed pipeline (without the new Accenture rows) + the audit corrections that are NOT the two
     bugs now fixed at source must reproduce data/corrected/{core_quarterly,yoy_metrics}_corrected.csv exactly.
  4. Decisions applied for the final files:
       - HCLTech divestiture: adjust NEITHER revenue nor headcount (the divested business's revenue is not disclosed;
         the only figure is a forward-looking "80-bps impact" on FY25 guidance, Q1FY25 call). DIVEST is emptied.
       - Wipro: growth observations spanning the ISRE perimeter change (YoY windows 2017Q2-2018Q1, level-based:
         gR_usd, gL) and the Alight staff transfer in Q2FY19 (gL windows 2018Q3-2019Q2) set to missing; levels kept.
       - Accenture Q4FY26 added.
       - LTI counted once: done at aggregation time in scripts/final/tables_figures.py (no data change needed).
Outputs: data/corrected/core_quarterly_final.csv, yoy_metrics_final.csv, CHANGELOG.csv (= audit-round rows, kept in
         CHANGELOG_v1_audit.csv, + final-pass rows).
"""
import importlib.util
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CORR = ROOT / "data" / "corrected"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "audit"))
BC = load_module("build_corrected", ROOT / "scripts" / "audit" / "build_corrected.py")
BT = BC.BT                      # the (fixed) scripts/01_build_tidy.py, as imported by build_corrected
ORIG_LOAD_RAW = BT.load_raw
NEW_ACN = ROOT / "audit" / "new_raw_accenture_q4fy26.csv"
LTIM_FIXED = ROOT / "data" / "rebuilt" / "raw" / "ltim.csv"


def make_loader(include_new_accenture):
    def load_raw():
        files = [f for f in sorted((ROOT / "data" / "raw").glob("*.csv")) if f.name != "ltim.csv"] + [LTIM_FIXED]
        if include_new_accenture:
            files.append(NEW_ACN)
        frames = []
        for f in files:
            d = pd.read_csv(f, low_memory=False, dtype={"cal_q": str})
            d["raw_file"] = "gfc.csv" if f.name == "gfc.csv" else f.name
            frames.append(d)
        d = pd.concat(frames, ignore_index=True)
        d["value"] = pd.to_numeric(d["value"], errors="coerce")
        for c in ["dimension", "dim_type", "basis", "period_type", "unit"]:
            d[c] = d[c].fillna("na").astype(str).str.strip()
        d["doc_date"] = pd.to_datetime(d["doc_date"], errors="coerce")
        d["is_gfc_file"] = d.raw_file.eq("gfc.csv")
        return d
    return load_raw


def non_bug_corrections():
    """Audit corrections minus the two bugs now fixed at source (LTI/Mindtree sign; Cognizant attrition pick)."""
    c = BC.load_corrections("corrections_*.csv")
    bug = (c.firm.isin(["lti", "mindtree"]) & c.action.eq("replace")) | \
          (c.firm.eq("cognizant") & c.column.eq("attrition") & c.action.eq("replace"))
    return c[~bug].copy(), c[bug].copy()


def frames_equal(a, b, keys=("firm", "cal_q")):
    a = a.sort_values(list(keys)).reset_index(drop=True)
    b = b.sort_values(list(keys)).reset_index(drop=True)
    if a.shape != b.shape or list(a.columns) != list(b.columns):
        return False, f"shape/columns differ {a.shape} vs {b.shape}"
    bad = []
    for col in a.columns:
        x, y = a[col], b[col]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            ok = ((x - y).abs() < 1e-9) | (x.isna() & y.isna())
        else:
            ok = (x.astype(str) == y.astype(str))
        if not ok.all():
            bad.append((col, int((~ok).sum())))
    return not bad, bad


def main():
    corr, bug = non_bug_corrections()
    print(f"audit corrections: {len(corr) + len(bug)} rows; {len(bug)} are now fixed at source and not re-applied")

    # ---- 3. reproduction check
    BT.load_raw = make_loader(include_new_accenture=False)
    core_chk, yoy_chk = BC.build(corr, [])
    for name, df in [("core_quarterly_corrected.csv", core_chk), ("yoy_metrics_corrected.csv", yoy_chk)]:
        ref = pd.read_csv(CORR / name, dtype={"cal_q": str}, low_memory=False)
        df2 = pd.read_csv(pd.io.common.StringIO(df.to_csv(index=False)), dtype={"cal_q": str}, low_memory=False)
        ok, why = frames_equal(df2, ref)
        print(f"reproduction check vs data/corrected/{name}: {'IDENTICAL' if ok else 'DIFFERENT ' + str(why)}")
        if not ok:
            raise SystemExit("fixed pipeline does not reproduce data/corrected - stop")

    # ---- 4. final build
    BT.load_raw = make_loader(include_new_accenture=True)
    divest_before = dict(BT.DIVEST)
    BT.DIVEST.clear()                                    # HCLTech: adjust neither (see docstring)
    log = []
    core, yoy = BC.build(corr, log)
    BT.DIVEST.update(divest_before)

    changes = []
    # Wipro exclusions (growth observations only; levels kept)
    excl = {"gR_usd": [f"{y}Q{q}" for y, q in [(2017, 2), (2017, 3), (2017, 4), (2018, 1)]],
            "gL": [f"{y}Q{q}" for y, q in [(2017, 2), (2017, 3), (2017, 4), (2018, 1),
                                           (2018, 3), (2018, 4), (2019, 1), (2019, 2)]]}
    reason = {"2017Q2": "ISRE", "2017Q3": "ISRE", "2017Q4": "ISRE", "2018Q1": "ISRE",
              "2018Q3": "Alight", "2018Q4": "Alight", "2019Q1": "Alight", "2019Q2": "Alight"}
    for col, qs in excl.items():
        for q in qs:
            m = (yoy.firm == "wipro") & (yoy.cal_q == q)
            old = yoy.loc[m, col].iloc[0]
            yoy.loc[m, col] = np.nan
            why = ("YoY window spans the ISRE perimeter change: FY18 levels restated to exclude ISRE, FY17 base not "
                   "(Wipro Q3FY19 data sheet Note 1)") if reason[q] == "ISRE" else \
                  ("YoY window spans the ~9,000-employee Alight transfer in Q2FY19 (Wipro Q2FY19 call p15)")
            changes.append(dict(firm="wipro", cal_q=q, column=col, level="yoy", action="set_missing", old=old, new="",
                                reason=f"Final-pass decision 3: {why}"))
    yoy["gRPE"] = yoy.gR - yoy.gL
    yoy["resid"] = yoy.gR - yoy.gL - yoy.du

    # record the HCLTech divestiture removal and Accenture additions as changes vs the audit-round corrected file
    prev = pd.read_csv(CORR / "yoy_metrics_corrected.csv", dtype={"cal_q": str})
    d = prev.merge(yoy, on=["firm", "cal_q"], how="outer", suffixes=("_p", "_f"))
    for col in ["gR", "gR_usd", "gL", "du", "gTCV", "dsub", "gRPE", "resid"]:
        diff = d[~(((d[col + "_p"] - d[col + "_f"]).abs() < 1e-9) | (d[col + "_p"].isna() & d[col + "_f"].isna()))]
        for r in diff.itertuples():
            if r.firm == "wipro" and col in ("gR_usd", "gL"):
                continue                                    # logged above
            if r.firm == "hcltech":
                why = ("Final-pass decision 2: HCLTech divestiture - revenue of the divested State Street JV not disclosed "
                       "(only a forward-looking '80-bps impact' on FY25 guidance, Q1FY25 call), so neither revenue nor "
                       "headcount is adjusted; the 7,398 headcount base adjustment (D10) is removed")
            elif r.firm == "accenture":
                why = "Final-pass decision 5: Accenture Q4FY26 added from the 1 Oct 2026 8-K (audit/new_raw_accenture_q4fy26.csv)"
            elif r.firm == "wipro":
                why = "derived from the Wipro gL exclusion (decision 3)"
            else:
                why = "unexpected - investigate"
            changes.append(dict(firm=r.firm, cal_q=r.cal_q, column=col, level="yoy",
                                action="replace" if pd.notna(getattr(r, col + "_f")) else "set_missing",
                                old=getattr(r, col + "_p"), new=getattr(r, col + "_f"), reason=why))
    assert not any(c["reason"] == "unexpected - investigate" for c in changes), "unexpected yoy change"
    for _, r in pd.read_csv(NEW_ACN).iterrows():
        changes.append(dict(firm="accenture", cal_q=r.cal_q, column=r.metric, level="raw", action="add",
                            old="", new=r.value, reason=f"Final-pass decision 5 ({r.basis}): {r.source_loc}. {r.notes}",
                            source=r.source_url))
    # source fixes (decision 4): the audit corrections they replace
    for r in bug.itertuples():
        changes.append(dict(firm=r.firm, cal_q=r.cal_q, column=r.column, level="source", action="fixed_at_source",
                            old=r.old_value, new=r.new_value,
                            reason="Final-pass decision 4: now produced by the fixed pipeline (" +
                                   ("ltim_parse_tables.parse_num sign fix" if r.firm in ("lti", "mindtree")
                                    else "01_build_tidy.pick period-type ranking") + "); no longer applied as a correction"))

    core.to_csv(CORR / "core_quarterly_final.csv", index=False)
    yoy.to_csv(CORR / "yoy_metrics_final.csv", index=False)
    v1 = CORR / "CHANGELOG_v1_audit.csv"
    if not v1.exists():
        shutil.copy(CORR / "CHANGELOG.csv", v1)
    a = pd.read_csv(v1).assign(round="audit (Oct 2026), data/corrected/*_corrected.csv")
    b = pd.DataFrame(changes).assign(round="final pass (Oct 2026), data/corrected/*_final.csv")
    pd.concat([a, b], ignore_index=True).to_csv(CORR / "CHANGELOG.csv", index=False)
    print(f"final files written; final-pass changelog rows: {len(b)}")
    print(b.groupby(["firm", "column", "action"]).size().to_string())


if __name__ == "__main__":
    main()
