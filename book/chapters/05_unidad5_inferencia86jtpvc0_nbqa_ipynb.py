# %%NBQA-CELL-SEP2b5a54
import numpy as np
import pandas as pd

from core import Observations, Settings
from exercises import (
    IntervalContainsInput,
    NumericAnswerInput,
    verify_interval_contains,
    verify_numeric_answer,
)
from inference import (
    MeanKnownVarianceInput,
    MeanUnknownVarianceInput,
    OneSampleMeanTestInput,
    ProportionInput,
    SampleSizeForMeanInput,
    SampleSizeForProportionInput,
    VarianceInput,
    build_confidence_interval_for_mean_known_variance,
    build_confidence_interval_for_mean_unknown_variance,
    build_confidence_interval_for_proportion,
    build_confidence_interval_for_variance,
    sample_size_for_mean,
    sample_size_for_proportion,
    test_one_sample_mean,
)
from inference.hypothesis_tests import Alternative
from sampling import BootstrapInput, bootstrap_mean
from visualization import BootstrapDistributionChartInput, chart_bootstrap_distribution
from widgets import MeanCIExplorerInput, build_mean_ci_explorer


# %%NBQA-CELL-SEP2b5a54
settings = Settings()


# %%NBQA-CELL-SEP2b5a54
confidence_interval = build_confidence_interval_for_mean_known_variance(
    MeanKnownVarianceInput(
        sample_mean=12.0,
        population_standard_deviation=3.0,
        sample_size=36,
        confidence_level=0.95,
    )
)
confidence_interval


# %%NBQA-CELL-SEP2b5a54
build_mean_ci_explorer(MeanCIExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
build_confidence_interval_for_mean_unknown_variance(
    MeanUnknownVarianceInput(
        sample_mean=12.0,
        sample_standard_deviation=3.0,
        sample_size=36,
        confidence_level=0.95,
    )
)


# %%NBQA-CELL-SEP2b5a54
build_confidence_interval_for_proportion(ProportionInput(successes=200, sample_size=400, confidence_level=0.95))


# %%NBQA-CELL-SEP2b5a54
build_confidence_interval_for_variance(VarianceInput(sample_variance=9.0, sample_size=36, confidence_level=0.95))


# %%NBQA-CELL-SEP2b5a54
mean_test_result = test_one_sample_mean(
    OneSampleMeanTestInput(
        sample_mean=12.0,
        sample_standard_deviation=3.0,
        sample_size=36,
        null_mean=11.0,
        alternative=Alternative.TWO_SIDED,
        significance_level=0.05,
    )
)
mean_test_result


# %%NBQA-CELL-SEP2b5a54
rng = np.random.default_rng(settings.random_seed)
synthetic_sample = Observations.validate(pd.DataFrame({"value": rng.normal(loc=12.0, scale=3.0, size=36)}))
bootstrap_result = bootstrap_mean(BootstrapInput(observations=synthetic_sample, replicates=3_000, settings=settings))
chart_bootstrap_distribution(BootstrapDistributionChartInput(bootstrap_result=bootstrap_result, settings=settings))


# %%NBQA-CELL-SEP2b5a54
sample_size_for_mean(
    SampleSizeForMeanInput(
        population_standard_deviation=3.0,
        margin_of_error=1.0,
        confidence_level=0.95,
    )
)


# %%NBQA-CELL-SEP2b5a54
interval = build_confidence_interval_for_mean_known_variance(
    MeanKnownVarianceInput(
        sample_mean=12.0,
        population_standard_deviation=3.0,
        sample_size=36,
        confidence_level=0.95,
    )
)
verify_interval_contains(
    IntervalContainsInput(
        lower_bound=interval.lower_bound,
        upper_bound=interval.upper_bound,
        target_value=11.5,
    )
)


# %%NBQA-CELL-SEP2b5a54
expected_size = sample_size_for_proportion(
    SampleSizeForProportionInput(
        estimated_proportion=0.5,
        margin_of_error=0.03,
        confidence_level=0.95,
    )
).required_sample_size

student_answer = 1067.0
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=student_answer,
        expected_answer=float(expected_size),
        absolute_tolerance=1.0,
    )
)
