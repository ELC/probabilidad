from collections.abc import Iterator

import ipywidgets as widgets

from core import Settings
from widgets import (
    DiscreteDistributionExplorerInput,
    build_discrete_distribution_explorer,
)


def _walk_widgets(container: widgets.Widget) -> Iterator[widgets.Widget]:
    for child in getattr(container, "children", ()):
        yield child
        yield from _walk_widgets(child)


def test_discrete_explorer_returns_vbox(fixed_settings: Settings) -> None:
    container = build_discrete_distribution_explorer(DiscreteDistributionExplorerInput(settings=fixed_settings))
    assert isinstance(container, widgets.VBox)


def test_discrete_explorer_switches_to_poisson(fixed_settings: Settings) -> None:
    container = build_discrete_distribution_explorer(DiscreteDistributionExplorerInput(settings=fixed_settings))
    dropdowns = [child for child in _walk_widgets(container) if isinstance(child, widgets.Dropdown)]
    dropdowns[0].value = "Poisson"
