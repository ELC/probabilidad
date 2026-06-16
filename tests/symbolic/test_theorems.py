import sympy as sp

from core import NormalParams
from symbolic import bayes_theorem, standardize_normal, total_probability_theorem


def test_bayes_theorem_returns_equality() -> None:
    statement = bayes_theorem()
    assert isinstance(statement.formula, sp.Equality)
    assert str(statement.posterior_symbol) == "P_A_given_B"


def test_total_probability_theorem_partition_size() -> None:
    statement = total_probability_theorem(partition_size=5)
    assert statement.partition_size == 5
    assert isinstance(statement.formula, sp.Equality)


def test_total_probability_theorem_default_partition() -> None:
    assert total_probability_theorem().partition_size == 3


def test_standardize_normal_formula_uses_parameters() -> None:
    statement = standardize_normal(NormalParams(mean=10.0, standard_deviation=2.0))
    formula_text = str(statement.formula)
    assert "X" in formula_text
    assert "Z" in formula_text
    assert str(statement.standard_variable) == "Z"
