"""Fetch an SEC htm exhibit and save as plain text. Usage: python sec_text.py name url"""
import sys, os, re, html, urllib.request
SCR = os.environ.get("SCR", "/tmp")
UA = {"User-Agent": "ndeshpande research ndeshpande@college.harvard.edu"}
raw = urllib.request.urlopen(urllib.request.Request(sys.argv[2], headers=UA)).read().decode("utf-8", "ignore")
raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
raw = re.sub(r"(?i)</(tr|p|div|br|h\d)>", "\n", raw)
raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
t = "\n".join(re.sub(r"[ \t\xa0|]+", lambda m: " | " if "|" in m.group() else " ", l).strip(" |") for l in t.splitlines())
t = re.sub(r"\n\s*\n+", "\n", t)
open(os.path.join(SCR, sys.argv[1] + ".txt"), "w").write(t)
print(sys.argv[1], len(t))
