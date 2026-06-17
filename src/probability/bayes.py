from pydantic import BaseModel, ConfigDict, Field

from core import RichMarkdownModel
from probability.total_probability import (
    TotalProbabilityBranch,
    TotalProbabilityInput,
    evaluate_total_probability,
)

_FROZEN = ConfigDict(frozen=True)


class BayesInput(BaseModel):
    model_config = _FROZEN

    branches: tuple[TotalProbabilityBranch, ...]


class BayesPosterior(RichMarkdownModel):
    model_config = _FROZEN

    label: str
    prior: float = Field(ge=0.0, le=1.0)
    likelihood: float = Field(ge=0.0, le=1.0)
    joint_probability: float = Field(ge=0.0, le=1.0)
    posterior: float = Field(ge=0.0, le=1.0)


def evaluate_bayes(input_data: BayesInput) -> tuple[BayesPosterior, ...]:
    total = evaluate_total_probability(TotalProbabilityInput(branches=input_data.branches))
    if total.total_probability == 0.0:
        msg = "evidence probability is zero; Bayes' theorem is undefined"
        raise ValueError(msg)
    return tuple(
        BayesPosterior(
            label=branch.label,
            prior=branch.prior,
            likelihood=branch.likelihood,
            joint_probability=joint,
            posterior=joint / total.total_probability,
        )
        for branch, joint in zip(input_data.branches, total.joint_probabilities, strict=True)
    )
