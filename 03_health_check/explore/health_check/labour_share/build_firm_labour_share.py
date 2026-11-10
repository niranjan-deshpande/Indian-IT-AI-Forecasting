"""Build firm-level labour share of value added for Indian IT services firms, FY16-FY26.

Definitions (consolidated statements, INR crore, Indian FY Apr-Mar):
  EBITDA       = revenue from operations - operating expenses before D&A
                 (excludes other income, finance cost and exceptional items)
  value added  = employee benefit expense + EBITDA
  labour share = employee benefit expense / value added
Subcontracting / purchased services stay in intermediate input.

Inputs:
  raw_parsed_screener_tickertape.csv  (from parse_firm_financials.py; run with python3 -I)
    - Screener consolidated P&L: Sales, Operating Profit (=EBITDA, pre-exceptional), Depreciation
    - Tickertape annual income: employee cost (incEpc), FY17-FY26
  data/tidy/panel_long.csv (repo): FY16 employee cost for TCS, Wipro, Tech Mahindra
  Primary filings (values typed in below, with URLs) for FY16 Infosys, HCLTech, LTI and LTI FY17/FY22.
Run: python3 -I build_firm_labour_share.py
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

SCR_URL = {
    'tcs': 'https://www.screener.in/company/TCS/consolidated/',
    'infosys': 'https://www.screener.in/company/INFY/consolidated/',
    'hcltech': 'https://www.screener.in/company/HCLTECH/consolidated/',
    'wipro': 'https://www.screener.in/company/WIPRO/consolidated/',
    'techm': 'https://www.screener.in/company/TECHM/consolidated/',
    'ltim': 'https://www.screener.in/company/LTM/consolidated/',
    'mindtree': 'https://www.screener.in/company/MINDTREE/consolidated/',
    'persistent': 'https://www.screener.in/company/PERSISTENT/consolidated/',
    'coforge': 'https://www.screener.in/company/COFORGE/consolidated/',
    'mphasis': 'https://www.screener.in/company/MPHASIS/consolidated/',
}
TT_SID = {'tcs': 'TCS', 'infosys': 'INFY', 'hcltech': 'HCLT', 'wipro': 'WIPR', 'techm': 'TEML',
          'ltim': 'LRTI', 'mindtree': 'MINT', 'persistent': 'PERS', 'coforge': 'COFO', 'mphasis': 'MBFL'}
TOP6 = ['tcs', 'infosys', 'hcltech', 'wipro', 'techm']  # + LTI/Mindtree (to FY22) or LTIM (FY23+)
MID3 = ['persistent', 'coforge', 'mphasis']

FIRM_NOTES = {
    'wipro': 'Consolidated incl. small non-IT segments (IT Products, ISRE); Wipro Enterprises (consumer) demerged FY13.',
    'hcltech': 'Includes HCLSoftware (IP/products, high margin, ~10-11% of revenue post-FY20 IBM IP deals).',
    'techm': 'Includes BPS and non-IT subsidiaries (e.g. Comviva).',
}


def load():
    d = pd.read_csv(os.path.join(HERE, 'raw_parsed_screener_tickertape.csv'))
    d = d[d.period.str.startswith('Mar')].copy()
    d['fy'] = 'FY' + d.period.str[6:8]
    d = d[d.fy.between('FY16', 'FY26')]
    return d


def repo_fy16_emp():
    """FY16 employee cost from repo quarterly panel (INR crore)."""
    p = pd.read_csv(os.path.join(REPO, 'data', 'tidy', 'panel_long.csv'))
    p = p[(p.metric == 'employee_cost') & p.unit.str.startswith('INR')]
    p = p[p.fiscal_q.isin([f'Q{i}FY16' for i in range(1, 5)])]
    out = {}
    for firm in ['tcs', 'wipro', 'techm']:
        x = p[p.firm == firm]
        div = x.unit.map({'INR_cr': 1, 'INR_mn': 10})
        v = (x.value / div)
        nq = x.fiscal_q.nunique()
        if nq == 4:
            out[firm] = (round(v.sum(), 1), '; '.join(sorted(x.source_doc.dropna().unique())[:2]))
    return out


def main():
    d = load()
    rows = []
    rep16 = repo_fy16_emp()
    for _, r in d.iterrows():
        firm = 'lti' if r.firm == 'ltim' and r.fy <= 'FY22' else r.firm
        rec = dict(firm=firm, fy=r.fy, revenue_inr_cr=r.sales, ebitda_inr_cr=r.op,
                   depreciation_inr_cr=r.dep, employee_cost_inr_cr=r.tt_emp,
                   source='screener (revenue, EBITDA=Operating Profit, D&A) + tickertape (employee cost)',
                   source_url=f"{SCR_URL[r.firm]} ; https://api.tickertape.in/stocks/financials/income/{TT_SID[r.firm]}/annual/normal?count=10",
                   notes=FIRM_NOTES.get(r.firm, ''))
        if r.fy == 'FY16' and r.firm in rep16:
            v, doc = rep16[r.firm]
            rec['employee_cost_inr_cr'] = v
            rec['source'] = 'screener (revenue, EBITDA, D&A) + repo panel_long (employee cost, sum of 4 quarters)'
            rec['notes'] = (rec['notes'] + f' FY16 employee cost from repo quarterly ({doc}).').strip()
            if r.firm == 'wipro':
                rec['notes'] += ' Wipro FY16 employee cost is IFRS.'
        if r.fy == 'FY16' and r.firm in MID3:
            rec['employee_cost_inr_cr'] = round(r.scr_emp_pct / 100 * r.sales, 1)
            rec['source'] = 'screener (all items; employee cost = integer-rounded Employee Cost % x sales)'
            rec['notes'] = 'FY16 employee cost APPROXIMATE: Screener integer % (+/-0.5pp of revenue, ~+/-0.6pp on labour share).'
        if r.fy == 'FY16' and r.firm == 'infosys':
            # 20-F FY2017 (IFRS, USD mn): employee benefit costs 5,236 / revenue 9,501 in fiscal 2016
            ratio = 5236 / 9501
            rec['employee_cost_inr_cr'] = round(ratio * r.sales, 1)
            rec['source'] = 'screener (revenue, EBITDA, D&A) + SEC 20-F FY2017 (employee cost ratio)'
            rec['source_url'] = SCR_URL['infosys'] + ' ; https://www.sec.gov/Archives/edgar/data/1067491/000106749117000021/form20f.htm'
            rec['notes'] = ('FY16 employee cost = IFRS USD ratio (employee benefit costs 5,236 / revenue 9,501, '
                            '20-F note 2.10) x INR revenue; the same method reproduces FY17 Ind AS to 0.01pp.')
        if r.fy == 'FY16' and r.firm == 'ltim':
            # LTI Q4FY17 SEBI consolidated audited results (Ind AS), year ended Mar 31 2016, INR mn
            rec.update(revenue_inr_cr=5846.4, employee_cost_inr_cr=3526.6,
                       ebitda_inr_cr=round((58464 - 35266 - 12950) / 10, 1), depreciation_inr_cr=174.0,
                       source='annual report/SEBI results (LTI FY17 audited consolidated, FY16 Ind AS comparative)',
                       source_url='https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2017/05/CFS_outcome.pdf',
                       notes='LTI standalone group (pre-merger). EBITDA = revenue - employee - other expenses.')
        if r.fy == 'FY17' and r.firm == 'ltim':
            rec.update(employee_cost_inr_cr=3775.8,
                       source='screener (revenue, EBITDA, D&A) + SEBI results (employee cost)',
                       source_url=SCR_URL['ltim'] + ' ; https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2017/05/CFS_outcome.pdf',
                       notes='LTI pre-merger. Employee cost from original FY17 audited results (37,758 mn); '
                             'Tickertape shows 3,715.3 (likely later reclassification); Screener EBITDA 1,230 matches the filing.')
        if r.fy == 'FY22' and r.firm == 'ltim':
            # keep the restated merged LTIM FY22 as its own row (excluded from sums) ...
            rr = dict(rec)
            rr.update(firm='ltim', notes='LTIMindtree FY22 RESTATED for merger (common-control pooling: LTI+Mindtree). '
                                         'Not used in top6_sum (which uses LTI + Mindtree as originally reported).')
            rows.append(rr)
            # ... and LTI as originally reported
            rec.update(revenue_inr_cr=15668.7, employee_cost_inr_cr=9700.7,
                       ebitda_inr_cr=round((156687 - 97007 - 26565 - 2531) / 10, 1), depreciation_inr_cr=354.9,
                       source='SEBI audited consolidated results Q4FY22 (LTI, as originally reported)',
                       source_url='https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2022/04/Consolidated-financial-statements-Q4FY2022.pdf',
                       notes='LTI pre-merger, as originally reported. EBITDA = revenue - employee - operating expenses - other expenses.')
        if r.fy <= 'FY21' and r.firm == 'ltim' and r.fy not in ('FY16', 'FY17'):
            rec['notes'] = 'LTI pre-merger (Screener LTM page history = L&T Infotech). FY21 employee cost verified vs SEBI results (74,289 mn).'
        if r.firm == 'mindtree':
            rec['notes'] = 'Mindtree pre-merger (merged into LTI Nov 2022). FY22 employee cost = repo panel (6,328).'
        if r.firm == 'hcltech' and r.fy == 'FY16':
            continue  # handled below
        rows.append(rec)

    # HCLTech FY16 (Apr 2015-Mar 2016): HCL moved from a June to a March year end; FY2015-16 was a 9-month
    # transition (Jul15-Mar16). Construct 12 months = 9m Jul15-Mar16 (Indian GAAP SEBI audited results, consolidated)
    # + Apr-Jun 2015 quarter (IR release, US GAAP INR: revenue 9,777, EBITDA 2,100, D&A 124; employee cost estimated
    # at the 12m-to-Jun-2015 Indian GAAP ratio 17,726.43/36,701.22).
    nine = dict(rev=30780.80, emp=15093.18, ebitda=6212.69 + 392.95, dep=392.95)
    q = dict(rev=9777.0, ebitda=2100.0, dep=124.0)
    q['emp'] = 17726.43 / 36701.22 * q['rev']
    rows.append(dict(firm='hcltech', fy='FY16',
                     revenue_inr_cr=round(nine['rev'] + q['rev'], 1),
                     employee_cost_inr_cr=round(nine['emp'] + q['emp'], 1),
                     ebitda_inr_cr=round(nine['ebitda'] + q['ebitda'], 1),
                     depreciation_inr_cr=round(nine['dep'] + q['dep'], 1),
                     source='annual report/SEBI results (9m Jul15-Mar16) + IR release (Apr-Jun15 quarter); employee cost of Apr-Jun15 estimated',
                     source_url=('https://www.hcltech.com/sites/default/files/documents/investor-reports/full_financial_results_qtr._and_year_nine_months_ended_march_31_2016_0.pdf'
                                 ' ; repo data/sources/hcltech/hcl-q4_2015-investor_release.pdf'),
                     notes=('CONSTRUCTED 12m Apr15-Mar16: 9m transition period (Indian GAAP, consolidated) + Apr-Jun15 quarter '
                            '(US GAAP INR from IR release; employee cost = 48.3% x quarter revenue, the Jul14-Jun15 ratio). '
                            'Cross-check: IR 12m Apr15-Mar16 revenue 40,913 and EBITDA 8,795 (US GAAP). ' + FIRM_NOTES['hcltech'])))

    df = pd.DataFrame(rows)

    # LTI + Mindtree pro-forma rows (FY16-FY22) so LTIM has a continuous per-firm series
    pre = df[df.firm.isin(['lti', 'mindtree']) & (df.fy <= 'FY22')]
    g = pre.groupby('fy')[['revenue_inr_cr', 'employee_cost_inr_cr', 'ebitda_inr_cr', 'depreciation_inr_cr']].sum().reset_index()
    g['firm'] = 'ltim_proforma'
    g['source'] = 'sum of lti and mindtree rows'
    g['source_url'] = ''
    g['notes'] = 'LTI + Mindtree as separately reported (no intercompany elimination). Compare restated LTIM FY22 row.'
    df = pd.concat([df, g], ignore_index=True)

    def agg(members_by_fy, name, note):
        out = []
        for fy in sorted(df.fy.unique()):
            mem = members_by_fy(fy)
            x = df[(df.fy == fy) & df.firm.isin(mem)]
            if len(x) != len(mem) or x[['employee_cost_inr_cr', 'ebitda_inr_cr']].isna().any().any():
                continue
            s = x[['revenue_inr_cr', 'employee_cost_inr_cr', 'ebitda_inr_cr', 'depreciation_inr_cr']].sum()
            out.append(dict(firm=name, fy=fy, **s.to_dict(), source='sum of firm rows', source_url='',
                            notes=note + f" Members: {'+'.join(mem)}."))
        return out

    top6 = lambda fy: TOP6 + (['lti', 'mindtree'] if fy <= 'FY22' else ['ltim'])
    rows2 = agg(top6, 'top6_sum', 'Sum of levels; LTI+Mindtree (as reported) to FY22, LTIMindtree from FY23.')
    rows2 += agg(lambda fy: MID3, 'mid3_sum', 'Sum of levels. FY16 employee cost approximate (Screener integer %).')
    df = pd.concat([df, pd.DataFrame(rows2)], ignore_index=True)

    df['value_added_inr_cr'] = df.employee_cost_inr_cr + df.ebitda_inr_cr
    df['labour_share_va'] = df.employee_cost_inr_cr / df.value_added_inr_cr
    df['employee_cost_to_revenue'] = df.employee_cost_inr_cr / df.revenue_inr_cr
    df['ebitda_margin'] = df.ebitda_inr_cr / df.revenue_inr_cr
    for c in ['revenue_inr_cr', 'employee_cost_inr_cr', 'ebitda_inr_cr', 'depreciation_inr_cr', 'value_added_inr_cr']:
        df[c] = df[c].round(1)
    for c in ['labour_share_va', 'employee_cost_to_revenue', 'ebitda_margin']:
        df[c] = df[c].round(4)

    # FY26 note: exceptional items (Labour Code / restructuring) excluded from EBITDA and employee cost
    exc = d[d.fy == 'FY26'].set_index('firm')
    exc_amt = (exc.tt_ebitda - (exc.tt_trev - exc.sales) - exc.op).round(0)
    for f, v in exc_amt.items():
        if abs(v) > 5:
            m = (df.firm == f) & (df.fy == 'FY26')
            df.loc[m, 'notes'] = (df.loc[m, 'notes'].fillna('') + f' FY26 exceptional items of ~{abs(v):,.0f} cr '
                                  '(incl. one-time new Labour Code gratuity/leave charge and/or restructuring) are EXCLUDED '
                                  'from EBITDA and employee cost.').str.strip()

    order = {f: i for i, f in enumerate(['tcs', 'infosys', 'hcltech', 'wipro', 'techm', 'lti', 'mindtree',
                                          'ltim_proforma', 'ltim', 'top6_sum', 'persistent', 'coforge', 'mphasis', 'mid3_sum'])}
    df['_o'] = df.firm.map(order)
    df = df.sort_values(['_o', 'fy']).drop(columns='_o')
    cols = ['firm', 'fy', 'revenue_inr_cr', 'employee_cost_inr_cr', 'ebitda_inr_cr', 'depreciation_inr_cr',
            'value_added_inr_cr', 'labour_share_va', 'employee_cost_to_revenue', 'ebitda_margin', 'source',
            'source_url', 'notes']
    df[cols].to_csv(os.path.join(HERE, 'firm_labour_share.csv'), index=False)
    pd.set_option('display.width', 200)
    print(df.pivot(index='fy', columns='firm', values='labour_share_va').round(3).to_string())


if __name__ == '__main__':
    main()
