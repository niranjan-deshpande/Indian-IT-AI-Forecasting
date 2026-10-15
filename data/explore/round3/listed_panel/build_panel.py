"""Build the FY23-FY26 panel of listed Indian IT-services / ER&D / ITeS firms beyond the top six.

Inputs
  parts/*.csv                         firm x year x metric rows collected from company documents
  ../../midtier/midtier_raw.csv       headcount + USD revenue for the four mid-tier firms (repo, unchanged)
  ../gcc/top6_headcount_fy.csv        top-six year-end headcount (repo)
  ../../../corrected/core_quarterly_final.csv  top-six quarterly revenue (repo), summed to Indian FY

Outputs
  listed_panel_long.csv      one row per firm x year x metric (with source URL + page)
  listed_panel_firms.csv     one row per firm: levels FY23..FY26 and FY23->FY26 changes
  listed_panel_summary.csv   aggregates (broader set with/without the mid-tier four, vs top six)

Conventions
  * Calendar-year reporters: CY(t) is aligned to Indian FY(t+1) (as the repo does for Hexaware).
  * Aggregates use a balanced panel: a firm enters an aggregate only if it has the metric in both
    FY23 and FY26 (primary rows). Firms left out are listed in the summary.
  * Growth figures are simple % changes (cum) and CAGR over 3 years.
Run: python3 -I build_panel.py   (from any directory)
"""
import glob
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
MID4 = ['persistent', 'coforge', 'mphasis', 'hexaware']
YEARS = ['FY23', 'FY24', 'FY25', 'FY26']

# universe: firm -> (display name, group)
UNIVERSE = {
    'persistent': ('Persistent Systems', 'IT services (mid-4)'),
    'coforge': ('Coforge', 'IT services (mid-4)'),
    'mphasis': ('Mphasis', 'IT services (mid-4)'),
    'hexaware': ('Hexaware Technologies (CY)', 'IT services (mid-4)'),
    'ltts': ('L&T Technology Services', 'ER&D'),
    'tata_elxsi': ('Tata Elxsi', 'ER&D'),
    'kpit': ('KPIT Technologies', 'ER&D'),
    'cyient': ('Cyient (group, incl. DLM)', 'ER&D'),
    'tata_technologies': ('Tata Technologies', 'ER&D'),
    'birlasoft': ('Birlasoft', 'IT services'),
    'zensar': ('Zensar Technologies', 'IT services'),
    'sonata': ('Sonata Software (intl IT services rev)', 'IT services'),
    'mastek': ('Mastek', 'IT services'),
    'happiest_minds': ('Happiest Minds', 'IT services'),
    'datamatics': ('Datamatics Global Services', 'IT services / ITeS'),
    'r_systems': ('R Systems International (CY)', 'IT services'),
    'firstsource': ('Firstsource Solutions', 'ITeS / BPM'),
    'eclerx': ('eClerx Services', 'ITeS / KPO'),
    'hgs': ('Hinduja Global Solutions', 'ITeS / BPM'),
    'sagility': ('Sagility India', 'ITeS / BPM'),
    'inventurus': ('Inventurus Knowledge Solutions', 'ITeS / BPM'),
}

# Basis overrides: (firm, aligned_fy, metric) -> basis to use as primary, so each firm's FY23 and FY26
# endpoints are on a like-for-like footprint. Documented in listed_panel_long.csv via the primary flag.
#  * Cyient: headcount is only disclosed for DET (services, ex-DLM electronics manufacturing), so revenue
#    is switched to the DET segment too (group revenue kept as primary=0).
#  * LTTS: SWC (bought from parent L&T in FY24, restated into FY23; reclassified as discontinued in Q4FY26).
#    FY23 = as originally reported (ex-SWC), FY25/FY26 = continuing ops ex-SWC, FY24 = incl. SWC (no ex-SWC
#    figure published), so FY24 is not comparable.
OVERRIDE = {}
for y, b in [('FY23', 'segment_DET'), ('FY24', 'segment_DET'), ('FY25', 'segment_DET_incl_semis'),
             ('FY26', 'segment_DET_excl_semis')]:
    OVERRIDE[('cyient', y, 'revenue_inr_cr')] = b
    OVERRIDE[('cyient', y, 'revenue_usd_mn')] = b
OVERRIDE.update({
    ('ltts', 'FY23', 'headcount'): 'total_headcount_as_originally_reported_excl_SWC',
    ('ltts', 'FY23', 'revenue_inr_cr'): 'consolidated_as_originally_reported',
    ('ltts', 'FY23', 'revenue_usd_mn'): 'as_originally_reported',
    ('ltts', 'FY25', 'headcount'): 'total_headcount_continuing_ops_excl_SWC',
    ('ltts', 'FY25', 'revenue_inr_cr'): 'consolidated_continuing_ops_excl_SWC',
    ('ltts', 'FY25', 'revenue_usd_mn'): 'continuing_ops_excl_SWC',
    ('ltts', 'FY26', 'revenue_usd_mn'): 'continuing_ops_excl_SWC',
})

# Known acquired headcount added inside FY23->FY26 (acquisitions closed after the FY23 year-end).
# Lower bound: only deals whose headcount a document states. (persons, source, primary/secondary)
ACQ_HC = {
    'inventurus': (6349, 'AQuity (Oct-2023): 6,349 employees in Mar-2024 headcount; IKS RHP (SEBI) PDF p253', 'primary'),
    'happiest_minds': (1350, 'PureSoftware ~1,200 (IP Q4FY24 p6) + Aureus ~150 (IAR 2024-25 M&A page)', 'primary'),
    'sagility': (1083, 'BroadPath (Jan-2025): 1,083 staff in Mar-2025 headcount; Q4FY25 deck p9', 'primary'),
    'kpit': (900, 'Caresoft (Aug-2025): 900+ employees; BSE filing 6-May-2025 p4', 'primary'),
    'tata_technologies': (300, 'ES-Tec (Nov-2025): 300+ employees; NSE intimation 13-Sep-2025 p2', 'primary'),
    'coforge': (4200, 'Cigniti (consolidated Q2FY25): "4200+ Cignitians" at Sep-2023; Cigniti Q2FY24 investor PPT PDF p3 (BSE filing https://www.bseindia.com/xml-data/corpfiling/AttachHis/02d27acb-573a-47eb-8dbb-c90b6cda42c4.pdf)', 'primary'),
    'ltts': (1500, 'Intelliswift (Jan-2025): ~1,500 employees; secondary (HFS Research / Economic Times)', 'secondary'),
}

COLS = ['firm', 'fiscal_year', 'aligned_fy', 'period_end', 'metric', 'value', 'unit', 'basis',
        'includes_contractors', 'source_url', 'source_doc', 'source_page', 'primary', 'notes']


def load_parts():
    frames = []
    for p in sorted(glob.glob(os.path.join(HERE, 'parts', '*.csv'))):
        d = pd.read_csv(p, dtype=str)
        d['part_file'] = os.path.basename(p)
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d.columns = [c.strip() for c in d.columns]
    return d


def mid4_from_repo():
    raw = pd.read_csv(os.path.join(REPO, 'data', 'explore', 'midtier', 'midtier_raw.csv'), dtype=str)
    raw = raw[raw.metric.isin(['headcount', 'revenue_usd_mn'])]

    def afy(fy):
        return 'FY%02d' % (int(fy[2:]) % 100) if fy.startswith('FY') else 'FY%02d' % ((int(fy[2:]) + 1) % 100)
    raw['aligned_fy'] = raw.fiscal_year.map(afy)
    raw = raw[raw.aligned_fy.isin(YEARS)]
    contr = {'mphasis': 'yes (billable contractors; excl. interns)', 'hexaware': 'yes (FTE + contractors)',
             'persistent': 'not_stated', 'coforge': 'not_stated'}
    out = pd.DataFrame({
        'firm': raw.firm, 'fiscal_year': raw.fiscal_year, 'aligned_fy': raw.aligned_fy,
        'period_end': raw.period_end, 'metric': raw.metric, 'value': raw.value, 'unit': raw.unit,
        'basis': raw.basis,
        'includes_contractors': [contr[f] if m == 'headcount' else '' for f, m in zip(raw.firm, raw.metric)],
        'source_url': raw.source_url, 'source_doc': raw.source_doc, 'source_page': raw.source_loc,
        'primary': raw.primary, 'notes': raw.notes.fillna('') + ' [from repo midtier_raw.csv]'})
    out['part_file'] = 'repo:midtier_raw.csv'
    return out


def main():
    parts = load_parts()
    # parts may contain mid-4 rows only for INR revenue (and acquisitions); headcount/USD come from repo
    keep = ~(parts.firm.isin(MID4) & parts.metric.isin(['headcount', 'revenue_usd_mn']))
    long = pd.concat([parts[keep], mid4_from_repo()], ignore_index=True)
    long['value_num'] = pd.to_numeric(long.value.astype(str).str.replace(',', ''), errors='coerce')
    long['primary'] = pd.to_numeric(long.primary, errors='coerce').fillna(0).astype(int)
    for (f, y, m), b in OVERRIDE.items():
        sel = (long.firm == f) & (long.aligned_fy == y) & (long.metric == m)
        assert (sel & (long.basis == b)).sum() == 1, (f, y, m, b)
        long.loc[sel, 'primary'] = (long.loc[sel, 'basis'] == b).astype(int)
        long.loc[sel & (long.basis == b), 'notes'] = long.loc[sel & (long.basis == b), 'notes'].fillna('') + \
            ' [primary set by build_panel.py OVERRIDE for like-for-like endpoints]'
    long = long.sort_values(['firm', 'metric', 'aligned_fy', 'primary'], ascending=[True, True, True, False])
    long[COLS + ['part_file']].to_csv(os.path.join(HERE, 'listed_panel_long.csv'), index=False)

    core = long[(long.primary == 1) & long.metric.isin(['headcount', 'revenue_inr_cr', 'revenue_usd_mn'])
                & long.aligned_fy.isin(YEARS) & long.value_num.notna()]
    dup = core.groupby(['firm', 'aligned_fy', 'metric']).size()
    if (dup > 1).any():
        print('WARNING duplicate primary rows:\n', dup[dup > 1])
    core = core.drop_duplicates(['firm', 'aligned_fy', 'metric'])
    wide = core.pivot_table(index='firm', columns=['metric', 'aligned_fy'], values='value_num', aggfunc='first')

    def g(firm, metric, fy):
        try:
            v = wide.loc[firm, (metric, fy)]
            return None if pd.isna(v) else float(v)
        except KeyError:
            return None

    acq = long[long.metric == 'acquisition'].groupby('firm').apply(
        lambda x: ' | '.join((x.notes.fillna('') if x.notes.notna().any() else x.value.fillna('')).astype(str).str[:160]),
        include_groups=False)

    firms = []
    for f, (name, grp) in UNIVERSE.items():
        r = {'firm': f, 'name': name, 'group': grp, 'mid4': int(f in MID4)}
        for m, short in [('headcount', 'hc'), ('revenue_inr_cr', 'rev_inr_cr'), ('revenue_usd_mn', 'rev_usd_mn')]:
            for y in YEARS:
                r[f'{short}_{y}'] = g(f, m, y)
            a, b = r[f'{short}_FY23'], r[f'{short}_FY26']
            r[f'{short}_chg_pct_FY23_26'] = round(100 * (b / a - 1), 2) if a and b else None
            r[f'{short}_cagr_FY23_26'] = round(100 * ((b / a) ** (1 / 3) - 1), 2) if a and b else None
        r['hc_fell_FY23_26'] = (None if r['hc_chg_pct_FY23_26'] is None else int(r['hc_chg_pct_FY23_26'] < 0))
        hcs = [r[f'hc_{y}'] for y in YEARS]
        r['hc_fell_any_year'] = (None if None in hcs else int(any(hcs[i + 1] < hcs[i] for i in range(3))))
        bc = long[(long.firm == f) & (long.metric == 'headcount') & (long.primary == 1)]
        r['hc_basis'] = '; '.join(sorted(set(bc.basis.dropna().astype(str))))
        r['hc_includes_contractors'] = '; '.join(sorted(set(bc.includes_contractors.dropna().astype(str))))
        ah = ACQ_HC.get(f)
        r['acquired_hc_known'] = ah[0] if ah else None
        r['acquired_hc_source'] = ah[1] if ah else ''
        if ah and r['hc_FY23'] and r['hc_FY26']:
            r['hc_chg_pct_ex_known_acq'] = round(100 * ((r['hc_FY26'] - ah[0]) / r['hc_FY23'] - 1), 2)
        else:
            r['hc_chg_pct_ex_known_acq'] = r['hc_chg_pct_FY23_26']
        r['acquisitions'] = acq.get(f, '')
        firms.append(r)
    firms = pd.DataFrame(firms)
    firms.to_csv(os.path.join(HERE, 'listed_panel_firms.csv'), index=False)

    # ---- top six (repo) ----
    t6 = pd.read_csv(os.path.join(REPO, 'data', 'explore', 'round3', 'gcc', 'top6_headcount_fy.csv'))
    t6hc = dict(zip(t6.fy, t6.top6))
    q = pd.read_csv(os.path.join(REPO, 'data', 'corrected', 'core_quarterly_final.csv'))
    q = q[q.firm.isin(['tcs', 'infosys', 'hcltech', 'wipro', 'techm', 'ltim'])].copy()
    yy = q.cal_q.str[:4].astype(int)
    qq = q.cal_q.str[-1].astype(int)
    q['fy'] = ['FY%02d' % ((y + (1 if k >= 2 else 0)) % 100) for y, k in zip(yy, qq)]
    q = q[q.fy.isin(YEARS)]
    t6inr = (q.groupby('fy').rev_inr.sum() / 10).to_dict()  # INR mn -> crore
    t6usd = q.groupby('fy').rev_usd.sum().to_dict()

    rows = []

    def agg(label, sub, short, unit):
        bal = sub[sub[f'{short}_FY23'].notna() & sub[f'{short}_FY26'].notna()]
        miss = sorted(set(sub.firm) - set(bal.firm))
        lv = {y: bal[f'{short}_{y}'].sum() for y in YEARS}
        allyrs = bal[[f'{short}_{y}' for y in YEARS]].notna().all(axis=1)
        a, b = lv['FY23'], lv['FY26']
        chg = bal[f'{short}_chg_pct_FY23_26']
        w = bal['rev_inr_cr_FY23']
        wmask = w.notna() & chg.notna()
        extra = ''
        if short == 'hc':
            acqhc = bal.acquired_hc_known.fillna(0).sum()
            extra = 'known acquired heads %d; agg change ex known acquired heads %.2f%%' % (
                acqhc, 100 * ((b - acqhc) / a - 1))
        rows.append({
            'set': label, 'metric': short, 'unit': unit, 'n_firms': len(bal),
            'FY23': round(a, 1), 'FY24_partial': round(bal.loc[allyrs, f'{short}_FY24'].sum(), 1),
            'FY25_partial': round(bal.loc[allyrs, f'{short}_FY25'].sum(), 1), 'FY26': round(b, 1),
            'abs_change_FY23_26': round(b - a, 1), 'agg_pct_change_FY23_26': round(100 * (b / a - 1), 2),
            'agg_cagr_FY23_26': round(100 * ((b / a) ** (1 / 3) - 1), 2),
            'median_firm_pct_change': round(chg.median(), 2),
            'rev_weighted_mean_firm_pct_change': (round((chg[wmask] * w[wmask]).sum() / w[wmask].sum(), 2)
                                                  if wmask.any() else None),
            'n_firms_falling': int((chg < 0).sum()),
            'firms_missing_FY23_or_FY26': ';'.join(miss),
            'note': '; '.join(x for x in ['FY24/FY25 partial = sum over firms with all four years'
                                          if not allyrs.all() else '', extra] if x)})

    sets = [('broader_all_21', firms), ('broader_ex_mid4', firms[firms.mid4 == 0]),
            ('mid4', firms[firms.mid4 == 1]),
            ('ERD_5', firms[firms.group == 'ER&D']),
            ('ITservices_ex_mid4_7', firms[firms.group.str.startswith('IT services') & (firms.mid4 == 0)]),
            ('ITeS_BPM_5', firms[firms.group.str.startswith('ITeS')]),
            ('broader_ex_mid4_ex_ITeS_12', firms[(firms.mid4 == 0) & ~firms.group.str.startswith('ITeS')])]
    for label, sub in sets:
        agg(label, sub, 'hc', 'persons')
        agg(label, sub, 'rev_inr_cr', 'INR crore')
        agg(label, sub, 'rev_usd_mn', 'USD mn')
    for short, d, unit in [('hc', t6hc, 'persons'), ('rev_inr_cr', t6inr, 'INR crore'), ('rev_usd_mn', t6usd, 'USD mn')]:
        a, b = d['FY23'], d['FY26']
        rows.append({'set': 'top6 (repo)', 'metric': short, 'unit': unit, 'n_firms': 6,
                     'FY23': round(a, 1), 'FY24_partial': round(d['FY24'], 1), 'FY25_partial': round(d['FY25'], 1),
                     'FY26': round(b, 1), 'abs_change_FY23_26': round(b - a, 1),
                     'agg_pct_change_FY23_26': round(100 * (b / a - 1), 2),
                     'agg_cagr_FY23_26': round(100 * ((b / a) ** (1 / 3) - 1), 2),
                     'note': 'repo: gcc/top6_headcount_fy.csv; revenue = sum of quarters in corrected/core_quarterly_final.csv'})
    summ = pd.DataFrame(rows)
    summ.to_csv(os.path.join(HERE, 'listed_panel_summary.csv'), index=False)
    pd.set_option('display.width', 250)
    pd.set_option('display.max_columns', 30)
    print(summ.drop(columns=['note']).to_string())
    print(firms[['firm', 'hc_FY23', 'hc_FY24', 'hc_FY25', 'hc_FY26', 'hc_chg_pct_FY23_26', 'rev_inr_cr_FY23',
                 'rev_inr_cr_FY26', 'rev_inr_cr_chg_pct_FY23_26', 'rev_usd_mn_chg_pct_FY23_26']].to_string())


if __name__ == '__main__':
    main()
