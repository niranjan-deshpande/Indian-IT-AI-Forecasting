"""Download consolidated annual P&L data for Indian IT services firms.

Sources (saved untouched to raw/firms/):
  - Screener.in consolidated company page (P&L table: Sales, Expenses, Operating Profit,
    Other Income, Interest, Depreciation; Mar-ending fiscal years)
  - Screener.in expense schedule API (Employee Cost % of sales, integer-rounded)
  - Tickertape annual income API (absolute employee cost 'incEpc', FY17-FY26)

Downloads are data only; parse them with parse_firm_financials.py (run with python3 -I).
Polite: sleeps 2.5 s between requests; skips files already downloaded.
"""
import os, subprocess, time, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw', 'firms')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120 Safari/537.36')

# firm key -> (screener symbol, tickertape sid)
FIRMS = {
    'tcs': ('TCS', 'TCS'),
    'infosys': ('INFY', 'INFY'),
    'hcltech': ('HCLTECH', 'HCLT'),
    'wipro': ('WIPRO', 'WIPR'),
    'techm': ('TECHM', 'TEML'),
    'ltim': ('LTM', 'LRTI'),  # LTIMindtree (renamed LTM Ltd on Screener) = renamed L&T Infotech entity
    'mindtree': ('MINDTREE', 'MINT'),  # delisted Nov 2022 after merger
    'persistent': ('PERSISTENT', 'PERS'),
    'coforge': ('COFORGE', 'COFO'),
    'mphasis': ('MPHASIS', 'MBFL'),
}


def get(url, out, referer=None):
    if os.path.exists(out) and os.path.getsize(out) > 500:
        return False
    cmd = ['curl', '-sL', '--max-time', '60', '-A', UA, '-o', out, '-w', '%{http_code}']
    if referer:
        cmd += ['-H', f'Referer: {referer}']
    code = subprocess.run(cmd + [url], capture_output=True, text=True).stdout
    print(code, url)
    return True


def main():
    os.makedirs(RAW, exist_ok=True)
    for key, (scr, tt) in FIRMS.items():
        page = f'https://www.screener.in/company/{scr}/consolidated/'
        f_page = os.path.join(RAW, f'screener_{scr}_consolidated.html')
        if get(page, f_page):
            time.sleep(2.5)
        html = open(f_page, errors='ignore').read()
        m = re.search(r'data-company-id="(\d+)"', html)
        if m:
            cid = m.group(1)
            api = (f'https://www.screener.in/api/company/{cid}/schedules/'
                   '?parent=Expenses&section=profit-loss&consolidated=')
            if get(api, os.path.join(RAW, f'screener_{scr}_expenses.json'), referer=page):
                time.sleep(2.5)
        else:
            print('no company id for', scr)
        tturl = f'https://api.tickertape.in/stocks/financials/income/{tt}/annual/normal?count=10'
        if get(tturl, os.path.join(RAW, f'tickertape_{tt}_income_annual.json')):
            time.sleep(2.5)


if __name__ == '__main__':
    main()
