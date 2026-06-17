import math
from typing import Any

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


class _NestedListModel(RichMarkdownModel):
    model_config = ConfigDict(frozen=True)

    members: tuple[_NestedModel, ...]


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


def test_format_value_renders_array_as_inline_list() -> None:
    rendered = format_value(np.array([0.65]))
    assert rendered == "0.65"
    rendered = format_value(np.array([1.0, 2.0, 3.0]))
    assert rendered == "1.00, 2.00, 3.00"


def test_format_value_truncates_long_arrays() -> None:
    rendered = format_value(np.arange(1.0, 13.0))
    assert rendered.startswith("1.00, 2.00")
    assert rendered.endswith(", ...")
    assert "8.00" in rendered
    assert "9.00" not in rendered


def test_format_value_flattens_two_dimensional_array() -> None:
    rendered = format_value(np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert rendered == "1.00, 2.00, 3.00, 4.00"


def test_format_value_handles_tuples_and_lists_inline() -> None:
    rendered = format_value((1.0, 2.0, 3.0))
    assert rendered == "1.00, 2.00, 3.00"
    assert format_value(()) == "(vacío)"


def test_format_value_handles_frozenset() -> None:
    rendered = format_value(frozenset({"a", "b"}))
    assert rendered.startswith("{")
    assert "a" in rendered
    assert "b" in rendered
    assert format_value(frozenset()) == "∅"


def test_format_value_handles_plain_basemodel() -> None:
    rendered = format_value(_PlainModel(value=3))
    assert rendered == "_PlainModel(...)"


def test_format_value_handles_unknown_object_uses_str() -> None:
    class _Custom:
        def __str__(self) -> str:
            return "custom-object"

    assert format_value(_Custom()) == "custom-object"


def test_format_value_handles_none() -> None:
    assert format_value(None) == "None"


class _OnlyChildrenModel(RichMarkdownModel):
    model_config = ConfigDict(frozen=True)

    location: _NestedModel
    dispersion: _NestedModel


def test_repr_html_renders_outer_table_with_scalar_fields() -> None:
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
    rendered = outer._repr_html_()  # pylint: disable=protected-access
    assert "<table" in rendered
    assert 'colspan="2"' in rendered
    assert "<thead>" in rendered
    assert "<tbody>" in rendered
    assert "float_field" in rendered
    assert "1.23" in rendered
    assert "Sí" in rendered
    assert "hijo" in rendered
    assert "None" in rendered


def test_repr_markdown_falls_back_to_html_table() -> None:
    nested = _NestedModel(name="hijo", value=2.5)
    markdown = nested._repr_markdown_()  # pylint: disable=protected-access
    assert markdown.startswith("<table")
    assert "hijo" in markdown


def test_repr_html_emits_sibling_tables_for_rich_fields() -> None:
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
    rendered = outer._repr_html_()  # pylint: disable=protected-access
    assert rendered.count("<table") == 2
    nested_index = rendered.find("hijo")
    outer_table_close = rendered.find("</table>")
    assert nested_index > outer_table_close


def test_repr_html_drops_outer_table_when_all_fields_are_rich() -> None:
    container = _OnlyChildrenModel(
        location=_NestedModel(name="centro", value=4.0),
        dispersion=_NestedModel(name="ancho", value=1.5),
    )
    rendered = container._repr_html_()  # pylint: disable=protected-access
    assert rendered.count("<table") == 2
    assert ">location<" in rendered
    assert ">dispersion<" in rendered
    assert "centro" in rendered
    assert "ancho" in rendered


def test_repr_html_indexes_rich_sequence_fields() -> None:
    container = _NestedListModel(
        members=(
            _NestedModel(name="a", value=1.0),
            _NestedModel(name="b", value=2.0),
        ),
    )
    rendered = container._repr_html_()  # pylint: disable=protected-access
    assert ">members[0]<" in rendered
    assert ">members[1]<" in rendered
    assert rendered.count("<table") == 2


def test_repr_html_renders_empty_rich_sequence_inline() -> None:
    container = _NestedListModel(members=())
    rendered = container._repr_html_()  # pylint: disable=protected-access
    assert "(vacío)" in rendered


def test_repr_html_renders_plain_sequence_value_as_list() -> None:
    class _PlainListModel(RichMarkdownModel):
        items: tuple[_PlainModel, ...]

    container = _PlainListModel(items=(_PlainModel(value=1), _PlainModel(value=2)))
    rendered = container._repr_html_()  # pylint: disable=protected-access
    assert "<ul" in rendered
    assert "<li>" in rendered
    assert "_PlainModel(...)" in rendered


def test_repr_html_renders_mixed_sequence_with_inline_rich_table() -> None:
    class _MixedModel(RichMarkdownModel):
        model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

        items: tuple[Any, ...]

    container = _MixedModel(items=(_NestedModel(name="x", value=1.0), 42))
    rendered = container._repr_html_()  # pylint: disable=protected-access
    assert "<ul" in rendered
    assert rendered.count("<table") == 2
    assert "<li>" in rendered


def test_repr_html_escapes_field_and_value_text() -> None:
    class _UnsafeModel(RichMarkdownModel):
        text: str

    rendered = _UnsafeModel(text="<script>alert(1)</script>")._repr_html_()  # pylint: disable=protected-access
    assert "&lt;script&gt;" in rendered
    assert "<script>alert(1)</script>" not in rendered


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (math.pi, "3.14"),
        ([1.0, 2.0], "1.00, 2.00"),
        ({"a": 1}, "{'a': 1}"),
    ],
)
def test_format_value_parametrized_substrings(value: object, expected: str) -> None:
    assert expected in format_value(value)
