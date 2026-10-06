# Management statements on pricing, 2021–2026: timeline

Pilot: slowing headcount growth at Indian IT-services firms. This file pulls together **commentary-level evidence on g_p** (price per unit of work) from earnings calls of TCS, Infosys, HCLTech, Wipro, Tech Mahindra and LTIMindtree, with Cognizant and Accenture as comparators. Built 2026-10-05.

**How this was built.** I collected 183 earnings-call transcripts dated Jan 2021 to Oct 2026. The coverage table below lists them. Most came from local copies; the rest I downloaded from company IR sites into `data/sources/<firm>/transcripts_task3/`. I keyword-screened every transcript (price/pricing, deflation, discount, renewal, give back, pass on/through, productivity commitment/benefit/gain, consolidation, cost take-out, fixed price, outcome-based, realization, rate card/increase/cut, bill rate, COLA, like-for-like, cannibalization, commercial model). For each hit I read the surrounding passage and confirmed the speaker against the transcript. I kept only management statements; analysts appear only in context notes. Every quote below was **machine-checked as a verbatim substring** of the source text, with whitespace normalized and `...` marking an elision, and its page was re-derived from the PDF. Pages are PDF page indices, which can differ by about 1 from printed page numbers. Infosys transcripts are SEC 6-K HTML exhibits with no pagination.

All 389 verified rows are in `audit/price_calls_quotes.csv`. This timeline shows 159 of them: a selection of qualitative quotes plus **every quantified statement**. A further 10 quantified client case-study claims, which are not statements about the firm's own pricing, are listed in the appendix. `Q:` marks a number stated; `measured` marks a firm-reported figure, with an explanation.

Topic codes: `pricing_level`, `pricing_increase`, `renewal_terms`, `deflation`, `productivity_passthrough`, `other`.

## Timeline

### 2021H1

- **HCLTech Q3FY21** (2021-01-15) — C. Vijayakumar, President & Chief Executive Officer · `pricing_level`
  > “So, these are the qualitative factors from a pricing perspective. Nothing unusual, it is pretty much similar dynamics as well in the past.”
  — [HCLTech Q3FY21 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcl_tech_q3_2021_earnings_call_transcript_0.pdf), p. 18 · `HCLTech-00`
  _Context:_ Answer to analyst on post-COVID steady-state margin outlook; pricing described as normal.
- **Accenture Q2FY21** (2021-03-18) — KC McClure, Chief Financial Officer · `pricing_level`
  > “the business environment does remain competitive. And in some areas, we experience pricing pressure, but we are seeing signs of stability.”
  — [Accenture Q2FY21 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2021/q2fy21/q2fy21-conference-call-transcript.pdf), p. 14 · `Accenture-00`
  _Context:_ Answer to Ashwin Shirvaikar (Citi) asking about pricing/price-for-value. Accenture defines "pricing" as contract profitability / margin on the work sold, not bill rates.
- **TCS Q4FY21** (2021-04-12) — Rajesh Gopinathan, Chief Executive Officer and Managing Director · `pricing_level`
  > “From our side, pricing remains quite stable. In our industry, old services get priced differently and newer services have price resilience, but overall portfolio remains quite stable.”
  — [TCS Q4FY21 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2020-21/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202020-21%20Earnings%20Conference%20Call%20held%20at%202000%20hrs%20IST%20on%20Apr%2012,%202021.pdf), p. 14 · `TCS-01`
  _Context:_ Analyst (Sandeep Shah) noted peers reporting pricing pressure in some pockets.
- **Wipro Q4FY21** (2021-04-15) — Thierry Delaporte, Chief Executive Officer & Managing Director · `pricing_level`
  > “yes, there is a pressure on pricing, but not more than what we have seen for many, many years, frankly. And second is, when you are on the right offerings, when you provide the right talent, the clients are willing to pay”
  — [Wipro Q4FY21 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2020-2021/q4fy21/wipro-limited-q4-fy21-quarterly-investor-conference-call-transcript.pdf), p. 11 · `Wipro-01`
  _Context:_ Continuation of same answer; pricing pressure characterized as normal/structural, not elevated.
- **LTIMindtree Q4FY21** (2021-05-12) — Sanjay Jalona, Chief Executive Officer & Managing Director · `pricing_level`
  > “Divya, rates are stable, pricing is stable. ... Last year was about a lot of discounts, this year I don't want to preempt by saying we are able to increase pricing, so we will leave it at stable pricing right now.”
  — [LTIMindtree Q4FY21 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2021/05/Transcript.pdf), p. 18 · `LTIMindtree-02`
  _Context:_ LTI (pre-merger). Analyst (UBS) asked whether supply constraints let rates move up.

### 2021H2

- **HCLTech Q1FY22** (2021-07-19) — C. Vijayakumar, Chief Executive Officer & Managing Director · `renewal_terms` · **Q:** 2%-3% of revenue lost at renewal (M&A or client demanding better pricing)
  > “There is obviously some leakage which happens, because not 100% of the deals get renewed. Sometimes there is an M&A, sometimes they want a much better pricing which we are not able to. So, usually 2% to 3% is lost on those dimensions”
  — [HCLTech Q1FY22 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcl-earnings_call_transcript_19-7-2021q1fy22.pdf), p. 18 · `HCLTech-02`
  _Context:_ Response to question on revenue leakage vs peers.
- **Cognizant Q2CY2021** (2021-07-28) — Jan Siegmund, Chief Financial Officer, Cognizant Technology Solutions Corp. · `pricing_level`
  > “We see also continued pricing pressure in the more traditional services that we have been talking about in past quarters, where clients are seeking additional cost benefit and that pricing pressure in those more traditional type of services haven't changed at this point in time.”
  — [Cognizant Q2CY2021 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2021/q2/Q2-2021-Earnings-Transcript.pdf), p. 17 · `Cognizant-02`
  _Context:_ Same answer; pre-GenAI pricing pressure in legacy/traditional services.
- **TCS Q2FY22** (2021-10-08) — Rajesh Gopinathan, Chief Executive Officer and Managing Director · `deflation`
  > “Deals that come up for renewal five years later will benefit from all the technological progress that has happened in that period. So, when you compare it against the deal value of the last period versus the current period, that might seem optically to be a reduction. But remember that it also reflects the kind of efficiency gains”
  — [TCS Q2FY22 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2021-22/q2/Management%20Commentary/Transcript%20of%20the%20Q2%202021-22%20Earnings%20Conference%20Call%20held%20at%202000%20hrs%20IST%20on%20Oct%208,%202021.pdf), p. 15 · `TCS-04`
  _Context:_ Analyst asked whether legacy-renewal deflation would ease given supply crunch. Pre-GenAI statement that renewals structurally reprice lower due to technology-driven efficiency.
- **Wipro Q2FY22** (2021-10-13) — Thierry Delaporte, Chief Executive Officer & Managing Director · `pricing_level`
  > “There is opportunities to have these discussions with our clients. In this current context, our clients feel the same they are also exposed to attrition. ... Now, from a portfolio standpoint, I would say, I would still talk about a certain level of stability of the pricing.”
  — [Wipro Q2FY22 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2021-2022/q2fy22/wipro-limited-q2-fy22-quarterly-investor-conference-call-transcript.pdf), p. 11 · `Wipro-03`
  _Context:_ Analyst (Apurva Prasad) asked about propensity for rate card increases amid tight supply.
- **HCLTech Q2FY22** (2021-10-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `pricing_increase`
  > “Rate card increase, definitely, obviously, given the, the supply situation we are doing everything possible to get increases, definitely new deals are going in with a slightly higher price. Even negotiations, we are probably holding much more firmer on our price. Of course, existing customers, it's difficult.”
  — [HCLTech Q2FY22 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-oct14-2021_0.pdf), p. 14 · `HCLTech-03`
  _Context:_ Analyst asked about rate card increases; talent supply shortage context.
- **HCLTech Q2FY22** (2021-10-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `renewal_terms` · **Q:** renewal rates 97%-98% · **measured:** Firm-reported renewal rate (97-98%), stated as a recurring figure.
  > “I don't think renewal pressures or anything material to callout, as I said in the past renewal rates are 97%, 98%.”
  — [HCLTech Q2FY22 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-oct14-2021_0.pdf), p. 17 · `HCLTech-04`
  _Context:_ Analyst asked about renewal pressure in legacy infrastructure business.
- **LTIMindtree Q2FY22** (2021-10-22) — Sanjay Jalona, Chief Executive Officer & Managing Director · `pricing_increase`
  > “I think we are seeing increased rates in pockets ... We are seeing some increased rate realizations as well.”
  — [LTIMindtree Q2FY22 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2021/10/IntimationSigned.pdf), p. 10 · `LTIMindtree-04`
  _Context:_ LTI (pre-merger). Question on whether demand allows offsetting talent cost inflation via higher pricing.
- **Accenture Q1FY22** (2021-12-16) — KC McClure, Chief Financial Officer · `pricing_increase`
  > “we’re focused on pricing to absorb our higher labor costs. And one of the things that we can point out, Lisa, is that we were very pleased with the improved pricing that we had this quarter on our record bookings.”
  — [Accenture Q1FY22 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2022/q1fy22/q1-fy22-conference-call-transcript.pdf), p. 12 · `Accenture-03`
  _Context:_ Answer to Lisa Ellis (MoffettNathanson) asking whether Accenture can pass labor-cost inflation through to clients; KC adds improved pricing lags compensation in the P&L.

### 2022H1

- **TCS Q3FY22** (2022-01-12) — Rajesh Gopinathan, Chief Executive Officer and Managing Director · `pricing_increase`
  > “Yes Diviya, we are seeing a slight uptick in pricing in the current quarter. And we should be able to get some of it, but keep it balanced by the fact that in long term existing customer relationships, we will need to be more nuanced about it. But overall, there is definitely an expectation of a rising pricing environment.”
  — [TCS Q3FY22 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2021-22/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202021-22%20Earnings%20Conference%20Call%20held%20at%202000%20hrs%20IST%20on%20Jan%2012,%202022.pdf), p. 15 · `TCS-07`
  _Context:_ Analyst asked about pushing through price increases amid demand strength and supply constraints. Later in call Rajesh adds the pricing trend 'has an upward bias'.
- **Infosys Q3FY22** (2022-01-12) — Salil Parekh, Chief Executive Officer & Managing Director · `pricing_level`
  > “I think on pricing first we have seen some level of stability in what we saw in the specific deals that we closed in Q3 versus Q2. ... broadly we are seeing large enterprises for the first time in a very long time are seeing inflation in their daily environment and so are more open to having these discussions.”
  — [Infosys Q3FY22 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749122000004/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-03`
  _Context:_ Answer to Diviya Nagarajan asking if like-for-like pricing can rise given strong demand.
- **HCLTech Q3FY22** (2022-01-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `pricing_increase`
  > “the most sustainable lever that we believe which will help us will be to really get rate increases, and we are already we increased our price list, all the new bids go in at a much higher price. We have approached all our clients. So, clients are also responding quite positively.”
  — [HCLTech Q3FY22 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Jan14-2022-q3.pdf), p. 17 · `HCLTech-06`
  _Context:_ Margin discussion; industry cost structures changing (supply-side wage inflation).
- **TechM Q3FY22** (2022-02-01) — Rohit Anand, Global Head of Business Finance · `pricing_increase`
  > “When we think about the cost pressures, another big thing that we had articulated was price increases. And that's something that we are trying to have a great momentum going across the business units, because that's the inflationary environment, right, and hence, from a price perspective, that's an important lever that we'll have to drive.”
  — [TechM Q3FY22 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-22-earnings-transcript.pdf), p. 10 · `TechM-01`
  _Context:_ Answer on FY23 margin levers; inflation pass-through via client price increases.
- **Cognizant Q4CY2021** (2022-02-02) — Brian J. Humphries, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `pricing_increase`
  > “So, Darrin, first of all, pricing remained somewhat stable. ... But, of course, price increases can and have lagged talent related to cost increases.”
  — [Cognizant Q4CY2021 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2021/q4/Q4-2021-Transcript-(FactSet).pdf), p. 12 · `Cognizant-06`
  _Context:_ Answer to Darrin Peller on pricing vs wage inflation.
- **TCS Q4FY22** (2022-04-11) — Rajesh Gopinathan, Chief Executive Officer and Managing Director · `pricing_increase`
  > “Typically, in renewals and other aspects of ongoing relationships, there is a slight uptick in terms of the pricing that we are seeing. It could manifest itself as COLA clauses being better enforceable, or in terms of renewals at a slightly increased price points”
  — [TCS Q4FY22 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2021-22/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202021-22%20Earnings%20Conference%20Call%20held%20at%202000%20hrs%20IST%20on%20Apr%2011,%202022.pdf), p. 16 · `TCS-08`
  _Context:_ Same answer: fresh new deals face high competitive intensity; cumulative impact will take time.
- **Infosys Q4FY22** (2022-04-13) — Nilanjan Roy, Chief Financial Officer · `other` · **Q:** 1.6% sequential margin headwind (bundles working days, client contractual provision, pricing puts and takes) · **measured:** Reported Q4FY22 margin-walk component; pricing effect not separated from working days and a one-off client contractual provision.
  > “1.6% impact due to lower calendar working days, client contractual provision as explained above and other pricing puts and takes”
  — [Infosys Q4FY22 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749122000020/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-05`
- **Cognizant Q1CY2022** (2022-05-04) — Brian J. Humphries, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `pricing_increase` · **Q:** 20-30 bps margin expansion guidance attributed mainly to pricing
  > “So pricing is ultimately the factor that gives us an ability to maintain margin growth of 20 to 30 basis points for the year.”
  — [Cognizant Q1CY2022 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2022/q1/CORRECTED-TRANSCRIPT_-Cognizant-Technology-Solutions-Corp.(CTSH-US),-Q1-2022-Earnings-Call,-4-May-2022-5_00-PM-ET.pdf), p. 18 · `Cognizant-10`
- **Cognizant Q1CY2022** (2022-05-04) — Brian J. Humphries, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `renewal_terms`
  > “we're not the only company in the world approaching clients outside of standard renewal dates to intersect the classic rate card work.”
  — [Cognizant Q1CY2022 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2022/q1/CORRECTED-TRANSCRIPT_-Cognizant-Technology-Solutions-Corp.(CTSH-US),-Q1-2022-Earnings-Call,-4-May-2022-5_00-PM-ET.pdf), p. 19 · `Cognizant-11`
  _Context:_ Off-cycle rate card increases in 2022.
- **TechM Q4FY22** (2022-05-13) — Rohit Anand, Global Head of Business Finance · `pricing_increase`
  > “we've also seen in the second half a little bit of advantage come through for price, but that's lagging, the cost increases dramatically. So, when you look forward, one of the big levers that we'll continue to work on with our customers going to be price increase, right”
  — [TechM Q4FY22 transcript](https://insights.techmahindra.com/investors/tml-q4-fy-22-earnings-transcript.pdf), p. 5 · `TechM-02`
  _Context:_ Margin puts and takes; price increases lagging wage/supply-side cost inflation.

### 2022H2

- **TCS Q1FY23** (2022-07-08) — Rajesh Gopinathan, Chief Executive Officer and Managing Director · `pricing_increase`
  > “So, we're seeing smaller increases in existing ones and newer contracts coming in at better terms. Also with existing renewals, certain terms like COLA are much better being able to push through. But the aggregate impact of it is still not positive. So, our overall realization numbers ... are still negative on a sequential basis.”
  — [TCS Q1FY23 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2022-23/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202022-23%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20Jul%208%202022.pdf), p. 14 · `TCS-10`
  _Context:_ Analyst asked about expected price/realization improvement. Later in call: pricing conversations 'picking up momentum rather than losing momentum'.
- **Wipro Q1FY23** (2022-07-20) — Jatin Dalal, Chief Financial Officer · `pricing_level` · **Q:** offshore (India) realization is one-third of onsite
  > “realization is one-third in India. So, that has definitely played out in terms of IT services per employee realization coming down. I am not seeing from a pricing power standpoint, any concern where we are giving away price discounts.”
  — [Wipro Q1FY23 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2022-2023/q1fy23/wipro-limited-q1-fy23-quarterly-investor-conference-call-transcript.pdf), p. 10 · `Wipro-06`
  _Context:_ Analyst (Sandeep Shah) noted revenue per employee down 8% YoY and asked if traditional business faces higher pricing pressure; CFO attributes decline to offshore mix, not price discounts.
- **LTIMindtree Q1FY23** (2022-07-21) — Sudhir Chaturvedi, President (Sales) · `pricing_increase`
  > “we are not seeing any conversations on that. In fact, right now, just to cover the point on pricing, we are still able to get some price increase in pockets because there is still a gap between demand and supply, especially on new technology talent and clients are open to increases for hot skills.”
  — [LTIMindtree Q1FY23 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2022/07/Earnings-call-transcript-Q1FY2023.pdf), p. 11 · `LTIMindtree-08`
  _Context:_ LTI (pre-merger). "that" = pricing cuts; analyst asked about recession prep / reluctance to negotiate pricing.
- **Infosys Q1FY23** (2022-07-24) — Nilanjan Roy, Chief Financial Officer · `other` · **Q:** 0.5% margin tailwind from RPP increase (working days + provision reversal, partly offset by discounts) · **measured:** Reported margin-walk component; discount effect not separately quantified.
  > “These were offset by tailwinds of 0.5% due to increase in RPP from higher working days, a reversal of a client's contractual provision in our FS segment partially offset by discounts.”
  — [Infosys Q1FY23 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749122000036/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-06`
- **TechM Q1FY23** (2022-07-25) — Rohit Anand, Chief Financial Officer · `pricing_increase` · **Q:** ~50 bps QoQ EBIT margin benefit from pricing actions · **measured:** Firm-reported margin-walk component attributed to price increases (Q1FY23 vs Q4FY22).
  > “Specifically for current quarter walk versus last quarter, as I mentioned, we saw approximately a 50 bps expansion due to pricing actions”
  — [TechM Q1FY23 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-23-earnings-transcript.pdf), p. 7 · `TechM-04`
  _Context:_ Margin walk: pricing +50 bps vs salary/subcon/large-deal -100 bps.
- **TechM Q1FY23** (2022-07-25) — Rohit Anand, Chief Financial Officer · `pricing_increase` · **Q:** 50 bps margin impact from price increases; similar or better expected next quarter · **measured:** Reported margin impact of realized price increases.
  > “So we've sequentially quarter-over-quarter seen increase in the quantum of price increase we've got. This time the impact as I mentioned was 50 bps. What we look at next quarter is similar or better outcome of that.”
  — [TechM Q1FY23 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-23-earnings-transcript.pdf), p. 10 · `TechM-05`
  _Context:_ Analyst (Sandeep Shah) asked how much the 100-150 bps margin target depends on pricing.
- **HCLTech Q2FY23** (2022-10-12) — Prateek Aggarwal, Chief Financial Officer · `pricing_increase` · **Q:** realization + utilization > half of 115 bps services margin gain · **measured:** Firm-reported margin-walk attribution: realization (higher billing rates from existing and new projects) plus utilization contributed >57 bps of sequential services margin.
  > “So, the total impact of realization and utilization was more than half of that 115 basis points.”
  — [HCLTech Q2FY23 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q2_FY23_Transcript_0.pdf), p. 9 · `HCLTech-14`
  _Context:_ Preceding sentence: biggest factor is realization increase from existing customers/projects and new deals. Analyst later references "100 basis points increase in realization".
- **HCLTech Q2FY23** (2022-10-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `pricing_increase`
  > “in existing engagements and all the new deals that we have won since January, we had a significant price increase. In spite of the price increase, we've been able to continue to accelerate our bookings.”
  — [HCLTech Q2FY23 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q2_FY23_Transcript_0.pdf), p. 13 · `HCLTech-17`
- **Wipro Q2FY23** (2022-10-12) — Thierry Delaporte, Chief Executive Officer & Managing Director · `pricing_increase`
  > “Over the last quarters it has been the case, we’ve been able to raise prices with a lot of our clients, and we’ve really driven conscious focus on that”
  — [Wipro Q2FY23 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2022-2023/q2fy23/wipro-limited-q2-fy23-quarterly-investor-conference-call-transcript.pdf), p. 14 · `Wipro-09`
  _Context:_ Analyst (Manik Taneja) asked whether price increases remain a margin lever over next 6-9 months. Price increases framed as passing through supply-side/inflation cost pressure.
- **Wipro Q2FY23** (2022-10-12) — Thierry Delaporte, Chief Executive Officer & Managing Director · `pricing_increase`
  > “for the time being I believe that we should continue to expect price increase from our clients. Certainly, our view.”
  — [Wipro Q2FY23 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2022-2023/q2fy23/wipro-limited-q2-fy23-quarterly-investor-conference-call-transcript.pdf), p. 14 · `Wipro-10`
  _Context:_ Same answer; forward-looking expectation of continued price increases (late 2022).
- **Infosys Q2FY23** (2022-10-13) — Nilanjan Roy, Chief Financial Officer · `pricing_increase`
  > “We have seen discount, which used to be a quite large in terms of pricing, in terms of renewal etc., that definitely has come down. ... Some we have seen in terms of COLA clauses, we have seen a larger implementation of that - being able to push as the COLA increases.”
  — [Infosys Q2FY23 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749122000046/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-10`
  _Context:_ Answer to Aniket Pande on tone of pricing conversations.
- **TechM Q2FY23** (2022-11-01) — Rohit Anand, Chief Financial Officer · `pricing_increase` · **Q:** 50 bps margin benefit from price improvements (2nd consecutive quarter) · **measured:** Firm-reported margin-walk component from price improvements.
  > “price improvements which we had articulated before, we are continuing to work with customers & that has helped us in the quarter by 50 basis points, consecutively now for two quarters in a row”
  — [TechM Q2FY23 transcript](https://insights.techmahindra.com/investors/tml-q2-fy-23-earnings-transcript.pdf), p. 3 · `TechM-07`
  _Context:_ Prepared remarks margin walk; offset wage hike/inflation of ~120 bps.

### 2023H1

- **HCLTech Q3FY23** (2023-01-12) — Prateek Aggarwal, Chief Financial Officer · `pricing_increase` · **Q:** 30 bps margin gain from realization improvements · **measured:** Margin-walk attribution of realization (billing-rate) improvement: +30 bps this quarter.
  > “This quarter, we gained 40 basis points through pyramid optimization, deployment and billing of freshers as well as 30 basis points on top by realization improvements and other efficiencies”
  — [HCLTech Q3FY23 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q3_FY23_Transcript_0.pdf), p. 6 · `HCLTech-18`
  _Context:_ Prepared margin walk.
- **HCLTech Q3FY23** (2023-01-12) — Prateek Aggarwal, Chief Financial Officer · `pricing_increase` · **Q:** billing realization improvement: 1% (Q2FY23), 30 bps (Q3FY23) · **measured:** Reported billing-realization improvement figures for two consecutive quarters.
  > “we continue to see improvement in our billing realizations as well. So, last quarter was a 1%, this quarter, it's that 30 bps that I called out.”
  — [HCLTech Q3FY23 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q3_FY23_Transcript_0.pdf), p. 10 · `HCLTech-19`
- **Cognizant Q4CY2022** (2023-02-02) — Jan Siegmund, Chief Financial Officer, Cognizant Technology Solutions Corp. · `pricing_increase` · **Q:** Q4 2022 pricing contribution to gross margin 50% higher than all prior quarters of the initiative combined · **measured:** Firm-reported realized contribution of price increases to gross margin (relative magnitude only).
  > “the contribution of our pricing initiative to gross margin in the fourth quarter was the highest. So we have really built quarter-after-quarter momentum, and it was 50% higher than all other quarters together.”
  — [Cognizant Q4CY2022 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2022/q4/Cognizant-Technology-Solutions-Corp.(CTSH-US),-Q4-2022-Earnings-Call,-2-February-2023-5_00-PM-ET.pdf), p. 16 · `Cognizant-15`
  _Context:_ Answer to David Togut on 2023 gross margin.
- **Cognizant Q4CY2022** (2023-02-02) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `deflation`
  > “In fact, I would say, digital technologies is almost like a deflationary force in an inflationary economy.”
  — [Cognizant Q4CY2022 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2022/q4/Cognizant-Technology-Solutions-Corp.(CTSH-US),-Q4-2022-Earnings-Call,-2-February-2023-5_00-PM-ET.pdf), p. 15 · `Cognizant-16`
  _Context:_ Context: clients pursuing cost takeout/vendor consolidation.
- **Accenture Q2FY23** (2023-03-23) — KC McClure, Chief Financial Officer · `pricing_level`
  > “when we talk about pricing, it's the margin on the work that we sold. And that has been improving over the last 5 quarters, it's now stable, which we're really happy with.”
  — [Accenture Q2FY23 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2023/q2fy23/q2fy23-conference-call-transcript.pdf), p. 17 · `Accenture-12`
  _Context:_ Pricing turns from improving (5 quarters) to stable.
- **Infosys Q4FY23** (2023-04-13) — Nilanjan Roy, Chief Financial Officer · `renewal_terms`
  > “One is the renewal discounts, which clients come back when programs are ending. And basically, after productivity increases at the renewal stage, which we are just loosely calling discounts. That is something which we have really curved over the last few years, basically pushing back on the renewal because there are other ways we can get productivity as well.”
  — [Infosys Q4FY23 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749123000027/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-13`
  _Context:_ Answer to Keith Bachman on price reductions; "curved" (sic, = curbed). Renewal discounts = productivity give-backs at renewal.
- **HCLTech Q4FY23** (2023-04-20) — C. Vijayakumar, Chief Executive Officer & Managing Director · `pricing_level`
  > “I don’t believe there is going to be a price expansion in this environment, and I don’t think we have baked in that in the revenue or the margins. It’s primarily due to volume.”
  — [HCLTech Q4FY23 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q4_FY23_Transcript_0.pdf), p. 11 · `HCLTech-21`
  _Context:_ Analyst asked whether FY24 guidance is volume- or price-driven; marks end of the 2022 price-increase phase.
- **TechM Q4FY23** (2023-04-27) — Rohit Anand, Chief Financial Officer · `pricing_increase` · **Q:** ~1% (100 bps) FY23 margin expansion from price · **measured:** Firm-reported full-year margin bridge component attributed to pricing.
  > “The offset for the year were driven by pricing, we had communicated at the beginning of the year that we will target close to 1% of expansion due to price and that is what we've delivered close to that number.”
  — [TechM Q4FY23 transcript](https://insights.techmahindra.com/investors/tml-q4-fy-23-earnings-transcript.pdf), p. 5 · `TechM-11`
  _Context:_ FY23 prepared remarks margin bridge (EBIT 11.4% vs 14.5% FY22).
- **TechM Q4FY23** (2023-04-27) — Rohit Anand, Chief Financial Officer · `pricing_level`
  > “But on a broad-based perspective versus last year is going to be quite limited as an opportunity. ... So that's kind of what we'll drive and the pricing as a lever is going to be limited this year versus last year.”
  — [TechM Q4FY23 transcript](https://insights.techmahindra.com/investors/tml-q4-fy-23-earnings-transcript.pdf), p. 10 · `TechM-12`
  _Context:_ Analyst (Girish Pai) asked about pricing view for FY24 after FY23 price increases; carry-forward of FY23 increases only.
- **LTIMindtree Q4FY23** (2023-05-02) — Vinit Teredesai, Chief Financial Officer · `pricing_level`
  > “Pricing is pretty much stable. Just remember as DC has mentioned that in his opening remarks that the nature of the deals and the revenue profile is changing from the transformation to the cost takeouts, to that extent that's the change that is coming in.”
  — [LTIMindtree Q4FY23 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2023/05/Earnings-call-transcript-Q4FY2023.pdf), p. 9 · `LTIMindtree-12`
  _Context:_ Analyst asked about Q4 pricing given lower headcount/utilization but higher revenue.
- **Cognizant Q1CY2023** (2023-05-03) — Jan Siegmund, Chief Financial Officer, Cognizant Technology Solutions Corp. · `pricing_level`
  > “First, we expect the macroeconomic environment will impact pricing, which was a key lever for us in 2022 to help offset the elevated wage inflation.”
  — [Cognizant Q1CY2023 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2023/q1/Corrected-Transcript_CTSHQ1-2023-Earnings-Call-3-May-2023-5_00-PM-ET.pdf), p. 9 · `Cognizant-17`
  _Context:_ Prepared remarks on 2023 margin outlook; pricing tailwind ending.
- **Accenture Q3FY23** (2023-06-22) — KC McClure, Chief Financial Officer · `pricing_level`
  > “after five quarters of consecutive improvement in pricing - we mentioned last quarter that it's stabilized. And this quarter, we see the pricing is lower in some areas of our business.”
  — [Accenture Q3FY23 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2023/q3fy23/accenture-third-quarter-fiscal-2023-conference-call-transcript.pdf), p. 17 · `Accenture-13`
  _Context:_ Answer to Rod Bourgeois (DeepDive) asking about like-for-like pricing and contract terms in consulting and outsourcing.
- **Accenture Q3FY23** (2023-06-22) — Julie Sweet, Chair and Chief Executive Officer · `productivity_passthrough` · **Q:** at least 10% productivity per year (Managed Services)
  > “Every year, right, we have to find at least 10% of productivity. ... Our business model requires us to get at least 10% productivity year in and year out. ... we see generative AI as our ability to continue to give at least that 10% productivity year in and year out.”
  — [Accenture Q3FY23 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2023/q3fy23/accenture-third-quarter-fiscal-2023-conference-call-transcript.pdf), p. 11 · `Accenture-14`
  _Context:_ Answer to Lisa Ellis on GenAI impact; context is Managed Services, where productivity is given to clients annually; also notes 13,000 jobs automated YTD in operations.

### 2023H2

- **TCS Q1FY24** (2023-07-12) — N G Subramaniam, Chief Operating Officer and Executive Director · `productivity_passthrough`
  > “I don't know. It is not showing that much as being a differentiated feature in our contract discussions.”
  — [TCS Q1FY24 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202023-24%20Earnings%20Conference%20Call%20held%20on%20July%2012,%202023.pdf), p. 23 · `TCS-13`
  _Context:_ Analyst (Ankur Rudra) asked whether GenAI shows up in contract discussions as a source of price aggression in cost-takeout deals.
- **HCLTech Q1FY24** (2023-07-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** revenue -1.3% QoQ (Q1 with productivity benefits kicking in; not solely attributed) · **measured:** Reported revenue change (-1.3% QoQ) in a quarter where annual productivity benefits kick in; productivity share not separated.
  > “Q1 is seasonally a soft quarter for HCLTech. As you would know, a lot of productivity benefits for a number of deals kick in during this quarter. Our revenues declined 1.3% sequentially”
  — [HCLTech Q1FY24 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q1_FY24_Transcript_0.pdf), p. 2 · `HCLTech-24`
  _Context:_ Prepared remarks.
- **HCLTech Q1FY24** (2023-07-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** GenAI deflation expected at least 2-3 years away
  > “one of the key benefits are going to be around efficiency. So which means there will be some deflation, but I think it's at least two to three years away.”
  — [HCLTech Q1FY24 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q1_FY24_Transcript_0.pdf), p. 8 · `HCLTech-26`
  _Context:_ Same answer on GenAI price deflation.
- **Cognizant Q2CY2023** (2023-08-02) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough`
  > “The question is how much of the productivity has to be shared with the clients so that we stay competitive to win as well as keep a part of it for ourselves.”
  — [Cognizant Q2CY2023 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2023/q2/transcript/Corrected-Transcript_CTSHQ2-2023-Earnings-Call.pdf), p. 11 · `Cognizant-20`
  _Context:_ Answer to Lisa Ellis on internal GenAI deployment.
- **Infosys Q2FY24** (2023-10-12) — Nilanjan Roy, Chief Financial Officer · `other` · **Q:** 0.5% sequential margin benefit from cost optimization incl. utilization and pricing · **measured:** Reported margin-walk component; pricing share not separated.
  > “0.5% from cost optimization benefits, comprising of higher utilization, pricing, etc.”
  — [Infosys Q2FY24 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749123000057/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-15`
- **LTIMindtree Q2FY24** (2023-10-20) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “Whereas if you look at the efficiency or the cost takeout deals, you cannot really commit to that efficiency to the client unless it's a slightly longer tenure because you need to understand the environment and then do a few things in terms of whether it is Gen AI or whatever you say.”
  — [LTIMindtree Q2FY24 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2023/10/Earnings-call-transcript-Q2FY2024.pdf), p. 22 · `LTIMindtree-14`
  _Context:_ Efficiency commitments (incl. GenAI) built into longer-tenure cost-takeout deals.
- **Cognizant Q3CY2023** (2023-11-01) — Jan Siegmund, Chief Financial Officer, Cognizant Technology Solutions Corp. · `renewal_terms`
  > “Growth was negatively impacted by a large renewal that we signed earlier this year with a payer customer, which resulted in a lower revenue run rate, but meaningfully improved profitability.”
  — [Cognizant Q3CY2023 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2023/q3/transcript/Corrected-Transcript_CTSHQ3-2023-Earnings-Call.pdf), p. 8 · `Cognizant-22`
  _Context:_ Health Sciences segment, prepared remarks.

### 2024H1

- **TCS Q3FY24** (2024-01-11) — Samir Seksaria, Chief Financial Officer · `pricing_level` · **Q:** 60 bps margin improvement from productivity and realization · **measured:** Firm-reported margin bridge item (combined productivity + realization); not a price change per se.
  > “offset by 60 basis points improvement on account of efficiency improvements through productivity and realization”
  — [TCS Q3FY24 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202023-24%20Earnings%20Conference%20Call%20held%20on%20January%2011,%202023.pdf), p. 2 · `TCS-14`
  _Context:_ Prepared remarks, Q3 margin walk.
- **TCS Q3FY24** (2024-01-11) — Samir Seksaria, Chief Financial Officer · `pricing_level`
  > “Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is an outcome. You can measure it as revenue per FTE and you will notice that it has been improving”
  — [TCS Q3FY24 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202023-24%20Earnings%20Conference%20Call%20held%20on%20January%2011,%202023.pdf), p. 17 · `TCS-15`
  _Context:_ Analyst asked whether client negotiations were helping realization in a tough environment.
- **TechM Q3FY24** (2024-01-24) — Rohit Anand, Chief Financial Officer · `pricing_level`
  > “the wage inflation that we saw the annual hikes that we did at the beginning of the year with the market that we saw through the year didn't come up with equal and price increases. That's a big value drop.”
  — [TechM Q3FY24 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-24-earnings-transcript.pdf), p. 16 · `TechM-15`
  _Context:_ Explaining ~500 bps YoY margin decline: wage inflation not matched by client price increases, plus service revenue drop.
- **Infosys Q4FY24** (2024-04-18) — Salil Parekh, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “we have not seen so far the rate discussion, but we can certainly see in some instances, benefits where clients can do more work in terms of creating more output for the same type of effort. ... But we have not seen something which has come back on the rates in that sense.”
  — [Infosys Q4FY24 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749124000016/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-18`
  _Context:_ Answer to Keith Bachman asking if GenAI coding productivity leads clients to ask for lower billing rates.
- **HCLTech Q4FY24** (2024-04-26) — Prateek Aggarwal, Chief Financial Officer · `productivity_passthrough` · **Q:** Q1FY25 revenue expected ~-2% QoQ vs -1.3% in Q1FY24 (productivity pass back plus offshoring impact in a large FS deal)
  > “In Q1, as you know, there is the usual annual productivity pass back that we have for a large number of our clients and the same impact would be there this year as well. ... which is expected to land the Q1 revenues at about (-2%) versus the (-1.3%) that we had in the June quarter of last year.”
  — [HCLTech Q4FY24 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Apr26-2024.pdf), p. 8 · `HCLTech-27`
  _Context:_ Elided text says the extra decline vs last year comes from an offshoring impact in one large FS deal.
- **LTIMindtree Q4FY24** (2024-04-26) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `other` · **Q:** 80% of pipeline = cost takeout/consolidation
  > “There is still caution as far as discretionary spend is concerned, 80% of the pipeline that we have are still cost takeout, consolidation kind of opportunities.”
  — [LTIMindtree Q4FY24 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2024/04/Earnings-call-transcript-Q4FY24.pdf), p. 10 · `LTIMindtree-16`
  _Context:_ Demand-mix evidence (discretionary weak) rather than pricing per se.
- **Cognizant Q1CY2024** (2024-05-01) — Jatin Pravinchandra Dalal, Chief Financial Officer, Cognizant Technology Solutions Corp. · `pricing_level`
  > “By design, these deals come with an expectation of superior pricing than what is the pricing, which is inherent in the current work. So yes, there is a downward pressure on pricing, but it is nothing out of ordinary that one would expect in the current demand environment.”
  — [Cognizant Q1CY2024 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2024/q1/ctsh-q1-2024-earnings-call-transcript.pdf), p. 11 · `Cognizant-26`
  _Context:_ Answer to Bryan Keane on rate-card pressure; consolidation/productivity deals priced below incumbent work.
- **Accenture Q3FY24** (2024-06-20) — KC McClure, Chief Financial Officer · `pricing_level`
  > “we've had overall in our entire business continued pricing pressure.”
  — [Accenture Q3FY24 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2024/q3fy24/accenture-third-quarter-fiscal-2024-earnings-transcript.pdf), p. 22 · `Accenture-16`
  _Context:_ Answer to Keith Bachman (BMO) asking whether BPO pricing is under 'material duress' as a competitor said; Julie adds 'it's a tight market'.

### 2024H2

- **TCS Q1FY25** (2024-07-11) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough` · **Q:** GenAI software productivity 5%-25% in POCs; 5%-20% rule of thumb; 100-150 projects tested
  > “We have done POC’s also, close to more than 100, 150 projects where we have tested this out on terms of software productivity. It varies anywhere between 5% to 25%. ... But we do see about 5% to 20% depending on the type of project is thumb rule that's quite possible.”
  — [TCS Q1FY25 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202024-25%20Earnings%20Conference%20Call%20held%20on%20Jul%2011,%202024.pdf), p. 19 · `TCS-18`
  _Context:_ Analyst cited a 30% GenAI cost-saving figure. This is delivery productivity, not a stated price cut.
- **TCS Q1FY25** (2024-07-11) — K Krithivasan, Chief Executive Officer and Managing Director · `renewal_terms` · **Q:** 5%-20% productivity on certain program phases only
  > “I said the 5% to 20% productivity on certain phases of the programs are possible. I didn't say the entire project endto-end life cycle, we can get 5% to 20%.”
  — [TCS Q1FY25 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202024-25%20Earnings%20Conference%20Call%20held%20on%20Jul%2011,%202024.pdf), p. 20 · `TCS-19`
  _Context:_ Analyst (Sandeep Shah) asked whether large renewals see clients negotiating 5-20% reductions due to GenAI.
- **TCS Q1FY25** (2024-07-11) — K Krithivasan, Chief Executive Officer and Managing Director · `renewal_terms`
  > “Coming back to renewal, it's a common experience that the customers do experience a productivity improvement but what they also do at that time is usually they add more scope at the time of renewal so that it is to a great extent top line neutral for us and we also bring productivity.”
  — [TCS Q1FY25 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202024-25%20Earnings%20Conference%20Call%20held%20on%20Jul%2011,%202024.pdf), p. 20 · `TCS-20`
  _Context:_ Same exchange; productivity given at renewal offset by added scope.
- **HCLTech Q1FY25** (2024-07-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** 50% savings on outsourced DPO/testing spend
  > “The first is DPO and testing. I believe the benefits would be to the extent of 50% and we ourselves have delivered programs or delivering programs which is promising 50% savings from their current outsourced spend on DPO and testing.”
  — [HCLTech Q1FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/Hcltech-call-earnings-Jul12-2024.pdf), p. 14 · `HCLTech-32`
- **HCLTech Q1FY25** (2024-07-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** ADM productivity 10%-30%
  > “In ADM, we expect productivity improvement anywhere from 10% to 30% by adoption of a GitHub Copilot.”
  — [HCLTech Q1FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/Hcltech-call-earnings-Jul12-2024.pdf), p. 14 · `HCLTech-33`
- **HCLTech Q1FY25** (2024-07-12) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** ~10% incremental GenAI benefit in infrastructure/application operations
  > “the incremental benefit you would see would be in the range of 10%. That's what we expect.”
  — [HCLTech Q1FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/Hcltech-call-earnings-Jul12-2024.pdf), p. 15 · `HCLTech-34`
  _Context:_ Refers to infrastructure and application operations already automated with ML.
- **Infosys Q1FY25** (2024-07-18) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** 0.5% revenue benefit from improved realization (one-timers) · **measured:** Reported contribution of one-time realization to Q1FY25 revenue growth.
  > “This included benefit from improved realization from one-timers of 0.5%.”
  — [Infosys Q1FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749124000026/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-19`
- **Infosys Q1FY25** (2024-07-18) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** 0.8% margin benefit (Maximus: utilization + value-based selling); 0.4% margin benefit from realization · **measured:** Reported margin-walk components.
  > “0.8% benefit from Project Maximus largely from higher utilization and value-based selling, 0.4% from the improvement in realization mentioned above”
  — [Infosys Q1FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749124000026/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-20`
- **Wipro Q1FY25** (2024-07-19) — Srini Pallia, Chief Executive Officer & Managing Director · `renewal_terms`
  > “Deal tenures are definitely becoming shorter. Three-year to five-year deals are becoming more commonplace. The only deals where tenures exceed five years include optionalities and clients agree only when cost savings are front-loaded with potentially financial engineering involved.”
  — [Wipro Q1FY25 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2024-2025/q1fy25/q1fy25-earnings-transcript.pdf), p. 7 · `Wipro-16`
  _Context:_ Analyst (Gaurav Rateria) asked about deal tenor and new vs renewal mix. Front-loaded client savings implies upfront price concessions in long deals.
- **HCLTech Q2FY25** (2024-10-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** two-thirds of committed productivity already achieved
  > “Only one DPO deal which is significantly pre-announced where we are very well into implementing a lot of automation led by the previous version of AI Force, so which really helped us pass back the productivity. In fact, almost two-thirds of what we needed to achieve is already in place.”
  — [HCLTech Q2FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-call-earnings-oct14-2024-Transcript.pdf), p. 9 · `HCLTech-35`
  _Context:_ Analyst asked about AI-led productivity baked into deal wins (BPO deal); CVK later says it is a renewal.
- **Infosys Q2FY25** (2024-10-17) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** 80 bps margin benefit from Project Maximus (incl. realization) · **measured:** Reported margin-walk component; pricing not separated from utilization/subcon.
  > “80 basis points benefit from Project Maximus ... successes of that is visible in improved operating metrics like utilization, realization, subcontracting costs, etc.”
  — [Infosys Q2FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749124000034/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-21`
- **TechM Q2FY25** (2024-10-19) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough`
  > “there is a level of productivity that we can see coming from GenAI. But from what I understand, and it is quite evident in the pricing, that when people are making assumptions about deals that could be, have a five-year type tenure, they are assuming productivity in the out-years, which is not visible to me just now.”
  — [TechM Q2FY25 transcript](https://insights.techmahindra.com/investors/tml-q2-fy-25-earnings-transcript.pdf), p. 15 · `TechM-19`
  _Context:_ Analyst (Kawaljeet Saluja) asked about competitors' large-deal assumptions; Mohit says peers bake unproven GenAI productivity into deal pricing; TechM will not.
- **Cognizant Q3CY2024** (2024-10-30) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough`
  > “Equally, if you're in a fiercely competitive situation, you probably give it away to – you partially give it away to clients.”
  — [Cognizant Q3CY2024 transcript](https://cognizant.q4cdn.com/123993165/files/doc_financials/2024/q3/00/CTSH-Q3-2024-Earnings-Call-Transcript.pdf), p. 16 · `Cognizant-32`
  _Context:_ Bryan Keane asked whether pricing is roughly 20%-40% less; Ravi declined to give a number ("hard to put a number").

### 2025H1

- **Infosys Q3FY25** (2025-01-16) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** realization +3.6% over 9M FY25 · **measured:** Firm-reported realization increase over 9 months.
  > “One such area is realization, which has increased by 3.6% over 9 months, resulting from strong performance emanating from value-based selling track.”
  — [Infosys Q3FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000004/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-23`
- **Infosys Q3FY25** (2025-01-16) — Salil Parekh, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “So on the AI-driven productivity point, in general, what we see is whenever there is a productivity benefit, there is always sharing with clients. So in the AI-driven or the other, like outside of AI driven, we are not seeing a difference in the way it is being treated.”
  — [Infosys Q3FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000004/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-24`
  _Context:_ Answer to Surendra Goel citing a peer AI-driven productivity pass-back to a large client.
- **TechM Q3FY25** (2025-01-17) — Rohit Anand, Chief Financial Officer · `renewal_terms`
  > “There is obviously challenge at every renewal opportunity to pass on new technology benefits, right. So, I think that continues to be a discussion at each and every renewal that we do ... the discussions on renewals are paying in the new technology benefits, but I think we are seeing a decent renewal rate from a trend perspective.”
  — [TechM Q3FY25 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-25-earnings-transcript.pdf), p. 14-15 · `TechM-22`
  _Context:_ Analyst (Abhishek Kumar) asked about renewals and client asks for productivity pass-through pricing.
- **LTIMindtree Q3FY25** (2025-01-20) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `other`
  > “while AI may cannibalize some revenue, it offers substantial opportunity for growth and increased market share when strategically leveraged.”
  — [LTIMindtree Q3FY25 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/01/Earnings-Call-Transcript-Q3FY25.pdf), p. 4 · `LTIMindtree-18`
  _Context:_ Prepared remarks; references Investor Day Nov 2024.
- **LTIMindtree Q3FY25** (2025-01-20) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** TMC vertical +9.1% YoY, -5.5% QoQ cc · **measured:** Reported segment revenue change (-5.5% QoQ cc) that management links to AI productivity pass-back to top Hi-Tech client; not an isolated price measure.
  > “Technology, Media and Communications vertical grew 9.1% year-over-year and declined by 5.5% quarter-over-quarter in constant currency. Tech companies continue to be at the forefront of AI adoption. In the spirit of doing more for less, we are passing on AI-driven productivity benefits to our clients.”
  — [LTIMindtree Q3FY25 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/01/Earnings-Call-Transcript-Q3FY25.pdf), p. 7 · `LTIMindtree-19`
  _Context:_ First explicit AI productivity give-back; top client (Hi-Tech).
- **LTIMindtree Q3FY25** (2025-01-20) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** pass-back in effect ~2 months of Q3FY25, extends into Q4FY25
  > “The entire theme of doing more with less and the productivity benefits that we are talking about, I think you can probably say at least two months within this quarter, and which will also extend into the next quarter.”
  — [LTIMindtree Q3FY25 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/01/Earnings-Call-Transcript-Q3FY25.pdf), p. 13 · `LTIMindtree-20`
  _Context:_ Kawaljeet Saluja asked when the pass-on to the large client happened.
- **LTIMindtree Q3FY25** (2025-01-20) — Nachiket Deshpande, Chief Operating Officer · `productivity_passthrough`
  > “Where we are passing on the productivity benefit, we are actually generating those benefits and passing on. That's why it is relatively margin-neutral.”
  — [LTIMindtree Q3FY25 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/01/Earnings-Call-Transcript-Q3FY25.pdf), p. 14 · `LTIMindtree-21`
  _Context:_ Analyst then asked "So, it's not a pricing reset ... from that large account?"; Nachiket answered "No."
- **Accenture Q2FY25** (2025-03-20) — Angie Park, Chief Financial Officer · `pricing_level`
  > “So what are we focused on? Pricing, which this quarter was relatively stable.”
  — [Accenture Q2FY25 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2025/q2fy25/accenture-second-quarter-fiscal-2025-conference-call-transcript.pdf), p. 13 · `Accenture-19`
  _Context:_ On margin guidance; at p15 Angie reiterates 'relatively stable' after David Koning (Baird) notes pricing had been called down for ~7 quarters.
- **TCS Q4FY25** (2025-04-10) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough` · **Q:** Illustrative: work done for $100 delivered for $95 or $90 (5-10% gain shared)
  > “AI for IT, I won't try to call it deflation. ... And particularly, if there is AI for IT, because of AI if there is a productivity gain, we will try to share those gains with our customers. So, in that sense, that will be what we did with $100 if we are able to do with $95 or $90.”
  — [TCS Q4FY25 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202024-25%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20Apr%2010,%202025.pdf), p. 17 · `TCS-23`
  _Context:_ Analyst (Ankur Rudra) asked whether AI infusion causes deflation in the existing order book.
- **Wipro Q4FY25** (2025-04-16) — Aparna Iyer, Chief Financial Officer · `pricing_level`
  > “a lot of deals that we've spoken about which are a part of our pipeline are actually cost takeout and vendor consolidation deals which inherently come with pricing pressure and therefore are also very competitively fought.”
  — [Wipro Q4FY25 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2024-2025/q4fy25/q4fy25-earnings-transcript.pdf), p. 12 · `Wipro-19`
  _Context:_ Cited as margin headwind entering Q1FY26 alongside weak revenue environment.
- **Infosys Q4FY25** (2025-04-17) — Salil Parekh, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** 20%-40% client benefit in large customer-service programs
  > “Where for example, if there are large customer service programs, we see that there could be benefits to the clients of 20% to 40%. ... Sometimes, the client view are maybe larger than what we are seeing in realization and so, we have a choice to make there.”
  — [Infosys Q4FY25 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000010/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-27`
  _Context:_ Answer to Keith Bachman on deflationary nature of AI in pricing discussions.
- **HCLTech Q4FY25** (2025-04-22) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “we're winning higher wallet share with existing customers, even as we bake in Generative AI-induced productivity gains in our bids.”
  — [HCLTech Q4FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q4FY25-Transcript.pdf), p. 9 · `HCLTech-37`
  _Context:_ Prepared remarks.
- **HCLTech Q4FY25** (2025-04-22) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** software development 20%-25%
  > “Yes, so the level of deflation is something which is very dependent on what services are we delivering. ... And in software development, we are looking like 20% to 25% when we are able to implement and the maturity picks up.”
  — [HCLTech Q4FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q4FY25-Transcript.pdf), p. 18 · `HCLTech-38`
  _Context:_ Analyst asked level of deflation on existing business where AI efficiencies are passed back.
- **HCLTech Q4FY25** (2025-04-22) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** digital process operations 20%-50%
  > “In digital process operations, agentic solutions are very real. We believe there can be a significant reduction. ... There it can be anywhere between 20% to even 50%.”
  — [HCLTech Q4FY25 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q4FY25-Transcript.pdf), p. 18 · `HCLTech-39`
  _Context:_ Same answer.
- **LTIMindtree Q4FY25** (2025-04-28) — Vipul Chandra, Chief Financial Officer · `productivity_passthrough`
  > “It was productivity pass back as we had called out in Q3 and that is what it was. As we had said in our Q3 earnings call also, it had not affected the margins of our segment. So there is no pricing reset.”
  — [LTIMindtree Q4FY25 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/04/Earnings-Call-Transcript-Q4FY25.pdf), p. 22 · `LTIMindtree-24`
  _Context:_ Venu Lambu (CEO Designate) also said "There is no pricing reset that has happened." Analyst asked whether Hi-Tech client had a pricing reset.

### 2025H2

- **TCS Q1FY26** (2025-07-10) — K Krithivasan, Chief Executive Officer and Managing Director · `renewal_terms`
  > “Revenue conversion from signing is not impacted because of productivity. Because usually the productivity is given up at the time of signing.”
  — [TCS Q1FY26 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202025-26%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20Jul%2010,%202025.pdf), p. 20 · `TCS-27`
  _Context:_ Analyst asked whether AI-infused productivity pass-through would impact conversion of bookings to revenue.
- **HCLTech Q1FY26** (2025-07-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “if you allow us to use AI Force and use all the recipes that we’ve created, we will showcase to you the optimization that is possible. ... And it will mean some reduction in revenue for us. And we are okay with that.”
  — [HCLTech Q1FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1FY26-Transcript-18.pdf), p. 22 · `HCLTech-43`
- **HCLTech Q1FY26** (2025-07-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `renewal_terms` · **Q:** 8 of 9 renewals in quarter had higher total client revenue · **measured:** Firm-reported count of renewals (8 of 9) where total client revenue exceeded prior run rate despite productivity give-backs.
  > “in 8 of them, the total revenue from the client is higher than the existing run rate that we had. So, we have been able to get a little more wallet share, which more than offsets some of the productivity benefits that we have given.”
  — [HCLTech Q1FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1FY26-Transcript-18.pdf), p. 22 · `HCLTech-44`
  _Context:_ Preceding text: number of renewals done this quarter was 9.
- **HCLTech Q1FY26** (2025-07-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** SDLC 25%-30%; BPO 40%-50%
  > “It’s only in a software development lifecycle- 25% to 30% benefit is realistic. And in a lot of business process operations, we think it can be 40% to 50%. ... So, I think in these two areas, it will definitely create deflation.”
  — [HCLTech Q1FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1FY26-Transcript-18.pdf), p. 23 · `HCLTech-45`
  _Context:_ Analyst compared to IMS cannibalization by cloud. Elided text cites contact centers with people reduced by 75%.
- **Wipro Q1FY26** (2025-07-17) — Srini Pallia, Chief Executive Officer & Managing Director · `pricing_level`
  > “some of these large deal wins are very competitive. There will be price pressures on that. What matters is, how do you transition and how do you execute these deals.”
  — [Wipro Q1FY26 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2025-2026/q1fy26/q1fy26-earnings-transcript.pdf), p. 17 · `Wipro-21`
  _Context:_ Analyst (Sandeep Shah) asked whether mega-deal margin pressure reflects competitive pricing.
- **Infosys Q1FY26** (2025-07-23) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** 70 bps margin tailwind from realization increase · **measured:** Reported margin-walk component (includes seasonality).
  > “70 basis points from increase in realization due to Maximus and seasonality”
  — [Infosys Q1FY26 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000022/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-29`
- **Infosys Q1FY26** (2025-07-23) — Jayesh Sanghrajka, Chief Financial Officer · `pricing_increase` · **Q:** 3.5% pricing benefit in FY25 · **measured:** Firm-reported FY25 pricing benefit.
  > “last year, we did talk about 3.5% on terms of pricing benefit that we got. Of course, there were also low-hanging fruits that we captured.”
  — [Infosys Q1FY26 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000022/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-30`
  _Context:_ Answer to Kumar Rakesh on pricing/productivity benefit.
- **Cognizant Q2CY2025** (2025-07-30) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `renewal_terms`
  > “I would equally say that clients are looking for sharing productivity when the renewal cycles come.”
  — [Cognizant Q2CY2025 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q2/transcript/Transcript_CTSHQ2-2025-Earnings-Call.pdf), p. 10 · `Cognizant-37`
  _Context:_ Answer to Tien-Tsin Huang on early renewals tied to AI efficiencies.
- **Accenture Q4FY25** (2025-09-25) — Julie Sweet, Chair and Chief Executive Officer · `deflation`
  > “So we don't see AI as deﬂationary. We do see and are seeing it as expansionary similar to every tech evolution we've been through.”
  — [Accenture Q4FY25 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2025/q4-fy-25/accenture-fourth-quarter-fiscal-2025-conference-call-transcript.pdf), p. 14 · `Accenture-22`
  _Context:_ Answer to Tien-Tsin Huang (JPMorgan) asking about AI-driven productivity and potential deflationary effects.
- **Accenture Q4FY25** (2025-09-25) — Angie Park, Chief Financial Officer · `pricing_level`
  > “Let me just start on the pricing for our Gen AI projects and the pure Gen AI that we were -- or advanced AI that we've been talking about, we do see pricing that is accretive overall to average.”
  — [Accenture Q4FY25 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2025/q4-fy-25/accenture-fourth-quarter-fiscal-2025-conference-call-transcript.pdf), p. 17 · `Accenture-24`
  _Context:_ Answer to James Faucette (Morgan Stanley) on pricing of GenAI projects.
- **TCS Q2FY26** (2025-10-09) — Aarthi Subramanian, Executive Director, President and Chief Operating Officer · `productivity_passthrough` · **Q:** SDLC AI productivity 10%-15% initially, evolving toward 20%-25% (continues on next page)
  > “Again, starting to see good benefits coming in, but then there is an evolution, right? You start with single digits, 10% to 15% productivity, then there's an evolution”
  — [TCS Q2FY26 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q2/Management%20Commentary/Transcript%20of%20the%20Q2%202025-26%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20October%209,%202025.pdf), p. 22 · `TCS-29`
  _Context:_ Delivery productivity in software engineering; sentence continues on next page 'to reach 20%-25%'. Not stated as a price change.
- **HCLTech Q2FY26** (2025-10-13) — C. Vijayakumar, Chief Executive Officer & Managing Director · `renewal_terms` · **Q:** 5 of top 10 renewals with increased ACV; other 5 had SOW declines from AI productivity · **measured:** Firm-reported outcome of top-10 renewals: 5 up in ACV, 5 with AI-linked SOW declines.
  > “Five of our top 10 renewables came with increased ACV, while the specific SOWs in the remaining ones had a decline due to AI-linked productivity.”
  — [HCLTech Q2FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q2FY26-transcript-updated_0.pdf), p. 6 · `HCLTech-47`
  _Context:_ Prepared remarks.
- **HCLTech Q2FY26** (2025-10-13) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** 5 of top 10 renewals saw SOW deflation
  > “Other 5 of them had specific SOWs, which saw some deflation. But what is comforting is these are large clients of us. One segment of the work, there is some deflation.”
  — [HCLTech Q2FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q2FY26-transcript-updated_0.pdf), p. 19 · `HCLTech-48`
  _Context:_ Analyst noted net new bookings coming at the expense of renewals; CVK refers to "renewal deflation".
- **HCLTech Q2FY26** (2025-10-13) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** BPO 40%-50%; SDLC 25%-30%; IT Ops/app support 10%-15%
  > “We think the biggest impact is on the BPO business, which could be as much as 40% to 50%. In SDLC, 25% to 30% is what we think is doable with a lot of maturity. In IT Ops, application support and maintenance, it will be 10% to 15%”
  — [HCLTech Q2FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q2FY26-transcript-updated_0.pdf), p. 16 · `HCLTech-49`
  _Context:_ Analyst asked about AI impact on existing book of business.
- **TechM Q2FY26** (2025-10-14) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough` · **Q:** 80% productivity over five years (cited as unrealistic)
  > “while there is productivity expectation from customers, I think customers' expectations are becoming more realistic over time. ... Nobody's expecting, and if people are giving it, I know how they're giving it, 80% productivity over the next five years.”
  — [TechM Q2FY26 transcript](https://insights.techmahindra.com/investors/tml-q2-fy-26-earnings-transcript.pdf), p. 9 · `TechM-26`
  _Context:_ Analyst (Sudheer Guntupalli) asked whether AI is deflationary or expansionary for TechM.
- **Infosys Q2FY26** (2025-10-16) — Jayesh Sanghrajka, Chief Financial Officer · `deflation`
  > “We are at the forefront of leveraging AI and automation to increase productivity and offset pricing deflation.”
  — [Infosys Q2FY26 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749125000036/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-33`
  _Context:_ Manufacturing vertical commentary in prepared remarks.
- **Wipro Q2FY26** (2025-10-16) — Aparna Iyer, Chief Financial Officer · `deflation`
  > “In terms of just renewal, is there a deflationary pressure, like I said, every deal, every time there is a productive renewal, there is a productivity that gets passed on.”
  — [Wipro Q2FY26 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2025-2026/q2fy26/q2fy26-earnings-transcript.pdf), p. 15 · `Wipro-26`
  _Context:_ Analyst (Abhishek Kumar) asked whether deflation in renewals offsets new scope.
- **LTIMindtree Q2FY26** (2025-10-23) — Venu Lambu, Chief Executive Officer & Managing Director · `deflation`
  > “The price points did change. The renewal recalibration happened. We passed on the benefit to the customer as well at that time.”
  — [LTIMindtree Q2FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/10/earnings-call-transcript-q2fy26.pdf), p. 13 · `LTIMindtree-29`
  _Context:_ "Pre-productivity era" vs "post-productivity era" framing for BFSI/Tech (~60% of revenue).
- **LTIMindtree Q2FY26** (2025-10-23) — Venu Lambu, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** top-5 client bucket -5% · **measured:** Reported top-5 client revenue decline (-5%) attributed to productivity pass-on net of new business.
  > “we are talking about the top five bringing it minus 5%. ... because if you are just passing on the productivity benefit, you do not just degrow at minus 5%, it will be much higher.”
  — [LTIMindtree Q2FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/10/earnings-call-transcript-q2fy26.pdf), p. 22 · `LTIMindtree-34`
  _Context:_ Analyst asked if AI recalibration at renewals risks wallet share.
- **Cognizant Q3CY2025** (2025-10-29) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough` · **Q:** productivity up 30%
  > “So, productivity has gone up 30%, which means there is more throughput. So, you can actually create more throughput, share the savings, lower cost of deployment with our clients.”
  — [Cognizant Q3CY2025 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q3/transcript/Transcript_CTSHQ3-2025-Earnings-Call.pdf), p. 10 · `Cognizant-40`
  _Context:_ Answer on revenue per person (+8%) and margin per person (+10%).
- **Cognizant Q3CY2025** (2025-10-29) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `pricing_level`
  > “Right now, pricing is productivity-led, and it depends on how much you can use your platforms and how much you can use your AI tooling and the culture we have established now. So, pricing is kind of linked to how fast we can keep that runway on productivity.”
  — [Cognizant Q3CY2025 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q3/transcript/Transcript_CTSHQ3-2025-Earnings-Call.pdf), p. 14 · `Cognizant-41`
  _Context:_ Darrin Peller asked whether Cognizant passes AI savings through into price.
- **Accenture Q1FY26** (2025-12-18) — Angie Park, Chief Financial Officer · `other` · **Q:** ~60% of FY25 work fixed-price; +~10 pts over 3 years · **measured:** Firm-reported share of work that is fixed-price (commercial-model mix), not a price change.
  > “In FY25, about 60% of our work was ﬁxed-price, which is up about 10 points over the last three years.”
  — [Accenture Q1FY26 transcript](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/accenture-first-quarter-fiscal-2026-conference-call-transcript.pdf), p. 8 · `Accenture-25`
  _Context:_ Prepared remarks 'update on our commercial models'; attributed to proprietary platforms and clients wanting cost/delivery certainty.

### 2026H1

- **TCS Q3FY26** (2026-01-12) — K Krithivasan, Chief Executive Officer and Managing Director · `renewal_terms` · **Q:** 10%-15% productivity baked into renewals over contract term
  > “Even without AI coming to picture, most of the renewals have some productivity baked in. It could weigh in the range of 10%-15% over a term of the contract.”
  — [TCS Q3FY26 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202025-26%20Earnings%20Conference%20Call%20held%20on%20Jan%2012,%202026.pdf), p. 29 · `TCS-31`
  _Context:_ Analyst (Keith Bachman, BMO) asked the like-for-like price difference at renewal and price declines driven by AI. Preceding words (prev page): renewals bake in productivity as 'business as usual', not related to AI.
- **TCS Q3FY26** (2026-01-12) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough`
  > “it's fair to say most contracts assume a fairly aggressive AI productivity to come in and baking the expected productivity at the beginning of the contract itself. ... Most contracts assume a certain productivity over a period of time and are priced accordingly.”
  — [TCS Q3FY26 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202025-26%20Earnings%20Conference%20Call%20held%20on%20Jan%2012,%202026.pdf), p. 30 · `TCS-34`
  _Context:_ Analyst asked whether new contracts include gain-sharing flexibility; Krithi says flexibility is generally not built in.
- **TechM Q3FY26** (2026-01-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough` · **Q:** BFSI revenue -0.8% YoY (attributed to furloughs and annual productivity pass-through) · **measured:** Reported segment revenue change (BFSI -0.8% YoY); attribution to furloughs + productivity give-backs is commentary, give-back share not separated.
  > “BFSI declined 0.8% year-on-year, primarily due to higher than normal furloughs during the quarter and the passing of annual productivity gains to the large infrastructure contract in the rest of the world, which impacted revenues.”
  — [TechM Q3FY26 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-26-earnings-transcript.pdf), p. 3 · `TechM-28`
  _Context:_ First explicit statement that contractual productivity give-backs reduced reported revenue.
- **TechM Q3FY26** (2026-01-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough` · **Q:** ROW revenue -4% YoY (attributed to furlough and annual productivity gains) · **measured:** Reported geography revenue change (ROW -4% YoY); attribution to furlough + annual productivity gains is commentary, not separated.
  > “Revenue from the ROW declined by 4% YoY, primarily on account of furlough and annual productivity gains.”
  — [TechM Q3FY26 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-26-earnings-transcript.pdf), p. 3 · `TechM-29`
  _Context:_ Same large infrastructure contract in ROW.
- **TechM Q3FY26** (2026-01-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `renewal_terms`
  > “As far as the productivity benefit for a larger client that we have spoken about, again, the productivity stepped down because it is a multi-year contract, you have to take a step down every year.”
  — [TechM Q3FY26 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-26-earnings-transcript.pdf), p. 8 · `TechM-30`
  _Context:_ Analyst (Kumar Rakesh) asked about the BFSI productivity pass-through and whether more is to come; Mohit says it does not spill into the next quarter.
- **TechM Q3FY26** (2026-01-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `other`
  > “building a new pricing model itself, where the pricing for human labour and the pricing for digital labour is very clearly distinguished. And the pricing for digital labour is then based on token consumption, right?”
  — [TechM Q3FY26 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-26-earnings-transcript.pdf), p. 10 · `TechM-31`
  _Context:_ Asked how to measure AI revenue; cites white paper with Forrester on new pricing model.
- **Cognizant Q4CY2025** (2026-02-04) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough` · **Q:** fixed price ~50% of revenue vs 41-42% three years ago · **measured:** Firm-reported share of revenue that is fixed price (~50% vs 41-42% three years earlier): commercial-mix metric, not a price change.
  > “And we are very excited about the fact that our fixed price business now is almost 50%. I mean, three years ago, that used to be 41% to 42%. So, we can in some ways fixed price it, share the productivity of our clients and actually pass on some of it to ourselves.”
  — [Cognizant Q4CY2025 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q4/transcript/Transcript_CTSHQ4-2025-Earnings-Call.pdf), p. 12 · `Cognizant-44`
- **Cognizant Q4CY2025** (2026-02-04) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough` · **Q:** revenue per person +5% TTM; margin per person +8% TTM · **measured:** Firm-reported revenue per person (+5% TTM) and margin per person (+8% TTM); a per-FTE realization metric, not price per unit of work. Attribution to productivity sharing is commentary.
  > “Look at our revenue per person and margin per person. It's gone up by 5% trailing 12 months, 8% margin and 5% revenue trailing 12 months, which essentially means we are able to share with our clients the productivity win”
  — [Cognizant Q4CY2025 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q4/transcript/Transcript_CTSHQ4-2025-Earnings-Call.pdf), p. 14 · `Cognizant-45`
  _Context:_ Keith Bachman asked whether prices on fixed-price contracts are more aggressive.
- **Accenture Q2FY26** (2026-03-19) — Angie Park, Chief Financial Officer · `other` · **Q:** fixed-price >60% of work (FY25) · **measured:** Firm-reported fixed-price share of work, not a price change.
  > “Within bookings, the percentage of our work which is fixed price continues to increase over 60% in FY25.”
  — [Accenture Q2FY26 transcript](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/second-quarter-fiscal-2026-conference-call-transcript.pdf), p. 6 · `Accenture-28`
  _Context:_ Prepared remarks.
- **TCS Q4FY26** (2026-04-09) — Samir Seksaria, Chief Financial Officer · `pricing_level` · **Q:** Realization improvement = ~40 bps margin benefit (currency 110 bps) · **measured:** Firm-reported margin bridge: realization contributed ~40 bps in Q4FY26.
  > “During the quarter, we saw an improvement in realizations driven by continued focus on value-led delivery. Currency was also supportive during the quarter, providing a translation tailwind. These factors contributed to a beneﬁt of around 40 basis points and 110 basis points respectively.”
  — [TCS Q4FY26 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202025-26%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20April%209,%202026.pdf), p. 6 · `TCS-35`
  _Context:_ Prepared remarks.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** FY26 net new TCV $9.3B flat despite AI deflation · **measured:** Firm-reported net new TCV ($9.3B, flat YoY); size of AI deflation within it not quantified.
  > “TCV of net new bookings for the year clocked $9.3 billion, same as last year, in spite of some of the AI deflation that you see in the TCV net new booking.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 4 · `HCLTech-50`
  _Context:_ Prepared remarks.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** 40% of industry AI-disrupted; shrink 3%-5% CAGR; to 25% of spend
  > “40% of the industry runs the risk of being disrupted by AI and can shrink 3% to 5% CAGR for a few years and can eventually be 25% of the enterprise spend.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 10 · `HCLTech-51`
  _Context:_ Prepared remarks on industry segmentation.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** 3%-5% deflation in AI-disrupted services; 2%-3% for HCLTech portfolio
  > “And the 3% to 5% deflation that I mentioned in the AI disrupted services, based on the mix of services that we have, it would translate to 2% to 3% for our portfolio.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 11 · `HCLTech-52`
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** 2%-3% portfolio deflation; SDLC could be higher
  > “I think that piece could go through a little higher deflation based on the model outcomes. ... For us, we called out 2% to 3% and I think that holds true even now.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 16 · `HCLTech-53`
  _Context:_ Analyst asked risk of 3-5% deflation estimate expanding as models improve (SDLC piece).
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** 2%-3% deflation; FY27 guidance 2%-5%
  > “given it is a well-known fact that 2% to 3% deflation happens, I think barring this, getting to 2% to 5% is a reasonable growth in the given environment”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 18 · `HCLTech-54`
  _Context:_ Explaining FY27 revenue guidance.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** $100M deal now ~$80M; 25%-30% more effort to keep TCV flat
  > “$100 million deal would be much lesser today - maybe 80 million, just on a rough ballpark. So, deal TCV is flat. But technically, it does require at least 25%, 30% more effort to convert and get to the same number.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 21 · `HCLTech-55`
  _Context:_ Analyst asked about AI deflationary impact on deal TCV.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `pricing_level` · **Q:** >= $1B TCV walked away from
  > “We have walked away from some deals which will not make sense and that would have easily contributed at least $1 billion more to this number.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 21 · `HCLTech-56`
  _Context:_ Same answer continues: walked away from traditional deals that are hyper-competitive.
- **HCLTech Q4FY26** (2026-04-21) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation`
  > “No, I would say that very little has really played out in already reported numbers. We expect this to happen in FY'27 and onwards.”
  — [HCLTech Q4FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf), p. 23 · `HCLTech-58`
  _Context:_ Analyst asked whether poor demand of last years was partly AI deflation.
- **TechM Q4FY26** (2026-04-22) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough` · **Q:** 20% or 30% productivity (typical give-back framing, criticized)
  > “if you're thinking about AI and the only thing that you're doing is going and talking to a client saying, I'll give you 20% productivity or 30% productivity. It's really a very simplistic way of looking about how clients are thinking about deriving the benefit of AI.”
  — [TechM Q4FY26 transcript](https://insights.techmahindra.com/investors/tml-q4-fy-26-earnings-transcript.pdf), p. 10 · `TechM-34`
  _Context:_ April 2026 Analyst Day; proposes service-token pricing mixing human and digital labour instead of flat productivity commitments.
- **TechM Q4FY26** (2026-04-22) — Atul Soneja, Chief Operating Officer · `other` · **Q:** 7% AI-only productivity improvement in programs · **measured:** Firm-measured internal delivery productivity (not a price change).
  > “We started measuring the true AI-led productivity improvement in our programs starting last year and 7% improvement might not sound much but I think it's a very healthy start with respect to AI-only led productivity improvement.”
  — [TechM Q4FY26 transcript](https://insights.techmahindra.com/investors/tml-q4-fy-26-earnings-transcript.pdf), p. 17 · `TechM-37`
  _Context:_ April 2026 Analyst Day; measured labor-productivity effect of AI in delivery.
- **Infosys Q4FY26** (2026-04-23) — Jayesh Sanghrajka, Chief Financial Officer · `other` · **Q:** 0.75%-1% FY27 revenue guidance reduction from one client · **measured:** Firm-quantified revenue impact, attributed to client spend cut (macro) and deal selection, not pricing.
  > “Reduction of 0.75% to 1% due to lower revenue from one of our large European manufacturing client. This was due to reduced client spend on account of challenging macro environment, along with our conscious decision to not pursue certain deals that were not aligned to our return expectations.”
  — [Infosys Q4FY26 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749126000018/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-41`
  _Context:_ Useful as a demand-side (not AI-pricing) attribution.
- **Infosys Q4FY26** (2026-04-23) — Jayesh Sanghrajka, Chief Financial Officer · `productivity_passthrough`
  > “So Yogesh, market is competitive. As I said, the competitive intensity in the market has gone up and the productivity will get passed back to the client largely.”
  — [Infosys Q4FY26 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749126000018/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-42`
  _Context:_ Answer to Yogesh Aggarwal asking why productivity pass-through hurts margins.
- **LTIMindtree Q4FY26** (2026-04-29) — Vipul Chandra, Chief Financial Officer · `productivity_passthrough` · **Q:** EBIT margin -100 bps QoQ to 15.1% · **measured:** Reported margin decline partly attributed to productivity commitments in key accounts (not separately quantified).
  > “Q4 operating EBIT margin declined by 100-basis points sequentially to 15.1%. The decline was primarily on account of partial wage hikes implemented from 1st January and due to productivity commitments, we have made in key accounts offset by the Forex benefit.”
  — [LTIMindtree Q4FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/04/earnings-call-transcript-q4fy26.pdf), p. 13 · `LTIMindtree-38`
  _Context:_ Prepared remarks.
- **LTIMindtree Q4FY26** (2026-04-29) — Venu Lambu, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** planned 4 months compressed into 3 months
  > “The AI productivity journey started in Q3. In fact, in the later part of Q2, went up in Q3. And I said that in the Q3 earnings call, the plan was to go for another four months, but we wanted to squeeze it in three months.”
  — [LTIMindtree Q4FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/04/earnings-call-transcript-q4fy26.pdf), p. 27 · `LTIMindtree-40`
  _Context:_ Top BFSI account productivity give-back timing.
- **LTIMindtree Q4FY26** (2026-04-29) — Venu Lambu, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** FY26 growth 3.7% despite top-account decline · **measured:** Reported FY26 revenue growth (3.7%); pass-back impact not separately quantified.
  > “Yes even if you look at the whole year performance of 3.7% for the full year, in spite of having a decline in that category of that account that you are highlighting, we still grew, right?”
  — [LTIMindtree Q4FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/04/earnings-call-transcript-q4fy26.pdf), p. 19 · `LTIMindtree-41`
  _Context:_ Continues: "if I did not have this productivity journey going through in the top account, we probably would have delivered much more."
- **Cognizant Q1CY2026** (2026-04-29) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `pricing_level`
  > “unlike in the past where pricing was determined by the unit price which is billing rate equivalent, the race now is about the number of units and how well we could deliver with lower number of units for the same output, for the same outcome.”
  — [Cognizant Q1CY2026 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q1/transcript/Transcript_CTSHQ1-2026-Earnings-Call.pdf), p. 10 · `Cognizant-46`
  _Context:_ Jason Kupferberg asked about competitor comments on more pass-through of AI productivity and irrational pricing.
- **Accenture Q3FY26** (2026-06-18) — Angie Park, Chief Financial Officer · `other` · **Q:** fixed-price >60% of work · **measured:** Firm-reported fixed-price share, not a price change.
  > “We continue to see our fixed price work be over 60% and continuing to increase. ... So margins, not a big difference that I would call out relative to fixed-price versus the other commercial constructs”
  — [Accenture Q3FY26 transcript](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/accenture-third-quarter-fiscal-2026-conference-call-transcript.pdf), p. 23 · `Accenture-31`
  _Context:_ Answer to Jamie Friedman (Susquehanna). No explicit pricing-level statement found in this call; Julie also describes shift to more non-FTE commercial models (p4).

### 2026H2

- **TCS Q1FY27** (2026-07-09) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough` · **Q:** Productivity gain passed on ~10%-15%
  > “One quantiﬁcation I can give you is in most places, the productivity gain passed on is around 10% to 15% range.”
  — [TCS Q1FY27 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf), p. 12 · `TCS-40`
  _Context:_ Same exchange; most explicit quantified pass-through statement.
- **TCS Q1FY27** (2026-07-09) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough` · **Q:** AI productivity ~10%-15% over project tenure
  > “What I said is, there is an overall productivity we are able to achieve, about 10% to 15%, when we leverage AI for client engagements. You should look at that productivity gain coming through the tenure of the project. And we also mentioned that this usually is compensated by additional opportunities that we generate from the customers.”
  — [TCS Q1FY27 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf), p. 23 · `TCS-41`
  _Context:_ Analyst asked whether 10-15% is ACV or TCV basis and referenced a claim that $1T services spend could compress by ~$300B.
- **TCS Q1FY27** (2026-07-09) — K Krithivasan, Chief Executive Officer and Managing Director · `productivity_passthrough` · **Q:** 10%-15% average productivity; front-loaded commitment
  > “By and large, as I said, it's a rule of thumb, saying we can expect a 10% to 15% productivity on average. But we are able to o er a front loaded commitment to our customers which we are able to balance it out, to smoothen it out over the term of our project.”
  — [TCS Q1FY27 transcript](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf), p. 24 · `TCS-43`
  _Context:_ Analyst asked whether productivity (typically 3-5% annually) is spread evenly over a 5-year deal.
- **HCLTech Q1FY27** (2026-07-13) — C. Vijayakumar, Chief Executive Officer & Managing Director · `productivity_passthrough`
  > “AMJ is typically a weaker quarter for us due to planned revenue declines driven by productivity commitments in large managed services contracts.”
  — [HCLTech Q1FY27 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1-FY27-Transcript.pdf), p. 3 · `HCLTech-59`
  _Context:_ Prepared remarks.
- **HCLTech Q1FY27** (2026-07-13) — Shiv Walia, Chief Financial Officer · `productivity_passthrough` · **Q:** 110 bps margin headwind (annual productivity benefits + ERS decline) · **measured:** Firm-reported EBIT margin bridge item (combined with ERS revenue decline).
  > “This tailwind was offset by 110 basis points headwind from the seasonality due to annual productivity benefits and decline in ERS revenue.”
  — [HCLTech Q1FY27 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1-FY27-Transcript.pdf), p. 14 · `HCLTech-61`
  _Context:_ Margin walk.
- **Wipro Q1FY27** (2026-07-16) — Aparna Iyer, Chief Financial Officer · `productivity_passthrough`
  > “Wherever the intention is to use AI for you to be able to drive higher productivity and take costs out for a large operations for a client where the cost take-out is priority, you will see that, there will be a lot of productivity, forward productivity that gets baked into deals.”
  — [Wipro Q1FY27 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/q1fy27-earnings-transcript.pdf), p. 13 · `Wipro-33`
  _Context:_ Analyst (Vibhor Singhal) asked about margins on AI-driven deals.
- **Wipro Q1FY27** (2026-07-16) — Srini Pallia, Chief Executive Officer and Managing Director · `other`
  > “the traditional IT, the traditional BPO that we do and the support aspects of it, those budgets are getting compressed.”
  — [Wipro Q1FY27 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/q1fy27-earnings-transcript.pdf), p. 14 · `Wipro-35`
  _Context:_ Analyst (Abhishek Bhandari) asked about competitive intensity and margin pressure. AI reallocating client spend away from traditional run work.
- **TechM Q1FY27** (2026-07-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `productivity_passthrough` · **Q:** 70%-80% productivity benefit over 5-year deals (competitor offers; TechM holds back)
  > “I think one example is obviously the level of productivity baked into, 5 to 7 year deals. Now, obviously, we want to make sure that we are aggressive, but getting into a 70%, 80% productivity benefit over a 5-year deal, I feel is getting into productivity benefits that are not visible today”
  — [TechM Q1FY27 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-transcript.pdf), p. 15 · `TechM-43`
  _Context:_ Analyst (Kawaljeet Saluja) asked for examples of 'irrational' competition.
- **TechM Q1FY27** (2026-07-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `other`
  > “our productivity for our fixed price engagements was below our expectations, and so we've driven with the help of the new AI tooling a higher level of productivity, which has meant lower headcount.”
  — [TechM Q1FY27 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-transcript.pdf), p. 17 · `TechM-46`
  _Context:_ Analyst (Surendra Goyal) noted IT services headcount down 7% YoY; Mohit says revenue up, headcount down via AI in fixed-price work (labor per unit falling, gains retained as margin).
- **LTIMindtree Q1FY27** (2026-07-16) — Venu Lambu, Chief Executive Officer & Managing Director · `deflation`
  > “The productivity-linked pricing conversations we have had with some of our large clients are now behind us. That transition is complete”
  — [LTIMindtree Q1FY27 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/07/earnings-call-transcript-q1fy27.pdf), p. 15 · `LTIMindtree-43`
  _Context:_ Prepared outlook; firm now LTM Limited.
- **LTIMindtree Q1FY27** (2026-07-16) — Venu Lambu, Chief Executive Officer & Managing Director · `deflation` · **Q:** order book USD 1.7bn vs USD 1.7bn last year · **measured:** Reported order book (USD 1.7bn, flat YoY); the deflation adjustment within it is not quantified.
  > “you should assume that there is a natural deflation adjustment that has happened, so it is not fair to say USD 1.7 billion is the same as USD 1.7 billion of last year, so that means we are delivering more work for the same amount of order book”
  — [LTIMindtree Q1FY27 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/07/earnings-call-transcript-q1fy27.pdf), p. 34 · `LTIMindtree-45`
  _Context:_ Second (re-scheduled) call; analyst asked about reaching USD 2bn+ bookings.
- **LTIMindtree Q1FY27** (2026-07-16) — Venu Lambu, Chief Executive Officer & Managing Director · `deflation` · **Q:** ~15% lower price for same scope vs a year ago
  > “the same requirement or the same deal, I would have priced probably, let us say, 15% higher a year back, but the same scope of work I am picking up at, let us say, 15% less.”
  — [LTIMindtree Q1FY27 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/07/earnings-call-transcript-q1fy27.pdf), p. 36 · `LTIMindtree-46`
  _Context:_ Analyst asked if 15%-20% AI deflation is built into deals; Venu said "it is fair".
- **LTIMindtree Q1FY27** (2026-07-16) — Venu Lambu, Chief Executive Officer & Managing Director · `deflation`
  > “All the new deals that we are pricing anyway as per the new productivity level that a particular scope of work can be delivered with using different AI technologies so the reference point is a new reference point.”
  — [LTIMindtree Q1FY27 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/07/earnings-call-transcript-q1fy27.pdf), p. 47 · `LTIMindtree-48`
  _Context:_ Asked whether further productivity-led discounts are being asked on deals already through a cycle.
- **Infosys Q1FY27** (2026-07-23) — Jayesh Sanghrajka, Chief Financial Officer · `deflation`
  > “whenever the deal comes up for renewal, we always used to have the additional productivity ask from the client, which is how traditionally this industry has been. On the back of AI, there is an additional deflation or the AI led deflation as we call it.”
  — [Infosys Q1FY27 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749126000038/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-51`
  _Context:_ Renewal productivity asks plus incremental AI-led deflation.
- **Infosys Q1FY27** (2026-07-23) — Salil Parekh, Chief Executive Officer and Managing Director · `deflation`
  > “On the quantification, we do not quantify that compression part externally, but we acknowledge of course there is a compression and internally, we track it to see how that works. ... So it is not easy to simply say like-for-like in many cases, but they are definitely we see a compression.”
  — [Infosys Q1FY27 transcript](https://www.sec.gov/Archives/edgar/data/1067491/000106749126000038/exv99w05.htm), n/a (HTML exhibit, no pagination) · `Infosys-52`
  _Context:_ Answer to Abhishek Pathak asking to quantify deflation.
- **Cognizant Q2CY2026** (2026-07-29) — Ravi Kumar Singisetti, Chief Executive Officer & Director, Cognizant Technology Solutions Corp. · `productivity_passthrough` · **Q:** >50% productivity improvement over five years committed
  > “We signed a major engagement with a leading insurance brokerage, committing to more than 50% productivity improvement over five years through AI and operating model redesign.”
  — [Cognizant Q2CY2026 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q2/transcript/Transcript_CTSHQ2-2026-Earnings-Call.pdf), p. 6 · `Cognizant-50`
  _Context:_ Prepared remarks.
- **Cognizant Q2CY2026** (2026-07-29) — Jatin Pravinchandra Dalal, Chief Financial Officer, Cognizant Technology Solutions Corp. · `renewal_terms` · **Q:** T&M ~50% of revenue; renewal cycles 6-9 to 12-15 months, max 2-2.5 years; fixed-price contracts 24-36 months
  > “So, our view is that time and material is continually every time we renew it and that short-cycle business, typically six to nine months, sometimes 12 to 15 months, but never more than 2 years or 2.5 years. So that's a short-cycle business. So that's continually embedding in itself, even on managed services basis, the benefit of AI into itself.”
  — [Cognizant Q2CY2026 transcript](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q2/transcript/Transcript_CTSHQ2-2026-Earnings-Call.pdf), p. 17 · `Cognizant-53`
  _Context:_ Bryan Bergin asked about the multiyear book still to be renewed and "existing base compression" from AI.
- **Accenture Q4FY26** (2026-10-01) — Angie Park, Chief Financial Officer · `other` · **Q:** fixed-price (incl. outcome-based) >65% of bookings · **measured:** Firm-reported share of bookings, not a price change.
  > “Fixed price work, which includes outcome based, is now over 65% of bookings and continues to grow.”
  — [Accenture Q4FY26 transcript](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/fourth-quarter-fiscal-2026-conference-call-transcript.pdf), p. 9 · `Accenture-33`
  _Context:_ Prepared remarks.
- **Accenture Q4FY26** (2026-10-01) — Julie Sweet, Chair and Chief Executive Officer · `productivity_passthrough`
  > “So we are definitely giving more productivity due to AI. And like overall though, the impact has been steady. So -- and we're offsetting as we have in the past with new kinds of work, more scope, et cetera. So absolutely giving more AI efficiencies and more than offsetting that as a whole.”
  — [Accenture Q4FY26 transcript](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/earnings-reports/2026/fourth-quarter-fiscal-2026-conference-call-transcript.pdf), p. 19 · `Accenture-36`
  _Context:_ Same renewals/deflation question from Keith Bachman; explicit statement that AI productivity is being given to clients.

## Synthesis

Bracketed IDs are row IDs in `audit/price_calls_quotes.csv`. All of this is commentary, not measured prices.

- **When the language shifted:**
  - **2021H1:** pricing "stable" after COVID discounts [TCS-01, LTIMindtree-02].
  - **2021H2–2022:** rate cards, COLA and price-list increases. HCLTech realization +1% then +30 bps [HCLTech-19]; TechM ≈50 bps margin per quarter, ≈1% over FY23 [TechM-04, -11].
  - **Apr–Jun 2023, the turn:** no "price expansion" [HCLTech-21]; the pricing lever is "limited" [TechM-12]; Accenture pricing lower in some areas [Accenture-13].
  - **2023H2–2024:** "stable" or under consolidation pressure. AI deflation described as "at least two to three years away" [HCLTech-26].
  - **Pass-through made explicit:** LTIMindtree from Jan 2025 [LTIMindtree-19]; TCS's "$100 … $95 or $90" in Apr 2025 [TCS-23]; Wipro and Infosys from Oct 2025 [Wipro-26, Infosys-33].
  - **2026:** quantified deflation [HCLTech-52, -55; LTIMindtree-46; TCS-40]. Accenture says AI is not deflationary [Accenture-22], then that it is giving more productivity but "more than offsetting" it [Accenture-36].
- **Who gives numbers:**
  - **HCLTech** gives the most: 2–3% a year portfolio deflation; a "$100 million deal … maybe 80 million"; SDLC 25–30% and BPO 40–50%.
  - **TCS:** 10–15% productivity passed on, the same as is baked into renewals "even without AI" [TCS-31].
  - **LTIMindtree:** ≈15% less for the same scope.
  - **Accenture:** "at least 10%" a year in managed services [Accenture-14].
  - **Infosys:** realization +3.5–3.6% in FY25.
  - **Cognizant:** revenue per person +5%.
  - **Wipro:** essentially none.
- **Rough g_p:**
  - **Baseline, before AI:** managed-services give-backs of about 10–15% per contract term, roughly −2% to −5% a year on that work.
  - **Extra from AI:** about −2% to −3% a year on the portfolio (HCLTech's forecast, from FY27). About −10% to −20% like-for-like on exposed services.
  - **Little shows up in reported numbers yet** ("very little", HCLTech-58).
  - **Per-FTE realization rose in FY24–26** at Infosys, TCS and Cognizant. That fits S3 only if price per unit of work fell by less than labor per unit of work.
- **S1 vs S3:**
  - **2023–24**, when headcount stalled, pricing was called stable and pass-through prospective. That favours S1.
  - **S3-type pass-through** becomes explicit in 2025 and material in 2026.
- **Caveats:**
  - **Cheap talk:** firms have an incentive to say losses are offset by added scope.
  - **Selection:** pricing talk follows analyst questions, and keyword search misses implicit statements.
  - **Definitions differ:**
    - Accenture's "pricing" means contract margin;
    - "realization" means revenue per billed FTE or hour;
    - "deflation" means deal value for the same scope.
  - **Weak numbers:** many figures are illustrative ("let us say", "rough ballpark"), forward-looking, or apply to one segment.


## Coverage: transcripts screened (by call date)

| Firm | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Total | Calls covered | Rows in CSV |
|---|---|---|---|---|---|---|---|---|---|
| TCS | 4 | 4 | 3 | 4 | 4 | 3 | 22 | Q3FY21–Q1FY27 | 45 |
| Infosys | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q3FY21–Q1FY27 | 54 |
| HCLTech | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q3FY21–Q1FY27 | 63 |
| Wipro | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q3FY21–Q1FY27 | 38 |
| TechM | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q3FY21–Q1FY27 | 47 |
| LTIMindtree | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q3FY21–Q1FY27 | 50 |
| Cognizant | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q4CY2020–Q2CY2026 | 55 |
| Accenture | 4 | 4 | 4 | 4 | 4 | 3 | 23 | Q2FY21–Q4FY26 | 37 |
| **All** | 32 | 32 | 31 | 32 | 32 | 24 | **183** | | **389** |

**Sources.** All transcripts come from the companies' own IR sites, or from SEC EDGAR for Infosys (6-K Ex. 99.5). No aggregator or paywalled site was used.
- **Already local:** TCS, Infosys, Wipro, and some Accenture calls.
- **Downloaded for this task:** stored under `data/sources/<firm>/transcripts_task3/`, each folder with a `urls.tsv` listing source URLs:
  - LTIMindtree, all calls (ltimindtree.com);
  - HCLTech, all calls (hcltech.com);
  - Tech Mahindra, all calls (insights.techmahindra.com);
  - Cognizant, all calls (cognizant.q4cdn.com, FactSet CallStreet transcripts posted by Cognizant);
  - Accenture Q1–Q3 of FY21–FY23 and Q4FY26 (investor.accenture.com);
  - Wipro Q3FY21 (wipro.com).

**Missing calls, and why.**
- **TCS Q4FY23 (12 Apr 2023):** tcs.com returns HTTP 403 (Akamai "Access Denied") to scripted downloads, the file is not archived in the Wayback Machine, and there is no local copy. It is therefore absent: TCS has 3 calls in 2023 instead of 4. I did not use an aggregator copy.
- **Not yet held as of 2026-10-05:** Oct-2026 results calls for TCS, Infosys, HCLTech, Wipro, TechM, LTIMindtree (Q2FY27) and Cognizant (Q3 2026). 2026 therefore has 3 calls per firm; for Accenture these are Q2FY26, Q3FY26 and Q4FY26 (1 Oct 2026).
- **Outside the window:** calls dated 2020, including Accenture Q1FY21 on 17 Dec 2020, are in the corpus but excluded.

**Calls screened with no relevant management pricing statement found** (according to the per-firm readers):
| Firm | Calls |
|---|---|
| TCS | Q3FY23, Q2FY24, Q2FY25 |
| Infosys | Q3FY21 |
| HCLTech | Q2FY24, Q3FY24 (software pricing only), Q3FY26 |
| Wipro | Q3FY21 (passing mention only), Q3FY22, Q4FY22, Q4FY23, Q4FY24, Q3FY25 |
| TechM | Q4FY21, Q1FY22, Q2FY22, Q1FY24, Q2FY24 (Q1FY25 generic only) |
| LTIMindtree | Q3FY24, Q1FY25, Q2FY25 |
| Cognizant | Q1 2021 |
| Accenture | Q4FY21, Q4FY23, Q1FY24, Q2FY24 |

**Notes on the documents.**
- LTIMindtree calls up to Q2FY23 (Oct 2022) are those of LTI, before the merger with Mindtree.
- The Tech Mahindra "Q4FY26" document is the April 2026 Analyst Day transcript, which served as the Q4 results event. Its date, 22 Apr 2026, is taken from IR.
- The Infosys Q1FY23 exhibit's header says "Q1 FY22" but is dated July 24, 2022. I label it Q1FY23.
- **Labels:** "measured" is used only when the quote states a firm-reported figure. Most of these are margin-walk components, realization changes, reported segment revenue changes, or fixed-price mix. In almost all cases the pricing component is bundled with other effects or attributed by management; the CSV's `label_note` explains each one. No firm reports a like-for-like price index.


## Appendix: quantified client case-study / productivity claims (not statements about the firm's own pricing)

- **Accenture Q2FY22** (2022-03-17) — Julie Sweet, Chair & Chief Executive Officer · `productivity_passthrough` · **Q:** up to 30% cost reduction for client (BBVA) via managed services
  > “we will create an “intelligent” data-driven banking operation with greater agility and productivity—lowering costs by up to 30% by leveraging our strategic managed services”
  — [Accenture Q2FY22 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2022/q2fy22/q2fy22-conference-call-transcript.pdf), p. 7 · `Accenture-06`
  _Context:_ Prepared remarks, BBVA managed-services example.
- **Wipro Q1FY24** (2023-07-13) — Thierry Delaporte, Chief Executive Officer & Managing Director · `productivity_passthrough` · **Q:** 40% automation (client deal)
  > “We will help this client achieve 40% automation, cost optimization and while simplifying their global operations.”
  — [Wipro Q1FY24 transcript](https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2023-2024/q1fy24/q1fy24-earnings-transcript.pdf), p. 5 · `Wipro-13`
  _Context:_ Deal example (global medical device/healthcare company, cloud-first operations infrastructure). Automation target is a client outcome commitment; no explicit price figure.
- **LTIMindtree Q1FY24** (2023-07-17) — Debashis Chatterjee, Chief Executive Officer & Managing Director · `other` · **Q:** 40%-60% productivity improvement (GenAI, legacy code conversion)
  > “Application modernization use cases have shown 40% to 60% productivity improvement in large legacy code conversions for cloud.”
  — [LTIMindtree Q1FY24 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2023/07/Earnings-call-transcript-FY2024.pdf), p. 5 · `LTIMindtree-13`
  _Context:_ Prepared remarks on Canvas.ai GenAI platform; relevant to labor per unit of work, no pass-through stated.
- **Accenture Q4FY24** (2024-09-26) — Julie Sweet, Chair and Chief Executive Officer · `productivity_passthrough` · **Q:** ~60% productivity increase; costs reduced by half (client deal)
  > “Through a Managed Services program we are consolidating IT vendors, increasing productivity by an estimated 60% and reducing costs by half.”
  — [Accenture Q4FY24 transcript](https://investor.accenture.com/~/media/Files/A/Accenture-IR-V3/quarterly-earnings/2024/q4fy24/accenture-fourth-quarter-fiscal-2024-conference-call-transcript.pdf), p. 7 · `Accenture-17`
  _Context:_ Prepared remarks; vendor consolidation plus productivity/cost cut in a managed-services deal.
- **TechM Q3FY25** (2025-01-17) — Mohit Joshi, Managing Director & Chief Executive Officer · `other` · **Q:** up to 70% productivity improvement (TechM agentX GenAI suite)
  > “Through these solutions, enterprises can automate complex business, IT and data tasks, improving productivity by up to 70%.”
  — [TechM Q3FY25 transcript](https://insights.techmahindra.com/investors/tml-q3-fy-25-earnings-transcript.pdf), p. 5 · `TechM-21`
  _Context:_ Product marketing claim for client-side productivity from GenAI automation, not a contracted pass-through.
- **HCLTech Q1FY26** (2025-07-14) — C. Vijayakumar, Chief Executive Officer & Managing Director · `deflation` · **Q:** contact center headcount reduced 75%
  > “we are seeing contact centers where a very large number of people get reduced by 75% even by implementing Agentic, Conversational AI and things like that.”
  — [HCLTech Q1FY26 transcript](https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1FY26-Transcript-18.pdf), p. 23 · `HCLTech-46`
- **LTIMindtree Q2FY26** (2025-10-23) — Venu Lambu, Chief Executive Officer & Managing Director · `other` · **Q:** 60% productivity improvement (client case)
  > “We developed an AI-powered quality engineering framework for a global real estate major, streamlining story refinement and automating test case generation. This resulted in a 60% productivity improvement.”
  — [LTIMindtree Q2FY26 transcript](https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2025/10/earnings-call-transcript-q2fy26.pdf), p. 6 · `LTIMindtree-33`
  _Context:_ Prepared remarks.
- **TechM Q1FY27** (2026-07-16) — Atul Soneja, Chief Operating Officer · `other` · **Q:** 40% fewer tickets; 20% lower MTTR; 30-35% less technical debt
  > “The commercial model is tied to measurable outcomes, roughly 40% fewer tickets, 20% lower mean time to resolution, 30% to 35% reduction in technical debt, and significant productivity improvement over the deal duration.”
  — [TechM Q1FY27 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-transcript.pdf), p. 7 · `TechM-40`
  _Context:_ Healthcare deal win with outcome-linked commercial model.
- **TechM Q1FY27** (2026-07-16) — Atul Soneja, Chief Operating Officer · `productivity_passthrough` · **Q:** ~40% reduction in incident handling effort; 2x release velocity
  > “The program targets doubling the release velocity and about 40% reduction in incident handling effort, leading to significant cost reduction.”
  — [TechM Q1FY27 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-transcript.pdf), p. 7 · `TechM-41`
  _Context:_ Telecom managed-operations deal win where AI is central.
- **TechM Q1FY27** (2026-07-16) — Mohit Joshi, Managing Director & Chief Executive Officer · `other` · **Q:** 20% YoY memory/chip price inflation; 3-5 year price holds
  > “If you're seeing a pricing inflation of 20% year-on-year, to tell clients that you will hold the price for a 3 or 5-year deal, we think is a forward call which doesn't really make sense.”
  — [TechM Q1FY27 transcript](https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-transcript.pdf), p. 16 · `TechM-44`
  _Context:_ Hardware/memory price inflation in infrastructure deals (TechM declines multi-year price holds); not services pricing.
