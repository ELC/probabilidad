import ipywidgets as widgets

from core import Settings
from widgets import DescriptiveExplorerInput, build_descriptive_explorer


def _find_slider(container: widgets.Widget, description_prefix: str) -> widgets.Widget:
    for child in container.children:
        if isinstance(child, (widgets.HBox, widgets.VBox)):
            for grandchild in child.children:
                if getattr(grandchild, "description", "").startswith(description_prefix):
                    return grandchild
    raise LookupError(description_prefix)


def test_build_descriptive_explorer_yields_vbox(fixed_settings: Settings) -> None:
    container = build_descriptive_explorer(DescriptiveExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_descriptive_explorer_reacts_to_slider_change(fixed_settings: Settings) -> None:
    container = build_descriptive_explorer(DescriptiveExplorerInput(settings=fixed_settings))
    mean_slider = _find_slider(container, "μ")
    mean_slider.value += 1.0
