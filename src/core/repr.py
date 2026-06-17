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

FIELD_LABELS: dict[str, str] = {
    "alternative": "Hipótesis alternativa",
    "bin_counts": "Frecuencias por casilla",
    "bin_positions": "Posiciones de casillas",
    "bootstrap_means": "Medias bootstrap",
    "coefficient_of_variation": "Coeficiente de variación",
    "complement_a": "Complemento de A",
    "complement_b": "Complemento de B",
    "confidence_level": "Nivel de confianza",
    "critical_value": "Valor crítico",
    "cumulative": "Acumulada",
    "degrees_of_freedom": "Grados de libertad",
    "density": "Densidad",
    "dispersion": "Dispersión",
    "distribution_name": "Distribución",
    "excess_kurtosis": "Curtosis (exceso)",
    "expectation": "Esperanza",
    "first_quartile": "Primer cuartil",
    "grid": "Grilla",
    "interquartile_range": "Rango intercuartil",
    "intersection": "Intersección",
    "joint_probabilities": "Probabilidades conjuntas",
    "joint_probability": "Probabilidad conjunta",
    "label": "Etiqueta",
    "likelihood": "Verosimilitud",
    "location": "Posición",
    "lower_bound": "Cota inferior",
    "lower_critical_value": "Valor crítico inferior",
    "lower_fence": "Cota inferior",
    "lower_quantile": "Cuantil inferior",
    "margin_of_error": "Margen de error",
    "maximum": "Máximo",
    "mean": "Media",
    "median": "Mediana",
    "message": "Mensaje",
    "minimum": "Mínimo",
    "name": "Nombre",
    "neither": "Ninguno",
    "normal_approximation_mean": "Media de la aproximación normal",
    "normal_approximation_standard_deviation": "Desvío de la aproximación normal",
    "only_a": "Solo A",
    "only_b": "Solo B",
    "outlier_count": "Cantidad de outliers",
    "outlier_values": "Valores atípicos",
    "outliers": "Outliers",
    "p_value": "Valor p",
    "passed": "Verificación",
    "point_estimate": "Estimador puntual",
    "posterior": "Posterior",
    "prior": "Prior",
    "probability": "Probabilidad",
    "quantile": "Cuantil",
    "range_width": "Rango",
    "reject_null": "Rechaza H₀",
    "required_sample_size": "Tamaño de muestra requerido",
    "running_mean": "Media acumulada",
    "sample_mean": "Media muestral",
    "sample_means": "Medias muestrales",
    "sample_size": "Tamaño de muestra",
    "sample_size_per_replicate": "Tamaño por réplica",
    "sample_standard_deviation": "Desvío estándar muestral",
    "sample_variance": "Varianza muestral",
    "samples": "Muestras",
    "skewness": "Asimetría",
    "standard_deviation": "Desvío estándar",
    "standard_error": "Error estándar",
    "standardized_means": "Medias estandarizadas",
    "step": "Paso",
    "survival_probability": "Probabilidad de supervivencia",
    "symmetric_difference": "Diferencia simétrica",
    "table": "Tabla",
    "test_statistic": "Estadístico de prueba",
    "third_quartile": "Tercer cuartil",
    "threshold": "Umbral",
    "total_probability": "Probabilidad total",
    "underlying_mean": "Media subyacente",
    "underlying_standard_deviation": "Desvío estándar subyacente",
    "union": "Unión",
    "upper_bound": "Cota superior",
    "upper_critical_value": "Valor crítico superior",
    "upper_fence": "Cota superior",
    "upper_quantile": "Cuantil superior",
    "value": "Valor",
    "values": "Valores",
    "variance": "Varianza",
    "z_scores": "Puntajes z",
}

_TABLE_STYLE = (
    "border-collapse: collapse; margin: 0; font-family: var(--jp-content-font-family, sans-serif); font-size: 0.95em;"
)
_HEADER_STYLE = (
    "padding: 0.25em 0.6em; text-align: left;"
    " background: rgba(120, 120, 120, 0.12); border-bottom: 1px solid rgba(120, 120, 120, 0.4);"
)
_CELL_STYLE = "padding: 0.2em 0.6em; border-bottom: 1px solid rgba(120, 120, 120, 0.2); vertical-align: top;"
_FIELD_STYLE = _CELL_STYLE + " white-space: nowrap; text-align: left;"
_CODE_STYLE = (
    "font-family: var(--jp-code-font-family, monospace); font-size: 0.8em;"
    " color: rgba(120, 120, 120, 0.95); font-weight: normal;"
)
_GROUP_STYLE = "display: flex; flex-direction: column; gap: 0.6em; align-items: flex-start;"
_RICH_LABEL_STYLE = (
    "font-size: 0.9em; font-weight: 500; padding-bottom: 0.2em; color: var(--jp-ui-font-color1, inherit);"
)
_OUTER_TITLE_STYLE = "font-weight: 600; font-size: 1em; padding: 0.1em 0; color: var(--jp-ui-font-color1, inherit);"


def display_name_for(model_class: type) -> str:
    return DISPLAY_NAMES.get(model_class.__name__, model_class.__name__)


def field_label_for(field_name: str) -> str:
    return FIELD_LABELS.get(field_name, field_name)


def _field_label_html(field_name: str) -> str:
    label = field_label_for(field_name)
    code_html = f'<div style="{_CODE_STYLE}">{html.escape(field_name)}</div>'
    if label == field_name:
        return code_html
    return f"{html.escape(label)}{code_html}"


def _rich_label_html(field_name: str, index: int | None = None) -> str:
    label = field_label_for(field_name)
    suffix = f"[{index}]" if index is not None else ""
    code_html = f'<span style="{_CODE_STYLE}">{html.escape(field_name)}{suffix}</span>'
    if label == field_name:
        return code_html
    return f'<span style="{_RICH_LABEL_STYLE}">{html.escape(label)}{suffix}</span> {code_html}'


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


def _labelled(label: str | None, body_html: str, label_index: int | None = None) -> str:
    if label is None:
        return body_html
    return f"<div>{_rich_label_html(label, label_index)}{body_html}</div>"


def _model_to_html(
    model: RichMarkdownModel,
    label: str | None = None,
    label_index: int | None = None,
) -> str:
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
    return _labelled(label, inner, label_index)


def _scalar_rows_html(scalar_fields: list[tuple[str, Any]]) -> str:
    return "".join(
        f'<tr><th style="{_FIELD_STYLE}">{_field_label_html(name)}</th>'
        f'<td style="{_CELL_STYLE}">{_value_to_html(value)}</td></tr>'
        for name, value in scalar_fields
    )


def _rich_field_blocks(name: str, value: Any) -> list[str]:
    if _is_rich(value):
        return [_model_to_html(value, label=name)]
    return [_model_to_html(item, label=name, label_index=index) for index, item in enumerate(value)]


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
