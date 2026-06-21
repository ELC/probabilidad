from collections.abc import Callable

import ipywidgets as widgets
import pandas as pd
import pytest
from pandera.typing import DataFrame

from core import Observations, Settings
from widgets import (
    SummaryEvolutionExplorerInput,
    build_iqr_evolution_explorer,
    build_location_evolution_explorer,
    build_mean_evolution_explorer,
    build_median_evolution_explorer,
    build_mode_evolution_explorer,
    build_range_evolution_explorer,
    build_standard_deviation_evolution_explorer,
)


def _observations() -> DataFrame[Observations]:
    return pd.DataFrame({"value": [2.0, 3.0, 4.0, 5.0, 6.0]}).pipe(DataFrame[Observations])


def _button(container: widgets.VBox, description: str) -> widgets.Button:
    controls = container.children[0]
    assert isinstance(controls, widgets.HBox)
    for child in controls.children:
        if isinstance(child, widgets.Button) and child.description == description:
            return child
    raise LookupError(description)


@pytest.mark.parametrize(
    "builder",
    [
        build_mean_evolution_explorer,
        build_mode_evolution_explorer,
        build_median_evolution_explorer,
        build_location_evolution_explorer,
        build_standard_deviation_evolution_explorer,
        build_range_evolution_explorer,
        build_iqr_evolution_explorer,
    ],
)
def test_summary_evolution_builders_return_vbox(
    builder: Callable[[SummaryEvolutionExplorerInput], widgets.Widget],
    fixed_settings: Settings,
) -> None:
    container = builder(SummaryEvolutionExplorerInput(observations=_observations(), settings=fixed_settings))

    assert isinstance(container, widgets.VBox)
    assert isinstance(container.children[0], widgets.HBox)
    assert isinstance(container.children[1], widgets.Output)
    assert container.layout.width == "100%"
    assert container.children[0].layout.width == "100%"
    assert container.children[1].layout.width == "100%"


def test_summary_evolution_add_value_button_rerenders(fixed_settings: Settings) -> None:
    container = build_mean_evolution_explorer(
        SummaryEvolutionExplorerInput(observations=_observations(), settings=fixed_settings)
    )
    add_button = _button(container, "Agregar valor")

    add_button.click()

    assert isinstance(container, widgets.VBox)


def test_summary_evolution_rejects_empty_observations(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": []}).pipe(DataFrame[Observations])
    with pytest.raises(ValueError, match="observations"):
        SummaryEvolutionExplorerInput(observations=observations, settings=fixed_settings)
