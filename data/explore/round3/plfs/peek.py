"""Print value counts of selected columns (aggregate only). Usage: python3 -I peek.py FILE col1,col2 [describe_cols]"""
import sys
import pandas as pd
f, cols = sys.argv[1], sys.argv[2].split(",")
desc = sys.argv[3].split(",") if len(sys.argv) > 3 else []
df = pd.read_stata(f, columns=cols + desc, convert_categoricals=False)
print(f, len(df))
for c in cols:
    print("--", c, df[c].dtype)
    print(df[c].value_counts(dropna=False).sort_index().head(40).to_string())
for c in desc:
    print("--", c); print(df[c].describe().to_string())
