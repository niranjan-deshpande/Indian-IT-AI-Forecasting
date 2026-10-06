"""Polite Wayback Machine helper for the HCLTech GFC collection.
Usage:
  python gfc_hcltech_wayback.py cdx '<cdx query string>'     -> prints CDX rows
  python gfc_hcltech_wayback.py get <timestamp> <original_url> <outfile>
Retries with backoff when archive.org returns its 'Temporarily Offline' page.
"""
import sys, time, requests
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
S = requests.Session(); S.headers["User-Agent"] = UA

def fetch(url, tries=8, timeout=120):
    delay = 5
    for i in range(tries):
        try:
            r = S.get(url, timeout=timeout, allow_redirects=True)
            body = r.content
            if r.status_code == 200 and b"Temporarily Offline" not in body[:600]:
                return r
            sys.stderr.write(f"try {i}: status {r.status_code} len {len(body)}\n")
        except Exception as e:
            sys.stderr.write(f"try {i}: {e}\n")
        time.sleep(delay); delay = min(delay * 2, 90)
    return None

if __name__ == "__main__":
    if sys.argv[1] == "cdx":
        r = fetch("http://web.archive.org/cdx/search/cdx?" + sys.argv[2])
        print(r.text if r else "FAILED")
    elif sys.argv[1] == "get":
        ts, orig, out = sys.argv[2:5]
        r = fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
        if r is None:
            print("FAILED", orig); sys.exit(1)
        open(out, "wb").write(r.content)
        print("OK", out, len(r.content), r.headers.get("content-type"), r.url)
        time.sleep(1)
