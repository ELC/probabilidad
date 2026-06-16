from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

_FROZEN = ConfigDict(frozen=True)


class NormalParams(BaseModel):
    model_config = _FROZEN

    mean: float = 0.0
    standard_deviation: float = Field(default=1.0, gt=0.0)


class StandardNormalParams(BaseModel):
    model_config = _FROZEN


class ContinuousUniformParams(BaseModel):
    model_config = _FROZEN

    minimum: float = 0.0
    maximum: float = 1.0

    @model_validator(mode="after")
    def _validate_bounds(self) -> Self:
        if self.minimum >= self.maximum:
            msg = "minimum must be strictly less than maximum"
            raise ValueError(msg)
        return self


class DiscreteUniformParams(BaseModel):
    model_config = _FROZEN

    minimum: int = 1
    maximum: int = 6

    @model_validator(mode="after")
    def _validate_bounds(self) -> Self:
        if self.minimum > self.maximum:
            msg = "minimum must be <= maximum"
            raise ValueError(msg)
        return self


class ExponentialParams(BaseModel):
    model_config = _FROZEN

    rate: float = Field(default=1.0, gt=0.0)


class BinomialParams(BaseModel):
    model_config = _FROZEN

    trials: int = Field(default=10, ge=1)
    success_probability: float = Field(default=0.5, ge=0.0, le=1.0)


class PoissonParams(BaseModel):
    model_config = _FROZEN

    rate: float = Field(default=1.0, gt=0.0)


class GeometricParams(BaseModel):
    model_config = _FROZEN

    success_probability: float = Field(default=0.5, gt=0.0, le=1.0)


class HypergeometricParams(BaseModel):
    model_config = _FROZEN

    population_size: int = Field(default=20, ge=1)
    success_states: int = Field(default=7, ge=0)
    draws: int = Field(default=5, ge=0)

    @model_validator(mode="after")
    def _validate_counts(self) -> Self:
        if self.success_states > self.population_size:
            msg = "success_states cannot exceed population_size"
            raise ValueError(msg)
        if self.draws > self.population_size:
            msg = "draws cannot exceed population_size"
            raise ValueError(msg)
        return self


class ChiSquareParams(BaseModel):
    model_config = _FROZEN

    degrees_of_freedom: int = Field(default=1, ge=1)


class StudentTParams(BaseModel):
    model_config = _FROZEN

    degrees_of_freedom: float = Field(default=10.0, gt=0.0)


class FParams(BaseModel):
    model_config = _FROZEN

    numerator_degrees_of_freedom: int = Field(default=5, ge=1)
    denominator_degrees_of_freedom: int = Field(default=10, ge=1)


class BetaParams(BaseModel):
    model_config = _FROZEN

    alpha: float = Field(default=2.0, gt=0.0)
    beta: float = Field(default=5.0, gt=0.0)
