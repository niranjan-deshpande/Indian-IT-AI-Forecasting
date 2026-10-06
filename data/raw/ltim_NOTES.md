# LTIMindtree (`ltim`), pre-merger L&T Infotech (`lti`) and Mindtree (`mindtree`): collection notes

Output: `data/raw/ltim.csv` has 9,751 rows. The `firm` column separates `lti` and `mindtree` (pre-merger standalone documents) from `ltim` (LTIMindtree documents, including the restated combined figures for pre-merger quarters). Nothing was summed.
Scripts: `scripts/extract/ltim_fetch_and_convert.sh` (downloads + pdftotext), `ltim_docs.py` (document index), `ltim_parse_tables.py` (layout-text table parser that assigns columns by header position), `ltim_build.py` (label → metric mapping, CSV writer), `ltim_hand_entered.csv` (hand-entered rows), `ltim_nse_announcements.py` / `ltim_nse_download.py` (NSE filings).
Local copies are in `data/sources/ltim/`: LTI/LTIM PDFs + `txt/`, `mindtree/nse/`, `lti_nse/`, `consol/`.

## VERDICT: is the merger break manageable?

**Partly. It is manageable for revenue, attrition and segment mix. It is NOT seamless for headcount and utilization.**

1. **A combined pro-forma series exists only from Q1FY22.** LTIMindtree accounted for the merger as a common-control combination and restated comparatives. The Addendum tables of the Q3FY23 and Q4FY23 fact sheets give combined quarterly figures for Q1FY22–Q2FY23 (6 pre-merger quarters). They cover USD revenue, QoQ growth (reported and cc), vertical and geography shares, client buckets, top-client shares, effort mix, utilization (excl. trainees), headcount (with split), and TTM attrition. Nothing combined was published for FY21 or earlier. The only other combined figure is the May-2022 merger deck's FY22 "Proforma (As-is)". That is a simple sum: USD 3,513mn revenue, 81,719 employees, and vertical/geo splits built by adding the two firms' own definitions. It was not collected as rows because it is annual, computed by adding, and has no quarterly detail. So the pre-FY22 history must come from the two standalone series (both available Q1FY16/Q2FY16–Q2FY23).
2. **Revenue aligns well.** LTI + Mindtree USD revenue vs the LTIM restated figure: Q1FY22 780.7 vs 780.3; Q3FY22 919.4 vs 918.4; Q1FY23 979.5 vs 979.5; Q2FY23 1,023.1 vs 1,021.9. Q4FY22 is the outlier at 954.2 vs 944.7 (−1.0%, probably FX translation or intercompany elimination; not explained in the documents). Summing the standalone series before FY22 is reasonable. It will overstate the combined level by roughly 0–1%.
3. **Headcount does not align.** The LTIM restated "Total Employees" is consistently 1.9–2.3k (about 2.8–3.0%) below LTI "Total Headcount" + "Total Mindtree Minds":

   | Quarter | Sum of standalones | LTIM restated | Gap |
   |---|---|---|---|
   | Q1FY22 | 65,554 | 63,696 | −1,858 |
   | Q4FY22 | 81,719 | 79,594 | −2,125 |
   | Q2FY23 | 89,271 | 86,936 | −2,335 |

   The gap grows over time, so the combined entity used a harmonised headcount definition that is narrower than one or both standalone definitions. The deck's 81,719 equals the simple sum. Splicing a summed pre-FY22 series onto the LTIM series therefore creates a level break of about −3% at the splice. Use the 6 overlap quarters to estimate a ratio adjustment, or splice on growth rates rather than levels.
4. **Utilization is definitionally inconsistent.** LTIM combined utilization excl. trainees runs above both parents: Q1FY22 86.1 vs LTI 84.1 and Mindtree 83.2 (incl. trainees); Q3FY22 84.0 vs 81.4 / 81.5. A weighted average cannot exceed both inputs, so the definitions differ. Specific differences:
   - Mindtree's fact sheet states "Billed Hours / Available Hours; available hours do NOT exclude leave".
   - From Q4FY21, Mindtree reports only one "Utilization" row. It equals the old incl-trainees series (Q4FY20 76.5% in both vintages). Mindtree excl-trainees ends Q4FY20.
   - LTI reports incl. and excl. trainees, computed from billed person-months (definition not stated).
   - LTIM reports excl. trainees only.
   - Also a break within LTIM in **Q1FY24**: the footnote attributes +1.6pp of utilization to reclassifying delivery staff to sales & support.
   Treat utilization as a series with a break at the merger; use the combined Q1FY22–Q2FY23 overlap only as a level shift.
5. **Attrition aligns.** All three report TTM/LTM attrition, and the LTIM restated figure falls between the parents: Q1FY22 14.5 vs 15.2 / 13.7; Q4FY22 23.8 vs 24.0 / 23.8. None of the fact sheets says whether this is voluntary or total attrition.
6. **Segments need a mapping.** LTI verticals (BFS, Insurance, Manufacturing, E&U, CPG-Retail-Pharma, Hi-Tech/Media, Others) and Mindtree verticals (CMT, BFSI, RCM, TTH, HealthCare) differ from the LTIM verticals (BFSI; Hi-Tech, Media & Entertainment → Technology, Media & Communications; Manufacturing & Resources; Retail/CPG/Travel/Transport & Hospitality → Consumer Business; Health, Life Sciences & Public Services).
   - Geography: LTIM uses North America / Europe / RoW. LTI splits out India and RoW. Mindtree splits UK & Ireland and Continental Europe.
   - Service-line shares stop at the merger: LTIM reports none.
   - Client buckets are summable only approximately. Clients are shared: active clients LTI + MT = 698 vs LTIM 608 in Q1FY22.
   - TCV is not comparable: LTI had no quarterly TCV table; Mindtree reported total TCV signed (renewals + new); LTIM reports "order inflow".

**Bottom line:** for revenue and attrition, a 2-firm sum from Q1FY16 to Q4FY21, spliced to the LTIM restated series from Q1FY22, is defensible (with a 6-quarter overlap to verify). For headcount, splice with a level adjustment (about −3%). For utilization and TCV, do not splice levels.

## 1. Sources

**LTI and LTIMindtree fact sheets.** The investor site is now **ltm.com** (ltimindtree.com redirects there; the company rebranded to "LTM" in 2026). Document listings come from an AEM JSON endpoint:
`https://www.ltm.com/content/ltimcorporatewebsite/us/investors/financial-results/jcr:content/root/container/investorfinancial.json?year=YYYY&investorType=ltimcorporatewebsite:investors/financial-results`.
This returns LTI documents for FY2017–FY2023 as well as LTIM documents. The "Earnings Release & Fact Sheet" PDFs (e.g. `.../uploads/investors/2019/10/Earnings-Call-Factsheet.pdf`) are the row sources. The URL list is in `data/sources/ltim/download_index.tsv`.
- Each LTI and LTIM fact sheet has 3 columns (Q-4, Q-1, Q) plus QoQ and YoY growth. Every column is kept as a separate vintage (doc_date differs).
- LTI Q1FY17–Q4FY17 give FY16 quarters as comparatives, so LTI covers Q1FY16 onward.
- The newest LTIM releases (Q4FY26, Q1FY27 "Investor Release") show 5 quarters.
- The Q3FY23 and Q4FY23 LTIM releases contain the combined **Addendum** (Q1FY22 onward).

**LTI broken PDFs.** Three fact sheets on ltm.com are image-only ("Microsoft: Print To PDF") or have garbled fonts: Q1FY20, Q1FY23 and Q4FY17. For these, text copies of the same release came from the NSE results filings (NSE symbol is now **LTM**):
- Q4FY17: `https://nsearchives.nseindia.com/corporate/LTI_Results_04052017164048.zip`
- Q1FY20: `.../listcontract3_18072019191541_larsen_outcome_387.pdf`
- Q1FY23: `.../LTI_14072022152621_OutcomeofBoardmeeting.pdf`

**Mindtree.** mindtree.com now redirects to ltm.com and the Mindtree PDFs are gone. The Wayback Machine (web.archive.org) was **"Temporarily Offline"** on every attempt during this session, so no archive copies were used. The source was instead the NSE corporate-announcement API (`https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=MINDTREE&...`). The results filing for each quarter embeds the full "Earnings release": Key Revenue / Client / Employee metrics, 3 columns each. The attachment URLs are in `data/sources/ltim/mindtree/nse/index.tsv`, and each row's source_url points to the NSE zip or PDF. For zips, source_loc says "PDF inside NSE zip".
- Q1FY16–Q1FY17 Mindtree filings are **scanned images**, containing only the financial statements and a short press release. Q2FY16–Q4FY16 and Q1FY17 metric tables come from the comparative columns of the Q2FY17–Q1FY18 releases (Ind AS basis).
- The FY16 press-release headline figures were **hand-entered** from the scanned PDFs as the original pre-Ind-AS vintage: revenue, growth, cc growth, active clients, headcount, gross additions, attrition, and Q4FY16 client buckets. This is the only Q1FY16 Mindtree data. There are no Q1FY16 segment shares, utilization or TCV.

**Skipped or blocked sources:**
- web.archive.org: offline all session.
- BSE API (`api.bseindia.com`): "Access Denied".
- Mindtree Q1FY21 results zip on NSE (`67LetterQ1Results_14072020133601.zip`): 0 bytes. Q1FY21 values exist only as comparatives in the Q2FY21 and Q1FY22 docs; Q1FY21 growth rates are missing.
- LTIM Q1FY27 consolidated-financials PDF: no text layer.
- Nothing required login or payment.

## 2. Coverage (quarter = fiscal quarter; all of these are continuous unless a gap is listed)

**lti (Q1FY16–Q2FY23):**
- Q1FY16–Q2FY23: revenue (USD and INR mn), headcount (+ Development / Sales & Support split), LTM attrition, utilization incl./excl. trainees, vertical / service-line / geography shares, Digital share (Q1FY19–Q4FY21), client buckets (USD1/5/10/20/50/100mn+, LTM), active/new clients, top-5/10/20 shares, effort and revenue offshore mix.
- Q1FY17–Q2FY23: revenue growth QoQ/YoY (reported and cc) and segment growth QoQ/YoY (USD; cc from the "Constant Currency Reporting" table).
- Not reported: quarterly TCV (only narrative large-deal mentions) and subcontracting cost (lumped into "Operating expenses").

**mindtree (Q2FY16–Q2FY23; plus Q1FY16 headline values only, hand-entered):**
- Q2FY16–Q2FY23: revenue, headcount (+ Software Professionals / Sales / Support split), LTM attrition, industry / service / geography shares, client buckets, active clients, TCV (total signed, renewals, new).
- Utilization excl. trainees: Q2FY16–Q4FY20. Incl. trainees (single "Utilization" row from Q4FY21): Q2FY16–Q2FY23.
- Gross/net additions and fixed-price share: Q2FY16–Q4FY20.
- Revenue offshore share: Q2FY16–Q4FY18.
- Effort offshore share: gap Q1FY19–Q1FY20.
- cc growth: from press text, Q2FY17 onward; missing Q1FY21.
- Subcontracting cost and employee cost (consolidated, INR mn): Q4FY21–Q2FY23 only (hand-entered; the line is broken out only in the FY22–FY23 filings).

**ltim (Q1FY22–Q1FY27; Q1FY22–Q2FY23 are restated combined):**
- Q1FY22–Q1FY27: revenue (USD), QoQ growth (reported and cc), headcount (+ split), TTM attrition, utilization excl. trainees, vertical and geography shares, client buckets, top-client shares, effort offshore mix.
- Q3FY23–Q1FY27: YoY growth and segment growth QoQ/YoY (USD; the Q4FY26 and Q1FY27 docs also give cc segment growth).
- Order inflow (`tcv`, USD bn): Q3FY23–Q1FY27. Q3FY23–Q3FY24 and Q1FY25 come from press text; the rest from tables.
- No service-line shares, no subcontracting cost, and no quantitative AI revenue or bookings in any fact sheet. AI is only narrative ("AI pivot", BlueVerse).

## 3. Definitional breaks and restatements

- **Merger:** effective Nov 2022; first combined quarter Q3FY23. Comparatives restated combined from Q1FY22 (see verdict).
- **LTI Q1FY18 reorganisation:** verticals changed from Energy & Process / Auto-Aero & Others to Manufacturing / Energy & Utilities / Others; service lines were renamed. The Q1FY18 fact sheet re-presents FY16–FY17 mix under the new classification (8-quarter table). Earlier vintages differ (e.g. RoW/India split, ADM 38.5 vs 40.0 in Q1FY17). Rows are flagged in notes.
- **LTI service lines re-cut again around FY20–FY21:** e.g. Enterprise Solutions Q1FY20 28.4% in older vintages vs 31.5% in newer ones; later "ADM and Testing" and "Cloud Infrastructure & Security". Rows are kept as reported.
- **Mindtree FY21 re-segmentation:** industries became CMT / BFSI / RCM / TTH / HealthCare; service lines became Customer Success / Data & Intelligence / Cloud / Enterprise IT; geographies became North America / Continental Europe / UK & Ireland / APAC & ME. Some accounts were reclassified in FY22 (footnote). "Digital" share was redefined around Q1FY19 (34.9 vs 47.5 across vintages).
- **Mindtree FY16 to FY17 Ind AS transition:** FY16 comparatives in the FY17 releases differ slightly from the originally reported FY16 press releases. Both vintages are kept.
- **Mindtree utilization:** from Q4FY21 there is a single "Utilization" row, mapped to incl-trainees (verified equal to the earlier incl-trainees series). Excl-trainees stops at Q4FY20. Definition: Billed Hours / Available Hours, where leave is not excluded.
- **LTIM Q1FY24:** +1.6pp of utilization came from reclassifying delivery staff to sales & support (footnote). The headcount split shifts too.
- **LTIM Q1FY27 segment reorganisation:** Financial Services / Consumer / Technology & Services / Production. Media & Entertainment moved out of TMC, and Healthcare, Life Sciences & Public Services moved into Consumer. Prior quarters were restated in the Q1FY27 document. Earlier LTIM vertical labels also changed wording over time: "Hi-Tech, Media & Entertainment" became "Technology, Media & Communications", "Retail, CPG, Travel, Transportation & Hospitality" became "Consumer Business", and "Health…" became "Healthcare…".
- **Headcount definitions:**
  - LTI: "Total Headcount" = Development + Sales & Support.
  - Mindtree: "Total Mindtree Minds" = Software Professionals + Sales + Support (Sales and Support are merged as "Sales & Support" in later docs).
  - LTIM: "Total Employees" = Software Professionals + Sales & Support.
  - None of them states whether subcontractors or trainees are included.

## 4. Judgment calls

- Metrics added beyond the vocabulary: `new_clients` (new clients added in quarter), `top_client_share` (dimension "Top 1/5/10/20/40", share of quarterly revenue), `revenue_share` with dimension "Digital" (dim_type `other`), and `headcount` with dim_type `other` for the sub-categories.
- `tcv` covers two different measures: LTIM "Order Inflow" in USD_bn, and Mindtree "Total Contract Value signed" in USD_mn (total plus renewals/new). The notes column says which is which.
- Segment growth columns in fact sheets are USD growth (basis `reported`) unless marked CC. LTI's "Constant Currency Reporting" table gives cc growth.
- Growth values are recorded against the document's own quarter.
- INR revenue is recorded alongside USD for cross-checks.
- Trivial label variants were unified: "Rest of World" → "Rest of the World", "Platiorm" → "Platform", and a truncated "High-Tech, Media &". Otherwise segment names are exactly as reported.
- Mindtree cc growth comes from press-release text by regex, e.g. "constant currency growth of 1.2% q-o-q" or "13.4% QoQ CC growth" (source_loc quotes the snippet).
- Hand-entered rows (flagged `hand-entered` in notes): the Mindtree FY16 press-release values (scanned), and Mindtree sub-contractor charges / employee benefit expense for Q4FY21–Q2FY23 (from the text layer of the consolidated results).
- Checks run:
  - Segment shares sum to 98.5–101.5 for every (document, quarter, dimension type): 574 of 574 pass.
  - Headcount, revenue, attrition and utilization agree across all vintages (only 1-unit INR rounding differences).
  - 14 random values were spot-checked against the PDF text.
  - That spot-check found a split-header misalignment (LTI Q4FY19 INR table), which was fixed. The remaining 26 rows assigned by column order rather than position were checked by hand and are correct.
