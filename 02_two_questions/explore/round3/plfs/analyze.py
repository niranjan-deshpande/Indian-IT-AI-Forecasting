"""PLFS IT/ITeS employment series. Reads standardised unit-level parquet files (kept inside
data/sources/plfs/work) and writes AGGREGATE tables only.

Usage: python3 -I analyze.py WORK_DIR OUT_DIR

Definitions (see FINDINGS text):
- Employment = usual principal status (PS) worker, status 11-51. Industry = PS NIC-2008 code.
- Validation uses usual status (ps+ss), age 15+, as in the published reports.
- Weights: July-June rounds and CY2024: MULT/(100 if NSS==NSC else 200)/NO_QTR; CY2025: MULT/100.
- Standard errors: Taylor linearisation, ultimate-cluster (with-replacement) variance with
  PSU = first-stage unit (FSU x quarter, or FSU x month in CY2025) within strata
  (state x sector x stratum x sub-stratum [x group in CY2025]). Singleton strata contribute 0.
"""
import sys, os, glob
import numpy as np
import pandas as pd

WORK, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
ROUNDS = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "cy2024", "cy2025"]
Z90 = 1.645

# Published headline figures: usual status (ps+ss), age 15+, all-India, rural+urban, persons (%).
PUBLISHED = {
    "2017-18": (49.8, 46.8, 6.1), "2018-19": (50.2, 47.3, 5.8), "2019-20": (53.5, 50.9, 4.8),
    "2020-21": (54.9, 52.6, 4.2), "2021-22": (55.2, 52.9, 4.1), "2022-23": (57.9, 56.0, 3.2),
    "2023-24": (60.1, 58.2, 3.2), "cy2024": (59.6, 57.7, 3.2), "cy2025": (59.3, 57.4, 3.1),
}
WORKER = [11, 12, 21, 31, 41, 51]
AGEBANDS = [(15, 20), (21, 25), (26, 30), (31, 40), (41, 60)]


class Design:
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
        """y: per-person contribution already multiplied by weight."""
        t = np.bincount(self.psu, weights=y, minlength=self.npsu)
        sh = np.bincount(self.s, weights=t)
        mean_h = sh / self.n_h
        dev2 = np.bincount(self.s, weights=(t - mean_h[self.s]) ** 2)
        f = np.where(self.n_h > 1, self.n_h / np.maximum(self.n_h - 1, 1), 0.0)
        return float((f * dev2).sum())

    def total(self, ind):
        ind = ind.astype(float)
        y = self.w * ind
        return y.sum(), np.sqrt(self.var_total(y)), int((ind > 0).sum())

    def ratio(self, num, den):
        num = num.astype(float); den = den.astype(float)
        Y, X = (self.w * num).sum(), (self.w * den).sum()
        R = Y / X if X > 0 else np.nan
        z = self.w * (num - R * den) / X
        return R, np.sqrt(self.var_total(z)), int((num > 0).sum()), int((den > 0).sum())


def wquantile(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(c, q)])


def prep(d, rnd):
    age = d["age"].to_numpy()
    nic = d["ps_nic"].str.zfill(5)
    nco = d["ps_nco"].str.zfill(3)
    v = {}
    v["age"] = age
    v["ps_worker"] = d["ps_status"].isin(WORKER).to_numpy()
    v["ss_worker"] = d["ss_status"].isin(WORKER).to_numpy()
    v["upss_worker"] = v["ps_worker"] | v["ss_worker"]
    v["ps_unemp"] = (d["ps_status"] == 81).to_numpy()
    v["upss_unemp"] = v["ps_unemp"] & ~v["ss_worker"]
    v["grad"] = d["gedu"].isin([12, 13]).to_numpy()
    v["engdeg"] = (d["tedu"] == 3).to_numpy()                 # technical degree: engineering/technology
    v["eng_deg_or_gdip"] = d["tedu"].isin([3, 13]).to_numpy()  # + diploma/certificate (graduate level) in eng/tech
    v["urban"] = (d["sector"] == 2).to_numpy()
    v["regular"] = (d["ps_status"] == 31).to_numpy()
    n2, n3 = nic.str[:2], nic.str[:3]
    pw = v["ps_worker"]
    ind = {
        "nic62": (n2 == "62").to_numpy() & pw,
        "nic63": (n2 == "63").to_numpy() & pw,
        "nic62_63": n2.isin(["62", "63"]).to_numpy() & pw,
        "nic822": (n3 == "822").to_numpy() & pw,
        "nic82": (n2 == "82").to_numpy() & pw,
        "it_ites": (n2.isin(["62", "63"]) | (n3 == "822")).to_numpy() & pw,
    }
    if rnd in ["2017-18", "2018-19", "2019-20", "2020-21"]:  # NCO-2004 in these rounds
        ict = nco.isin(["213", "312"]).to_numpy()
    else:                                                     # NCO-2015
        ict = nco.isin(["251", "252", "351"]).to_numpy()
    in_it = n2.isin(["62", "63"]).to_numpy()
    ind["ictocc_all"] = ict & pw
    ind["ictocc_in_it62_63"] = ict & pw & in_it
    ind["ictocc_outside_it"] = ict & pw & ~in_it
    v["ind"] = ind
    # CWS regular wage earnings
    v["cws_regular"] = d["cws_status"].isin([31, 71, 72]).to_numpy()
    cn2 = d["cws_nic"].str.zfill(2).str[:2]  # CWS industry is recorded at NIC 2-digit only
    v["cws_it"] = cn2.isin(["62", "63"]).to_numpy()
    v["earn"] = d["earn_regular"].to_numpy(float)
    return v


def main():
    levels, keyrows, valrows, earnrows, urrows, occrows, hostrows = [], [], [], [], [], [], []
    for rnd in ROUNDS:
        d = pd.read_parquet(os.path.join(WORK, f"{rnd}.parquet"))
        D = Design(d)
        v = prep(d, rnd)
        age = v["age"]
        a15 = age >= 15

        # ---------- validation ----------
        lf = v["upss_worker"] | v["upss_unemp"]
        lfpr = D.ratio(lf & a15, a15)[0] * 100
        wpr = D.ratio(v["upss_worker"] & a15, a15)[0] * 100
        ur = D.ratio(v["upss_unemp"] & a15, lf & a15)[0] * 100
        ps_lf = v["ps_worker"] | v["ps_unemp"]
        pub = PUBLISHED[rnd]
        valrows.append(dict(round=rnd, lfpr_upss=round(lfpr, 1), wpr_upss=round(wpr, 1), ur_upss=round(ur, 1),
                            pub_lfpr=pub[0], pub_wpr=pub[1], pub_ur=pub[2],
                            wpr_ps=round(D.ratio(v["ps_worker"] & a15, a15)[0] * 100, 1),
                            ur_ps=round(D.ratio(v["ps_unemp"] & a15, ps_lf & a15)[0] * 100, 1),
                            est_population_m=round(D.w.sum() / 1e6, 1), n_persons=len(d), n_psu=D.npsu,
                            n_strata=len(D.n_h), singleton_strata=int((D.n_h == 1).sum())))
        print(valrows[-1], flush=True)

        # ---------- (a) levels by group ----------
        cuts = {"all": np.ones(len(d), bool)}
        for lo, hi in AGEBANDS:
            cuts[f"age_{lo}_{hi}"] = (age >= lo) & (age <= hi)
        cuts["grad_plus"] = v["grad"]; cuts["non_grad"] = ~v["grad"]
        cuts["eng_tech_degree"] = v["engdeg"]
        cuts["eng_tech_degree_or_grad_diploma"] = v["eng_deg_or_gdip"]
        cuts["urban"] = v["urban"]; cuts["rural"] = ~v["urban"]
        cuts["regular_salaried"] = v["regular"]; cuts["other_status"] = ~v["regular"]
        cuts["grad_21_30"] = v["grad"] & (age >= 21) & (age <= 30)
        cuts["engdeg_21_30"] = v["engdeg"] & (age >= 21) & (age <= 30)
        for g, gi in v["ind"].items():
            for c, ci in cuts.items():
                T, se, n = D.total(gi & ci)
                levels.append(dict(round=rnd, group=g, cut=c, estimate=T, se=se, n_unweighted=n))

        # ---------- (b),(c) key series ----------
        g2130 = v["grad"] & (age >= 21) & (age <= 30)
        allg = v["ps_worker"] & g2130
        T_all, se_all, n_all = D.total(allg)
        keyrows.append(dict(round=rnd, series="all_employed_grads_21_30", estimate=T_all, se=se_all,
                            n_unweighted=n_all, share=np.nan, share_se=np.nan))
        for g in ["nic62_63", "it_ites", "ictocc_all", "ictocc_in_it62_63", "ictocc_outside_it"]:
            num = v["ind"][g] & g2130
            T, se, n = D.total(num)
            R, rse, _, _ = D.ratio(num, allg)
            keyrows.append(dict(round=rnd, series=g, estimate=T, se=se, n_unweighted=n, share=R, share_se=rse))
        # tech-degree variant
        e2130 = v["engdeg"] & (age >= 21) & (age <= 30)
        for g in ["nic62_63", "it_ites"]:
            T, se, n = D.total(v["ind"][g] & e2130)
            R, rse, _, _ = D.ratio(v["ind"][g] & e2130, v["ps_worker"] & e2130)
            keyrows.append(dict(round=rnd, series=g + "__engdeg_21_30", estimate=T, se=se, n_unweighted=n,
                                share=R, share_se=rse))

        # ---------- occupation split: share of ICT-occupation workers outside NIC 62-63 ----------
        ict, out_it = v["ind"]["ictocc_all"], v["ind"]["ictocc_outside_it"]
        for lab, pop in [("all_ages", np.ones(len(d), bool)), ("grads_21_30", g2130),
                         ("age_21_30", (age >= 21) & (age <= 30))]:
            R, se, nn, nd = D.ratio(out_it & pop, ict & pop)
            occrows.append(dict(round=rnd, population=lab, ict_occ_total=D.total(ict & pop)[0],
                                ict_occ_outside_it=D.total(out_it & pop)[0], share_outside=R, share_outside_se=se,
                                n_outside=nn, n_ict_total=nd,
                                nco_version="NCO-2004 (213+312)" if rnd in ROUNDS[:4] else "NCO-2015 (251+252+351)"))
        # host industries (NIC 2-digit) of ICT-occupation workers outside 62-63, all ages
        n2 = d["ps_nic"].str.zfill(5).str[:2].to_numpy()
        for code in np.unique(n2[out_it]):
            T, se, n = D.total(out_it & (n2 == code))
            hostrows.append(dict(round=rnd, nic2=code, estimate=T, se=se, n_unweighted=n))

        # ---------- (d) earnings ----------
        base_e = v["cws_regular"] & (v["earn"] > 0)
        for sample, sel in [("cws_regular_nic62_63", base_e & v["cws_it"]),
                            ("cws_regular_nic62_63_grads", base_e & v["cws_it"] & v["grad"]),
                            ("cws_regular_all_grads", base_e & v["grad"])]:
            for lo, hi in [(21, 25), (26, 30), (31, 40)]:
                s = sel & (age >= lo) & (age <= hi)
                n = int(s.sum())
                if n == 0:
                    continue
                x, w = v["earn"][s], D.w[s]
                mean, mse, _, _ = D.ratio(np.where(s, v["earn"], 0.0), s)
                earnrows.append(dict(round=rnd, sample=sample, age_band=f"{lo}-{hi}", n_unweighted=n,
                                     mean_inr=mean, mean_se=mse, median_inr=wquantile(x, w, 0.5),
                                     p25_inr=wquantile(x, w, 0.25), p75_inr=wquantile(x, w, 0.75)))

        # ---------- (e) unemployment ----------
        for lab, pop in [("grads_21_30", g2130), ("engdeg_21_30", e2130),
                         ("grads_21_25", v["grad"] & (age >= 21) & (age <= 25))]:
            lfx = (v["upss_worker"] | v["upss_unemp"]) & pop
            R, se, nn, nd = D.ratio(v["upss_unemp"] & pop, lfx)
            R2, se2, nn2, nd2 = D.ratio(v["ps_unemp"] & pop, (v["ps_worker"] | v["ps_unemp"]) & pop)
            urrows.append(dict(round=rnd, population=lab, ur_upss=R, ur_upss_se=se, n_unemp=nn, n_lf=nd,
                               ur_ps=R2, ur_ps_se=se2))

    def finish(df, est="estimate", se="se"):
        df["ci90_lo"] = df[est] - Z90 * df[se]
        df["ci90_hi"] = df[est] + Z90 * df[se]
        df["flag_n_lt_100"] = df["n_unweighted"] < 100
        return df

    pd.DataFrame(valrows).to_csv(os.path.join(OUT, "validation.csv"), index=False)
    lv = finish(pd.DataFrame(levels))
    lv["rse_pct"] = 100 * lv["se"] / lv["estimate"].replace(0, np.nan)
    lv.round(4).to_csv(os.path.join(OUT, "employment_levels_long.csv"), index=False)
    kr = finish(pd.DataFrame(keyrows))
    kr["share_ci90_lo"] = kr["share"] - Z90 * kr["share_se"]
    kr["share_ci90_hi"] = kr["share"] + Z90 * kr["share_se"]
    kr.to_csv(os.path.join(OUT, "key_series_grads_21_30.csv"), index=False)
    er = pd.DataFrame(earnrows)
    er["flag_n_lt_100"] = er["n_unweighted"] < 100
    er.round(1).to_csv(os.path.join(OUT, "earnings_regular_salaried.csv"), index=False)
    ur = pd.DataFrame(urrows)
    ur["flag_n_lf_lt_100"] = ur["n_lf"] < 100
    ur.to_csv(os.path.join(OUT, "unemployment_grads.csv"), index=False)
    oc = pd.DataFrame(occrows)
    oc["share_ci90_lo"] = oc["share_outside"] - Z90 * oc["share_outside_se"]
    oc["share_ci90_hi"] = oc["share_outside"] + Z90 * oc["share_outside_se"]
    oc["flag_n_outside_lt_100"] = oc["n_outside"] < 100
    oc.to_csv(os.path.join(OUT, "occupation_split.csv"), index=False)
    hr = pd.DataFrame(hostrows)
    hr["share_of_outside"] = hr["estimate"] / hr.groupby("round")["estimate"].transform("sum")
    hr["flag_n_lt_100"] = hr["n_unweighted"] < 100
    small = hr["n_unweighted"] < 3  # suppress cells built from fewer than 3 respondents
    hr.loc[small, ["estimate", "se", "share_of_outside"]] = np.nan
    hr.sort_values(["round", "estimate"], ascending=[True, False]).round(4).to_csv(
        os.path.join(OUT, "ict_occ_outside_it_host_industries.csv"), index=False)


if __name__ == "__main__":
    main()
