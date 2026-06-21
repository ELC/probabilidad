# pyright: reportMissingTypeStubs=false, reportPrivateUsage=false, reportUnknownMemberType=false, reportUnknownVariableType=false

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
from widgets.summary_evolution import (
    _MEAN,
    _fixed_evolution_domain,
    _summary_chart,
)


def _observations() -> DataFrame[Observations]:
    return pd.DataFrame({"value": [2.0, 3.0, 4.0, 5.0, 6.0]}).pipe(DataFrame[Observations])


def _button(container: widgets.Widget, description: str) -> widgets.Button:
    assert isinstance(container, widgets.VBox)
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
    assert _button(container, "Reiniciar") is not None


def test_summary_evolution_add_value_button_rerenders(fixed_settings: Settings) -> None:
    container = build_mean_evolution_explorer(
        SummaryEvolutionExplorerInput(observations=_observations(), settings=fixed_settings)
    )
    add_button = _button(container, "Agregar valor")

    add_button.click()

    assert isinstance(container, widgets.VBox)


def test_summary_evolution_reset_button_rerenders(fixed_settings: Settings) -> None:
    container = build_mean_evolution_explorer(
        SummaryEvolutionExplorerInput(observations=_observations(), settings=fixed_settings)
    )
    _button(container, "Agregar valor").click()
    _button(container, "Reiniciar").click()

    assert isinstance(container, widgets.VBox)


def test_summary_evolution_rejects_empty_observations(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": []}).pipe(DataFrame[Observations])
    with pytest.raises(ValueError, match="observations"):
        SummaryEvolutionExplorerInput(observations=observations, settings=fixed_settings)


def test_summary_evolution_uses_fixed_evolution_y_domain(fixed_settings: Settings) -> None:
    observations = _observations()
    input_data = SummaryEvolutionExplorerInput(
        observations=observations,
        settings=fixed_settings,
        manual_value=20.0,
    )
    evolution_domain = _fixed_evolution_domain(input_data, (_MEAN,))
    mean_after_extreme = pd.Series([2.0, 3.0, 4.0, 5.0, 6.0, 20.0]).mean()

    assert evolution_domain[1] >= mean_after_extreme
    assert evolution_domain == _fixed_evolution_domain(input_data, (_MEAN,))


def test_summary_chart_uses_container_width_and_dynamic_x_domain(fixed_settings: Settings) -> None:
    observations = _observations()
    values = observations["value"].to_numpy(dtype=float)
    input_data = SummaryEvolutionExplorerInput(observations=observations, settings=fixed_settings, manual_value=20.0)
    chart = _summary_chart(
        values,
        (_MEAN,),
        "Evolución de la media",
        fixed_settings,
        _fixed_evolution_domain(input_data, (_MEAN,)),
    )

    chart_spec = chart.to_dict()
    assert chart_spec["vconcat"][0]["width"] == "container"
    assert chart_spec["vconcat"][1]["width"] == "container"
    assert "scale" not in chart_spec["vconcat"][0]["encoding"]["x"]
    assert "scale" not in chart_spec["vconcat"][1]["encoding"]["x"]
