import math
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import RichMarkdownModel

_FROZEN = ConfigDict(frozen=True)


class TotalProbabilityBranch(RichMarkdownModel):
    model_config = _FROZEN

    label: str
    prior: float = Field(ge=0.0, le=1.0)
    likelihood: float = Field(ge=0.0, le=1.0)


class TotalProbabilityInput(BaseModel):
    model_config = _FROZEN

    branches: tuple[TotalProbabilityBranch, ...]

    @model_validator(mode="after")
    def _validate_partition(self) -> Self:
        if not self.branches:
            msg = "at least one branch is required"
            raise ValueError(msg)
        total_prior = sum(branch.prior for branch in self.branches)
        if not math.isclose(total_prior, 1.0, abs_tol=1e-9):
            msg = f"branch priors must sum to 1; got {total_prior}"
            raise ValueError(msg)
        return self


class TotalProbabilityResult(RichMarkdownModel):
    model_config = _FROZEN

    joint_probabilities: tuple[float, ...]
    total_probability: float = Field(ge=0.0, le=1.0)


def evaluate_total_probability(input_data: TotalProbabilityInput) -> TotalProbabilityResult:
    joint_probabilities = tuple(branch.prior * branch.likelihood for branch in input_data.branches)
    return TotalProbabilityResult(
        joint_probabilities=joint_probabilities,
        total_probability=sum(joint_probabilities),
    )
