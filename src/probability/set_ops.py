from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

_FROZEN = ConfigDict(frozen=True)


class JointEventInput(BaseModel):
    model_config = _FROZEN

    probability_a: float = Field(ge=0.0, le=1.0)
    probability_b: float = Field(ge=0.0, le=1.0)
    probability_intersection: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _validate_intersection(self) -> Self:
        if self.probability_intersection > min(self.probability_a, self.probability_b):
            msg = "intersection cannot exceed min(P(A), P(B))"
            raise ValueError(msg)
        return self


class JointEventProbabilities(BaseModel):
    model_config = _FROZEN

    union: float = Field(ge=0.0, le=1.0)
    intersection: float = Field(ge=0.0, le=1.0)
    complement_a: float = Field(ge=0.0, le=1.0)
    complement_b: float = Field(ge=0.0, le=1.0)
    only_a: float = Field(ge=0.0, le=1.0)
    only_b: float = Field(ge=0.0, le=1.0)
    neither: float = Field(ge=0.0, le=1.0)


def joint_event_probabilities(input_data: JointEventInput) -> JointEventProbabilities:
    union = input_data.probability_a + input_data.probability_b - input_data.probability_intersection
    return JointEventProbabilities(
        union=union,
        intersection=input_data.probability_intersection,
        complement_a=1.0 - input_data.probability_a,
        complement_b=1.0 - input_data.probability_b,
        only_a=input_data.probability_a - input_data.probability_intersection,
        only_b=input_data.probability_b - input_data.probability_intersection,
        neither=1.0 - union,
    )


class SetOperationInput(BaseModel):
    model_config = _FROZEN

    universe: frozenset[str]
    event_a: frozenset[str]
    event_b: frozenset[str]

    @model_validator(mode="after")
    def _validate_subsets(self) -> Self:
        if not self.event_a.issubset(self.universe):
            msg = "event_a must be a subset of universe"
            raise ValueError(msg)
        if not self.event_b.issubset(self.universe):
            msg = "event_b must be a subset of universe"
            raise ValueError(msg)
        return self


class SetOperationResult(BaseModel):
    model_config = _FROZEN

    union: frozenset[str]
    intersection: frozenset[str]
    complement_a: frozenset[str]
    only_a: frozenset[str]
    only_b: frozenset[str]
    symmetric_difference: frozenset[str]


def evaluate_set_operations(input_data: SetOperationInput) -> SetOperationResult:
    intersection = input_data.event_a & input_data.event_b
    return SetOperationResult(
        union=input_data.event_a | input_data.event_b,
        intersection=intersection,
        complement_a=input_data.universe - input_data.event_a,
        only_a=input_data.event_a - input_data.event_b,
        only_b=input_data.event_b - input_data.event_a,
        symmetric_difference=input_data.event_a ^ input_data.event_b,
    )
