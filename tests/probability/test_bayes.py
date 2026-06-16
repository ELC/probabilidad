import math

import pytest

from probability import BayesInput, TotalProbabilityBranch, evaluate_bayes


def test_bayes_two_boxes() -> None:
    branches = (
        TotalProbabilityBranch(label="C1", prior=0.5, likelihood=0.3),
        TotalProbabilityBranch(label="C2", prior=0.5, likelihood=0.6),
    )
    posteriors = evaluate_bayes(BayesInput(branches=branches))
    assert math.isclose(posteriors[0].posterior, 1 / 3)
    assert math.isclose(posteriors[1].posterior, 2 / 3)
    assert math.isclose(sum(p.posterior for p in posteriors), 1.0)


def test_bayes_rejects_zero_evidence() -> None:
    branches = (
        TotalProbabilityBranch(label="A", prior=1.0, likelihood=0.0),
    )
    with pytest.raises(ValueError, match="evidence"):
        evaluate_bayes(BayesInput(branches=branches))
