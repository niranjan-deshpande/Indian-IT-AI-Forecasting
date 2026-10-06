"""Earnings-call coding: reliability, disagreement list, spot-check sample, Figure 3.

    python3 scripts/final/calls_analysis.py

Inputs : audit/calls_statements.csv, audit/calls_coding_coder1.csv, audit/calls_coding_coder2.csv, audit/calls_transcripts.csv
Outputs: calls_disagreements.csv, calls_spotcheck.csv (repo root), output/final/calls_agreement.csv,
         output/final/fig3_data.csv, figures/final/fig3_call_categories.{png,svg}
Figure 3 uses coder 1's primary codes (disagreements are listed for resolution, not resolved here); a variant using
coder 2's codes is written as fig3_call_categories_coder2.{png,svg} so the reader can see whether the pattern depends on the coder.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT, FIG = ROOT / "output" / "final", ROOT / "figures" / "final"
OUT.mkdir(parents=True, exist_ok=True); FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams["svg.fonttype"] = "none"
CATS = ["A", "B", "C", "D", "E"]
CAT_NAME = {"A": "A. Demand weakness", "B": "B. Pricing stable", "C": "C. Pricing pressure, not AI",
            "D": "D. AI productivity passed to clients", "E": "E. Other / unclear"}

s = pd.read_csv(ROOT / "audit/calls_statements.csv")
c1 = pd.read_csv(ROOT / "audit/calls_coding_coder1.csv").rename(columns={"primary": "c1_primary", "secondary": "c1_secondary", "note": "c1_note"})
c2 = pd.read_csv(ROOT / "audit/calls_coding_coder2.csv").rename(columns={"primary": "c2_primary", "secondary": "c2_secondary", "note": "c2_note"})
for c, col in [(c1, "c1_primary"), (c2, "c2_primary")]:
    c[col] = c[col].astype(str).str.strip().str.upper()
    assert c.stmt_id.is_unique and set(c[col]) <= set(CATS), f"bad codes in {col}"
d = s.merge(c1, on="stmt_id", how="left").merge(c2, on="stmt_id", how="left")
assert d.c1_primary.notna().all() and d.c2_primary.notna().all(), "a coder file is incomplete"

# ---------------------------------------------------------------- agreement
n = len(d)
agree = (d.c1_primary == d.c2_primary)
po = agree.mean()
p1 = d.c1_primary.value_counts(normalize=True).reindex(CATS, fill_value=0)
p2 = d.c2_primary.value_counts(normalize=True).reindex(CATS, fill_value=0)
pe = (p1 * p2).sum()
kappa = (po - pe) / (1 - pe)
rows = [dict(category="overall", n_coder1=n, n_coder2=n, n_both=int(agree.sum()), percent_agreement=100 * po,
             positive_agreement=np.nan, cohen_kappa=kappa)]
for k in CATS:
    a, b = d.c1_primary == k, d.c2_primary == k
    both = int((a & b).sum())
    pa = 2 * both / (a.sum() + b.sum()) if (a.sum() + b.sum()) else np.nan
    # per-category kappa (category k vs not-k)
    po_k = ((a & b) | (~a & ~b)).mean(); pe_k = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    rows.append(dict(category=k, n_coder1=int(a.sum()), n_coder2=int(b.sum()), n_both=both,
                     percent_agreement=100 * both / a.sum() if a.sum() else np.nan,    # of coder 1's k, share coder 2 also coded k
                     positive_agreement=100 * pa, cohen_kappa=(po_k - pe_k) / (1 - pe_k)))
AG = pd.DataFrame(rows)
for sub, m in [("price pass only", d.source_pass == "price"), ("demand pass only", d.source_pass == "demand")]:
    x = d[m]
    AG = pd.concat([AG, pd.DataFrame([dict(category=f"overall, {sub}", n_coder1=len(x), n_coder2=len(x),
                                           n_both=int((x.c1_primary == x.c2_primary).sum()),
                                           percent_agreement=100 * (x.c1_primary == x.c2_primary).mean())])])
AG.round(3).to_csv(OUT / "calls_agreement.csv", index=False)
conf = pd.crosstab(d.c1_primary, d.c2_primary, rownames=["coder1"], colnames=["coder2"]).reindex(index=CATS, columns=CATS, fill_value=0)
conf.to_csv(OUT / "calls_confusion.csv")

cols = ["stmt_id", "firm", "call", "call_date", "half_year", "speaker", "quote", "c1_primary", "c1_secondary",
        "c2_primary", "c2_secondary", "c1_note", "c2_note", "source_pass", "source_url", "page"]
dis = d[~agree][cols].copy()
dis.insert(len(dis.columns), "resolved_primary", "")      # for the user to fill in
dis.to_csv(ROOT / "calls_disagreements.csv", index=False)
spot = d.sample(30, random_state=20261006)[cols].assign(check_correct_primary="", check_comment="")
spot.to_csv(ROOT / "calls_spotcheck.csv", index=False)

# ---------------------------------------------------------------- Figure 3
T = pd.read_csv(ROOT / "audit/calls_transcripts.csv")
HY = [f"{y}H{h}" for y in range(2021, 2027) for h in (1, 2)]
ntr = T.half_year.value_counts().reindex(HY, fill_value=0)
COL = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a", "D": "#e34948", "E": "#8a8984"}


def fig3(code_col, tag):
    cnt = d.groupby(["half_year", code_col]).size().unstack(fill_value=0).reindex(index=HY, columns=CATS, fill_value=0)
    per = cnt.div(ntr, axis=0)
    dd = d.assign(callkey=d.firm + " " + d.call)
    pres = dd.groupby(["half_year", code_col]).callkey.nunique().unstack(fill_value=0).reindex(index=HY, columns=CATS, fill_value=0)
    share = pres.div(ntr, axis=0)
    tab = pd.concat({"statements": cnt, "per_transcript": per.round(3), "share_of_transcripts_with_any": share.round(3)}, axis=1)
    tab["n_transcripts"] = ntr
    tab.to_csv(OUT / f"fig3_data{tag}.csv")
    x = np.arange(len(HY))
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, cats, title in [(axes[0], ["A", "E"], "Demand weakness (A) and other (E)"),
                            (axes[1], ["B", "C", "D"], "Pricing statements (B, C, D)")]:
        for k in cats:
            ax.plot(x, per[k], color=COL[k], lw=2.2, marker="o", ms=4, label=CAT_NAME[k])
            ax.text(x[-1] + 0.15, per[k].iloc[-1], k, color=COL[k], fontsize=9, va="center", fontweight="bold")
        ax.set_title(title, fontsize=9.5, loc="left")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{h[:4]}\nH{h[-1]}\nn={ntr[h]}" for h in HY], fontsize=7)
        ax.grid(axis="y", color="#e4e3df", lw=0.6)
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=7.5, frameon=False, loc="lower right" if "A" in cats else "upper left")
    axes[0].set_ylabel("statements per transcript (primary category)", fontsize=8)
    who = "coder 1" if tag == "" else "coder 2"
    fig.suptitle(f"Figure 3. Management statements per earnings-call transcript, by category and half-year ({who}'s primary codes)",
                 fontsize=10.5, x=0.01, ha="left")
    fig.text(0.01, 0.005, "n = transcripts in the half-year (8 firms; 2026H2 = calls to 5 Oct 2026). Panels use different scales: A/E come mostly "
             "from the demand re-scan (~9 statements per call),\nB/C/D from the pricing pass (~2 per call), so compare trends within a category, "
             "not levels across categories. Source: audit/calls_statements.csv; codebook calls_codebook.md.", fontsize=6.8, color="#52514e")
    fig.tight_layout(rect=[0, 0.08, 1, 0.94])
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"fig3_call_categories{tag}.{ext}", dpi=170)
    plt.close(fig)


fig3("c1_primary", "")
fig3("c2_primary", "_coder2")
print(AG.round(2).to_string()); print(conf); print("disagreements:", len(dis))
