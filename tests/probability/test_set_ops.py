import math

import pytest
from pydantic import ValidationError

from probability import (
    JointEventInput,
    SetOperationInput,
    evaluate_set_operations,
    joint_event_probabilities,
)


def test_joint_event_probabilities_additive_rule() -> None:
    result = joint_event_probabilities(
        JointEventInput(probability_a=0.6, probability_b=0.5, probability_intersection=0.2)
    )
    assert math.isclose(result.union, 0.9)
    assert math.isclose(result.only_a, 0.4)
    assert math.isclose(result.only_b, 0.3)
    assert math.isclose(result.neither, 0.1)


def test_joint_event_rejects_invalid_intersection() -> None:
    with pytest.raises(ValidationError):
        JointEventInput(probability_a=0.3, probability_b=0.4, probability_intersection=0.5)


def test_evaluate_set_operations_returns_expected_sets() -> None:
    universe = frozenset({"1", "2", "3", "4"})
    event_a = frozenset({"1", "2"})
    event_b = frozenset({"2", "3"})
    result = evaluate_set_operations(SetOperationInput(universe=universe, event_a=event_a, event_b=event_b))
    assert result.union == {"1", "2", "3"}
    assert result.intersection == {"2"}
    assert result.complement_a == {"3", "4"}
    assert result.only_a == {"1"}
    assert result.only_b == {"3"}
    assert result.symmetric_difference == {"1", "3"}


def test_evaluate_set_operations_rejects_non_subset_a() -> None:
    with pytest.raises(ValidationError):
        SetOperationInput(
            universe=frozenset({"a"}),
            event_a=frozenset({"a", "b"}),
            event_b=frozenset({"a"}),
        )


def test_evaluate_set_operations_rejects_non_subset_b() -> None:
    with pytest.raises(ValidationError):
        SetOperationInput(
            universe=frozenset({"a"}),
            event_a=frozenset({"a"}),
            event_b=frozenset({"a", "b"}),
        )
