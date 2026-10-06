"""One command for the final-pass data, tables and figures:

    python3 scripts/final/make_all.py            # data -> subcontracting series -> tables and figures
    python3 scripts/final/make_all.py --ltim     # also re-extract data/rebuilt/raw/ltim.csv with the fixed parser first

Outputs: data/corrected/*_final.csv + CHANGELOG.csv; output/final/table_A.*, table_B.*, calls_agreement.csv, note_numbers.csv;
         figures/final/fig1*, fig2*, fig3* (png, svg); calls_disagreements.csv, calls_spotcheck.csv.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd, env=None):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, env={**os.environ, **(env or {})})


if "--ltim" in sys.argv:
    run([sys.executable, "scripts/extract/ltim_build.py"], env={"LTIM_OUT": str(ROOT / "data/rebuilt/raw/ltim.csv")})
run([sys.executable, "scripts/final/build_final_data.py"])
run([sys.executable, "scripts/audit/subcontracting_series.py"])
run([sys.executable, "scripts/final/tables_figures.py"])
run([sys.executable, "scripts/final/calls_analysis.py"])
run([sys.executable, "scripts/final/verify_note_quotes.py"])
run([sys.executable, "scripts/final/note_numbers.py"])
