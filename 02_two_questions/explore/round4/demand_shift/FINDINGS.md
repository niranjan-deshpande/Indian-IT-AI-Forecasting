# FINDINGS — M5: outside measures of the demand shift (d)

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14. Scripts run as `python3 -I <script> <folder>`. Downloads are in `raw/` (BEA, BLS OEWS, SEC XBRL). BLS required an identifying user agent; the subagent used a placeholder contact address (example.org), not the user's email.*

## 1. What each proxy measures, and which ones are circular

**Model:**
- g_Q = d − ε·g_p
- g_L = g_Q − s̄ − ρ

Here d is the real shift in vendor volume at a constant vendor price.

**Circularity.** Client spending with vendors equals vendor revenue (p·Q). Its growth is d + (1−ε)g_p, which identifies d only if ε = 1.

**Market vs vendor share.**
- Vendor d = market d + d_share, where d_share = (1−σ) × (relative shift toward in-house work at constant relative prices), and σ is the vendor share of the market.
- d_share falls when clients move work in-house in the US, to GCCs, or to their own AI tools.
- GCCs count against vendor d only at a scope that excludes them.

**Nominal vs real.** The US GDP deflator grew 2.76%/yr over 2016–22 and 2.94%/yr over 2023–25 (+0.2pp). Against a 2016–19 baseline (1.66%/yr) the difference is +1.3pp.

**US vs global clients.** RBI Table 5 (CONFIRMED) gives the USA 54.1%, 52.9% and 54.1% of exports in FY24–26, and Europe 30.8–32.8%. All proxies below are US-only, so about 45% of demand is unmeasured.

| proxy | measures | circular? | role |
|--|--|--|--|
| BEA purchased custom software (NIPA 5.6.5 line 4) | vendor output | **Yes** | vendor share only, net of price |
| BEA own-account software (line 5) | in-house developer labour cost | No | in-house work |
| BEA "real" custom | deflated by the same input-cost index as own-account | Yes | not usable as vendor volume |
| BEA prepackaged/SaaS | substitute | No | context |
| OEWS computer jobs in client industries | in-house tech labour | No | in-house work, net of AI replacement |
| OEWS computer jobs in NAICS 5415 | US vendor labour | Outcome | share denominator |
| Bank 10-K tech expense lines | client tech budget | Partly; bias ≤ w(1−ε)\|g_p\| ≈ 0.75pp, where w ≤ 0.3 is the vendor share of the budget | market d |
| Real GDP, profits | client drivers | No | market d |
| Gartner IT services spend; ISG ACV (consultancy) | vendor revenue or contract value | **Yes** | context only |
| PLFS ICT occupations outside IT (India) | in-housing by Indian domestic clients | No | context; GCCs sit inside NIC 62 |

## 2. Series

### (a) BEA NIPA 5.6.4–5.6.6
CONFIRMED; flat files downloaded 2026-10-14. Files: `bea_software_annual.csv`, `bea_software_quarterly_total.csv`.

Average log growth, %/yr:

| series | 2016–19 | 2016–22 | 2023–25 | 2024 | 2025 |
|--|--|--|--|--|--|
| custom, nominal | 8.0 | 8.6 | 5.3 | 4.3 | 6.9 |
| own-account, nominal | 4.8 | 5.1 | 5.7 | 4.6 | 2.6 |
| own-account, real | 6.5 | 7.2 | 6.9 | 5.3 | 5.6 |
| prepackaged, nominal | 10.9 | 11.2 | 9.7 | 10.5 | 12.6 |
| custom minus own-account | 3.3 | 3.5 | −0.4 | −0.3 | 4.4 |

- **Own-account share of (custom + own-account):** 31.1% (2015), 26.1% (2022), 27.2% (2023–24), 26.4% (2025). Outsourcing gained share until 2022, then stalled; 2025 partly reverses the stall.
- **Total software investment:** +8.6 log points, H1 2026 vs H1 2025.

### (b) Bank tech budgets
Files: `bank_tech_xbrl_long.csv`, `bank_tech_budgets_disclosed.csv`.

**XBRL lines (CONFIRMED).**
- The "CommunicationsAndInformationTechnology" line summed across JPM, BAC and C grew 4.7%/yr over 2016–22 and 4.7%/yr over 2023–25, with 2025 at +6.7%.
- JPM + BAC grew 6.5 log points in H1 2025 and 11.3 in H1 2026.
- The JPM line fell over 2020–23 while JPM's disclosed total rose, so it is partial.
- WFC has no comparable line.

**Disclosed totals (secondary press, not confirmed).**
- JPM: about $12bn (2021), more than $15bn (2023), $17bn (2024), and a $19.8bn budget for 2026. Its definitions widen over time.
- BAC: $13bn (2025).

Client tech budgets show no slowdown and accelerated into 2026, partly because of AI hardware.

### (c) BLS OEWS, May 2015 – May 2025
CONFIRMED. File: `oews_computer_occ_by_bucket.csv`.
- Occupations: SOC 15-1100 through 2018, 15-1200 from 2019.
- Industries: national 4-digit NAICS. "Client industries" excludes 5415, 5416, 5613 and the tech producers.

| bucket | 2015 | 2022 | 2025 | growth 2016–22 (%/yr) | growth 2023–25 (%/yr) |
|--|--|--|--|--|--|
| NAICS 5415 (vendors) | 1.071m | 1.279m | 1.207m | 2.5 | −1.9 |
| Client in-house | 1.910m | 2.275m | 2.505m | 2.5 | 3.2 |
| of which finance & insurance | 0.315m | 0.402m | 0.438m | 3.5 | 2.9 |
| Staffing (5613) | 0.128m | 0.178m | 0.139m | 4.7 | −8.3 |
| All industries | 3.854m | 4.678m | 4.828m | 2.8 | 1.1 |

- **In-house share of (client + 5415) computer jobs:** 64.1–64.9% over 2015–22, then 65.7% (2023), 66.9% (2024), 67.5% (2025).
- **Caveats:** OEWS is not designed as a time series (rolling panel; SOC change in 2019), and the 2022 jump in 5415 may be noise. A 2016–19 baseline gives a similar relative shift (−4.7pp).

### (d) PLFS India
From round 3. The share of ICT-occupation workers outside NIC 62–63 went from 8.2% to 12.5% (2022-23 to CY2025); treating NIC 58 as IT, from 5.6% to 8.8%. This reflects Indian domestic clients, and GCCs cannot be separated out, so it is **not used in the bound**.

### Context (consultancy; circular)
`consultancy_context.csv`:
- Gartner IT services spending: +6.2% (2025); +9.0% forecast for 2026 (April 2026).
- ISG Americas managed-services ACV: −12% y/y in Q2 2026.

## 3. Bounds on Δd, 2023–25 vs 2016–22 (pp/yr)
File: `d_bounds.csv`.

| component | low | central | high | basis |
|--|--|--|--|--|
| Δd, market (US, real) | −1.5 | −0.5 | +0.5 | see note 1 |
| Δd, share (OEWS) | −3.3 | −2.5 | −1.7 | see note 2 |
| Δd, share (BEA) | −1.0 | −0.7 | −0.4 | see note 3 |
| Δd, share (US combined) | −3.3 | −1.6 | −0.4 | envelope of OEWS and BEA |
| Δd, share (GCC; vendor scope only) | −2.5 | −1.0 | 0 | see note 4 |
| **Δd, vendor (excl. GCC)** | **−7.3** | **−3.1** | **+0.1** | ranges added |
| **Δd, sector (incl. GCC)** | **−4.8** | **−2.1** | **+0.1** | ranges added |

Notes:
1. **Market.** Real GDP +0.4; own-account real −0.3; bank tech lines 0.0. Custom + own-account nominal is −2.3 but partly circular; adding back up to 1.8 of AI pass-through and adjusting for inflation gives −2.5 to −0.4.
2. **OEWS share.** 0.64 × relative labour shift (−5.2) + (s_vendor − s_in-house), where the second term is assumed to lie in [0, 2.5].
3. **BEA share.** 0.26 × relative nominal shift (−3.9) + a relative vendor price cut in [0, 2.5].
4. **GCC.** About 260k GCC tech jobs were added over FY23–26 (range 155–430k), against a non-GCC base of about 3.6m, i.e. 2–3%/yr. Pre-2023 GCC growth was not checked.

**Directions of bias:**
- OEWS overstates in-housing if vendors adopted AI faster than in-house teams, or if 5415 jobs moved offshore. Round 3 found India's share of offshore work flat, so the second effect is unlikely to be large.
- The share measures understate the shift at a constant price if vendors cut prices relative to in-house costs.
- The European 45% of demand is unmeasured.

## 4. Implication for the (d, ε) line
File: `d_eps_mapping.csv`.

In change form, with π and ρ unchanged:

  Δd + φs̄ε = s̄ + Δg_L

With s̄ = 2.5, φ = 1 and post-2023 vendor employment growth g_L ≈ 0, this becomes Δd + 2.5ε = 2.5 − g_L,base, where g_L,base is pre-2023 vendor employment growth.

| baseline | result |
|--|--|
| g_L,base = 5 | Vendor central (Δd = −3.1) gives **ε ≈ 0.25**. ε ∈ [0, 1] needs Δd ∈ [−5, −2.5], which is inside the band. |
| g_L,base = 7 (top six, FY16–20) | Central gives ε = −0.56, which is infeasible. Feasibility needs Δd ≤ −4.5 or s̄ > 2.5. |
| Sector scope including GCCs | Use g_L ≈ +2 (Nasscom). The line becomes Δd + 2.5ε = 4.5 − g_L,base. |

**Takeaway.**
- Client-side drivers (GDP, tech budgets, in-house tech work) suggest market-wide demand barely moved: the market term is pinned to within about ±1pp.
- So if ε ≥ 0, almost all of the fall in demand facing vendors must come from vendors losing share, through US in-housing and GCCs. The alternative is that s̄ is above 2.5.
- The share term is the main remaining uncertainty.
- **Next steps:**
  - the pre-2023 GCC growth rate;
  - checking the OEWS 5415 fall against BLS CES;
  - a European proxy.

## 5. Not done or not confirmed
- BEA NIPA Handbook ch. 6 text not opened.
- BAC 2025 annual report not opened.
- JPM 2022 and 2025 tech totals not confirmed.
- Nasscom FY16–23 employment baseline not in the repo.
- No European proxies pulled.
- No 2026 BEA type detail; no 2026 OEWS.

## Files
**Scripts:**
- `bea_software.py`
- `bank_tech_xbrl.py`
- `oews_inhouse.py`
- `d_bounds.py`

**Outputs:**
- `bea_software_annual.csv`
- `bea_software_quarterly_total.csv`
- `bank_tech_xbrl_long.csv`
- `bank_tech_budgets_disclosed.csv`
- `oews_computer_occ_by_bucket.csv`
- `rbi_destination_split.csv`
- `consultancy_context.csv`
- `proxy_series_annual.csv`
- `proxy_prepost_summary.csv`
- `d_bounds.csv`
- `d_eps_mapping.csv`
