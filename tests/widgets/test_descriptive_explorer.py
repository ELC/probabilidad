import ipywidgets as widgets
import pandas as pd
import pytest
from pandera.typing import DataFrame

from core import Observations, Settings
from descriptive import FrequencyTableInput, build_frequency_table
from widgets import (
    DescriptiveExplorerInput,
    IntervalWidthExplorerInput,
    build_descriptive_explorer,
    build_interval_width_explorer,
)
from widgets.descriptive_explorer import _fixed_domains, _slider_widths


def _find_slider(container: widgets.Widget, description_prefix: str) -> widgets.Widget:
    for child in container.children:
        if getattr(child, "description", "").startswith(description_prefix):
            return child
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


def test_interval_width_explorer_yields_vbox_with_stacked_outputs(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": [2.0, 2.5, 3.0, 4.0, 4.5, 5.0]}).pipe(DataFrame[Observations])
    container = build_interval_width_explorer(
        IntervalWidthExplorerInput(observations=observations, settings=fixed_settings)
    )
    assert isinstance(container, widgets.VBox)
    slider, first_output, second_output = tuple(container.children)
    assert isinstance(slider, widgets.FloatSlider)
    assert isinstance(first_output, widgets.Output)
    assert isinstance(second_output, widgets.Output)
    assert container.layout.width == "100%"
    assert first_output.layout.width == "100%"
    assert second_output.layout.width == "100%"


def test_interval_width_explorer_reacts_to_slider_change(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": [2.0, 2.5, 3.0, 4.0, 4.5, 5.0]}).pipe(DataFrame[Observations])
    container = build_interval_width_explorer(
        IntervalWidthExplorerInput(observations=observations, settings=fixed_settings)
    )
    width_slider = _find_slider(container, "ancho")
    width_slider.value += 0.25


def test_interval_width_explorer_rejects_invalid_initial_width(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": [2.0, 2.5, 3.0]}).pipe(DataFrame[Observations])
    with pytest.raises(ValueError, match="initial_width"):
        IntervalWidthExplorerInput(
            observations=observations,
            settings=fixed_settings,
            initial_width=4.0,
            maximum_width=3.0,
        )


def test_interval_width_explorer_fixed_domains_cover_all_slider_widths(fixed_settings: Settings) -> None:
    observations = pd.DataFrame({"value": [2.0, 2.5, 3.0, 4.0, 4.5, 5.0]}).pipe(DataFrame[Observations])
    input_data = IntervalWidthExplorerInput(observations=observations, settings=fixed_settings)
    x_domain, _ = _fixed_domains(input_data)

    for width in _slider_widths(input_data):
        table = build_frequency_table(
            FrequencyTableInput(observations=observations, bin_width=width)
        )
        assert float(table["interval_start"].min()) >= x_domain[0]
        assert float(table["interval_end"].max()) <= x_domain[1]
