from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict

from core import RichMarkdownModel


class NestedModel(RichMarkdownModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str
    value: float


class OuterModel(RichMarkdownModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    integer_field: int
    float_field: float
    boolean_field: bool
    string_field: str
    nested_field: NestedModel
    array_field: np.ndarray
    tuple_field: tuple[float, ...]
    set_field: frozenset[str]
    optional_field: float | None


class NestedListModel(RichMarkdownModel):
    model_config = ConfigDict(frozen=True)

    members: tuple[NestedModel, ...]


class PlainModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: int


class OnlyChildrenModel(RichMarkdownModel):
    model_config = ConfigDict(frozen=True)

    location: NestedModel
    dispersion: NestedModel


class MixedModel(RichMarkdownModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    items: tuple[Any, ...]
