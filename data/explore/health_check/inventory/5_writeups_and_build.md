# Inventory: write-ups, round-4 estimates and page build system

## 1. Project history: how the argument changed

**Pilot (`REPORT.md`, `DECISIONS.md`, about 5 Oct).** This asked whether public data can tell why headcount fell at the six largest firms. It set up four scenarios:
- **S1:** demand fell.
- **S2:** each unit of work needed less labour, prices held, and firms kept the saving.
- **S3:** the saving was passed on as lower prices.
- **S4:** work moved to clients' own Indian centres (GCCs), smaller firms or contractors.

Its tools were the identity g(R/L) = g_u + (g_p − g_a), a calibrated simulation of how well the data could tell the scenarios apart, and an illustrative Bayesian test on FY25–27. Its verdicts:
- S2 is rejected.
- S1 and S3 cannot be told apart (about 0.77 accuracy at best). With full pass-through they predict the same paths.
- S4 is fragile.
- The S1, S3 and S4 posteriors flip with judgment calls (D1–D5).

**`NEXT_STEPS.md`.** This was a funding memo built around user personas. It argues that hours and rate cards measure p/a, so they fail by construction. It proposed a gated plan to buy role-level data. It also contains early descriptive leads:
- Total software exports grew 7–8% in FY25–26, against −1% to +6% for the big vendors.
- The GCC share kept rising, but did not speed up.
- Management talk moved from demand to pass-through.

**`FOLLOWUP_SUMMARY.md` and `FINAL_PASS_SUMMARY.md` (5 Oct).** These are a data audit and the inputs to the note.
- The audit found the pilot's "FY25–27" baseline row counted the LTI business up to three times: baseline headcount growth is 9.9%, not 11.8%.
- The 0.90 → 0.58 correlation with Accenture rests on one episode, the 2021–22 boom and bust. It was dropped.
- A clean fiscal-year table: headcount +7.4 (FY16–20), +18.5 (FY22), +14.3 (FY23), −3.6 (FY24), −0.5 (FY25), +1.2 (FY26).
- 2,087 earnings-call statements were coded by two independent LLM coders (κ = 0.87).
- Subcontracting fell at all six firms in FY24.
- BLS publishes no price index for NAICS 5415.
- Mid-tier four: +14–15% revenue in FY25–26.

**The pilot note (`note_text.md` → `docs/index.html`, 6 Oct).** This kept the S1–S4 framing. Its claims:
- At four firms, there is no sign firms kept AI savings (S2 out).
- There is no shift to contractors.
- GCC evidence is weak.
- Managers added AI pass-through talk on top of demand talk.
- A price index would settle the question.

**Andrei's direction on 6 Oct (memory note; not recorded in the repo).** Make it a general health check, with AI as the motivation rather than the claimed cause. The policymaker cares about the sector as a job and mobility ladder for educated Indians. Lead with S4 against S1/S3, then split S4:
- S4a: to GCCs.
- S4b: to mid-tier firms.
- S4c: to contractors (already ruled out).
- S4d: out of India.

S4a and S4b are benign; S1, S3 and S4d are harmful.

**Reframe on 14–15 Oct (`ESTIMATION_PLAN.md`, `round4/SYNTHESIS.md`, robustness R1–R3, `OUTLINE.md`, `checkpoint_text.md` → `docs/two-questions.html`).** The project now estimates two quantities, using g_L = d − s(1 − εφ):
- s: the replacement rate.
- φ: the share of the saving passed on in prices.
- ε: the price elasticity of demand.
- d: the demand shift.

There are six measurements, M1–M6. The old scenarios become regions of this parameter space (checkpoint appendix).

**Current best numbers (checkpoint, from `robustness/m1_scope_subcon`):**

| Quantity | Estimate |
|---|---|
| Saving kept (M1, top six, subcontracting-corrected, FY16–20 baseline) | **2.1 pp/yr** (1.8–2.4 across k; 1.5–3.0 within bounds) |
| Saving passed on (M2) | **0.2** (FY24 0, FY25 0.1, FY26 0.4; FY27 about 1.5, range 0.4–2.7, mostly expected) |
| Replacement rate s̄ | **2.3 pp/yr** (1.5–3.6 bounds; −0.8 to 7.1 with sampling noise; zero not rejected), i.e. **about 93 workers per 100** after three years (90–96) |
| φ | about 0.09: firms kept about nine-tenths of the saving |
| Headcount slowdown vs FY16–20 growth | −8.3; revenue (cc) −7.1 |
| Gap vs pre-COVID path | headcount −3.0, revenue −5.7 |
| Gap vs Accenture and Cognizant | headcount −1.5, revenue −3.1 |

Against the peers yardstick, 57% of the revenue slowdown is shared with Accenture and Cognizant. Levels in FY26: headcount 11% below trend, revenue 18% below, Accenture back on trend.

Demand shift d ≈ −7 under the growth yardstick. Measured causes total about −1.6:
- client spending −0.5;
- US in-housing −1.6;
- GCCs +0.5 (−2.2 to +1.6);
- mid-tier firms at most about 1.5, excluded from the total.

Bringing subcontracted work in-house added about +1.1 to headcount. ε is not identified; the prior is 0.5–1.5 for IT (centre 0.9) and 0.2–0.9 for BPO.

**Stale or wrong claims:**
- The note's "no sign firms kept AI savings" is reversed by the subcontracting correction (four firms, no correction before).
- `SYNTHESIS.md`'s s̄ ≈ 1.2, "AI is 15% of the slowdown" and M5 = −3.1. Its GCC estimate of about −1 is now +0.5.
- "The slowdown was 8.3 pp" holds only under growth-rate baselines.
- "The hangover explains the residual" holds only on the headcount route.
- "Unexplained 3–4 pp" was never statistically established (R1 §5).
- The pilot's Bayesian posteriors, the 11.8% baseline, the Accenture correlation, and the HCLTech divestiture adjustment (D10, now removed).
- `NEXT_STEPS`' "GCC shift slowed (+1.6 vs +3.0 pp)" now reads as "similar pace before and after".
- The note's §5b GCC evidence (RBI ₹6.5 → 8.5 lakh crore; BEA 600k → 900k) is weak and has been superseded.
- `note_number_check.md` lists doc-vs-data discrepancies: Cognizant FY25 is −2.5, not −2.6; BLS 2025 is +3.2, not +3.3; HCLTech is not the second-largest firm.

## 2. Claims about the sector's current state

**Well supported (primary filings, checked by script or by hand):**
- Top-six headcount: about +7%/yr before COVID, +18% in FY22, +14% in FY23, −3.6% in FY24 (fell at 5 of 6 firms), roughly flat since.
- Revenue (cc): about 9%/yr before COVID, 1–3% from FY24.
- In levels, FY26 headcount is about 11% and revenue about 18% below the FY16–20 trend. Accenture is back on trend; Cognizant slowed without having boomed.
- The FY22–23 boom overshoot was in staff (+14 log points), not revenue (+3.5).
- About half of the revenue slowdown is shared with global peers. About 3 pp/yr is specific to the Indian firms.
- Mid-tier four: revenue +14–15% in FY25–26, but their share of combined revenue rose only from 5.1% to 7.3%.
- Subcontracting share fell at all six firms in FY24 and edged up at five in FY26.
- No measured AI price cuts through FY26. Firms say so themselves:
  - HCLTech (Apr 2026): "very little has really played out".
  - TCS (Oct 2026): pricing "broadly stable".
- Demand talk on calls peaked in 2023 (7.5–7.9 per transcript) and has stayed at about 5. Pass-through talk rose from 2024H2.
- India's share of world computer-services exports (excluding Ireland) is flat at about 30% for 2022–25. The work did not leave India.
- PLFS sector employment in IT (NIC 62–63) is flat at about 5.7m since 2022-23. Young graduates in IT are flat at about 2.6–3.0m.
- US in-house share of computer jobs rose from 64–65% to 67.5%. CES employment in NAICS 5415 went from +3.6%/yr to −0.6%/yr.
- Infosys: hiring of over-30s up 65%, under-30 hiring flat.

**Shaky:**
- s̄ itself. Zero is not rejected, it rests on the subcontracting correction (breaks if more than about 60% of the cost fall was cheaper contractors), and the level view could shrink it to zero.
- Non-AI productivity growth is unchecked.
- The "share of slowdown" figures swing from about 25% to over 100% depending on the yardstick.
- The demand decomposition: the UK in-housing piece is unverified, GCC numbers come from staffing firms and Nasscom-Zinnov (editions not comparable), and the residual is wide.
- Junior effects:
  - The firm-level junior gap is 0 to +1 (range −2 to +3).
  - The PLFS gap has a confidence interval that includes zero.
  - Relative junior pay: −5.4/yr from 2020-21, but about −1.6/yr from 2017-18, which is not significant.
  - The PLFS 2025 redesign plus one heavily weighted sampling unit inflate the latest points.
- ε is borrowed from history.
- Call statements were coded by LLMs and not checked by hand.
- Utilisation is missing for TCS and HCLTech.
- No figures are adjusted for acquisitions.

## 3. Style and build system

**Two pages, two builders.** Both write self-contained HTML into `docs/` for GitHub Pages. The repo is public (`REPO_URL = github.com/niranjan-deshpande/Indian-IT-AI-Forecasting`).
- `scripts/final/build_note.py`: `note_text.md` → `docs/index.html`. The template is inline (`TEMPLATE = r"""..."""`); there is no left table of contents.
- `scripts/final/build_checkpoint.py`: `checkpoint_text.md` → `docs/two-questions.html`. The template is the separate file `scripts/final/checkpoint_template.html`. This is the model to copy (per the write-up style memory).

**Markdown conventions** (documented in the HTML comments at the top of each text file):
- YAML-like front matter: `title`, `byline` (the last "·" item becomes a tag pill, e.g. "Working draft"), `thanks`.
- `## 1. Title` makes a numbered h2 (number shown in a grey span); `### ` makes an h3. Under `## Appendix`, each `###` becomes a `<details class="app">` collapsible.
- Inline (`inline()` in `build_note.py`): `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, automatic curly quotes (`smarten()`), and tokens such as `{{repo}}`. The note also supports `{{quote key}}`, rendered from the `QUOTES` dict as a `<blockquote>` with a source link.
- `$$ … $$` on their own lines: displayed equation, rendered client-side by KaTeX from `data-tex`.
- Footnotes (checkpoint only): `[^key]` in text, defined as `[^key]: text` lines at the end. `Doc.il()` turns them into numbered hover pop-ups (`span.fn > a.fn-ref + span.fn-pop`), with tap support on mobile. An "All notes" collapsible is appended. `main()` asserts there are no undefined and no unused footnotes.
- Blocks:
  - `::: answer … :::` makes the "Short answer" box.
  - `::: details Title … :::` makes a `details.more` collapsible; it can contain figures, appears in the TOC with a "+", and nests.
  - `::: figure NAME … :::`: the body is the caption.
  - `::: table [NAME]`: first line is the caption, pipe-format rows, then `---` and a note line. A named table is generated from CSVs (`GENERATED_TABLES` in the note); an unnamed one is hand-written. Rows containing ↑ or ↓ get the "pred" styling.
  - HTML comments are dropped.

**Charts.** Plotly.js 2.27.0 from cdnjs, drawn client-side.
- Each figure's HTML shell lives in a Python `FIGURES` dict. In the checkpoint this is built by the helper `fig(name, title, legend)`, with legend swatches from `sw()` (square) and `ln()` (line). The shell contains `<div id="chart-NAME" class="chart">` and a `{caption}` slot.
- Data: one Python function per figure (`levels_data()`, `kept_data()`, `demand_data()`, …) reads repo CSVs. All results go into one dict, serialised as JSON into `%%DATA%%`, i.e. `const DATA = {...}` in the page. Nothing is hand-typed.
- JS: one function per figure (`figLevels`, `figSubcon`, …) using the helpers `baseLayout`, `axis`, `draw`, `twoPanels` (side by side, or stacked when narrower than 640px), `forest()` (range and forest plots), `ptitle`, `zeroLine`, `vZero`, `tint`, `f1`, `FYT`.
- Registry: `CHARTS = {"chart-x": fn}`. Charts are drawn lazily, including when a `<details>` is opened, and redrawn on resize.
- Config: mode bar off, axes fixed (no zoom), legends drawn in HTML rather than Plotly.
- Firm colours: `FIRM = {tcs:"#4d6f91", infosys:"#b8643f", hcltech:"#5a9370", wipro:"#8f68a6", techm:"#ae8a2c", ltim:"#c0607e"}`.
- `main()` asserts every `chart-` id in the text has data.
- Template placeholders: `%%TITLE%%`, `%%TOC%%`, `%%BODY%%`, `%%DATA%%`; the build asserts none is left over.
- The note has interactive toggles (revenue-weighted vs simple average; coder 1 vs coder 2).

**CSS look (light only, warm paper):**
- Background `#fbf8f3`, panels `#fffdf9`, ink `#2a2318`, `#5e5245`, `#8a7d6d`, rules `#e6ddd0` and `#cfc4b4`.
- Accent blue `#235fa6`, mid-tier green `#2f8a57`, Accenture grey `#7a7268`, category orange `#b0702a`.
- Fonts: Source Serif 4 for body (17.5px, line height 1.6) and Source Sans 3 for UI, captions, tables and the TOC (Google Fonts).
- Layout: centred 700px column on a 3-column grid; `.wide` figures span up to 920px. Figures sit in bordered panels with sans captions. Tables use tabular numerals, right-aligned.
- Left TOC: fixed 250px sidebar at widths of 1180px and up, with scroll-spy (`.active`) and auto-opening of collapsed targets. Below that width it becomes a `details.toc-mobile` "Contents" dropdown. Breadcrumbs link the two pages.
- Print styles included.

**Number checking.** `scripts/final/note_number_check.py` → `note_number_check.md`. It currently covers only `docs/index.html` (152/152 pass). There is no number check for `two-questions.html`.
- Each number in the prose is registered by hand with `num(printed, where, source, key, value, shown, digits)`. The check passes if the value rounds to the printed precision.
- Other entry types: `rng()` for ranges, `cond()` for word claims ("barely grew"), and `txt()` for strings that must appear verbatim in the cited file.
- A final coverage scan strips years, FY labels and section numbers from the page text and lists any numeric token no entry covers.
- `verify_note_quotes.py` checks quotes.

**Data pipeline.** `make_all.py` runs `build_final_data` → `audit/subcontracting_series` → `tables_figures` → `calls_analysis` → `verify_note_quotes` → `note_numbers`. Outputs go to `output/final/` (`table_A.csv`, `table_A_firms.csv`, `table_B`, `note_numbers.csv`, `fig2_data.csv`, `fig3_data.csv`). Neither page builder is part of `make_all.py`.

**Reusing it for a health-check page:**
1. Copy `build_checkpoint.py` to a new builder with new `OUT` and `TEXT` paths. Keep `from build_note import inline, pipe_table, clean, fig2_data, ROOT, FINAL, REPO_URL`.
2. Copy or adapt `checkpoint_template.html`: meta description, breadcrumbs in `main()`, JS chart functions and the `CHARTS` map.
3. Write the text file using the same block syntax.
4. Add a `*_data()` function, a `FIGURES` entry and a JS `figX` for each chart.
5. Clone `note_number_check.py` with `PAGE` and `OUT` repointed.
6. Add the PLFS (MoSPI) attribution line: aggregate tabulations only, cite MoSPI, and send MoSPI a copy.

## 4. Material for the health-check framing

- **Policy question already written down** (`ESTIMATION_PLAN.md` §1): "Is India's IT sector still growing as a source of good jobs, and in particular as an entry point for young graduates? If not, why not?" This is close to Andrei's job-ladder framing.
- **Andrei's requested claims** (memory note): S4 vs S1/S3 with a confidence level; data that would raise confidence, ranked by cost; S2 ruled out; S1 vs S3 not separable, with a call to action. The benign/harmful split of S4 maps onto the checkpoint's demand-shift parts:
  - GCCs: no change in pace.
  - Mid-tier: bounded at ≤1.5 pp/yr.
  - Contractors: ruled out, since subcontracting fell.
  - Out of India: no, since India's export share is flat.
- **Job-ladder indicators already measured**, mostly with charts already built:
  - PLFS IT employment flat at about 5.7m.
  - Graduates aged 21–30 in IT flat at 2.6–3.0m.
  - IT's share of employed young graduates fell from 12.8% to 9.9%.
  - NIRF engineering placements fell for the class of 2023-24 (73.8% → 70.1%), the first fall since 2016-17.
  - Relative pay of 21–25-year-olds in IT fell from 0.64 to 0.52 (suggestive only).
  - Under-30 share of headcount by firm; Infosys hires by age.
  - Fresher hires per $bn of revenue about half the pre-COVID level.
  - GCCs hire few freshers: rising GCC fresher postings offset only about a fifth of the fall at IT firms.
  - Warning: the boom cohort turns 30 around FY30–31, which will push under-30 shares down mechanically.
- **"Sector vs top six" leads** that suit a broad but nuanced claim (the top six stalled; the sector did not collapse):
  - Mid-tier growth and the 21-listed-firm panel.
  - Total software exports up 7–8% in FY25–26.
  - Flat export share.
  - Naukri Sep 2026: GCC postings +4%, IT services −4%.
  - Caveat: GCC staff are in PLFS but cannot be separated out.
- **Vintage caveat.** All outcome data predate the mid-2026 step change in coding agents.
- **What would sharpen the picture:** FY27 results, utilisation for TCS and HCLTech, the RBI census of foreign-owned firms (due late Oct 2026), GCC employee counts the RBI collects but does not publish, a price index, and a UK in-housing series.
- **Open items before writing, from `OUTLINE.md`:** size the mid-tier share gain in pp; check the assumed junior share of about 40% (the footnote now uses half); decide where the page lives, since the repo is public.