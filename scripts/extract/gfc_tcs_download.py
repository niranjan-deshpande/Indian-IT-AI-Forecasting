"""Download TCS FY07-FY12 investor documents (GFC window) from Wayback Machine copies of tcs.com.
tcs.com itself returns 403 (Akamai) to scripted requests, so Wayback `id_` raw captures are used.
Output: data/sources/gfc/tcs/<localname>.pdf ; manifest data/sources/gfc/tcs/_manifest.csv
"""
import csv, os, time, subprocess
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'data', 'sources', 'gfc', 'tcs')
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DOCS = [
 # (timestamp, original url, local name)
 ("20140123005927","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q4_07.PDF","TCS_Analysts_Q4FY07.pdf"),
 ("20140123005819","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q1_08.PDF","TCS_Analysts_Q1FY08.pdf"),
 ("20140123005828","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q2_08.PDF","TCS_Analysts_Q2FY08.pdf"),
 ("20140123005843","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q3_08.PDF","TCS_Analysts_Q3FY08.pdf"),
 ("20110304162702","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q4_2008.PDF","TCS_Analysts_Q4FY08.pdf"),
 ("20080910041147","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q1_09.pdf","TCS_Analysts_Q1FY09.pdf"),
 ("20090206045020","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q2_09.pdf","TCS_Analysts_Q2FY09.pdf"),
 ("20090126153439","http://www.tcs.com:80/investors/Documents/presentations/TCS_Analysts_Q3_08-09.pdf","TCS_Analysts_Q3FY09.pdf"),
 ("20090521050525","http://www.tcs.com:80/sitecollectiondocuments/investors/presentations/TCS_Analysts_Q4_09.pdf","TCS_Analysts_Q4FY09.pdf"),
 ("20090824095509","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q1_10.pdf","TCS_Analysts_Q1FY10.pdf"),
 ("20091229184223","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q2_10.pdf","TCS_Analysts_Q2FY10.pdf"),
 ("20100215050728","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_Analysts_Q3_10.pdf","TCS_Analysts_Q3FY10.pdf"),
 ("20100601164656","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_Analysts_Q4_10.pdf","TCS_Analysts_Q4FY10.pdf"),
 ("20140123005635","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q1_11.PDF","TCS_Analysts_Q1FY11.pdf"),
 ("20101129014115","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q2_11.pdf","TCS_Analysts_Q2FY11.pdf"),
 ("20110125042130","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_Analysts_Q3_11.pdf","TCS_Analysts_Q3FY11.pdf"),
 ("20111027120950","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q4_11.pdf","TCS_Analysts_Q4FY11.pdf"),
 ("20110812184123","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_Analysts_Q1_12.pdf","TCS_Analysts_Q1FY12.pdf"),
 ("20111216004635","http://www.tcs.com:80/investors/Documents/Presentations/TCS_Analysts_Q2_12.PDF","TCS_Analysts_Q2FY12.pdf"),
 ("20120131144553","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_Analysts_Q3_12.pdf","TCS_Analysts_Q3FY12.pdf"),
 ("20140123005626","http://www.tcs.com/investors/Documents/Presentations/TCS_Analysts_Q4_12.PDF","TCS_Analysts_Q4FY12.pdf"),
 # operating metrics (fact sheets)
 ("20090411073308","http://www.tcs.com:80/investors/Documents/financial%20statements/TCS_OperatingMetrics_Q3_09.pdf","TCS_OperatingMetrics_Q3FY09.pdf"),
 ("20090824095421","http://www.tcs.com:80/investors/Documents/Financial%20Statements/TCS_OperatingMetrics_Q1_10.pdf","TCS_OperatingMetrics_Q1FY10.pdf"),
 ("20110812183926","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_OperatingMetrics_Q1_12.pdf","TCS_OperatingMetrics_Q1FY12.pdf"),
 # press releases (US GAAP / IFRS USD)
 ("20070421050744","http://www.tcs.com:80/pdf/TCS_PressRelease_USGAAP_Q4_07.pdf","TCS_PR_USGAAP_Q4FY07.pdf"),
 ("20161020022541","http://www.tcs.com/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q2_08.PDF","TCS_PR_USGAAP_Q2FY08.pdf"),
 ("20120227120502","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q4_08.PDF","TCS_PR_USGAAP_Q4FY08.pdf"),
 ("20090126162357","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q3_09.pdf","TCS_PR_USGAAP_Q3FY09.pdf"),
 ("20100331105739","http://www.tcs.com:80/investors/documents/Press%20Releases/TCS_PressRelease_USGAAP_Q4_09.pdf","TCS_PR_USGAAP_Q4FY09.pdf"),
 ("20091025000821","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q1_10.pdf","TCS_PR_USGAAP_Q1FY10.pdf"),
 ("20100401070620","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_USGAAP_Q3_10.pdf","TCS_PR_USGAAP_Q3FY10.pdf"),
 ("20100816181422","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q4_10.pdf","TCS_PR_USGAAP_Q4FY10.pdf"),
 ("20101011141652","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_USGAAP_Q1_11.pdf","TCS_PR_USGAAP_Q1FY11.pdf"),
 ("20101129014128","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q2_11.pdf","TCS_PR_USGAAP_Q2FY11.pdf"),
 ("20110125042511","http://www.tcs.com:80/investors/Documents/Press%20Releases/TCS_PressRelease_USGAAP_Q3_11.pdf","TCS_PR_USGAAP_Q3FY11.pdf"),
 ("20110516175334","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_USGAAP_Q4_11.pdf","TCS_PR_USGAAP_Q4FY11.pdf"),
 ("20110812184040","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_IFRS_Q1_12.pdf","TCS_PR_IFRS_Q1FY12.pdf"),
 ("20111027023716","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_IFRS_Q2_12.pdf","TCS_PR_IFRS_Q2FY12.pdf"),
 ("20120907113127","http://www.tcs.com:80/SiteCollectionDocuments/Investors/Presentations/TCS_PressRelease_IFRS_USD_Q4_12.pdf","TCS_PR_IFRS_USD_Q4FY12.pdf"),
]
def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for ts, url, name in DOCS:
        dest = os.path.join(OUT, name)
        wb = f"https://web.archive.org/web/{ts}id_/{url}"
        if not (os.path.exists(dest) and open(dest,'rb').read(4) == b'%PDF'):
            for attempt in range(3):
                subprocess.run(["curl","-sL","-A",UA,"--max-time","180","-o",dest,wb])
                if os.path.exists(dest) and open(dest,'rb').read(4) == b'%PDF':
                    break
                time.sleep(5)
            time.sleep(1)
        ok = os.path.exists(dest) and open(dest,'rb').read(4) == b'%PDF'
        print(ok, name)
        rows.append({"local": name, "archive_url": f"https://web.archive.org/web/{ts}/{url}", "original_url": url, "ok": ok})
    with open(os.path.join(OUT, '_manifest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=["local","archive_url","original_url","ok"]); w.writeheader(); w.writerows(rows)
if __name__ == '__main__':
    main()
