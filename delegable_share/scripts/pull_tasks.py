"""Download O*NET and Eloundou et al. labels, and build the task lists.

Stage 1 (download, skipped with --skip-download) writes into delegable_share/data/raw/
(git-ignored):
  onet/db_31_0_text.zip, onet/db_31_0_text/*.txt   O*NET 31.0, tab-delimited text release
  eloundou/*                                       github.com/openai/GPTs-are-GPTs, pinned commit
  manifest.json                                    URL, time (UTC), bytes, SHA-256 per file

Stage 2 (build) writes into delegable_share/data/:
  pilot_tasks.csv          one row per O*NET task statement, 3 pilot occupations
  bpo_tasks.csv            same, 13 BPO occupations
  comparison_tasks.csv     same, 16 hand-picked comparison occupations (control_group column)
  occupation_summary.csv   per-occupation checks: code exists, task counts, ratings, Eloundou match

Downloaded files are untrusted data: this script only writes bytes, unzips with a path check
and parses tables. Nothing downloaded is executed. Run with `python3 -I`.

Usage (from anywhere):
  python3 -I delegable_share/scripts/pull_tasks.py                 # download if missing, then build
  python3 -I delegable_share/scripts/pull_tasks.py --force         # re-download everything
  python3 -I delegable_share/scripts/pull_tasks.py --skip-download # rebuild from data/raw only
"""

import argparse
import datetime as dt
import difflib
import hashlib
import json
import pathlib
import re
import shutil
import urllib.request
import zipfile

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]  # delegable_share/
DATA = ROOT / "data"
RAW = DATA / "raw"

# --------------------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------------------
ONET_VERSION = "31.0"  # August 2026 release, current production database as of 2026-11-09
ONET_TAG = "db_31_0_text"
ONET_URL = f"https://www.onetcenter.org/dl_files/database/{ONET_TAG}.zip"
ONET_DIR = RAW / "onet" / ONET_TAG

# Pin the Eloundou repo to a commit so the labels cannot change under us.
ELOUNDOU_COMMIT = "0471612fef3cc22b74fb884d27bff9dbd3770582"  # 2025-10-04, "Update README.md"
ELOUNDOU_BASE = f"https://raw.githubusercontent.com/openai/GPTs-are-GPTs/{ELOUNDOU_COMMIT}/"
ELOUNDOU_FILES = [
    "README.md",
    "LICENSE",
    "data/full_labelset.tsv",                 # task-level exposure labels, human + GPT-4 (main file)
    "data/automation_gpt4_human_labels.tsv",  # automation (T0-T4) labels, GPT-4 + human
    "data/full_onet_data.tsv",                # their O*NET 27.2 task table with core/equal weights
    "data/occ_level.csv",                     # occupation-level scores
]
ELOUNDOU_PAPER_URL = "https://arxiv.org/pdf/2303.10130v5"
EL_DIR = RAW / "eloundou"

# --------------------------------------------------------------------------------------
# Occupation sets
# --------------------------------------------------------------------------------------
PILOT = ["15-1232.00", "43-4051.00", "15-1253.00"]
BPO = [
    "15-1252.00", "15-1254.00", "15-1253.00", "15-1232.00", "15-1244.00", "15-1242.00",
    "15-1211.00", "43-4051.00", "43-3031.00", "43-3021.00", "43-9021.00", "43-9041.00",
    "29-2072.00",
]
# Hand-picked comparison set (2026-11-10): positive controls (text/computer work, short items),
# negative controls (physical or interpersonal), and white-collar occupations outside IT/BPO.
# Excludes the pilot, the BPO set, and the occupations used as worked examples in the prompts
# (43-6014 Secretaries, 13-1161 Market Research, 13-1071 HR Specialists, 43-4171 Receptionists).
COMPARISON = {
    "27-3091.00": "positive", "43-9081.00": "positive", "27-3042.00": "positive",
    "23-2011.00": "positive", "13-2082.00": "positive",
    "47-2111.00": "negative", "29-1141.00": "negative", "39-9011.00": "negative",
    "37-2011.00": "negative", "53-3032.00": "negative",
    "13-2011.00": "white_collar", "23-1011.00": "white_collar", "13-2041.00": "white_collar",
    "25-2031.00": "white_collar", "41-4012.00": "white_collar", "13-1111.00": "white_collar",
}
# Second wave (2026-11-10): more IT/BPO service lines, and high-employment occupations across the
# economy. Same exclusions as COMPARISON.
MORE = {
    "15-1251.00": "bpo_extra", "15-1212.00": "bpo_extra", "41-9041.00": "bpo_extra", "43-3051.00": "bpo_extra",
    "43-3011.00": "bpo_extra", "31-9094.00": "bpo_extra", "15-2051.00": "bpo_extra",
    "41-2031.00": "general", "41-2011.00": "general", "43-9061.00": "general", "11-1021.00": "general",
    "13-1082.00": "general", "25-2021.00": "general", "31-9092.00": "general", "47-2061.00": "general",
    "35-2014.00": "general", "33-3051.00": "general", "41-3021.00": "general", "27-1024.00": "general",
    "11-2021.00": "general", "13-2072.00": "general",
    # 29 more high-employment occupations across all major SOC groups (user asked for ~50 in this wave)
    "11-3021.00": "general", "11-9111.00": "general", "13-2031.00": "general", "13-1151.00": "general",
    "13-1041.00": "general", "15-2031.00": "general", "17-2051.00": "general", "17-2141.00": "general",
    "19-3011.00": "general", "21-1021.00": "general", "27-3031.00": "general", "27-3041.00": "general",
    "29-2061.00": "general", "29-1051.00": "general", "31-1121.00": "general", "33-9032.00": "general",
    "35-3031.00": "general", "35-3023.00": "general", "37-3011.00": "general", "41-1011.00": "general",
    "41-9022.00": "general", "43-5071.00": "general", "43-6013.00": "general", "43-1011.00": "general",
    "47-2031.00": "general", "49-9071.00": "general", "51-2092.00": "general", "53-7062.00": "general",
    "53-7065.00": "general",
}

# --------------------------------------------------------------------------------------
# Frequency (FT) method
# --------------------------------------------------------------------------------------
# O*NET FT gives, for each task, the percent of respondents choosing each of 7 categories.
# freq_mean_cat  = sum_k p_k * k            (k = 1..7; p normalised to sum to 1)
# freq_per_year  = sum_k p_k * r_k          (r_k = assumed occurrences per year, below)
# freq_pct_daily_plus = 100 * sum_{k>=5} p_k (share reporting daily or more often)
# r_k: geometric midpoint of each band, assuming 260 working days and 8 working hours a day.
# The two end categories are open, so r_1 and r_7 are bounds, not midpoints.
FT_PER_YEAR = {
    1: 1.0,     # Yearly or less                -> once a year (upper bound)
    2: 3.5,     # More than yearly (<= monthly)  -> sqrt(1 * 12)
    3: 25.0,    # More than monthly (<= weekly)  -> sqrt(12 * 52)
    4: 116.0,   # More than weekly (< daily)     -> sqrt(52 * 260)
    5: 260.0,   # Daily                          -> once per working day
    6: 1040.0,  # Several times daily (< hourly) -> sqrt(2 * 8) = 4 per day
    7: 2080.0,  # Hourly or more                 -> 8 per day (lower bound)
}


# ======================================================================================
# Stage 1: download
# ======================================================================================
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, dest, force=False):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print(f"  exists, skipping: {dest.relative_to(ROOT)}")
    else:
        print(f"  GET {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "delegable-share-research/0.1"})
        with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
    return {
        "url": url,
        "path": str(dest.relative_to(ROOT)),
        "bytes": dest.stat().st_size,
        "sha256": sha256(dest),
        "downloaded_utc": dt.datetime.fromtimestamp(dest.stat().st_mtime, dt.timezone.utc)
        .isoformat(timespec="seconds"),
    }


def safe_extract(zip_path, out_dir):
    out_dir = out_dir.resolve()
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            target = (out_dir / info.filename).resolve()
            if out_dir not in target.parents and target != out_dir:
                raise RuntimeError(f"unsafe path in zip: {info.filename}")
        z.extractall(out_dir)


def download(force=False):
    manifest = {
        "onet": {"version": ONET_VERSION, "release": "August 2026"},
        "eloundou": {"repo": "https://github.com/openai/GPTs-are-GPTs", "commit": ELOUNDOU_COMMIT},
    }
    print("O*NET")
    zip_path = RAW / "onet" / f"{ONET_TAG}.zip"
    manifest["onet"]["zip"] = fetch(ONET_URL, zip_path, force)
    if force or not ONET_DIR.exists():
        safe_extract(zip_path, RAW / "onet")
    manifest["onet"]["extracted_to"] = str(ONET_DIR.relative_to(ROOT))

    print("Eloundou et al.")
    manifest["eloundou"]["files"] = [
        fetch(ELOUNDOU_BASE + f, EL_DIR / pathlib.Path(f).name, force) for f in ELOUNDOU_FILES
    ]
    manifest["eloundou"]["paper"] = fetch(
        ELOUNDOU_PAPER_URL, EL_DIR / "eloundou_2303.10130v5.pdf", force
    )
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {(RAW / 'manifest.json').relative_to(ROOT)}")


# ======================================================================================
# Stage 2: build
# ======================================================================================
def norm_text(s):
    """Normalise a task statement for exact-text matching: trim, strip wrapping quotes,
    collapse whitespace. Case and punctuation are kept, so this is still an exact match."""
    if not isinstance(s, str):
        return ""
    s = s.strip().strip('"').strip()
    return re.sub(r"\s+", " ", s)


def sim(a, b):
    return round(difflib.SequenceMatcher(None, norm_text(a).lower(), norm_text(b).lower()).ratio(), 3)


def read_onet(name):
    return pd.read_csv(ONET_DIR / f"{name}.txt", sep="\t", dtype={"O*NET-SOC Code": str}, keep_default_na=True)


def load_onet():
    occ = read_onet("Occupation Data").rename(columns={
        "O*NET-SOC Code": "onetsoc_code", "Title": "occupation_title", "Description": "occupation_description"})
    ts = read_onet("Task Statements").rename(columns={
        "O*NET-SOC Code": "onetsoc_code", "Task ID": "task_id", "Task": "task_statement",
        "Task Type": "task_type", "Incumbents Responding": "task_incumbents_responding",
        "Date": "task_date", "Domain Source": "task_domain_source"})
    tr = read_onet("Task Ratings").rename(columns={"O*NET-SOC Code": "onetsoc_code", "Task ID": "task_id"})
    t2d = read_onet("Tasks to DWAs").rename(columns={"O*NET-SOC Code": "onetsoc_code", "Task ID": "task_id"})
    dwa = read_onet("GWAs to IWAs to DWAs")[["DWA Element ID", "DWA Element Name"]].drop_duplicates()
    return occ, ts, tr, t2d, dwa


def ratings_wide(tr):
    key = ["onetsoc_code", "task_id"]
    out = []
    for scale, p in [("IM", "im"), ("RT", "rt")]:
        s = tr[tr["Scale ID"] == scale].set_index(key)
        out.append(pd.DataFrame({
            p: s["Data Value"],
            f"{p}_n": s["N"],
            f"{p}_se": s["Standard Error"],
            f"{p}_ci_lower": s["Lower CI Bound"],
            f"{p}_ci_upper": s["Upper CI Bound"],
            f"{p}_suppress": s["Recommend Suppress"],
        }))
    # Date and source of the ratings (taken from IM; identical across scales for a task)
    s = tr[tr["Scale ID"] == "IM"].set_index(key)
    out.append(pd.DataFrame({"ratings_date": s["Date"], "ratings_domain_source": s["Domain Source"]}))

    ft = tr[tr["Scale ID"] == "FT"].copy()
    ft["Category"] = ft["Category"].astype(int)
    pct = ft.pivot_table(index=key, columns="Category", values="Data Value", aggfunc="first")
    pct = pct.reindex(columns=range(1, 8))
    p = pct.div(pct.sum(axis=1), axis=0)  # category sums are 100 +/- rounding
    cats = np.arange(1, 8)
    rates = np.array([FT_PER_YEAR[k] for k in cats])
    ftw = pd.DataFrame(index=pct.index)
    ftw["freq_mean_cat"] = (p.values * cats).sum(axis=1).round(3)
    ftw["freq_per_year"] = (p.values * rates).sum(axis=1).round(1)
    ftw["freq_pct_daily_plus"] = (100 * p[[5, 6, 7]].sum(axis=1)).round(2)
    for k in cats:
        ftw[f"ft_pct_{k}"] = pct[k]
    g = ft.groupby(key)
    ftw["ft_n"] = g["N"].max()
    ftw["ft_suppress_n"] = g["Recommend Suppress"].apply(lambda x: int((x == "Y").sum()))
    ftw["ft_suppress_flagged"] = g["Recommend Suppress"].apply(lambda x: x.notna().any())
    out.append(ftw)
    w = pd.concat(out, axis=1).reset_index()
    # ft_suppress_n is only meaningful where flags exist (Incumbent data); blank it otherwise
    w.loc[~w["ft_suppress_flagged"].astype(bool), "ft_suppress_n"] = np.nan
    return w.drop(columns="ft_suppress_flagged")


def dwa_lists(t2d, dwa):
    m = t2d.merge(dwa, on="DWA Element ID", how="left").sort_values(["onetsoc_code", "task_id", "DWA Element ID"])
    g = m.groupby(["onetsoc_code", "task_id"])
    return pd.DataFrame({
        "dwa_ids": g["DWA Element ID"].apply(lambda x: "; ".join(x)),
        "dwa_titles": g["DWA Element Name"].apply(lambda x: " | ".join(x.fillna(""))),
    }).reset_index()


EXPOSURE_SCORE = {  # per-task versions of Eloundou's alpha / beta / gamma (zeta in paper v5)
    "alpha": {"E0": 0.0, "E1": 1.0, "E2": 0.0},
    "beta": {"E0": 0.0, "E1": 1.0, "E2": 0.5},
    "gamma": {"E0": 0.0, "E1": 1.0, "E2": 1.0},
}


def load_eloundou():
    el = pd.read_csv(EL_DIR / "full_labelset.tsv", sep="\t", index_col=0, dtype={"O*NET-SOC Code": str})
    el["Task ID"] = el["Task ID"].astype(int)
    # Sanity checks on what the README says: alpha/beta/gamma columns are GPT-4 (rubric 1),
    # human_labels duplicates human_exposure_agg.
    for k, mp in EXPOSURE_SCORE.items():
        assert (el["gpt4_exposure"].map(mp) == el[k]).all(), f"{k} is not derived from gpt4_exposure"
    assert (el["human_labels"] == el["human_exposure_agg"]).all()
    assert not el["Task ID"].duplicated().any()

    auto = pd.read_csv(EL_DIR / "automation_gpt4_human_labels.tsv", sep="\t", dtype={"O*NET-SOC Code": str})
    auto = auto[["Task ID", "human_automation"]].drop_duplicates("Task ID")
    el = el.merge(auto, on="Task ID", how="left")

    out = pd.DataFrame({
        "el_task_id": el["Task ID"],
        "el_onetsoc_code": el["O*NET-SOC Code"],
        "el_task_text": el["Task"],
        "el_task_type": el["Task Type"],
        "el_human_exposure": el["human_exposure_agg"],
        "el_gpt4_exposure": el["gpt4_exposure"],
        "el_gpt4_exposure_alt_rubric": el["gpt4_exposure_alt_rubric"],
    })
    for k, mp in EXPOSURE_SCORE.items():
        out[f"el_human_{k}"] = el["human_exposure_agg"].map(mp)
    for k in EXPOSURE_SCORE:
        out[f"el_gpt4_{k}"] = el[k]
    out["el_gpt3_relevant"] = el["gpt_3_relevant"]
    out["el_gpt4_automation"] = el["gpt4_automation"]
    out["el_human_automation"] = el["human_automation"]
    out["el_gpt4_automation_score"] = el["automation"]
    out["_norm"] = el["Task"].map(norm_text)
    return out


def match_eloundou(tasks, el):
    """Attach Eloundou labels to each O*NET task.
    1. task_id: same O*NET Task ID.
    2. text:    no ID match, but the normalised statement equals an Eloundou statement
                (same occupation preferred, then any occupation).
    3. none:    no match; record the most similar Eloundou statement in the same occupation."""
    by_id = el.set_index("el_task_id", drop=False)
    by_text = el.drop_duplicates(["_norm", "el_onetsoc_code"])
    rows = []
    for _, t in tasks.iterrows():
        rec = {"_key": (t.onetsoc_code, t.task_id)}
        if t.task_id in by_id.index:
            e = by_id.loc[t.task_id]
            rec["eloundou_match"] = "task_id"
        else:
            n = norm_text(t.task_statement)
            cand = by_text[by_text["_norm"] == n]
            same = cand[cand["el_onetsoc_code"] == t.onetsoc_code]
            cand = same if len(same) else cand
            if len(cand):
                e = cand.iloc[0]
                rec["eloundou_match"] = "text"
            else:
                e = None
                rec["eloundou_match"] = "none"
        if e is not None:
            rec.update({c: e[c] for c in el.columns if c != "_norm"})
            rec["el_text_identical"] = norm_text(e["el_task_text"]) == norm_text(t.task_statement)
            rec["el_text_similarity"] = sim(e["el_task_text"], t.task_statement)
        else:
            pool = el[el["el_onetsoc_code"] == t.onetsoc_code]
            if len(pool):
                sims = pool["el_task_text"].map(lambda x: sim(x, t.task_statement))
                j = sims.idxmax()
                rec["el_nearest_task_id"] = pool.loc[j, "el_task_id"]
                rec["el_nearest_similarity"] = sims[j]
                rec["el_nearest_task_text"] = pool.loc[j, "el_task_text"]
        rows.append(rec)
    m = pd.DataFrame(rows)
    for c in ["el_text_identical", "el_text_similarity", "el_nearest_task_id", "el_nearest_similarity",
              "el_nearest_task_text", *[c for c in el.columns if c != "_norm"]]:
        if c not in m.columns:
            m[c] = np.nan
    m[["onetsoc_code", "task_id"]] = pd.DataFrame(m.pop("_key").tolist(), index=m.index)
    return tasks.merge(m, on=["onetsoc_code", "task_id"], how="left")


COLUMNS = [
    "onetsoc_code", "occupation_title", "occupation_description",
    "task_id", "task_statement", "task_type", "task_incumbents_responding", "task_date", "task_domain_source",
    "has_ratings",
    "im", "im_n", "im_se", "im_ci_lower", "im_ci_upper", "im_suppress",
    "rt", "rt_n", "rt_se", "rt_ci_lower", "rt_ci_upper", "rt_suppress",
    "freq_mean_cat", "freq_per_year", "freq_pct_daily_plus",
    "ft_pct_1", "ft_pct_2", "ft_pct_3", "ft_pct_4", "ft_pct_5", "ft_pct_6", "ft_pct_7",
    "ft_n", "ft_suppress_n",
    "ratings_date", "ratings_domain_source",
    "dwa_ids", "dwa_titles",
    "eloundou_match", "el_task_id", "el_onetsoc_code", "el_task_type", "el_text_identical", "el_text_similarity",
    "el_task_text",
    "el_human_exposure", "el_gpt4_exposure", "el_gpt4_exposure_alt_rubric",
    "el_human_alpha", "el_human_beta", "el_human_gamma",
    "el_gpt4_alpha", "el_gpt4_beta", "el_gpt4_gamma",
    "el_gpt3_relevant", "el_gpt4_automation", "el_human_automation", "el_gpt4_automation_score",
    "el_nearest_task_id", "el_nearest_similarity", "el_nearest_task_text",
]


def build_set(codes, occ, ts, ratings, dwas, el):
    t = ts[ts["onetsoc_code"].isin(codes)].copy()
    t = t.merge(occ, on="onetsoc_code", how="left")
    t = t.merge(ratings, on=["onetsoc_code", "task_id"], how="left")
    t = t.merge(dwas, on=["onetsoc_code", "task_id"], how="left")
    t["has_ratings"] = t["im"].notna()
    t = match_eloundou(t, el)
    # Keep el_task_text only where it differs from the O*NET statement (saves width)
    t.loc[t["el_text_identical"] == True, "el_task_text"] = np.nan  # noqa: E712
    for c in ["task_incumbents_responding", "im_n", "rt_n", "ft_n", "ft_suppress_n", "el_task_id",
              "el_nearest_task_id"]:
        t[c] = t[c].astype("Int64")
    t["_order"] = t["onetsoc_code"].map({c: i for i, c in enumerate(codes)})
    t = t.sort_values(["_order", "task_id"]).drop(columns="_order")
    return t[COLUMNS]


def occupation_summary(codes, occ, ts, tr, el, built, set_name):
    rows = []
    for c in codes:
        o = occ[occ["onetsoc_code"] == c]
        b = built[built["onetsoc_code"] == c]
        e = el[el["el_onetsoc_code"] == c]
        siblings = sorted(set(occ.loc[occ["onetsoc_code"].str[:7] == c[:7], "onetsoc_code"]) - {c})
        notes = []
        if o.empty:
            notes.append("code not in O*NET 31.0 Occupation Data")
        if len(b) == 0:
            notes.append("no task statements")
        if len(b) and not b["has_ratings"].all():
            notes.append(f"{(~b['has_ratings']).sum()} task(s) without ratings")
        if len(b) and b["task_type"].isna().any():
            notes.append(f"{b['task_type'].isna().sum()} task(s) without Core/Supplemental type")
        if e.empty:
            notes.append("occupation absent from Eloundou labels")
        dropped = len(set(e["el_task_id"]) - set(b["task_id"]))
        if dropped:
            notes.append(f"{dropped} Eloundou (O*NET 27.2) task(s) no longer in 31.0 for this code")
        if siblings:
            notes.append("other O*NET codes under same SOC: " + ", ".join(siblings))
        rows.append({
            "set": set_name,
            "onetsoc_code": c,
            "occupation_title": o["occupation_title"].iloc[0] if len(o) else "",
            "in_onet_31": not o.empty,
            "n_tasks": len(b),
            "n_core": int((b["task_type"] == "Core").sum()),
            "n_supplemental": int((b["task_type"] == "Supplemental").sum()),
            "n_no_type": int(b["task_type"].isna().sum()),
            "n_with_im": int(b["im"].notna().sum()),
            "n_im_suppress_Y": int((b["im_suppress"] == "Y").sum()),
            "n_rt_suppress_Y": int((b["rt_suppress"] == "Y").sum()),
            "n_ft_any_suppress_Y": int((b["ft_suppress_n"].fillna(0) > 0).sum()),
            "task_dates": ", ".join(sorted(b["task_date"].dropna().unique())),
            "ratings_dates": ", ".join(sorted(b["ratings_date"].dropna().unique())),
            "ratings_sources": ", ".join(sorted(b["ratings_domain_source"].dropna().unique())),
            "n_el_tasks_for_code": len(e),
            "n_match_task_id": int((b["eloundou_match"] == "task_id").sum()),
            "n_match_task_id_text_differs": int(((b["eloundou_match"] == "task_id") & (b["el_text_identical"] == False)).sum()),  # noqa: E712
            "n_match_text": int((b["eloundou_match"] == "text").sum()),
            "n_match_none": int((b["eloundou_match"] == "none").sum()),
            "n_el_tasks_dropped": dropped,
            "n_task_type_differs_from_eloundou": int(
                (b.loc[b["eloundou_match"] != "none", "task_type"].fillna("none")
                 != b.loc[b["eloundou_match"] != "none", "el_task_type"].fillna("none")).sum()),
            "notes": "; ".join(notes),
        })
    return pd.DataFrame(rows)


def build():
    occ, ts, tr, t2d, dwa = load_onet()
    ratings = ratings_wide(tr)
    dwas = dwa_lists(t2d, dwa)
    el = load_eloundou()

    # Whole-database match statistics, for the README (same matcher as the task sets)
    allm = match_eloundou(ts[["onetsoc_code", "task_id", "task_statement", "task_date"]], el)
    vc = allm["eloundou_match"].value_counts()
    idm = allm[allm["eloundou_match"] == "task_id"]
    none = allm[allm["eloundou_match"] == "none"]
    stats = {
        "onet_tasks": len(ts),
        "onet_occupations_with_tasks": int(ts["onetsoc_code"].nunique()),
        "eloundou_tasks": len(el),
        "match_task_id": int(vc.get("task_id", 0)),
        "match_task_id_text_identical": int((idm["el_text_identical"] == True).sum()),  # noqa: E712
        "match_text": int(vc.get("text", 0)),
        "match_none": int(vc.get("none", 0)),
        "none_task_dates": none["task_date"].value_counts().to_dict(),
        "none_nearest_similarity_quartiles": none["el_nearest_similarity"].quantile([.25, .5, .75]).round(2).tolist(),
        "none_occupation_absent_from_eloundou": int(none["el_nearest_task_id"].isna().sum()),
        "eloundou_tasks_not_in_onet31": int((~el["el_task_id"].isin(ts["task_id"])).sum()),
    }
    (DATA / "eloundou_match_stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(f"O*NET {ONET_VERSION} whole-database Eloundou match: " + json.dumps(stats))

    summaries = []
    for name, codes in [("pilot", PILOT), ("bpo", BPO), ("comparison", list(COMPARISON)), ("more", list(MORE))]:
        built = build_set(codes, occ, ts, ratings, dwas, el)
        if name == "bpo":
            built.insert(0, "in_pilot", built["onetsoc_code"].isin(PILOT))
        if name == "comparison":
            built.insert(0, "control_group", built["onetsoc_code"].map(COMPARISON))
        if name == "more":
            built.insert(0, "control_group", built["onetsoc_code"].map(MORE))
        out = DATA / f"{name}_tasks.csv"
        built.to_csv(out, index=False)
        print(f"wrote {out.relative_to(ROOT)}: {len(built)} rows; "
              f"match {built['eloundou_match'].value_counts().to_dict()}")
        summaries.append(occupation_summary(codes, occ, ts, tr, el, built, name))
    s = pd.concat(summaries, ignore_index=True)
    s.to_csv(DATA / "occupation_summary.csv", index=False)
    print(f"wrote {(DATA / 'occupation_summary.csv').relative_to(ROOT)}")
    with pd.option_context("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 120):
        print(s.drop(columns=["task_dates", "ratings_dates"]).to_string())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download files that already exist")
    ap.add_argument("--skip-download", action="store_true", help="build from data/raw only")
    args = ap.parse_args()
    if not args.skip_download:
        download(args.force)
    build()


if __name__ == "__main__":
    main()
