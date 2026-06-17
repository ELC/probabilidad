import html
import math
from collections.abc import Callable
from typing import Any

import numpy as np
from pydantic import BaseModel

DISPLAY_NAMES: dict[str, str] = {
    "DescriptiveStatistics": "Resumen descriptivo",
    "LocationStatistics": "Posición",
    "DispersionStatistics": "Dispersión",
    "OutlierReport": "Reporte de outliers",
    "StandardizedObservations": "Observaciones estandarizadas",
    "JointEventProbabilities": "Probabilidades conjuntas",
    "SetOperationResult": "Operaciones de conjuntos",
    "ConditionalProbability": "Probabilidad condicional",
    "BayesPosterior": "Posterior de Bayes",
    "TotalProbabilityResult": "Probabilidad total",
    "TotalProbabilityBranch": "Rama (prior y verosimilitud)",
    "ProbabilityMassTable": "Tabla de masa de probabilidad",
    "DensityGrid": "Grilla de densidad",
    "TailProbabilityResult": "Probabilidad de cola",
    "QuantileResult": "Cuantil",
    "SurvivalResult": "Supervivencia",
    "DistributionMoments": "Momentos numéricos",
    "MeanConfidenceInterval": "IC para la media",
    "ProportionConfidenceInterval": "IC para una proporción",
    "VarianceConfidenceInterval": "IC para la varianza",
    "OneSampleMeanTestResult": "Test de una media",
    "OneSampleProportionTestResult": "Test de una proporción",
    "BootstrapMeanResult": "Bootstrap de la media",
    "SampleSizeResult": "Tamaño muestral requerido",
    "CLTSimulationResult": "Simulación TCL",
    "LLNSimulationResult": "Simulación LLN",
    "GaltonBoardResult": "Tablero de Galton",
    "MonteCarloResult": "Muestra Monte Carlo",
    "VerificationResult": "Resultado de verificación",
    "SymbolicMoments": "Momentos simbólicos",
    "BayesStatement": "Teorema de Bayes",
    "TotalProbabilityStatement": "Probabilidad total",
    "StandardizationStatement": "Estandarización",
}

_TABLE_STYLE = (
    "border-collapse: collapse; margin: 0.25em 0;"
    " font-family: var(--jp-content-font-family, sans-serif); font-size: 0.95em;"
)
_HEADER_STYLE = (
    "padding: 0.25em 0.6em; text-align: left;"
    " background: rgba(120, 120, 120, 0.12); border-bottom: 1px solid rgba(120, 120, 120, 0.4);"
)
_CELL_STYLE = "padding: 0.2em 0.6em; border-bottom: 1px solid rgba(120, 120, 120, 0.2); vertical-align: top;"
_FIELD_STYLE = _CELL_STYLE + " font-family: var(--jp-code-font-family, monospace); white-space: nowrap;"


def display_name_for(model_class: type) -> str:
    return DISPLAY_NAMES.get(model_class.__name__, model_class.__name__)


def _format_float(value: float) -> str:
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "∞" if value > 0 else "-∞"
    return f"{value:.2f}"


def _format_array(value: np.ndarray) -> str:
    size = int(value.size)
    if size == 0:
        return "(vacío)"
    head_count = min(4, size)
    flat = value.flatten()
    head = ", ".join(_format_float(float(x)) for x in flat[:head_count])
    suffix = ", ..." if size > head_count else ""
    shape = "×".join(str(dim) for dim in value.shape)
    return f"array[{shape}] [{head}{suffix}]"


def _format_basemodel(value: BaseModel) -> str:
    return f"{type(value).__name__}(...)"


def _format_bool(value: bool) -> str:  # noqa: FBT001
    return "Sí" if value else "No"


def _format_sequence_text(value: tuple[Any, ...] | list[Any]) -> str:
    if not value:
        return "(vacío)"
    return ", ".join(format_value(item) for item in value)


def _format_set_text(value: frozenset[Any] | set[Any]) -> str:
    if not value:
        return "∅"
    items = sorted(value, key=str)
    return "{" + ", ".join(format_value(item) for item in items) + "}"


class RichMarkdownModel(BaseModel):
    def _repr_html_(self) -> str:  # noqa: PLW3201 — IPython display hook
        return _model_to_html(self)

    def _repr_markdown_(self) -> str:  # noqa: PLW3201 — IPython display hook
        return _model_to_html(self)


def _model_to_html(model: RichMarkdownModel) -> str:
    title = html.escape(display_name_for(type(model)))
    rows: list[str] = []
    # pylint: disable-next=not-an-iterable
    field_names = list(type(model).model_fields)
    for field_name in field_names:
        cell_html = _value_to_html(getattr(model, field_name))
        rows.append(
            f'<tr><th style="{_FIELD_STYLE}">{html.escape(field_name)}</th>'
            f'<td style="{_CELL_STYLE}">{cell_html}</td></tr>',
        )
    body = "".join(rows)
    return (
        f'<table style="{_TABLE_STYLE}">'
        f'<thead><tr><th colspan="2" style="{_HEADER_STYLE}">{title}</th></tr></thead>'
        f"<tbody>{body}</tbody>"
        f"</table>"
    )


def _sequence_to_html(value: tuple[Any, ...] | list[Any]) -> str:
    if not value:
        return "(vacío)"
    items = "".join(f"<li>{_value_to_html(item)}</li>" for item in value)
    return f'<ul style="margin: 0; padding-left: 1.1em;">{items}</ul>'


def _value_to_html(value: Any) -> str:
    if isinstance(value, RichMarkdownModel):
        return _model_to_html(value)
    if isinstance(value, tuple | list):
        return _sequence_to_html(value)
    return html.escape(format_value(value))


_Predicate = type | tuple[type, ...]
_Formatter = Callable[[Any], str]
_DISPATCH: tuple[tuple[_Predicate, _Formatter], ...] = (
    (BaseModel, _format_basemodel),
    (bool, _format_bool),
    (np.integer, lambda value: str(int(value))),
    (np.floating, lambda value: _format_float(float(value))),
    (int, str),
    (float, _format_float),
    (np.ndarray, _format_array),
    ((tuple, list), _format_sequence_text),
    ((frozenset, set), _format_set_text),
    (str, lambda value: value),
)


def format_value(value: Any) -> str:
    for value_type, formatter in _DISPATCH:
        if isinstance(value, value_type):
            return formatter(value)
    return str(value)
