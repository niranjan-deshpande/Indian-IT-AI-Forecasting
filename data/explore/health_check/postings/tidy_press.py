"""Tidy press/report-sourced India posting data points.

Input : press_datapoints_raw.csv  (hand-collected from press coverage and blog posts;
        columns source_org,series,month,value,unit,article_title,publisher,article_date,url,quote)
Output: press_datapoints.csv      same rows, de-duplicated, sorted, with
        reproducible = False (numbers read from articles, no underlying data file).
Run   : python3 -I tidy_press.py
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "press_datapoints_raw.csv"))
d["value"] = pd.to_numeric(d["value"], errors="coerce")
d = d.dropna(subset=["value"])
# keep one row per series-month-unit, preferring the earliest-published article (first print)
d = d.sort_values(["series", "month", "unit", "article_date"]).drop_duplicates(["series", "month", "unit"], keep="first")
d["reproducible"] = False
d["flag"] = "press/report-sourced; not reproducible from public microdata"
d.to_csv(os.path.join(HERE, "press_datapoints.csv"), index=False)
print(d.groupby(["source_org", "series", "unit"]).size().to_string())
