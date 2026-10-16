"""Count AI mentions in the 183 earnings-call transcripts listed in audit/calls_transcripts.csv.

Inputs : audit/calls_transcripts.csv (local_path -> PDF or SEC .htm exhibit under data/sources/, git-ignored)
Outputs: data/explore/health_check/charts/ai_mentions_halfyear.csv  (one row per half-year)
         data/explore/health_check/charts/ai_mentions_by_call.csv   (one row per transcript; audit trail)

Text extraction: pdftotext -layout is NOT used (columns would split phrases); plain `pdftotext` to stdout.
.htm exhibits are stripped of tags with a regex and HTML entities unescaped. Whitespace is collapsed
so phrases broken across lines still match.

Patterns (applied to the whole transcript, including operator text and safe-harbour boilerplate):
  ai_word     : r'\bAI\b' case-sensitive (matches "AI", "AI-led", "AI's", "Gen AI", "generative AI";
                does NOT match the single token "GenAI") + 'artificial intelligence' (case-insensitive)
  genai       : 'GenAI' / 'Gen AI' / 'Gen-AI' / 'generative AI' / 'generative artificial intelligence'
                (case-insensitive). Overlaps ai_word except for the single token "GenAI".
  agentic     : 'agentic' + 'AI agent' / 'AI agents' (case-insensitive)
  ai_any      : ai_word + occurrences of the single token "GenAI" (so every AI reference counts once)
Words: whitespace-separated tokens containing at least one letter.
"""
import html
import re
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

PAT = {
    "ai_word": re.compile(r"\bAI\b|(?i:\bartificial\s+intelligence\b)"),
    "genai_token": re.compile(r"(?i)\bgenai\b"),
    "genai": re.compile(r"(?i)\bgen(?:\s+|-)?ai\b|\bgenerative\s+(?:ai|artificial\s+intelligence)\b"),
    "agentic": re.compile(r"(?i)\bagentic\b|\bai\s+agents?\b"),
}
WORD = re.compile(r"\S*[A-Za-z]\S*")


def extract(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"],
                           capture_output=True, text=True, errors="replace")
        txt = r.stdout
    else:
        raw = path.read_text(errors="replace")
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", txt)


def main():
    calls = pd.read_csv(ROOT / "audit/calls_transcripts.csv")
    rows = []
    for _, c in calls.iterrows():
        t = extract(ROOT / c.local_path)
        n = {k: len(p.findall(t)) for k, p in PAT.items()}
        rows.append(dict(firm=c.firm, call=c.call, call_date=c.call_date, half_year=c.half_year,
                         words=len(WORD.findall(t)), ai_word=n["ai_word"], genai=n["genai"],
                         agentic=n["agentic"], ai_any=n["ai_word"] + n["genai_token"],
                         local_path=c.local_path))
    bc = pd.DataFrame(rows)
    bc.to_csv(OUT / "ai_mentions_by_call.csv", index=False)

    g = bc.groupby("half_year").agg(n_calls=("call", "size"), words=("words", "sum"),
                                     ai_any=("ai_any", "sum"), ai_word=("ai_word", "sum"),
                                     genai=("genai", "sum"), agentic=("agentic", "sum"))
    out = pd.DataFrame({"half_year": g.index, "n_calls": g.n_calls.values,
                        "total_words": g.words.values})
    for k in ["ai_any", "ai_word", "genai", "agentic"]:
        out[f"{k}_count"] = g[k].values
        out[f"{k}_per_10k_words"] = (g[k] / g.words * 1e4).round(2).values
        out[f"{k}_per_call"] = (g[k] / g.n_calls).round(2).values
    out["low_n_flag"] = (out.n_calls < 12).map({True: "few calls (partial half-year)", False: ""})
    out["source"] = "audit/calls_transcripts.csv transcripts; count_ai_mentions.py"
    with open(OUT / "ai_mentions_halfyear.csv", "w") as f:
        f.write("# AI mentions on earnings calls (8 firms: TCS, Infosys, HCLTech, Wipro, TechM, LTIMindtree, "
                "Cognizant, Accenture). Pooled rate = sum(mentions)/sum(words)*10k. ai_any = 'AI' whole word "
                "(case-sensitive) + 'artificial intelligence' + token 'GenAI'; ai_word = same without the single token "
                "'GenAI' (comparable to the earlier read-only pass); genai and agentic are sub-families "
                "that overlap ai_any. 2026H2 = Jul-Oct 2026 calls only (8). Built by count_ai_mentions.py\n")
        out.to_csv(f, index=False)
    print(out.drop(columns=["source"]).to_string(index=False))
    print("calls with <500 words (extraction problems?):")
    print(bc[bc.words < 500][["firm", "call", "words", "local_path"]])


if __name__ == "__main__":
    main()
