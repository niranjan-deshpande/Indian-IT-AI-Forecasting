# 01 Pilot: feasibility study and research note (27 Sep – 6 Oct 2026)

Can public firm data tell why headcount growth at India's six largest IT-services firms stalled after FY23: falling demand (S1), AI cutting labour per unit of work with prices held (S2) or passed on (S3), or work moving to clients' own centres and subcontractors (S4)? The pilot built a quarterly panel from primary filings, ran a decomposition and a detection-power simulation, then audited the data and wrote a short public note.

**Main deliverable:** the research note, `docs/index.html` ([live](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/)). Its text is `note_text.md`.

| file or folder | what it is |
|--|--|
| `note_text.md` | Text of the note. `python3 01_pilot/scripts/note/build_note.py` turns it into `docs/index.html`. |
| `note_number_check.md` | Every number in the note checked against its source (`python3 01_pilot/scripts/note/note_number_check.py`). |
| `REPORT.md` | The pilot report (27 Sep), with appendices on data coverage (A), judgment calls (B) and next steps (C). |
| `FOLLOWUP.md` | Working record of the 5 Oct follow-up and final pass: data audit, price-data search, earnings-call coding, and the inputs used to write the note. |
| `evidence/` | Source screens behind the note: `price_data.md` (is there a usable price series?), `price_calls_timeline.md` (management statements on pricing, 2021–26), `discriminating_data.md` (sources that could separate S1–S4), `note_quotes.md` (the six verified quotes). |
| `audit/` | Row-level audit evidence and the earnings-call corpus: 2,087 coded statements, both coders' codes, the codebook (`calls_codebook.md`), spot-checks, corrections. |
| `output/` | Pilot tables (`*.csv`, `*.md`); `output/final/` holds the note's tables and `note_numbers.csv`. |
| `figures/` | Pilot figures (`fig1`–`fig9`, used in `REPORT.md`); `figures/final/` the note's figures; `figures/task2/` the follow-up graphs. |
| `explore/` | Feasibility probes run after the pilot (`PROBE_BRIEF.md` is the brief): `lca/` (H-1B filings), `midtier/` (mid-tier firms), `prices/` (price indices), `text_firms/` (call-text term counts), `trade/` (services trade), `workforce/` (firm workforce and fresher data). Most have a `FINDINGS.md`. |
| `scripts/` | `01_build_tidy.py` … `08_task2_graphs.py`: the pilot pipeline (run from `01_pilot/scripts/`; `common.py`, `sim_model.py`, `noise_calibration.py` are its helpers). `audit/`: the audit and call-coding scripts. `note/`: the note's data, tables, figures, page builder and number check; `python3 01_pilot/scripts/note/make_all.py` rebuilds them all. |

`01_pilot/scripts/note/build_note.py` also holds the page helpers that the later page builders (`02_two_questions/`, `03_health_check/`) import.
