# %%NBQA-CELL-SEP2b5a54
from core import Settings
from exercises import NumericAnswerInput, verify_numeric_answer
from probability import (
    BayesInput,
    ConditionalInput,
    JointEventInput,
    SetOperationInput,
    evaluate_bayes,
    evaluate_conditional_probability,
    evaluate_set_operations,
    joint_event_probabilities,
)
from probability.total_probability import TotalProbabilityBranch
from symbolic import bayes_theorem, total_probability_theorem
from widgets import BayesExplorerInput, build_bayes_explorer


# %%NBQA-CELL-SEP2b5a54
settings = Settings()


# %%NBQA-CELL-SEP2b5a54
universe = frozenset({"1", "2", "3", "4", "5", "6"})
event_even = frozenset({"2", "4", "6"})
event_at_least_four = frozenset({"4", "5", "6"})

set_result = evaluate_set_operations(
    SetOperationInput(
        universe=universe,
        event_a=event_even,
        event_b=event_at_least_four,
    )
)
set_result


# %%NBQA-CELL-SEP2b5a54
joint = joint_event_probabilities(
    JointEventInput(
        probability_a=3 / 6,
        probability_b=3 / 6,
        probability_intersection=2 / 6,
    )
)
joint


# %%NBQA-CELL-SEP2b5a54
conditional = evaluate_conditional_probability(
    ConditionalInput(
        probability_intersection=2 / 6,
        probability_conditioning_event=3 / 6,
    )
)
conditional


# %%NBQA-CELL-SEP2b5a54
bayes_theorem().formula


# %%NBQA-CELL-SEP2b5a54
branches = (
    TotalProbabilityBranch(label="Enfermo", prior=0.01, likelihood=0.99),
    TotalProbabilityBranch(label="Sano", prior=0.99, likelihood=0.05),
)
posteriors = evaluate_bayes(BayesInput(branches=branches))
for _posterior in posteriors:
    pass


# %%NBQA-CELL-SEP2b5a54
build_bayes_explorer(BayesExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
total_probability_theorem(partition_size=3).formula


# %%NBQA-CELL-SEP2b5a54
expected_union = joint_event_probabilities(
    JointEventInput(probability_a=0.6, probability_b=0.5, probability_intersection=0.2)
).union

student_answer = 0.9
verify_numeric_answer(NumericAnswerInput(student_answer=student_answer, expected_answer=expected_union))


# %%NBQA-CELL-SEP2b5a54
box_branches = (
    TotalProbabilityBranch(label="C1", prior=0.5, likelihood=0.3),
    TotalProbabilityBranch(label="C2", prior=0.5, likelihood=0.6),
)
expected_posterior = evaluate_bayes(BayesInput(branches=box_branches))[0].posterior

student_answer = 1 / 3
verify_numeric_answer(NumericAnswerInput(student_answer=student_answer, expected_answer=expected_posterior))
