from typing import Any

import altair as alt
import ipywidgets as widgets
import pandas as pd
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import Settings
from probability import BayesInput, evaluate_bayes
from probability.total_probability import TotalProbabilityBranch
from visualization.theme import apply_theme


class BayesExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def build_bayes_explorer(input_data: BayesExplorerInput) -> widgets.Widget:
    prevalence_slider = widgets.FloatSlider(min=0.001, max=0.5, step=0.001, value=0.01, description="Prevalencia")
    sensitivity_slider = widgets.FloatSlider(min=0.5, max=0.999, step=0.001, value=0.99, description="Sensibilidad")
    specificity_slider = widgets.FloatSlider(min=0.5, max=0.999, step=0.001, value=0.95, description="Especificidad")
    posterior_label = widgets.HTML(value="")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        sick_branch = TotalProbabilityBranch(
            label="Enfermo",
            prior=prevalence_slider.value,
            likelihood=sensitivity_slider.value,
        )
        healthy_branch = TotalProbabilityBranch(
            label="Sano",
            prior=1.0 - prevalence_slider.value,
            likelihood=1.0 - specificity_slider.value,
        )
        posteriors = evaluate_bayes(BayesInput(branches=(sick_branch, healthy_branch)))
        sick_posterior = posteriors[0].posterior
        posterior_label.value = (
            f"<b>P(Enfermo | Test positivo) = {sick_posterior:.4f}</b>"
        )
        data = pd.DataFrame(
            {
                "hipótesis": [posterior.label for posterior in posteriors],
                "previo": [posterior.prior for posterior in posteriors],
                "posterior": [posterior.posterior for posterior in posteriors],
            }
        ).melt(id_vars="hipótesis", var_name="distribución", value_name="probabilidad")
        chart = (
            alt.Chart(data)
            .mark_bar(opacity=input_data.settings.chart_theme.bar_opacity)
            .encode(
                x=alt.X("hipótesis:N", title="Hipótesis"),
                xOffset="distribución:N",
                y=alt.Y("probabilidad:Q", title="Probabilidad"),
                color=alt.Color("distribución:N", title="Distribución"),
                tooltip=["hipótesis", "distribución", "probabilidad"],
            )
            .properties(title="Previa vs. Posterior")
        )
        themed = apply_theme(chart, input_data.settings)
        with output:
            output.clear_output(wait=True)
            display(themed)

    for control in (prevalence_slider, sensitivity_slider, specificity_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([prevalence_slider, sensitivity_slider, specificity_slider, posterior_label, output])
