"""Parse Wipro 'Key Operating Metrics' tables (text) from quarterly presentation exhibits in EDGAR 6-Ks.
Prints label -> (cur, prev, yago) for revenue break-down and people rows. Output json: data/sources/gfc/wipro/kom.json"""
import re, json, os
B="data/sources/gfc/wipro"
PRES={ # results 6-K acc -> presentation exhibit
"0000950134-07-008992":"f29501exv99w3.htm","0000950134-07-015826":"f32110exv99w3.htm","0000950134-07-024638":"f34790exv99w3.htm",
"0000950134-08-000990":"f37267exv99w3.htm","0000950134-08-007163":"f40103exv99w3.htm","0000950134-08-013325":"f42331exv99w3.htm",
"0000950134-08-018764":"f50269exv99w3.htm","0000950134-09-001133":"f51248exv3w1.htm","0000950134-09-008587":"f52247exv99w3.htm",
"0000950123-09-026917":"f53101exv99w3.htm","0000950123-09-056551":"f53916exv99w3.htm","0000950123-10-005459":"f54728exv99w3.htm",
"0000950123-10-041641":"f55660exv99w2.htm","0000950123-10-070468":"f56475exv99w2.htm","0000950123-10-098736":"f57204exv99w2.htm",
"0000950123-11-005997":"f58049exv99w2.htm","0000950123-11-043644":"f59084exv99w2.htm","0001193125-11-195696":"dex992.htm",
"0001193125-11-302366":"d253399dex992.htm","0001193125-12-021628":"d287472dex992.htm","0001193125-12-199790":"d342992dex992.htm",
"0001193125-12-325209":"d387651dex992.htm"}
out={}
pct=r"\(?(\d+\.\d+)\s?%\)?"
for acc,ex in PRES.items():
    t=re.sub(r"\s+"," ",open(f"{B}/edgar/{acc}/{ex}.txtc").read())
    i=t.find("Revenue Break"); 
    if i<0: i=t.find("Key Operating Metrics")
    j=t.find("Customer Concentration",i)
    seg=t[i:j if j>0 else i+3000]
    shares=[(m.group(1).strip(" :-"),[float(m.group(k)) for k in (2,3,4)]) for m in re.finditer(r"([A-Za-z][A-Za-z&.,/' \-]*?)\s*:?\s*"+pct+r"\s*"+pct+r"\s*"+pct,seg)]
    people=[(m.group(1).strip(),[m.group(k) for k in (2,3,4)]) for m in re.finditer(r"(IT Services|BPO Services|India / Middle East IT Services|Total|Number of employees|Numberof employees)\s*(\(?[\d,]+\)?)\s+(\(?[\d,]+\)?)\s+(\(?[\d,]+\)?)",seg)]
    hdr=re.search(r"Particulars\s*(.{0,40}?)\s*Revenue",seg)
    out[acc]=dict(ex=ex,hdr=hdr.group(1) if hdr else None,shares=shares,people=people,seg=seg[:2500])
    print("==",acc,ex,out[acc]["hdr"]); 
    for s in shares: print("   ",s)
    for p in people: print("   P",p)
json.dump(out,open(f"{B}/kom.json","w"),indent=1)
