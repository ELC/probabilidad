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
    "border-collapse: collapse; margin: 0; font-family: var(--jp-content-font-family, sans-serif); font-size: 0.95em;"
)
_HEADER_STYLE = (
    "padding: 0.25em 0.6em; text-align: left;"
    " background: rgba(120, 120, 120, 0.12); border-bottom: 1px solid rgba(120, 120, 120, 0.4);"
)
_CELL_STYLE = "padding: 0.2em 0.6em; border-bottom: 1px solid rgba(120, 120, 120, 0.2); vertical-align: top;"
_FIELD_STYLE = _CELL_STYLE + " font-family: var(--jp-code-font-family, monospace); white-space: nowrap;"
_GROUP_STYLE = "display: flex; flex-direction: column; gap: 0.6em; align-items: flex-start;"
_LABEL_STYLE = (
    "font-family: var(--jp-code-font-family, monospace); font-size: 0.85em; color: rgba(120, 120, 120, 0.95);"
)
_OUTER_TITLE_STYLE = "font-weight: 600; font-size: 1em; padding: 0.1em 0; color: var(--jp-ui-font-color1, inherit);"


def display_name_for(model_class: type) -> str:
    return DISPLAY_NAMES.get(model_class.__name__, model_class.__name__)


def _format_float(value: float) -> str:
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "∞" if value > 0 else "-∞"
    return f"{value:.2f}"


_MAX_INLINE_ITEMS = 8


def _format_basemodel(value: BaseModel) -> str:
    return f"{type(value).__name__}(...)"


def _format_bool(value: bool) -> str:  # noqa: FBT001
    return "Sí" if value else "No"


def _format_sequence_text(value: tuple[Any, ...] | list[Any]) -> str:
    if not value:
        return "(vacío)"
    head = value[:_MAX_INLINE_ITEMS]
    suffix = ", ..." if len(value) > _MAX_INLINE_ITEMS else ""
    return ", ".join(format_value(item) for item in head) + suffix


def _format_array(value: np.ndarray) -> str:
    return _format_sequence_text(value.flatten().tolist())


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


def _is_rich(value: Any) -> bool:
    return isinstance(value, RichMarkdownModel)


def _is_rich_sequence(value: Any) -> bool:
    return isinstance(value, tuple | list) and len(value) > 0 and all(_is_rich(item) for item in value)


def _scalar_table_html(title: str, rows_html: str) -> str:
    return (
        f'<table style="{_TABLE_STYLE}">'
        f'<thead><tr><th colspan="2" style="{_HEADER_STYLE}">{title}</th></tr></thead>'
        f"<tbody>{rows_html}</tbody>"
        f"</table>"
    )


def _labelled(label: str | None, body_html: str) -> str:
    if label is None:
        return body_html
    label_html = f'<div style="{_LABEL_STYLE}">{html.escape(label)}</div>'
    return f"<div>{label_html}{body_html}</div>"


def _model_to_html(model: RichMarkdownModel, label: str | None = None) -> str:
    title = html.escape(display_name_for(type(model)))
    # pylint: disable-next=not-an-iterable
    field_names = list(type(model).model_fields)
    scalar_fields: list[tuple[str, Any]] = []
    rich_fields: list[tuple[str, Any]] = []
    for name in field_names:
        value = getattr(model, name)
        if _is_rich(value) or _is_rich_sequence(value):
            rich_fields.append((name, value))
        else:
            scalar_fields.append((name, value))

    blocks: list[str] = []
    if scalar_fields or not rich_fields:
        blocks.append(_scalar_table_html(title, _scalar_rows_html(scalar_fields)))
    else:
        blocks.append(f'<div style="{_OUTER_TITLE_STYLE}">{title}</div>')

    for name, value in rich_fields:
        blocks.extend(_rich_field_blocks(name, value))

    body = "".join(blocks)
    inner = body if len(blocks) <= 1 else f'<div style="{_GROUP_STYLE}">{body}</div>'
    return _labelled(label, inner)


def _scalar_rows_html(scalar_fields: list[tuple[str, Any]]) -> str:
    return "".join(
        f'<tr><th style="{_FIELD_STYLE}">{html.escape(name)}</th>'
        f'<td style="{_CELL_STYLE}">{_value_to_html(value)}</td></tr>'
        for name, value in scalar_fields
    )


def _rich_field_blocks(name: str, value: Any) -> list[str]:
    if _is_rich(value):
        return [_model_to_html(value, label=name)]
    return [_model_to_html(item, label=f"{name}[{index}]") for index, item in enumerate(value)]


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
