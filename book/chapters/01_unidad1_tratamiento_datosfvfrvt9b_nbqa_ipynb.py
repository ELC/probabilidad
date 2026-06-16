# %%NBQA-CELL-SEP2b5a54
import numpy as np
import pandas as pd

from core import Observations, Settings
from descriptive import (
    FrequencyTableInput,
    build_frequency_table,
    detect_outliers_tukey,
    standardize_observations,
    summarize_observations,
)
from exercises import NumericAnswerInput, verify_numeric_answer
from visualization import (
    DescriptiveSummaryChartInput,
    FrequencyChartInput,
    chart_descriptive_summary,
    chart_frequency_table,
)
from widgets import DescriptiveExplorerInput, build_descriptive_explorer


# %%NBQA-CELL-SEP2b5a54
settings = Settings()


# %%NBQA-CELL-SEP2b5a54
rng = np.random.default_rng(settings.random_seed)
raw_waiting_times = rng.normal(loc=4.0, scale=1.2, size=80).clip(min=0.0)
waiting_times = Observations.validate(pd.DataFrame({"value": raw_waiting_times}))
waiting_times.head()


# %%NBQA-CELL-SEP2b5a54
frequency_table = build_frequency_table(FrequencyTableInput(observations=waiting_times, bin_count=10))
chart_frequency_table(FrequencyChartInput(frequency_table=frequency_table, settings=settings))


# %%NBQA-CELL-SEP2b5a54
summary = summarize_observations(waiting_times)
summary


# %%NBQA-CELL-SEP2b5a54
chart_descriptive_summary(
    DescriptiveSummaryChartInput(observations=waiting_times, statistics=summary, settings=settings)
)


# %%NBQA-CELL-SEP2b5a54
outlier_report = detect_outliers_tukey(waiting_times)
outlier_report


# %%NBQA-CELL-SEP2b5a54
standardized = standardize_observations(waiting_times)


# %%NBQA-CELL-SEP2b5a54
build_descriptive_explorer(DescriptiveExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
exercise_sample = Observations.validate(pd.DataFrame({"value": [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]}))
expected_mean = summarize_observations(exercise_sample).location.mean

student_answer = 5.0
verify_numeric_answer(NumericAnswerInput(student_answer=student_answer, expected_answer=expected_mean))


# %%NBQA-CELL-SEP2b5a54
expected_standard_deviation = summarize_observations(exercise_sample).dispersion.sample_standard_deviation
student_answer = 2.138
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=student_answer,
        expected_answer=expected_standard_deviation,
        absolute_tolerance=1e-2,
        relative_tolerance=1e-2,
    )
)
