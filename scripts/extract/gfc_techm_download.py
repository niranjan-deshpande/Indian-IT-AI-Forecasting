"""Download Tech Mahindra GFC-era (FY07-FY12) investor documents from Wayback Machine copies
of techmahindra.com. Captures found via the Wayback CDX API (see gfc_techm_notes.md).
Saves to data/sources/gfc/techm/ and writes manifest.csv (local file, wayback URL, original URL)."""
import csv, os, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'data', 'sources', 'gfc', 'techm')
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
FC = 'http://techmahindra.com/Documents/Financials/financialchart/'
FCW = 'http://www.techmahindra.com:80/Documents/Financials/financialchart/'
CI = 'http://techmahindra.com/content/investor/'
DOCS = [  # (local name, timestamp, original url)
 ('TechM_Q4_F07_Consolidated.pdf', '20120327030045', FC + '2006-07/TechM_Q4_F07_Consolidated.pdf'),
 ('Tech_Mahindra_Fact_Sheet_200702.pdf', '20070202144357', 'http://www.techmahindra.com:80/content/investors/Tech_Mahindra_Fact_Sheet.pdf'),
 ('TechM_Q1_F08_Factsheet.pdf', '20110919192433', FCW + '08_q1/TechM_Q1_F08_Factsheet.pdf'),
 ('TechM_Q1_F08_Consolidated.pdf', '20110919192247', FCW + '08_q1/TechM_Q1_F08_Consolidated.pdf'),
 ('TechM_Q2_F08_Factsheet.pdf', '20120327220918', FC + '08_q2/TechM_Q2_F08_Factsheet.pdf'),
 ('TechM_Q2_F08_Consolidated.pdf', '20120327221953', FC + '08_q2/TechM_Q2_F08_Consolidated.pdf'),
 ('TechM_Q3_F08_Factsheet.pdf', '20120327104912', FC + '08_q3/TechM_Q3_F08_Factsheet.pdf'),
 ('TechM_Q3_F08_Consolidated.pdf', '20120327031336', FC + '08_q3/TechM_Q3_F08_Consolidated.pdf'),
 ('TechM_Q4_F08_Factsheet.pdf', '20120327105353', FC + '08_q4/TechM_Q4_F08_Factsheet.pdf'),
 ('TechM_Q4_F08_Consolidated.pdf', '20120327130255', FC + '08_q4/TechM_Q4_F08_Consolidated.pdf'),
 ('TechM_Q1_F09_Factsheet.pdf', '20120327083818', FC + '09/TechM_Q1_F09_Factsheet.pdf'),
 ('TechM_Q1_F09_Consolidated.pdf', '20120327035211', FC + '09/TechM_Q1_F09_Consolidated.pdf'),
 ('TechM_Q2_F09_Factsheet.pdf', '20110919195416', FCW + '09_q2/TechM_Q2_F09_Factsheet.pdf'),
 ('TechM_Q2_F09_Consolidated.pdf', '20120327221228', FC + '09_q2/TechM_Q2_F09_Consolidated.pdf'),
 ('TechM_Q3_F09_Factsheet.pdf', '20120327024402', FC + '09_q3/TechM_Q3_F09_Factsheet.pdf'),
 ('TechM_Q3_F09_Consolidated.pdf', '20120327144710', FC + '09_q3/TechM_Q3_F09_Consolidated.pdf'),
 ('TechM_Q4_F09_Factsheet.pdf', '20120327045821', FC + '2009/TechM_Q4_F09_Factsheet.pdf'),
 ('TechM_Q4_F09_Consolidated.pdf', '20120327221056', FC + '2009/TechM_Q4_F09_Consolidated.pdf'),
 ('TechM_Q1_F10_Factsheet.pdf', '20120327090528', FC + '2009-10/TechM_Q1_F10_Factsheet.pdf'),
 ('TechM_Q1_F10_Consolidated.pdf', '20120327044640', FC + '2009-10/TechM_Q1_F10_Consolidated.pdf'),
 ('TechM_Q2_F10_Factsheet.pdf', '20120327221157', FC + '2009-10/TechM_Q2_F10_Factsheet.pdf'),
 ('TechM_Q2_F10_Consolidated.pdf', '20110919210135', FCW + '2009-10/TechM_Q2_F10_Consolidated.pdf'),
 ('TechM_Q3_F10_Consolidated.pdf', '20120327063728', FC + '2009-10/TechM_Q3_F10_Consolidated.pdf'),
 ('TechM_Q3_F10_Calltranscripts.pdf', '20120327105858', FC + '2009-10/TechM_Q3_F10_Calltranscripts.pdf'),
 ('TechM_Q4_F10_Factsheet.pdf', '20120327220747', FC + '2009-10/TechM_Q4_F10_Factsheet.pdf'),
 ('TechM_Q4_F10_Consolidated.pdf', '20120327124245', FC + '2009-10/TechM_Q4_F10_Consolidated.pdf'),
 ('TechM_Q1_F11_Factsheet.pdf', '20120327131309', FC + '2010-2011/TechM_Q1_F11_Factsheet.pdf'),
 ('TechM_Q1_F11_Consolidated.pdf', '20110919214209', FCW + '2010-2011/TechM_Q1_F11_Consolidated.pdf'),
 ('TechM_Q2_F11_Factsheet.pdf', '20120327150554', FC + '2010-2011/TechM_Q2_F11_Factsheet.pdf'),
 ('TechM_Q2_F11_Consolidated.pdf', '20120327150856', FC + '2010-2011/TechM_Q2_F11_Consolidated.pdf'),
 ('TechM_Q3_F11_Factsheet.pdf', '20120327221654', FC + '2010-2011/TechM_Q3_F11_Factsheet.pdf'),
 ('TechM_Q3_F11_Consolidated.pdf', '20120327140648', FC + '2010-2011/TechM_Q3_F11_Consolidated.pdf'),
 ('TechM_Q4_F11_Factsheet.pdf', '20120327220540', FC + '2010-2011/TechM_Q4_F11_Factsheet.pdf'),
 ('TechM_Q4_F11_Consolidated.pdf', '20120327095744', FC + '2010-2011/TechM_Q4_F11_Consolidated.pdf'),
 ('TechM_Q1_F12_Factsheet.pdf', '20120327023537', FC + '2011-2012/TechM_Q1_F12_Factsheet.pdf'),
 ('TechM_Q1_F12_Consolidated.pdf', '20120327221042', FC + '2011-2012/TechM_Q1_F12_Consolidated.pdf'),
 ('Factsheet_Q2F12.pdf', '20120327220826', FC + '2011-2012/Factsheet_Q2F12.pdf'),
 ('Consolidated_Q2F12.pdf', '20120327111825', FC + '2011-2012/Consolidated_Q2F12.pdf'),
 ('Factsheet_Q3F12.pdf', '20130828234230', FCW + '2011-2012/Factsheet_Q3F12.pdf'),
 ('Consolidated_Q3F12.pdf', '20130828234208', FCW + '2011-2012/Consolidated_Q3F12.pdf'),
 ('Factsheet_Q4F12.pdf', '20130828234144', FCW + '2011-2012/Factsheet_Q4F12.pdf'),
 ('Consolidated_Q4F12.pdf', '20130828234219', FCW + '2011-2012/Consolidated_Q4F12.pdf'),
 # older content/investor copies (same factsheets under earlier names; for vintage cross-check)
 ('TML_Consol_Factsheet_data_13_Qtrs_Q1_07_08.pdf', '20091231000649', CI + 'TML_Consol_Factsheet_data_13_Qtrs_Q1_07_08.pdf'),
 ('TML_Consol_Factsheet_data.pdf', '20091231000739', CI + 'TML%20Consol%20Factsheet%20data.pdf'),
 ('TML_Consol_Factsheet_data_11_Qtrs.pdf', '20090424012837', 'http://www.techmahindra.com:80/content/investor/TML%20Consol%20Factsheet%20data%20-%2011%20Qtrs.pdf'),
 ('TML_Consol_Factsheet_data_Q2F10.pdf', '20091231001043', CI + 'TML%20Consol%20Factsheet%20data%20Q2F10.pdf'),
 ('annual_report_0708.pdf', '20090419033747', 'http://www.techmahindra.com:80/content/investor/annual_report_0708.pdf'),
 ('TML_AR_2009_final.pdf', '20091122132446', 'http://techmahindra.com/content/investor/TML_AR_2009_final.pdf'),
 ('TML_Consol_Factsheet_data_10_Qtrs_Q2_07_08.pdf', '20091231002436', CI + 'TML_Consol_Factsheet_data_10_Qtrs_in_Rs_&_$_Q2_07_08.pdf'),
 ('TML_Consol_Factsheet_data_11_Qtrs_Q3_07_08.pdf', '20091231002018', CI + 'TML_Consol_Factsheet_data_11_Qtrs_in_INR_and_USD_Q3_07_08.pdf'),
 ('TML_Consol_Factsheet_data_12_Qtrs_Q4_07_08.pdf', '20091231000952', CI + 'TML_Consol_Factsheet_data_12_Qtrs_in_INR_&_USD_Q4_07_08.pdf'),
 ('TML_Consol_Factsheet_data_9_Qtrs_Q1_09.pdf', '20091231000939', CI + 'TML%20Consol%20Factsheet%20data%20-%209%20Qtrs_Q1%2009.pdf'),
 ('TML_Consol_Factsheet_data_10_Qtrs_Q2_09.pdf', '20091231001123', CI + 'TML%20Consol%20Factsheet%20data%20-%2010%20Qtrs_Q2%2009.pdf'),
 ('TML_Consol_Factsheet_data_Q1F10.pdf', '20091231001944', CI + 'TML_Consol_Factsheet_data_Q1F10.pdf'),
 ('TechM_Q4_F09_Statement.pdf', '20120327085351', FC + '2009/TechM_Q4_F09_Statement.pdf'),
 ('TechM_Q1_F08_Calltranscripts.pdf', '20120327135210', FC + '08_q1/TechM_Q1_F08_Calltranscripts.pdf'),
 ('TechM_Q2_F08_Calltranscripts.pdf', '20120327085926', FC + '08_q2/TechM_Q2_F08_Calltranscripts.pdf'),
 ('TechM_Q3_F08_Calltranscripts.pdf', '20120327022456', FC + '08_q3/TechM_Q3_F08_Calltranscripts.pdf'),
 ('TechM_Q4_F08_Calltranscripts.pdf', '20120327220553', FC + '08_q4/TechM_Q4_F08_Calltranscripts.pdf'),
 ('TechM_Q1_F09_Calltranscripts.pdf', '20120327010303', FC + '09/TechM_Q1_F09_Calltranscripts.pdf'),
 ('TechM_Q2_F09_Calltranscripts.pdf', '20120327221318', FC + '09_q2/TechM_Q2_F09_Calltranscripts.pdf'),
 ('TechM_Q3_F09_Calltranscripts.pdf', '20120327042445', FC + '09_q3/TechM_Q3_F09_Calltranscripts.pdf'),
 ('TechM_Q4_F09_Calltranscripts.pdf', '20110919193155', FCW + '2009/TechM_Q4_F09_Calltranscripts.pdf'),
 ('TechM_Q1_F10_Calltranscripts.pdf', '20120326234117', FC + '2009-10/TechM_Q1_F10_Calltranscripts.pdf'),
 ('TechM_Q2_F10_Calltranscripts.pdf', '20120327073425', FC + '2009-10/TechM_Q2_F10_Calltranscripts.pdf'),
 ('TechM_Q4_F10_Calltranscripts.pdf', '20120327074455', FC + '2009-10/TechM_Q4_F10_Calltranscripts.pdf'),
 ('TechM_Q1_F11_Calltranscripts.pdf', '20120327101802', FC + '2010-2011/TechM_Q1_F11_Calltranscripts.pdf'),
 ('TechM_Q2_F11_Calltranscripts.pdf', '20120327221902', FC + '2010-2011/TechM_Q2_F11_Calltranscripts.pdf'),
 ('TechM_Q3_F11_Calltranscripts.pdf', '20110812095756', FCW + '2010-2011/TechM_Q3_F11_Calltranscripts.pdf'),
 ('TechM_Q4_F11_Calltranscripts.pdf', '20120327221558', FC + '2010-2011/TechM_Q4_F11_Calltranscripts.pdf'),
 ('TechM_Q1_F12_Calltranscripts.pdf', '20120327012804', FC + '2011-2012/TechM_Q1_F12_Calltranscripts.pdf'),
 ('Calltranscripts_Q2F12.pdf', '20120327045615', FC + '2011-2012/Calltranscripts_Q2F12.pdf'),
 ('Calltranscripts_Q3F12.pdf', '20130828234123', FCW + '2011-2012/Calltranscripts_Q3F12.pdf'),
 ('Calltranscripts_Q4F12.pdf', '20130828234132', FCW + '2011-2012/Calltranscripts_Q4F12.pdf'),
 ('TechMahindra_transcript.pdf', '20090424012844', 'http://www.techmahindra.com:80/content/investor/TechMahindra_transcript.pdf'),
 ('AR_2010.pdf', '20120327130029', FC + '2010.pdf'),
 ('TML_Annual_Report_2010_2011.pdf', '20111216071548', 'http://www.techmahindra.com:80/Documents/Financials/AnnualReports/TML_Annual_Report_2010_2011.pdf'),
]
def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, ts, orig in DOCS:
        wb = f'https://web.archive.org/web/{ts}/{orig}'
        raw = f'https://web.archive.org/web/{ts}id_/{orig}'
        path = os.path.join(OUT, name)
        if not (os.path.exists(path) and os.path.getsize(path) > 1000):
            for attempt in range(3):
                r = subprocess.run(['curl', '-s', '-L', '-A', UA, '--max-time', '180', '-o', path, raw])
                if os.path.exists(path) and open(path, 'rb').read(4) == b'%PDF':
                    break
                time.sleep(10)
            time.sleep(1.5)
        ok = os.path.exists(path) and open(path, 'rb').read(4) == b'%PDF'
        print(name, 'OK' if ok else 'FAIL', os.path.getsize(path) if os.path.exists(path) else 0)
        rows.append({'file': name, 'wayback_url': wb, 'original_url': orig.replace(':80/', '/'), 'ok': ok})
    with open(os.path.join(OUT, 'manifest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
if __name__ == '__main__':
    main()
