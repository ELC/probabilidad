import ipywidgets as widgets

from core import Settings
from widgets import BayesExplorerInput, build_bayes_explorer


def test_build_bayes_explorer(fixed_settings: Settings) -> None:
    container = build_bayes_explorer(BayesExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_bayes_explorer_reacts_to_slider(fixed_settings: Settings) -> None:
    container = build_bayes_explorer(BayesExplorerInput(settings=fixed_settings))
    sliders = [child for child in container.children if isinstance(child, widgets.FloatSlider)]
    sliders[0].value = 0.05
