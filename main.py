import sys

import matplotlib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression


def print_environment() -> None:
    print("Python data environment check")
    print("-----------------------------")
    print(f"Executable: {sys.executable}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"pandas: {pd.__version__}")
    print(f"NumPy: {np.__version__}")
    print(f"matplotlib: {matplotlib.__version__}")
    print(f"scikit-learn: {sklearn.__version__}")
    print()


def build_sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8],
            "practice_score": [45, 50, 55, 60, 66, 72, 78, 85],
            "passed": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )


def run_logistic_regression(df: pd.DataFrame) -> None:
    features = df[["hours_studied", "practice_score"]]
    target = df["passed"]

    model = LogisticRegression()
    model.fit(features, target)

    new_student = pd.DataFrame(
        {
            "hours_studied": [5],
            "practice_score": [70],
        }
    )

    probability = model.predict_proba(new_student)[0][1]

    print("Sample data")
    print("-----------")
    print(df.to_string(index=False))
    print()

    print("Minimal logistic regression example")
    print("-----------------------------------")
    print(f"Predicted pass probability for the sample student: {probability:.2%}")


def main() -> None:
    print_environment()
    sample_data = build_sample_data()
    run_logistic_regression(sample_data)


if __name__ == "__main__":
    main()
