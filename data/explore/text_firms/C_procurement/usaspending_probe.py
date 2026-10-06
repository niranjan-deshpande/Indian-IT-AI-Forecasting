"""USAspending.gov feasibility probe: award counts & obligations by firm-group x calendar year (2018-2026).
API: https://api.usaspending.gov (no key). Recipient UEIs identified via spending_by_category/recipient name search."""
import requests, pandas as pd, time
U="https://api.usaspending.gov/api/v2/"
FIRMS={
 "TCS":[],  # name search 'Tata Consultancy' -> 0 prime contract recipients
 "Infosys":["U3ECNCGEU6S6"],
 "HCL":["CSWEUJJ4AK95","DXMYWCBFQQY1","MH4BJN91NNS4"],  # MH4BJN91NNS4 = Actian (HCL-owned software)
 "Wipro":["EFXZSFAZU6Q1","HABTUSA7ANL4","CJK7LZB1ZSM5","VDGMDCDWP8R3"],  # Appirio, ITI, Topcoder, Infocrossing
 "TechMahindra":[],
 "LTIMindtree":["VMWXM6P9DNK3"],
 "Cognizant":["QGLKHDNEX3R5","PMUXVDTHLGW5"],
 "Accenture_AFS_LLP":["C47BNA8GM833","S71BLA1TM5A6","ZGREJDD6LDQ3","NKF4GENK83K4"],
 "Accenture_acquired_subs":["TDJMB5JLT149","XDDKMXTVJSN8","EPDKY563HAG7","FMJBEPWHLRW6","CWBQY3MZT8H7"],
}
C=["A","B","C","D"]
def post(ep,body):
    for i in range(4):
        try:
            r=requests.post(U+ep,json=body,timeout=60); r.raise_for_status(); return r.json()
        except Exception as e: time.sleep(3)
    return {}
rows=[]
for f,ueis in FIRMS.items():
    for y in range(2018,2027):
        tp={"start_date":f"{y}-01-01","end_date":min(f"{y}-12-31","2026-09-30")}
        if not ueis:
            rows.append(dict(source="USAspending",firm=f,year=y,n_active_contracts=0,n_new_contracts=0,n_new_idvs=0,obligations_usd=0,subaward_usd=None)); continue
        filt={"recipient_search_text":ueis,"time_period":[tp]}
        act=post("search/spending_by_award_count/",{"filters":filt}).get("results",{})
        new=post("search/spending_by_award_count/",{"filters":{"recipient_search_text":ueis,"time_period":[dict(tp,date_type="new_awards_only")]}}).get("results",{})
        amt=post("search/spending_by_category/recipient/",{"filters":dict(filt,award_type_codes=C),"limit":100})
        ob=sum(x["amount"] for x in amt.get("results",[]) if x.get("uei") in ueis)
        rows.append(dict(source="USAspending",firm=f,year=y,n_active_contracts=act.get("contracts"),n_new_contracts=new.get("contracts"),
                         n_new_idvs=new.get("idvs"),obligations_usd=round(ob)))
        print(rows[-1])
pd.DataFrame(rows).to_csv("usaspending_counts_by_firm_year.csv",index=False)

# subawards: firm as sub-recipient (name search), whole period
sub=[]
for t in ["Tata Consultancy","Infosys","HCL America","Wipro","Tech Mahindra","Mindtree","Cognizant","Accenture"]:
    r=post("search/spending_by_category/recipient/",{"filters":{"recipient_search_text":[t],"award_type_codes":C,"time_period":[{"start_date":"2018-01-01","end_date":"2026-09-30"}]},"spending_level":"subawards","limit":10})
    for x in r.get("results",[]): sub.append(dict(term=t,name=x["name"],uei=x.get("uei"),subaward_usd_2018_2026=round(x["amount"])))
pd.DataFrame(sub).to_csv("usaspending_subawards_by_recipient.csv",index=False); print(pd.DataFrame(sub))

# award-level list for Indian firms + Cognizant (small N) for inspection
aw=[]
fields=["Award ID","Recipient Name","Award Amount","Start Date","End Date","Awarding Agency","Awarding Sub Agency","Description","NAICS","PSC","generated_internal_id"]
for f in ["Infosys","HCL","Wipro","LTIMindtree","Cognizant"]:
    for codes in [C,["IDV_A","IDV_B","IDV_B_A","IDV_B_B","IDV_B_C","IDV_C","IDV_D","IDV_E"]]:
        pg=1
        while True:
            r=post("search/spending_by_award/",{"filters":{"recipient_search_text":FIRMS[f],"award_type_codes":codes,"time_period":[{"start_date":"2018-01-01","end_date":"2026-09-30"}]},"fields":fields,"limit":100,"page":pg,"sort":"Award Amount","order":"desc"})
            for x in r.get("results",[]): x["firm"]=f; aw.append(x)
            if not r.get("page_metadata",{}).get("hasNext"): break
            pg+=1
d=pd.DataFrame(aw); d["url"]="https://www.usaspending.gov/award/"+d["generated_internal_id"].astype(str)
d.drop(columns=[c for c in ["internal_id","agency_slug","awarding_agency_id"] if c in d],errors="ignore").to_csv("usaspending_awards_indianfirms_cognizant.csv",index=False)
print(len(d))
