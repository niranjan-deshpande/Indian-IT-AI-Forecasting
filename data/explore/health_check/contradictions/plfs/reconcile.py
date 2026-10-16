"""Reconcile external PLFS-based claims (Future of India Substack, 2 Oct 2026; State of Working India 2026)
with this repo's PLFS pipeline. Reads the standardised unit-level parquet files that stay inside
data/sources/plfs/work (built by round3/plfs/extract_std.py) plus, for self-employment earnings only,
one column from the raw first-visit person files. Writes AGGREGATE, survey-weighted tables only
(estimate, linearised SE, unweighted n). No unit records are written or printed.

Source: PLFS unit-level data, MoSPI (NSO), used under the microdata.gov.in Data Access Agreement.

Usage: python3 -I reconcile.py WORK_DIR EXTRACTED_DIR MAPPING_CSV OUT_DIR
"""
import sys, os
import numpy as np
import pandas as pd

WORK, EXT, MAPF, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
ROUNDS = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "cy2024", "cy2025"]
WORKER = [11, 12, 21, 31, 41, 51]
Z90 = 1.645
# Raw variable holding CWS self-employment earnings (last 30 days), per round.
SELF_EARN = {"2017-18": "b6q10_per_fv", "2018-19": None, "2019-20": None, "2020-21": None, "2021-22": None,
             "2022-23": "b6q10_perv1", "2023-24": "b6q10_perv1", "cy2024": "CWS_Earnings_SelfEmployed",
             "cy2025": "ern_self"}
# CPI-Combined (base 2012=100) annual averages: FY rounds from RBI Handbook Table 37 (2017-18 135.0,
# 2022-23 174.7, 2023-24 184.1); CY2024 and CY2025 are simple means of the monthly base-2012 index
# (CY2025 = 195.1 incl. provisional Dec-2025; CY2024 approximated as 190.8). Rebased to CY2025 = 1.
CPI = {"2017-18": 135.0, "2022-23": 174.7, "2023-24": 184.1, "cy2024": 190.8, "cy2025": 195.1}


class Design:
    """Taylor-linearised, ultimate-cluster variance (same as round3/plfs/analyze.py)."""
    def __init__(self, d):
        self.w = d["w"].to_numpy(float)
        psu_codes, psu_uni = pd.factorize(d["psu"])
        self.psu = psu_codes
        strata_of_psu = d.groupby(psu_codes)["strata"].first()
        s_codes, _ = pd.factorize(strata_of_psu.sort_index())
        self.s = s_codes
        self.n_h = np.bincount(s_codes)
        self.npsu = len(psu_uni)

    def var_total(self, y):
        t = np.bincount(self.psu, weights=y, minlength=self.npsu)
        sh = np.bincount(self.s, weights=t)
        mean_h = sh / self.n_h
        dev2 = np.bincount(self.s, weights=(t - mean_h[self.s]) ** 2)
        f = np.where(self.n_h > 1, self.n_h / np.maximum(self.n_h - 1, 1), 0.0)
        return float((f * dev2).sum())

    def total(self, ind):
        y = self.w * ind.astype(float)
        return y.sum(), np.sqrt(self.var_total(y)), int(ind.sum())

    def ratio(self, num, den):
        num = num.astype(float); den = den.astype(float)
        Y, X = (self.w * num).sum(), (self.w * den).sum()
        R = Y / X if X > 0 else np.nan
        z = self.w * (num - R * den) / X
        return R, np.sqrt(self.var_total(z)), int((num > 0).sum()), int((den > 0).sum())


def wq(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(c, q)])


mp = pd.read_csv(MAPF, dtype=str).fillna("")
lev, shr, occ, earn, ur, sens = [], [], [], [], [], []

for rnd in ROUNDS:
    d = pd.read_parquet(os.path.join(WORK, f"{rnd}.parquet"))
    D = Design(d)
    age = d["age"].to_numpy()
    ps = d["ps_status"].isin(WORKER).to_numpy()
    ss = d["ss_status"].isin(WORKER).to_numpy()
    upss_w = ps | ss
    ps_u = (d["ps_status"] == 81).to_numpy()
    upss_u = ps_u & ~ss
    cws_w = d["cws_status"].between(11, 72).to_numpy()
    cws_u = d["cws_status"].isin([81, 82]).to_numpy()
    grad = d["gedu"].isin([12, 13]).to_numpy()
    reg = (d["ps_status"] == 31).to_numpy()
    n2 = d["ps_nic"].str.zfill(5).str[:2].to_numpy()
    it = np.isin(n2, ["62", "63"]) & ps
    nco = d["ps_nco"].str.zfill(3).to_numpy()
    a15 = age >= 15
    bands = {"15plus": a15, "21_25": (age >= 21) & (age <= 25), "26_29": (age >= 26) & (age <= 29),
             "30plus": age >= 30, "21_30": (age >= 21) & (age <= 30)}

    # ---- 1. IT employment levels (all ages, UPS NIC 62+63) ----
    T, se, n = D.total(it)
    lev.append(dict(round=rnd, series="it_62_63_all_ages_ups", estimate=T, se=se, n_unweighted=n,
                    plfs_weighted_pop=D.w.sum()))
    for b in ["21_25", "26_29", "30plus"]:
        T, se, n = D.total(it & reg & grad & bands[b])
        lev.append(dict(round=rnd, series=f"salaried_grad_it_{b}", estimate=T, se=se, n_unweighted=n,
                        plfs_weighted_pop=D.w.sum()))
    T, se, n = D.total(it & reg & grad)
    lev.append(dict(round=rnd, series="salaried_grad_it_all", estimate=T, se=se, n_unweighted=n,
                    plfs_weighted_pop=D.w.sum()))
    R, rse, nn, nd = D.ratio(it & reg & grad, it)
    shr.append(dict(round=rnd, measure="share_of_it_workers_that_are_salaried_grads", age="all",
                    share=R, se=rse, n_num=nn, n_den=nd))

    # ---- 2. IT shares of graduate groups (FOI definitions and variants) ----
    for b, bi in bands.items():
        # (a) salaried graduates: UPS status 31
        R, rse, nn, nd = D.ratio(it & reg & grad & bi, reg & grad & bi)
        shr.append(dict(round=rnd, measure="it_share_of_salaried_grads_ups31", age=b, share=R, se=rse, n_num=nn, n_den=nd))
        # (b) all employed graduates (our headline denominator)
        R, rse, nn, nd = D.ratio(it & grad & bi, ps & grad & bi)
        shr.append(dict(round=rnd, measure="it_share_of_employed_grads_ups", age=b, share=R, se=rse, n_num=nn, n_den=nd))
        # (c) graduates in the labour force (UPS)
        R, rse, nn, nd = D.ratio(it & grad & bi, (ps | ps_u) & grad & bi)
        shr.append(dict(round=rnd, measure="it_share_of_grad_labour_force_ups", age=b, share=R, se=rse, n_num=nn, n_den=nd))
        # (d) CWS regular wage workers (status 31/71/72), CWS NIC 62/63
        cr = d["cws_status"].isin([31, 71, 72]).to_numpy()
        cit = np.isin(d["cws_nic"].str.zfill(2).str[:2].to_numpy(), ["62", "63"])
        R, rse, nn, nd = D.ratio(cr & cit & grad & bi, cr & grad & bi)
        shr.append(dict(round=rnd, measure="it_share_of_salaried_grads_cws", age=b, share=R, se=rse, n_num=nn, n_den=nd))

    # ---- 3. Occupations within IT (NCO-2015 rounds only) ----
    if rnd not in ROUNDS[:4]:
        for lab, codes in [("nco251_dev_analysts", ["251"]), ("nco25_ict_professionals", ["251", "252"]),
                           ("nco413_keyboard_operators", ["413"]), ("nco351_ict_ops_support_tech", ["351"])]:
            sel = np.isin(nco, codes)
            T, se, n = D.total(it & sel)
            R, rse, _, _ = D.ratio(it & sel, it)
            occ.append(dict(round=rnd, occupation=lab, scope="in_it_62_63", estimate=T, se=se, n_unweighted=n,
                            share_of_it=R, share_se=rse))
            T, se, n = D.total(ps & sel)
            occ.append(dict(round=rnd, occupation=lab, scope="all_industries", estimate=T, se=se, n_unweighted=n,
                            share_of_it=np.nan, share_se=np.nan))

    # ---- 4. Earnings, CWS NIC 62/63 ----
    cit = np.isin(d["cws_nic"].str.zfill(2).str[:2].to_numpy(), ["62", "63"])
    er = d["earn_regular"].to_numpy(float)
    cs = d["cws_status"].to_numpy()
    if SELF_EARN[rnd]:
        g = mp[(mp["round"] == rnd)]
        rawf = os.path.join(EXT, g["file"].iloc[0])
        es = pd.read_stata(rawf, columns=[SELF_EARN[rnd], g.loc[g.std_var == "age", "source_var"].iloc[0]],
                           convert_categoricals=False)
        assert len(es) == len(d)
        assert (pd.to_numeric(es.iloc[:, 1], errors="coerce").to_numpy() == age).mean() > 0.999  # row alignment
        es = pd.to_numeric(es.iloc[:, 0], errors="coerce").to_numpy(float)
    else:
        es = np.full(len(d), np.nan)
    reg_e = np.isin(cs, [31, 71, 72]) & (er > 0)
    self_e = np.isin(cs, [11, 12, 21, 61, 62]) & (es > 0)
    any_e = np.where(reg_e, er, np.where(self_e, es, np.nan))
    defl = CPI["cy2025"] / CPI[rnd] if rnd in CPI else np.nan
    for samp, base, x in [("regular_wage", reg_e, er), ("regular_or_self_employed", reg_e | self_e, any_e)]:
        if samp == "regular_or_self_employed" and not SELF_EARN[rnd]:
            continue
        for b in ["all", "21_25", "30plus"]:
            bi = np.ones(len(d), bool) if b == "all" else bands[b]
            s = base & cit & bi
            if s.sum() == 0:
                continue
            mean, mse, _, _ = D.ratio(np.where(s, np.nan_to_num(x), 0.0), s)
            med = wq(x[s], D.w[s], 0.5)
            earn.append(dict(round=rnd, sample=samp, age=b, n_unweighted=int(s.sum()), median_nominal=med,
                             mean_nominal=mean, mean_se=mse, cpi_c=CPI.get(rnd, np.nan),
                             median_real_cy2025_prices=med * defl, mean_real_cy2025_prices=mean * defl))

    # ---- 5. Graduate unemployment (SWI reconciliation) ----
    ub = {"15_24": (15, 24), "15_25": (15, 25), "21_25": (21, 25), "20_24": (20, 24), "25_29": (25, 29),
          "26_29": (26, 29), "20_29": (20, 29), "15_29": (15, 29), "21_30": (21, 30)}
    male = (d["sex"] == 1).to_numpy()
    for lab, (lo, hi) in ub.items():
        pop = grad & (age >= lo) & (age <= hi)
        for sx, sxi in [("persons", np.ones(len(d), bool)), ("male", male), ("female", ~male)]:
            if sx != "persons" and lab not in ["15_25", "15_24", "21_25"]:
                continue
            p = pop & sxi
            for concept, u, lf in [("upss", upss_u, upss_w | upss_u), ("ups", ps_u, ps | ps_u), ("cws", cws_u, cws_w | cws_u)]:
                R, rse, nn, nd = D.ratio(u & p, lf & p)
                ur.append(dict(round=rnd, age=lab, sex=sx, concept=concept, ur=R, se=rse, n_unemp=nn, n_lf=nd))
        if lab in ["21_25", "21_30"]:  # engineering/technology degree holders (tedu 03)
            p = (d["tedu"] == 3).to_numpy() & (age >= lo) & (age <= hi)
            for concept, u, lf in [("upss", upss_u, upss_w | upss_u), ("ups", ps_u, ps | ps_u), ("cws", cws_u, cws_w | cws_u)]:
                R, rse, nn, nd = D.ratio(u & p, lf & p)
                ur.append(dict(round=rnd, age=lab, sex="persons_engdeg", concept=concept, ur=R, se=rse, n_unemp=nn, n_lf=nd))
        # count of unemployed (upss) and all graduates in the age band (for SWI "1.1 of 6.3 crore")
        if lab == "20_29":
            Tu, seu, nu = D.total(upss_u & pop)
            Tp, sep, npp = D.total(pop)
            sens.append(dict(round=rnd, item="grads_20_29_unemployed_upss", estimate=Tu, se=seu, n_unweighted=nu))
            sens.append(dict(round=rnd, item="grads_20_29_population", estimate=Tp, se=sep, n_unweighted=npp))

    # ---- 6. Sensitivity: drop the single most influential FSU (young-grad IT series) ----
    if rnd in ["2023-24", "cy2024"]:
        sel = it & grad & bands["21_30"]
        t = pd.Series(D.w * sel).groupby(d["fsu"].to_numpy()).sum().sort_values(ascending=False)
        keep = d["fsu"].to_numpy() != t.index[0]
        for lab, num in [("it_62_63_all_ages_ups", it), ("salaried_grad_it_21_25", it & reg & grad & bands["21_25"]),
                         ("salaried_grad_it_all", it & reg & grad)]:
            sens.append(dict(round=rnd, item=f"{lab}__excl_top_fsu", estimate=float((D.w * (num & keep)).sum()),
                             se=np.nan, n_unweighted=int((num & keep).sum())))
        R = (D.w * (it & reg & grad & bands["21_25"] & keep)).sum() / (D.w * (reg & grad & bands["21_25"] & keep)).sum()
        sens.append(dict(round=rnd, item="it_share_of_salaried_grads_21_25__excl_top_fsu", estimate=R, se=np.nan,
                         n_unweighted=int((it & reg & grad & bands["21_25"] & keep).sum())))
    print(rnd, "done", flush=True)


def ci(df, est, se):
    df["ci90_lo"] = df[est] - Z90 * df[se]
    df["ci90_hi"] = df[est] + Z90 * df[se]
    return df

ci(pd.DataFrame(lev), "estimate", "se").round(1).to_csv(os.path.join(OUT, "it_levels.csv"), index=False)
ci(pd.DataFrame(shr), "share", "se").round(5).to_csv(os.path.join(OUT, "it_shares_of_grad_groups.csv"), index=False)
ci(pd.DataFrame(occ), "estimate", "se").round(4).to_csv(os.path.join(OUT, "it_occupations.csv"), index=False)
pd.DataFrame(earn).round(1).to_csv(os.path.join(OUT, "it_earnings_real.csv"), index=False)
ci(pd.DataFrame(ur), "ur", "se").round(5).to_csv(os.path.join(OUT, "grad_unemployment_variants.csv"), index=False)
pd.DataFrame(sens).round(4).to_csv(os.path.join(OUT, "sensitivity_and_counts.csv"), index=False)
