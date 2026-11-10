#!/bin/bash
# Fetch NIRF "Data Submitted by Institution" PDFs (Engineering category) for every institution ID
# that appeared in the ranked list (top 100/200) of any edition 2019-2025, for each edition 2019-2025.
# ID list: raw/nirf/ids_ranked_engineering_2019_2025.txt (scraped from
# https://www.nirfindia.org/Rankings/<YYYY>/EngineeringRanking.html)
cd "$(dirname "$0")/raw/nirf"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for y in 2019 2020 2021 2022 2023 2024 2025; do
  sub=Engineering; [ $y = 2019 ] && sub=ENGINEERING
  mkdir -p pdf/$y
  while read id; do echo "https://www.nirfindia.org/nirfpdfcdn/$y/pdf/$sub/$id.pdf pdf/$y/$id.pdf"; done < ids_ranked_engineering_2019_2025.txt
done | xargs -P 12 -n 2 sh -c 'curl -s -f -A "'"$UA"'" -m 60 -o "$1" "$0" || rm -f "$1"'
