"""Build m2_statements.csv: classified quantitative management statements relevant to M2 (phi * s_bar).

Sources
 - corpus rows: audit/price_calls_quotes.csv (ids reused; quote/url/page taken from there)
 - new corpus rows: quotes read by hand in this round from the local transcripts (data/sources/...)
 - extension rows (Q2FY27 calls, investor days, BPO firms, baselines): raw/*/agent_rows.csv, merged by
   merge_extension.py (separate script, run with python3 -I because it reads downloaded files).

Every quote is re-checked here against the local transcript text (whitespace/ligature/quote-mark
normalised, '...' = elision, fragments in order, within one page or across one page break).
confirmed = CONFIRMED if found, else NOT CONFIRMED.
Read-only with respect to project data. Run: python3 build_m2_statements.py
"""
import csv, os, re, sys

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
OUT = f"{ROOT}/data/explore/round4/price_statements"
sys.dont_write_bytecode = True  # do not leave __pycache__ in scripts/audit
sys.path.insert(0, f"{ROOT}/scripts/audit")
import calls_common as cc  # noqa: E402  (read-only helpers: page text, doc index)

LIG = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
                     "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                     "­": "", "…": "..."})


def nrm(s):
    return re.sub(r"\s+", " ", s.translate(LIG)).strip().lower()


def verify(firm, call, quote):
    P = cc.pages_of(firm, call)
    frags = [f.strip() for f in re.split(r"\.\.\.|…", quote) if f.strip()]
    for i, (pn, txt) in enumerate(P):
        win = nrm(txt + " " + (P[i + 1][1] if i + 1 < len(P) else ""))
        pos, first, ok = 0, None, True
        for f in frags:
            j = win.find(nrm(f).strip(" \"'"), pos)
            if j < 0:
                ok = False; break
            first = j if first is None else first
            pos = j + len(nrm(f).strip(" \"'"))
        if ok:
            own = len(nrm(txt))
            pg = pn if first < own else P[i + 1][0]
            return ("HTML exhibit (no pages)" if pg == "n/a" else f"PDF p.{pg}"), "CONFIRMED"
    return "", "NOT CONFIRMED"


# Classification fields
# type: price_same_scope | deal_value_same_scope | portfolio_deflation_rate | giveback_over_term |
#       baseline_pre_AI | delivery_productivity (s, not phi*s) | single_deal_commitment |
#       timing_or_bound | renewal_structure | price_increase (counter-evidence)
# scope: portfolio | renewals | new_deals | single_deal | single_client | service_line | industry
# horizon: one_off_level | per_year | over_contract_term | n/a
# tense: past | current | expectation
# net_of_baseline: Y (AI-incremental stated) | N (includes / is the pre-AI baseline) | unclear
# mag_lo/mag_hi: % (positive = price/deal value LOWER for same work, or productivity %)
F = ["stmt_id", "firm", "segment", "event", "date", "speaker", "speaker_role", "type", "scope", "horizon",
     "tense", "net_of_baseline", "mag_lo", "mag_hi", "mag_unit", "use_in_m2", "quote", "page", "url",
     "confirmed", "source", "note"]

# (id, segment, type, scope, horizon, tense, net, lo, hi, unit, use_in_m2, note)
FROM_PRICE_PASS = [
    ("HCLTech-26", "IT", "timing_or_bound", "industry", "n/a", "expectation", "unclear", "", "", "", "timing",
     "Jul 2023: GenAI deflation 'at least two to three years away'."),
    ("TCS-15", "IT", "timing_or_bound", "portfolio", "n/a", "past", "n/a", "", "", "'Pricing environment is stable' (Jan 2024)", "timing", ""),
    ("HCLTech-24", "IT", "baseline_pre_AI", "portfolio", "per_year", "past", "N", 1.3, 1.3, "% QoQ revenue fall in Q1 (bundles seasonality)", "baseline",
     "Annual productivity benefits kick in each Q1; -1.3% QoQ is an upper bound on the pre-AI annual give-back (Q1FY24)."),
    ("HCLTech-27", "IT", "baseline_pre_AI", "portfolio", "per_year", "expectation", "N", 2.0, 2.0, "% QoQ revenue fall in Q1 (incl. one offshoring)", "baseline",
     "'usual annual productivity pass back' (Apr 2024)."),
    ("TCS-18", "IT", "delivery_productivity", "service_line", "n/a", "current", "unclear", 5, 20, "% effort (POCs)", "s_only",
     "Delivery productivity, not a price."),
    ("TCS-19", "IT", "timing_or_bound", "renewals", "n/a", "current", "unclear", 5, 20, "% effort, certain phases only", "timing",
     "Rejects analyst's suggestion of 5-20% renewal cuts (Jul 2024)."),
    ("HCLTech-32", "BPO", "single_deal_commitment", "single_deal", "over_contract_term", "current", "unclear", 50, 50, "% client spend saving (DPO and testing)", "bpo_context",
     "Programs 'promising 50% savings from their current outsourced spend on DPO and testing'."),
    ("HCLTech-33", "IT", "delivery_productivity", "service_line", "n/a", "expectation", "unclear", 10, 30, "% effort (ADM, Copilot)", "s_only", ""),
    ("HCLTech-35", "BPO", "single_deal_commitment", "single_deal", "over_contract_term", "past", "unclear", "", "", "", "bpo_context",
     "One DPO renewal with productivity pass-back; 2/3 already achieved; no % given."),
    ("LTIMindtree-19", "IT", "giveback_over_term", "single_client", "one_off_level", "past", "unclear", 5.5, 5.5, "% QoQ fall in TMC vertical revenue", "timing",
     "First explicit AI give-back (Q3FY25, Oct-Dec 2024); top Hi-Tech client; revenue, not price."),
    ("LTIMindtree-20", "IT", "timing_or_bound", "single_client", "n/a", "past", "unclear", "", "", "", "timing",
     "Pass-back effective ~2 months of Q3FY25, extends into Q4FY25."),
    ("Infosys-23", "IT", "price_increase", "portfolio", "n/a", "past", "n/a", -3.6, -3.6, "% realization change (negative = price up), 9M FY25", "counter",
     "Realization up 3.6% over 9M FY25 (value-based selling)."),
    ("Infosys-30", "IT", "price_increase", "portfolio", "per_year", "past", "n/a", -3.5, -3.5, "% pricing benefit FY25 (negative = price up)", "counter", ""),
    ("TCS-23", "IT", "price_same_scope", "portfolio", "one_off_level", "expectation", "unclear", 5, 10, "% lower price for same work ('$100 -> $95 or $90')", "core",
     "Illustrative; 'AI for IT' work only; 'we will try to share'."),
    ("Infosys-27", "BPO", "price_same_scope", "service_line", "one_off_level", "current", "unclear", 20, 40, "% client benefit, large customer-service programs", "bpo_context",
     "Client benefit from automation+lean+AI+consolidation cumulatively; not all price, not all AI."),
    ("HCLTech-38", "IT", "delivery_productivity", "service_line", "n/a", "expectation", "unclear", 20, 25, "% (software development, at maturity)", "s_only",
     "Framed as 'level of deflation' when implemented and mature: a ceiling on phi*s for SDLC."),
    ("HCLTech-39", "BPO", "delivery_productivity", "service_line", "n/a", "expectation", "unclear", 20, 50, "% (digital process operations)", "s_only", "Ceiling for BPO."),
    ("HCLTech-44", "IT", "timing_or_bound", "renewals", "n/a", "past", "unclear", "", "", "8 of 9 renewals had higher total client revenue", "timing",
     "Q1FY26: wallet share more than offsets productivity given."),
    ("HCLTech-45", "IT", "delivery_productivity", "service_line", "n/a", "expectation", "unclear", 25, 30, "% (SDLC); BPO 40-50%", "s_only", "'it will definitely create deflation'."),
    ("HCLTech-47", "IT", "timing_or_bound", "renewals", "n/a", "past", "Y", "", "", "5 of top-10 renewals had SOW declines due to AI productivity", "timing",
     "Q2FY26 (Jul-Sep 2025): first count of AI-linked renewal SOW declines; no %."),
    ("HCLTech-49", "IT", "delivery_productivity", "service_line", "n/a", "expectation", "unclear", 10, 50, "% (BPO 40-50, SDLC 25-30, IT ops 10-15)", "s_only",
     "Impact on existing book 'with a lot of maturity'."),
    ("Cognizant-45", "IT", "timing_or_bound", "portfolio", "n/a", "past", "unclear", -5, -5, "% revenue per person TTM (negative = up)", "counter",
     "Revenue per person +5% TTM while 'sharing productivity' - realized price per worker not falling."),
    ("TechM-26", "IT", "giveback_over_term", "new_deals", "over_contract_term", "current", "unclear", 80, 80, "% productivity over 5 yrs (cited as unrealistic)", "outlier",
     "Competitor bids; TechM says unrealistic."),
    ("TechM-28", "IT", "baseline_pre_AI", "single_deal", "per_year", "past", "N", 0.8, 0.8, "% YoY BFSI revenue fall (furloughs + annual productivity)", "baseline",
     "Contractual annual productivity on one large infrastructure contract."),
    ("TechM-29", "IT", "baseline_pre_AI", "single_deal", "per_year", "past", "N", 4, 4, "% YoY ROW revenue fall (furlough + annual productivity)", "baseline", ""),
    ("TCS-31", "IT", "baseline_pre_AI", "renewals", "over_contract_term", "past", "N", 10, 15, "% productivity baked into renewals over contract term", "baseline",
     "Explicitly 'not related to AI'; 'business as usual'."),
    ("HCLTech-50", "IT", "deal_value_same_scope", "new_deals", "one_off_level", "past", "unclear", "", "", "TCV flat at $9.3B despite AI deflation", "timing", ""),
    ("HCLTech-51", "IT", "portfolio_deflation_rate", "industry", "per_year", "expectation", "Y", 3, 5, "% per year shrink (CAGR) of AI-disrupted 40% of industry", "core",
     "Spend shrink; HCL calls it deflation; incremental to traditional productivity (see NEW-HCL-Q4FY26-a)."),
    ("HCLTech-52", "IT", "portfolio_deflation_rate", "portfolio", "per_year", "expectation", "Y", 2, 3, "% per year, HCLTech portfolio", "core", "Primary per-year portfolio figure."),
    ("HCLTech-53", "IT", "portfolio_deflation_rate", "portfolio", "per_year", "expectation", "Y", 2, 3, "% per year, HCLTech portfolio", "core", "Reaffirmed; SDLC piece could be higher."),
    ("HCLTech-54", "IT", "portfolio_deflation_rate", "portfolio", "per_year", "expectation", "Y", 2, 3, "% per year", "core", "Built into FY27 guidance."),
    ("HCLTech-55", "IT", "deal_value_same_scope", "new_deals", "one_off_level", "current", "Y", 20, 20, "% lower TCV for same deal ($100M -> ~$80M)", "core",
     "'rough ballpark'; base year not stated."),
    ("TechM-34", "IT", "giveback_over_term", "new_deals", "over_contract_term", "current", "unclear", 20, 30, "% productivity offered (typical framing, criticised)", "context", ""),
    ("TechM-37", "IT", "delivery_productivity", "portfolio", "per_year", "past", "Y", 7, 7, "% AI-only productivity improvement in programs (FY26)", "s_only",
     "Measured s-type number; caps how much could have been passed on in FY26."),
    ("LTIMindtree-34", "IT", "timing_or_bound", "single_client", "n/a", "past", "unclear", 5, 5, "% fall, top-5 client bucket", "timing", "Says pure pass-back would mean a larger fall."),
    ("LTIMindtree-38", "IT", "timing_or_bound", "single_client", "n/a", "past", "unclear", "", "", "EBIT -100 bps (wage hike + productivity commitments)", "timing", ""),
    ("TCS-40", "IT", "giveback_over_term", "renewals", "over_contract_term", "past", "unclear", 10, 15, "% productivity passed on ('in most places')", "core",
     "Horizon is the project tenure (TCS-41, TCS-43); same size as TCS's own pre-AI renewal baseline (TCS-31)."),
    ("TCS-41", "IT", "giveback_over_term", "renewals", "over_contract_term", "current", "unclear", 10, 15, "% over project tenure", "core", "Usually compensated by additional work."),
    ("TCS-43", "IT", "giveback_over_term", "renewals", "over_contract_term", "current", "unclear", 10, 15, "% average, front-loaded", "core", ""),
    ("HCLTech-61", "IT", "baseline_pre_AI", "portfolio", "per_year", "past", "N", 1.1, 1.1, "pp margin headwind (annual productivity benefits + ERS)", "baseline", "Q1FY27."),
    ("TechM-43", "IT", "giveback_over_term", "new_deals", "over_contract_term", "current", "unclear", 70, 80, "% productivity over 5-yr deal (competitors' bids)", "outlier",
     "TechM says not credible; marks the aggressive tail."),
    ("LTIMindtree-45", "IT", "deal_value_same_scope", "new_deals", "one_off_level", "past", "unclear", "", "", "order book flat at $1.7B with 'natural deflation adjustment'", "timing", ""),
    ("LTIMindtree-46", "IT", "price_same_scope", "new_deals", "one_off_level", "past", "Y", 15, 15, "% lower price for same scope vs a year earlier", "core",
     "'let us say'; applies to 'certain category of services' (NEW-LTIM-Q1FY27-a)."),
    ("Cognizant-50", "IT", "single_deal_commitment", "single_deal", "over_contract_term", "current", "unclear", 50, 50, "% productivity over 5 years (one deal)", "outlier",
     "Prepared-remarks showcase deal; ~13%/yr compounded."),
    ("Cognizant-53", "IT", "renewal_structure", "portfolio", "n/a", "current", "n/a", "", "", "T&M ~50% reprices every 6-15 months (max 2-2.5 yrs)", "conversion", ""),
    ("Accenture-14", "IT", "baseline_pre_AI", "service_line", "per_year", "current", "N", 10, 10, "% productivity per year in managed services", "baseline",
     "GenAI framed as continuing a pre-existing >=10%/yr managed-services productivity model."),
    ("Accenture-17", "IT", "single_deal_commitment", "single_deal", "over_contract_term", "current", "unclear", 50, 50, "% cost reduction (one managed-services deal)", "outlier", ""),
    ("HCLTech-02", "IT", "renewal_structure", "renewals", "per_year", "past", "n/a", 2, 3, "% of revenue lost at renewal (pre-AI, 2021)", "baseline", ""),
    ("HCLTech-04", "IT", "renewal_structure", "renewals", "n/a", "past", "n/a", "", "", "renewal rates 97-98% (2021)", "conversion", ""),
]

# New rows read by hand this round from local transcripts (quote text as printed by pdftotext / HTML).
NEW = [
    dict(stmt_id="NEW-HCL-Q4FY26-a", firm="HCLTech", call="Q4FY26", speaker="C. Vijayakumar, CEO & MD", role="management",
         quote="No, I think we were always careful that this is the incremental impact. I mean, considering the traditional productivity what we normally commit",
         cls=("IT", "baseline_pre_AI", "portfolio", "per_year", "current", "Y", "", "", "states 2-3% / 3-5% figures are incremental to traditional productivity", "core"),
         note="Answer to analyst who said pre-AI renewals already cut 10-15% over deal life (~3-5%/yr)."),
    dict(stmt_id="NEW-HCL-Q4FY26-b", firm="HCLTech", call="Q4FY26", speaker="C. Vijayakumar, CEO & MD", role="management",
         quote="No, I would say that very little has really played out in already reported numbers.",
         cls=("IT", "timing_or_bound", "portfolio", "n/a", "past", "Y", "", "", "AI deflation in reported numbers to FY26: 'very little'", "core"),
         note="Next sentence: expects it to happen in FY27 onwards. Key timing evidence for FY24-26."),
    dict(stmt_id="ANL-HCL-Q4FY26", firm="HCLTech", call="Q4FY26", speaker="Rushabh Jain (analyst)", role="analyst",
         quote="In renewal deals, we were seeing 10% to 15% cut in pricing over the life of the deal, which would translate to more or less 3% to 5%.",
         cls=("IT", "baseline_pre_AI", "renewals", "over_contract_term", "past", "N", 10, 15, "% price cut over deal life, pre-AI (~3-5%/yr)", "baseline"),
         note="ANALYST statement, not management; CEO does not dispute the baseline, only says AI figure is incremental."),
    dict(stmt_id="ANL-TCS-Q1FY27", firm="TCS", call="Q1FY27", speaker="Abhishek Shindadkar (analyst)", role="analyst",
         quote="Typically, the understanding was the productivity could be 3% to 5% annually.",
         cls=("IT", "baseline_pre_AI", "renewals", "per_year", "past", "N", 3, 5, "% per year productivity commitment (pre-AI understanding)", "baseline"),
         note="ANALYST statement; CEO answer does not confirm or reject the 3-5% figure."),
    dict(stmt_id="NEW-TCS-Q1FY27-a", firm="TCS", call="Q1FY27", speaker="K Krithivasan, CEO & MD", role="management",
         quote="But we also see in many places, whenever we go to our customers with such opportunities, customers give us additional work and the top line is not significantly impacted.",
         cls=("IT", "timing_or_bound", "renewals", "n/a", "past", "unclear", "", "", "volume offset to give-backs", "context"),
         note="Volume response (epsilon / d) to the price cut; does not change phi*s."),
    dict(stmt_id="NEW-TCS-Q3FY26-a", firm="TCS", call="Q3FY26", speaker="K Krithivasan, CEO & MD", role="management",
         quote="So by and large, the total value of the contract doesn't change or reduce much",
         cls=("IT", "timing_or_bound", "renewals", "n/a", "past", "unclear", "", "", "contract value roughly unchanged at renewal; scope rises", "context"),
         note="Price per unit falls, volume rises; consistent with phi*s>0 and epsilon>0."),
    dict(stmt_id="NEW-LTIM-Q1FY27-a", firm="LTIMindtree", call="Q1FY27", speaker="Venu Lambu, CEO & MD", role="management",
         quote="for certain category of services, the price at which we get paid not the unit level, but at the order book level, is definitely lesser than what it was in FY2026",
         cls=("IT", "price_same_scope", "new_deals", "one_off_level", "past", "Y", "", "", "scope qualifier for LTIMindtree-46", "core"),
         note="Restricts the ~15% to 'certain category of services'."),
    dict(stmt_id="NEW-CTSH-Q2CY26-a", firm="Cognizant", call="Q2CY2026", speaker="Jatin Dalal, CFO", role="management",
         quote="On the remaining 50%, which is fixed price book of business, typically, the contract lines are between 24 and 36 months on an average.",
         cls=("IT", "renewal_structure", "portfolio", "n/a", "current", "n/a", "", "", "FP ~50% of revenue, 24-36 month terms", "conversion"),
         note="With Cognizant-53: whole book reprices within ~1-3 years."),
    dict(stmt_id="NEW-CTSH-Q2CY26-b", firm="Cognizant", call="Q2CY2026", speaker="Jatin Dalal, CFO", role="management",
         quote="If we believe that we have started this journey of embedding AI into our solution more actively from beginning of last year, which is 2025, we are roughly halfway into it, and we have probably another half to go.",
         cls=("IT", "renewal_structure", "portfolio", "n/a", "current", "n/a", 50, 50, "% of fixed-price book re-priced with AI by mid-2026", "conversion"),
         note="Timing: AI embedding in pricing from Jan 2025."),
    dict(stmt_id="NEW-ACN-Q1FY26-a", firm="Accenture", call="Q1FY26", speaker="Julie Sweet, Chair & CEO", role="management",
         quote="this has been a business model for the industry, really all the way going back to the introduction of technology in RPA, right, where we're signing contracts that depend on our use of more technology over time to provide productivity.",
         cls=("IT", "baseline_pre_AI", "portfolio", "per_year", "current", "N", "", "", "productivity-commitment contracts pre-date GenAI", "baseline"),
         note="Answer on how AI savings are passed to clients."),
    dict(stmt_id="NEW-INFY-Q4FY26-a", firm="Infosys", call="Q4FY26", speaker="Salil Parekh, CEO & MD", role="management",
         quote="And that is the balance that we are seeing in the past year with 3.1% and if you adjust for the one-timers from the prior year, we had a growth rate which was more than the compression we were seeing.",
         cls=("IT", "timing_or_bound", "portfolio", "per_year", "past", "unclear", 0, 3.1, "% FY26 compression < FY26 growth (upper bound)", "core"),
         note="Weak upper bound on Infosys FY26 compression; 'compression' not split into price vs volume."),
    dict(stmt_id="NEW-INFY-Q4FY26-b", firm="Infosys", call="Q4FY26", speaker="Salil Parekh, CEO & MD", role="management",
         quote="Now the compression is definitely there, I do not know if I have a sense that it is more than last year.",
         cls=("IT", "timing_or_bound", "portfolio", "n/a", "past", "unclear", "", "", "FY27 compression not seen as larger than FY26", "context"), note=""),
    dict(stmt_id="NEW-INFY-Q4FY26-c", firm="Infosys", call="Q4FY26", speaker="Jayesh Sanghrajka, CFO", role="management",
         quote="Overall at this point in time, the volumes for the last year has remained flattish.",
         cls=("IT", "timing_or_bound", "portfolio", "n/a", "past", "unclear", "", "", "FY26 volumes flat while revenue +3.1% cc", "context"),
         note="Revenue per unit of effort rose in FY26: realized price per effort did not fall at Infosys."),
]


def main():
    pq = {r["id"]: r for r in csv.DictReader(open(f"{ROOT}/audit/price_calls_quotes.csv"))}
    tx = {(r["firm"], r["call"]): r for r in csv.DictReader(open(f"{ROOT}/audit/calls_transcripts.csv"))}
    rows = []
    for (sid, seg, typ, scope, hor, tense, net, lo, hi, unit, use, note) in FROM_PRICE_PASS:
        r = pq[sid]
        page, conf = verify(r["firm"], r["call"], r["quote"])
        rows.append(dict(stmt_id=sid, firm=r["firm"], segment=seg, event=f"{r['call']} earnings call", date=r["call_date"],
                         speaker=r["speaker"], speaker_role="management", type=typ, scope=scope, horizon=hor, tense=tense,
                         net_of_baseline=net, mag_lo=lo, mag_hi=hi, mag_unit=unit, use_in_m2=use, quote=r["quote"],
                         page=page or r["page"], url=r["source_url"], confirmed=conf,
                         source="audit/price_calls_quotes.csv", note=note))
    for n in NEW:
        t = tx[(n["firm"], n["call"])]
        page, conf = verify(n["firm"], n["call"], n["quote"])
        seg, typ, scope, hor, tense, net, lo, hi, unit, use = n["cls"]
        rows.append(dict(stmt_id=n["stmt_id"], firm=n["firm"], segment=seg, event=f"{n['call']} earnings call", date=t["call_date"],
                         speaker=n["speaker"], speaker_role=n["role"], type=typ, scope=scope, horizon=hor, tense=tense,
                         net_of_baseline=net, mag_lo=lo, mag_hi=hi, mag_unit=unit, use_in_m2=use, quote=n["quote"],
                         page=page, url=t["source_url"], confirmed=conf, source="local transcript, read this round", note=n["note"]))
    rows.sort(key=lambda r: (r["date"], r["firm"]))
    with open(f"{OUT}/m2_statements_corpus.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=F); w.writeheader(); w.writerows(rows)
    bad = [r["stmt_id"] for r in rows if r["confirmed"] != "CONFIRMED"]
    print(len(rows), "rows;", len(rows) - len(bad), "CONFIRMED; not confirmed:", bad)


if __name__ == "__main__":
    main()
