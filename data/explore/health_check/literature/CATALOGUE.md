# Citation catalogue for the IT-services health check

*Compiled 2026-10-15. Machine-readable version: `CATALOGUE.csv` (one row per citable claim). Sources: the four literature-search reports in this folder, re-verified by opening each source, plus gap searches, plus the repo's own checks in `contradictions/`, `labour_share/`, `fresher_thirdparty/`, `postings/` and `epfo/`.*

**How to read the labels.**
- **Verified:** *primary* = we opened the original document and saw the number; *press* = we opened a press or secondary article that states it, but not the original; *unverified (press-only)* = only search snippets or blocked pages; *not found* = the claim could not be located.
- **Reproducible:** *yes* = we can rebuild it from free data we hold (filings, RBI, PLFS, EPFO, WTO, NAS); *partly* = some ingredients are free; *no* = needs survey microdata, proprietary postings or payroll, or a broker model. Every *no* that we cite must be flagged as such in the final report.
- **Stance** is relative to our four claims: C1 output growing; C2 big firms stopped adding jobs; C3 sector job growth slow; C4 entry rung narrowing.
- Notes marked **CORRECTED** or **REPRODUCED** come from the repo's own checks; they override the press reading.

**Counts.** 222 claim rows from about 109 distinct sources. Rows: 154 primary, 55 press, 7 unverified (press-only), 6 not found. Three of the not-found rows are gap-search notes, not sources.

## The citations that matter most

1. **ICRIER (Feb 2026), *AI and Jobs: This Time Is No Different*.** 651-firm survey: 55% of firms report lower entry-level employment vs 35% higher; 42% report more mid-level. Not reproducible (survey). OpenAI-funded. Its 'employment still growing' line is PLFS to 2023-24 only and matches our tabulation. <https://www.icrier.org/pdf/AI-and-Jobs.pdf>
2. **World Bank, India Development Update (Oct 2026), p.41.** Top six firms cut ~64,000 from 1.7m (we reproduce −63,557); the rest of the sector 'added ~700,000' (Goldman; overstated by a Nasscom restatement, like-for-like ~+0.39m). The only citable source for the Goldman numbers.
3. **World Bank, South Asia Development Update (Oct 2025), *Jobs, AI, and Trade*.** Lightcast postings: business-services postings −35% and posted wages −8% relative to other occupations after ChatGPT; 0–5-year-experience postings fall most. Not reproducible (Lightcast).
4. **RBI, Survey on Computer Software and ITES Exports 2025-26 (Sep 2026).** $221.4bn (+8.2%); computer services $153.4bn, 69.3%. Reproducible; our C1 anchor. <https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625>
5. **Brynjolfsson, Chandar & Chen (revised Aug 2026), *Canaries in the Coal Mine?*** US workers aged 22–25 in AI-exposed jobs 19% below the less-exposed path, through hiring not separations; halves when occupational college share is controlled. Not reproducible (ADP).

Close behind: Nasscom Strategic Review 2026 (revenue +6.1% vs jobs +2.3%); Economic Survey 2025-26 Box VII.2 (AI-exposed exports +39.5%, relative DiD); the Future of India Substack (closest replica of our PLFS work; shares reproduce, levels and the labour-share chart do not); Baldwin and ING on exports (reproduced, with caveats).

## Output and exports

**Nasscom (2026)** — Nasscom (2026). Technology Sector in India: Strategic Review 2026 - 'Steering through the tides of uncertainty: charting opportunities amid disruption'. New Delhi: Nasscom (released Feb 24, 2026; full report paid). <https://nasscom.in/knowledge-center/publications/technology-sector-india-strategic-review-2026>

- `IND-01a` Nasscom estimates India's tech sector revenue (incl. hardware) will cross USD 315bn in FY26, up 6.1% y/y. *[315 USD bn, FY26E]* — agrees; reproducible: no; verified: primary.
  - C1. Nasscom report page states 'cross the $315 bn mark'; the 6.1% growth figure is from PTI coverage (etvbharat), not on the public page. Estimate made in Feb, before year end. Suggested: S1 output box, alongside RBI exports.
- `IND-01b` Nasscom puts FY26 tech exports at about USD 246bn (+5.6%) and domestic revenue growth at 7.9%. *[246 USD bn, FY26E]* — agrees; reproducible: partly; verified: press.
  - C1. PTI via ETV Bharat; not on Nasscom public summary page. Compare with RBI software-services exports (different definition: BoP vs industry revenue). S1 output box / methods footnote on definitions.
- `IND-01d` Nasscom revised FY25 revenue up to USD 297bn (from USD 282.6bn) and puts FY25 net hiring at about 133,000 (vs 126,000 in the FY25 edition). *[297 USD bn, FY25 (revised)]* — complements; reproducible: no; verified: press.
  - Methods caveat: Nasscom's series is revised/rebased between editions (revenue +USD 14bn; FY25 adds 126k -> 133k; employee base FY24 5.43m + 126k does not equal FY25 5.80m). Do not chain Nasscom levels across editions. Methods footnote.

**Nasscom (2025)** — Nasscom (2025). Technology Sector in India: Strategic Review 2025 - 'Beyond Disruption: Staying Future-Ready Today'. Nasscom (Feb 2025); summary on Nasscom Community. <https://community.nasscom.in/communities/nasscom-insights/technology-sector-india-strategic-review-2025>

- `IND-01j` FY25 edition: industry revenue est. USD 283bn (+5.1%), exports USD 224bn (+4.6%), domestic USD 58.2bn (+7.0%). *[283 USD bn, FY25E]* — agrees; reproducible: no; verified: primary.
  - C1 series point. Later revised to USD 297bn in the 2026 edition. Use for series chart with revision caveat.

**Kotak Institutional Equities (2026a)** — Kotak Institutional Equities (2026). Indian IT services sector note (post Q4FY26 results). Reported by ANI, Apr 29, 2026 (The Tribune; webindia123). <https://www.tribuneindia.com/news/business/it-services-growth-to-stay-range-bound-at-3-per-cent-as-ai-deflation-pressures-margins-mid-tiers-better-placed-says-kotak/>

- `IND-03a` Kotak sees Indian IT services growth range-bound at about 3% with no meaningful FY27 recovery; global IT services averaged 5% cc over 10 years and slowed to 3% in CY2025. *[3 % y/y revenue growth, FY27E / CY25]* — agrees; reproducible: no; verified: press.
  - C1 (output growing slowly). Article body says only 'a brokerage report'; Kotak named only in headline. Broker model. S1 output box.

**J.P. Morgan (2026)** — J.P. Morgan (2026). Indian IT services sector note (late June 2026). Reported in Nahar, P.K., 'TCS, Infosys, Wipro, HCL Tech: Top-5 IT stocks' m-cap slips to RIL as AI disruption bites', Business Today, Jul 4, 2026; and People Matters, Jun 30, 2026. <https://www.businesstoday.in/markets/stocks/story/indian-it-stocks-fall-tcs-infosys-wipro-hcl-tech-reliance-market-cap-ai-impact-540988-2026-07-04>

- `IND-04a` J.P. Morgan says the sector has been stuck at 2-3% revenue growth over the past three years. *[2-3 % y/y revenue growth, FY24-FY26]* — agrees; reproducible: partly; verified: press.
  - C1 (growing slowly). The phrase is in Business Today (Jul 4) and wire copies (~Jun 28), NOT in the People Matters article the literature report cited. Reproducible approx. from filings. S1 output box.

**Future of India Foundation (2026)** — Future of India Foundation [unsigned; same text posted by Ruchi Gupta on her Substack 6 Oct 2026] (2026), 'IT Sector Helped Build the Indian Middle Class. For Its Workers, It Is Starting to Sputter', India After Liberalisation series Part 5, YouthPOWER / Future of India Substack, Oct 2. <https://foifaction.substack.com/p/it-sector-helped-build-the-indian>

- `JRN-01h` RBI software-services exports roughly doubled from about $108bn in 2017-18 to about $221bn in 2025-26, and rose 16% from 2023-24 to 2025-26. *[108 -> 221 USD bn, 2017-18 to 2025-26]* — agrees; reproducible: yes; verified: primary.
  - C1. RBI survey basis, excluding overseas commercial presence. The FY26 $221.4bn matches RBI's 18 Sep 2026 release (see JRN-03a). The 2017-18 $108bn was not checked against RBI. The +16% is consistent with $190.7bn -> $221.4bn.

**Sidhant (2026)** — Aman Kai Sidhant (2026), 'India's $300B AI Shock', india300.ai, Jun 18. <https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=61562>

- `JRN-02b` In the RBI survey, BPO exports of medical transcription and document management fell from $0.8bn to $0.1bn, HR administration and content development fell from $0.4bn to $0.3bn each, and 'other BPO' rose by about $5bn. *[0.8 -> 0.1 USD bn, 2023-24 to 2024-25]* — complements; reproducible: yes; verified: primary.
  - C1, prices/AI-exposed tasks. I checked these against RBI's 2024-25 survey release (4 Nov 2025): other BPO went from 37.1 to 42.3. DISCREPANCY: the essay dates the change FY2022-23 to FY2024-25, but RBI shows the whole drop in one year (2023-24 to 2024-25), which could be a reclassification. The essay also gives both …

**Weijin Research (2026)** — Weijin Research (2026), 'AI goes long on India, shorts Indian software outsourcing', Weijin Research Substack, Sep 23 (translated from Huxiu, Sep 20); figure from RBI, 'Survey on Computer Software and ITES Exports: 2025-26', press release, Sep 18 2026. <https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63625>

- `JRN-03a` India's software services exports rose 8.2% to $221.4bn in 2025-26 (excluding sales through overseas commercial presence), or $239.3bn including it. IT services were $147.0bn, BPO $56.0bn, engineering $12.0bn and software products $6.4bn. *[221.4 USD bn, FY26 (2025-26)]* — agrees; reproducible: yes; verified: primary.
  - Same RBI figure as TT-09b (primary there). C1. CONFIRMED: this is the RBI annual SURVEY of computer software and ITES exports, NOT BoP. 2,363 of 7,569 firms responded, covering about 89% of exports; 2024-25 was $204.7bn. BPO was nearly flat (55.8 -> 56.0) while IT services grew 12%. Cite RBI directly, not Weijin.

**Malik & Jain (2026)** — Malik, P. & Jain, N. (2026). Interactions of Artificial Intelligence with India's Labour Market: Devising an AI-for-Labour Model Using the Productivity, Inclusivity, and Entrepreneurship Framework. ICRIER Policy Brief 10, ICRIER Prosus Centre for Internet and Digital Economy (February). <https://icrier.org/pdf/Interactions-of-Artificial-Intelligence-with-India-s-Labour-Market.pdf>

- `TT-02a` Within knowledge-intensive services (group G3), computer and information services' GVA share nearly doubled from 6% to 12% over the past decade; AI exposure and productivity potential are highest in this group. *[12 % of GVA (base ambiguous), c.2013-2023]* — complements; reproducible: partly; verified: primary.
  - p.7; cites Economic Survey 2025-26. Base of the share (G3 or services GVA) is not stated in the text. Policy brief using KLEMS + PLFS 2022-23. No IT employment or entry-level numbers. Low relevance; context only. Funded by ICRIER Prosus Centre.

**Economic Survey 2025-26, Ch. 7** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 7: Services: From Stability to New Frontiers (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf>

- `TT-03a` Box VII.2: two-way fixed-effects DiD on quarterly RBI BoP data finds AI-exposed services exports (software, business, financial) rose about 39.5% relative to less-exposed services after Q2 FY23 (coef 0.333, 1%). *[39.5 % relative increase in exports, Q1 FY18-Q2 FY26; post = from Q2 FY23]* — agrees; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Approximately replicated (pooled coef 0.361 vs their 0.333; 0.392 extending to 2026Q2). Caveats for citing: the 'intervention' is Q2 FY23 (Jul-Sep 2022), before ChatGPT; it is a relative difference-in-differences against travel/transport/insurance etc., not …
- `TT-03b` Category effects: software services +44% (coef 0.37) and business services +67% (0.51), both significant at 1%; financial services positive but insignificant. *[44 % relative increase (software), Q1 FY18-Q2 FY26]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): Our replication: software 0.329, business 0.498, financial 0.257. || Original verification note: Box VII.2, Table B, p.271. C1. Note the control group's own post-COVID travel/transport dynamics drive part of a DiD like this; footnote.

**RBI (2025)** — Reserve Bank of India (2025). Survey on Computer Software and Information Technology Enabled Services Exports: 2024-25. Press release (November 4). <https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61562>

- `TT-09a` Software services exports (excl. commercial presence) rose 7.3% to US$204.7bn in 2024-25; computer services US$138.1bn (67.4%), ITES US$66.6bn (32.6%, BPO 55.8bn). *[204.7 USD bn, 2024-25]* — agrees; reproducible: yes; verified: primary.
  - RBI press release (HTML) opened. US share fell to 52.9% (US +4.9%, Europe +14.3%). Incl. Mode 3: US$218.6bn. C1.

**RBI (2026a)** — Reserve Bank of India (2026). Survey on Computer Software and Information Technology Enabled Services Exports: 2025-26. Press release (September 18). <https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625>

- `TT-09b` Software services exports (excl. commercial presence) rose 8.2% to US$221.4bn in 2025-26; incl. overseas commercial presence US$239.3bn (+9.5%). *[221.4 USD bn, 2025-26]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): RBI survey: $221bn FY26, +19% since FY23 (~6%/yr). BoP software exports grow about twice as fast; level gap vs survey narrowed from -$34-39bn (FY19-23) to -$18bn (FY26). Use the survey for C1 and footnote the BoP. || Original verification note: RBI press …
- `TT-09c` Computer services exports US$153.4bn in 2025-26 (69.3% share, up from 67.4%), ~11% growth; ITES/BPO US$68.0bn (30.7%), ~2% growth. *[153.4 USD bn, 2025-26]* — agrees; reproducible: yes; verified: primary.
  - Growth rates computed from the two releases (138.1 to 153.4; 66.6 to 68.0). Computer services accelerating while BPO stalls. C1; useful for split chart.
- `TT-09d` US share of software exports rose back to 54.1% (US$119.7bn) in 2025-26; Europe 31.8%, UK 15.4%; off-site delivery 91.7%. *[54.1 % of software exports, 2025-26]* — agrees; reproducible: yes; verified: primary.
  - From the RBI release as summarized by fetch tool; US growth ~10.5% computed. C1.

**RBI (2026b)** — Reserve Bank of India (2026). Developments in India's Balance of Payments during the First Quarter (April-June) of 2026-27. Press release (September 1). <https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63493>

- `TT-09e` BoP Q1 2026-27: services exports (credit) US$106.2bn vs 97.4bn a year earlier (+9%); net services US$51.6bn; RBI says computer services exports rose y-o-y. *[106.2 USD bn, Q1 2026-27 (Apr-Jun 2026)]* — agrees; reproducible: yes; verified: primary.
  - RBI BoP press release Sep 1, 2026. Release does not give computer-services amounts; need RBI's quarterly invisibles table. C1 latest quarter.

**RBI Annual Report 2025-26** — Reserve Bank of India (2026). Annual Report 2025-26 (May), as reported by ANI/The Tribune (May 31, 2026). <https://www.tribuneindia.com/news/business/indias-service-trade-remittances-to-support-current-account-balance-in-fy27-rbi-annual-report/>

- `TT-09f` RBI Annual Report 2025-26: net services exports grew 15.3% y-o-y in Apr-Dec 2025, driven by software and business services (77.8% of services exports); robust IT spending (Gartner) bodes well for software exports. *[15.3 % y-o-y growth, net services, Apr-Dec 2025]* — agrees; reproducible: yes; verified: press.
  - Seen in ANI/Tribune coverage only; annual report text not opened. No GCC or AI-jobs content reported. C1.

**World Bank (2025)** — World Bank. 2025. South Asia Development Update, October 2025: Jobs, AI, and Trade. Ch. 2 'Artificial Intelligence, Real Impact' by P. Kirby, J. Rexer, S. Sharma. Washington, DC (Oct 7). <https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf>

- `WB-01e` India's technology-services exports kept growing rapidly after ChatGPT even as hiring slowed (indexed exports vs total exports, Q3 2022=100), read as early evidence of productivity gains in the sector. *[index (Q3 2022=100), 2020Q2-2025Q2]* — agrees; reproducible: yes; verified: primary.
  - C1 + C2/C3 divergence. Fig. 2.11D p.39 (RBI data); text p.38 and p.30 ('notwithstanding a recent export surge'). The text gives no exact index value (axis runs to ~140). Reproducible from RBI BoP. Note: report says 'tech services', while the literature report said 'BPO exports'.

**World Bank (2026a, SAEU Apr)** — World Bank. 2026. South Asia Economic Update, April 2026: Working with Industrial Policy. Washington, DC (Apr 8). <https://documents.worldbank.org/curated/en/099919404082611180/pdf/IDU-2569cd85-1e68-48e3-8e5c-ddc710893e1f.pdf>

- `WB-02b` Fig. 1.10D shows India's BPO/technology-services exports rising well above total exports since Q3 2022 (index to 2025Q3); South Asia's real services exports grew about 15% a year on average since the pandemic. *[15 % per year (real services exports, South Asia), post-pandemic to 2025]* — agrees; reproducible: yes; verified: primary.
  - C1. p.28 (PDF p.50); Fig. 1.10D p.27. No exact India index value in the text. Services were 44% of South Asia's exports vs 27% globally (2024).

**World Bank (2026, SAEU Oct)** — World Bank. 2026. South Asia Economic Update, October 2026: Adopting AI for Growth. Washington, DC (Oct 6). GVC analysis draws on Chiplunkar et al. (2026). <https://documents.worldbank.org/curated/en/099552210132636511/pdf/IDU-c65c3333-7e66-4072-9ce4-05ce12d2f398.pdf>

- `WB-02e` But firm-to-firm GVC data show US-South Asia links grew FASTEST where both sides are AI-exposed: a 1 s.d. rise in a US firm's AI exposure is linked to a 27.5% larger rise in customer/partner links with South Asian firms (63.1% when the South Asian counterparty is highly exposed, vs 7.4% otherwise); report concludes reshoring is not GenAI's dominant effect. *[27.5 % larger post-GPT increase in links per 1 s.d. AI exposure, 2020-2025Q4 (FactSet GVC links)]* — complements; reproducible: no; verified: primary.
  - C1 (demand side). pp.56-59 (PDF pp.76-79), Figs. 2.8-2.9; Chiplunkar et al. (2026). South Asian side: +30% supplier links per 1 s.d. own exposure. DISCREPANCY: the literature report says the report 'flags reshoring'. In fact it tests reshoring and finds a scale effect dominates. It supports 'output up' and does not …
- `WB-02g` India's services exports grew 11.6% (nominal) in the first eight months of 2026, up from 10% in 2025. *[11.6 % y/y nominal, Jan-Aug 2026]* — agrees; reproducible: yes; verified: primary.
  - C1. ch.1 p.10 (PDF p.30). All services, not IT only. Reproducible from RBI monthly data.

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03f` Software-services exports remained well above their pre-pandemic trend through FY2026; ICT-BPM is 7-8% of GDP and employs over 5 million; software and business services are about 50% of services exports; report sees 'little evidence so far' that AI has undermined the export model, but warns productivity gains may pass to clients via lower prices. *[5 million ICT-BPM workers (more than), through FY2026]* — agrees; reproducible: yes; verified: primary.
  - C1 (and our price pass-through mechanism). p.42 (PDF p.44), Fig. 4.11 (NASSCOM, Haver). Services exports rose from <10% to ~10.5% of GDP 2024-25. Frames this as restructuring within firms, not aggregate job loss.

**Bastos & Nayyar (2026)** — Bastos, Paulo, and Gaurav Nayyar. 2026. 'Artificial Intelligence and International Trade in Services: Evidence from the United States.' WDR 2026 background paper, draft. World Bank (July). <https://thedocs.worldbank.org/en/doc/0c3320b04832ac7407cd0fba03949383-0050062026/original/AI-and-services-trade-draft-July2026.pdf>

- `WB-06a` US services sectors with stronger AI adoption saw larger export increases (to developed and developing economies alike), with no robust evidence that AI adoption reduced US services imports, including from developing countries. *[qualitative (OLS and IV), 2011-2024]* — agrees; reproducible: partly; verified: primary.
  - C1 (no reshoring signal in US imports). Abstract p.1 and import results. BEA trade by partner. Mostly pre-GenAI years (sample ends 2024), so a weak test of GenAI. 'No effect' paper cited by Kruse & Yu.

**WTO (2026)** — World Trade Organization. 2026. Global Trade Outlook and Statistics - March 2026. Geneva: WTO (Mar). <https://www.wto.org/english/res_e/booksp_e/gtos0326_e.pdf>

- `WB-07a` India exported US$328bn of digitally delivered services in 2025, 6.2% of world, up 18% y/y, ranking 4th (after US, UK, Ireland). *[328 USD bn, 2025]* — agrees; reproducible: yes; verified: primary.
  - C1. Appendix Table 5, p.39 (preliminary). The 18% growth exceeds the world's 10%. Not ex-Ireland, so our ex-Ireland share must be computed separately. Check against our ~30% computer-services ex-Ireland share.
- `WB-07c` India's commercial services exports were US$415bn in 2025, 4.3% of world, up 11%, ranking 8th. *[415 USD bn, 2025]* — agrees; reproducible: yes; verified: primary.
  - C1. Appendix Table 3, p.37 (5.3% excluding intra-EU, Table 4 p.38).

**ETV Bharat (2026)** — ETV Bharat. 2026. 'India Is Now World's Fourth Largest Exporter Of Digitally Delivered Services...: WTO Data' (Oct 10). <https://www.etvbharat.com/amp/en/business/india-is-now-worlds-fourth-largest-exporter-of-digitally-delivered-services-but-trade-deficit-widens-wto-data-showss-enn26101005063>

- `WB-07d` Press report of WTO data puts India's 2025 digitally delivered services exports at US$317bn, +15%, 4th globally. *[317 USD bn, 2025]* — agrees; reproducible: yes; verified: press.
  - DISCREPANCY with the WTO March 2026 table ($328bn, +18%). It may reflect a revised October 2026 WTO update, which I could not find or open. Use the WTO primary table and note revisions.

**Baldwin (2026)** — Baldwin, Richard. 2026. 'The Jobs AI Was Supposed to Eliminate Are Booming.' Richard Baldwin Substack (Factful Friday), Jul 30-31 (also on LinkedIn). <https://rbaldwin.substack.com/p/the-jobs-ai-was-supposed-to-eliminate>

- `WB-08a` India's 'other business services' (back-office) exports rose from US$121bn (2022) to US$185bn (2025), about 15.1% a year since ChatGPT vs 13.5% in 2015-22, and now sit 27% above a log-linear 2015-22 trend. *[27 % above 2015-22 trend, 2015-2025Q4 (WTO quarterly)]* — agrees; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Reproduced exactly from WTO ITS_CS_QX via DBnomics (India $184.7bn 2025; +27.0% at 2025Q4 vs 2015Q1-2022Q4 log-linear trend). But about 15 points of the 27 predate ChatGPT (gap already +15.4% at 2022Q4); the post-ChatGPT increment is ~+10%. The series is RBI …

**ING (Bhargava 2026)** — Bhargava, Deepali. 2026. 'Why India and Philippines aren't losing the AI battle - yet.' ING Think (Sep 16). <https://think.ing.com/articles/why-ai-matters-for-india-and-the-philippines/>

- `WB-10a` India's software-services exports reached about 5.2% of GDP vs 3.3% pre-Covid, and business-services exports 3.3% vs 1.6%; software exports are about US$205bn a year and grew about 12% y/y in mid-2026. *[5.2 % of GDP (software services exports), pre-Covid vs mid-2026]* — agrees; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Reproduced: BoP software exports 3.35% (FY20) -> 5.21% (FY26) of GDP. But on the RBI survey the share is 4.62% (FY20), 5.69% (FY23), 5.66% (FY26): the rise is mostly a BoP-measurement effect and was already 4.51% on BoP by FY23, i.e. largely pre-ChatGPT. || …
- `WB-10b` India's digitally delivered services exports grew 45% since 2022 vs 32% worldwide (WTO data); its OBS DDS grew about 15% a year vs 9.3% globally, a market-share gain. *[45 % cumulative growth since 2022 (vs 32% world), 2022-2025]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): Digitally delivered exports 2022-25 (deliverable BoP items as proxy): India +44.0% vs world +32.0% (139 reporters); world ex India/Ireland/Netherlands/Luxembourg +29.7%. India's computer/telecom/information line grew +38.4% vs world +35.5% ex IE/NL/LU; the …

**Business Today (2026)** — Business Today Desk. 2026. 'Reshaping, not shrinking: How India's $205 billion tech engine defies job threats in AI era.' Business Today (Sep 18). <https://www.businesstoday.in/jobs/story/reshaping-not-shrinking-how-indias-205-billion-tech-engine-defies-job-threats-in-ai-era-556430-2026-09-18>

- `WB-10d` Business Today summary of the ING note: 'reshaping, not shrinking'; software exports 5.2% of GDP vs 3.3%; DDS +45% since 2022 vs 32% world; about $205bn and 5.8 million workers. *[45 % DDS export growth since 2022, 2022-2026]* — agrees; reproducible: yes; verified: press.
  - Press summary of WB-10a/b. Matches the ING original, with no discrepancies. Cite ING Think rather than Business Today.

## Firms (top six, mid-tier)

**IANS (2026)** — IANS (2026), 'Top IT firms' hiring turns negative as headcount falls over 7,000 in FY26', 25 Apr 2026. <https://ianslive.in/top-it-firms-hiring-turns-negative-as-headcount-falls-over-7000-in-fy26--20260425104000>

- `HIR-06a` Combined headcount of TCS, Infosys, HCLTech, Wipro and Tech Mahindra fell by 7,389 in FY26, after rising 12,718 in FY25. *[-7389 persons (net change), FY26 (vs FY25 +12,718)]* — agrees; reproducible: yes; verified: press.
  - REPRODUCED (repo check, contradictions/FINDINGS_jobs.md): Our panel gives -6,981 for FY26 (vs IANS -7,389; 408-person gap unresolved) and exactly +12,718 for FY25; all five Q4 FY26 firm figures match. || Original verification note: C2. Our filings sum (HIR-06b) gives -6,981 for FY26 (408 difference, unexplained, …

**Company filings (own calc)** — TCS, Infosys, HCLTech, Wipro, Tech Mahindra, LTIMindtree Q4 FY24-FY26 press releases / fact sheets / data sheets; compiled in project file data/explore/round3/gcc/top6_headcount_fy.csv. <https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q4/IFRS/Press%20Release%20-%20USD.pdf>

- `HIR-06b` Top-5 year-end headcount: FY24 1,524,336, FY25 1,537,054, FY26 1,530,073, so +12,718 in FY25 and -6,981 in FY26. By firm in FY26: TCS -23,460, Infosys +5,016, HCL +3,761, Wipro +8,810, TechM -1,108. *[-6981 persons (net change, top 5), FY26 (Mar-25 to Mar-26)]* — agrees; reproducible: yes; verified: primary.
  - C2. S2 firms chart. Year-ends: TCS 607,979->584,519 (confirmed in TCS Q4 FY26 release); Infosys 323,578->328,594; HCL 223,420->227,181; Wipro 233,346->242,156; TechM 148,731->147,623. Caveat: Wipro's Q3 FY26 jump (+6,529) probably includes an acquisition, so organic top-5 change is more negative. TCS alone drives the …
- `HIR-06c` Top-6 (adding LTIMindtree) headcount: 1,605,986 (FY24), 1,621,361 (FY25), 1,618,023 (FY26), so +15,375 in FY25 and -3,338 in FY26. *[-3338 persons (net change, top 6), FY26]* — agrees; reproducible: yes; verified: primary.
  - C2 headline uses top 6. LTIM +3,643 in FY26. Top-6 headcount at Mar-26 is 0.2% below Mar-25 and 3.7% below the FY23 peak (1,679,489).

**Computerworld (Singal, 2026)** — Singal, Nidhi (2026), 'AI boom, hiring bust: Indian IT firms add just 17 net employees in nine months', Computerworld, 20 Jan 2026. <https://www.computerworld.com/article/4119064/ai-boom-hiring-bust-indian-it-firms-add-just-17-net-employees-in-nine-months.html>

- `HIR-07a` Top five Indian IT firms added only 17 net employees in Apr-Dec 2025 (9M FY26), against 17,764 in the same period a year earlier. *[17 persons (net change), 9M FY26 (Apr-Dec 2025)]* — agrees; reproducible: yes; verified: press.
  - REPRODUCED (repo check, contradictions/FINDINGS_jobs.md): We get +159 for Apr-Dec 2025 (vs +17). For 9M FY25 we get +10,372, or +17,770 adding back HCLTech's 7,398 divested staff, so Constellation/Computerworld adjusted for the divestiture. Cite as 'roughly zero'. || Original verification note: C2. Figure is a quote …

**The Register (Sharwood, 2026)** — Sharwood, Simon (2026), 'Hiring at India's Big Four outsourcers stalls, as AI seemingly makes an impact', The Register, 19 Jan 2026. <https://www.theregister.com/2026/01/19/hcl_infosys_tcs_wipro_results/>

- `HIR-07b` The big four (TCS, Infosys, HCL, Wipro) added just 3,910 staff over the year to Dec 2025; Q3 FY26 changes were TCS -11,000, Infosys +5,000, Wipro +6,500, HCL -261. *[3910 persons (net change, 4 firms, 12 months), Dec 2024-Dec 2025]* — agrees; reproducible: yes; verified: press.
  - C2. Correction to literature report: The Register does NOT report the '17 net' figure. Its metric is a 4-firm, 12-month figure. Filings check: Dec-24 4-firm total 1,384,220 vs Dec-25 1,387,597 = +3,377 (close to 3,910; Wipro acquisition inflates).

**TCS (2026)** — Tata Consultancy Services (2026), Q2 FY2026-27 Fact Sheet, 8 Oct 2026; and Thapliyal, Aseem, 'TCS adds 4,258 employees in Q2...', Business Today, 8 Oct 2026. <https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q2/Presentations/Q2%202026-27%20Fact%20Sheet.pdf>

- `HIR-08a` TCS headcount rose 4,258 to 598,056 at end-Sep 2026, its third straight quarterly net gain (Q4 FY26 +2,356; Q1 FY27 +9,279 to 593,798). *[4258 persons (net QoQ), Q2 FY27]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Acknowledge but does not overturn C2: TCS's three additions (+2,356, +9,279, +4,258) follow -30,906 over Jun-Dec 2025; TCS is +0.8% YoY and -18.1k below its Sep 2022 peak. Four firms reporting Q2 FY27: +9,438 (TCS +4,258, HCLTech +6,450, TechM +5,446, Wipro …
- `HIR-08b` TCS headcount of 598,056 is 4,742 ABOVE a year earlier (593,314, Sep 2025) but 15,013 below the June 2025 peak of 613,069. *[+4742 YoY persons, Sep 2025 to Sep 2026]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Our literature note's 'about 15k below a year earlier' was wrong: TCS is +4.7k YoY; the -15k compares with Jun 2025 (613,069). || Original verification note: Correction to literature report: '~15k below a year earlier' is wrong; it is ~15k below the Jun-2025 …

**HCLTech via SightsIn Plus (2026)** — SightsIn Plus (2026), 'HCLTech adds 6,450 employees in Q2 FY27, fresher hiring rises, attrition at 12.8%', 12 Oct 2026 (HCLTech Q2 FY27 results). <https://www.sightsinplus.com/news/industry-news/hcltech-adds-6450-employees-in-q2-fy27-fresher-hiring-rises-attrition-at-12-8/>

- `HIR-08d` HCLTech added 6,450 net employees in Q2 FY27 (to a record 230,339) after cutting 3,292 in Q1; 6,136 freshers joined in the quarter vs 1,056 in Q1 and 5,196 a year earlier. *[6450 persons (net QoQ), Q2 FY27]* — complements; reproducible: yes; verified: press.
  - REPRODUCED (repo check, contradictions/FINDINGS_jobs.md): HCLTech investor release (NSE, 12 Oct 2026) confirms +6,450 to 230,339, 6,136 freshers. Counter-signal, fresher-led; Wipro -6,716 in the same quarter. || Original verification note: Partly contradicts C2/C4 for FY27: HCL's biggest quarterly addition in 16 …

**Nasscom (2026)** — Nasscom (2026). Technology Sector in India: Strategic Review 2026 - 'Steering through the tides of uncertainty: charting opportunities amid disruption'. New Delhi: Nasscom (released Feb 24, 2026; full report paid). <https://nasscom.in/knowledge-center/publications/technology-sector-india-strategic-review-2026>

- `IND-01h` Nasscom says mid-tier firms are outpacing top-tier peers, and that GCC expansion and BFSI demand drive the sector's shift. *[FY26]* — agrees; reproducible: partly; verified: primary.
  - Consistent with C2 (top-6 stagnation while sector grows). Reproducible partly from filings of mid-tier firms. S2 firms box.

**Kotak Institutional Equities (2026a)** — Kotak Institutional Equities (2026). Indian IT services sector note (post Q4FY26 results). Reported by ANI, Apr 29, 2026 (The Tribune; webindia123). <https://www.tribuneindia.com/news/business/it-services-growth-to-stay-range-bound-at-3-per-cent-as-ai-deflation-pressures-margins-mid-tiers-better-placed-says-kotak/>

- `IND-03c` Tier-1 guidance and consensus cluster at 1-4% growth; all Tier-1s except TCS missed March-quarter revenue estimates; mid-tiers better placed. *[1-4 % FY27 revenue growth guidance, FY27]* — agrees; reproducible: partly; verified: press.
  - C2 context (top firms slowing). Guidance ranges reproducible from company filings. Also cites Gartner IT services 3.1% (2025) and 4.2% (2026), not explicitly attributed in body; differs from Gartner's own releases (see IND-08c).

**Sidhant (2026)** — Aman Kai Sidhant (2026), 'India's $300B AI Shock' (two-part essay), india300.ai, Jun 18. <https://india300.ai/>

- `JRN-02a` TCS headcount fell from 607,979 (Q4 FY25) to 584,519 (Q4 FY26), down about 23,460 or 3.8%, while quarterly USD revenue rose from $7,465m to $7,621m. *[-23460 persons, FY26 (Q4 FY25 to Q4 FY26)]* — agrees; reproducible: yes; verified: press.
  - C2. Taken from TCS filings; we can reproduce it from quarterly fact sheets. The essay also says FY26 USD revenue fell 0.5%, which contradicts its own rising quarterly series (an internal inconsistency). The author is a VC investor and the essay is a bearish scenario piece.

**Forkast (2026)** — Dana Ellison [byline 'Forkast mind', likely AI-generated] (2026), 'India's IT Giants Are Cutting Jobs for the First Time in 20 Years. AI Agents Are Eating the Model That Built Them.', Forkast, Jul 10. <https://forkast.news/indias-it-giants-are-cutting-jobs-for-the-first-time-in-20-years-ai-agents-are-eating-the-model-that-built-them/>

- `JRN-05c` Claims the top 5 firms shed 7,389 staff in FY26 after adding 12,718 in FY25, and repeats broker estimates (Motilal Oswal: 9-12% of revenue at risk over four years). *[-7389 persons, FY26]* — agrees; reproducible: yes; verified: press.
  - Repeats IANS (HIR-06a); low-quality outlet, cite IANS or filings instead. LOW QUALITY: no outbound links and an apparently AI-generated byline. The -7,389 / +12,718 figure is from IANS (25 Apr 2026, see JRN-06b); cite IANS or the filings instead. Do not cite Forkast.

**IANS (2026)** — IANS (2026), 'Top IT firms' hiring turns negative as headcount falls over 7,000 in FY26', IANS, Apr 25. <https://ianslive.in/top-it-firms-hiring-turns-negative-as-headcount-falls-over-7000-in-fy26--20260425104000>

- `JRN-06b` Combined headcount of TCS, Infosys, Wipro, HCLTech and Tech Mahindra fell by 7,389 in FY26, after a net addition of 12,718 in FY25. *[-7389 persons, FY26]* — agrees; reproducible: yes; verified: press.
  - Duplicate of HIR-06a (IANS). C2 corroboration (top-5 rather than our top-6). Another outlet reports -6,981, so check against the filings. In Q4 FY26 Infosys fell by 8,440 and TCS rose by 2,356.

**ICRIER (2026)** — Mishra, D., Kedia, M., Reddy, A., Fernandez, C. & Khanduri, A. (2026). AI and Jobs: This Time Is No Different - A Case Study of India's IT Sector. ICRIER, New Delhi (February). Supported by OpenAI. <https://www.icrier.org/pdf/AI-and-Jobs.pdf>

- `TT-01h` CMIE data on ~750 IT firms: wage-to-revenue ratio rose from 37% (2020-21) to ~49% (2023-24 and 2024-25). *[49 % wage bill / revenue, 2020-21 to 2024-25]* — complements; reproducible: partly; verified: primary.
  - Section 7, p.34, Figure 14. Revenue/wage levels reported as INR 1,719 to 2,449 crore and 644 to 1,190 crore, which look like per-firm averages or a unit error. Use only the ratio, with caution. Could be checked against top-6 filings (firms section).

**Sunny (2026)** — Sunny, K. P. (2026). Artificial Intelligence and Future of India's IT Companies. Economic and Political Weekly, EPW Engage (July 1). <https://www.epw.in/engage/article/artificial-intelligence-and-future-indias-it>

- `TT-06a` Argues the revenue-by-headcount model is breaking; AI has so far reduced entry-level hiring rather than causing mass layoffs; market caps of TCS and Infosys roughly halved from 2024 peaks to mid-2026. *[2021 to mid-2026]* — agrees; reproducible: partly; verified: primary.
  - Opinion piece. TCS ~INR 15.2trn (2024) to <8trn (mid-2026); Infosys ~8trn to ~4.3trn. No headcount or hiring figures. Cites Cognizant-Pearson 2026 (AI does 37% of entry-level tasks in India). Supports C2/C4 framing only qualitatively. Context/intro.

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03c` The six largest IT-services firms cut about 64,000 workers from a combined 1.7 million after the post-pandemic surge, while the rest of the tech-services sector incl. GCCs added about 700,000 over three years, to about 4.4 million (Goldman Sachs 2026). *[-64000 persons (top-6 IT firms), post-pandemic peak to ~FY26]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_jobs.md): Only for the -64k: our panel gives -63,557 for Dec 2022->Dec 2025 (FY23->FY26 -61,466). The figure is Goldman Sachs, 'Gen-AI in India: Jobs Crosswinds, Productivity Tailwinds' (Jul 2026, client-only), citable ONLY via this World Bank IDU p.41. The +700k part is …

**ING (Bhargava 2026)** — Bhargava, Deepali. 2026. 'Why India and Philippines aren't losing the AI battle - yet.' ING Think (Sep 16). <https://think.ing.com/articles/why-ai-matters-for-india-and-the-philippines/>

- `WB-10c` ING notes IT-BPM supports about 5.8m workers and NASSCOM puts the tech workforce at about 6m in FY26 (+2.3%), while the top IT firms added only 17 net staff in 9M FY26; entry- and mid-level roles face the most pressure; ING says sector employment data are scarce. *[17 net employees added (top IT firms, 9M FY26), Apr-Dec 2025]* — agrees; reproducible: yes; verified: primary.
  - C2 agrees (top firms flat). NASSCOM +2.3% sector growth partly contradicts C3 (unverified NASSCOM). Title signals 'reshaping, not shrinking'.

## Global capability centres

**Nasscom-Zinnov (2026)** — Nasscom & Zinnov (2026). Nasscom-Zinnov GCC Landscape Report 2026 ('The GCC Value Orbit'). Nasscom and Zinnov, with K Raheja Corp (May 2026; data as of March 2026). <https://media.zinnov.com/wp-content/uploads/2026/05/zinnov-nasscom-india-gcc-landscape-report-2026.pdf>

- `IND-02a` India has 2,117 GCCs across 3,728 units in FY26E; the number of GCCs grew ~32% since FY21. *[2117 GCCs, FY26E]* — complements; reproducible: no; verified: primary.
  - C3 GCC section. Sources on p.5: Zinnov, PrivateCircle, ROC, EPFO, Wizmatic, Nasscom; proprietary database. Press release syndicated Jul 3, 2026; PDF dated May 2026.
- `IND-02b` Installed GCC talent is 2.36mn and GCC revenue USD 98.4bn in FY26E. *[2.36 million persons, FY26E]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): GCC growth is real but not faster than before 2023 (our GCC reconciliation: hiring absorbed ~2.4% of vendor workforce a year after 2023 vs ~2.8% before). Edition levels are not comparable; Nasscom folded ~0.24m GCC staff into its FY24 base. || Original …

**Nasscom-Zinnov (2024)** — Nasscom & Zinnov (2024). India GCC Landscape: The 5-Year Journey. Nasscom/Zinnov (Sep 2024); reported by ANI via ThePrint, Sep 15, 2024. <https://theprint.in/economy/indias-position-as-gcc-capital-of-the-world-nasscom-zinnov-study/2268673/>

- `IND-02e` Prior edition: 1,700+ GCCs, 2,975+ units, 1.9mn+ employees and USD 64.6bn revenue in FY24; GCC count up 32% FY19-FY24 (from ~1,285). *[1.9 million persons, FY24]* — complements; reproducible: no; verified: press.
  - Prior edition; levels not comparable with 2026 edition. Comparability point for IND-02a/b. Note both editions report '~32% growth' over different 5-year windows (FY19-24 and FY21-26). Nasscom page for the report: nasscom.in/knowledge-center/publications/india-gcc-landscape-report-5-year-journey (members only).

**Weijin Research (2026)** — Weijin Research (2026), 'AI goes long on India, shorts Indian software outsourcing', Weijin Research Substack, Sep 23. <https://weijinresearch.substack.com/p/ai-goes-long-on-india-shorts-indian>

- `JRN-03b` India is expected to have about 2,117 GCCs with 2.36m employees and about $100bn in revenue as of FY2026. *[2117 / 2.36m centres / employees, FY26 (expected)]* — complements; reproducible: no; verified: unverified (press-only).
  - C3/GCCs. No source is given (probably NASSCOM-Zinnov), and the figures are projections. Do not cite from Weijin; trace them to NASSCOM-Zinnov if needed. Compare india300's 1,800+ centres / 1.9m staff (FY25, via IBEF).

**Economic Survey 2025-26, Ch. 7** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 7: Services: From Stability to New Frontiers (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf>

- `TT-03d` As of FY24 India hosts 1,700+ GCCs employing over 19 lakh (1.9m) professionals; GCC revenue US$64.6bn (FY24E) vs 40.4bn (FY19). *[1.9 million GCC employees, FY24]* — complements; reproducible: no; verified: primary.
  - Para 7.33 and Chart VII.12, p.279; source NASSCOM. Only India IT employment figure in the Survey. Also para 7.32: Nasscom IT-ITeS revenue US$283bn FY25 (+5.1%), IT services exports +3.7% FY25. GCC box.

**Roy Bardhan & Bhowmick (2026)** — Roy Bardhan, A. & Bhowmick, S. (2026). Capability in the Age of AI: India's GCCs and the Future of White-Collar Work. ORF Special Report No. 312, Observer Research Foundation (June 16). DOI 10.64503/20260616. <https://www.orfonline.org/research/capability-in-the-age-of-ai-india-s-gccs-and-the-future-of-white-collar-work>

- `TT-05a` Stress test of AI displacement in GCCs: gross displacement of 40,183 to 150,686 jobs by 2030 (net 24,110 to 120,549 after 20-40% reinstatement), against a 4.5m baseline. *[40,183-150,686 jobs (gross), to 2030]* — complements; reproducible: no; verified: primary.
  - ORF SR 312. Six scenarios (linear/exponential x 50/67.5/87.5% convergence). 0.9-3.3% of baseline. Authors call it a stress test, not a forecast; sensitive to optimistic 4.5m baseline. GCC box.
- `TT-05b` GCC employment about 1.9m in FY24 and over 2.3m in FY26; >2,100 GCCs; revenue ~US$98-100bn (Zinnov-NASSCOM 2026). *[2.3 million GCC employees, FY24-FY26]* — complements; reproducible: no; verified: primary.
  - Secondary figures within ORF SR 312. Says AI may reduce entry-level absorption even if GCC output grows (C4). Says PLFS cannot disaggregate enough to detect it. Proprietary source (Zinnov).

**Roy Bardhan & Joshi (2026)** — Roy Bardhan, A. & Joshi, S. (2026). Evaluating the AI Threat to India's IT Model. ORF Expert Speak (Raisina Debates), Observer Research Foundation (June 29). <https://www.orfonline.org/expert-speak/evaluating-the-ai-threat-to-india-s-it-model>

- `TT-05c` Zinnov data: installed GCC talent rose from ~1.75m (FY21) to 2.36m (FY26E), a ~6.2% CAGR, while GCC revenue grew ~9.9% CAGR (US$61.4bn to 98.4bn). *[6.2 % CAGR GCC headcount, FY21-FY26E]* — agrees; reproducible: no; verified: primary.
  - ORF Expert Speak, Table 1 (from Zinnov GCC Landscape 2026). Authors are Roy Bardhan and Siddharth Joshi (not Bhowmick). Revenue outpacing headcount supports C3 (GCC hiring not a boom); five-year CAGR cannot split pre/post-2023. Argues revenue can grow while jobs shrink and PLFS/EPFO/GDP data cannot capture …

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03e` India exported about US$200bn of ICT services in 2025; its GCC ecosystem had 2,117 centres employing 2.36 million and generating US$98.4bn revenue in FY2026 (Zinnov-NASSCOM). *[2.36 million GCC employees, FY2026]* — complements; reproducible: no; verified: primary.
  - C1/C3. p.32 (PDF p.34). The GCC figure is Zinnov-NASSCOM (we lack it); IBEF-style coverage gives growth from 1.9m to 2.36m. ICT exports from World Bank Open Data (BoP).

## Sector jobs

**Nomura (Varma & Toh, 2026)** — Varma, Sonal & Si Ying Toh (2026), Nomura economics note on AI and jobs in Asia (title not public), as reported by Business Today Desk, 'India is hiring more for AI than it is laying off, says Nomura', 7 Aug 2026, and 9 Aug 2026. <https://businesstoday.in/jobs/story/india-is-hiring-more-for-ai-than-it-is-laying-off-says-nomura-547943-2026-08-07>

- `HIR-05a` Nomura counts 83,100 AI-related hires against 31,921 AI-linked layoffs/attrition in India (about 2.6 hires per job lost), 2022 to Aug 2026. *[83100 vs 31921 persons (announced cases), 2022-Aug 2026]* — complements; reproducible: no; verified: press.
  - C2/C3: net AI-attributed effect is positive, but it is a tally of company announcements from news reports, not a census. Correction to literature report: the 69 cases cover ALL of Asia, not India. Asia totals: 130,758 hires vs 60,654 losses; >90% of hires in tech; ~60% of cuts in financial services. Primary note not …

**Nasscom (2026)** — Nasscom (2026). Technology Sector in India: Strategic Review 2026 - 'Steering through the tides of uncertainty: charting opportunities amid disruption'. New Delhi: Nasscom (released Feb 24, 2026; full report paid). <https://nasscom.in/knowledge-center/publications/technology-sector-india-strategic-review-2026>

- `IND-01c` Nasscom projects direct tech-sector employment of ~6mn in FY26 (PTI: 59.5 lakh, up from 58.15 lakh), +2.3% or net 135,000 added. *[135000 persons (net additions), FY26E]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Compatible with PLFS (Nasscom +6.1% chained FY23-26 ~ +4.9% over PLFS's 2.5-yr window vs PLFS +4.1%, z=0.12). Treat as 'about 2% a year, unverified': published before year-end, revised each edition, no sampling error, not independent of the Zinnov GCC count. …
- `IND-01f` Nasscom president Rajesh Nambiar highlighted the gap ('non-linearity') between job growth of 2.3% and revenue growth of 6.1%. *[2.3 vs 6.1 % y/y growth (jobs vs revenue), FY26E]* — agrees; reproducible: no; verified: press.
  - Supports C2/C3 framing (revenue decoupling from headcount); the word 'non-linearity' is from coverage, not seen on primary page. S2 jobs box, epigraph-style.

**Nasscom (2025)** — Nasscom (2025). Technology Sector in India: Strategic Review 2025 - 'Beyond Disruption: Staying Future-Ready Today'. Nasscom (Feb 2025); summary on Nasscom Community. <https://community.nasscom.in/communities/nasscom-insights/technology-sector-india-strategic-review-2025>

- `IND-01k` FY25 edition: net hiring rose to 126,000, taking the employee base to 5.80mn (+2.2% y/y); only 45% of providers expected higher hiring in FY26. *[126000 persons (net additions), FY25E]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Vintage issue: FY25 net adds 126k in the FY25 edition, revised to 133k in the FY26 edition. Nasscom's FY24 base was restated from 5.43m to ~5.68m, equal to Nasscom-Zinnov's +0.24m GCC revision; chain within vintages. || Original verification note: Contradicts …

**Nasscom (2024)** — Nasscom (2024). Technology Sector in India: Strategic Review 2024 - 'Rewiring for Growth'. Nasscom (Feb 2024); summary on Nasscom Community. <https://community.nasscom.in/communities/nasscom-insights/rewiring-growth-changing-tech-landscape-strategic-review-2024>

- `IND-01l` FY24 edition: revenue est. USD 254bn (+3.8%); industry stayed a net hirer, adding 60,000 to reach 5.43mn employees (+1.1%). *[60000 persons (net additions), FY24E]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): The 5.43m FY24 level was later restated to ~5.68m (GCC coverage revision of ~0.24m); do not difference levels across editions. || Original verification note: Series point for Nasscom headcount; FY24 low point matches top-6 stagnation. Note 5.43m + 126k != 5.80m …

**Goldman Sachs (2026b)** — Goldman Sachs (2026). India strategy note pushing back on 'short-AI India' narrative; reported via Bloomberg in Business Today, Oct 1, 2026. <https://www.businesstoday.in/markets/stocks/story/goldman-sachs-pushes-back-on-short-ai-india-narrative-says-report-42-stocks-in-focus-559148-2026-10-01>

- `IND-06b` Goldman (citing Sengupta) says hiring at smaller tech companies and GCCs is helping offset job losses in traditional software services. *[2026]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Goldman press coverage gives no numbers. Its -64k/+700k figures are citable only via World Bank IDU Oct 2026 p.41 (see WB-03c, WB-03g). Like-for-like the non-top-6 sector grew ~+0.39m over FY23-26, consistent with 'big firms stopped adding, sector growing …

**Future of India Foundation (2026)** — Future of India Foundation [unsigned; same text posted by Ruchi Gupta on her Substack 6 Oct 2026] (2026), 'IT Sector Helped Build the Indian Middle Class. For Its Workers, It Is Starting to Sputter', India After Liberalisation series Part 5, YouthPOWER / Future of India Substack, Oct 2. <https://foifaction.substack.com/p/it-sector-helped-build-the-indian>

- `JRN-01b` IT's share of all salaried graduates rose from 6.9% to 13.7% and then fell to 11.2%. *[6.9 -> 13.7 -> 11.2 % of salaried graduates, 2017-18, 2022-23, 2025]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_entry_level.md): Exact match: ours 6.9 / 13.8 / 11.2%. || Original verification note: C3/C4. Peak in 2022-23. The article also gives IT's share of graduates in the labour force as 3.9% -> 7.4% -> 6.0% (years implied to be the same).
- `JRN-01c` IT employment (NIC 62-63) rose from 28.8 lakh to 69.3 lakh, then dipped to 68.2 lakh. *[28.8 -> 69.3 -> 68.2 lakh persons, 2017-18, 2023-24, 2025]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md): Their levels are 1.16-1.22x ours (ours 23.5 / 59.8 / 57.0 lakh), consistent with rescaling to population projections (inference). 'IT employment peaked in 2023-24' is NOT robust: excluding the high-weight cluster, 2023-24 is 56.7 lakh, below CY2025's …
- `JRN-01d` Software developers and analysts in IT fell from 42.5 lakh to 36.7 lakh, which the article rounds to about 14% (13.6% by calculation). *[-14 % change (42.5 -> 36.7 lakh), 2023-24 to 2025]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md): Fragile: ours 36.8 -> 30.7 lakh (theirs after rescaling); z ~1.5, 2023-24 includes the inflated cluster, and the shift to keyboard operators/support technicians coincides with the 2025 survey redesign. Do not cite as a finding. || Original verification …

**Gupta (2026)** — Ruchi Gupta (2026), 'Indian IT Sector is Growing. Its Gains Are Not Reaching Workers.', India: Politics, Power & Public Discourse (Substack), Oct 6. <https://rgupta.substack.com/p/indian-it-sector-is-still-growing>

- `JRN-06c` Signed version of JRN-01 (same India After Liberalisation Part 5 text): IT's share of salaried graduates peaked in 2022-23; headcount, median earnings and labour share of value added peaked in 2023-24. *[2017-18 to 2025]* — agrees; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md; labour_share/FINDINGS.md): Same text as JRN-01; see corrections there (levels rescaled, peaks not robust, labour-share fall an artefact). || Original verification note: This identifies the likely author of JRN-01 as Ruchi Gupta (Future of India …

**LinkedIn Economic Graph (2026)** — LinkedIn Economic Graph, India hiring rate (monthly, 2016=1), series embedded on economicgraph.linkedin.com, accessed Oct 2026; repo file postings/linkedin_hiring_rate_monthly.csv. <https://economicgraph.linkedin.com/>

- `REP-02a` LinkedIn's India hiring-rate index averaged 2.64 in 2022 and 1.79 in Jan-May 2026, about 32% lower; year-on-year change negative in 11 of the last 12 months. *[-32 % vs 2022 (hiring-rate index), 2022 to Jan-May 2026]* — complements; reproducible: partly; verified: primary.
  - C3 context (all industries, LinkedIn members only, <40% of workforce, urban/tech skew). Agrees with Naukri JobSpeak IT (~-30% vs 2022). US/UK software postings fell about twice as far (Indeed). Source: postings/FINDINGS.md

**Xpheno via Business Standard (2026)** — Xpheno estimates as reported in Business Standard, 20 May 2026; compiled in repo fresher_thirdparty/fresher_thirdparty_long.csv. (URL in repo CSV)

- `REP-05a` Xpheno puts net headcount additions at IT firms at 50k (FY24), 100k (FY25), 110k (FY26) and at GCCs at 60k, 110k, 200k. *[110000 net headcount additions, IT firms (persons), FY24-FY26]* — complements; reproducible: no; verified: press.
  - C2/C3: with top-5 at -7.4k in FY26, non-top-5 IT firms would have added >100k; UnearthInsight says IT services net adds 'up to 35k' in FY26, so FY26 IT net adds are uncertain (35-110k). GCC FY25 silently revised 140k -> 110k. Source: fresher_thirdparty/FINDINGS.md

**ICRIER (2026)** — Mishra, D., Kedia, M., Reddy, A., Fernandez, C. & Khanduri, A. (2026). AI and Jobs: This Time Is No Different - A Case Study of India's IT Sector. ICRIER, New Delhi (February). Supported by OpenAI. <https://www.icrier.org/pdf/AI-and-Jobs.pdf>

- `TT-01b` 65% of firms report hiring fell after introducing AI, 24% report an increase, 11% no significant change. *[65 % of firms, after AI adoption (to 2025-26)]* — agrees; reproducible: no; verified: primary.
  - Section 4.1, p.15, Figure 1 left panel. Supports C2/C3 (hiring slowdown). Literature report's 'about two-thirds' is correct.
- `TT-01f` Executive summary states that while AI adoption has moderated hiring, total employment in the IT sector has continued to grow; no evidence of large-scale job losses. *[2021-22 to 2023-24]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Not a contradiction. The 'employment continued to grow' line rests on ICRIER's own PLFS tabulation (Section 7, pp.32-33), not the 651-firm survey, and covers only 2021-22 to 2023-24 (the boom tail, ending at the 2023-24 round inflated by one high-weight sampling …
- `TT-01g` PLFS employment in NIC 62 (computer programming, consultancy) rose from 3.8m in 2021-22 to 5.2m in 2023-24; NIC 63 (information services) from 731k to 810k. *[5.2 million persons, 2021-22 to 2023-24]* — complements; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_jobs.md): ICRIER NIC 62 3.8m->5.2m vs ours 3.818m->5.179m; 62+63 ~4.53m->5.99m vs ours 4.583m->5.976m. Cite our numbers; mention theirs match. || Original verification note: Section 7, pp.32-33. This is the basis of 'total employment continued to grow'. Most growth is …
- `TT-01i` Expectations: 44% of firms expect no major change in employment, 28% expect expansion, 27% expect decline. *[27 % of firms expecting decline, near term (from 2025-26)]* — complements; reproducible: no; verified: primary.
  - Exec summary p.9. Context.

**Economic Survey 2025-26, Ch. 7** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 7: Services: From Stability to New Frontiers (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf>

- `TT-03c` Survey notes a 'services employment-output paradox': rapid GVA growth in high-end services has not translated proportionately into jobs, citing NITI Aayog (Oct 2025). *[2011-2024]* — agrees; reproducible: partly; verified: primary.
  - Box in Ch.7, p.265. Qualitative; not an India IT test. The Survey does not estimate Indian IT employment anywhere in Ch.7 or Ch.14. The press line about export gains 'not translating into jobs' is this general sentence, not a result. Confirms the literature report's caution.

**NITI Aayog (2025)** — NITI Aayog (with NASSCOM and BCG) (2025). Roadmap for Job Creation in the AI Economy. NITI Frontier Tech Hub, New Delhi (October). <https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf>

- `TT-04a` India's tech workforce was 7.5-8m in 2023 (tech services plus tech jobs in other sectors); headwinds could cut it to ~6m by 2031, tailwinds raise it to ~10m. *[6-10 million persons, 2023 to 2031]* — complements; reproducible: no; verified: primary.
  - p.6 (summary) and pp.21-22 (pdf), Fig. 8. Baseline is 'total tech workforce' incl. tech jobs in other sectors, not IT services only (literature report says 'tech-services jobs'). Text also says 'lose 1.5m or create up to 4m' and elsewhere 'by 2030 add 2m' (internally inconsistent). Scenario, not data. …
- `TT-04c` Customer-experience (CX/BPO) workforce of 2-2.5m in 2023 could fall to 1.8m or rise to 3.1m by 2031. *[1.8-3.1 million persons, 2023 to 2031]* — complements; reproducible: no; verified: primary.
  - pp.6 and 22. BPM context.

**EPFO payroll (availability)** — Employees' Provident Fund Organisation / MoSPI. Payroll Reporting in India: An Employment Perspective (monthly), net payroll by industry and age. <https://www.epfo.gov.in/site_en/Estimate_of_Payroll.php>

- `TT-10b` EPFO publishes monthly net payroll additions by industry (incl. 'expert services'/computer-related) and by age band; the Economic Survey cites it for FY26. *[monthly]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, epfo/FINDINGS.md): Repo has 66 EPFO net-payroll PDFs (Jul 2019-Aug 2025) via Wayback (epfindia.gov.in returns 403 from outside India). EPFO appears to have stopped publishing after the Sep 2025 release. IT heading appears only in top-10 tables for ages 18-28; see REP-01. || Original verification …

**World Bank (2025)** — World Bank. 2025. South Asia Development Update, October 2025: Jobs, AI, and Trade. Ch. 2 'Artificial Intelligence, Real Impact' by P. Kirby, J. Rexer, S. Sharma. Washington, DC (Oct 7). <https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf>

- `WB-01a` After ChatGPT's release, job postings in business-services occupations grew about 35% more slowly than in other occupations (diff-in-diff, occupation and month fixed effects; Lightcast South Asia, mostly India). *[-35 % relative to other occupations (log points -0.349), Aug 2020-Mar 2025 (post = after Nov 2022)]* — agrees; reproducible: no; verified: primary.
  - Repo extracted chart workbook: most-exposed quartile posting index 2.45 -> 1.53 (-37%) Nov 2022-Mar 2025 vs least-exposed 2.56 -> 2.81 (+10%); AI-skill share of postings 2.65% -> 6.51% (postings/FINDINGS.md). || Original verification note: C3/C4. Text p.38 (PDF p.60); Fig. 2.11C p.39; Annex Table A2.10 p.55. The …
- `WB-01c` GenAI cut monthly job listings by about 20% for the most AI-exposed, least AI-complementary white-collar occupations (e.g. call-centre agents, software developers); call-centre agents fell 24% relative to machine operators. *[-20 % of monthly listings, post-Nov 2022 vs pre, through Mar 2025]* — agrees; reproducible: no; verified: primary.
  - C3/C4. Chapter summary p.27 and p.30; call-centre figure p.37; event study Fig. 2.10 p.38. Postings only.

**World Bank (2026a, SAEU Apr)** — World Bank. 2026. South Asia Economic Update, April 2026: Working with Industrial Policy. Washington, DC (Apr 8). <https://documents.worldbank.org/curated/en/099919404082611180/pdf/IDU-2569cd85-1e68-48e3-8e5c-ddc710893e1f.pdf>

- `WB-02a` Across South Asian firms, an interquartile-range rise in AI exposure is associated with a 1.5% fall in job postings relative to trend, about twice that for multinational affiliates; suppliers to highly AI-exposed foreign buyers cut hiring about 10% per IQR of buyer exposure. *[-1.5 % of job postings per IQR of firm AI exposure, post-Nov 2022 (Lightcast, to 2025)]* — agrees; reproducible: no; verified: primary.
  - C3. Overview Box 2.1 p.xvi (PDF p.18); ch.1 pp.27-28 Fig. 1.10E-F. This is 'World Bank 2026a' in Kruse & Yu (source of the 'BPO postings decline' line). The literature report did not have it. Firm-level postings, not employment.

**World Bank (2026, SAEU Oct)** — World Bank. 2026. South Asia Economic Update, October 2026: Adopting AI for Growth. Washington, DC (Oct 6). GVC analysis draws on Chiplunkar et al. (2026). <https://documents.worldbank.org/curated/en/099552210132636511/pdf/IDU-c65c3333-7e66-4072-9ce4-05ce12d2f398.pdf>

- `WB-02c` Oct 2026 SAEU (title 'Adopting AI for Growth') reports that hiring has slowed among South Asian firms whose workforces are highly AI-exposed, while AI-skill jobs carry a wage premium of nearly 30%. *[30 % wage premium for AI skills, 2020-2025]* — agrees; reproducible: no; verified: primary.
  - C3. ch.2 p.46 (PDF p.66), Fig. 2.2. It is titled 'South Asia Economic Update', not 'Development Update'. The IDU reference list calls it 'Delivering the promise of AI in South Asia'. The WDS catalogue title is 'Adopting AI for Growth'.
- `WB-02d` Indian GVC suppliers selling highly AI-exposed services cut hiring sharply after ChatGPT, most where foreign buyers were AI-exposed and suppliers had low AI complementarity (the routine BPO/ICT profile), consistent with buyers reshoring tasks. *[qualitative, post-Nov 2022]* — agrees; reproducible: no; verified: primary.
  - C3/C4. p.57 (PDF p.77), citing World Bank Group 2026b. This is the 'reshoring' evidence the literature report mentions.

**World Bank (2026, IDU)** — World Bank (2026), India Development Update, 'India and Artificial Intelligence: Seizing the Development Opportunity', October 2026, p.41, citing Goldman Sachs, 'Gen-AI in India: Jobs Crosswinds, Productivity Tailwinds' (July 2026). <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03g` The rest of the tech-services sector, including GCCs, added around 700,000 workers over three years to about 4.4 million (Goldman Sachs via World Bank). *[700000 persons (net additions, ex top-6), ~FY23-FY26]* — complements; reproducible: partly; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_jobs.md): Overstated as hiring. Reconstruction (inference; Goldman workings not public): Nasscom FY23 old vintage (~5.37m) minus top-6 (1.68m) = 3.69m; Nasscom FY26 2026 vintage (5.95m) minus top-6 (1.62m) = 4.33m. About 0.24m of the gap is Nasscom's FY24 GCC restatement. …

**Kruse & Yu (2026)** — Kruse, Hagen, and Shu Yu. 2026. 'The AI Exposure of Export-Linked Jobs.' Background Note for the World Development Report 2026. World Bank (July). <https://thedocs.worldbank.org/en/doc/9df559d23a6d80b3dfa2c4bc808f3a20-0050062026/original/The-AI-Exposure-of-Export-Linked-Jobs.pdf>

- `WB-04b` India has a revealed comparative advantage (RCA>1) in AI-substitutable export-linked jobs in business services; authors expect negative within-sector but only moderate aggregate employment effects, while exports might keep growing. *[qualitative (RCA>1), recent LFS/IO]* — agrees; reproducible: partly; verified: primary.
  - C1+C3 ('output up, sector jobs under pressure'). p.11 (PDF pp.11-12), Table 1. Cites World Bank 2026a (SAEU Apr 2026) for the BPO postings decline. Says its findings align more with the negative-offshoring studies.

## Entry level

**TeamLease EdTech (2026)** — Sharma, Anurag (2026), 'Fresher hiring intent rises to 75%, but IT demand loses ground: Report', People Matters, Aug 2026 (reporting TeamLease EdTech, Career Outlook Report HY2 2026). <https://www.peoplematters.in/amp/news/workforce-planning/fresher-hiring-intent-rises-to-75percent-but-it-demand-loses-ground-report-51352>

- `HIR-01a` Share of IT employers intending to hire freshers in Jul-Dec 2026 fell to 76% from 81% in Jan-Jun 2026. *[76 (from 81) % of employers intending to hire freshers, H2 2026 vs H1 2026]* — agrees; reproducible: no; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Series break at the 2025 H2 edition (sample ~650 -> ~1,065, more small firms; sector values leap). Only within-regime comparisons are safe: 2021-2025H1 IT fell 67 -> 42 then recovered to 59; 2025H2-2026H2 IT went 75 -> 81 -> 76. Stated intent, unweighted share of …
- `HIR-01b` Overall fresher hiring intent across sectors rose to 75% from 73%, led by e-commerce/tech start-ups and retail (93% each), manufacturing 89%. *[75 (from 73) % of employers intending to hire freshers, H2 2026 vs H1 2026]* — agrees; reproducible: no; verified: press.
  - C4 (IT falling while other sectors rise = IT-specific entry narrowing, not a general graduate-market collapse). Same caveats as HIR-01a. IT (76%) still above the all-sector average.

**foundit (2026)** — The Hans India (2026), 'Employers seek more specialised skills from freshers: Survey', 16 Sep 2026 (reporting foundit Insights Tracker, July 2026). <https://www.thehansindia.com/hans/young-hans/employers-seek-more-specialised-skills-from-freshers-survey-1122312>

- `HIR-02a` IT hardware & software firms' share of fresher hiring fell from 32% (2025) to 24% (2026). *[24 (from 32) % of fresher hiring (postings), Jul 2025 vs Jul 2026]* — agrees; reproducible: no; verified: press.
  - foundit reports 24% in Sep 2026 coverage; the postings check found 22% for Jul 2026 in another release. foundit fresher postings negative YoY since Mar 2026 (-2, -2, -2, -6, -10). Postings, not hires (fresher_thirdparty/FINDINGS.md; postings/FINDINGS.md). || Original verification note: C4. Entry-level section. foundit …
- `HIR-02b` Overall fresher hiring on foundit fell 10% year on year (and 2% month on month) in July 2026. *[-10 % YoY (postings index), Jul 2026]* — agrees; reproducible: no; verified: press.
  - C4. Contrasts with Naukri JobSpeak, which shows 0-3 yr postings rising in 2026 (HIR-10). Portal-specific; metric is a postings index.

**Xpheno via Outlook Business (2026)** — Acharya, Shristi (2026), 'India Inc's Fresher Hiring Sees Steep Drop amid AI Adoption', Outlook Business, 1 Jun 2026 (Xpheno data; Mint analysis). <https://www.outlookbusiness.com/corporate/india-incs-fresher-hiring-sees-steep-drop-amid-ai-adoption>

- `HIR-03a` Active entry-level tech openings (up to 2 years' experience) were about 10,000, down 44% year on year (from 13,000 in May 2026 per the article). *[10000 (-44% YoY) job openings (count), mid-2026 (month not stated)]* — agrees; reproducible: no; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md; postings/FINDINGS.md): Jun 2026 was the low. By Oct 2026 Xpheno reported entry-level tech openings at ~15k, +15% YoY, total openings 120-123k (18-month high), IT services 66k (+57% YoY). The narrowing shows as a SHARE (entry-level share of openings 16.1% Jun 2025 …
- `HIR-03b` Active tech openings were 93,000, the lowest in 28 months, down 14% MoM and 17% YoY. *[93000 job openings (count), June 2026 (as stated)]* — agrees; reproducible: no; verified: press.
  - C2/C4 context. Inconsistency: article dated 1 Jun 2026 but labels the figure 'June'; probably end-May snapshot. Taggd/ET coverage repeats 93k for June. Openings stock, not hires.

**Mint via Outlook Business (2026)** — Acharya, Shristi (2026), 'India Inc's Fresher Hiring Sees Steep Drop amid AI Adoption', Outlook Business, 1 Jun 2026 (Xpheno data; Mint analysis). <https://www.outlookbusiness.com/corporate/india-incs-fresher-hiring-sees-steep-drop-amid-ai-adoption>

- `HIR-03c` Infosys staff aged 30 and under were 50.7% of its workforce at end-FY26, the lowest in 15 years, vs 53% in FY25; at least two-thirds until FY18. *[50.7 % of employees aged <=30, FY26]* — agrees; reproducible: yes; verified: press.
  - C4. Verified against Infosys ESG Databook - see HIR-09a (FY25 is 52.5%, not 53%). Same article: TCS under-30 ~48% in FY25.

**Xpheno via Business Today (2026)** — Sangani, Priyanka (2026), 'Indian IT's fresher hiring slump signals structural shift, not just slowdown', Business Today, 21 Mar 2026 (Xpheno data). <https://www.businesstoday.in/technology/story/indian-its-fresher-hiring-slump-signals-structural-shift-not-just-slowdown-521374-2026-03-21>

- `HIR-04a` Xpheno estimates IT-sector fresher hiring fell from a peak of about 600,000 in FY22 to about 120,000 in FY25 (-80%), with FY26 expected to be only slightly higher. *[600000 -> 120000 fresher hires (persons), FY22-FY25]* — agrees; reproducible: no; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Xpheno's FY22 peak has drifted from ~450k (projected Feb 2022, 'almost double' 225k) to 600k (quoted from 2026) without explanation; treat 450-600k as the range. FY24 was the trough (60-70k, 'lowest in two decades'), FY25 ~120k, FY26 'marginally higher': the …

**Business Today (2026)** — Sangani, Priyanka (2026), 'Indian IT's fresher hiring slump signals structural shift, not just slowdown', Business Today, 21 Mar 2026 (Xpheno data). <https://www.businesstoday.in/technology/story/indian-its-fresher-hiring-slump-signals-structural-shift-not-just-slowdown-521374-2026-03-21>

- `HIR-04b` Offer deferrals: Wipro cut its fresher guidance to 7,500-8,000 (from 10,000) and deferred joining dates; about 1,000 Tech Mahindra candidates were awaiting joining letters; Infosys kept its 20,000 target (18,000 onboarded). *[7500-8000 fresher hires guided (Wipro), FY26]* — agrees; reproducible: partly; verified: press.
  - C4 colour. Firm-specific anecdotes; Infosys figure cuts the other way (HIR-08e).

**Nomura / Business Today (2026)** — Business Today Desk (2026), 'India adds 2.6 AI jobs for every role lost...', 9 Aug 2026. <https://www.businesstoday.in/technology/artificial-intelligence/story/india-adds-2-6-ai-jobs-for-every-role-lost-but-a-widening-skills-gap-threatens-freshers-report-548182-2026-08-09>

- `HIR-04c` Claimed citation of Xpheno: net IT hiring 600,000 (FY22) to 140,000 (FY26). NOT found in the BT 9 Aug or 7 Aug articles or in TNW's Nomura coverage. *[FY22-FY26]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Source located: ET, 23 Aug 2026, attributes to Xpheno 'net hiring in the IT sector fell from around 600,000 in FY22 to 140,000 in FY26'. This is a mislabel: 600k is Xpheno's FRESHER-intake peak, not net hiring (Nasscom FY22 net adds ~230k; Xpheno's own FY26 IT …

**Nomura (Varma & Toh, 2026)** — Varma, Sonal & Si Ying Toh (2026), Nomura economics note on AI and jobs in Asia (title not public), as reported by Business Today Desk, 'India is hiring more for AI than it is laying off, says Nomura', 7 Aug 2026, and 9 Aug 2026. <https://www.businesstoday.in/technology/artificial-intelligence/story/india-adds-2-6-ai-jobs-for-every-role-lost-but-a-widening-skills-gap-threatens-freshers-report-548182-2026-08-09>

- `HIR-05b` Nomura calls India 'ground zero' for AI's employment effects and warns of a two-tier labour market: more demand for experienced staff, less for entry-level workers. *[2022-2026]* — agrees; reproducible: no; verified: press.
  - C4 (qualitative). Cuts land in support/BPO roles; hiring goes to experienced AI talent. Usable as a framing quote in the entry-level section.

**TCS via Business Today (2026)** — Tata Consultancy Services (2026), Q2 FY2026-27 Fact Sheet, 8 Oct 2026; and Thapliyal, Aseem, 'TCS adds 4,258 employees in Q2...', Business Today, 8 Oct 2026. <https://www.businesstoday.in/markets/stocks/story/tcs-adds-4258-employees-in-q2-marks-third-quarter-of-headcount-addition-560460-2026-10-08>

- `HIR-08c` TCS issued about 25,000 fresher offers at the start of FY27; about 14,000 had joined by end of Q1 FY27. *[25000 fresher offers, FY27]* — agrees; reproducible: partly; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): TCS hired ~44k freshers in FY26; 25k offers for FY27 is lower. Stated FY27 targets (TCS 25k + Infosys 20k + Cognizant 20k) sum to ~65k vs ~84k FY26 actuals for the same firms; Wipro and HCLTech give none. || Original verification note: Partly contradicts C4 at …

**Infosys (2026)** — Infosys Integrated Annual Report 2025-26 p.25; Outlook Business Desk (2026), 'Infosys plans to hire 20,000 freshers in FY27 even as quarterly headcount dips', 24 Apr 2026. <https://www.outlookbusiness.com/corporate/infosys-plans-to-hire-20000-freshers-in-fy27-even-as-quarterly-headcount-dips>

- `HIR-08e` Infosys hired 20,000+ fresh graduates in FY26 and expects at least 20,000 in FY27 (CFO Jayesh Sanghrajka). *[20000 fresher hires, FY26 actual; FY27 plan]* — complements; reproducible: yes; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Infosys fresher intake recovered from 11.9k (FY24) to 20k+ (FY26) and is flat at 20k for FY27: partial recovery, well below FY22. || Original verification note: Partly contradicts C4. But Infosys freshers were 84,782 in FY22 and ~50,000 in FY23 (IARs), so 20k is …

**Cognizant (2026)** — Kanchwala, Tasneem (2026), 'Cognizant Plans To Hire 25,000 Freshers In 2026: CFO Jatin Dalal Confirms', Free Press Journal, 6 Feb 2026. <https://www.freepressjournal.in/amp/tech/cognizant-plans-to-hire-25000-freshers-in-2026-cfo-jatin-dalal-confirms>

- `HIR-08f` Cognizant plans to hire 24,000-25,000 fresh graduates in 2026, about 20% more than the ~20,000 it hired in 2025. *[24000-25000 fresher hires (plan), CY2026]* — complements; reproducible: partly; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Cognizant cut its CY2026 plan from 24-25k (Feb) to 20k (Jul 2026), i.e. flat on CY2025's ~20k. || Original verification note: Contradicts C4 for Cognizant (a US-listed firm with most staff in India). The CEO argues AI makes juniors productive faster ('broader …

**Infosys ESG Databook (2026)** — Infosys (2026), ESG Databook 2025-26, Annexure (employees by age group), p.27; Infosys ESG Databook 2024-25 p.26. <https://www.infosys.com/sustainability/documents/infosys-esg-databook-2025-26.pdf>

- `HIR-09a` Infosys employees aged 30 and under: 166,636 of 328,594 (50.7%) at end-FY26, vs 169,765 of 323,578 (52.5%) at end-FY25. *[50.7 % of employees aged <=30, FY26 (vs 52.5 FY25)]* — agrees; reproducible: yes; verified: primary.
  - C4. Confirms Mint/People Matters 50.7%. Their '53%' for FY25 is rounded; the exact figure is 52.5%. FY23 was 59.6%. The count of under-30s fell only ~3k in FY26; the share fell mainly because the 31-50 band grew (+6.5k). Pre-FY22 trend was already about -2 pp/yr.

**TCS Integrated Annual Reports (2022-2025)** — TCS Integrated Annual Report 2021-22 (Human Capital, p.22) and 2024-25 (MD&A, p.85), employee age infographic (India employees). <https://www.tcs.com/investor-relations>

- `HIR-09b` Share of TCS India employees under 30 fell from 59.0% (FY22) to 47.7% (FY25); FY23 52.9%, FY24 50.3%. *[47.7 % of India employees aged <30, FY22-FY25]* — agrees; reproducible: yes; verified: primary.
  - C4. Matches Mint's 59%->47.7%. Values are read from infographic labels (male+female summed) in the project extract (data/explore/workforce/extract_tcs_infosys.csv). TCS gives no age counts in numbers, and BRSR splits by gender only, not age. FY26 IAR age chart not yet in the extract.

**Naukri JobSpeak (Jan-Feb 2026)** — Info Edge / Naukri (2026), Naukri JobSpeak Index, monthly reports Jan, Feb, Jun, Sep 2026. <https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-Feb-2026.pdf>

- `HIR-10a` Fresher (0-3 yrs) postings, all industries, rose 8% YoY in Jan 2026 and 17% in Feb; IT-Software postings were -2% YoY in Jan and +6% in Feb. *[17 % YoY (postings, 0-3 yrs, all industries), Jan-Feb 2026]* — complements; reproducible: partly; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md): Not a contradiction: postings, not hires, all industries, no campus hiring. Chained vs 2022, fresher (0-3 yr) postings in 2026 are only back to the 2022 level (-0.1% Jan, +1.0% Feb, +6.1% Aug) after a 12% fall 2022-24, while the IT-Software index is …

**Naukri JobSpeak (Jun 2026)** — Info Edge / Naukri (2026), Naukri JobSpeak Index, monthly reports Jan, Feb, Jun, Sep 2026. <https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-June-2026.pdf>

- `HIR-10b` IT-Software/Software Services postings fell 3% YoY in June 2026 (index 3,415 vs 3,523), while overall white-collar postings rose 6%. *[-3 % YoY (postings index), Jun 2026]* — agrees; reproducible: partly; verified: primary.
  - Confirms the literature report's 'June IT -3%'. May 2026 was -8% (log). IT postings swung between -8% and +10% in 2026, a noisy series.

**Naukri JobSpeak (Sep 2026)** — Info Edge / Naukri (2026), Naukri JobSpeak Index, monthly reports Jan, Feb, Jun, Sep 2026. <https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-September-2026.pdf>

- `HIR-10c` Latest month: IT-Software postings were down 4% YoY in Sep 2026 (index 3,432 vs 3,585); overall postings +2%; fresher (0-3 yrs, all industries) +1%; AI/ML roles +20%. *[-4 % YoY (postings index), Sep 2026]* — agrees; reproducible: partly; verified: primary.
  - Naukri 0-3 band positive every month of 2026 (to +1% in Sep) while foundit fresher postings turned negative from Mar 2026; the portals diverge by 15-25 pts a month (fresher_thirdparty/FINDINGS.md). || Original verification note: C4/C2 support: IT is among the weakest sectors; fresher posting growth slowed from +17% …

**LinkedIn Grad's Guide (2026)** — Srivastava, Samriddhi (2026), 'Entry-level hiring climbs 168% as AI roles and internships gain ground: LinkedIn', People Matters, 17 Apr 2026 (LinkedIn Grad's Guide 2026). <https://peoplematters.in/news/strategic-hr/entry-level-hiring-climbs-168percent-as-ai-roles-and-internships-gain-ground-linkedin-49290>

- `HIR-11a` LinkedIn reports India entry-level hiring up 168% from 2023 to 2025. *[168 % change (undefined), 2023-2025]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md): The source wording: for bachelor's holders, hiring into firms with 1-10 employees grew 64% 2023-25, 'while for the broader entry-level cohort, it grew 168%'. So the 168% is micro-firm (1-10 employee) hiring of entry-level LinkedIn members; not total …

**EY (unverified)** — Bhattacharya, Ananya (2026), 'Why Claude Cowork is a math problem Indian IT can't solve', Rest of World, 6 Feb 2026. <https://restofworld.org/2026/indian-it-ai-stock-crash-claude-cowork/>

- `HIR-13a` Claimed: EY says entry-level IT roles are down 20-25%. The Rest of World article does NOT mention EY or this figure. *[20-25 % decline (claimed)]* — agrees; reproducible: no; verified: not found.
  - Do not cite as EY. Correction to literature report: the cited source does not contain it. Aggregators attribute the 20-25% to a 2025 EY analysis (via Storyboard18) or to NASSCOM, inconsistently. No EY primary found. EY Economy Watch (May 2026) discusses AI and the IT workforce without this number (press only).

**EPFO payroll (gap)** — EPFO, Provisional Monthly Estimate of Payroll (industry x age-group tables); compiled by Dataful dataset 19334 (FY2019-20 to FY2025-26, updated 30 Mar 2026). <https://dataful.in/datasets/19334/>

- `HIR-14a` EPFO publishes monthly net payroll by industry and age band (<18, 18-21, 22-25, 26-28, 29-35, >35). The IT-related category is 'Establishments engaged in manufacture, marketing, servicing, usage of computers'. *[FY20-FY26 monthly]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, epfo/FINDINGS.md): Repo built the series from 66 EPFO PDFs (Wayback). IT heading = 'manufacture, marketing, servicing, usage of computers'; top-10 tables only, ages 18-28 only; big firms with own PF trusts may not be covered; first prints revised down a median 32%. Publication stopped after Sep …

**Quess Corp (2025)** — Quess Corp (2025), IT Workforce Trends in India 2025, as reported by Siasat/PTI, 22 Dec 2025. <https://www.siasat.com/india-sees-16-pc-growth-in-it-hiring-in-2025-report-3314848/amp/>

- `HIR-14b` Quess: IT job demand reached 1.8m roles in 2025 (+16%); GCC share of demand 27% (from 15%); entry-level just 15% of demand; mid-career (4-10 yrs) share up to 65% from 50%. *[15 % of IT job demand that is entry-level, 2025]* — complements; reproducible: no; verified: press.
  - Agrees with C4 (entry share low, mid-career up). Contradicts strict C3 (demand +16%), and backs the GCC shift. Built from secondary sources, method thin. No Quess or CIEL 2026 IT-specific report found. Quess (Aug 2025) said IT services hiring had been 'almost nil' for 6-7 quarters.

**Business Today (2026)** — Kelkar, N. (2026). 'IT industry likely to hire 135,000 employees in FY26, projects Nasscom'. Business Today, Feb 24, 2026. <https://www.businesstoday.in/amp/latest/corporate/story/it-industry-likely-to-hire-135000-employees-in-fy26-projects-nasscom-517760-2026-02-24>

- `IND-01i` Nasscom officials said overall campus hiring has fallen significantly compared with earlier years, and that much of the hiring growth comes from GCCs (no share given). *[FY26]* — agrees; reproducible: no; verified: press.
  - Supports C4 (entry rung) and qualifies C3 (GCCs carry the growth). No GCC share-of-hiring number found in any source opened. Entry-level section.

**Nasscom-Zinnov (2026)** — Nasscom & Zinnov (2026). Nasscom-Zinnov GCC Landscape Report 2026 ('The GCC Value Orbit'). Nasscom and Zinnov, with K Raheja Corp (May 2026; data as of March 2026). <https://media.zinnov.com/wp-content/uploads/2026/05/zinnov-nasscom-india-gcc-landscape-report-2026.pdf>

- `IND-02c` The report says the hiring slowdown spans all seniority levels and several GCCs have paused junior recruitment; redeployment is replacing recruitment. *[FY26]* — agrees; reproducible: no; verified: primary.
  - Strong support for C4 and for C3's 'GCC hiring not faster'. Page 9 (Theme 3, hiring model). Also: AI-focused skills rose 1.5pp as share of open roles in last 6 months; non-AI hiring shrank. Entry-level section, quote-worthy.

**Swarajya (2026)** — Swarajya Staff (2026). 'AI, data skills now drive two in three new GCC jobs in India as hiring rises 11 per cent'. Swarajya, Jul 2, 2026. <https://swarajyamag.com/economy/ai-data-skills-now-drive-two-in-three-new-gcc-jobs-in-india-as-hiring-rises-11-per-cent>

- `IND-02d` Press reports early-career talent at 30% of GCC hires and 4-10 years' experience at 56%, attributed loosely to the Nasscom-Zinnov 2026 report. *[30 % of GCC hires, 2026 (unclear)]* — complements; reproducible: no; verified: unverified (press-only).
  - Not found in the 26-page Zinnov PDF (summary version); article mixes several sources (Business Today, ORF, TechRepublic) and gives no period. Also claims GCCs added ~200k net in FY26 vs 110k by IT services firms (unsourced). Do not cite without the full report.

**Future of India Foundation (2026)** — Future of India Foundation [unsigned; same text posted by Ruchi Gupta on her Substack 6 Oct 2026] (2026), 'IT Sector Helped Build the Indian Middle Class. For Its Workers, It Is Starting to Sputter', India After Liberalisation series Part 5, YouthPOWER / Future of India Substack, Oct 2. <https://foifaction.substack.com/p/it-sector-helped-build-the-indian>

- `JRN-01a` The share of salaried graduates aged 21-25 who work in IT fell from 20.0% to 15.8%. *[20.0 -> 15.8 % of salaried graduates aged 21-25, 2022-23 to 2025]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_entry_level.md): Ours 20.4% -> 16.0% (SE 1.5/1.0). Robust, but it is about the denominator: salaried graduates aged 21-25 in IT are flat (9.5 -> 9.95 lakh, 2022-23 to CY2025) while all salaried graduates 21-25 rose 46.8 -> 62.0 lakh. IT stopped absorbing growing supply; …
- `JRN-01e` Salaried IT graduates aged 21-25 are down about 10% from their 2023-24 peak, those aged 30+ are down 6.5% from 2022-23, and those aged 26-29 are down less than 1%. *[-10 / -6.5 / <-1 % change from peak, peak to 2025]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md): 'Peaked' not robust: all-ages salaried-graduate IT jobs 47.9 lakh (2023-24 ex cluster) vs 47.0 (CY2025); ages 21-25 10.3 vs 9.95 lakh, about -3%. || Original verification note: C4: the youngest group took the largest fall.

**Sidhant (2026)** — Aman Kai Sidhant (2026), 'India's $300B AI Shock', india300.ai, Jun 18. <https://india300.ai/>

- `JRN-02c` Fresher hiring at the top 5 IT firms went from about 180k at the FY22 peak to about 60k in FY25, then about 90k in FY26, with about 70k projected for FY27. TCS's FY27 fresher target is 25k, down from 44k in FY26. *[180k -> 60k -> 90k freshers hired, FY22-FY27]* — agrees; reproducible: partly; verified: press.
  - CORRECTED (repo check, fresher_thirdparty/FINDINGS.md): Our filings: TCS+Infosys+HCL fresher hires 218k (FY22) -> 65k (FY25) -> 76k (FY26); top-6 86k (FY25), 91k (FY26). Direction matches; Sidhant's levels are not reproducible from his sources. || Original verification note: C4. Compiled from company commentary and …

**Mint via People Matters (2026)** — Samriddhi Srivastava (2026), 'Infosys sees lowest proportion of under-30 employees in 15 years', People Matters, Jun 1 (reporting a Mint analysis of Infosys annual filings). <https://www.peoplematters.in/news/business/infosys-sees-lowest-proportion-of-under-30-employees-in-15-years-50011>

- `JRN-06a` Infosys staff aged 30 or under fell to 50.7% of 328,594 employees at end-FY26, from 53% in FY25 and about 60% in FY22, the lowest in at least 15 years; the 31-50 share rose to 45.7%. *[50.7 % of employees aged <=30, FY26]* — agrees; reproducible: yes; verified: press.
  - Duplicate of HIR-03c / HIR-09a (Infosys under-30; primary in HIR-09a). C4 (under-30 share falling at firms). Comes from Infosys annual report / BRSR age bands, so we can reproduce it. Earlier Mint (via The Wire): TCS India staff under 30 fell from 59% (FY22) to 47.7% (FY25). FY25 Infosys is given as 52% in one source …

**EPFO net payroll (2019-2025)** — Employees' Provident Fund Organisation, 'Net Payroll Data EPFO', monthly releases Jul 2019-Aug 2025 (66 reports, retrieved via Wayback Machine); repo tabulation data/explore/health_check/epfo/. <https://www.epfindia.gov.in/site_en/Estimate_of_Payroll.php>

- `REP-01a` Net payroll additions aged 18-25 under EPFO's computers/IT establishment heading fell from 366k (FY22) to 289k, 210k and 251k (FY25), -31%, the largest fall among top-10 industries; IT's share of all 18-25 net additions fell 5.8% -> 3.9%. *[-31 % change in net payroll additions, ages 18-25, FY22-FY25]* — agrees; reproducible: yes; verified: primary.
  - C4 (and C3). Entry-level section chart. Caveats: net payroll is a flow not headcount; top-10-industry tables only; IT heading is EPFO's own (not NIC); firms with own PF trusts (several big IT firms) may be excluded; Apr-Jun FY26 IT 18-25 75k, +3% YoY but -26% vs FY23 (like-for-like August releases). EPFO stopped …
- `REP-01b` Net payroll additions under the IT heading aged 22-25 fell 238k -> 152k (-36%) and aged 26-28 70k -> 24k (-66%) FY22-FY25, while all-industry 18-25 additions were flat (6.37m both years) and 18-25 new subscribers rose 8%. *[-36 % change, IT ages 22-25, FY22-FY25]* — agrees; reproducible: yes; verified: primary.
  - C4. Shows the IT weakness is not a shortage of young formal entrants. Monthly first prints are revised down a median 32%; use annual frozen totals. Source: epfo/FINDINGS.md

**Xpheno via press (Oct 2026)** — Xpheno, Active Tech Jobs Outlook, Oct 2026, as reported in Indian business press (multiple outlets); compiled in repo fresher_thirdparty/fresher_thirdparty_long.csv and postings/press_datapoints.csv. (URL in repo CSV)

- `REP-03a` Active tech openings rebounded to 120-123k in Oct 2026 (18-month high, +15-17% YoY); IT-services openings 66k (+57% YoY); entry-level (0-2 yrs) openings ~15k (+15% YoY), but the entry-level share of openings is 12.2% vs 16.1% in Jun 2025. *[12.2 % of active tech openings that are entry-level, Jun 2025-Oct 2026]* — complements; reproducible: no; verified: press.
  - C4 counter-signal: rung narrowing shows in share, not count, by H2 2026. Openings not hires; agency postings excluded. URLs in repo CSVs. Source: fresher_thirdparty/FINDINGS.md; postings/FINDINGS.md

**HAN Digital via ET (2026)** — HAN Digital estimate, as reported in The Economic Times, 14 Oct 2026; compiled in repo fresher_thirdparty/fresher_thirdparty_long.csv. (URL in repo CSV)

- `REP-04a` IT-BPM (incl. GCCs and BPO) fresher hiring fell from about 400k in FY22 to about 175k in FY26 (estimate) and could reach up to 210k in FY27 (+20%), ~60% at IT services and 28% at GCCs. *[175000 fresher hires (persons), FY22-FY27]* — complements; reproducible: no; verified: press.
  - C4: confirms a large fall from peak (-56%) but a partial recovery since FY24. No published method; scope wider than Xpheno; most recent sector estimate. Source: fresher_thirdparty/FINDINGS.md

**ICRIER (2026)** — Mishra, D., Kedia, M., Reddy, A., Fernandez, C. & Khanduri, A. (2026). AI and Jobs: This Time Is No Different - A Case Study of India's IT Sector. ICRIER, New Delhi (February). Supported by OpenAI. <https://www.icrier.org/pdf/AI-and-Jobs.pdf>

- `TT-01a` Survey of 651 IT firms (IT services, products, BPM, ER&D/GCCs, startups) in 10 Indian cities, fielded Nov 2025-Jan 2026 (72% in person), about 10% response rate; authors say not fully representative. *[651 firms, 2025-11 to 2026-01]* — complements; reproducible: no; verified: primary.
  - Methods: Section 3 p.13 and Appendix. Funded/supported by OpenAI (acknowledgements; figures sourced 'ICRIER-OpenAI survey'). Direction-of-change questions, not magnitudes. Cite as a methods caveat wherever ICRIER numbers are used.
- `TT-01c` Entry level: 55% of firms report a decline in entry-level employment over the last 24 months, 35% an increase. *[55 % of firms, last 24 months to Nov 2025-Jan 2026]* — agrees; reproducible: no; verified: primary.
  - Section 4.1, p.16, Figure 1 right panel. Supports C4. Caveat: the question asks about change in employment by level over 24 months, not hiring specifically and not explicitly attributed to AI; secondary sources describe it as 'entry-level hiring'. Entry-level section.
- `TT-01d` Mid level: 42% of firms report increased mid-level employment, 33% no change, 25% a decline. *[42 % of firms, last 24 months to Nov 2025-Jan 2026]* — agrees; reproducible: no; verified: primary.
  - Section 4.1, p.16, Figure 1 right panel. Fits C4 (rung narrowing at the bottom, demand for experienced staff).
- `TT-01e` Senior level: 82% of firms report no change in senior-level employment. *[82 % of firms, last 24 months to Nov 2025-Jan 2026]* — complements; reproducible: no; verified: primary.
  - Section 4.1, p.16. Entry-level section.

**Mahambare, Jadhav & Venugopalan (2026)** — Mahambare, V., Jadhav, V. & Venugopalan, V. (2026). AI, Automation and India's Workforce: Who Gains, Who's Exposed, and How Policy Can Shape the Future. Great Lakes CFER White Paper WP 5, Great Lakes Institute of Management, Chennai (October). <https://greatlakes.edu.in/chennai/assets/greatlakes/images/GLCFER-WP5.pdf>

- `TT-07a` PLFS 2025: 39.4% of employed 15-24-year-olds are in high-routine occupations (vs 24.2% for 55-64); 55.0% of urban 15-24s. *[39.4 % of employed aged 15-24, 2025]* — complements; reproducible: yes; verified: primary.
  - WP5 pp.5, 7, 17 (Fig. 3). Economy-wide occupation exposure, not IT. Foreword by CEA. Context for entry-level section.
- `TT-07b` PLFS 2025: among young adults (20-29) with engineering degrees, 25% were unemployed; graduate unemployment at 20-29 is more than twice the overall rate. *[25 % unemployment rate, 2025]* — complements; reproducible: yes; verified: primary.
  - WP5 p.5. Cross-check with our PLFS graduate tabulations (C4). No IT-specific (NIC 62/63) employment numbers in the paper. 34.2m workers (5.6%) in exposed 'balance open' occupations incl. ICT professionals.

**Azim Premji University (2026)** — Centre for Sustainable Employment, Azim Premji University (2026). State of Working India 2026, Executive Summary (March 16). <https://azimpremjiuniversity.edu.in/media/resources/SWI/SWI-2026/Executive-Summary_SWI2026-16-March.pdf>

- `TT-08a` Graduate unemployment is nearly 40% among 15-25-year-olds and 20% among 25-29-year-olds; 40% of graduates in the labour force report open unemployment, a rate roughly unchanged at 35-40% since 1983. *[40 % unemployment rate (graduates aged 15-25), 2023-24]* — complements; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_entry_level.md): Our PLFS 2023-24, graduates 15-25: principal status 41.2%, weekly 38.2%, official ps+ss 34.5%. SWI's ~40% most likely uses principal status. Rates have fallen since 2017-18 (46-48%); the further CY2025 fall shows only on usual status (28% ps+ss, ages …
- `TT-08b` Of young graduate men who report being unemployed, about half find work within a year but only ~7% (6.7%) find permanent salaried work. *[6.7 % finding permanent salaried work within a year, CMIE-CPHS pooled panel]* — complements; reproducible: no; verified: primary.
  - CMIE CPHS-based; cite as SWI/CMIE only (cannot reproduce). || Original verification note: Exec summary p.17 (Table 6.5). Conditional on reporting unemployed, not 'within a year of graduation' as press says. CMIE CPHS (we lack it).

**World Bank (2025)** — World Bank. 2025. South Asia Development Update, October 2025: Jobs, AI, and Trade. Ch. 2 'Artificial Intelligence, Real Impact' by P. Kirby, J. Rexer, S. Sharma. Washington, DC (Oct 7). <https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf>

- `WB-01d` Entry-level postings in jobs as exposed as software developers grew 21% more slowly than for electrician-level exposure; senior roles showed no change; secondary-education postings fell 24% across the IQR of exposure, while degree jobs were unchanged. *[-21 % (entry-level postings, software-dev vs electrician exposure), post-Nov 2022, through Mar 2025]* — agrees; reproducible: no; verified: primary.
  - Repo extracted the chart workbook: posting effect per +1 sd AI exposure after ChatGPT: 0-5 yrs -11.9% (+/-4.7), 5-10 yrs -3.2%, 10-15 yrs +3.1%; Annex A2.12 coef -0.290 (s.e. 0.058) for 0-5 yrs (postings/FINDINGS.md). Lightcast South Asia skews professional; postings not hires; ends Mar 2025. || Original verification …

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03d` Cites ICRIER survey of 651 IT firms: no fall in aggregate employment with GenAI, but 55% of firms report lower entry-level hiring vs 25% mid-level and 14% senior. *[55 % of firms reporting lower entry-level hiring, survey 2025-26]* — agrees; reproducible: no; verified: primary.
  - C4. p.42 (PDF p.44); cites Mishra, Kedia, Reddy, Fernandez & Khanduri (2026) 'AI and Jobs: This Time Is No Different', ICRIER. The secondary citation is confirmed. ICRIER also says aggregate employment did not fall (tension with C2/C3 at sector level).

## Pay

**Future of India Foundation (2026)** — Future of India Foundation [unsigned; same text posted by Ruchi Gupta on her Substack 6 Oct 2026] (2026), 'IT Sector Helped Build the Indian Middle Class. For Its Workers, It Is Starting to Sputter', India After Liberalisation series Part 5, YouthPOWER / Future of India Substack, Oct 2. <https://foifaction.substack.com/p/it-sector-helped-build-the-indian>

- `JRN-01f` Median real monthly earnings of IT workers rose from about Rs 35,700 to Rs 40,000 by 2025, after peaking in 2023-24. *[35700 -> 40000 Rs per month, 2025 prices (CPI-C), 2017-18 to 2025]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_entry_level.md; labour_share/FINDINGS.md): Medians reproduced (36.1k -> 40.0k; age 21-25 Rs 28k vs 30+ Rs 45k exact), but medians are heaped at round numbers. Real MEAN for all IT workers is flat (51.0k -> 49.5k); for ages 21-25 the real mean fell 35.2k -> 30.9k (-12%, …

**Parth MN (2026)** — Parth MN (2026), 'Death of an Indian tech worker', Rest of World, Jan 27. <https://restofworld.org/2026/india-tech-workers-crisis-suicide/>

- `JRN-04c` Worker-distress reporting: 227 reported suicides of Indian tech workers 2017-2025 (Rest of World count of local news); entry-level pay at the top 5 firms rose less than 10% in 15 years (Careers360). *[10 % nominal rise in entry-level pay over 15 years, c.2010-2025]* — complements; reproducible: partly; verified: press.
  - C4/pay context. The Careers360 entry-salary stat is secondary; we could check it against firm fresher CTC disclosures. Mostly human-interest; low priority.

**Azim Premji University (2026)** — Centre for Sustainable Employment, Azim Premji University (2026). State of Working India 2026: Youth in the Labour Market - Pathways from Learning to Earning. Bengaluru (March). <https://publications.azimpremjiuniversity.edu.in/6848/1/SWI%202026%20-%20Web.pdf>

- `TT-08c` Computer and information services has become a major employer of young (20-29) graduate men and women by 2023; report also finds entry-level salary growth for young graduate men has slowed. *[1983 to 2023-24]* — agrees; reproducible: yes; verified: primary.
  - Report pp.20, 85-89, 97-101 (Figs 3.5-3.6, section 3.6). Supports C4 pay finding qualitatively; we can reproduce from PLFS. Notes AI's effect on entry-level salaried jobs is 'uncertain'.

**World Bank (2025)** — World Bank. 2025. South Asia Development Update, October 2025: Jobs, AI, and Trade. Ch. 2 'Artificial Intelligence, Real Impact' by P. Kirby, J. Rexer, S. Sharma. Washington, DC (Oct 7). <https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf>

- `WB-01b` Posted wages in business-services occupations fell about 8% relative to other occupations after ChatGPT. *[-8 % relative to other occupations (log points -0.080), Aug 2020-Mar 2025]* — agrees; reproducible: no; verified: primary.
  - C4 (pay). p.38; Annex Table A2.10 p.55 (col 5 = -0.080; -0.047 with AIOE control). Posted salaries in Lightcast, not realised pay. It sits beside our PLFS relative-pay result.

## Prices and AI deflation

**Nasscom (2026)** — Nasscom (2026). Technology Sector in India: Strategic Review 2026 - 'Steering through the tides of uncertainty: charting opportunities amid disruption'. New Delhi: Nasscom (released Feb 24, 2026; full report paid). <https://nasscom.in/knowledge-center/publications/technology-sector-india-strategic-review-2026>

- `IND-01g` Nasscom says FY27 hiring will shift from volume to skill mix, reflecting greater AI-driven productivity gains passed through to clients. *[FY27 outlook]* — agrees; reproducible: no; verified: primary.
  - Supports model assumption that AI productivity is passed to clients as lower prices (deflation). Also C4 (less volume hiring). Prices section / model motivation.

**Kotak Institutional Equities (2026a)** — Kotak Institutional Equities (2026). Indian IT services sector note (post Q4FY26 results). Reported by ANI, Apr 29, 2026 (The Tribune; webindia123). <https://www.tribuneindia.com/news/business/it-services-growth-to-stay-range-bound-at-3-per-cent-as-ai-deflation-pressures-margins-mid-tiers-better-placed-says-kotak/>

- `IND-03b` Kotak's industry base case is 3.5% AI-led pricing erosion, appearing first in renewals of large multi-year contracts; it calls GenAI deflation cyclical (a 2-3 year phase), not secular. *[3.5 % price deflation per year, FY27 onward]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Gross forecast; unit and horizon unstated in coverage. Our M2 measured AI-specific give-back: 0.43% FY26 (range 0.01-1.32), 1.51% expected FY27; gross incl. usual ~1.55%/yr pre-AI give-back 1.98% / 3.06%. Cite as a forecast, not a measured price change. || …

**Kotak Institutional Equities (2026b)** — Kotak Institutional Equities (2026). Q1FY27 IT services review. Reported by ANI, Aug 7, 2026 (NewKerala). <https://www.newkerala.com/news/a/ai-led-deflation-weak-demand-keep-it-sector-growth-358.htm>

- `IND-03d` Kotak expects ~0-2% q/q growth for Tier-1 IT in Q2FY27, says headwinds fall largely on incumbents, and that base-business deflation will more than offset AI revenue tailwinds near to medium term. *[0-2 % q/q revenue growth, Q2FY27E]* — agrees; reproducible: no; verified: press.
  - C1/C2. Also notes margins protected via layoffs, delayed/lower wage hikes and reduced variable pay (no numbers) - relevant to pay section. No deflation % in this note.

**Kotak Institutional Equities (2026c)** — Kotak Institutional Equities (2026). Q2FY27 IT services preview. Reported by ANI, Sep 30, 2026 (NewKerala). <https://www.newkerala.com/news/a/ai-deflation-weak-demand-keep-large-it-growth-314.htm>

- `IND-03e` Kotak estimates gross AI-led deflation of ~7% and net deflation of 3.5% for IT companies, with muted Tier-1 growth in Q2FY27 and mid-tiers outperforming. *[7 (gross) / 3.5 (net) % revenue deflation, FY27E]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Gross vs net forecasts; compare with our measured AI-specific 0.4% (FY26) / ~1.5% (FY27). || Original verification note: Useful for model: gross vs net (after new AI work) deflation split. Broker model. Prices section.

**J.P. Morgan (2026)** — J.P. Morgan (2026). Indian IT services sector note (late June 2026). Reported in Nahar, P.K., 'TCS, Infosys, Wipro, HCL Tech: Top-5 IT stocks' m-cap slips to RIL as AI disruption bites', Business Today, Jul 4, 2026; and People Matters, Jun 30, 2026. <https://www.businesstoday.in/markets/stocks/story/indian-it-stocks-fall-tcs-infosys-wipro-hcl-tech-reliance-market-cap-ai-impact-540988-2026-07-04>

- `IND-04b` J.P. Morgan says AI deflation is only in its second year and expects further headwinds over the next two years; large caps to hover around 3-4% growth rather than return to mid-single digits. *[3-4 % medium-term revenue growth (large caps), medium term (to ~FY30)]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Coverage gives no numeric deflation rate, only 2-3% growth now and 3-4% medium term. || Original verification note: Model context: deflation phase where productivity gains cut demand faster than new AI spend. Wire copies add recovery not expected until FY30 …

**ICICI Securities (2026)** — ICICI Securities (2026). Indian IT Sector Analysis 2026: Valuation, Growth, AI Risks and Top Picks. ICICIdirect Research (Mar 30, 2026). <https://www.icicidirect.com/research/equity/finace/indian-it-sector-analysis-2026-valuation-growth-ai-risks-and-top-picks>

- `IND-05a` ICICI Securities expects AI to deflate traditional IT services revenue by about 2-3% a year, peaking FY26-FY28, with recovery from end-FY28 or FY29. *[2-3 % revenue deflation per year, FY26-FY28]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): Applies to ~30% of revenue (traditional services), i.e. 0.6-0.9 pp of the whole portfolio a year, close to our M2 FY27 estimate. || Original verification note: Broker's own published research page (opened). Model parameter range. Prices section.
- `IND-05b` About 30% of IT services is at risk from AI; base case (50% deflation of that segment) implies a ~USD 40bn hit to India, worst case (100% loss) USD 80-85bn. *[40 (base) / 80-85 (worst) USD bn revenue at risk, to ~FY29]* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): The $40bn base case assumes 50% deflation of the at-risk 30% segment; a scenario, not an estimate. || Original verification note: Explicit sizing; base on ~USD 280-285bn Indian IT industry. Ignores demand response (elasticity) - useful contrast with our model. …

**BNP Paribas (2026)** — Rakesh, K. (BNP Paribas) (2026). Indian IT 'AI-led deflation' note; reported in Verma, I., 'BNP Paribas: AI-led deflation pressures Indian IT sector', Whalesbook, Oct 2, 2026. <https://www.whalesbook.com/news/English/brokerage-reports/BNP-Paribas-AI-Led-Deflation-Pressures-Indian-IT-Sector/6abf2f9d5aacb956d08943cc>

- `IND-07a` BNP Paribas says GenAI is reducing demand for large labour-intensive teams, firms are passing productivity gains to clients, and large caps are more exposed via legacy contracts; decoupling revenue from headcount is the key monitorable. *[2026]* — agrees; reproducible: no; verified: unverified (press-only).
  - Qualitative only; single low-quality aggregator; no better coverage (ET/Mint/Moneycontrol) found before search budget ran out. Optional footnote at most.

**HCLTech (2026)** — HCL Technologies (2026). Q4 FY26 earnings conference call transcript, Apr 21, 2026 (filed with NSE/BSE Apr 24, 2026). <https://nsearchives.nseindia.com/corporate/HCLTECH_24042026174011_TranscriptEarningsCall.pdf>

- `IND-08a` HCLTech CEO says ~40% of the industry (app dev/support, traditional infra ops, customer support) is AI-disrupted and can shrink at a 3-5% CAGR for a few years; for HCLTech's mix this is 2-3%. *[3-5 (segment) / 2-3 (HCLTech) % CAGR shrink, FY27 onward, 'a few years']* — complements; reproducible: no; verified: primary.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): 3-5%/yr applies to AI-disrupted services only (= 2-3% of HCLTech's portfolio), from FY27. Forecast, not measured. || Original verification note: Discrepancy: Kotak/press report '3-5% for the industry'; the transcript applies 3-5% only to the 40% AI-disrupted …
- `IND-08b` HCLTech says the deflation is incremental to traditional productivity commitments and that very little has played out in reported numbers; it expects it in FY27 onward. *[FY26 vs FY27+]* — complements; reproducible: no; verified: primary.
  - Important for interpreting C2: management says FY24-26 stagnation is NOT mainly AI deflation (demand weakness). An analyst on the call noted renewals already carried 10-15% price cuts over deal life pre-AI. Prices section / caveat on attributing C2 to AI.

**Jefferies (2026)** — Jefferies (2026). Indian IT sector downgrade note on AI risks (Feb 2026); reported in '5paisa: Jefferies downgrades Infosys, TCS and peers amid AI concerns; trims FY26-28 estimates', Feb 24, 2026. <https://www.5paisa.com/index.php/news/jefferies-downgrades-infosys-tcs-and-peers-amid-ai-concerns-trims-fy26-28-estimates>

- `IND-08d` Jefferies says application managed services (22-45% of revenue at several firms) could see sharp AI deflation; in its worst case FY26-31 revenue CAGR is 3pp lower (~15% cumulative deflation) with no growth after FY31. *[15 % cumulative revenue deflation (worst case), FY26-FY31]* — complements; reproducible: no; verified: press.
  - Upper-bound scenario for model. Single secondary source (5paisa). Prices section.

**NITI Aayog (2025)** — NITI Aayog (with NASSCOM and BCG) (2025). Roadmap for Job Creation in the AI Economy. NITI Frontier Tech Hub, New Delhi (October). <https://niti.gov.in/sites/default/files/2025-10/Roadmap_for_Job_Creation_in_the_AI_Economy.pdf>

- `TT-04b` Assumes IT services industry revenue grows 3-9% a year and price-per-FTE grows 5-8% a year, so headcount implied roughly flat to modestly growing. *[5-8 % per year price per FTE, next few years from 2025]* — complements; reproducible: no; verified: primary.
  - p.22 (pdf). Directly relevant to our model: rising revenue per FTE means headcount growth ~ revenue growth minus 5-8pp. Contrasts with our AI price-deflation assumption (they assume price per FTE rises). Prices/model section.

**Betai & Chen (2026)** — Betai, Neha, and Maggie Chen (George Washington University). 2026. 'Automation without Borders: Generative AI and Cross-Border Service Outsourcing.' Slides, Fourth Annual AI in Action Conference, Georgetown-World Bank (Jan 26). <https://thedocs.worldbank.org/en/doc/2770aa5def57e42a6d2449c90d6cf974-0070062026/original/10-Chen.pdf>

- `WB-05b` Continuing workers' average contract value rose 41% and the top 1% captured a 17-20 pp larger share of jobs and earnings: fewer but higher-value tasks. *[41 % rise in avg contract value (continuing workers), Jan 2022-Dec 2024]* — complements; reproducible: no; verified: primary.
  - Mixed signal for the price model: task upgrading rather than price deflation. Slide 6.

## AI productivity and capability

**Humlum & Vestergaard (2026)** — Humlum, A. & Vestergaard, E. (2026). Still Waters, Rapid Currents: Early Labor Market Transformation under Generative AI. NBER Working Paper 33777, May 2025, revised March 2026 (previously titled 'Large Language Models, Small Labor Market Effects'). <https://www.nber.org/system/files/working_papers/w33777/w33777.pdf>

- `ACA-03c` Adopters report average time savings of about 3% of work hours (Appendix; earlier 2025 version reported 2.8%). *[3 % of work hours, 2023-2024 surveys]* — complements; reproducible: no; verified: primary.
  - Input for replacement-rate prior (small realised time savings). Self-reported; coded from bins.

**Stanford AI Index (2026)** — Stanford HAI (2026). Artificial Intelligence Index Report 2026, Chapter 4: Economy. Stanford Institute for Human-Centered AI, April 2026. <https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf>

- `ACA-05e` Micro studies summarised: customer support +14-15% issues/hour, software developers +26% pull requests (Cui et al.), marketing +50% output per worker; less experienced workers benefit most. *[26 % more pull requests (Copilot), 2023-2025 studies]* — complements; reproducible: no; verified: primary.
  - Secondary compilation; cite underlying studies (ACA-07*).

**Becker et al. (2025)** — Becker, J., Rush, N., Barnes, E. & Rein, D. (2025). Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. METR, arXiv:2507.09089, July 2025. <https://arxiv.org/abs/2507.09089>

- `ACA-06a` RCT with 16 experienced open-source developers on 246 tasks: AI tools increased completion time by 19%, although developers forecast a 24% speedup and afterwards believed 20%. *[19 % slower (completion time increase), Feb-Jun 2025]* — complements; reproducible: no; verified: primary.
  - Caveat for replacement-rate prior; METR now labels it historical. Experts forecast 38-39% speedup.

**METR (2026)** — Becker, J., Rush, N., Cunningham, T., Rein, D. & Mahamud, K. (2026). We are Changing our Developer Productivity Experiment Design. METR blog, February 24, 2026. <https://metr.org/blog/2026-02-24-uplift-update/>

- `ACA-06b` Late-2025 follow-up: returning developers -18% time with AI (speedup; 95% CI -38% to +9%, n=10), newly recruited -4% (CI -15% to +9%, n=47); METR calls the data unreliable due to selection (devs refusing no-AI work, 30-50% withholding tasks). *[-18 % change in completion time (negative = speedup), Aug 2025-early 2026]* — complements; reproducible: no; verified: primary.
  - No pooled estimate; neither CI excludes zero. Do not cite as 'METR reversed to 18% faster' without caveat. METR's informal view: developers likely more sped up in early 2026 than early 2025.
- `ACA-06d` Updated suite: doubling time 196.5 days for the stitched 2019+ trend, 130.8 days (95% CI 107-161) since 2023, 88.6 days since 2024; top model Claude Opus 4.5 at 320 min (CI 170-729). *[131 days (doubling time since 2023), 2019-Jan 2026]* — complements; reproducible: no; verified: primary.
  - Faster recent doubling (~4 months) relevant to scenario for AI replacement rate.
- `ACA-06e` Public frontier 50% time horizon about 12 hours (range 5-61); internal frontier at least 16 hours (point estimate 16-20); suite saturated and cannot measure above ~16 hours reliably. *[12 hours (50% time horizon, public frontier), Feb-Mar 2026]* — complements; reproducible: no; verified: primary.
  - METR time-horizons page lists Claude Mythos Preview (May 8 2026) as latest and says page no longer actively updated. Benchmark tasks are software/ML; not workplace productivity.

**Kwa et al. (2025)** — Kwa, T., West, B., et al. (2025). Measuring AI Ability to Complete Long Software Tasks (orig. 'Measuring AI Ability to Complete Long Tasks'). METR, arXiv:2503.14499, March 2025 (v4 July 2026). <https://arxiv.org/abs/2503.14499>

- `ACA-06c` The 50% task-completion time horizon of frontier AI has doubled roughly every 7 months since 2019; Claude 3.7 Sonnet about 50 minutes. *[7 months (doubling time), 2019-2025]* — complements; reproducible: no; verified: primary.
  - Context for speed of AI replacement-rate growth; external validity limited.

**Peng et al. (2023)** — Peng, S., Kalliamvakou, E., Cihon, P. & Demirer, M. (2023). The Impact of AI on Developer Productivity: Evidence from GitHub Copilot. arXiv:2302.06590, February 2023. <https://arxiv.org/abs/2302.06590>

- `ACA-07a` Lab RCT: developers with GitHub Copilot completed an HTTP-server task in JavaScript 55.8% faster than controls. *[55.8 % faster, 2022]* — complements; reproducible: no; verified: primary.
  - Upper-bound style lab estimate; single task; authors include GitHub/Microsoft staff.

**Cui et al. (2026)** — Cui, K. Z., Demirer, M., Jaffe, S., Musolff, L., Peng, S. & Salz, T. (2026). The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers. Management Science, published online Feb 27, 2026, doi:10.1287/mnsc.2025.00535. <https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf>

- `ACA-07b` Pooled field RCTs at Microsoft, Accenture and a Fortune 100 firm (4,867 developers): Copilot access raised completed pull requests 26.08% (SE 10.3%); commits +13.55%, builds +38.38%; less experienced developers gained more. *[26.08 % more completed tasks (pull requests), 2022-2023]* — complements; reproducible: no; verified: primary.
  - Numbers from Feb 2025 MIT draft; publication confirmed via Crossref (journal page blocked). Accenture is an IT-services firm -- relevant to Indian IT. Junior gains larger.

**Brynjolfsson, Li & Raymond (2025)** — Brynjolfsson, E., Li, D. & Raymond, L. (2025). Generative AI at Work. Quarterly Journal of Economics 140(2): 889-942, doi:10.1093/qje/qjae044. <https://arxiv.org/abs/2304.11771>

- `ACA-07c` AI assistant for 5,172 customer-support agents raised issues resolved per hour by 15% on average; lowest-skill quintile gained about 36% and the most skilled saw no gain. *[15 % more resolutions per hour, 2020-2021]* — complements; reproducible: no; verified: primary.
  - BPO benchmark. DISCREPANCY: the 14% average / 34% novice figures are from the 2023 NBER working paper (w31161); the published/arXiv v2 version says 15% and 36% (lowest skill quintile). Cite the published numbers.

**Dell'Acqua et al. (2023)** — Dell'Acqua, F., McFowland III, E., Mollick, E., Lifshitz-Assaf, H., Kellogg, K., Rajendran, S., Krayer, L., Candelon, F. & Lakhani, K. (2023). Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality. Harvard Business School Working Paper 24-013, September 2023. <https://www.hbs.edu/faculty/Pages/item.aspx?num=64700>

- `ACA-07d` 758 BCG consultants: inside the AI frontier, GPT-4 users completed 12.2% more tasks, 25.1% faster, with >40% higher quality; on a task outside the frontier they were 19 pp less likely to be correct. *[12.2 % more tasks, 2023]* — complements; reproducible: no; verified: press.
  - Could not open HBS/SSRN (403); numbers from multiple secondary summaries and author's blog. WP number 24-013 not confirmed from primary.

**Unearthinsight via AIM (2026)** — Rag, Ajay (2026), 'Indian IT's Revenue Per Employee is Rising. But is AI Getting Too Much Credit?', Analytics India Magazine, 21 Aug 2026 (Unearthinsight data). <https://analyticsindiamag.com/it-services/indian-its-revenue-per-employee-is-rising-but-is-ai-getting-too-much-credit>

- `HIR-12a` Unearthinsight: revenue per employee grew slowly FY19-FY26 (CAGR TCS 0.59%, $49,290->$51,353; Infosys 2.47%; HCL 0.45%; TechM 0.75%; Wipro -1.45%, $45,144->$40,763). *[0.59 % CAGR revenue per employee (TCS), FY19-FY26]* — complements; reproducible: yes; verified: press.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): TCS, Infosys, HCLTech and TechM CAGRs reproduced exactly from FY USD revenue / FY-end headcount; Wipro differs (ours -1.28%/yr vs -1.45%). Top-six FY23-26 revenue per employee +3.6%/yr. || Original verification note: C1/C2: no big break in labour productivity …
- `HIR-12b` Gaurav Vasu (Unearthinsight) attributes about 60% of recent revenue-per-employee gains to workforce rationalisation and about 40% to AI-driven efficiency. *[60/40 % attribution, recent (FY26-Q1 FY27)]* — complements; reproducible: no; verified: press.
  - CORRECTED (repo check, contradictions/FINDINGS_output.md): The 60% 'from workforce cuts' does not hold for FY19-26 (top-six headcount rose 39 log points). For FY23-26, an accounting split gives ~33% from fewer heads (RPE +10.3 log pts = revenue +6.9 + headcount -3.4). The AI share is not identifiable from these data. …

**Nasscom (2026)** — Nasscom (2026). Technology Sector in India: Strategic Review 2026 - 'Steering through the tides of uncertainty: charting opportunities amid disruption'. New Delhi: Nasscom (released Feb 24, 2026; full report paid). <https://www.etvbharat.com/en/business/india-fy26-tech-revenues-hit-usd-315-billion-enn26022404879>

- `IND-01e` Nasscom estimates FY26 AI-related revenue at USD 10-12bn, the first time it has given such an estimate; it notes not all firms report AI revenue separately. *[10-12 USD bn, FY26E]* — complements; reproducible: no; verified: press.
  - Context for model (AI-native work offsetting deflation); roughly 3-4% of USD 315bn. Undefined metric. Business Today adds Nambiar said AI is at best 5-6% of topline. Prices/AI section.

**ICICI Securities (2026)** — ICICI Securities (2026). Indian IT Sector Analysis 2026: Valuation, Growth, AI Risks and Top Picks. ICICIdirect Research (Mar 30, 2026). <https://www.icicidirect.com/research/equity/finace/indian-it-sector-analysis-2026-valuation-growth-ai-risks-and-top-picks>

- `IND-05c` ICICI Securities sizes the incremental AI-led opportunity for IT services at USD 300-400bn by 2030. *[300-400 USD bn TAM, by 2030]* — complements; reproducible: no; verified: primary.
  - Offset side of the model (new demand). Global TAM, not India revenue. Page also cites '170m new / 92m displaced jobs' - that is WEF Future of Jobs, not ICICI; do not attribute.

**World Bank (2025)** — World Bank. 2025. South Asia Development Update, October 2025: Jobs, AI, and Trade. Ch. 2 'Artificial Intelligence, Real Impact' by P. Kirby, J. Rexer, S. Sharma. Washington, DC (Oct 7). <https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf>

- `WB-01f` By March 2025, 12% of business-services job postings required AI skills, vs 4% for other jobs, double pre-ChatGPT levels. *[12 % of postings requiring AI skills, Nov 2022 vs Mar 2025]* — complements; reproducible: no; verified: primary.
  - Context for AI adoption in the sector. p.38; Fig. 2.11B p.39. Annex Table A2.10 cols 1-2.

**World Bank (2026, SAEU Oct)** — World Bank. 2026. South Asia Economic Update, October 2026: Adopting AI for Growth. Washington, DC (Oct 6). GVC analysis draws on Chiplunkar et al. (2026). <https://documents.worldbank.org/curated/en/099552210132636511/pdf/IDU-c65c3333-7e66-4072-9ce4-05ce12d2f398.pdf>

- `WB-02f` 23.4% of Indian firms report using some form of AI vs 42.7% of US firms (World Bank Enterprise Survey AI module 2025-26); gap wider for sophisticated uses. *[23.4 % of firms using AI, 2025-26]* — complements; reproducible: no; verified: primary.
  - Context for AI-adoption pace (prices/deflation pass-through). p.52 (PDF p.72), Fig. 2.4. Same survey as the IDU '23%'.

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03a` Among formal Indian firms with at least five employees, 23% use AI; adjusted for sophistication, adoption is about one-third of the US level. *[23 % of formal firms (5+ employees), 2025 (WBES)]* — complements; reproducible: no; verified: primary.
  - Context. p.34 (PDF p.36). Source: World Bank Enterprise Survey 2025 AI module. AI agents/workflow automation about 10% in six developing economies incl. India vs 24% in the US.

## International benchmarks

**Brynjolfsson, Chandar & Chen (2025)** — Brynjolfsson, E., Chandar, B. & Chen, R. (2025). Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence. Stanford Digital Economy Lab working paper, August 26, 2025. <https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/>

- `ACA-01a` Early-career workers (22-25) in the most AI-exposed occupations saw a 13% relative employment decline after controlling for firm-level shocks (firm-time effects), ADP data through July 2025. *[-13 % relative employment decline, late 2022-Jul 2025]* — agrees; reproducible: no; verified: primary.
  - C4 benchmark. Regression estimate with firm-time FE; later versions replaced it as headline. Opened a third-party copy of the Aug 26 2025 PDF (Stanford URL now redirects to the 2026 version). US only, ADP proprietary.
- `ACA-01b` Employment of software developers aged 22-25 fell nearly 20% from its late-2022 peak by July 2025 (Section on case studies, Figure 1). *[-20 % vs late-2022 peak (approx.), late 2022-Jul 2025]* — agrees; reproducible: no; verified: primary.
  - C4; this is the origin of the 'young software developers ~-20%' figure later repeated by Stanford AI Index 2026. Not a trend-adjusted estimate.

**Brynjolfsson, Chandar & Chen (2026)** — Brynjolfsson, E., Chandar, B. & Chen, R. (2026). Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence. Stanford Digital Economy Lab working paper, August 2026 revision. <https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf>

- `ACA-01c` Employment of 22-25-year-olds in AI-exposed occupations is 19% below where it would be had it kept pace with less-exposed peers (ADP through June 2026); no comparable gap for experienced workers; gap widening since Aug 2025. *[-19 % below kept-pace counterfactual, Nov 2022-Jun 2026]* — agrees; reproducible: no; verified: primary.
  - C4 main US benchmark (abstract, fact 2). Descriptive, not causal. Same measure was 15% at the July 2025 vintage; earlier headline regression estimates were 13% (Jul 2025 data) and 16% (Sep 2025 data). Do not compare 19% with 13% as same metric.
- `ACA-01d` In levels, employment of 22-25-year-olds in the two most exposed quintiles fell about 11% while the three least-exposed quintiles grew about 10% (a 21 pp divergence); total 22-25 employment roughly flat (-1.9%). *[-11 % change in employment (levels), Nov 2022-Jun 2026]* — agrees; reproducible: no; verified: primary.
  - C4; useful levels framing parallel to 'output up, entry rung narrowing'. Section 1 / Fact 2 text.
- `ACA-01e` Most-exposed-quintile coefficient for ages 22-25 is -0.18 with no controls but halves to -0.09 (significant only at 10%) when occupational college share is controlled (Table 1, Panels A and C); patterns attenuate with education control, show some pre-trends, and are larger in ADP than in national surveys. *[-0.09 log-point/proportional change vs least-exposed quintile (with education control), Nov 2022-Jun 2026]* — agrees; reproducible: no; verified: primary.
  - Key caveat for citing C4 benchmark: education control halves the estimate; authors say the two estimates bracket a range. Also note ADP vs CPS discrepancy (Section 5).
- `ACA-01f` The divergence operates mainly through reduced hiring of young workers rather than increased separations, and adjustment is via employment not base pay; declines concentrated where AI usage substitutes rather than complements. *[Nov 2022-Jun 2026]* — agrees; reproducible: no; verified: primary.
  - C4 mechanism (facts 4-6). Parallels Indian firms' fresher-hiring slowdown rather than layoffs. Note: fact 6 (no pay adjustment) differs from our PLFS relative-pay decline (C4 pay) -- possibly complements/contradicts on the pay channel.

**Hosseini & Lichtinger (2026)** — Hosseini, S. M. & Lichtinger, G. (2026). Generative AI as Seniority-Biased Technological Change: Evidence from U.S. Resume and Job Posting Data. Working paper, version of May 6, 2026 (first version Aug 31, 2025; SSRN 5425555). <https://raw.githack.com/s-mahdihosseini/Website/b99fa2962dcc4c165bbc3c41dd283afa99c5ccfb/GenAI_SenBTC_May_2026.pdf>

- `ACA-02a` At GenAI-adopting firms, junior employment fell about 9% relative to non-adopters after six quarters from 2023Q1 (DiD and triple-difference), while senior employment showed no break. *[-9 % relative junior employment, 2023Q1-2024Q2 (six quarters)]* — agrees; reproducible: no; verified: primary.
  - C4 firm-level benchmark. Data: Revelio resumes, 65m workers, >280k firms, 2015-2025. Adopters = firms posting 'GenAI integrator' roles (3.7% of firms, 16% of employment). Earlier press reported 7.7% (Aug 2025 draft); the May 2026 headline is ~9%.
- `ACA-02b` Staggered event study: junior employment at adopters starts falling about two quarters after adoption and is about 8% lower after eight quarters, with no pre-trends. *[-8 % junior employment vs non-adopters, 8 quarters post adoption]* — agrees; reproducible: no; verified: primary.
  - C4; robustness to adoption timing.
- `ACA-02c` Junior employment in high-exposure occupations fell about 7% relative to low-exposure occupations within adopters vs non-adopters (2022Q4-2025Q1); decline driven mainly by reduced hiring, not separations (separations actually fell; promotions rose slightly). *[-7 % relative junior employment (high vs low exposure), 2022Q4-2025Q1]* — agrees; reproducible: no; verified: primary.
  - C4 hiring channel. Matches 'fewer fresher hires' story for Indian IT.
- `ACA-02d` By alma-mater prestige, the junior decline is U-shaped: mid-tier university graduates see the largest relative declines; elite and lowest-tier less affected (Supplemental Appendix A.19). *[2023-2025]* — complements; reproducible: no; verified: primary.
  - Parallel to NIRF tier analysis (C4). Result is in supplemental appendix, footnote 6 of May 2026 version; no single headline magnitude in main text.

**Humlum & Vestergaard (2026)** — Humlum, A. & Vestergaard, E. (2026). Still Waters, Rapid Currents: Early Labor Market Transformation under Generative AI. NBER Working Paper 33777, May 2025, revised March 2026 (previously titled 'Large Language Models, Small Labor Market Effects'). <https://www.nber.org/system/files/working_papers/w33777/w33777.pdf>

- `ACA-03a` Danish admin data linked to adoption surveys: precise null effects of AI chatbots on earnings and recorded hours at worker and workplace level; pooled DiD rules out effects larger than 2% (dynamic DiD rules out >3%) two years after ChatGPT. *[2 % (upper bound of ruled-out effect), 2022-2024]* — contradicts; reproducible: no; verified: primary.
  - Contradicts strong displacement story; bears on C2/C4 (no workplace-level effect). Paper retitled in March 2026 revision -- cite new title. 11 exposed occupations, Denmark.
- `ACA-03b` No differential change in early-career employment share at workplaces encouraging chatbot use; estimates rule out effects greater than about one-third of a percentage point, so adoption explains at most ~0.14 pp of a ~0.6 pp aggregate early-career decline in Denmark. *[0.33 pp of early-career employment share (bound), Oct 2022-Dec 2024]* — contradicts; reproducible: no; verified: primary.
  - Direct counterpoint to C4 attribution to AI; they do replicate an aggregate early-career decline in exposed occupations (Appendix D.2) but find it is not at adopting workplaces. Section 3.4, fn 21.

**Fairlie & Wu (2026)** — Fairlie, R. W. & Wu, J. (2026). The Early Impacts of AI on Employment among Recent College Graduates. NBER Working Paper 35796, September 2026 (also IZA DP 18945 per lit report). <https://www.nber.org/papers/w35796>

- `ACA-04a` CPS microdata: recent US college graduates' unemployment did not spike in summer (Jun-Aug) 2026 vs previous summers and did not rise significantly relative to older graduates or young non-graduates (DiD and event study). *[Jun-Aug 2026 vs prior summers]* — complements; reproducible: no; verified: primary.
  - NBER number w35796 verified (Sep 2026). IZA DP 18945 not checked. Parallels our 'graduate unemployment still falling' point; partly contradicts strong C4 reading for unemployment (not hiring). Authors report no funding.
- `ACA-04b` Adding 'want a job' non-participants raises recent graduates' unemployment by nearly 2 pp (5.7% to 7.6% in their sample) but still shows no significant 2026 increase; some positive association with remote-work availability, not AI exposure. *[1.9 pp added by expanded unemployment definition, 2022-2026]* — complements; reproducible: no; verified: primary.
  - Methods idea for PLFS: expanded/sidelined unemployment measure.

**Atkinson & Yamco (2026)** — Atkinson, T. & Yamco, S. (2026). Young workers' employment drops in occupations with high AI exposure. Federal Reserve Bank of Dallas, Economics, January 6, 2026 (reposted FRBSF EERN, March 3, 2026). <https://www.dallasfed.org/research/economics/2026/0106>

- `ACA-05a` CPS: share of employment held by 20-24-year-olds in the most AI-exposed occupations fell from 16.4% to 15.5% (-0.9 pp) Nov 2022-Sep 2025; driven by lower job-finding of new entrants, not layoffs; implies at most ~0.1 pp of aggregate unemployment. *[-0.9 pp of employment share, Nov 2022-Sep 2025]* — agrees; reproducible: partly; verified: primary.
  - C4; small magnitude. Uses public CPS -- reproducible method for US. Lit report labelled it 'Dallas Fed (Jan-Mar 2026)'; the FRBSF URL is a repost and itself has no numbers. Job-finding of exposed new entrants fell >3 pp from Nov 2023 peak.

**Davis (2026)** — Davis, S. (2026). AI is simultaneously aiding and replacing workers, wage data suggest. Federal Reserve Bank of Dallas, Economics, February 24, 2026. <https://www.dallasfed.org/research/economics/2026/0224>

- `ACA-05b` Across 205 occupations, AI exposure lowers wage growth where the experience premium is low (-0.28 pp per SD at 0% premium) but raises it where the premium is high (+0.2 pp at 90th pct); median experience premium 40%; computer systems design employment -5% since fall 2022 while its wages rose 16.7%. *[-5 % employment change, US computer systems design (CES), fall 2022-early 2026]* — agrees; reproducible: yes; verified: primary.
  - Source of the 'rising returns to experience' claim (lit report attributed it loosely to Dallas Fed Jan-Mar). Parallels C4 pay (PLFS relative pay of young falling) and C2 (US IT-services employment down while wages up). BLS data, reproducible.

**Revelio Labs (2026)** — Revelio Labs (2026). Entry-Level Job Postings Are Down 35%. Revelio Labs blog, Aug 21, 2026 (updated Oct 5, 2026). <https://www.reveliolabs.com/blog/fast-company-entry-level-hiring>

- `ACA-05c` US entry-level job postings are down about 35% since early 2023; Revelio notes this alone does not establish AI as the cause. *[-35 % change in entry-level postings, early 2023-2026]* — agrees; reproducible: no; verified: primary.
  - C4; proprietary postings, metric undefined on page. Hosseini & Lichtinger cite Simon (2025, Revelio): >35% since Jan 2023 and a 10-point exposure increase predicts 11% lower entry-level demand.

**Stanford AI Index (2026)** — Stanford HAI (2026). Artificial Intelligence Index Report 2026, Chapter 4: Economy. Stanford Institute for Human-Centered AI, April 2026. <https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf>

- `ACA-05d` Employment for US software developers aged 22-25 fell close to 20% from its 2022 peak by September 2025 (Figure 4.4.29), based on Brynjolfsson et al. (2025) ADP data. *[-20 % vs 2022 peak (approx.), 2022 peak-Sep 2025]* — agrees; reproducible: no; verified: primary.
  - Not independent evidence: it reproduces Canaries/ADP. DISCREPANCY: chapter takeaway #7 says 'fallen nearly 20% from 2024' while the body says from the 2022 peak -- cite the body text. Same chapter: most-exposed 22-25 employment down ~16% vs least exposed (firm-type controls).

**Gartner (2026)** — Gartner (2026). 'Gartner Forecasts Worldwide IT Spending to Grow 14.2% in 2026, Totaling $6.37 Trillion'. Press release, Stamford, Jul 27, 2026. <https://www.gartner.com/en/newsroom/press-releases/2026-07-27-gartner-forecasts-worldwide-it-spending-to-grow-14-point-2-percent-in-2026-totaling-6-point-37-trillion>

- `IND-08c` Gartner forecasts worldwide services spending (ex-IaaS) of USD 1,570bn in 2026, +5.3%, after +3.8% in 2025; IaaS +29.3%; total IT +14.2%. *[5.3 % y/y nominal USD growth, 2025-2026]* — complements; reproducible: partly; verified: primary.
  - Demand benchmark for C1 (India's share). Differs from Kotak's cited 'Gartner IT services 3.1%/4.2%' (likely different vintage/currency basis). April 2026 release …

**Economic Survey 2025-26, Ch. 14** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 14: Evolution of the AI Ecosystem in India: The Way Forward, Box XIV.1 (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap14.pdf>

- `TT-03f` Box XIV.1: ARDL model of US non-supervisory PBIS employment (Mar 2016-Jul 2025) finds post-Dec 2022 regime dummy positive but its interaction with real GDP negative: long-run interaction -0.938 (SE 0.154), short-run -2.572 (SE 0.37). *[-0.938 coefficient (regime x output, long run), 2016-03 to 2025-07]* — agrees; reproducible: yes; verified: primary.
  - Box XIV.1, pp.551-553, Tables XIV.1-2. Employment responds less to output growth after Dec 2022; non-PBIS falsification shows near-zero effect. US data only, framed as structural change not causal. Employment level is not lower. Benchmark for C2/C3 and the replacement-rate parameter (S model section).

**Kruse & Yu (2026)** — Kruse, Hagen, and Shu Yu. 2026. 'The AI Exposure of Export-Linked Jobs.' Background Note for the World Development Report 2026. World Bank (July). <https://thedocs.worldbank.org/en/doc/9df559d23a6d80b3dfa2c4bc808f3a20-0050062026/original/The-AI-Exposure-of-Export-Linked-Jobs.pdf>

- `WB-04a` India's share of export-linked jobs at risk of AI substitution sits about one-half above the cross-country income trend line, at 5-6% of export-linked jobs, because of its specialisation in business services (about 30% of exports in 2024). *[50 % above income-trend line (share of export-linked jobs at risk), latest LFS (India PLFS ~2023) + ADB MRIO]* — complements; reproducible: partly; verified: primary.
  - C3/C4 context. p.4 (PDF p.5), Fig. 1. DISCREPANCY: the '50% above trend' is about EXPOSURE of export-linked jobs (Gmyrek et al. ILO scores, gradients 3-4), not exports or jobs above trend. Range across 26 economies is 1.3% (Pakistan) to 17.4% (Switzerland).

**Betai & Chen (2026)** — Betai, Neha, and Maggie Chen (George Washington University). 2026. 'Automation without Borders: Generative AI and Cross-Border Service Outsourcing.' Slides, Fourth Annual AI in Action Conference, Georgetown-World Bank (Jan 26). <https://thedocs.worldbank.org/en/doc/2770aa5def57e42a6d2449c90d6cf974-0070062026/original/10-Chen.pdf>

- `WB-05a` On a leading global online labour marketplace, GenAI cut outsourced contracts to developing-country freelancers by about 34% at mean skill exposure (buyers -34%, active workers -35%); effects null in developed countries. *[-34 % of contracts at mean exposure, Jan 2022-Dec 2024]* — agrees; reproducible: no; verified: primary.
  - C3/C4 analogue (freelance, not IT firms). Slides 6, 17, 33. Diff-in-diff over 2,700+ skills, using an LLM-elicited exposure measure. Platform not named. The document is a CONFERENCE SLIDE DECK, not a paper. DISCREPANCY inside the deck: value decline is -43% on the summary slides 6 and 33 but -53% on results slide 17 …

**Stapleton & O'Kane (2021/2026)** — Stapleton, Katherine, and Layla O'Kane. 'Artificial Intelligence and Services Offshoring.' Unpublished manuscript (dated 2021 in Bastos & Nayyar 2026; 2026 in Kruse & Yu 2026). <https://thedocs.worldbank.org/en/doc/0c3320b04832ac7407cd0fba03949383-0050062026/original/AI-and-services-trade-draft-July2026.pdf>

- `WB-06b` Using UK online job adverts 2012-17, machine-learning deployment in UK firms raised services offshoring, especially to lower-income countries; India was the main beneficiary (ICT and business/professional services). *[qualitative, 2012-2017]* — complements; reproducible: no; verified: unverified (press-only).
  - C1. Paper not found online. Known only via the summary in Bastos & Nayyar (2026, pp.2-3) and a 2019 Oxford CSAE talk by Stapleton. Pre-GenAI (ML). The date is inconsistent: 2021 in Bastos & Nayyar, 2026 in Kruse & Yu. Cite only as 'cited in'.

**WTO (2026)** — World Trade Organization. 2026. Global Trade Outlook and Statistics - March 2026. Geneva: WTO (Mar). <https://www.wto.org/english/res_e/booksp_e/gtos0326_e.pdf>

- `WB-07b` World digitally delivered services exports reached US$5.26tn in 2025 (+10%); world computer-services trade grew 11%, double digits for a third straight year; world other commercial services +10% to US$5.78tn. *[5.26 USD tn, 2025]* — complements; reproducible: yes; verified: primary.
  - C1 denominator. pp.25-27. Gives a benchmark for India's growth vs the world.

**Baldwin (2026)** — Baldwin, Richard. 2026. 'The Jobs AI Was Supposed to Eliminate Are Booming.' Richard Baldwin Substack (Factful Friday), Jul 30-31 (also on LinkedIn). <https://rbaldwin.substack.com/p/the-jobs-ai-was-supposed-to-eliminate>

- `WB-08b` Across the big eight services exporters plus the Philippines, OBS exports kept growing after ChatGPT; India's index reached 153 (Q4 2022=100), the highest; Philippines only ~120 (monthly, to Mar 2026) and +3.2% latest 12-month growth. *[153 index (Q4 2022=100), 2022Q4-2025Q4]* — complements; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): All nine rows of Baldwin's table reproduced to the decimal (baldwin_table_reproduced.csv). Philippines is the weak series. || Original verification note: C1. Excludes Ireland, Netherlands and Luxembourg. The Philippines' weak growth is the counter-signal …

## Demand elasticity priors

**Demirci, Hannane & Zhu (2025)** — Demirci, O., Hannane, J. & Zhu, X. (2025). Who Is AI Replacing? The Impact of Generative AI on Online Freelancing Platforms. Management Science 71(10): 8097-8108, doi:10.1287/mnsc.2024.05420. <https://doi.org/10.1287/mnsc.2024.05420>

- `ACA-08a` Job posts for automation-prone freelance jobs (writing, coding) fell 21% relative to manual-intensive jobs within eight months of ChatGPT; image-creation posts fell 17% after image-generation AI. *[-21 % change in job posts, Nov 2022-Jul 2023]* — agrees; reproducible: no; verified: primary.
  - Abstract read via Crossref metadata (journal page blocked). Cross-price/substitution effect on outsourced freelance work -- closest analogue to outsourced IT demand; listed as ELA in FINDINGS.

**Bessen (2019)** — Bessen, J. (2019). Artificial Intelligence and Jobs: The Role of Demand. In Agrawal, Gans & Goldfarb (eds.), The Economics of Artificial Intelligence: An Agenda, ch. 10, pp. 291-307. University of Chicago Press / NBER (chapter c14029). <https://www.nber.org/system/files/chapters/c14029/c14029.pdf>

- `ELA-01a` Rough price-elasticity-of-demand estimates (Table 10.1): cotton 2.13 (1810) to 0.02 (1995); steel 3.49 (1860) to 0.16 (1982); autos 6.77 (1910) to 0.15 (2007). *[2.13->0.02; 3.49->0.16; 6.77->0.15 price elasticity of demand (absolute), 1810-2007]* — complements; reproducible: no; verified: primary.
  - Prior for epsilon: elastic early, inelastic once satiated. 'Very rough' per author; lognormal-preference model.
- `ELA-01b` Two centuries of US textile, steel and auto data: automation initially raised industry employment because demand was highly elastic, then demand satiated and jobs fell. *[1800s-2010s]* — complements; reproducible: no; verified: primary.
  - Abstract verified via Crossref; Table 1 values (early 1.3/2.2/2.4 vs 1950 0.2/-1.2/0.4 per FINDINGS) NOT seen by me (paywall). A negative steel elasticity in 1950 looks odd -- recheck the table before citing.

**Bessen (2015)** — Bessen, J. (2015). Toil and Technology. Finance & Development 52(1), IMF, March 2015. <https://www.imf.org/external/pubs/ft/fandd/2015/03/bessen.htm>

- `ELA-01c` ATMs cut tellers needed per urban branch from 20 to 13 (1988-2004) but urban branches rose 43%, so teller jobs did not decline. *[20->13; +43 tellers per branch; % change in branches, 1988-2004]* — complements; reproducible: no; verified: primary.
  - Classic analogue: unit labour requirement falls, demand/outlet expansion offsets. Opened via WebFetch (curl blocked).

**Tevlin & Whelan (2003)** — Tevlin, S. & Whelan, K. (2000/2003). Explaining the Investment Boom of the 1990s. FEDS 2000-11, Federal Reserve Board, March 2000; Journal of Money, Credit and Banking 35(1), 2003. <https://www.federalreserve.gov/pubs/feds/2000/200011/200011pap.pdf>

- `ELA-02` Long-run elasticity of the computer capital stock with respect to its user cost is -1.6, nearly 9 times the aggregate equipment estimate. *[-1.6 user-cost elasticity, 1960s-1990s]* — complements; reproducible: no; verified: primary.
  - Demand for IT capital, not IT services; JMCB volume/issue from memory, not re-checked.

**Byrne, Corrado & Sichel (2018)** — Byrne, D., Corrado, C. & Sichel, D. E. (2018). The Rise of Cloud Computing: Minding Your P's, Q's and K's. NBER Working Paper 25188, October 2018. <https://www.nber.org/papers/w25188>

- `ELA-03` Hedonic AWS prices fell about 7%/yr (EC2 compute), >11%/yr (database) and ~17%/yr (storage) over 2009-2016, faster after 2014; AWS revenue grew 70% and 55% in 2015 and 2016. *[-7 to -17 % per year (quality-adjusted price), 2009-2016]* — complements; reproducible: no; verified: primary.
  - No elasticity estimated; price-quantity co-movement only. Analogue for AI-driven price deflation passed to clients.

**Nakano & Nishimura (2024)** — Nakano, S. & Nishimura, K. (2024). How do we measure trade elasticity for services? arXiv:2401.08594, v2 October 2024. <https://arxiv.org/abs/2401.08594>

- `ELA-04` Armington (source-country substitution) elasticity for Japan's imports of telecommunications, computer and information services is 1.066 (s.e. 0.054), 2005-2020 (Table 4); services elasticities generally near unity. *[1.066 Armington elasticity of substitution, 2005-2020]* — complements; reproducible: partly; verified: primary.
  - DISCREPANCY with FINDINGS: category is telecom+computer+information combined, not computer services alone. Substitution between supplier countries, not a market price elasticity of demand. Uses WTO data (reproducible for India's partners).

**Raissi & Tulin (2015)** — Raissi, M. & Tulin, V. (2015). Price and Income Elasticity of Indian Exports -- The Role of Supply-Side Bottlenecks. IMF Working Paper WP/15/161, July 2015. <https://www.imf.org/external/pubs/ft/wp/2015/wp15161.pdf>

- `ELA-05` Long-run price elasticity of Indian (goods) exports about -0.86. *[-0.86 price elasticity of exports, 1990s-2010s]* — complements; reproducible: no; verified: not found.
  - Could not open (IMF Akamai block, elibrary 403); number carried from FINDINGS section 6, not re-verified. Goods exports, not services.

**McKinsey Global Institute (2003)** — McKinsey Global Institute (2003). Offshoring: Is It a Win-Win Game? MGI report, August 2003. <https://www.mckinsey.com/featured-insights/employment-and-growth/offshoring-is-it-a-win-win-game>

- `ELA-06` For each dollar of US corporate spending offshored to India, US firms save about 58 cents (total value creation ~$1.45-1.47, India captures ~33 cents). *[58 US cents saved per dollar offshored, 2003]* — complements; reproducible: no; verified: not found.
  - Page timed out; search budget exhausted. Numbers are from memory/FINDINGS only -- do not cite until opened. Relevant to client price savings, not an elasticity.

**Brynjolfsson (1996)** — Brynjolfsson, E. (1996). The Contribution of Information Technology to Consumer Welfare. Information Systems Research 7(3): 281-300, doi:10.1287/isre.7.3.281. <https://doi.org/10.1287/isre.7.3.281>

- `ELA-07` Integrating the BEA-based demand curve for IT, IT spending generated about $50-70bn in net consumer value in 1987 (about 3x its cost), raising growth ~0.3%/yr. *[50-70 USD bn consumer surplus (1987), 1987]* — complements; reproducible: no; verified: primary.
  - Abstract verified via Crossref. The price elasticity of IT demand itself was NOT retrieved (paywall); FINDINGS still UNCONFIRMED. IT hardware, not services.

**(gap)** — No published estimate of the price elasticity of demand for outsourced IT services or BPO located. (URL in repo CSV)

- `ELA-08` No published market-level price elasticity of demand for outsourced IT/BPO services was found in this pass (search budget exhausted before a dedicated search). — complements; reproducible: no; verified: not found.
  - Consistent with FINDINGS section 6. Gartner/academic search not completed -- follow-up needed.

## Context and commentary

**Eloundou et al. (2024)** — Eloundou, T., Manning, S., Mishkin, P. & Rock, D. (2024). GPTs are GPTs: Labor market impact potential of LLMs. Science 384(6702): 1306-1308, doi:10.1126/science.adj0998 (arXiv:2303.10130). <https://arxiv.org/abs/2303.10130>

- `ACA-08b` About 80% of US workers could have at least 10% of tasks affected by LLMs, and about 19% at least 50% of tasks. *[80 % of US workforce with >=10% tasks exposed, 2023]* — complements; reproducible: yes; verified: primary.
  - Exposure score source (methods footnote). Science metadata verified via Crossref; numbers from arXiv abstract. Science version is a short Policy Forum.

**Felten, Raj & Seamans (2021)** — Felten, E., Raj, M. & Seamans, R. (2021). Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses. Strategic Management Journal 42(12): 2195-2217, doi:10.1002/smj.3286. <https://doi.org/10.1002/smj.3286>

- `ACA-08c` Introduces the AI Occupational Exposure (AIOE) index by occupation, industry and geography. — complements; reproducible: yes; verified: primary.
  - Citation verified via Crossref metadata (journal page blocked). Methods footnote for exposure scores. Dallas Fed (Davis 2026) uses this index.

**Felten, Raj & Seamans (2023)** — Felten, E., Raj, M. & Seamans, R. (2023). How will Language Modelers like ChatGPT Affect Occupations and Industries? arXiv:2303.01157, March 2023. <https://arxiv.org/abs/2303.01157>

- `ACA-08d` Adapts AIOE to language modelling; most exposed occupations include telemarketers and post-secondary teachers; most exposed industries legal services and securities; exposure positively correlated with wages. — complements; reproducible: yes; verified: primary.
  - Methods footnote.

**Acemoglu (2024)** — Acemoglu, D. (2024). The Simple Macroeconomics of AI. NBER Working Paper 32487, May 2024; published Economic Policy 40(121): 13-58, doi:10.1093/epolic/eiae042. <https://www.nber.org/papers/w32487>

- `ACA-10a` Task-based Hulten calculation: AI raises TFP by no more than 0.66% over 10 years (below 0.53% once hard-to-learn tasks are considered). *[0.66 % TFP over 10 years, 2024-2034]* — complements; reproducible: no; verified: primary.
  - Context for modest macro effects; uses Eloundou exposure and micro productivity estimates. Published version metadata via Crossref.

**Indeed Hiring Lab (gap)** — Indeed Hiring Lab, Job Postings Index data repository (GitHub hiring-lab/job_postings_tracker). <https://github.com/hiring-lab/job_postings_tracker>

- `HIR-14c` Indeed Hiring Lab publishes no India job-postings index: its public tracker covers AU, CA, DE, EA, ES, FR, GB, IE, IT, NL and US only. — complements; reproducible: no; verified: primary.
  - GAP: no free Indeed India software-postings series. Use Naukri JobSpeak (HIR-10) instead. NIRF 2026 placement statements were not searched in this pass (search budget exhausted); the project already holds NIRF data for C4.

**Goldman Sachs (2026a)** — Sengupta, S. (Goldman Sachs) (2026). Remarks to Bloomberg Television, reported in 'Goldman Sachs says AI unlikely to cause widespread job losses in India; services sector faces risk', Free Press Journal, Aug 14, 2026. <https://www.freepressjournal.in/business/goldman-sachs-says-ai-unlikely-to-cause-widespread-job-losses-in-india-services-sector-faces-risk>

- `IND-06a` Goldman's chief India economist says widespread AI job losses in India are unlikely as most workers are in physical jobs, but IT (esp. call centres), telecom and postal services carry the most substitution risk. *[0.4 pp productivity gain over 10 years, 10-year horizon]* — complements; reproducible: no; verified: press.
  - Economy-wide; no IT headcount numbers. GCC offset and junior-openings claims are NOT in this article. Context box.

**Future of India Foundation (2026)** — Future of India Foundation [unsigned; same text posted by Ruchi Gupta on her Substack 6 Oct 2026] (2026), 'IT Sector Helped Build the Indian Middle Class. For Its Workers, It Is Starting to Sputter', India After Liberalisation series Part 5, YouthPOWER / Future of India Substack, Oct 2. <https://foifaction.substack.com/p/it-sector-helped-build-the-indian>

- `JRN-01g` Labour's share of IT value added (PLFS earnings over MoSPI GVA) was about 14% in 2017-18 and nearly a quarter by 2023-24 on the old series, then fell. On the new series, value added rose about 26% and earnings about 20% from 2022-23 to 2024-25. *[14 -> ~22-25 % of IT GVA, 2017-18 to 2023-24 (old base); 2022-23 to 2024-25 (new base)]* — complements; reproducible: yes; verified: primary.
  - CORRECTED (repo check, labour_share/FINDINGS.md): Methodological artefact; do not cite as evidence. The PLFS-earnings-over-NAS-GVA method gives a wage bill far too low (top-6 employee cost alone, Rs 3.9 lakh cr in FY24, exceeds the PLFS wage bill for the whole sector, Rs 3.5 lakh cr: PLFS omits employer PF, …

**Sidhant (2026)** — Aman Kai Sidhant (2026), 'India's $300B AI Shock', india300.ai, Jun 18. <https://india300.ai/>

- `JRN-02d` Scenario: a 20% fall in software exports would widen the FY25 current-account deficit from $23.3bn (0.6% of GDP) to $64bn (1.65%), and a 50% fall to $126bn (3.24%). *[1.65 / 3.24 % of GDP (CAD), FY25 baseline, scenarios]* — complements; reproducible: yes; verified: press.
  - Static scenario arithmetic with no behavioural response; not evidence. Context only, if we discuss macro stakes.

**Bhattacharya (2026)** — Ananya Bhattacharya (2026), 'Why Claude Cowork is a math problem Indian IT can't solve', Rest of World, Feb 6. <https://restofworld.org/2026/indian-it-ai-stock-crash-claude-cowork/>

- `JRN-04a` Indian IT stocks fell nearly 6% on 4 Feb 2026 after Anthropic released Claude Cowork; the article frames per-person billing as the vulnerable part of the model. *[-6 % index move (one day), 2026-02-04]* — complements; reproducible: yes; verified: press.
  - Context for the AI-shock narrative. DISCREPANCY: the literature report says this article cites EY on entry-level roles down 20-25%; the article contains NO EY figure. The 20-25% traces to a 2025 EY analysis relayed by Storyboard18 and content sites; the primary was not found. Do not cite.

**Elias (2026)** — Jibu Elias (2026), 'Growth without work: The human cost of the AI revolution', Rest of World, Aug 5 (book excerpt). <https://restofworld.org/2026/ai-jobs-economy-impact/>

- `JRN-04b` Argues that AI brings 'productivity without participation': output can rise while employment and wages stagnate, with costs falling on young, clerical and Global South workers. — agrees; reproducible: no; verified: press.
  - Same framing as our C1 + C3/C4, but most numbers are unsourced (e.g. 500k Indian tech jobs lost 2022-Apr 2024). Cite only as an example of the narrative, not for data.

**Dharmakumar (2026)** — Rohin Dharmakumar (2026), 'AI, India, and the giant sucking sound', Zero Shot #40, The Ken, Jun 6. <https://the-ken.com/columns/zero-shot/ai-india-and-the-giant-sucking-sound/>

- `JRN-05a` Opinion: Indian firms are investing abroad and underinvesting in domestic AI, so India supplies labour, data and compute while value sits in the frontier-model layer. — complements; reproducible: no; verified: primary.
  - No IT-sector employment or output data; the only IT figure is the '6m programmers' borrowed from Andy Mukherjee. Not relevant to C1-C4 except as framing. The literature report's summary ('IT firms too timid on AI') is roughly right.

**Reuters Breakingviews (2026)** — Aimee Donnellan & Una Galani (2026), 'India is patient zero for AI job loss onslaught' (podcast), Reuters Breakingviews, May 14. <https://www.stockopedia.com/share-prices/hsbc-holdings-HKG:5/news/india-is-patient-zero-for-ai-job-loss-onslaught-podcast-019e6a25-9d37-78ef-8116-0b29c8e29088/>

- `JRN-05b` Podcast arguing that India is the most exposed economy to AI white-collar job loss, with hiring already slowing; a linked column warns that the AI job shock risks throttling consumption. — agrees; reproducible: no; verified: unverified (press-only).
  - Only search snippets were available; the Stockopedia page returned 403. Forkast attributes a scenario to Breakingviews (a 30% cut in a 15m workforce -> ~5m fewer consumers, ~$75bn spending), which we could not verify. Context only.

**Mukherjee (2025)** — Andy Mukherjee (2025), 'Amazon's Layoffs Show How AI Is Coming for India', Bloomberg Opinion, Nov 2. <https://www.bloomberg.com/opinion/articles/2025-11-02/amazon-s-layoffs-show-how-ai-is-coming-for-india>

- `JRN-05d` Column arguing that Amazon's 14,000 corporate cuts signal generative AI moving beyond entry-level coding and threatening Indian white-collar outsourcing hubs. — agrees; reproducible: no; verified: unverified (press-only).
  - Paywalled; only the opening and the Bloomberg Tax syndication snippet were seen. Opinion, no India data. Context only.

**New York Times (2026)** — [Byline unconfirmed; one aggregator credits Paul Mozur] (2026), article on India's outsourcing industry racing to adapt to AI, The New York Times, Feb 27. (URL in repo CSV)

- `JRN-05e` Reportedly describes India's outsourcing industry as employing 6m+ people and worth nearly $300bn, with TCS headcount at about 580k (more than 20k below its 2022 peak); quotes the NASSCOM president saying young engineers should be worried. *[6m+ persons, 2026]* — agrees; reproducible: no; verified: unverified (press-only).
  - nytimes.com is blocked for our tools. The date (27 Feb 2026) and headline gist come from a Reddit link and aggregators (bensbites, techloy); the exact title and author are unconfirmed. The 6m figure is NASSCOM's IT-BPM workforce, which is broader than PLFS NIC 62-63. Do not cite without opening the original.

**Malik & Jain (2026)** — Malik, P. & Jain, N. (2026). Interactions of Artificial Intelligence with India's Labour Market: Devising an AI-for-Labour Model Using the Productivity, Inclusivity, and Entrepreneurship Framework. ICRIER Policy Brief 10, ICRIER Prosus Centre for Internet and Digital Economy (February). <https://icrier.org/pdf/Interactions-of-Artificial-Intelligence-with-India-s-Labour-Market.pdf>

- `TT-02b` India's aggregate employment elasticity was about 0.2 from the 1990s, rising to 1.1 between 2017 and 2023 (citing ORF). *[1.1 employment elasticity, 2017-2023]* — complements; reproducible: partly; verified: primary.
  - p.1. Economy-wide, not IT. Context for the elasticity discussion only.

**Economic Survey 2025-26, Ch. 7** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 7: Services: From Stability to New Frontiers (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf>

- `TT-03e` EPFO data for Apr-Jul FY26: services 51.7% of net payroll additions, led by expert services. *[51.7 % of EPFO net additions, Apr-Jul FY26]* — complements; reproducible: yes; verified: primary.
  - Para 7.14, p.266-267. Shows EPFO industry splits are public ('expert services' contains computer-related services). Data availability note for S3.

**Economic Survey 2025-26, Ch. 14** — Ministry of Finance, Government of India (2026). Economic Survey 2025-26, Chapter 14: Evolution of the AI Ecosystem in India: The Way Forward, Box XIV.1 (January). <https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap14.pdf>

- `TT-03g` Survey warns that firms abroad may no longer need India's IT comparative advantage, risking 'hollowing out' its core value proposition, and that AI is outperforming entry-level educated workers. *[2026]* — complements; reproducible: no; verified: primary.
  - Para 14.7 p.553 and para 14.44 p.569. Qualitative government framing; useful quote for intro. No Indian IT employment data in Ch.14.

**RBI Bulletin / gap search** — Search note (2026-10-15): no 2026 RBI Bulletin article on IT services exports, GCCs or AI found; a 2024 RBI Bulletin article on GCCs is cited in secondary sources (1,700 GCCs, >US$100bn by 2030, >2.5m jobs). (URL in repo CSV)

- `TT-10a` No 2026 RBI Bulletin article linking AI, GCCs and software exports was found; latest GCC piece is a 2024 Bulletin article seen only via secondary citation. *[2024-2026]* — complements; reproducible: partly; verified: not found.
  - Web-search budget ran out before checking the RBI Bulletin archive directly; treat as incomplete.

**Indian academic gap search** — Search note (2026-10-15). (URL in repo CSV)

- `TT-10c` No 2026 IIM/ISI/IGIDR paper using PLFS specifically on IT-sector employment or young IT graduates was found; closest are Great Lakes WP5 (economy-wide PLFS 2025) and SWI 2026. *[2026]* — complements; reproducible: no; verified: not found.
  - Search incomplete (web-search budget exhausted). Supports novelty of our PLFS relative-pay result (C4).

**World Bank (2026, IDU)** — World Bank. 2026. India Development Update, October 2026: India and Artificial Intelligence - Seizing the Development Opportunity. Washington, DC (exec. summary Oct 6; full report posted Oct 13). Report No. 215496. <https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf>

- `WB-03b` About 22% of Indian employment is highly exposed to AI (AIOE), vs about 60% in advanced economies and 35% in EMDEs. *[22 % of employment highly exposed, recent LFS]* — complements; reproducible: partly; verified: primary.
  - Context/methods. p.38 (PDF p.40), Fig. 4.6, Box 4.2 (Felten-Raj-Seamans AIOE, Pizzinelli C-AIOE). We could partly reproduce this with PLFS plus a public crosswalk.

**Nunes (2026)** — Nunes, Marcus. 2026. 'A Critical Look at "The Jobs AI Was Supposed to Eliminate Are Booming".' Substack (Aug 2). <https://marcusnunes.substack.com/p/a-critical-look-at-the-jobs-ai-was>

- `WB-09a` Rebuttal of Baldwin: export value is not employment; OBS is too broad (includes consulting, legal, engineering); contract lags; the 2015-22 baseline is distorted by Covid; and the flat Philippines line fits displacement too. Three years of data cannot tell 'panic wrong' from 'panic early'. *[qualitative, 2022-2025]* — agrees; reproducible: yes; verified: primary.
  - REPRODUCED (repo check, contradictions/FINDINGS_output.md): Our numbers back Nunes's main points: export value is not jobs, the category is broad, and the trend window drives the result. || Original verification note: Supports our framing (C1 output up but C2-C4 jobs not). Good for a 'debate' box. Repeats Baldwin's …

**Smith (2026a)** — Smith, Noah. 2026. 'Roundup #86: Unintended consequences.' Noahpinion, section 4 'AI is creating demand for Indian outsourcers' (Aug 12). <https://www.noahpinion.blog/p/roundup-86-unintended-consequences>

- `WB-09b` Noah Smith argues AI is creating demand for Indian outsourcers and acting as a complement 'for now', using two charts from Baldwin's LinkedIn version of the post. *[qualitative, 2022-2026]* — contradicts; reproducible: yes; verified: primary.
  - Contradicts the alarm framing, not C2-C4 directly. The substantive India item is in Roundup #86 (Aug 12, section 4), NOT #88. #88 (Sep 18) has only a one-line callback with no numbers. Correct the literature report citation.

**Smith (2026b)** — Smith, Noah. 2026. 'Roundup #88: Is it time to panic yet?' Noahpinion (Sep 18). <https://www.noahpinion.blog/p/roundup-88-is-it-time-to-panic-yet>

- `WB-09c` One-line callback that AI 'keeps stubbornly refusing to kill Indian back-office outsourcing companies' (no data). *[qualitative]* — contradicts; reproducible: no; verified: primary.
  - Minor. Links back to Roundup #86. Cite #86 instead.

## Metrics we cite but cannot reproduce

Each needs a line in the report saying the figure is the source's own and we could not rebuild it. Rows marked 'partly' are listed where the key number itself is not rebuildable.

| item | source | metric | why we can't reproduce it | verified | stance |
|--|--|--|--|--|--|
| IND-01a | Nasscom (2026) | Nasscom estimates India's tech sector revenue (incl. hardware) will cross USD 315bn in FY26, up 6.1% y/y. [315 USD bn, FY26E] | industry-body estimate; method not public, revised each edition | primary | agrees |
| IND-01d | Nasscom (2026) | Nasscom revised FY25 revenue up to USD 297bn (from USD 282.6bn) and puts FY25 net hiring at about 133,000 (vs 126,000 in the FY25 edition). [297 USD bn, FY25 (revised)] | industry-body estimate; method not public, revised each edition | press | complements |
| IND-01j | Nasscom (2025) | FY25 edition: industry revenue est. USD 283bn (+5.1%), exports USD 224bn (+4.6%), domestic USD 58.2bn (+7.0%). [283 USD bn, FY25E] | industry-body estimate; method not public, revised each edition | primary | agrees |
| IND-03a | Kotak Institutional Equities (2026a) | Kotak sees Indian IT services growth range-bound at about 3% with no meaningful FY27 recovery; global IT services averaged 5% cc over 10 … [3 % y/y revenue growth, FY27E / CY25] | broker / company forecast model | press | agrees |
| WB-02e | World Bank (2026, SAEU Oct) | But firm-to-firm GVC data show US-South Asia links grew FASTEST where both sides are AI-exposed: a 1 s.d. rise in a US firm's AI exposure … [27.5 % larger post-GPT increase in links per 1 s.d. AI exposure, 2020-2025Q4 (FactSet GVC links)] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | complements |
| IND-02a | Nasscom-Zinnov (2026) | India has 2,117 GCCs across 3,728 units in FY26E; the number of GCCs grew ~32% since FY21. [2117 GCCs, FY26E] | industry-body estimate; method not public, revised each edition | primary | complements |
| IND-02b | Nasscom-Zinnov (2026) | Installed GCC talent is 2.36mn and GCC revenue USD 98.4bn in FY26E. [2.36 million persons, FY26E] | industry-body estimate; method not public, revised each edition | primary | complements |
| IND-02e | Nasscom-Zinnov (2024) | Prior edition: 1,700+ GCCs, 2,975+ units, 1.9mn+ employees and USD 64.6bn revenue in FY24; GCC count up 32% FY19-FY24 (from ~1,285). [1.9 million persons, FY24] | industry-body estimate; method not public, revised each edition | press | complements |
| TT-03d | Economic Survey 2025-26, Ch. 7 | As of FY24 India hosts 1,700+ GCCs employing over 19 lakh (1.9m) professionals; GCC revenue US$64.6bn (FY24E) vs 40.4bn (FY19). [1.9 million GCC employees, FY24] | not reproducible from free data | primary | complements |
| TT-05a | Roy Bardhan & Bhowmick (2026) | Stress test of AI displacement in GCCs: gross displacement of 40,183 to 150,686 jobs by 2030 (net 24,110 to 120,549 after 20-40% … [40,183-150,686 jobs (gross), to 2030] | scenario model | primary | complements |
| TT-05b | Roy Bardhan & Bhowmick (2026) | GCC employment about 1.9m in FY24 and over 2.3m in FY26; >2,100 GCCs; revenue ~US$98-100bn (Zinnov-NASSCOM 2026). [2.3 million GCC employees, FY24-FY26] | scenario model | primary | complements |
| TT-05c | Roy Bardhan & Joshi (2026) | Zinnov data: installed GCC talent rose from ~1.75m (FY21) to 2.36m (FY26E), a ~6.2% CAGR, while GCC revenue grew ~9.9% CAGR (US$61.4bn to … [6.2 % CAGR GCC headcount, FY21-FY26E] | scenario model | primary | agrees |
| WB-03e | World Bank (2026, IDU) | India exported about US$200bn of ICT services in 2025; its GCC ecosystem had 2,117 centres employing 2.36 million and generating US$98.4bn … [2.36 million GCC employees, FY2026] | Enterprise Survey AI module; Goldman client note | primary | complements |
| HIR-05a | Nomura (Varma & Toh, 2026) | Nomura counts 83,100 AI-related hires against 31,921 AI-linked layoffs/attrition in India (about 2.6 hires per job lost), 2022 to Aug 2026. [83100 vs 31921 persons (announced cases), 2022-Aug 2026] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| IND-01c | Nasscom (2026) | Nasscom projects direct tech-sector employment of ~6mn in FY26 (PTI: 59.5 lakh, up from 58.15 lakh), +2.3% or net 135,000 added. [135000 persons (net additions), FY26E] | industry-body estimate; method not public, revised each edition | primary | complements |
| IND-01f | Nasscom (2026) | Nasscom president Rajesh Nambiar highlighted the gap ('non-linearity') between job growth of 2.3% and revenue growth of 6.1%. [2.3 vs 6.1 % y/y growth (jobs vs revenue), FY26E] | industry-body estimate; method not public, revised each edition | press | agrees |
| IND-01k | Nasscom (2025) | FY25 edition: net hiring rose to 126,000, taking the employee base to 5.80mn (+2.2% y/y); only 45% of providers expected higher hiring in … [126000 persons (net additions), FY25E] | industry-body estimate; method not public, revised each edition | primary | complements |
| IND-01l | Nasscom (2024) | FY24 edition: revenue est. USD 254bn (+3.8%); industry stayed a net hirer, adding 60,000 to reach 5.43mn employees (+1.1%). [60000 persons (net additions), FY24E] | industry-body estimate; method not public, revised each edition | primary | complements |
| REP-05a | Xpheno via Business Standard (2026) | Xpheno puts net headcount additions at IT firms at 50k (FY24), 100k (FY25), 110k (FY26) and at GCCs at 60k, 110k, 200k. [110000 net headcount additions, IT firms (persons), FY24-FY26] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| TT-01b | ICRIER (2026) | 65% of firms report hiring fell after introducing AI, 24% report an increase, 11% no significant change. [65 % of firms, after AI adoption (to 2025-26)] | own survey of 651 firms; microdata not public | primary | agrees |
| TT-01i | ICRIER (2026) | Expectations: 44% of firms expect no major change in employment, 28% expect expansion, 27% expect decline. [27 % of firms expecting decline, near term (from 2025-26)] | own survey of 651 firms; microdata not public | primary | complements |
| TT-04a | NITI Aayog (2025) | India's tech workforce was 7.5-8m in 2023 (tech services plus tech jobs in other sectors); headwinds could cut it to ~6m by 2031, tailwinds … [6-10 million persons, 2023 to 2031] | scenario model | primary | complements |
| TT-04c | NITI Aayog (2025) | Customer-experience (CX/BPO) workforce of 2-2.5m in 2023 could fall to 1.8m or rise to 3.1m by 2031. [1.8-3.1 million persons, 2023 to 2031] | scenario model | primary | complements |
| WB-01a | World Bank (2025) | After ChatGPT's release, job postings in business-services occupations grew about 35% more slowly than in other occupations (diff-in-diff, … [-35 % relative to other occupations (log points -0.349), Aug 2020-Mar 2025 (post = after Nov 2022)] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| WB-01c | World Bank (2025) | GenAI cut monthly job listings by about 20% for the most AI-exposed, least AI-complementary white-collar occupations (e.g. call-centre … [-20 % of monthly listings, post-Nov 2022 vs pre, through Mar 2025] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| WB-02a | World Bank (2026a, SAEU Apr) | Across South Asian firms, an interquartile-range rise in AI exposure is associated with a 1.5% fall in job postings relative to trend, … [-1.5 % of job postings per IQR of firm AI exposure, post-Nov 2022 (Lightcast, to 2025)] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| WB-02c | World Bank (2026, SAEU Oct) | Oct 2026 SAEU (title 'Adopting AI for Growth') reports that hiring has slowed among South Asian firms whose workforces are highly … [30 % wage premium for AI skills, 2020-2025] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| HIR-01a | TeamLease EdTech (2026) | Share of IT employers intending to hire freshers in Jul-Dec 2026 fell to 76% from 81% in Jan-Jun 2026. [76 (from 81) % of employers intending to hire freshers, H2 2026 vs H1 2026] | employer intent survey; no microdata | press | agrees |
| HIR-01b | TeamLease EdTech (2026) | Overall fresher hiring intent across sectors rose to 75% from 73%, led by e-commerce/tech start-ups and retail (93% each), manufacturing … [75 (from 73) % of employers intending to hire freshers, H2 2026 vs H1 2026] | employer intent survey; no microdata | press | agrees |
| HIR-02a | foundit (2026) | IT hardware & software firms' share of fresher hiring fell from 32% (2025) to 24% (2026). [24 (from 32) % of fresher hiring (postings), Jul 2025 vs Jul 2026] | proprietary postings / staffing-firm estimates; method not published | press | agrees |
| HIR-02b | foundit (2026) | Overall fresher hiring on foundit fell 10% year on year (and 2% month on month) in July 2026. [-10 % YoY (postings index), Jul 2026] | proprietary postings / staffing-firm estimates; method not published | press | agrees |
| HIR-03a | Xpheno via Outlook Business (2026) | Active entry-level tech openings (up to 2 years' experience) were about 10,000, down 44% year on year (from 13,000 in May 2026 per the … [10000 (-44% YoY) job openings (count), mid-2026 (month not stated)] | proprietary postings / staffing-firm estimates; method not published | press | agrees |
| HIR-03b | Xpheno via Outlook Business (2026) | Active tech openings were 93,000, the lowest in 28 months, down 14% MoM and 17% YoY. [93000 job openings (count), June 2026 (as stated)] | proprietary postings / staffing-firm estimates; method not published | press | agrees |
| HIR-04a | Xpheno via Business Today (2026) | Xpheno estimates IT-sector fresher hiring fell from a peak of about 600,000 in FY22 to about 120,000 in FY25 (-80%), with FY26 expected to … [600000 -> 120000 fresher hires (persons), FY22-FY25] | proprietary postings / staffing-firm estimates; method not published | press | agrees |
| HIR-11a | LinkedIn Grad's Guide (2026) | LinkedIn reports India entry-level hiring up 168% from 2023 to 2025. [168 % change (undefined), 2023-2025] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| HIR-14b | Quess Corp (2025) | Quess: IT job demand reached 1.8m roles in 2025 (+16%); GCC share of demand 27% (from 15%); entry-level just 15% of demand; mid-career … [15 % of IT job demand that is entry-level, 2025] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| REP-03a | Xpheno via press (Oct 2026) | Active tech openings rebounded to 120-123k in Oct 2026 (18-month high, +15-17% YoY); IT-services openings 66k (+57% YoY); entry-level (0-2 … [12.2 % of active tech openings that are entry-level, Jun 2025-Oct 2026] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| REP-04a | HAN Digital via ET (2026) | IT-BPM (incl. GCCs and BPO) fresher hiring fell from about 400k in FY22 to about 175k in FY26 (estimate) and could reach up to 210k in FY27 … [175000 fresher hires (persons), FY22-FY27] | proprietary postings / staffing-firm estimates; method not published | press | complements |
| TT-01a | ICRIER (2026) | Survey of 651 IT firms (IT services, products, BPM, ER&D/GCCs, startups) in 10 Indian cities, fielded Nov 2025-Jan 2026 (72% in person), … [651 firms, 2025-11 to 2026-01] | own survey of 651 firms; microdata not public | primary | complements |
| TT-01c | ICRIER (2026) | Entry level: 55% of firms report a decline in entry-level employment over the last 24 months, 35% an increase. [55 % of firms, last 24 months to Nov 2025-Jan 2026] | own survey of 651 firms; microdata not public | primary | agrees |
| TT-01d | ICRIER (2026) | Mid level: 42% of firms report increased mid-level employment, 33% no change, 25% a decline. [42 % of firms, last 24 months to Nov 2025-Jan 2026] | own survey of 651 firms; microdata not public | primary | agrees |
| TT-01e | ICRIER (2026) | Senior level: 82% of firms report no change in senior-level employment. [82 % of firms, last 24 months to Nov 2025-Jan 2026] | own survey of 651 firms; microdata not public | primary | complements |
| TT-08b | Azim Premji University (2026) | Of young graduate men who report being unemployed, about half find work within a year but only ~7% (6.7%) find permanent salaried work. [6.7 % finding permanent salaried work within a year, CMIE-CPHS pooled panel] | CMIE CPHS panel | primary | complements |
| WB-01d | World Bank (2025) | Entry-level postings in jobs as exposed as software developers grew 21% more slowly than for electrician-level exposure; senior roles … [-21 % (entry-level postings, software-dev vs electrician exposure), post-Nov 2022, through Mar 2025] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| WB-03d | World Bank (2026, IDU) | Cites ICRIER survey of 651 IT firms: no fall in aggregate employment with GenAI, but 55% of firms report lower entry-level hiring vs 25% … [55 % of firms reporting lower entry-level hiring, survey 2025-26] | Enterprise Survey AI module; Goldman client note | primary | agrees |
| WB-01b | World Bank (2025) | Posted wages in business-services occupations fell about 8% relative to other occupations after ChatGPT. [-8 % relative to other occupations (log points -0.080), Aug 2020-Mar 2025] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | agrees |
| IND-03b | Kotak Institutional Equities (2026a) | Kotak's industry base case is 3.5% AI-led pricing erosion, appearing first in renewals of large multi-year contracts; it calls GenAI … [3.5 % price deflation per year, FY27 onward] | broker / company forecast model | press | complements |
| IND-03d | Kotak Institutional Equities (2026b) | Kotak expects ~0-2% q/q growth for Tier-1 IT in Q2FY27, says headwinds fall largely on incumbents, and that base-business deflation will … [0-2 % q/q revenue growth, Q2FY27E] | broker / company forecast model | press | agrees |
| IND-03e | Kotak Institutional Equities (2026c) | Kotak estimates gross AI-led deflation of ~7% and net deflation of 3.5% for IT companies, with muted Tier-1 growth in Q2FY27 and mid-tiers … [7 (gross) / 3.5 (net) % revenue deflation, FY27E] | broker / company forecast model | press | complements |
| IND-04b | J.P. Morgan (2026) | J.P. Morgan says AI deflation is only in its second year and expects further headwinds over the next two years; large caps to hover around … [3-4 % medium-term revenue growth (large caps), medium term (to ~FY30)] | broker / company forecast model | press | complements |
| IND-05a | ICICI Securities (2026) | ICICI Securities expects AI to deflate traditional IT services revenue by about 2-3% a year, peaking FY26-FY28, with recovery from end-FY28 … [2-3 % revenue deflation per year, FY26-FY28] | broker / company forecast model | primary | complements |
| IND-05b | ICICI Securities (2026) | About 30% of IT services is at risk from AI; base case (50% deflation of that segment) implies a ~USD 40bn hit to India, worst case (100% … [40 (base) / 80-85 (worst) USD bn revenue at risk, to ~FY29] | broker / company forecast model | primary | complements |
| IND-08a | HCLTech (2026) | HCLTech CEO says ~40% of the industry (app dev/support, traditional infra ops, customer support) is AI-disrupted and can shrink at a 3-5% … [3-5 (segment) / 2-3 (HCLTech) % CAGR shrink, FY27 onward, 'a few years'] | broker / company forecast model | primary | complements |
| IND-08d | Jefferies (2026) | Jefferies says application managed services (22-45% of revenue at several firms) could see sharp AI deflation; in its worst case FY26-31 … [15 % cumulative revenue deflation (worst case), FY26-FY31] | broker / company forecast model | press | complements |
| TT-04b | NITI Aayog (2025) | Assumes IT services industry revenue grows 3-9% a year and price-per-FTE grows 5-8% a year, so headcount implied roughly flat to modestly … [5-8 % per year price per FTE, next few years from 2025] | scenario model | primary | complements |
| WB-05b | Betai & Chen (2026) | Continuing workers' average contract value rose 41% and the top 1% captured a 17-20 pp larger share of jobs and earnings: fewer but … [41 % rise in avg contract value (continuing workers), Jan 2022-Dec 2024] | online-labour-platform contract microdata | primary | complements |
| ACA-03c | Humlum & Vestergaard (2026) | Adopters report average time savings of about 3% of work hours (Appendix; earlier 2025 version reported 2.8%). [3 % of work hours, 2023-2024 surveys] | Danish register data / CPS analysis outside our scope | primary | complements |
| ACA-05e | Stanford AI Index (2026) | Micro studies summarised: customer support +14-15% issues/hour, software developers +26% pull requests (Cui et al.), marketing +50% output … [26 % more pull requests (Copilot), 2023-2025 studies] | ADP payroll / Revelio profiles (proprietary) | primary | complements |
| ACA-06a | Becker et al. (2025) | RCT with 16 experienced open-source developers on 246 tasks: AI tools increased completion time by 19%, although developers forecast a 24% … [19 % slower (completion time increase), Feb-Jun 2025] | experiment / benchmark data | primary | complements |
| ACA-06b | METR (2026) | Late-2025 follow-up: returning developers -18% time with AI (speedup; 95% CI -38% to +9%, n=10), newly recruited -4% (CI -15% to +9%, … [-18 % change in completion time (negative = speedup), Aug 2025-early 2026] | experiment / benchmark data | primary | complements |
| ACA-06c | Kwa et al. (2025) | The 50% task-completion time horizon of frontier AI has doubled roughly every 7 months since 2019; Claude 3.7 Sonnet about 50 minutes. [7 months (doubling time), 2019-2025] | experiment / benchmark data | primary | complements |
| ACA-06d | METR (2026) | Updated suite: doubling time 196.5 days for the stitched 2019+ trend, 130.8 days (95% CI 107-161) since 2023, 88.6 days since 2024; top … [131 days (doubling time since 2023), 2019-Jan 2026] | experiment / benchmark data | primary | complements |
| ACA-06e | METR (2026) | Public frontier 50% time horizon about 12 hours (range 5-61); internal frontier at least 16 hours (point estimate 16-20); suite saturated … [12 hours (50% time horizon, public frontier), Feb-Mar 2026] | experiment / benchmark data | primary | complements |
| ACA-07a | Peng et al. (2023) | Lab RCT: developers with GitHub Copilot completed an HTTP-server task in JavaScript 55.8% faster than controls. [55.8 % faster, 2022] | experiment / benchmark data | primary | complements |
| ACA-07b | Cui et al. (2026) | Pooled field RCTs at Microsoft, Accenture and a Fortune 100 firm (4,867 developers): Copilot access raised completed pull requests 26.08% … [26.08 % more completed tasks (pull requests), 2022-2023] | experiment / benchmark data | primary | complements |
| ACA-07c | Brynjolfsson, Li & Raymond (2025) | AI assistant for 5,172 customer-support agents raised issues resolved per hour by 15% on average; lowest-skill quintile gained about 36% … [15 % more resolutions per hour, 2020-2021] | experiment / benchmark data | primary | complements |
| ACA-07d | Dell'Acqua et al. (2023) | 758 BCG consultants: inside the AI frontier, GPT-4 users completed 12.2% more tasks, 25.1% faster, with >40% higher quality; on a task … [12.2 % more tasks, 2023] | experiment / benchmark data | press | complements |
| HIR-12b | Unearthinsight via AIM (2026) | Gaurav Vasu (Unearthinsight) attributes about 60% of recent revenue-per-employee gains to workforce rationalisation and about 40% to … [60/40 % attribution, recent (FY26-Q1 FY27)] | press attribution of proprietary data | press | complements |
| IND-01e | Nasscom (2026) | Nasscom estimates FY26 AI-related revenue at USD 10-12bn, the first time it has given such an estimate; it notes not all firms report AI … [10-12 USD bn, FY26E] | industry-body estimate; method not public, revised each edition | press | complements |
| IND-05c | ICICI Securities (2026) | ICICI Securities sizes the incremental AI-led opportunity for IT services at USD 300-400bn by 2030. [300-400 USD bn TAM, by 2030] | broker / company forecast model | primary | complements |
| WB-01f | World Bank (2025) | By March 2025, 12% of business-services job postings required AI skills, vs 4% for other jobs, double pre-ChatGPT levels. [12 % of postings requiring AI skills, Nov 2022 vs Mar 2025] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | complements |
| WB-02f | World Bank (2026, SAEU Oct) | 23.4% of Indian firms report using some form of AI vs 42.7% of US firms (World Bank Enterprise Survey AI module 2025-26); gap wider for … [23.4 % of firms using AI, 2025-26] | Lightcast postings, FactSet links, Enterprise Survey (licensed) | primary | complements |
| WB-03a | World Bank (2026, IDU) | Among formal Indian firms with at least five employees, 23% use AI; adjusted for sophistication, adoption is about one-third of the US … [23 % of formal firms (5+ employees), 2025 (WBES)] | Enterprise Survey AI module; Goldman client note | primary | complements |
| ACA-01a | Brynjolfsson, Chandar & Chen (2025) | Early-career workers (22-25) in the most AI-exposed occupations saw a 13% relative employment decline after controlling for firm-level … [-13 % relative employment decline, late 2022-Jul 2025] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-01b | Brynjolfsson, Chandar & Chen (2025) | Employment of software developers aged 22-25 fell nearly 20% from its late-2022 peak by July 2025 (Section on case studies, Figure 1). [-20 % vs late-2022 peak (approx.), late 2022-Jul 2025] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-01c | Brynjolfsson, Chandar & Chen (2026) | Employment of 22-25-year-olds in AI-exposed occupations is 19% below where it would be had it kept pace with less-exposed peers (ADP … [-19 % below kept-pace counterfactual, Nov 2022-Jun 2026] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-01d | Brynjolfsson, Chandar & Chen (2026) | In levels, employment of 22-25-year-olds in the two most exposed quintiles fell about 11% while the three least-exposed quintiles grew … [-11 % change in employment (levels), Nov 2022-Jun 2026] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-01e | Brynjolfsson, Chandar & Chen (2026) | Most-exposed-quintile coefficient for ages 22-25 is -0.18 with no controls but halves to -0.09 (significant only at 10%) when occupational … [-0.09 log-point/proportional change vs least-exposed quintile (with education control), Nov 2022-Jun 2026] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-02a | Hosseini & Lichtinger (2026) | At GenAI-adopting firms, junior employment fell about 9% relative to non-adopters after six quarters from 2023Q1 (DiD and … [-9 % relative junior employment, 2023Q1-2024Q2 (six quarters)] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-02b | Hosseini & Lichtinger (2026) | Staggered event study: junior employment at adopters starts falling about two quarters after adoption and is about 8% lower after eight … [-8 % junior employment vs non-adopters, 8 quarters post adoption] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-02c | Hosseini & Lichtinger (2026) | Junior employment in high-exposure occupations fell about 7% relative to low-exposure occupations within adopters vs non-adopters … [-7 % relative junior employment (high vs low exposure), 2022Q4-2025Q1] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-03a | Humlum & Vestergaard (2026) | Danish admin data linked to adoption surveys: precise null effects of AI chatbots on earnings and recorded hours at worker and workplace … [2 % (upper bound of ruled-out effect), 2022-2024] | Danish register data / CPS analysis outside our scope | primary | contradicts |
| ACA-03b | Humlum & Vestergaard (2026) | No differential change in early-career employment share at workplaces encouraging chatbot use; estimates rule out effects greater than … [0.33 pp of early-career employment share (bound), Oct 2022-Dec 2024] | Danish register data / CPS analysis outside our scope | primary | contradicts |
| ACA-04b | Fairlie & Wu (2026) | Adding 'want a job' non-participants raises recent graduates' unemployment by nearly 2 pp (5.7% to 7.6% in their sample) but still shows no … [1.9 pp added by expanded unemployment definition, 2022-2026] | Danish register data / CPS analysis outside our scope | primary | complements |
| ACA-05c | Revelio Labs (2026) | US entry-level job postings are down about 35% since early 2023; Revelio notes this alone does not establish AI as the cause. [-35 % change in entry-level postings, early 2023-2026] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| ACA-05d | Stanford AI Index (2026) | Employment for US software developers aged 22-25 fell close to 20% from its 2022 peak by September 2025 (Figure 4.4.29), based on … [-20 % vs 2022 peak (approx.), 2022 peak-Sep 2025] | ADP payroll / Revelio profiles (proprietary) | primary | agrees |
| WB-05a | Betai & Chen (2026) | On a leading global online labour marketplace, GenAI cut outsourced contracts to developing-country freelancers by about 34% at mean skill … [-34 % of contracts at mean exposure, Jan 2022-Dec 2024] | online-labour-platform contract microdata | primary | agrees |
| ACA-08a | Demirci, Hannane & Zhu (2025) | Job posts for automation-prone freelance jobs (writing, coding) fell 21% relative to manual-intensive jobs within eight months of ChatGPT; … [-21 % change in job posts, Nov 2022-Jul 2023] | experiment / benchmark data | primary | agrees |
| ELA-01a | Bessen (2019) | Rough price-elasticity-of-demand estimates (Table 10.1): cotton 2.13 (1810) to 0.02 (1995); steel 3.49 (1860) to 0.16 (1982); autos 6.77 … [2.13->0.02; 3.49->0.16; 6.77->0.15 price elasticity of demand (absolute), 1810-2007] | not reproducible from free data | primary | complements |
| ELA-01c | Bessen (2015) | ATMs cut tellers needed per urban branch from 20 to 13 (1988-2004) but urban branches rose 43%, so teller jobs did not decline. [20->13; +43 tellers per branch; % change in branches, 1988-2004] | not reproducible from free data | primary | complements |
| ELA-02 | Tevlin & Whelan (2003) | Long-run elasticity of the computer capital stock with respect to its user cost is -1.6, nearly 9 times the aggregate equipment estimate. [-1.6 user-cost elasticity, 1960s-1990s] | not reproducible from free data | primary | complements |
| ELA-03 | Byrne, Corrado & Sichel (2018) | Hedonic AWS prices fell about 7%/yr (EC2 compute), >11%/yr (database) and ~17%/yr (storage) over 2009-2016, faster after 2014; AWS revenue … [-7 to -17 % per year (quality-adjusted price), 2009-2016] | not reproducible from free data | primary | complements |
| ELA-07 | Brynjolfsson (1996) | Integrating the BEA-based demand curve for IT, IT spending generated about $50-70bn in net consumer value in 1987 (about 3x its cost), … [50-70 USD bn consumer surplus (1987), 1987] | not reproducible from free data | primary | complements |

## Claims we checked and corrected

These are press or literature claims that our own data change. Use the corrected wording.

| claim as reported | what our check found | stance now | source of check |
|--|--|--|--|
| ICRIER: 'total employment in the sector has continued to grow' (contradicts C3) | Comes from ICRIER's own PLFS tabulation (Sec. 7, pp.32–33), not its survey, and covers 2021-22 → 2023-24 only. Our PLFS matches within ~1%. Since 2022-23 the change is +4.1% (90% CI −7.0% to +15.2%), not significant. | complements | `contradictions/FINDINGS_jobs.md` |
| Goldman: top six shed ~64k, rest of ecosystem added ~700k | Citable only via World Bank IDU (Oct 2026) p.41, citing a client-only Goldman note. −64k reproduced (−63,557). +700k most likely mixes two Nasscom vintages: ~0.24m is Nasscom adding GCCs to its count; like-for-like ~+0.39m (~3.4%/yr). Within PLFS CI even at face value. | −64k agrees; +700k complements (overstated) | `contradictions/FINDINGS_jobs.md` |
| Nasscom FY26 +135k (+2.3%) contradicts 'stopped adding jobs' | Compatible with PLFS (z = 0.12). Applies to the whole industry incl. GCCs; top six were −3.3k. Treat as ~2%/yr, unverified. Do not say 'sector employment is flat'. | complements | `contradictions/FINDINGS_jobs.md` |
| TCS 'about 15k below a year earlier' (our literature note) | Wrong: TCS is +4.7k YoY; −15k is vs Jun 2025. Q2 FY27 four-firm net +9,438, fresher-led; top six still −2.8% vs Mar 2023. | complements | `contradictions/FINDINGS_jobs.md` |
| Baldwin: India's back-office exports 27% above 2015–22 trend | Reproduced exactly from WTO data, but ~15 points predate ChatGPT (gap +15.4% at 2022Q4); post-ChatGPT increment ~+10%. Series includes ~$64bn of BPO/engineering RBI counts as software. | agrees (C1), smaller effect | `contradictions/FINDINGS_output.md` |
| ING: software exports 3.3% → 5.2% of GDP; DDS +45% vs world +32% | Reproduced on BoP (3.35% → 5.21%; +44.0% vs +32.0%). On the RBI survey the share is 4.62% → 5.66%, and was already 5.69% by FY23: mostly a BoP-measurement effect, largely pre-ChatGPT. | agrees (C1), with caveat | `contradictions/FINDINGS_output.md` |
| Economic Survey: AI-exposed exports up ~39.5% | Approximately replicated (0.361 vs 0.333). It is a relative DiD with a Q2 FY23 break that predates ChatGPT, not export growth. Software +41.5% raw on BoP vs +19.4% on the RBI survey and +7% for the top six. | agrees (C1), with caveat | `contradictions/FINDINGS_output.md` |
| Unearthinsight/AIM: revenue-per-employee gains ~60% workforce cuts, ~40% AI | RPE growth rates reproduced (Wipro aside). The 60% doesn't hold for FY19–26 (headcount rose); FY23–26 ~33% from fewer heads. The AI share is not identifiable. | complements | `contradictions/FINDINGS_output.md` |
| Broker deflation: Kotak 3.5%, ICICI 2–3%/yr, HCLTech 3–5% | Forecasts of gross deflation on parts of the portfolio. ICICI's 2–3% on 30% of revenue = 0.6–0.9pp of the portfolio. Our measured AI-specific give-back: ~0.4% FY26, ~1.5% expected FY27. | complements | `contradictions/FINDINGS_output.md` |
| Xpheno: 'net IT hiring fell from 600k (FY22) to 140k (FY26)' | Mislabel (ET, 23 Aug 2026): 600k is Xpheno's fresher-intake peak, not net hiring (Nasscom FY22 net adds ~230k; Xpheno's own FY26 IT net adds 110k). Read as gross fresher intake. Xpheno's FY22 peak itself drifted from ~450k to 600k. | complements | `fresher_thirdparty/FINDINGS.md` |
| LinkedIn: India entry-level hiring +168% (2023–25) | The 168% refers to hiring into micro-firms (1–10 employees) for the broad entry-level cohort (64% for bachelor's holders). Not total entry-level hiring, not IT. Do not cite as such. | complements (no longer a contradiction) | `contradictions/FINDINGS_entry_level.md` |
| Naukri: fresher postings +8% / +17% (Jan–Feb 2026) | All-industry postings, not hires, no campus hiring. Chained to 2022, fresher postings are only back to the 2022 level; IT-Software postings are 29–42% below 2022. The recovery is outside IT. | complements | `contradictions/FINDINGS_entry_level.md` |
| Future of India Substack: IT employment and graduate IT jobs 'peaked' in 2023-24; developers −14% | Shares reproduce (20.4% → 16.0% for salaried grads 21–25), but their levels are rescaled 1.16–1.22× ours. Excluding the high-weight 2023-24 cluster the series is flat since 2022-23; the developer fall is fragile (z ≈ 1.5) and coincides with the 2025 redesign. | complements | `contradictions/FINDINGS_entry_level.md` |
| Future of India Substack: labour's share of IT value added fell after 2023-24 | Methodological artefact. PLFS wage bill is far below firms' actual employee cost (top-6 alone exceeds the PLFS sector total); the fall comes from pairing the redesigned CY2025 PLFS with FY25 GVA. Accounts-based shares are flat (~0.71 top-6; RBI listed IT .687 → .686); KLEMS and NAS group shares rising. | complements (do not cite) | `labour_share/FINDINGS.md` |
| Future of India Substack: real IT pay peaked in 2023-24 | True only for juniors: real mean for all IT workers flat (51.0k → 49.5k); ages 21–25 −12% in CY2025 (35.2k → 30.9k, z ≈ 2). Use means; medians are heaped. | agrees (C4), narrower | `labour_share/FINDINGS.md; contradictions/FINDINGS_entry_level.md` |
| State of Working India: ~40% graduate unemployment, age 15–25 | Reproduced on principal status for 2023-24 (41.2%; weekly 38.2%; official ps+ss 34.5%). Rate has fallen since 2017-18. The 7% permanent-job transition figure is CMIE-only. | complements | `contradictions/FINDINGS_entry_level.md` |
| TeamLease: IT fresher intent 81% → 76% | True within the current regime, but the series breaks at 2025 H2 (sample ~650 → ~1,065); the earlier rise from 59 to 75 is not a demand change. | agrees (C4), weak | `fresher_thirdparty/FINDINGS.md` |
| Xpheno: entry-level tech openings −44% (Jun 2026) | June was the low; by Oct 2026 entry-level openings were +15% YoY and total openings at an 18-month high. The narrowing is in the entry-level share (16.1% → 12.2%), not the count. | complements | `fresher_thirdparty/FINDINGS.md; postings/FINDINGS.md` |
| Computerworld: top five added 17 net staff in 9M FY26 | We get +159; their 9M FY25 comparator adds back HCLTech's divested staff. Cite as 'roughly zero'. | agrees | `contradictions/FINDINGS_jobs.md` |
| EPFO payroll by industry 'available monthly' | Built from 66 archived PDFs; IT heading only in top-10 tables for ages 18–28. IT 18–25 net additions −31% FY22–25 (share 5.8% → 3.9%). EPFO stopped publishing after Sep 2025. | agrees (C4) | `epfo/FINDINGS.md` |

## Not found, or do not cite

- `JRN-03b` **Weijin Research (2026)** (unverified (press-only)): India is expected to have about 2,117 GCCs with 2.36m employees and about $100bn in revenue as of FY2026. — C3/GCCs. No source is given (probably NASSCOM-Zinnov), and the figures are projections. Do not cite from Weijin; trace them to NASSCOM-Zinnov if needed. Compare india300's 1,800+ centres / 1.9m staff (FY25, via IBEF).
- `HIR-13a` **EY (unverified)** (not found): Claimed: EY says entry-level IT roles are down 20-25%. The Rest of World article does NOT mention EY or this figure. — Do not cite as EY. Correction to literature report: the cited source does not contain it. Aggregators attribute the 20-25% to a 2025 EY analysis (via Storyboard18) or to NASSCOM, inconsistently. No EY primary found. EY …
- `IND-02d` **Swarajya (2026)** (unverified (press-only)): Press reports early-career talent at 30% of GCC hires and 4-10 years' experience at 56%, attributed loosely to the Nasscom-Zinnov 2026 report. — Not found in the 26-page Zinnov PDF (summary version); article mixes several sources (Business Today, ORF, TechRepublic) and gives no period. Also claims GCCs added ~200k net in FY26 vs 110k by IT services firms …
- `IND-07a` **BNP Paribas (2026)** (unverified (press-only)): BNP Paribas says GenAI is reducing demand for large labour-intensive teams, firms are passing productivity gains to clients, and large caps are more exposed via legacy contracts; decoupling revenue … — Qualitative only; single low-quality aggregator; no better coverage (ET/Mint/Moneycontrol) found before search budget ran out. Optional footnote at most.
- `WB-06b` **Stapleton & O'Kane (2021/2026)** (unverified (press-only)): Using UK online job adverts 2012-17, machine-learning deployment in UK firms raised services offshoring, especially to lower-income countries; India was the main beneficiary (ICT and … — C1. Paper not found online. Known only via the summary in Bastos & Nayyar (2026, pp.2-3) and a 2019 Oxford CSAE talk by Stapleton. Pre-GenAI (ML). The date is inconsistent: 2021 in Bastos & Nayyar, 2026 in Kruse & Yu. …
- `ELA-05` **Raissi & Tulin (2015)** (not found): Long-run price elasticity of Indian (goods) exports about -0.86. — Could not open (IMF Akamai block, elibrary 403); number carried from FINDINGS section 6, not re-verified. Goods exports, not services.
- `ELA-06` **McKinsey Global Institute (2003)** (not found): For each dollar of US corporate spending offshored to India, US firms save about 58 cents (total value creation ~$1.45-1.47, India captures ~33 cents). — Page timed out; search budget exhausted. Numbers are from memory/FINDINGS only -- do not cite until opened. Relevant to client price savings, not an elasticity.
- `ELA-08` **(gap)** (not found): No published market-level price elasticity of demand for outsourced IT/BPO services was found in this pass (search budget exhausted before a dedicated search). — Consistent with FINDINGS section 6. Gartner/academic search not completed -- follow-up needed.
- `JRN-05b` **Reuters Breakingviews (2026)** (unverified (press-only)): Podcast arguing that India is the most exposed economy to AI white-collar job loss, with hiring already slowing; a linked column warns that the AI job shock risks throttling consumption. — Only search snippets were available; the Stockopedia page returned 403. Forkast attributes a scenario to Breakingviews (a 30% cut in a 15m workforce -> ~5m fewer consumers, ~$75bn spending), which we could not verify. …
- `JRN-05d` **Mukherjee (2025)** (unverified (press-only)): Column arguing that Amazon's 14,000 corporate cuts signal generative AI moving beyond entry-level coding and threatening Indian white-collar outsourcing hubs. — Paywalled; only the opening and the Bloomberg Tax syndication snippet were seen. Opinion, no India data. Context only.
- `JRN-05e` **New York Times (2026)** (unverified (press-only)): Reportedly describes India's outsourcing industry as employing 6m+ people and worth nearly $300bn, with TCS headcount at about 580k (more than 20k below its 2022 peak); quotes the NASSCOM president … — nytimes.com is blocked for our tools. The date (27 Feb 2026) and headline gist come from a Reddit link and aggregators (bensbites, techloy); the exact title and author are unconfirmed. The 6m figure is NASSCOM's IT-BPM …
- `TT-10a` **RBI Bulletin / gap search** (not found): No 2026 RBI Bulletin article linking AI, GCCs and software exports was found; latest GCC piece is a 2024 Bulletin article seen only via secondary citation. — Web-search budget ran out before checking the RBI Bulletin archive directly; treat as incomplete.
- `TT-10c` **Indian academic gap search** (not found): No 2026 IIM/ISI/IGIDR paper using PLFS specifically on IT-sector employment or young IT graduates was found; closest are Great Lakes WP5 (economy-wide PLFS 2025) and SWI 2026. — Search incomplete (web-search budget exhausted). Supports novelty of our PLFS relative-pay result (C4).
- Elasticity priors: Raissi & Tulin (IMF WP/15/161, −0.86) and McKinsey Global Institute (2003, 58¢ saved per offshored dollar) were not re-located in this pass. The repo's elasticity FINDINGS marks Raissi & Tulin as confirmed earlier and McKinsey as unconfirmed; keep McKinsey out of the main text.

