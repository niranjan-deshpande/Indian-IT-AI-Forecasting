"""Feasibility probe: official price indices for IT services (p vs p/a).

Fetches (all free, no key):
  BLS PPI flat files  https://download.bls.gov/pub/time.series/{pc,wp}/
  BLS API v1 (ECI, CES) https://api.bls.gov/publicAPI/v1/timeseries/data/
  ONS SPPI JSON       https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/<cdid>/sppi/data
  BEA NIPA flat files https://apps.bea.gov/national/Release/TXT/NipaData{Q,A}.txt
Writes small extracts + stats to this folder. Raw downloads go to a temp dir and are discarded.
"""
import io, json, os, tempfile
import numpy as np, pandas as pd, requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
UA_BLS = {"User-Agent": "ndeshpande research ndeshpande@college.harvard.edu"}
UA_WEB = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
TMP = tempfile.mkdtemp()

# ---------------- series catalogue ----------------
BLS_FLAT = {  # series_id: (file, label, measures)
    "WPU4561": ("wp/wp.data.30.Services", "US PPI commodity: IT technical support & consulting (partial = produced by software publishers only; == PCU513210513210506)", "contract price, software-publisher support (not IT-services firms)"),
    "PCU513210513210506": ("pc/pc.data.53.Publishing", "US PPI: software publishers - maintenance, tech support & related services", "contract price"),
    "PCU518210518210": ("pc/pc.data.56.ISPsSearchPortandDataProcess", "US PPI: data processing, hosting & related (NAICS 518210)", "contract price (per service)"),
    "PCU5182105182101": ("pc/pc.data.56.ISPsSearchPortandDataProcess", "US PPI: 518210 - business process management services", "contract price (per service)"),
    "PCU541610541610": ("pc/pc.data.63.ProfessionalandTechnicalServ", "US PPI: management consulting (model pricing: hours x rates x realization)", "p/a (model)"),
}
BLS_API = {
    "CIU2025400000000I": ("US ECI wages & salaries, private, professional/scientific/technical services industry", "wage cost w"),
    "CIU2020000120000I": ("US ECI wages & salaries, private, professional & related occupations", "wage cost w"),
    "CEU6054150003": ("US CES avg hourly earnings, all employees, NAICS 5415 computer systems design", "wage cost w"),
}
ONS = {
    "HR6L": ("UK SPPI J62 computer programming, consultancy & related (domestic, 2015=100)", "p/a mostly (charge-out rates)"),
    "HRFE": ("UK SPPI J6202 computer consultancy services", "p/a mostly"),
    "HR6O": ("UK SPPI J6201 computer programming services", "p/a (time-based)"),
}
BEA_Q = {"B985RG": ("US BEA price index, private fixed investment in software (T5.3.4 l.17)", "input-cost based (circular)")}
BEA_A = {"Y003RG": "BEA T5.6.4 prepackaged software price (annual)",
         "Y004RG": "BEA T5.6.4 custom software price (annual)",
         "Y005RG": "BEA T5.6.4 own-account software price (annual)"}


def get(url, hdr, **kw):
    r = requests.get(url, headers=hdr, timeout=120, **kw)
    r.raise_for_status()
    return r


def bls_flat():
    out = {}
    files = {}
    for sid, (f, lab, m) in BLS_FLAT.items():
        if f not in files:
            files[f] = pd.read_csv(io.StringIO(get("https://download.bls.gov/pub/time.series/" + f, UA_BLS).text),
                                   sep="\t", dtype=str)
            files[f].columns = [c.strip() for c in files[f].columns]
            files[f]["series_id"] = files[f]["series_id"].str.strip()
        d = files[f][files[f].series_id == sid].copy()
        d = d[d.period.str.strip().str.match(r"M(0[1-9]|1[0-2])")]
        d["date"] = pd.PeriodIndex([f"{y.strip()}-{p.strip()[1:]}" for y, p in zip(d.year, d.period)], freq="M")
        out[sid] = d.set_index("date")["value"].astype(float).sort_index()
    return out


def bls_api():
    out = {}
    for a, b in [(2006, 2015), (2016, 2025), (2026, 2026)]:
        r = requests.post("https://api.bls.gov/publicAPI/v1/timeseries/data/", headers={**UA_BLS, "Content-Type": "application/json"},
                          data=json.dumps({"seriesid": list(BLS_API), "startyear": str(a), "endyear": str(b)}), timeout=120).json()
        assert r["status"] == "REQUEST_SUCCEEDED", r
        for s in r["Results"]["series"]:
            for x in s["data"]:
                p = x["period"]
                if p.startswith("Q"):
                    k = pd.Period(f"{x['year']}Q{int(p[1:])}", freq="Q")
                elif p.startswith("M") and p != "M13":
                    k = pd.Period(f"{x['year']}-{p[1:]}", freq="M")
                else:
                    continue
                out.setdefault(s["seriesID"], {})[k] = float(x["value"])
    return {k: pd.Series(v).sort_index() for k, v in out.items()}


def ons():
    out = {}
    for c in ONS:
        d = get(f"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/{c.lower()}/sppi/data", UA_WEB).json()
        s = {pd.Period(q["date"].replace(" ", ""), freq="Q"): float(q["value"]) for q in d["quarters"] if q["value"]}
        out[c] = pd.Series(s).sort_index()
    return out


def bea():
    q = pd.read_csv(io.StringIO(get("https://apps.bea.gov/national/Release/TXT/NipaDataQ.txt", UA_WEB).text), dtype=str)
    q.columns = ["code", "period", "value"]
    a = pd.read_csv(io.StringIO(get("https://apps.bea.gov/national/Release/TXT/NipaDataA.txt", UA_WEB).text), dtype=str)
    a.columns = ["code", "period", "value"]
    outq = {}
    for c in BEA_Q:
        d = q[q.code == c]
        outq[c] = pd.Series(d.value.str.replace(",", "").astype(float).values,
                            index=pd.PeriodIndex(d.period, freq="Q")).sort_index()
    outa = a[a.code.isin(BEA_A)].copy()
    outa["value"] = outa.value.str.replace(",", "").astype(float)
    return outq, outa


def to_q(s):
    if s.index.freqstr.startswith("M"):
        g = s.groupby(s.index.asfreq("Q"))
        s = g.mean()[g.count() == 3]
    return s


def yoy(sq):
    sq = sq.copy()
    return (100 * np.log(sq / sq.shift(4, freq="Q"))).dropna()


def noise(y):
    """brief item 4: 2015-2022 excl 2020Q2-2021Q2."""
    idx = y.index
    base = y[(idx >= pd.Period("2015Q1", "Q")) & (idx <= pd.Period("2022Q4", "Q"))
             & ~((idx >= pd.Period("2020Q2", "Q")) & (idx <= pd.Period("2021Q2", "Q")))]
    prev = base.index - 1
    ok = np.array([p in base.index for p in prev])  # consecutive in-sample pairs only (no lag across the COVID hole)
    x, z = base.reindex(prev[ok]).values, base[ok].values
    ar1 = np.polyfit(x, z, 1)[0] if len(x) > 4 else np.nan
    post = y[(idx >= pd.Period("2023Q1", "Q")) & (idx <= pd.Period("2026Q2", "Q"))]
    return dict(n=len(base), mean_1522=base.mean(), sd_1522=base.std(ddof=1), ar1=ar1,
                n_post=len(post), mean_2326=post.mean(), diff=post.mean() - base.mean(),
                last_q=str(y.index.max()), last_yoy=y.iloc[-1],
                y2023=post[post.index.year == 2023].mean(), y2024=post[post.index.year == 2024].mean(),
                y2025=post[post.index.year == 2025].mean(), y2026H1=post[post.index.year == 2026].mean())


def main():
    series, meta = {}, {}
    for k, v in bls_flat().items():
        series[k] = v; meta[k] = (BLS_FLAT[k][1], BLS_FLAT[k][2], "https://download.bls.gov/pub/time.series/" + BLS_FLAT[k][0])
    for k, v in bls_api().items():
        series[k] = v; meta[k] = (BLS_API[k][0], BLS_API[k][1], "https://api.bls.gov/publicAPI/v1/timeseries/data/" + k)
    for k, v in ons().items():
        series[k] = v; meta[k] = (ONS[k][0], ONS[k][1], f"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/{k.lower()}/sppi")
    bq, ba = bea()
    for k, v in bq.items():
        series[k] = v; meta[k] = (BEA_Q[k][0], BEA_Q[k][1], "https://apps.bea.gov/national/Release/TXT/NipaDataQ.txt")
    ba["label"] = ba.code.map(BEA_A)
    ba["source_url"] = "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"
    ba[ba.period.astype(int) >= 2005].to_csv(os.path.join(HERE, "bea_software_prices_annual.csv"), index=False)

    # quarterly levels + yoy (long format)
    rows, stats = [], []
    for k, s in series.items():
        sq = to_q(s)
        y = yoy(sq)
        for p, v in sq.items():
            rows.append(dict(series=k, cal_q=str(p), level=v, yoy_log100=y.get(p, np.nan)))
        st = noise(y); st.update(series=k, label=meta[k][0], maps_to=meta[k][1], source_url=meta[k][2],
                                 first_q=str(sq.index.min()))
        stats.append(st)
    q = pd.DataFrame(rows)
    q = q[q.cal_q >= "2005Q1"]
    q.to_csv(os.path.join(HERE, "price_indices_quarterly.csv"), index=False)
    st = pd.DataFrame(stats)[["series", "label", "maps_to", "first_q", "last_q", "n", "mean_1522", "sd_1522", "ar1",
                              "n_post", "mean_2326", "diff", "y2023", "y2024", "y2025", "y2026H1", "last_yoy", "source_url"]]
    st.round(3).to_csv(os.path.join(HERE, "noise_stats.csv"), index=False)
    pd.set_option("display.width", 250, "display.max_columns", 30)
    print(st.drop(columns=["label", "source_url"]).round(2).to_string())

    # price minus wage (markup / measured productivity proxy)
    w = q[q.series == "CIU2025400000000I"].set_index("cal_q").yoy_log100
    gap = []
    for k in ["WPU4561", "PCU541610541610", "PCU518210518210", "HR6L"]:
        p = q[q.series == k].set_index("cal_q").yoy_log100
        g = (p - w).dropna(); g.index = pd.PeriodIndex(g.index, freq="Q")
        s = noise(g); s.update(series=f"{k}_minus_ECI_PST"); gap.append(s)
    gap = pd.DataFrame(gap)[["series", "n", "mean_1522", "sd_1522", "ar1", "mean_2326", "diff", "y2023", "y2024", "y2025", "y2026H1"]]
    print("\nPrice YoY minus ECI (PST wages) YoY:\n", gap.round(2).to_string())
    gap.round(3).to_csv(os.path.join(HERE, "price_minus_wage_stats.csv"), index=False)

    # correlation with Indian-firm median gR, 2015-2022 (and excl COVID window)
    ym = pd.read_csv(os.path.join(ROOT, "data", "tidy", "yoy_metrics.csv"))
    ind = ym[ym.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"])]
    med = ind.groupby("cal_q").gR.median()
    cor = []
    for k in series:
        p = q[q.series == k].set_index("cal_q").yoy_log100
        df = pd.concat([p.rename("p"), med.rename("gR")], axis=1).dropna()
        df = df[(df.index >= "2015Q1") & (df.index <= "2022Q4")]
        ex = df[~((df.index >= "2020Q2") & (df.index <= "2021Q2"))]
        cor.append(dict(series=k, n=len(df), corr_all=df.p.corr(df.gR) if len(df) > 5 else np.nan,
                        n_excl=len(ex), corr_excl_covid=ex.p.corr(ex.gR) if len(ex) > 5 else np.nan))
    cor = pd.DataFrame(cor)
    print("\nCorr with Indian median gR 2015-2022:\n", cor.round(2).to_string())
    cor.round(3).to_csv(os.path.join(HERE, "corr_with_indian_gR.csv"), index=False)


if __name__ == "__main__":
    main()
