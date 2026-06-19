from collections.abc import Iterator

import ipywidgets as widgets

from core import Settings
from widgets import PivotInversionExplorerInput, build_pivot_inversion_explorer
from widgets.pivot_inversion_explorer import PivotCase, _bounds_for_case


def _walk_widgets(container: widgets.Widget) -> Iterator[widgets.Widget]:
    for child in getattr(container, "children", ()):
        yield child
        yield from _walk_widgets(child)


def _find_dropdown(container: widgets.Widget) -> widgets.Dropdown:
    for child in _walk_widgets(container):
        if isinstance(child, widgets.Dropdown):
            return child
    msg = "Dropdown not found"
    raise AssertionError(msg)


def _find_slider(container: widgets.Widget, description: str) -> widgets.Widget:
    for child in _walk_widgets(container):
        if isinstance(child, widgets.FloatSlider | widgets.IntSlider) and child.description == description:
            return child
    msg = f"Slider {description!r} not found"
    raise AssertionError(msg)


def test_pivot_inversion_explorer_returns_vbox(fixed_settings: Settings) -> None:
    container = build_pivot_inversion_explorer(PivotInversionExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_pivot_inversion_explorer_switches_to_student_t(fixed_settings: Settings) -> None:
    container = build_pivot_inversion_explorer(PivotInversionExplorerInput(settings=fixed_settings))
    dropdown = _find_dropdown(container)
    dropdown.value = PivotCase.STUDENT_T.value


def test_pivot_inversion_explorer_switches_to_chi_squared(fixed_settings: Settings) -> None:
    container = build_pivot_inversion_explorer(PivotInversionExplorerInput(settings=fixed_settings))
    dropdown = _find_dropdown(container)
    dropdown.value = PivotCase.CHI_SQUARED.value


def test_pivot_inversion_explorer_responds_to_sample_size(fixed_settings: Settings) -> None:
    container = build_pivot_inversion_explorer(PivotInversionExplorerInput(settings=fixed_settings))
    sample_slider = _find_slider(container, "n")
    sample_slider.value = 60


def test_pivot_inversion_widens_with_confidence_for_normal(fixed_settings: Settings) -> None:
    input_data = PivotInversionExplorerInput(settings=fixed_settings)
    narrow_lower, narrow_upper, _, _ = _bounds_for_case(PivotCase.NORMAL, input_data, 36, 0.80)
    wide_lower, wide_upper, _, _ = _bounds_for_case(PivotCase.NORMAL, input_data, 36, 0.99)
    assert (wide_upper - wide_lower) > (narrow_upper - narrow_lower)


def test_pivot_inversion_widens_with_confidence_for_student_t(fixed_settings: Settings) -> None:
    input_data = PivotInversionExplorerInput(settings=fixed_settings)
    narrow_lower, narrow_upper, _, _ = _bounds_for_case(PivotCase.STUDENT_T, input_data, 36, 0.80)
    wide_lower, wide_upper, _, _ = _bounds_for_case(PivotCase.STUDENT_T, input_data, 36, 0.99)
    assert (wide_upper - wide_lower) > (narrow_upper - narrow_lower)


def test_pivot_inversion_chi_squared_interval_is_asymmetric(fixed_settings: Settings) -> None:
    input_data = PivotInversionExplorerInput(settings=fixed_settings)
    lower, upper, point_estimate, parameter_label = _bounds_for_case(PivotCase.CHI_SQUARED, input_data, 36, 0.95)
    assert parameter_label == "σ²"
    assert lower < point_estimate < upper
    assert (upper - point_estimate) > (point_estimate - lower)
