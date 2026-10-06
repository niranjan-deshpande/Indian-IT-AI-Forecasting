"""STEP 2: demand re-scan of the 183 transcripts.

  python calls_demand_extract.py screen  <scratch_dir>   # keyword screen -> <scratch>/hits_<firm>_<part>.txt
  python calls_demand_extract.py compile <scratch_dir>   # <scratch>/cand/*.csv -> audit/demand_calls_quotes.csv

Procedure (same as the price pass): dictionary screen (audit/calls_demand_dictionary.json), +/-900-char
windows merged, each window read in context by a reader who confirms the speaker from the transcript's
speaker labels and keeps only MANAGEMENT statements explaining revenue / headcount / growth / hiring / deals
through demand (weak or strong). Candidate rows (firm, call, speaker_name, speaker_title, topic, quote,
context_note) are then machine-checked here: quote must be a whitespace-normalised verbatim substring of
the call's text ('...' = elision, fragments in order, within one page or across one page break),
<= 60 words, and its page is re-derived. Near-duplicates within a call (>= 60% token overlap) are
dropped, keeping the earlier/longer-context row. Rows failing the check are reported and excluded.
"""
import sys, os, re, csv, json, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
from calls_common import ROOT, FIRMS, build_docs, pages_of, locate, page_label, norm

DIC = json.load(open(f"{ROOT}/audit/calls_demand_dictionary.json"))
TERMS = [(fam, t) for fam, L in DIC["families"].items() for t in L]
KW = re.compile(r"\b(?:" + "|".join(f"(?:{t})" for _, t in TERMS) + r")\b", re.I)
W = 900
SPK = re.compile(r"^\s*([A-Z][A-Za-z\.\'’\- ]{2,45}?)\s*:\s*$|^\s*([A-Z][A-Za-z\.\'’\- ]{2,45}?):\s+\S")
TOPICS = {"demand_weak", "demand_strong", "macro", "vertical", "deal_delay", "other"}


def screen(scr):
    docs = build_docs()
    stats = collections.Counter(); cover = collections.Counter(); tot = collections.Counter()
    out = collections.defaultdict(list)
    for d in docs:
        P = pages_of(d['firm'], d['call'])
        t = "".join(f"\n=== PAGE {pn} ===\n{x}" for pn, x in P)
        pages = [(m.start(), m.group(1)) for m in re.finditer(r"=== PAGE (\S+) ===", t)]

        def pg(i):
            p = "?"
            for s, n in pages:
                if s <= i: p = n
                else: break
            return p
        spans = []
        for m in KW.finditer(t):
            a, b = max(0, m.start() - W), min(len(t), m.end() + W)
            if spans and a <= spans[-1][1]:
                spans[-1][1] = b; spans[-1][2].append(m.group(0))
            else:
                spans.append([a, b, [m.group(0)]])
            stats[d['firm']] += 1
        cover[d['firm']] += sum(b - a for a, b, _ in spans); tot[d['firm']] += len(t)
        part = "A" if d['call_date'] < "2023-07-01" else "B"
        for a, b, k in spans:
            pre = t[max(0, a - 6000):a].split("\n"); spk = ""
            for line in reversed(pre):
                mm = SPK.match(line)
                if mm: spk = (mm.group(1) or mm.group(2)).strip(); break
            out[(d['firm'], part)].append(
                f"\n##### {d['firm']} | {d['call']} | {d['call_date']} | pages {pg(a)}-{pg(b)} | prev_speaker_guess: {spk} | kw: "
                f"{', '.join(sorted(set(x.lower() for x in k)))[:300]}\n" + re.sub(r"\n{2,}", "\n", t[a:b]) + "\n")
    os.makedirs(scr, exist_ok=True)
    for (F, part), L in out.items():
        open(f"{scr}/hits_{F}_{part}.txt", "w").write("".join(L))
    for F in FIRMS:
        print(f"{F:12s} hits={stats[F]:5d}  text covered by windows={cover[F] / tot[F]:.0%}")


def toks(s):
    return set(re.findall(r"[a-z0-9']+", s.lower()))


def compile_(scr):
    idx = {(d['firm'], d['call']): d for d in build_docs()}
    rows, bad = [], []
    for f in sorted(glob.glob(f"{scr}/cand/*.csv")):
        for r in csv.DictReader(open(f)):
            r = {k: (v or "").strip() for k, v in r.items() if k}
            key = (r['firm'], r['call'])
            if key not in idx:
                bad.append((f, "BAD CALL", r)); continue
            q = re.sub(r"\s+", " ", r['quote']).strip().strip('"“”')
            pg, ep, st = locate(*key, q)
            nw = len(q.replace("...", " ").split())
            if st != "exact":
                bad.append((f, "NOT FOUND", r)); continue
            if nw > 60:
                bad.append((f, f"TOO LONG {nw}", r)); continue
            if r['topic'] not in TOPICS:
                r['topic'] = "other"
            r['quote'] = q; r['_page'] = page_label(pg, ep); r['_pos'] = (int(pg) if pg not in (None, "n/a") else 0)
            rows.append(r)
    # within-call near-duplicate removal
    keep = []
    for key in sorted({(r['firm'], r['call']) for r in rows}):
        L = [r for r in rows if (r['firm'], r['call']) == key]
        K = []
        for r in L:
            tr = toks(r['quote'])
            dup = next((k for k in K if len(tr & toks(k['quote'])) / max(1, min(len(tr), len(toks(k['quote'])))) >= 0.6), None)
            if dup is None:
                K.append(r)
            else:
                print("NEAR-DUP dropped:", key, "|", r['quote'][:90])
        keep += K
    keep.sort(key=lambda r: (FIRMS.index(r['firm']), idx[(r['firm'], r['call'])]['call_date'], r['_pos']))
    out, n = [], collections.Counter()
    for r in keep:
        d = idx[(r['firm'], r['call'])]; n[r['firm']] += 1
        out.append(dict(
            id=f"DEM-{r['firm']}-{n[r['firm']]:03d}", firm=r['firm'], call=r['call'], call_date=d['call_date'],
            speaker=f"{r['speaker_name']}, {r['speaker_title']}", topic=r['topic'], quote=r['quote'],
            quantitative="", quantitative_detail="", source_url=d['source_url'], source_doc=d['local_path'],
            page=r['_page'], label="commentary", label_note="", context_note=r.get('context_note', ''),
            in_timeline="N", source_type="company IR / SEC filing (no aggregator used)"))
    cols = list(csv.DictReader(open(f"{ROOT}/audit/price_calls_quotes.csv")).fieldnames)
    with open(f"{ROOT}/audit/demand_calls_quotes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    for f_, why, r in bad:
        print("REJECT", why, os.path.basename(f_), r.get('call'), "|", r.get('quote', '')[:120])
    print("candidates ok:", len(rows), "rejected:", len(bad), "kept after dedup:", len(out))
    print(dict(n))


if __name__ == "__main__":
    {"screen": screen, "compile": compile_}[sys.argv[1]](sys.argv[2])
