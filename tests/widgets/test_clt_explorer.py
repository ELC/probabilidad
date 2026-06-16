import ipywidgets as widgets

from core import Settings
from widgets import CLTExplorerInput, build_clt_explorer


def test_build_clt_explorer(fixed_settings: Settings) -> None:
    container = build_clt_explorer(CLTExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_clt_explorer_switches_to_uniform(fixed_settings: Settings) -> None:
    container = build_clt_explorer(CLTExplorerInput(settings=fixed_settings))
    dropdowns = [child for child in container.children if isinstance(child, widgets.Dropdown)]
    dropdowns[0].value = "Uniforme(0, 1)"
