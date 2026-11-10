"""Fetch BEA iTable (app 62: ITA / International Services) tables without an API key.
Uses the public backend the iTable web app calls: POST https://apps.bea.gov/iTable/core/data/app/GetSteps
Returns the table as a grid (list of rows)."""
import json, requests
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
URL = "https://apps.bea.gov/iTable/core/data/app/GetSteps"

def get_step(step, data):
    body = {"appid": 62, "steps": [step], "data": [[k, str(v)] for k, v in data.items()]}
    r = requests.post(URL, json=body, headers={"User-Agent": UA}, timeout=120)
    r.raise_for_status()
    return json.loads(r.text)

def table_grid(resp):
    st = [s for s in resp["Steps"] if s["IsTable"] == 1][0]
    filters = {p["Name"]: json.loads(p["PromtData"])["Table"] for p in st["Prompts"] if p["UIControl"] != "Table"}
    tp = [p for p in st["Prompts"] if p["UIControl"] == "Table"][0]
    t = json.loads(json.loads(tp["PromtData"])["Table"]) if tp["PromtData"] and len(tp["PromtData"]) > 50 else None
    if t is None:
        return None, filters
    nr, nc = int(t["Number_Of_Rows"]), int(t["Number_Of_Columns"])
    g = [[""] * nc for _ in range(nr)]
    for c in t["TD"]:
        g[int(c["Row_ID"]) - 1][int(c["Column_ID"]) - 1] = c["Cell_Value"]
    return {"title": t["Title"], "desc": t.get("Description"), "grid": g, "nhdr": int(t["Number_Of_Header_Rows"]),
            "foot": t.get("FN") or t.get("Footnotes")}, filters
