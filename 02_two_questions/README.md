# 02 Two questions: replacement rate and demand response (14–15 Oct 2026)

After the supervisor meeting on 6 Oct, the project stopped trying to separate the scenarios S1–S4 and instead estimated two quantities directly for the six largest firms, FY24–26: (1) the replacement rate, how much AI cut the labour needed per unit of work (overall and for juniors), and (2) the demand response, whether cheaper work led clients to buy more. Employment growth = d − s(1 − εφ).

**Main deliverable:** the internal checkpoint page for Andrei, `docs/two-questions.html` ([live](https://niranjan-deshpande.github.io/Indian-IT-AI-Forecasting/two-questions.html)). Its text is `checkpoint_text.md`.

| file or folder | what it is |
|--|--|
| `checkpoint_text.md` | Text of the page. `python3 02_two_questions/scripts/build_checkpoint.py` turns it into `docs/two-questions.html`. |
| `PLAN.md` | The estimation plan (model, measurement equations M1–M6, partial identification), then the numbers and file map handed to the writing agent on 15 Oct. |
| `explore/round3/` | Sector context: PLFS employment, GCCs, offshore competitors, listed-firm panel, seniority, red team. `SYNTHESIS.md` summarises. |
| `explore/round4/` | The measurements: `residual/` (M1, saving kept), `price_statements/` (M2, saving passed on), `junior_gap/` (M4), `demand_shift/` (M5), `elasticity_xsec/` (M6), and `robustness/` (R1–R3). `SYNTHESIS.md` is the first pass and is outdated on s̄; the robustness folders supersede it. |
| `scripts/` | The page builder and its HTML template. |

Every measurement folder has a `FINDINGS.md` with methods, numbers, source URLs and caveats. Raw downloads sit in gitignored `raw/` subfolders.
