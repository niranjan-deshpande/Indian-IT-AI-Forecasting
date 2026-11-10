# 03 Health check of India's IT services (15 Oct – 1 Nov 2026)

A chart-heavy tour of the evidence on how India's IT-services sector is doing in 2026: output still growing, growth moving away from the largest firms, employment not keeping pace, the entry level narrowing as a share, little strain on the firms, and AI mostly still ahead in the data. The two-questions estimates are deliberately left out as too assumption-sensitive.

**Main deliverable:** `docs/health-check.html` ([live](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/health-check.html)). Its text is `health_check_text.md`. `health_check_SPAR_midterm.pdf` is a 31-page PDF print of the page for the SPAR midterm (1 Nov; not tracked by git).

| file or folder | what it is |
|--|--|
| `health_check_text.md` | Text of the page. `python3 03_health_check/scripts/build_health_check.py` turns it into `docs/health-check.html`. |
| `health_check_number_check.md` | Every number on the page checked against its source (`python3 03_health_check/scripts/health_check_number_check.py`; 273 of 273 pass). |
| `explore/health_check/charts/` | The CSVs behind every chart, built by `prep_output.py`, `prep_jobs.py` and `prep_business.py` from data in all earlier stages. |
| `explore/health_check/inventory/` | Five-part read of all the project's data before drafting, with candidate charts. |
| `explore/health_check/literature/` | `CATALOGUE.md`/`.csv`: 222 citable claims from others' work, flagged by whether we can reproduce them. |
| `explore/health_check/{epfo,fresher_thirdparty,labour_share,postings,contradictions}/` | Data added for the page, and checks of claims that contradict it. Each has a `FINDINGS.md`. |
| `scripts/` | Page builder, HTML template and number check. |

PLFS results carry the MoSPI data-access obligations: aggregates only, cite PLFS (MoSPI), and send nssunit.dsdd@mospi.gov.in a copy of any publication.
