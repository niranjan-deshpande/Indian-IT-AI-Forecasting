"""Fetch free trade-in-services data for the Baldwin / ING reproductions.
1) WTO ITS_CS_QX (commercial services exports by main sector, quarterly, partner World) via the DBnomics mirror
   (https://db.nomics.world/WTO/ITS_CS_QX; WTO's own API needs a subscription key). Reporters: Baldwin's nine.
2) WTO ITS_CS_AX6 (annual, by sector and partner) for the same plus World, sectors S, SI, SJ, SOX.
3) IMF BOP (SDMX, no key) India quarterly credits S, SI, SI2, SI1, SI3, SJ.

Raw JSON/CSV written to ../raw_output/{wto,imf}/. Run: python3 -I fetch_wto_imf.py <raw_output_dir>"""
import sys, os, json, io, urllib.request, urllib.parse
RAW = sys.argv[1]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"}
def get(url, accept=None):
    h = dict(UA)
    if accept: h["Accept"] = accept
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=600) as r:
        return r.read()
NINE = ["840", "826", "356", "276", "702", "250", "156", "056", "608"]
def dn(dataset, dims, fname):
    if os.path.exists(os.path.join(RAW, "wto", fname)): print("skip", fname); return
    q = urllib.parse.quote(json.dumps(dims))
    url = f"https://api.db.nomics.world/v22/series/WTO/{dataset}?dimensions={q}&observations=1&limit=1000"
    b = get(url); open(os.path.join(RAW, "wto", fname), "wb").write(b)
    d = json.loads(b); print(dataset, fname, d["series"]["num_found"], d["dataset"].get("indexed_at"))
dn("ITS_CS_QX", {"reporting-economies": NINE, "partner-economies": ["000"], "products-sector": ["S", "SI", "SJ", "SOX"]}, "its_cs_qx_nine.json")
dn("ITS_CS_AX6", {"reporting-economies": NINE + ["000"], "partner-economies": ["000"], "products-sector": ["S", "SI", "SI2", "SJ", "SJ1", "SJ2", "SJ3", "SOX"]}, "its_cs_ax6_nine.json")
# IMF India quarterly, and Baldwin's other eight (computer SI2 + OBS SJ)
def imf_get(url, fname):
    if os.path.exists(os.path.join(RAW, "imf", fname)): print("skip", fname); return
    b = get(url, "application/vnd.sdmx.data+csv;version=1.0.0")
    open(os.path.join(RAW, "imf", fname), "wb").write(b); print(fname, len(b))
imf_get("https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/IND.CD_T.S+SI+SI1+SI2+SI3+SJ.USD.Q?startPeriod=2005", "imf_bop_ind_q.csv")
imf_get("https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/USA+GBR+DEU+SGP+FRA+CHN+BEL+PHL.CD_T.SI2+SJ.USD.Q?startPeriod=2010", "imf_bop_eight_q.csv")
# --- added for ING check -------------------------------------------------------------------
# 5) IMF WEO (DataMapper API) nominal GDP in USD bn; India is on a fiscal-year basis (2025 = FY2025/26)
if not os.path.exists(os.path.join(RAW, "imf", "weo_ngdpd.json")):
    req = urllib.request.Request("https://www.imf.org/external/datamapper/api/v1/NGDPD/IND", headers={"User-Agent": "curl/8.4.0"})  # site 403s browser-like UAs
    b = urllib.request.urlopen(req, timeout=300).read()
    open(os.path.join(RAW, "imf", "weo_ngdpd.json"), "wb").write(b); print("weo", len(b))
# 6) IMF BOP annual credits, all reporters, digitally deliverable BPM6 items (UNCTAD/WTO definition:
#    insurance SF, financial SG, IP charges SH, telecom-computer-info SI, other business SJ, audiovisual SK1) + total S
imf_get("https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/.CD_T.S+SF+SG+SH+SI+SJ+SK1+SK.USD.A?startPeriod=2015", "imf_bop_all_annual_dds.csv")
# 7) WTO quarterly India deliverable items (for 2025 Q-based totals)
dn("ITS_CS_QX", {"reporting-economies": ["356"], "partner-economies": ["000"], "products-sector": ["S", "SF", "SG", "SH", "SI", "SJ", "SK"]}, "its_cs_qx_india_dds.json")
# 8) IMF India quarterly credits for all main BPM6 items (Economic Survey Box VII.2 replication)
imf_get("https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/IND.CD_T.S+SA+SB+SC+SD+SE+SF+SG+SH+SI+SI1+SI2+SI3+SJ+SJ1+SJ2+SJ3+SK+SL.USD.Q?startPeriod=2010", "imf_bop_ind_q_allitems.csv")
