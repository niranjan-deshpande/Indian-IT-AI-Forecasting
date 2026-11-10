# 04 Estimating θ_j: per-task labour savings from AI (26 Oct – 7 Nov 2026)

A model of θ_j, the share of labour AI saves on service line j, built bottom-up from task lengths, AI time horizons (METR), agent costs, review time and wages, then taken to the data for a first-pass estimate.

**Main deliverable:** the internal memo for Andrei, `docs/theta-model.html` ([live](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/theta-model.html)). Its text is `theta_model_text.md`.

| file or folder | what it is |
|--|--|
| `theta_model_text.md` | Text of the memo. `python3 04_theta_model/scripts/build_theta_model.py` turns it into `docs/theta-model.html` (needs the `markdown` package). |
| `theta_j_literature.md` | Verified literature review (26 Oct): what the literature gives for each parameter, the gaps, and what to do next. `theta_j_literature.json` is the underlying digest. |
| `explore/theta_estimate/` | The first-pass estimate (7 Nov): `FINDINGS.md`, `results/` (independent priors), `results_correlated/` (correlated priors; work in progress, not yet committed), `figures/`, and `research/` notes behind the priors. |
| `explore/theta_lit/` | METR benchmark results used for the time horizons. |
| `scripts/` | `theta_model.py` (the model), `priors.py` (input ranges and their correlations), `run_estimate.py` (Monte Carlo; `--correlated` for correlated priors), `figures.py` and `page_figures.py` (the memo's SVGs in `docs/figures/theta/`), and the page builder. |
