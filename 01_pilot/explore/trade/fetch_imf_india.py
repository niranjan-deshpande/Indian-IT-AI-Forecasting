"""India BoP (RBI-compiled, reported to IMF BOP dataset) quarterly services credits, USD.
Source: IMF SDMX API (no key) https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/IND.CD_T.SI+SI2+SJ+S.USD.Q
Used because RBI's own Handbook XLSX (rbidocs.rbi.org.in) is behind a CAPTCHA/JS challenge for scripted access."""
import io, requests, pandas as pd
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
url = "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/IND.CD_T+DB_T.SI+SI2+SJ+S.USD.Q?startPeriod=2004"
r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=120)
d = pd.read_csv(io.StringIO(r.text), low_memory=False)
d = d[d.COUNTRY.notna()][["COUNTRY", "BOP_ACCOUNTING_ENTRY", "INDICATOR", "UNIT", "FREQUENCY", "TIME_PERIOD", "OBS_VALUE", "SCALE", "UPDATE_DATE"]]
d["url"] = url
d.to_csv("imf_bop_india_services_quarterly.csv", index=False)
print(d.groupby(["BOP_ACCOUNTING_ENTRY", "INDICATOR"]).TIME_PERIOD.agg(["min", "max", "count"]), d.SCALE.unique(), d.UPDATE_DATE.unique()[:3])
