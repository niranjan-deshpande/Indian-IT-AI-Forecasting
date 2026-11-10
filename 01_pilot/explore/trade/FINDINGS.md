# FINDINGS — official trade data as a test of S4 (work moving to GCCs)

*Saved by the orchestrator from the probe's report; the probe could not write files. The orchestrator added the acceleration test in §7.*

**Headline.** Official trade data give an annual S4 cross-check, not a quarterly test. BEA does not publish an India × affiliation split for computer services, so the affiliated side has to come from proxies.

## 1. Access

All sources below are free and need no login.

| source | series | period | lag |
|--|--|--|--|
| BEA ITA Table 1.3 (quarterly) | US imports from India: telecom, computer & information services (TCI); other business services. No computer-only line. | 2003Q1–2026Q2 | ~3 months |
| BEA Services Table 2.3 (annual) | US imports from India by type, incl. computer services | 1999–2025 | ~6 months |
| BEA multinational-enterprise data (MOFA) | services supplied by US-owned affiliates in India to their US parents; employment | 2009–2023 | ~2 years |
| India balance of payments, via the IMF open API (RBI's reporting to the IMF) | computer-services exports, quarterly | 2004Q1–2026Q2 | — |
| RBI annual software-exports survey | press releases | FY09–FY26, FY18 missing | — |

- The BEA API needs a name and email; the probe didn't register.
- RBI's Handbook spreadsheets sit behind a CAPTCHA; the probe didn't attempt it.

## 2. Level

Country, not firm. Cognizant is a US parent, so its India delivery counts as "affiliated".

## 3. Measurement

- **No country split.** BEA: "affiliation detail is available… for the total of trade with all countries" (Concepts & Methods §31.8).
- **Proxy 1: MOFA affiliate-to-parent services.** Broader than GCCs:
  - covers all US multinationals, all services, captive BPO, and US-headquartered vendors (Cognizant, IBM, Concentrix);
  - valued at transfer prices, mostly cost-plus. BEA "lacks the source data needed to identify transfer prices and adjust them" (§8.22).
- **Proxy 2: RBI split by company type.** Private-limited ≈ GCCs plus multinational vendors; public-limited ≈ the large Indian vendors.
- Both proxies measure the GCC share, not p or Q.
- **Coverage gap.** US computer-services imports from India were $13.6bn in 2023, against RBI's $103bn of software exports to the US in FY24. On-site work and work delivered through US branches count as US domestic output.

**Affiliated / GCC-type shares**

| series | early | middle | recent |
|--|--|--|--|
| MOFA affiliate-to-parent, % of US services imports from India | 24% (2009) | 49% (2015) | 72% (2023) |
| RBI private-limited share of software exports | 35% (FY13) | 52% (FY20) | 61% (FY26) |

Context only (consultancy estimate, not data): NASSCOM-Zinnov put GCC headcount at 2.36m in FY26. MOFA shows 1.79m employees at US-owned affiliates in India in 2023, across all industries.

## 4. Noise

YoY log ×100, 2015–22 excluding 2020Q2–2021Q2; annual series drop 2020–21.

| series | mean | s.d. | AR(1) | n | 2023+ mean |
|--|--|--|--|--|--|
| BEA TCI imports from India, quarterly | 1.6 | 6.3 | 0.21 | 27 | 10.5 |
| India computer-services exports, quarterly | 8.1 | 7.3 | 0.96 | 27 | 11.1 |
| BEA computer services from India, annual | 3.1 | 4.4 | — | 6 | 11.6 (2023–25) |
| MOFA affiliate-to-parent, annual | 11.0 | 5.6 | — | 6 | 9.6 (2023) |

## 5. Comparison with the pilot's Indian firms

Annual USD revenue growth, 2015–22, n=8.

- **Pre-2023 correlations** with the firms' growth: 0.41 with BEA computer imports, 0.70 with total services imports, 0.77 with India's computer-services exports.
- **Divergence since 2023.** BEA computer imports grew +7, +15 and +13 (2023–25); the firms grew about +3, +2 and +2.
- **Same split in the RBI survey:**
  - public-limited exports: −1% (FY24), +1% (FY25), +6% (FY26)
  - private-limited exports: +6%, +12%, +9%

## 6. Predicted signs and confounds

- **S1:** affiliated and unaffiliated both fall.
- **S2:** vendor value holds; cost-plus affiliated value falls.
- **S3:** unaffiliated value falls, and affiliated falls too at cost-plus, so it looks like S1.
- **S4:** affiliated and private-limited shares rise; the total is roughly flat.

**Confounds:**
- US-headquartered vendors and Indian vendors' own US affiliates sit inside "affiliated".
- Work invoiced via Singapore or Ireland is attributed to those countries.
- Exchange rates and wages move cost-plus values.

## 7. Orchestrator addition: did the GCC-type share accelerate after 2023?

| period | RBI private-limited share | change per year |
|--|--|--|
| FY14 → FY22 | 36.0 → 59.9 | **+3.0 pp/yr** |
| FY23 → FY26 | 56.1 → 60.8 | **+1.6 pp/yr** |

- There is a probable method break at FY22 → FY23 (59.9 → 56.1).
- **The shift toward GCC/MNC-type exporters continued but did not accelerate.** S4 therefore looks like an ongoing drag on the large vendors, not a new shock in FY25–27.
- **The sharper descriptive fact is the level gap.** India's total software exports grew 2.8%, 7.3% and 8.2% in FY24–26, while public-limited exporters grew −1%, +1% and +6%.
  - That gap is inconsistent with a pure fall in client demand for India-delivered work (S1).
  - It is consistent with S4, with share moving to other vendors, or with S3 hitting the large vendors' service mix harder.

## 8. Verdict

**Conditional (~2 RA-days).** Include as an annual S4 cross-check: the MOFA affiliate share plus the RBI split. It is not a quarterly test and cannot separate S1 from S3. A clean test needs BEA restricted microdata (BE-125, BE-10/11) via special-sworn-employee access, which takes months.

## Files

- `noise_stats.csv`
- `affiliated_share_annual.csv`
- `compare_firm_vs_trade_annual.csv`
- `rbi_survey_orgtype.csv`
- `bea_ita13_india_quarterly.csv`
- `bea_is23_annual.csv`
- `bea_mne_mofa_services_by_destination.csv`
- `bea_mne_mofa_employment_india.csv`
- `imf_bop_india_services_quarterly.csv`
- scripts: `bea_itable.py`, `fetch_bea.py`, `fetch_bea_mne.py`, `fetch_imf_india.py`, `analyze.py`
