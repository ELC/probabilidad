import math

import pytest
from pydantic import ValidationError

from core import Settings
from widgets import BayesAnywidget, BayesAnywidgetInput, build_bayes_anywidget


def test_build_bayes_anywidget_returns_anywidget_instance(fixed_settings: Settings) -> None:
    widget = build_bayes_anywidget(BayesAnywidgetInput(settings=fixed_settings))
    assert isinstance(widget, BayesAnywidget)


def test_bayes_anywidget_carries_initial_traits(fixed_settings: Settings) -> None:
    widget = build_bayes_anywidget(
        BayesAnywidgetInput(
            settings=fixed_settings,
            initial_prevalence=0.02,
            initial_sensitivity=0.97,
            initial_specificity=0.90,
        )
    )
    assert math.isclose(widget.prevalence, 0.02)
    assert math.isclose(widget.sensitivity, 0.97)
    assert math.isclose(widget.specificity, 0.90)


def test_bayes_anywidget_bundles_esm_and_css(fixed_settings: Settings) -> None:
    widget = build_bayes_anywidget(BayesAnywidgetInput(settings=fixed_settings))
    assert "export default" in widget._esm  # noqa: SLF001  # pylint: disable=protected-access
    assert "bayes-anywidget" in widget._css  # noqa: SLF001  # pylint: disable=protected-access


def test_bayes_anywidget_input_rejects_invalid_floats() -> None:
    with pytest.raises(ValidationError):
        BayesAnywidgetInput(initial_prevalence="not-a-float")  # type: ignore[arg-type]
