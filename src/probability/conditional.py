from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import RichMarkdownModel

_FROZEN = ConfigDict(frozen=True)


class ConditionalInput(BaseModel):
    model_config = _FROZEN

    probability_intersection: float = Field(ge=0.0, le=1.0)
    probability_conditioning_event: float = Field(gt=0.0, le=1.0)

    @model_validator(mode="after")
    def _validate_intersection(self) -> Self:
        if self.probability_intersection > self.probability_conditioning_event:
            msg = "intersection cannot exceed conditioning event probability"
            raise ValueError(msg)
        return self


class ConditionalProbability(RichMarkdownModel):
    model_config = _FROZEN

    probability: float = Field(ge=0.0, le=1.0)


def evaluate_conditional_probability(input_data: ConditionalInput) -> ConditionalProbability:
    return ConditionalProbability(
        probability=input_data.probability_intersection / input_data.probability_conditioning_event,
    )
