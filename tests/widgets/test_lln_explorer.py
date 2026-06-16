import ipywidgets as widgets

from core import Settings
from widgets import LLNExplorerInput, build_lln_explorer


def test_build_lln_explorer(fixed_settings: Settings) -> None:
    container = build_lln_explorer(LLNExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_lln_explorer_reacts_to_slider(fixed_settings: Settings) -> None:
    container = build_lln_explorer(LLNExplorerInput(settings=fixed_settings))
    horizon_sliders = [
        child
        for child in container.children
        if isinstance(child, widgets.IntSlider) and child.description == "horizonte"
    ]
    horizon_sliders[0].value = 500
