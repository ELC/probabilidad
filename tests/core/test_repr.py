import math

import numpy as np
import pytest
from pydantic import BaseModel, ConfigDict

from core import RichMarkdownModel
from core.repr import DISPLAY_NAMES, display_name_for, format_value


class _NestedModel(RichMarkdownModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str
    value: float


class _OuterModel(RichMarkdownModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    integer_field: int
    float_field: float
    boolean_field: bool
    string_field: str
    nested_field: _NestedModel
    array_field: np.ndarray
    tuple_field: tuple[float, ...]
    set_field: frozenset[str]
    optional_field: float | None


class _PlainModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: int


def test_display_name_for_known_class_returns_spanish_name() -> None:
    name = next(iter(DISPLAY_NAMES))
    expected = DISPLAY_NAMES[name]

    class _Stub:
        pass

    _Stub.__name__ = name
    assert display_name_for(_Stub) == expected


def test_display_name_for_unknown_class_returns_class_name() -> None:
    class _Unknown:
        pass

    assert display_name_for(_Unknown) == "_Unknown"


def test_format_value_rounds_floats_to_two_decimals() -> None:
    assert format_value(math.pi) == "3.14"
    assert format_value(2.5) == "2.50"
    assert format_value(-1.234) == "-1.23"


def test_format_value_handles_special_floats() -> None:
    assert format_value(float("nan")) == "NaN"
    assert format_value(float("inf")) == "∞"
    assert format_value(float("-inf")) == "-∞"


def test_format_value_handles_booleans() -> None:
    assert format_value(value=True) == "Sí"
    assert format_value(value=False) == "No"


def test_format_value_handles_integers_and_strings() -> None:
    assert format_value(42) == "42"
    assert format_value(np.int64(7)) == "7"
    assert format_value("texto") == "texto"


def test_format_value_handles_numpy_floats() -> None:
    assert format_value(np.float64(1.234)) == "1.23"


def test_format_value_handles_empty_array() -> None:
    assert format_value(np.array([])) == "(vacío)"


def test_format_value_truncates_long_arrays() -> None:
    rendered = format_value(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
    assert "..." in rendered
    assert "1.00" in rendered
    assert "4.00" in rendered


def test_format_value_renders_two_dimensional_array() -> None:
    rendered = format_value(np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert "2×2" in rendered


def test_format_value_handles_tuples_and_lists() -> None:
    rendered = format_value((1.0, 2.0, 3.0))
    assert "- 1.00" in rendered
    assert "- 3.00" in rendered
    assert format_value(()) == "(vacío)"


def test_format_value_handles_frozenset() -> None:
    rendered = format_value(frozenset({"a", "b"}))
    assert rendered.startswith("{")
    assert "a" in rendered
    assert "b" in rendered
    assert format_value(frozenset()) == "∅"


def test_format_value_handles_plain_basemodel() -> None:
    rendered = format_value(_PlainModel(value=3))
    assert rendered.startswith("`_PlainModel")


def test_format_value_handles_nested_rich_model() -> None:
    nested = _NestedModel(name="hijo", value=2.5)
    rendered = format_value(nested)
    assert "**" in rendered
    assert "name: hijo" in rendered
    assert "value: 2.50" in rendered


def test_format_value_handles_unknown_object_uses_str() -> None:
    class _Custom:
        def __str__(self) -> str:
            return "custom-object"

    assert format_value(_Custom()) == "custom-object"


def test_format_value_handles_none() -> None:
    assert format_value(None) == "None"


def test_repr_markdown_renders_table_for_outer_model() -> None:
    outer = _OuterModel(
        integer_field=3,
        float_field=1.234,
        boolean_field=True,
        string_field="hola",
        nested_field=_NestedModel(name="hijo", value=2.5),
        array_field=np.array([1.0, 2.0]),
        tuple_field=(0.5, 0.75),
        set_field=frozenset({"x"}),
        optional_field=None,
    )
    markdown = outer._repr_markdown_()  # pylint: disable=protected-access
    assert markdown.startswith("**")
    assert "| Campo | Valor |" in markdown
    assert "`float_field`" in markdown
    assert "1.23" in markdown
    assert "Sí" in markdown
    assert "name: hijo" in markdown
    assert "None" in markdown


@pytest.mark.parametrize(
    ("value", "expected_substring"),
    [
        (math.pi, "3.14"),
        ([1.0, 2.0], "- 1.00"),
        ({"a": 1}, "{'a': 1}"),
    ],
)
def test_format_value_parametrized_substrings(value: object, expected_substring: str) -> None:
    assert expected_substring in format_value(value)
