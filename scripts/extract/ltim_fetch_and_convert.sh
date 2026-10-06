#!/bin/bash
# Reproduce source downloads + text conversion for LTI / Mindtree / LTIMindtree (firm id ltim).
# Run from project root.
set -e
S="data/sources/ltim"; UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
mkdir -p $S/txt $S/mindtree/nse/txt $S/lti_nse
# 1) ltm.com (ex-ltimindtree.com) investor financial-results listing (AEM JSON), FY2017..FY2027
for y in 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026 2027; do
  curl -sL -A "$UA" "https://www.ltm.com/content/ltimcorporatewebsite/us/investors/financial-results/jcr:content/root/container/investorfinancial.json?year=$y&investorType=ltimcorporatewebsite:investors/financial-results" -o $S/fr_$y.json
done
# download_index.tsv (filename -> URL) lists the Earnings Release & Fact Sheet / Investor Presentation PDFs
while IFS=$'\t' read fn url; do [ -s "$S/$fn" ] || curl -sL -A "$UA" -o "$S/$fn" "$url"; done < $S/download_index.tsv
for f in $S/*.pdf; do b=$(basename "$f" .pdf); pdftotext -layout "$f" "$S/txt/$b.txt"; done
# 2) Mindtree results filings from NSE (announcements API; needs cookie from nseindia.com home page)
python3 scripts/extract/ltim_nse_announcements.py MINDTREE 2015-04-01 2022-12-31 $S/mindtree/nse_mindtree_announcements.json
python3 scripts/extract/ltim_nse_download.py $S/mindtree/nse_mindtree_announcements.json $S/mindtree/nse
(cd $S/mindtree/nse && for z in *.zip; do mkdir -p unz/${z%.zip}; unzip -o -q "$z" -d unz/${z%.zip} || true; done)
find $S/mindtree/nse/unz -name '*.pdf' | while read f; do pdftotext -layout "$f" "$S/mindtree/nse/txt/$(basename "$(dirname "$f")").txt"; done
for f in $S/mindtree/nse/*.pdf; do pdftotext -layout "$f" "$S/mindtree/nse/txt/$(basename "$f" .pdf).txt"; done
# 3) LTI NSE copies (NSE symbol is now LTM) for quarters whose ltm.com fact sheet is image-only / garbled
#    Q4FY17 LTI_Results_04052017164048.zip ; Q1FY20 listcontract3_18072019191541_larsen_outcome_387.pdf ;
#    Q1FY23 LTI_14072022152621_OutcomeofBoardmeeting.pdf  (https://nsearchives.nseindia.com/corporate/<name>)
# 4) Build CSV
python3 scripts/extract/ltim_build.py
