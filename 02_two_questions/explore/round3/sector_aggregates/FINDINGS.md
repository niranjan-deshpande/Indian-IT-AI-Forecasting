# FINDINGS — is the Indian IT/ITeS sector as a whole shrinking?

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14. CSVs and scripts in this folder were written by the subagent.*

## 1. Headline
- **No sector-wide series shows the sector shrinking.** FY23→FY26:
  - RBI survey exports +19.4%
  - balance-of-payments (BoP) computer-services exports +38.8%
  - Nasscom revenue +16.6% (chained within each edition)
  - Nasscom employment +6.1%
  - Nasscom minus the top six: about +10.6% (rough: top-six headcount is global, Nasscom's is India only)
  - top six: revenue +7.2%, headcount −3.7%
- **The "7–8%/yr in FY25–26" claim is confirmed.** It comes from RBI's annual software-exports survey.
  - Exports were USD 185.5 → 190.7 → 204.7 → 221.4 bn from FY23 to FY26.
  - Growth: FY24 +2.8%, FY25 +7.3%, FY26 +8.2%; in rupees, +9.7% (FY25) and +13.0% (FY26).
  - It is nominal USD export value, grossed up for non-respondents. It covers exports only and includes ITeS/BPO and GCCs.
- **The growth is in private-limited exporters.**
  - Private-limited exporters (GCCs, multinational vendors and unlisted Indian firms): 104.1 → 134.6 bn (+29%).
  - Public-limited exporters: 77.0 → 81.7 bn (+6%), about the same as the top six.
  - This fits S4a/S4b better than a sector-wide S1, but it cannot separate S4a from S4b.
- **Employment is the weak link.**
  - Nasscom net additions were +60k, +133k and +135k (about 2%/yr), while revenue grew 5–6%/yr.
  - Nasscom–Zinnov put GCC headcount up about 460k from FY24 to FY26, more than Nasscom's total industry net additions over FY25–26 (268k).
  - Either the two definitions don't overlap cleanly, or employment outside GCCs and the top six fell. This must be resolved before claiming that jobs simply moved to GCCs.
- **Pricing caveat.** Under the safe-harbour rules, captive (GCC) exports are invoiced at about 17–18% over operating cost (15.5% from April 2026). Their value therefore tracks the GCC wage bill, not volume or price. This was seen only in advisory-firm summaries, not in the CBDT notification itself.

## 2. Sources

| source | publisher | confirmed? | key detail | URL |
|--|--|--|--|--|
| Software and ITeS exports survey | RBI | yes, fetched | splits by activity, mode, company type and destination; 7,569 firms contacted, 2,363 responded; respondents cover ~89% of value | rbi.org.in press releases prid=63625, 61562 |
| BoP computer-services exports | RBI, via the IMF API | yes (repo CSV) | quarterly; excludes ITeS | api.imf.org (see CSV) |
| Strategic Review | Nasscom (industry body) | secondary, press | FY25 revenue revised from $282.6bn to $297bn; FY26 $315bn; employment 5.815m (FY25), 5.95m (FY26) | etvbharat.com, outlookbusiness.com |
| GCC Landscape | Nasscom–Zinnov (industry / consultancy) | secondary | FY26: 2.36m staff, $98.4bn; FY24's 1.9m and $64.6bn seen only in search snippets | businesstoday.in |
| Exports from software technology park (STP) units | MeitY, via ANI | secondary | ₹6.37 lakh crore (FY24), ₹6.88 (FY25), ₹7.74 (FY26) | tribuneindia.com |
| Listed IT companies' finances | RBI | yes for FY25–26 | sales growth 7.1% (FY25), 7.9% (FY26); staff cost +6.1% (FY26); dominated by the top six | prid=63008 |
| National accounts, new 2022-23 base | MoSPI | yes | IT is bundled with finance, real estate and professional services | static.pib.gov.in (Feb 2026) |
| PLFS unit-level data | MoSPI | catalog confirmed | login required | microdata.gov.in |
| EPFO payroll | EPFO / Ministry of Labour | partial | has a computer-related establishment category; full table returned 403 | |
| ASSSE pilot / full survey | MoSPI | secondary | no IT breakdown; full-survey results not out | |

## 3. How each source bears on the scenarios

**RBI survey**
- If total exports and both company groups fell, that would support S1.
- Total exports up with public-limited exporters flat supports S4a/S4b, and that is what the data show.
- Mode 3 (overseas affiliates of Indian firms) bears on S4d. It rose from $13.9bn to $17.9bn.
- Caveats:
  - exports only;
  - grossed up for non-respondents, and the survey frame grew 12% in one round;
  - method break in FY23;
  - the press release does not break out subsidiaries of foreign companies.

**BoP**
- Useful for timing only. Its level is far above the survey's computer-services figure, and the gap is unexplained.

**Nasscom**
- Use growth rates within one edition only; levels are revised upward every year.
- It is unclear whether GCC staff are counted inside the total.

**PLFS**
- The way to test whether entry-level graduate jobs in IT fell in 2024–25.
- The sample is thin: roughly 900–2,100 NIC-62 records a year.

## 4. Numbers
All numbers, with URLs, are in:
- `exports_recomputed.csv`
- `sector_series_pulled.csv`
- `sector_vs_top6_fy23_fy26.csv`

Not in the tables above:
- ITeS exports were USD 59.7, 66.6 and 68.0 bn (FY24–26), so growth slowed to +2% in FY26.
- BoP other-business-services exports were $124bn in FY26 (+16%).

## 5. Could not check
- PLFS microdata (needs login).
- EPFO's industry table (403).
- RBI Bulletin tables (CAPTCHA).
- MCA aggregates for IT companies, India KLEMS, ASUSE, GST and income-tax data, SEZ exports.
- Nasscom's FY23 headcount level, FY24 GCC figures, and the text of the CBDT safe-harbour notification.
