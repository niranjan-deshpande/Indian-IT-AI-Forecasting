# Task 2 figures

To regenerate every figure here from the corrected data in one step:

```bash
cd scripts && python 08_task2_graphs.py
```

To rebuild the corrected data first, run `python scripts/audit/build_corrected.py` from the repo root. Add `--original` to the graphs command to draw the same figures from the pilot's uncorrected `data/tidy` files; they go to `figures/task2_original/`, for comparison only.

| file | content |
|--|--|
| `01_revenue_usd.png` | Revenue growth, reported USD |
| `02_revenue_cc.png` | Revenue growth, constant currency, as reported by each firm |
| `03_headcount.png` | Headcount growth (HCLTech's base is net of the 7,398 people divested in Q1FY25) |
| `04_revenue_per_employee.png` | Revenue per employee growth, using reported-USD revenue |
| `05_utilization.png` | YoY change in utilization, within each firm's reported series |
| `06_residual.png` | Residual g(R/L) − g(u), using cc revenue (the pilot's definition); only firms that report utilization |
| `07_gap_vs_accenture.png` | Indian average minus Accenture, revenue (cc) and headcount, annual and quarterly |
| `08_rolling_correlation.png` | 8-quarter rolling correlation of the Indian average with Accenture, and with Cognizant |
| `plotted_series_*.csv` | Every plotted line as a table (table view) |
| `weighting_check.csv` | Simple mean vs revenue-weighted Indian average |

Each growth figure has two panels: annual (calendar year) on top, quarterly YoY below. Lines are the six Indian firms, two Indian averages, Accenture and Cognizant.

## Definitions
- **Growth rates** are YoY log changes × 100.
- **Annual panels use calendar years.**
  - Revenue in USD: log change of the sum of 4 quarters.
  - cc revenue, headcount, utilization and residual: mean of the 4 quarterly YoY values.
  - Revenue per employee: annual USD revenue growth minus annual headcount growth.
  - A year is plotted only if all 4 quarters exist.
  - Annual cc growth is therefore an approximation, not a firm-reported annual figure.
- **Fiscal-year alignment.** Each firm's fiscal quarter is placed in the calendar quarter that contains its quarter end (Accenture: Nov→Q4, Feb→Q1, May→Q2, Aug→Q3). Audit item 3 found this to be the best mapping available.
- **Indian average.** Both versions are always shown:
  - **Simple mean** (solid black) across the Indian firms that report that period.
  - **Revenue-weighted mean** (dashed black), weighted by USD revenue in the same period, over the firms that report USD revenue. Wipro has no IT Services USD revenue in 2007–12, so it is in the simple mean but not the weighted one in that window.
  - Before 2022Q3, pre-merger LTI and Mindtree count as **one** entity (their USD-revenue-weighted mean) and LTIMindtree is excluded. From 2022Q3 only LTIMindtree is used. There is no level splice. This differs from the pilot, which counted LTI and Mindtree as two firms (audit item 6). It changes only the simple mean, and only before 2022Q3.
  - The firm set changes over time, most of all for utilization and the residual: TCS stops after 2015Q4 and HCLTech after 2019Q1. A move in the average can therefore reflect a change in which firms are included.
- **Does the weighting choice matter?** See `weighting_check.csv`.
  - Across the quarterly metrics, the two averages differ by 0.5–1.2 pp on average (mean absolute difference). Single quarters differ by up to 2.7–6.9 pp, mostly in 2008–12 and 2021–22.
  - From 2023 on, the mean signed difference is within ±0.35 pp.
  - So weighting barely matters for the post-2023 comparison. It does matter for individual quarters.
- **Rolling correlation.** Pearson correlation over the 8 consecutive quarters ending at the plotted quarter. A window that spans a missing quarter is dropped.
- **Vertical lines** mark 2022 (2022-01-01) and 2023Q1 (2023-01-01).
- **Shading** marks 2008–09 and COVID. The COVID band covers the YoY quarters 2020Q2–2021Q2, the same quarters the pilot excludes from calibration (DECISIONS D30).
- **Dotted vertical lines** on the utilization and residual figures mark the last quarter of utilization data for TCS (Q3FY16 = 2015Q4) and HCLTech (Q4FY19 = 2019Q1).
- **Breaks in a line** mean no data. For most firms, 2012Q3–2015Q1 was not collected.
- **Clipping.** Values are clipped to [−40, 60].

## Caveats
- **Inorganic growth is not adjusted**, as in the pilot. Examples: Cognizant Belcan (about 4 pp, 2024Q4–2025Q2); Accenture's acquisitions (FY25 guidance "a bit more than 3%"); HCLTech's IBM products deal (2019); Wipro's Alight transfer (about 9,000 people, Q2FY19).
- **HCLTech revenue is not adjusted** for the Q2FY25 divestiture, although its headcount base is.
- **Palette.** Colours are the validated 8-slot categorical palette. Three of them (aqua, yellow, magenta) are below 3:1 contrast on white, so the `plotted_series_*.csv` tables serve as the accessible table view.
