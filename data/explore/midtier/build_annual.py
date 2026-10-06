"""Build midtier_annual.csv and midtier_vs_top6.csv from midtier_raw.csv + project top-six data.
Growth = 100*ln(x_t/x_{t-1}); computed only when a prior-year value on the SAME basis label exists
(restated comparators from the current-year document are used where the firm restated).
Hexaware reports calendar years: CY(t) is aligned to Indian FY(t+1) (9 of 12 months overlap)."""
import os, math
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
raw = pd.read_csv(os.path.join(HERE, 'midtier_raw.csv'))

def fynum(fy):  # 'FY24' -> 2024 ; 'CY2023' -> 2024 (aligned)
    return 2000 + int(fy[2:]) if fy.startswith('FY') else int(fy[2:]) + 1

raw['afy'] = raw.fiscal_year.map(fynum)
FIRMS = ['persistent', 'coforge', 'mphasis', 'hexaware']
YEARS = range(2020, 2027)

def lv(firm, afy, metric, basis=None, primary_only=True):
    d = raw[(raw.firm == firm) & (raw.afy == afy) & (raw.metric == metric)]
    if basis is not None:
        d = d[d.basis == basis]
    elif primary_only:
        d = d[d.primary == 1]
    return None if d.empty else d.iloc[0]

def growth(firm, afy, metric):
    cur = lv(firm, afy, metric)
    if cur is None:
        return None, None, None
    prv = lv(firm, afy - 1, metric, basis=cur.basis)
    if prv is None:
        return None, None, cur.basis
    return 100 * math.log(cur.value / prv.value), prv.value, cur.basis

rows = []
for f in FIRMS:
    for y in YEARS:
        r = lv(f, y, 'revenue_usd_mn'); h = lv(f, y, 'headcount'); c = lv(f, y, 'cc_growth_pct')
        inr = lv(f, y, 'revenue_inr_mn')
        gr, rprev, rb = growth(f, y, 'revenue_usd_mn'); gh, hprev, hb = growth(f, y, 'headcount')
        fy_label = (f'CY{y-1}' if f == 'hexaware' else f'FY{str(y)[2:]}')
        rows.append(dict(firm=f, fiscal_year=fy_label, aligned_fy=f'FY{str(y)[2:]}',
            period_end=(r.period_end if r is not None else (h.period_end if h is not None else '')),
            revenue_usd_mn=None if r is None else r.value, revenue_basis=rb,
            revenue_inr_mn=None if inr is None else inr.value,
            rev_prior_same_basis=rprev, rev_growth_logx100=None if gr is None else round(gr, 3),
            cc_growth_reported_pct=None if c is None else c.value,
            headcount=None if h is None else int(h.value), headcount_basis=hb,
            hc_prior_same_basis=None if hprev is None else int(hprev),
            hc_growth_logx100=None if gh is None else round(gh, 3)))
ann = pd.DataFrame(rows)

def combined(df, firms, label):
    out = []
    for y in YEARS:
        d = df[(df.aligned_fy == f'FY{str(y)[2:]}') & df.firm.isin(firms)]
        rec = dict(firm=label, fiscal_year=f'FY{str(y)[2:]}', aligned_fy=f'FY{str(y)[2:]}')
        for m, prev, g in [('revenue_usd_mn', 'rev_prior_same_basis', 'rev_growth_logx100'),
                           ('headcount', 'hc_prior_same_basis', 'hc_growth_logx100')]:
            have = d[d[m].notna()]
            rec[m] = have[m].sum() if len(have) else None
            rec[m + '_firms'] = '+'.join(have.firm)
            both = d[d[g].notna()]
            if len(both):
                rec[g] = round(100 * math.log(both[m].sum() / both[prev].sum()), 3)
                rec[g.replace('logx100', 'firms')] = '+'.join(both.firm)
        out.append(rec)
    return pd.DataFrame(out)

comb4 = combined(ann, FIRMS, 'combined_4 (Hexaware CY(t-1) as FY t)')
comb3 = combined(ann, ['persistent', 'coforge', 'mphasis'], 'combined_3_indianFY (ex-Hexaware)')
annual = pd.concat([ann, comb4, comb3], ignore_index=True)
annual.to_csv(os.path.join(HERE, 'midtier_annual.csv'), index=False)

# ---------------- top six ----------------
TOP6 = ['tcs', 'infosys', 'hcltech', 'wipro', 'techm', 'lti_group']
ta = pd.read_csv(os.path.join(ROOT, 'output', 'final', 'table_A_firms.csv'))
ta = ta[ta.firm.isin(TOP6)]
q = pd.read_csv(os.path.join(ROOT, 'data', 'corrected', 'core_quarterly_final.csv'))
def top6_hc(y):
    cq = f'{y}Q1'; d = q[q.cal_q == cq].set_index('firm').headcount
    lti = (d.get('lti', float('nan')) + d.get('mindtree', float('nan'))) if y <= 2022 else d.get('ltim', float('nan'))
    vals = [d.get(f, float('nan')) for f in ['tcs', 'infosys', 'hcltech', 'wipro', 'techm']] + [lti]
    return sum(vals), all(pd.notna(v) for v in vals)
cmp_rows = []
for y in YEARS:
    fy = f'FY{str(y)[2:]}'; pfy = f'FY{str(y-1)[2:]}'
    t = ta[ta.period == fy]; tp = ta[ta.period == pfy]
    t6r = t.weight_rev_usd.sum() if len(t) == 6 and t.weight_rev_usd.notna().all() else None
    t6rp = tp.weight_rev_usd.sum() if len(tp) == 6 and tp.weight_rev_usd.notna().all() else None
    h, okh = top6_hc(y); hp, okhp = top6_hc(y - 1)
    c4 = comb4[comb4.fiscal_year == fy].iloc[0]; c3 = comb3[comb3.fiscal_year == fy].iloc[0]
    rec = dict(fiscal_year=fy,
        top6_rev_usd_mn=t6r, top6_rev_growth_logx100=round(100 * math.log(t6r / t6rp), 3) if t6r and t6rp else None,
        top6_headcount=int(h) if okh else None,
        top6_hc_growth_logx100=round(100 * math.log(h / hp), 3) if okh and okhp else None,
        mid4_rev_usd_mn=c4.revenue_usd_mn, mid4_rev_firms=c4.revenue_usd_mn_firms,
        mid4_rev_growth_logx100=c4.get('rev_growth_logx100'), mid4_rev_growth_firms=c4.get('rev_growth_firms'),
        mid3_rev_growth_logx100=c3.get('rev_growth_logx100'), mid3_rev_growth_firms=c3.get('rev_growth_firms'),
        mid4_headcount=c4.headcount, mid4_hc_firms=c4.headcount_firms,
        mid4_hc_growth_logx100=c4.get('hc_growth_logx100'), mid4_hc_growth_firms=c4.get('hc_growth_firms'),
        mid3_hc_growth_logx100=c3.get('hc_growth_logx100'),
    )
    rec['mid4_rev_share_pct'] = round(100 * c4.revenue_usd_mn / (c4.revenue_usd_mn + t6r), 3) if t6r else None
    rec['mid4_hc_share_pct'] = round(100 * c4.headcount / (c4.headcount + h), 3) if okh else None
    for a, b in [('rev', 'rev'), ('hc', 'hc')]:
        m, tt = rec[f'mid4_{a}_growth_logx100'], rec[f'top6_{b}_growth_logx100']
        rec[f'{a}_growth_gap_mid4_minus_top6'] = round(m - tt, 3) if pd.notna(m) and pd.notna(tt) else None
    cmp_rows.append(rec)
cmp = pd.DataFrame(cmp_rows)
cmp['note'] = ('top6 rev = sum weight_rev_usd (table_A_firms.csv); top6 hc = FY-end (calendar Q1) levels from '
               'core_quarterly_final.csv, LTI=lti+mindtree to FY22, ltim from FY23; HCLTech FY25 includes 7,398-person divestiture. '
               'mid4 = Persistent+Coforge+Mphasis (Indian FY) + Hexaware CY(t-1); Coforge FY20 USD missing so FY20 mid4 revenue excludes Coforge '
               'and FY21 mid revenue growth excludes Coforge. Shares use levels (acquisition level breaks included).')
cmp.to_csv(os.path.join(HERE, 'midtier_vs_top6.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(ann[['firm', 'fiscal_year', 'revenue_usd_mn', 'rev_growth_logx100', 'cc_growth_reported_pct', 'headcount', 'hc_growth_logx100']])
print(pd.concat([comb4, comb3])[['firm', 'fiscal_year', 'revenue_usd_mn', 'revenue_usd_mn_firms', 'rev_growth_logx100', 'rev_growth_firms', 'headcount', 'hc_growth_logx100', 'hc_growth_firms']])
print(cmp.drop(columns='note').T)
