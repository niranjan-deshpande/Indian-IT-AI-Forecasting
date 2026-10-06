# Quotes for the note: from demand weakness to AI pass-through

Six management statements trace the shift. They are listed in date order, and each is verbatim.

On 2026-10-05 each quote was re-checked against the transcript text with `scripts/final/verify_note_quotes.py`. The check compares whitespace-normalised text on the cited page, in order, with "..." marking an elision. The result is in `output/final/note_quotes_check.csv`: all six pass.

Every quote has the same category from both coders (`calls_codebook.md`).

| # | category | firm, call, date | speaker | quote | source |
|---|---|---|---|---|---|
| 1 | **A** demand weakness | Infosys Q2FY24, 12 Oct 2023 | Salil Parekh, CEO & MD | "We continue to see the overall environment where digital transformation program and discretionary spends are low and decision-making is slow. This is impacting our volumes." | SEC 6-K Ex.99.5, https://www.sec.gov/Archives/edgar/data/1067491/000106749123000057/exv99w05.htm (HTML, no page numbers) |
| 2 | **A** demand weakness | TCS Q2FY24, 11 Oct 2023 | K Krithivasan, CEO & MD | "Our growth was affected by the holding back of discretionary spends by clients." | TCS transcript, PDF p.23: https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q2/Management%20Commentary/Transcript%20of%20the%20Q2%202023-24%20Earnings%20Conference%20Call%20held%20on%20October%2011,%202023.pdf |
| 3 | **B** pricing stable | TCS Q3FY24, 11 Jan 2024 | Samir Seksaria, CFO | "Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is an outcome. You can measure it as revenue per FTE and you will notice that it has been improving" | TCS transcript, PDF p.17: https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202023-24%20Earnings%20Conference%20Call%20held%20on%20January%2011,%202023.pdf (TCS's file name says 2023, but the call was held on 11 Jan 2024) |
| 4 | **D** AI productivity passed to clients | TCS Q4FY25, 10 Apr 2025 | K Krithivasan, CEO & MD | "AI for IT, I won't try to call it deflation. ... And particularly, if there is AI for IT, because of AI if there is a productivity gain, we will try to share those gains with our customers. So, in that sense, that will be what we did with $100 if we are able to do with $95 or $90." | TCS transcript, PDF p.17: https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202024-25%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20Apr%2010,%202025.pdf |
| 5 | **D** AI productivity passed to clients | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar, CEO & MD | "And the 3% to 5% deflation that I mentioned in the AI disrupted services, based on the mix of services that we have, it would translate to 2% to 3% for our portfolio." | HCLTech transcript, PDF p.11: https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf |
| 6 | **D** AI productivity passed to clients | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar, CEO & MD | "$100 million deal would be much lesser today - maybe 80 million, just on a rough ballpark. So, deal TCV is flat. But technically, it does require at least 25%, 30% more effort to convert and get to the same number." | HCLTech transcript, PDF p.21 (same URL) |

## Notes for use

- **Quote 4 is cut.** The ellipsis removes a passage between the two parts. In it, management says it would not call the effect deflation, and then says gains will be shared with customers.
- **Quotes 5 and 6 are rough figures.** Quote 5 is a forward-looking estimate for the firm's portfolio. Quote 6 is explicitly a "rough ballpark", and its context is deal value (TCV), not realized revenue.
- **Treat all six as commentary.** None is a measured price.
- **Demand talk did not stop in 2025–26.** Category A statements fall from 7.5–7.9 per transcript in 2023 to 4.7–5.9 per transcript in 2024H2–2026H2. That is lower, but it does not disappear (`output/final/fig3_data.csv`). Say "added" rather than "replaced" when describing the shift.
