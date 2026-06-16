import math

import pytest
from pydantic import ValidationError

from probability import ConditionalInput, evaluate_conditional_probability


def test_conditional_probability_known_value() -> None:
    result = evaluate_conditional_probability(
        ConditionalInput(probability_intersection=0.2, probability_conditioning_event=0.5)
    )
    assert math.isclose(result.probability, 0.4)


def test_conditional_rejects_intersection_larger_than_conditioning() -> None:
    with pytest.raises(ValidationError):
        ConditionalInput(probability_intersection=0.5, probability_conditioning_event=0.3)
