# FINDINGS — panel of listed IT firms beyond the top six, FY23–FY26

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14. Rebuild with `python3 -I data/explore/round3/listed_panel/build_panel.py`.*

## Summary
- **Universe:** 21 listed Indian firms with FY25 revenue of at least about ₹1,500 cr.
  - the mid-tier four (Persistent, Coforge, Mphasis, Hexaware);
  - 5 ER&D firms: LTTS, Tata Elxsi, KPIT, Cyient (services segment), Tata Technologies;
  - 7 IT-services firms: Birlasoft, Zensar, Sonata, Mastek, Happiest Minds, Datamatics, R Systems;
  - 5 ITeS/BPM firms: Firstsource, eClerx, HGS, Sagility, Inventurus.
- **Taken literally, the 21 firms' gain offsets the top six's loss.** FY23→FY26, all 21 firms added +62.7k staff (+18.6%) while the top six lost 61.5k, so combined headcount is flat at about 2.02m.
- **But the broad IT-services and ER&D mid-tier did not absorb the slack.** The gain went to BPM firms and acquisitions:
  - At least 15.7k of the gain is acquired staff (a lower bound).
  - 36k of the 43k added outside the four was at the 5 BPM firms, much of it outside India. All headcounts are global, not India-only.
  - IT-services and ER&D firms outside the four grew only about 2.3% organically over three years. 5 of these 12 shrank, and as a group they fell 1.2% in FY26.
- **Against the top six's 384k shortfall from trend, the whole set covers about 16%.**

## Method
- **Sources.** Primary documents only: Q4 fact sheets, investor decks, press releases, annual reports, IPO prospectuses and exchange filings. Every value carries a URL and page.
- **Mid-tier four.** Headcount and USD revenue come from `../../midtier/midtier_raw.csv`; INR revenue was added from fact sheets.
- **Calendar years.** Hexaware and R Systems report by calendar year; CY(t) is aligned to FY(t+1).
- **Aggregates.**
  - Endpoints are balanced at FY23 and FY26.
  - The revenue-weighted mean uses FY23 INR revenue as weights.
  - Acquired headcount is subtracted only where a document states it, so the adjustment is a lower bound.
- **Cyient.** The services segment (DET) is used for both revenue and headcount, because headcount is disclosed only excluding the electronics-manufacturing business.
- **LTTS.** Endpoints exclude SWC:
  - FY23 as reported;
  - FY25–26 continuing operations;
  - FY24 includes SWC, since no figure excluding it was published.

## Inclusion rules
- **Included:** listed (NSE/BSE) IT services, ER&D and ITeS/BPM firms with FY25 revenue of at least about ₹1,500 cr.
- **Excluded:**
  - Software-product firms: Intellect, OFSS, Newgen, Nucleus.
  - Below the threshold: Sasken, Latent View, Saksoft.
  - Digitide: pro-forma figures only, no history.
  - Quess: tech segment not separable.
  - Other businesses: Black Box (infrastructure); Tanla and Route Mobile (CPaaS); Zaggle (fintech); Sify (data centres).
  - Startek: not listed in India.
  - Cigniti: inside Coforge.
- **Segment choices:**
  - Sonata: International IT Services revenue.
  - HGS: BPM segment.

## Results, FY23 → FY26 (year-end headcount)

| set | n | headcount FY23→FY26 | % change | % excl. known acquired staff | INR revenue % | USD revenue % (n) | firms shrinking |
|--|--|--|--|--|--|--|--|
| Top six (repo) | 6 | 1,679,489 → 1,618,023 | −3.7 | – | +18.0 | +7.2 | – |
| All 21 | 21 | 337,269 → 399,974 | +18.6 | +13.9 | +44.9 | +32.8 (16) | 7 |
| 17 excl. mid-tier four | 17 | 228,506 → 271,672 | +18.9 (median +8.9; revenue-weighted +13.5) | +13.9 | +39.2 | +27.5 (12) | 6 |
| Mid-tier four | 4 | 108,763 → 128,302 | +18.0 | +14.1 | +53.6 | +39.4 | 1 |
| ER&D | 5 | 71,898 → 74,772 | +4.0 | +0.2 | +35.4 | +25.0 (4) | 2 |
| IT services excl. four | 7 | 56,612 → 60,755 | +7.3 | +4.9 | +29.0 | +13.7 (5) | 3 |
| ITeS/BPM | 5 | 99,996 → 136,145 | +36.2 | +28.7 | +55.1 | +47.7 (3) | 1 |
| IT + ER&D excl. four | 12 | 128,510 → 135,527 | +5.5 | +2.3 | +32.6 | +20.3 (9) | 5 |

- **FY26 alone:** headcount at the 17 firms rose 3.8%. At the 12 IT and ER&D firms, headcount fell 1.2% while USD revenue rose 2.6%, which is consistent with the red-team result.
- **Firms that shrank, FY23→FY26:**

  | firm | headcount change |
  |--|--|
  | HGS | −17.3% |
  | Mastek | −15.9% |
  | Mphasis | −8.4% |
  | Birlasoft | −6.8% |
  | Cyient (DET) | −6.2% |
  | Tata Elxsi | −2.7% |
  | Sonata | −2.4% |

- **16 of the 21 firms** had at least one year of falling headcount.
- **Top six plus the 21:** 2,016,758 → 2,017,997, essentially flat.

## Acquisitions that explain most of a firm's growth
- **Inventurus:** AQuity (Oct 2023, ₹1,674 cr) brought 6,349 of the 6,529 added staff. Pro-forma growth FY24→FY26 is about 22%.
- **Happiest Minds:** PureSoftware (~1,200 staff) and Aureus (~150) account for about 85% of the 1,580 added.
- **KPIT:** Caresoft (Aug 2025, 900+ staff) accounts for about 60% of the 1,507 added. Technica (Q3FY23) is only partly in the FY23 base, which inflates revenue growth.
- **LTTS, excluding SWC:** Intelliswift (Jan 2025, ~1,500 staff according to secondary sources) accounts for most of the 1,597 added and about 40% of USD revenue growth.
- **Datamatics:** TNQ (Dec 2024) accounts for about half of revenue growth.
- **R Systems:** Novigo (Nov 2025, ₹400 cr) probably drives the CY25 jump of 1,043 staff. Velotio was bought in CY23.

**Partly acquired:**
- Coforge: Cigniti accounts for about 4,200 of the 12,600 added.
- Firstsource: four deals account for about a third of revenue growth.
- Sagility: BroadPath, 1,083 staff and about 9 points of FY26 growth.
- Sonata: Quant, about 30% of international revenue growth.
- Mastek: MST.
- Tata Technologies: ES-Tec, about 300 staff.

**Organic:** Birlasoft, eClerx and Tata Elxsi. Zensar's acquisition is small.

## Caveats and gaps
- **Headcount is global, not India-only.** This matters most for the BPM firms, which have large operations in the Philippines, the UK and South Africa.
- **Contractors:**
  - included at Mphasis, Hexaware and Tata Technologies;
  - Sonata FY23–24 come from BRSR and include temporary staff;
  - not stated elsewhere.
- **Tata Elxsi FY23 headcount** is derived as FY24 minus net additions.
- **Mphasis:** INR revenue is net, while USD revenue is gross.
- **Coforge FY26** is continuing operations only.
- **Missing USD revenue:**
  - Tata Elxsi, Datamatics;
  - Inventurus FY23–24, HGS FY23–24;
  - Sonata FY23 level.
- **Acquired headcount not quantified:** TNQ, Novigo, Velotio, Firstsource deals.
- **Not collected:** India-only headcount.
- **`raw/` is 402 MB** (each file is under 50 MB).

## Files
- `build_panel.py`
- `listed_panel_long.csv` (367 rows, with URL and page)
- `listed_panel_firms.csv`
- `listed_panel_summary.csv`
- `universe.csv`
- `parts/*.csv`
- `raw/<firm>/`
