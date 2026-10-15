# Outline: AI and jobs in Indian IT services — two questions

*Draft outline, 2026-10-15. For agreement before any writing or building. Numbers are provisional and come from the FINDINGS.md files cited in brackets. Scope: the six largest firms (TCS, Infosys, HCLTech, Wipro, Tech Mahindra, LTIMindtree), FY24–26 compared with before 2023, unless stated. "pp/yr" means percentage points a year.*

---

## The spine

The whole piece answers two questions, in order. Every section, figure and number serves one of them.

1. **The replacement rate.** If a piece of work used to take 100 workers, how many does it take now with AI?
2. **The demand response.** When AI makes the work cheaper, do clients buy more of it?

They link through one chain, which the piece follows from left to right:

> AI saves labour on each piece of work → the firm keeps the saving or passes it on as a lower price → a lower price may lead clients to buy more → more work means more jobs.

Jobs move with two things: the amount of work, and the workers each piece of work needs. Question 1 is about the second. Question 2 is about whether the first rises in response. Anything else that moves the amount of work (clients' budgets, clients doing the work themselves) is a *demand shift*. We have to measure it and set it aside to see Question 2 clearly.

**Provisional answers, for the top of the page:**
1. About **93 workers instead of 100** after three years (FY24–26): a saving of roughly 2 pp a year. Plausibly 90–96. The data can't rule out no saving at all. Juniors were probably replaced faster than experienced staff.
2. **Not yet tested.** Firms kept about nine-tenths of the saving instead of cutting prices, so clients had little reason to buy more. Meanwhile the amount of work fell sharply for reasons unrelated to price. Price cuts begin in FY27, so the real test starts now.

---

## 1. The question and the accounting (short)

**Purpose:** set up the chain and the one equation, then get out of the way.

- **The fact, in two sentences.** Headcount at the top six grew about 7% a year before COVID, jumped during the FY22–23 boom, fell 4% in FY24 and has been flat since. Revenue in constant currency slowed from about 9% a year to 1–3%. [`output/final/note_numbers.csv`]
- **The accounting.** Jobs = amount of work × workers per piece of work. In growth rates:

  employment growth = demand shift − (price elasticity × price change) − replacement rate

  with price change = −(share of the saving passed on) × replacement rate. One box gives the symbols (s̄, φ, ε, d) for readers who want them. The text uses words.
- **The key consequence.** AI adds jobs only if clients' extra purchases outweigh the labour saved, i.e. only if (share passed on) × (elasticity) > 1. That needs firms to pass on almost all the saving *and* clients to be very responsive to price. Section 3 returns to this.
- **A third, temporary term: slack.** Firms over-hired in FY22–23 (headcount ended 14 log points above trend, revenue only 3.5) and then worked off their bench. Using up slack lowers hiring without any change in demand or AI. All our measures of the replacement rate are net of utilisation for this reason. [`round4/robustness/baseline`]
- **Scope, in one paragraph.** Why the top six: they are the only firms with long, consistent firm data. The sector as a whole looks similar: employment flat at about 5.7m since 2022-23 (PLFS), and young graduates in IT flat at about 2.6–2.8m. The work did not leave India: India's share of world computer-services exports was flat. [`round3/plfs`, `round3/offshore_competitors`]

**Figure 1.** The chain, as a simple diagram, with the three things we measure marked on it: the saving kept, the saving passed on, and the demand shift.

---

## 2. Question 1: How many workers does a piece of work need now?

**Provisional answer:** about 2 pp a year fewer in FY24–26, so about 93 per 100 after three years. Plausibly 90–96. Zero can't be ruled out. Juniors were probably replaced faster.

### 2a. Why we can't measure it directly, and what we do instead
- Nobody publishes workers per piece of work. But a labour saving has to go somewhere: either the firm keeps it, so revenue per worker rises, or it passes it on, so prices fall.
- So: **replacement rate = saving kept + saving passed on.** We measure each half separately.

### 2b. The saving kept: revenue per worker
- Measure: growth in revenue per employee, net of changes in utilisation, compared with each firm's own pre-2023 growth. [`round4/residual`]
- Raw result: about +1 pp a year faster after 2023.
- **Correction for subcontracting.** In FY24–25 the firms brought subcontracted work in-house: subcontracting fell by 1.2–3.9 pp of revenue. That adds own staff without adding revenue, so it hides productivity gains. Corrected, the saving kept is about **+2.1 pp a year** (1.5–3.0 within bounds). [`round4/robustness/m1_scope_subcon`]
- TCS and HCLTech don't report utilisation, so they are bounded using the range seen at the other four.
- What would overturn the correction: if more than about 60% of the fall in subcontracting spending was lower contractor rates rather than fewer contractors.

### 2c. The saving passed on: what firms said about prices
- Measure: 108 statements from earnings calls and investor days about price cuts on the same work, net of the routine 1.5% a year productivity give-backs firms offered before AI. [`round4/price_statements`]
- Result: almost nothing before FY26: 0 in FY24, 0.1 in FY25, 0.4 in FY26. It rises to about 1.5 in FY27 (0.4–2.7), mostly as expectation.
- Key quotes (two or three): HCLTech, April 2026, "very little has really played out in already reported numbers"; TCS, October 2026, pricing "broadly stable" at portfolio level.
- What would overturn it: firms understating cuts by a factor of more than five. Time-and-materials billing hides some pass-through as fewer billed hours, so this is probably a slight underestimate.

### 2d. Putting the halves together
- **About 2.3 pp a year** (2.0–2.6 across the subcontracting assumption; 1.5–3.6 within all bounds; −0.8 to 7.1 once sampling noise is included).
- In the reader's terms: 100 workers became about 93 over FY24–26 (90–96).
- About nine-tenths of the saving was kept and about one-tenth passed on. **This reverses the existing note's claim that there was "no sign firms kept AI savings."** That claim rested on four firms and no subcontracting correction.
- This is an average over the firms' whole mix of work. Exposed tasks such as testing and maintenance must have seen bigger savings, and less exposed ones smaller.

### 2e. The strongest objection, stated openly
- On *growth rates* the saving is about 2 pp a year. On *levels* it vanishes: revenue per employee is still about 11 log points below its FY16–20 trend, the same gap as in FY23. [`round4/robustness/baseline`]
- What each reading assumes: the growth reading treats the FY21–23 dip as a one-off that won't reverse; the level reading expects firms to catch back up to the old path.
- We can't settle this yet. Say so, and show both.

### 2f. Juniors
**Provisional answer:** juniors were probably replaced faster. The gap is about 0–2 pp a year, so roughly 2–3.5 pp a year for juniors against 1.5–2.3 for experienced staff. The pay evidence is the firmest.

- **Headcount.** Junior employment growth minus experienced, after netting out the boom: about 0 to +1 pp a year at the firms (range −2 to +3); about +2 at sector level in PLFS (the confidence interval includes 0). [`round4/junior_gap`]
- **Pay.** In IT, pay for 21–25-year-olds relative to 31–40-year-olds fell 5.4 log points a year faster than among all graduates (SE 1.85). Junior pay falling while junior numbers stagnate and graduate supply rises points to weaker demand for juniors. [`round4/junior_gap`, `round3/plfs`]
- **How it happened: hiring, not firing.** At Infosys, hiring of over-30s rose 65% while under-30 hiring stayed flat. Fresher hires per $bn of revenue at Infosys and HCLTech are about half their pre-COVID level. [`round4/junior_gap`, `round3/red_team`]
- **Across the sector.** The share of employed young graduates (21–30) who work in IT fell from 12.8% to 9.9%, while their number in IT stayed flat (PLFS, with a design break in 2025). NIRF placements fell for the class of 2023-24, the first fall since 2016-17. GCCs hire few freshers and offset about a fifth of the fall in IT fresher postings. [`round3/plfs`, `round3/seniority_sector`]
- **A warning for the forecast.** The boom-era freshers turn 30 around FY30–31. That will lower under-30 shares mechanically, and it is not AI.

### 2g. Vintage
All of this predates the step change in coding agents around summer 2026. It describes the tools of 2023–early 2026, so it is a floor for the future, not a forecast.

**Figures for Question 1:**
- **Figure 2:** the saving split in two, by year FY24–FY27: a bar for the saving kept and a bar for the saving passed on, with ranges. FY27 is drawn lighter because it is expectation.
- **Figure 3:** juniors. PLFS relative junior pay, IT vs all graduates, 2017-18 to CY2025, beside Infosys hires by age.

---

## 3. Question 2: When AI makes the work cheaper, do clients buy more?

**Provisional answer:** we can't tell yet, because the work hasn't got cheaper. What we can say is that the amount of work fell for other reasons, and by more than AI's direct effect.

### 3a. The test hasn't happened
- Prices fell by about 0.2 pp a year in FY24–26 (Section 2c). Even if clients were very responsive, a cut that small could not raise purchases noticeably.
- So the past four years tell us almost nothing about clients' responsiveness to price. This is a finding, not a gap: through FY26 the cheaper-work route to more jobs was switched off, because firms kept the saving.
- It switches on in FY27, as renewals start carrying AI price cuts (about 1.5 pp a year expected).

### 3b. But the amount of work did fall, for reasons other than price
- Since prices barely moved, the fall in volume is almost all a demand shift.
- How big depends on what you think "normal" growth would have been. Show three yardsticks side by side: [`round4/robustness/baseline`]

  | yardstick | fall in revenue growth (pp/yr) |
  |--|--|
  | pre-COVID growth rate (FY16–20) | about 7 |
  | return to the pre-COVID level path | about 6 |
  | compared with Accenture and Cognizant | about 3 |

- The revenue shortfall is real: top-six revenue is about 18 log points below its pre-COVID path, while Accenture's is back on trend.
- About 57% of the revenue slowdown is shared with Accenture and Cognizant, so much of it is global. About 3 pp a year is specific to the Indian firms.

### 3c. What moved demand
Take each candidate and say what the data show: [`round4/robustness/demand`, `round3/*`]
- **Clients' overall spending: little change.** GDP, bank technology budgets and US in-house software investment were all roughly flat or growing. About −0.5 pp a year.
- **Clients doing the work themselves: some.** The in-house share of US computer jobs rose from 64–65% to 67.5%, and US vendor employment (BLS CES) confirms the fall. Continental Europe shows no change; the UK may be large but is unverified. About −1.6 pp a year.
- **Clients' own Indian centres (GCCs): no extra effect.** GCCs kept growing, but no faster after 2023 than before. About +0.5 (range −2.2 to +1.6).
- **Smaller Indian firms: little.** Twenty-one other listed firms absorbed little organically. Four fast-growing mid-tier firms are a selected sample. (The share they took has not yet been sized in pp; it looks small.)
- **Work leaving India: no.** India's export share is flat; no onshoring.
- **Left unexplained:** about 5 pp a year against pre-COVID growth rates; about 3 pp against Accenture and Cognizant. Candidates: a work mix heavy in routine maintenance, clients using AI tools themselves, the post-boom hangover.

**A point for Andrei:** some of this "demand shift" may itself be AI, arriving by another route: clients doing more in-house with their own AI tools. We can't separate that from ordinary in-housing. It matters for the forecast: if so, demand keeps shifting as the tools improve.

### 3d. What we can say about responsiveness
- Our attempt to measure it from differences between service lines failed: the price differences between lines are tiny, and line-specific demand shocks swamp them. [`round4/elasticity_xsec`]
- So we borrow a range from history (Bessen on textiles, steel and cars; Tevlin and Whelan on computers): about 0.5–1.5 for IT services, centre 0.9; about 0.2–0.9 for BPO.
- **What that implies.** For AI to add jobs, (share passed on) × (elasticity) must exceed 1. Even with full pass-through, that needs an elasticity above 1, which is only the top of the plausible range for IT and outside it for BPO. With today's pass-through of about one-tenth, AI cuts jobs almost one-for-one with the saving.

**Figures for Question 2:**
- **Figure 4:** the demand shift as a waterfall: total implied shift (one bar per yardstick) → client markets → in-housing → GCCs → unexplained.
- **Figure 5:** the jobs effect of AI as a function of the share passed on, for elasticities of 0.5, 0.9 and 1.5. Mark today (about 0.1) and FY27's implied share. It shows at a glance how far we are from the zone where AI adds jobs.

---

## 4. What the two answers say about FY24–26

**Provisional answer:** AI took roughly 2 pp a year off employment growth directly. The cheaper-work offset was near zero. Demand shifting away from these firms did the rest, and it was the larger part on most yardsticks.

- One table: the slowdown in headcount growth split into (i) replacement, (ii) the price response, (iii) the demand shift, (iv) slack, under each of the three yardsticks.

  | yardstick | headcount slowdown | replacement | price response | demand shift and slack |
  |--|--|--|--|--|
  | pre-COVID growth rates | 8.3 | ~2.3 | ~0 | ~6 |
  | pre-COVID level path | 3.0 | ~2.3* | ~0 | ~1 |
  | vs Accenture / Cognizant | 1.5 | ≤2.3† | ~0 | — |

  \* The level yardstick also undercuts the replacement rate itself (Section 2e).
  † Only if AI affected the Indian firms more than their peers. If all vendors were hit equally, it cancels out in this comparison.
- Cross-check: two routes to the volume change (from headcount plus replacement, and from revenue minus price) agree under the growth yardstick (about −7) once the in-sourcing of subcontracted work is counted. [`round4/robustness/m1_scope_subcon`]
- What survives every yardstick: the replacement rate is smaller than the demand shortfall; and the price response was negligible.
- Report the replacement rate in pp a year, not as a share of the slowdown. The share swings from about 28% to over 100% depending on the yardstick.

---

## 5. Looking ahead to 2030 (placeholder)

*To be written later.* This section will turn the two answers into conditional scenarios, not forecasts. It will draw on:
- **Replacement rate paths** starting from about 2 pp a year and rising after the summer-2026 step change. Capability evidence (METR time horizons, the updated METR developer trial, coding benchmarks, the cost of AI relative to Indian wages) informs how fast it rises, not its starting level.
- **Pass-through rising** from about one-tenth toward the FY27 statements.
- **Elasticity** as a grid over the historical range, since the data can't pin it down.
- **Demand shift paths,** including the possibility that clients' own AI use keeps pulling work in-house.
- **Juniors** handled separately, with the FY30–31 ageing of the boom cohort netted out.
- For each scenario: junior and total employment in 2030, and the early signs that would tell us we are in it.

---

## 6. What would sharpen each answer

Organised by question, not by data source.

**Question 1 (replacement):**
- FY27 results. The first year after the step change, and the first with real price cuts, so both halves of the saving become visible.
- Billed effort (person-months) from the firms. This gives workers per unit of billed work directly; Infosys published it until FY20.
- Utilisation for TCS and HCLTech.
- Settling growth vs level (Section 2e) as more years arrive.

**Question 2 (demand response):**
- A price index for IT services. None exists in India, and BLS does not cover the sector.
- Price cuts on renewals by service line, for example application maintenance vs consulting. Gaps of a few pp would identify responsiveness.
- RBI's census of foreign-owned firms (FY26 round due late October 2026) and its unpublished employee counts, to pin down GCCs.
- A UK in-housing series, to check the one large unverified piece of the demand shift.

---

## Appendix (collapsible)
- **Methods:** the model in full; how each measurement maps to a parameter; the bounds and the points at which each conclusion breaks.
- **Robustness:** baselines, scope, the subcontracting correction, European and GCC checks.
- **How the old four scenarios map onto this:** demand fell = market shift; work moved = share shift; savings kept vs passed on = the split in Question 1.
- **Sources,** and the PLFS (MoSPI) citation.

---

## Notes for writing (not for the page)
- Style: short, plain sentences. Each section opens with its answer. No background section; context goes in Slack.
- Conventions as in the existing note (`note_text.md`, `scripts/final/build_note.py`): numbered sections, figures built from repo CSVs, numbers checked by script.
- New charts needed: Figures 1, 2, 4 and 5. Figure 3 can reuse PLFS and Infosys CSVs.
- Open items before writing:
  - size the mid-tier share gain in pp (Section 3c);
  - the junior and experienced replacement rates in 2f rest on an assumed junior share of about 40%; check it against the firms' under-30 shares;
  - decide where the page lives (private claude.ai page or a Pages tab; the repo is public).
