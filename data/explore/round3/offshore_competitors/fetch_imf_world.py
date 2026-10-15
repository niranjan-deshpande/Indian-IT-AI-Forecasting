"""Computer-services exports (credits, BPM6 item SI2) and other business services (SJ) for all reporting economies, annual + quarterly, USD.
Source: IMF SDMX API, BOP dataset (no key). Same endpoint pattern as data/explore/trade/fetch_imf_india.py."""
import io, sys, requests, pandas as pd
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
url = "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/.CD_T.SI2+SJ+S.USD.A+Q?startPeriod=2012"
r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=600)
print(r.status_code, len(r.text))
d = pd.read_csv(io.StringIO(r.text), low_memory=False)
d = d[d.COUNTRY.notna()][["COUNTRY", "BOP_ACCOUNTING_ENTRY", "INDICATOR", "UNIT", "FREQUENCY", "TIME_PERIOD", "OBS_VALUE", "SCALE", "UPDATE_DATE"]]
d["url"] = url
d.to_csv(sys.argv[1], index=False)
print(d.groupby(["FREQUENCY", "INDICATOR"]).COUNTRY.nunique(), d.SCALE.unique())
