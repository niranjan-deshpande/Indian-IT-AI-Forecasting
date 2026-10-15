"""EU27 imports (debits) of computer services (SI2) and total services (S) by partner, Eurostat bop_its6_det, MIO_EUR, annual.
API (no key): https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/bop_its6_det"""
import sys, json, itertools, requests, pandas as pd
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/bop_its6_det"
rows = []
for item in ["SI2", "S"]:
    url = f"{BASE}?format=JSON&lang=EN&geo=EU27_2020&bop_item={item}&stk_flow=DEB&currency=MIO_EUR&sinceTimePeriod=2010"
    d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=300).json()
    dims = d["id"]; size = d["size"]
    cats = [sorted(d["dimension"][k]["category"]["index"].items(), key=lambda x: x[1]) for k in dims]
    labs = {k: d["dimension"][k]["category"]["label"] for k in dims}
    for idx, combo in enumerate(itertools.product(*cats)):
        if str(idx) in d["value"]:
            r = {k: c[0] for k, c in zip(dims, combo)}
            r["partner_label"] = labs["partner"][r["partner"]]; r["value_meur"] = d["value"][str(idx)]
            r["flag"] = d.get("status", {}).get(str(idx), ""); r["url"] = url
            rows.append(r)
pd.DataFrame(rows).to_csv(sys.argv[1], index=False)
print(len(rows), d.get("updated"))
