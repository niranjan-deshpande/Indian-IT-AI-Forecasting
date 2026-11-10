"""One command for the final-pass data, tables and figures:

    python3 01_pilot/scripts/note/make_all.py            # data -> subcontracting series -> tables and figures
    python3 01_pilot/scripts/note/make_all.py --ltim     # also re-extract data/rebuilt/raw/ltim.csv with the fixed parser first

Outputs: data/corrected/*_final.csv + CHANGELOG.csv; 01_pilot/output/final/table_A.*, table_B.*, calls_agreement.csv, note_numbers.csv;
         01_pilot/figures/final/fig1*, fig2*, fig3* (png, svg); 01_pilot/audit/calls_disagreements.csv, 01_pilot/audit/calls_spotcheck.csv.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd, env=None):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, env={**os.environ, **(env or {})})


if "--ltim" in sys.argv:
    run([sys.executable, "scripts/extract/ltim_build.py"], env={"LTIM_OUT": str(ROOT / "data/rebuilt/raw/ltim.csv")})
run([sys.executable, "01_pilot/scripts/note/build_final_data.py"])
run([sys.executable, "01_pilot/scripts/audit/subcontracting_series.py"])
run([sys.executable, "01_pilot/scripts/note/tables_figures.py"])
run([sys.executable, "01_pilot/scripts/note/calls_analysis.py"])
run([sys.executable, "01_pilot/scripts/note/verify_note_quotes.py"])
run([sys.executable, "01_pilot/scripts/note/note_numbers.py"])
