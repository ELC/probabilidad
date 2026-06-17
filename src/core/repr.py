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
    return f"`array[{shape}]` [{head}{suffix}]"


def _format_sequence(value: tuple[Any, ...] | list[Any]) -> str:
    if not value:
        return "(vacío)"
    return "<br>".join(f"- {format_value(item)}" for item in value)


def _format_set(value: frozenset[Any] | set[Any]) -> str:
    if not value:
        return "∅"
    items = sorted(value, key=str)
    return "{" + ", ".join(format_value(item) for item in items) + "}"


def _format_basemodel(value: BaseModel) -> str:
    return f"`{type(value).__name__}(...)`"


def _format_bool(value: bool) -> str:  # noqa: FBT001
    return "Sí" if value else "No"


class RichMarkdownModel(BaseModel):
    def _repr_markdown_(self) -> str:  # noqa: PLW3201 — IPython display hook
        header = f"**{display_name_for(type(self))}**"
        rows = ["", "| Campo | Valor |", "| --- | --- |"]
        # pylint: disable=not-an-iterable
        for field_name in type(self).model_fields:
            value_text = format_value(getattr(self, field_name))
            rows.append(f"| `{field_name}` | {value_text} |")
        return "\n".join([header, *rows])


def _format_rich_model(value: RichMarkdownModel) -> str:
    parts = [f"**{display_name_for(type(value))}**"]
    # pylint: disable-next=not-an-iterable
    field_names = list(type(value).model_fields)
    parts.extend(f"{name}: {format_value(getattr(value, name))}" for name in field_names)
    return "<br>".join(parts)


_Predicate = type | tuple[type, ...]
_Formatter = Callable[[Any], str]
_DISPATCH: tuple[tuple[_Predicate, _Formatter], ...] = (
    (RichMarkdownModel, _format_rich_model),
    (BaseModel, _format_basemodel),
    (bool, _format_bool),
    (np.integer, lambda value: str(int(value))),
    (np.floating, lambda value: _format_float(float(value))),
    (int, str),
    (float, _format_float),
    (np.ndarray, _format_array),
    ((tuple, list), _format_sequence),
    ((frozenset, set), _format_set),
    (str, lambda value: value),
)


def format_value(value: Any) -> str:
    for value_type, formatter in _DISPATCH:
        if isinstance(value, value_type):
            return formatter(value)
    return str(value)
