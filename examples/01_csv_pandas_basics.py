"""
CSV / pandas basics.

This example uses a small in-memory CSV-style dataset.
It demonstrates:
- reading structured data
- creating a pandas DataFrame
- deriving a calculated column
- grouping and aggregating data

No external files are required.
"""

from io import StringIO

import pandas as pd


CSV_DATA = """city,category,month,value
Hamburg,weather,2026-06,18.5
Berlin,weather,2026-06,21.2
Munich,weather,2026-06,22.1
Hamburg,traffic,2026-06,74
Berlin,traffic,2026-06,81
Munich,traffic,2026-06,69
"""


def main() -> None:
    df = pd.read_csv(StringIO(CSV_DATA))

    print("Raw data:")
    print(df)

    print("\nAverage value by category:")
    summary = df.groupby("category", as_index=False)["value"].mean()
    print(summary)

    print("\nRows for Hamburg:")
    print(df[df["city"] == "Hamburg"])


if __name__ == "__main__":
    main()
