"""Shared paths and constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TIDY = ROOT / "data" / "tidy"
FIG = ROOT / "figures"
OUT = ROOT / "output"
for p in (TIDY, FIG, OUT):
    p.mkdir(parents=True, exist_ok=True)

INDIAN = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"]
COMPARATORS = ["cognizant", "accenture"]
FIRMS = INDIAN + COMPARATORS
LABEL = {"tcs": "TCS", "infosys": "Infosys", "hcltech": "HCLTech", "wipro": "Wipro",
         "techm": "Tech Mahindra", "ltim": "LTIMindtree", "cognizant": "Cognizant",
         "accenture": "Accenture", "lti": "LTI (pre-merger)", "mindtree": "Mindtree (pre-merger)"}

# windows (calendar quarters)
PRE_START, PRE_END = "2015Q2", "2022Q4"          # noise-calibration / baseline window
COVID = ["2020Q2", "2020Q3", "2020Q4"]            # excluded from noise calibration
RECENT_START = "2024Q2"                           # FY2025 Q1 for Indian firms
EPISODES = {  # (start, end) calendar quarters of past demand shocks, for signatures
    "GFC (FY2009-10)": ("2008Q3", "2009Q4"),
    "COVID (FY2021)": ("2020Q2", "2020Q4"),
    "FY2023-24 slowdown": ("2023Q1", "2024Q1"),
    "FY2025-27 (recent)": ("2024Q2", "2026Q2"),
}

RAW_COLS = ["firm", "fiscal_q", "period_end", "cal_q", "metric", "dimension", "dim_type", "value",
            "unit", "basis", "period_type", "source_url", "source_doc", "source_loc", "doc_date", "notes"]
