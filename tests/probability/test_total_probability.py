import math

import pytest
from pydantic import ValidationError

from probability import TotalProbabilityBranch, TotalProbabilityInput, evaluate_total_probability


def test_total_probability_balances_priors() -> None:
    branches = (
        TotalProbabilityBranch(label="C1", prior=0.5, likelihood=0.3),
        TotalProbabilityBranch(label="C2", prior=0.5, likelihood=0.6),
    )
    result = evaluate_total_probability(TotalProbabilityInput(branches=branches))
    assert math.isclose(result.total_probability, 0.45)


def test_total_probability_rejects_priors_not_summing_to_one() -> None:
    with pytest.raises(ValidationError):
        TotalProbabilityInput(
            branches=(
                TotalProbabilityBranch(label="A", prior=0.3, likelihood=0.5),
                TotalProbabilityBranch(label="B", prior=0.3, likelihood=0.5),
            )
        )


def test_total_probability_rejects_empty_branches() -> None:
    with pytest.raises(ValidationError):
        TotalProbabilityInput(branches=())
