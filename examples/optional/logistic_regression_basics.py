"""Optional logistic-regression example using a tiny synthetic dataset.

Install the optional ML dependency group before running this module:

    python -m pip install -e ".[ml]"

The example is intentionally small and demonstrates API usage only. It is not a
model-quality claim and is not suitable for real predictions.
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression


def build_sample_data() -> pd.DataFrame:
    """Return deterministic synthetic observations for the learning example."""
    return pd.DataFrame(
        {
            "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8],
            "practice_score": [45, 50, 55, 60, 66, 72, 78, 85],
            "passed": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )


def predict_pass_probability(
    frame: pd.DataFrame,
    *,
    hours_studied: float,
    practice_score: float,
) -> float:
    """Fit the demonstration model and return one probability between zero and one."""
    features = frame[["hours_studied", "practice_score"]]
    target = frame["passed"]

    model = LogisticRegression(max_iter=1_000, random_state=42)
    model.fit(features, target)

    observation = pd.DataFrame(
        {
            "hours_studied": [hours_studied],
            "practice_score": [practice_score],
        }
    )
    return float(model.predict_proba(observation)[0][1])


def main() -> None:
    sample_data = build_sample_data()
    probability = predict_pass_probability(
        sample_data,
        hours_studied=5,
        practice_score=70,
    )

    print("Optional logistic regression example")
    print("------------------------------------")
    print(sample_data.to_string(index=False))
    print(f"\nPredicted pass probability for the sample observation: {probability:.2%}")
    print("This output is a learning example, not a validated predictive model.")


if __name__ == "__main__":
    main()
