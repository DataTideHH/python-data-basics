from __future__ import annotations

from examples.optional.logistic_regression_basics import (
    build_sample_data,
    predict_pass_probability,
)


def test_optional_ml_example_returns_probability() -> None:
    sample_data = build_sample_data()
    probability = predict_pass_probability(
        sample_data,
        hours_studied=5,
        practice_score=70,
    )

    assert sample_data.shape == (8, 3)
    assert 0.0 < probability < 1.0
