from collections.abc import Iterator

import ipywidgets as widgets

from core import Settings
from widgets import (
    ContinuousDistributionExplorerInput,
    build_continuous_distribution_explorer,
)


def _walk_widgets(container: widgets.Widget) -> Iterator[widgets.Widget]:
    for child in getattr(container, "children", ()):
        yield child
        yield from _walk_widgets(child)


def test_continuous_explorer_returns_vbox(fixed_settings: Settings) -> None:
    container = build_continuous_distribution_explorer(ContinuousDistributionExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_continuous_explorer_switches_to_exponential(fixed_settings: Settings) -> None:
    container = build_continuous_distribution_explorer(ContinuousDistributionExplorerInput(settings=fixed_settings))
    dropdowns = [child for child in _walk_widgets(container) if isinstance(child, widgets.Dropdown)]
    assert dropdowns
    dropdowns[0].value = "Exponencial"


def test_continuous_explorer_responds_to_bound_slider(fixed_settings: Settings) -> None:
    container = build_continuous_distribution_explorer(ContinuousDistributionExplorerInput(settings=fixed_settings))
    sliders = [
        child
        for child in _walk_widgets(container)
        if isinstance(child, widgets.FloatSlider) and child.description == "x_max"
    ]
    sliders[0].value += 0.5
