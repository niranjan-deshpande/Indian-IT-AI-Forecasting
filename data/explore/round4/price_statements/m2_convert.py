"""M2: convert classified management statements into an annualised, AI-incremental phi*s_bar per firm-year,
then aggregate to the top-six Indian IT firms (scope rule: one scope per equation) and to BPO.

All numbers are % per year, positive = price per unit of same-scope work FALLS. Pre-AI productivity
commitments (part of pi in the model) are netted out by construction (see rules R0-R4 below).

Rules
 R0 Baseline. Pre-AI productivity give-backs (TCS-31: 10-15% over a renewal term, 'not related to AI';
    analysts' 3-5%/yr; Accenture-14: >=10%/yr in managed services; HCL Q1 'annual productivity pass back')
    belong to pi, not phi*s. Only the AI-incremental part counts. k = share of a stated give-back that is
    AI-incremental: 1 when management says so (HCL), 0-1 when ambiguous (TCS).
 R1 Per-year portfolio rate stated net of baseline (HCL 2-3%): used directly.
 R2 One-off same-scope level discount D on deals repriced (LTIM ~15% vs a year earlier; HCL $100M->$80M):
    portfolio rate in a year = D * r * a, r = share of revenue repriced in that year, a = share of the
    portfolio in the affected service categories.
 R3 Give-back G spread over a contract term T (TCS 10-15% over tenure): per-contract rate g = G/T;
    portfolio rate = g * k * c_t, c_t = cumulative share of revenue on AI-era contract terms in year t.
 R4 Firms that give no number (Infosys, Wipro, TechM) get the revenue-weighted mean of the quantifying
    firms (TCS, HCLTech, LTIMindtree) as central, 0 as low and 2x central as high (representativeness).
"""
import csv

OUT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis/data/explore/round4/price_statements"
FY = ["FY24", "FY25", "FY26", "FY27"]  # FY24 = Apr 2023-Mar 2024 ... FY27 = Apr 2026-Mar 2027 (partly expectation)

# Trailing-4-quarter USD revenue, 2025Q3-2026Q2, $m (data/corrected/core_quarterly_final.csv)
REV = {"TCS": 30220, "Infosys": 20297, "HCLTech": 14769, "Wipro": 10505, "TechM": 6481, "LTIMindtree": 4834}

# Conversion parameters (low, central, high)
C_T = {"FY24": (0, 0, 0), "FY25": (0, 0.05, 0.10), "FY26": (0.15, 0.30, 0.45), "FY27": (0.45, 0.60, 0.75)}
#   c_t: cumulative share of revenue on AI-era terms. AI enters pricing from ~Q3FY25 (LTIMindtree-19, Oct-Dec 2024)
#   and Jan 2025 (NEW-CTSH-Q2CY26-b); Cognizant's fixed-price book 'roughly halfway' by mid-2026; T&M (about half
#   of revenue at Cognizant) reprices within 6-15 months (Cognizant-53).
R = (0.20, 0.275, 0.35)   # share of revenue repriced per year: 3-5 yr FP/managed-services terms, 24-36 months at Cognizant
A = (0.40, 0.50, 0.60)    # share of portfolio in AI-affected categories: HCL's 40% 'AI-disrupted' industry share; HCL portfolio more exposed
K = (0.0, 0.5, 1.0)       # AI-incremental share of TCS's 10-15% (TCS-31 says same size pre-AI)
G_T = (10 / 5, 12.5 / 4, 15 / 3)  # TCS: G over T -> g (%/yr per contract)
TCS_FY27_CAP = 2.0

# Pre-AI baseline give-back at portfolio level (part of pi; reported only to show GROSS = baseline + AI increment).
# Bounded assumption: no pre-2023 percentage found in primary sources (HCL FY23 calls, Health Net/Cognizant and
# Nielsen/TCS contracts: commitments exist, % redacted). Per-contract 2-5%/yr (TCS-31: 10-15% over 3-5-yr term;
# analysts' 3-5%/yr) x share of revenue on multi-year annuity/managed-services terms 0.40-0.55 (Accenture managed
# services 49.6%; Cognizant outsourcing 35.9%; Infosys FP 54%; Wipro FP+volume 52.4%).
BASE_IT = (2 * 0.40, 3.1 * 0.50, 5 * 0.55)
# BPO (Sagility only): gross 'cannibalisation' = revenue lost to efficiency on existing work, incl. offshoring.
#   pre-AI 100-150 bps/yr (EXT-BPO-12); 150-200 bps in May 2025 and Jan 2026 (EXT-BPO-00, -09); 'could increase to
#   200 bps over the near future' (Jul 2026, EXT-BPO-12); 4-5%/yr predicted in 2-3 yrs from May 2025 (EXT-BPO-01).
BASE_BPO = (1.0, 1.25, 1.5)
GROSS_BPO = {"FY24": (1.0, 1.25, 1.5), "FY25": (1.5, 1.75, 2.0), "FY26": (1.5, 1.75, 2.0), "FY27": (1.75, 2.25, 4.0)}


def tcs(fy):
    lo = G_T[0] * K[0] * C_T[fy][0]
    ce = G_T[1] * K[1] * C_T[fy][1]
    hi = G_T[2] * K[2] * C_T[fy][2]
    rule, ev = "R3: g=G/T (10-15% over 3-5 yrs) x k x c_t", "TCS-31;TCS-40;TCS-41;TCS-43;TCS-23"
    if fy == "FY27":  # Q2FY27 CFO: portfolio pricing 'broadly stable', revenue/employee 'slight reduction' -> cap
        hi = min(hi, TCS_FY27_CAP)
        rule += f"; high capped at {TCS_FY27_CAP} by Q2FY27 'broadly stable'"
        ev += ";EXT-TCS-Q2FY27-a;EXT-TCS-Q2FY27-b"
    return lo, ce, hi, rule, ev


def hcl(fy):
    v = {"FY24": (0, 0, 0), "FY25": (0, 0, 0.25), "FY26": (0, 0.25, 0.5), "FY27": (2.0, 2.5, 3.0)}[fy]
    rule = "R1: stated 2-3%/yr net of baseline from FY27; 'very little' in reported numbers to FY26" if fy != "FY24" else "R1: 'two to three years away' (Jul 2023)"
    return (*v, rule, "HCLTech-26;HCLTech-47;HCLTech-52;HCLTech-53;HCLTech-54;HCLTech-55;NEW-HCL-Q4FY26-a;NEW-HCL-Q4FY26-b")


def ltim(fy):
    if fy == "FY27":
        D = 15.0
        return (D * R[0] * A[0], D * R[1] * A[1], D * R[2] * A[2],
                "R2: D=15% same scope vs a year earlier x r x a", "LTIMindtree-46;NEW-LTIM-Q1FY27-a;LTIMindtree-45")
    v = {"FY24": (0, 0, 0), "FY25": (0.25, 0.5, 1.0), "FY26": (0.25, 0.75, 1.5)}[fy]
    return (*v, "judgement: single top-client give-backs (TMC -5.5% QoQ Q3FY25; top BFSI account FY26), no % on portfolio",
            "LTIMindtree-19;LTIMindtree-20;LTIMindtree-34;LTIMindtree-38;LTIMindtree-40;LTIMindtree-41")


QUANT = {"TCS": tcs, "HCLTech": hcl, "LTIMindtree": ltim}


def build():
    rows = []
    for fy in FY:
        q = {f: fn(fy) for f, fn in QUANT.items()}
        wq = sum(REV[f] for f in q)
        mean_q = sum(REV[f] * q[f][1] for f in q) / wq
        for f, (lo, ce, hi, rule, ev) in q.items():
            rows.append(dict(segment="IT", firm=f, fy=fy, low=lo, central=ce, high=hi, rule=rule, evidence=ev))
        for f in ["Infosys", "Wipro", "TechM"]:
            if fy == "FY24":
                lo, ce, hi = 0, 0, 0.25
            else:
                lo, ce, hi = 0, mean_q, 2 * mean_q
            ev = {"Infosys": "NEW-INFY-Q4FY26-a;NEW-INFY-Q4FY26-b;NEW-INFY-Q4FY26-c;Infosys-23;Infosys-30",
                  "Wipro": "(no quantified statement 2023-Q1FY27)",
                  "TechM": "TechM-37 (7% AI-only delivery productivity FY26);TechM-43"}[f]
            rows.append(dict(segment="IT", firm=f, fy=fy, low=lo, central=ce, high=hi,
                             rule="R4: mean of quantifying firms (0 to 2x)", evidence=ev))
    # FY24: no firm quantified any AI give-back; HCL 'two to three years away', TCS 'pricing environment is stable',
    # Accenture frames GenAI as continuing its pre-existing >=10% managed-services productivity. Allow up to 0.25.
    for r in rows:
        if r["fy"] == "FY24":
            r["low"], r["central"], r["high"] = 0.0, 0.0, 0.25
            r["rule"] = "FY24: no quantified AI give-back by any firm; HCL 'two to three years away'; TCS 'pricing environment is stable'"
            r["evidence"] = "HCLTech-26;Accenture-14"
    for fy in FY:
        g = GROSS_BPO[fy]
        # net = gross - baseline; low pairs low gross with high baseline, floored at 0
        lo, ce, hi = max(0.0, g[0] - BASE_BPO[2]), max(0.0, g[1] - BASE_BPO[1]), max(0.0, g[2] - BASE_BPO[0])
        if fy == "FY24":
            lo, ce, hi = 0.0, 0.0, 0.25
        rows.append(dict(segment="BPO", firm="Sagility (only quantifying BPO firm)", fy=fy, low=lo, central=ce, high=hi,
                         rule="gross cannibalisation minus pre-AI 100-150 bps (incl. offshoring)",
                         evidence="EXT-BPO-00;EXT-BPO-01;EXT-BPO-09;EXT-BPO-12;EXT-BPO-21 (eClerx: no annual pass-back asked)"))
    return rows


def aggregate(rows):
    W = sum(REV.values())
    agg = []
    for fy in FY:
        sub = [r for r in rows if r["fy"] == fy and r["segment"] == "IT"]
        d = {k: sum(REV[r["firm"]] * r[k] for r in sub) / W for k in ("low", "central", "high")}
        qshare = sum(REV[f] for f in QUANT) / W
        # bias-widened: manager bias factor m in [0.5, 2] on the statement-based range
        agg.append(dict(segment="IT top-6", fy=fy, low=d["low"], central=d["central"], high=d["high"],
                        low_bias_widened=0.5 * d["low"], high_bias_widened=2 * d["high"],
                        gross_low=BASE_IT[0] + d["low"], gross_central=BASE_IT[1] + d["central"],
                        gross_high=BASE_IT[2] + d["high"], baseline_central=BASE_IT[1],
                        weight_on_quantifying_firms=qshare))
        b = [r for r in rows if r["fy"] == fy and r["segment"] == "BPO"][0]
        g = GROSS_BPO[fy]
        agg.append(dict(segment="BPO (Sagility)", fy=fy, low=b["low"], central=b["central"], high=b["high"],
                        low_bias_widened=0.5 * b["low"], high_bias_widened=2 * b["high"],
                        gross_low=g[0], gross_central=g[1], gross_high=g[2], baseline_central=BASE_BPO[1],
                        weight_on_quantifying_firms=float("nan")))
    return agg


def breakdown(rows, agg):
    W = sum(REV.values())
    out = []
    a = {x["fy"]: x for x in agg if x["segment"] == "IT top-6"}
    avg = sum(a[f]["central"] for f in ("FY24", "FY25", "FY26")) / 3
    for thr in (1.0, 2.0):
        out.append(dict(test=f"FY24-26 average top-6 phi*s >= {thr} pp/yr", central=avg,
                        uniform_scale_needed=thr / avg if avg else float("inf"),
                        note="factor by which every firm's central would have to be understated"))
    for thr in (1.0, 2.0):
        sub = [r for r in rows if r["fy"] == "FY26" and r["segment"] == "IT"]
        q = sum(REV[r["firm"]] * r["central"] for r in sub if r["firm"] in QUANT)
        wn = sum(REV[f] for f in ("Infosys", "Wipro", "TechM"))
        need = (thr * W - q) / wn
        out.append(dict(test=f"FY26 top-6 phi*s >= {thr} pp/yr", central=a["FY26"]["central"],
                        uniform_scale_needed=thr / a["FY26"]["central"],
                        note=f"or: silent firms (Infosys, Wipro, TechM; {wn / W:.0%} of revenue) would need {need:.2f} pp/yr each, "
                             f"holding quantifying firms at central"))
    for thr in (1.0,):
        out.append(dict(test=f"FY27 top-6 phi*s < {thr} pp/yr", central=a["FY27"]["central"],
                        uniform_scale_needed=thr / a["FY27"]["central"],
                        note="factor by which FY27 statements would have to be overstated"))
    bp = {x["fy"]: x for x in agg if x["segment"].startswith("BPO")}
    out.append(dict(test="BPO FY26 AI increment >= 1 pp/yr", central=bp["FY26"]["central"],
                    uniform_scale_needed=1 / bp["FY26"]["central"],
                    note="equivalently: true pre-AI baseline would have to be <= 0.75 pp (vs 1.0-1.5 stated), "
                         "or Sagility's gross figure understated by >= 0.5 pp"))
    return out


def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    rows = build()
    agg = aggregate(rows)
    bd = breakdown(rows, agg)
    write(f"{OUT}/m2_firm_year.csv", rows)
    write(f"{OUT}/m2_aggregate.csv", agg)
    write(f"{OUT}/m2_breakdown.csv", bd)
    for x in agg:
        print(x["fy"], {k: round(v, 2) for k, v in x.items() if isinstance(v, float)})
    for x in bd:
        print(x)
