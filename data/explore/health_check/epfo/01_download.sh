#!/bin/bash
# Download archived EPFO "Net Payroll Data" monthly reports via the Internet Archive.
# epfindia.gov.in / epfo.gov.in return HTTP 403 (CloudFront geo-block) from outside India,
# so each official PDF is fetched from its Wayback Machine capture (byte-identical "id_" mode).
# Input: wayback_captures.txt (lines: <timestamp> <original URL>), built from the Wayback CDX API.
cd "$(dirname "$0")"
mkdir -p raw
while read ts url; do
  base=$(basename "${url%%\?*}")
  out="raw/${base%.pdf}__wb${ts}.pdf"
  [ -s "$out" ] && continue
  curl -sL -m 240 -o "$out" "https://web.archive.org/web/${ts}id_/${url}"
  if ! file "$out" | grep -q PDF; then echo "FAILED $ts $url"; rm -f "$out"; fi
  sleep 1
done < wayback_captures.txt
