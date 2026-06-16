from collections.abc import Iterator

import ipywidgets as widgets

from core import Settings
from widgets import MeanCIExplorerInput, build_mean_ci_explorer


def _walk_widgets(container: widgets.Widget) -> Iterator[widgets.Widget]:
    for child in getattr(container, "children", ()):
        yield child
        yield from _walk_widgets(child)


def test_build_mean_ci_explorer(fixed_settings: Settings) -> None:
    container = build_mean_ci_explorer(MeanCIExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_mean_ci_explorer_reacts_to_replicates_slider(fixed_settings: Settings) -> None:
    container = build_mean_ci_explorer(MeanCIExplorerInput(settings=fixed_settings))
    sliders = [
        child
        for child in _walk_widgets(container)
        if isinstance(child, widgets.IntSlider) and child.description == "réplicas"
    ]
    sliders[0].value = 15
