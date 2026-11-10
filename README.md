# Indian IT and AI

Research on what AI is doing to jobs at India's IT-services and BPO firms, written as part of SPAR (Fall 2026) and supervised by Andrei Potlogea. It began as a feasibility pilot on why headcount at the six largest firms stalled after FY23, became a short public note, then two internal estimates (how much labour AI saves per unit of work, and whether cheaper work raises demand), a chart-heavy health check of the whole sector, and a bottom-up model of per-task AI labour savings (θ_j). Each stage lives in its own folder; the firm data, raw-data extraction code and published pages are shared.

## Project folders

| folder | dates (2026) | what it is | main deliverable |
|--|--|--|--|
| [`01_pilot/`](01_pilot/README.md) | 27 Sep – 6 Oct | Feasibility pilot (can public data separate demand, AI and offshoring explanations of the headcount slowdown?), then a data audit and a short research note. | [`docs/index.html`](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/), text in `01_pilot/note_text.md` |
| [`02_two_questions/`](02_two_questions/README.md) | 14 – 15 Oct | Internal checkpoint estimating the AI replacement rate and the demand response for the top six firms, FY24–26. | [`docs/two-questions.html`](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/two-questions.html), text in `02_two_questions/checkpoint_text.md` |
| [`03_health_check/`](03_health_check/README.md) | 15 Oct – 1 Nov | Health check of India's IT-services sector: output, who is growing, jobs, the entry level, firm health, demand. | [`docs/health-check.html`](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/health-check.html), text in `03_health_check/health_check_text.md` |
| [`04_theta_model/`](04_theta_model/README.md) | 26 Oct – 7 Nov | Model and first-pass estimate of θ_j, the share of labour AI saves on each service line; literature review. | [`docs/theta-model.html`](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/theta-model.html), text in `04_theta_model/theta_model_text.md` |
| `delegable_share/` | Nov – | Reliability-adjusted AI exposure measure. | spec in `delegable_share/SPEC.md` |

Inside each stage folder: the page text and its number check at the top, `explore/` for the data gathered in that stage (each topic folder has a `FINDINGS.md` with methods and source URLs), and `scripts/` for the code. Later stages read data from earlier ones by repo-relative path.

## Shared

- **`data/`**: the quarterly firm panel for eight firms (TCS, Infosys, HCLTech, Wipro, Tech Mahindra, LTIMindtree, Cognizant, Accenture), used by every stage: `raw/`, `tidy/`, `corrected/` (the `*_final.csv` files are what the pages use), `rebuilt/`. See `data/README.md` for the schema and how it was collected. Downloaded source documents (`data/sources/`, ≈7 GB, including PLFS microdata) are gitignored; their URLs are recorded in the data and audit files.
- **`scripts/extract/`**: the per-firm scripts that built `data/raw/` from filings.
- **`docs/`**: the published site (GitHub Pages serves this folder at https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/), with shared page figures in `docs/figures/`. The pages are generated; edit the text files in the stage folders and rebuild.

## Rebuilding

All commands run from the repo root; every path in code and docs is relative to it.

- Pilot note: `python3 01_pilot/scripts/note/build_note.py`; number check `python3 01_pilot/scripts/note/note_number_check.py`; data, tables and figures behind it `python3 01_pilot/scripts/note/make_all.py` (see `01_pilot/FOLLOWUP.md`).
- Two-questions page: `python3 02_two_questions/scripts/build_checkpoint.py`.
- Health check: `python3 03_health_check/scripts/build_health_check.py`; number check `python3 03_health_check/scripts/health_check_number_check.py`.
- θ memo: `python3 04_theta_model/scripts/build_theta_model.py` (needs `markdown`); estimate `python3 04_theta_model/scripts/run_estimate.py`.

PLFS unit-level data were obtained under a MoSPI data-access agreement: only aggregates leave `data/sources/plfs/`, results cite PLFS (MoSPI), and any publication using them is sent to nssunit.dsdd@mospi.gov.in.
