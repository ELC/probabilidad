import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import FrequencyTable, Observations, Settings
from core.theme import ChartTheme
from descriptive.summary import DescriptiveStatistics
from distributions.evaluations import DensityGrid, ProbabilityMassTable
from inference.mean_ci import MeanConfidenceInterval
from sampling.bootstrap import BootstrapMeanResult
from sampling.clt import CLTSimulationResult
from sampling.lln import LLNMultipleTrajectoriesResult, LLNSimulationResult
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class HistogramChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    bin_count: int = Field(default=20, ge=1)
    title: str = "Histograma"
    settings: Settings = Settings()


def chart_histogram(input_data: HistogramChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    chart = (
        alt
        .Chart(input_data.observations)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("value:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Valor"),
            y=alt.Y("count()", title="Frecuencia"),
        )
        .properties(title=input_data.title)
    )
    return apply_theme(chart, input_data.settings)


class FrequencyChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[FrequencyTable]
    title: str = "Distribución de frecuencias"
    settings: Settings = Settings()


def _build_frequency_chart(
    frequency_table: DataFrame[FrequencyTable],
    title: str,
    theme: ChartTheme,
) -> alt.Chart:
    base = alt.Chart(frequency_table)
    bars = base.mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary).encode(
        x=alt.X("midpoint:Q", title="Marca de clase"),
        y=alt.Y("absolute_frequency:Q", title="Frecuencia absoluta"),
        tooltip=["interval_start", "interval_end", "absolute_frequency", "relative_frequency"],
    )
    ogive = base.mark_line(color=theme.palette.secondary, strokeWidth=theme.line_stroke_width).encode(
        x=alt.X("midpoint:Q"),
        y=alt.Y(
            "cumulative_relative_frequency:Q",
            axis=alt.Axis(title="Frecuencia rel. acumulada"),
        ),
    )
    return alt.layer(bars, ogive).resolve_scale(y="independent").properties(title=title)


def chart_frequency_table(input_data: FrequencyChartInput) -> alt.Chart:
    chart = _build_frequency_chart(
        input_data.frequency_table,
        input_data.title,
        input_data.settings.chart_theme,
    )
    return apply_theme(chart, input_data.settings)


class DensityChartInput(BaseModel):
    model_config = _ARBITRARY

    density_grid: DensityGrid
    title: str | None = None
    settings: Settings = Settings()


def chart_density(input_data: DensityChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"x": input_data.density_grid.grid, "density": input_data.density_grid.density})
    title = input_data.title or f"Densidad — {input_data.density_grid.distribution_name}"
    chart = (
        alt
        .Chart(data)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("x:Q", title="x"),
            y=alt.Y("density:Q", title="f(x)"),
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)


class ProbabilityMassChartInput(BaseModel):
    model_config = _ARBITRARY

    probability_mass: ProbabilityMassTable
    title: str | None = None
    settings: Settings = Settings()


def chart_probability_mass(input_data: ProbabilityMassChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    title = input_data.title or f"Masa de probabilidad — {input_data.probability_mass.distribution_name}"
    chart = (
        alt
        .Chart(input_data.probability_mass.table)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("outcome:O", title="Resultado"),
            y=alt.Y("probability:Q", title="P(X = x)"),
            tooltip=["outcome", "probability"],
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)


class CLTComparisonChartInput(BaseModel):
    model_config = _ARBITRARY

    clt_result: CLTSimulationResult
    bin_count: int = Field(default=40, ge=5)
    title: str = "Medias estandarizadas vs. Normal(0,1)"
    settings: Settings = Settings()


def chart_clt_comparison(input_data: CLTComparisonChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"standardized_mean": input_data.clt_result.standardized_means})
    histogram = (
        alt
        .Chart(data)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("standardized_mean:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Media estandarizada"),
            y=alt.Y("count()", stack=None, title="Frecuencia"),
        )
    )
    grid = np.linspace(-4.0, 4.0, input_data.settings.grid_resolution)
    bin_width = 8.0 / input_data.bin_count
    expected_count = stats.norm.pdf(grid) * input_data.clt_result.standardized_means.size * bin_width
    overlay_data = pd.DataFrame({"x": grid, "y": expected_count})
    overlay = (
        alt
        .Chart(overlay_data)
        .mark_line(color=theme.palette.secondary, strokeWidth=theme.line_stroke_width)
        .encode(x="x:Q", y="y:Q")
    )
    layered = alt.layer(histogram, overlay).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class LLNChartInput(BaseModel):
    model_config = _ARBITRARY

    lln_result: LLNSimulationResult
    title: str = "Ley de los grandes números"
    settings: Settings = Settings()


def chart_lln_running_mean(input_data: LLNChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"step": input_data.lln_result.step, "running_mean": input_data.lln_result.running_mean})
    running = (
        alt
        .Chart(data)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(x=alt.X("step:Q", title="Tamaño de muestra"), y=alt.Y("running_mean:Q", title="Media acumulada"))
    )
    expected_label = "Media teórica"
    expected = (
        alt
        .Chart(pd.DataFrame({"expected_mean": [input_data.lln_result.underlying_mean], "marca": [expected_label]}))
        .mark_rule(strokeDash=[6, 4])
        .encode(
            y="expected_mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[expected_label], range=[theme.palette.secondary]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(running, expected).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class LLNMultipleTrajectoriesChartInput(BaseModel):
    model_config = _ARBITRARY

    lln_result: LLNMultipleTrajectoriesResult
    title: str = "Trayectorias de la media acumulada"
    settings: Settings = Settings()


def chart_lln_multiple_trajectories(input_data: LLNMultipleTrajectoriesChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    running_means = input_data.lln_result.running_means
    trajectory_count, horizon = running_means.shape
    step = input_data.lln_result.step
    trajectories = pd.DataFrame({
        "step": np.tile(step, trajectory_count),
        "running_mean": running_means.reshape(-1),
        "trajectory": np.repeat(np.arange(trajectory_count), horizon),
    })
    lines = (
        alt
        .Chart(trajectories)
        .mark_line(opacity=0.45, strokeWidth=1.0, color=theme.palette.primary)
        .encode(
            x=alt.X("step:Q", title="Tamaño de muestra"),
            y=alt.Y("running_mean:Q", title="Media acumulada"),
            detail="trajectory:N",
        )
    )
    expected_label = "Media teórica"
    expected = (
        alt
        .Chart(pd.DataFrame({"expected_mean": [input_data.lln_result.underlying_mean], "marca": [expected_label]}))
        .mark_rule(strokeDash=[6, 4], strokeWidth=2.0)
        .encode(
            y="expected_mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[expected_label], range=[theme.palette.accent]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(lines, expected).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class BootstrapDistributionChartInput(BaseModel):
    model_config = _ARBITRARY

    bootstrap_result: BootstrapMeanResult
    bin_count: int = Field(default=40, ge=5)
    title: str = "Distribución bootstrap de la media"
    settings: Settings = Settings()


def chart_bootstrap_distribution(input_data: BootstrapDistributionChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"bootstrap_mean": input_data.bootstrap_result.bootstrap_means})
    histogram = (
        alt
        .Chart(data)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("bootstrap_mean:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Media bootstrap"),
            y=alt.Y("count()", title="Frecuencia"),
        )
    )
    lower_label = "Cuantil inferior"
    upper_label = "Cuantil superior"
    point_label = "Estimación puntual"
    bounds = pd.DataFrame({
        "boundary": [lower_label, upper_label, point_label],
        "value": [
            input_data.bootstrap_result.lower_quantile,
            input_data.bootstrap_result.upper_quantile,
            input_data.bootstrap_result.point_estimate,
        ],
    })
    rules = (
        alt
        .Chart(bounds)
        .mark_rule(strokeWidth=2.0)
        .encode(
            x="value:Q",
            color=alt.Color(
                "boundary:N",
                scale=alt.Scale(
                    domain=[lower_label, upper_label, point_label],
                    range=[theme.palette.secondary, theme.palette.secondary, theme.palette.accent],
                ),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(histogram, rules).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class ConfidenceIntervalChartInput(BaseModel):
    model_config = _ARBITRARY

    intervals: tuple[MeanConfidenceInterval, ...]
    target_mean: float | None = None
    title: str = "Intervalos de confianza repetidos"
    settings: Settings = Settings()


def chart_confidence_interval(input_data: ConfidenceIntervalChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    records = []
    for index, interval in enumerate(input_data.intervals, start=1):
        contains_target = (
            input_data.target_mean is None or interval.lower_bound <= input_data.target_mean <= interval.upper_bound
        )
        records.append({
            "replicate": index,
            "lower": interval.lower_bound,
            "upper": interval.upper_bound,
            "point": interval.point_estimate,
            "covers": contains_target,
        })
    data = pd.DataFrame.from_records(records)
    bars = (
        alt
        .Chart(data)
        .mark_rule(strokeWidth=2.0)
        .encode(
            x="lower:Q",
            x2="upper:Q",
            y=alt.Y("replicate:O", title="Réplica"),
            color=alt.Color(
                "covers:N",
                scale=alt.Scale(
                    domain=[False, True],
                    range=[theme.palette.danger, theme.palette.primary],
                ),
                legend=alt.Legend(title="Cubre la media", orient="bottom"),
            ),
        )
    )
    points = (
        alt
        .Chart(data)
        .mark_point(filled=True, color=theme.palette.accent, size=theme.point_size)
        .encode(x="point:Q", y="replicate:O")
    )
    layers = [bars, points]
    if input_data.target_mean is not None:
        target_label = "Media verdadera"
        target = (
            alt
            .Chart(pd.DataFrame({"target": [input_data.target_mean], "marca": [target_label]}))
            .mark_rule(strokeDash=[6, 4])
            .encode(
                x="target:Q",
                color=alt.Color(
                    "marca:N",
                    scale=alt.Scale(domain=[target_label], range=[theme.palette.muted]),
                    legend=alt.Legend(title=None, orient="bottom"),
                ),
            )
        )
        layers.append(target)
    layered = alt.layer(*layers).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class DescriptiveSummaryChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    statistics: DescriptiveStatistics
    title: str = "Boxplot con marcas de resumen"
    settings: Settings = Settings()


def _build_descriptive_summary_chart(
    observations: DataFrame[Observations],
    statistics: DescriptiveStatistics,
    title: str,
    theme: ChartTheme,
) -> alt.Chart:
    box = (
        alt
        .Chart(observations)
        .mark_boxplot(extent=1.5, color=theme.palette.primary, size=40)
        .encode(x=alt.X("value:Q", title="Valor"))
    )
    mean_label = "Media muestral"
    mean_mark = (
        alt
        .Chart(pd.DataFrame({"mean": [statistics.location.mean], "marca": [mean_label]}))
        .mark_rule(strokeWidth=theme.line_stroke_width, strokeDash=[4, 4])
        .encode(
            x="mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[mean_label], range=[theme.palette.accent]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    return alt.layer(box, mean_mark).properties(title=title)


def chart_descriptive_summary(input_data: DescriptiveSummaryChartInput) -> alt.Chart:
    chart = _build_descriptive_summary_chart(
        input_data.observations,
        input_data.statistics,
        input_data.title,
        input_data.settings.chart_theme,
    )
    return apply_theme(chart, input_data.settings)


class ObservationsOverviewInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    frequency_table: DataFrame[FrequencyTable]
    statistics: DescriptiveStatistics
    frequency_title: str = "Distribución de frecuencias"
    summary_title: str = "Boxplot con marcas de resumen"
    settings: Settings = Settings()


def chart_observations_overview(input_data: ObservationsOverviewInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    histogram = _build_frequency_chart(
        input_data.frequency_table,
        input_data.frequency_title,
        theme,
    ).properties(width=theme.width, height=theme.height)
    boxplot = _build_descriptive_summary_chart(
        input_data.observations,
        input_data.statistics,
        input_data.summary_title,
        theme,
    ).properties(width=theme.width, height=120)
    composed = (
        alt
        .vconcat(histogram, boxplot, spacing=10)
        .resolve_scale(x="shared")
    )
    return apply_theme(composed, input_data.settings, set_size=False)


class VennTwoSetsInput(BaseModel):
    model_config = _ARBITRARY

    set_a_label: str = "A"
    set_b_label: str = "B"
    intersection_label: str | None = None
    title: str = "Diagrama de Venn"
    settings: Settings = Settings()


def chart_venn_two_sets(input_data: VennTwoSetsInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    chart_width = 520
    chart_height = 300
    centers = pd.DataFrame({
        "x": [-0.7, 0.7],
        "y": [0.0, 0.0],
        "label": [input_data.set_a_label, input_data.set_b_label],
    })
    color_scale = alt.Scale(
        domain=[input_data.set_a_label, input_data.set_b_label],
        range=[theme.palette.primary, theme.palette.secondary],
    )
    circles = (
        alt
        .Chart(centers)
        .mark_circle(size=42000, opacity=0.5, stroke=theme.palette.muted, strokeWidth=2)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[-2.6, 2.6]), axis=None),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[-1.5, 1.5]), axis=None),
            color=alt.Color("label:N", scale=color_scale, legend=None),
        )
    )
    set_label_data = pd.DataFrame({
        "x": [-1.7, 1.7],
        "y": [1.2, 1.2],
        "label": [input_data.set_a_label, input_data.set_b_label],
    })
    set_labels = (
        alt
        .Chart(set_label_data)
        .mark_text(fontSize=15, fontWeight="bold")
        .encode(x="x:Q", y="y:Q", text="label:N")
    )
    intersection_label = (
        input_data.intersection_label
        if input_data.intersection_label is not None
        else f"{input_data.set_a_label} ∩ {input_data.set_b_label}"
    )
    intersection_data = pd.DataFrame({"x": [0.0], "y": [0.0], "label": [intersection_label]})
    intersection_text = (
        alt
        .Chart(intersection_data)
        .mark_text(fontSize=13, fontWeight="bold", color=theme.title_color)
        .encode(x="x:Q", y="y:Q", text="label:N")
    )
    layered = (
        alt
        .layer(circles, set_labels, intersection_text)
        .properties(title=input_data.title, width=chart_width, height=chart_height)
    )
    return apply_theme(layered, input_data.settings, set_size=False)


class PartitionDiagramInput(BaseModel):
    model_config = _ARBITRARY

    partition_labels: tuple[str, ...] = ("A_1", "A_2", "A_3")
    partition_weights: tuple[float, ...] = (1.0, 1.0, 1.0)
    overlay_label: str | None = None
    overlay_fractions: tuple[float, ...] | None = None
    title: str = "Partición del espacio muestral"
    settings: Settings = Settings()


def chart_partition_diagram(input_data: PartitionDiagramInput) -> alt.Chart:  # noqa: PLR0914
    theme = input_data.settings.chart_theme
    if len(input_data.partition_labels) != len(input_data.partition_weights):
        raise ValueError("partition_labels and partition_weights must have the same length")
    weights = np.asarray(input_data.partition_weights, dtype=float)
    if weights.sum() <= 0:
        raise ValueError("partition_weights must sum to a positive number")
    fractions = weights / weights.sum()
    edges = np.concatenate(([0.0], np.cumsum(fractions)))
    records = []
    for index, (label, fraction) in enumerate(zip(input_data.partition_labels, fractions, strict=True)):
        records.append({
            "x_start": float(edges[index]),
            "x_end": float(edges[index + 1]),
            "y_start": 0.0,
            "y_end": 1.0,
            "label": label,
            "fraction": fraction,
        })
    bands = pd.DataFrame.from_records(records)
    rectangles = (
        alt
        .Chart(bands)
        .mark_rect(opacity=0.45, stroke=theme.palette.muted, strokeWidth=1.5)
        .encode(
            x=alt.X("x_start:Q", scale=alt.Scale(domain=[0.0, 1.0]), axis=None),
            x2="x_end:Q",
            y=alt.Y("y_start:Q", scale=alt.Scale(domain=[-0.4, 1.2]), axis=None),
            y2="y_end:Q",
            color=alt.Color("label:N", legend=None, scale=alt.Scale(scheme="tableau10")),
        )
        .properties(width=520, height=180)
    )
    bands_with_center = bands.assign(x_center=(bands["x_start"] + bands["x_end"]) / 2)
    text = (
        alt
        .Chart(bands_with_center)
        .mark_text(fontSize=14, fontWeight="bold", baseline="middle")
        .encode(x="x_center:Q", y=alt.Y(value=0.5), text="label:N")
    )
    layers: list[alt.Chart] = [rectangles, text]
    if input_data.overlay_label is not None and input_data.overlay_fractions is not None:
        if len(input_data.overlay_fractions) != len(input_data.partition_labels):
            raise ValueError("overlay_fractions must match partition length")
        overlay_records = []
        for index, fraction in enumerate(input_data.overlay_fractions):
            overlay_records.append({
                "x_start": float(edges[index]),
                "x_end": float(edges[index] + fraction * (edges[index + 1] - edges[index])),
                "y_start": -0.35,
                "y_end": -0.05,
            })
        overlay_df = pd.DataFrame.from_records(overlay_records)
        overlay = (
            alt
            .Chart(overlay_df)
            .mark_rect(color=theme.palette.accent, opacity=0.75)
            .encode(x="x_start:Q", x2="x_end:Q", y="y_start:Q", y2="y_end:Q")
        )
        overlay_label_df = pd.DataFrame({"x": [0.0], "y": [-0.2], "label": [input_data.overlay_label]})
        overlay_label = (
            alt
            .Chart(overlay_label_df)
            .mark_text(fontSize=13, baseline="middle", align="left", dx=6)
            .encode(x="x:Q", y="y:Q", text="label:N")
        )
        layers.extend([overlay, overlay_label])
    layered = alt.layer(*layers).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class ProbabilityTreeInput(BaseModel):
    model_config = _ARBITRARY

    root_label: str = "Ω"
    branch_labels: tuple[str, str] = ("D", "D̄")
    branch_probabilities: tuple[float, float] = (0.5, 0.5)
    leaf_labels: tuple[str, str] = ("+", "−")
    conditional_probabilities: tuple[tuple[float, float], tuple[float, float]] = (
        (0.5, 0.5),
        (0.5, 0.5),
    )
    title: str = "Árbol de probabilidad"
    settings: Settings = Settings()


def chart_probability_tree(input_data: ProbabilityTreeInput) -> alt.Chart:  # noqa: PLR0914
    theme = input_data.settings.chart_theme
    root_x, branch_x, leaf_x = 0.0, 1.0, 2.2
    branch_ys = (1.0, -1.0)
    leaf_offsets = (0.45, -0.45)
    edges = []
    nodes = [{"x": root_x, "y": 0.0, "label": input_data.root_label, "kind": "root"}]
    for branch_index, (branch_label, branch_prob) in enumerate(
        zip(input_data.branch_labels, input_data.branch_probabilities, strict=True),
    ):
        branch_y = branch_ys[branch_index]
        edges.append({
            "x": [root_x, branch_x],
            "y": [0.0, branch_y],
            "label_x": (root_x + branch_x) / 2,
            "label_y": (0.0 + branch_y) / 2,
            "weight": f"{branch_label}: {branch_prob:.2f}",
        })
        nodes.append({"x": branch_x, "y": branch_y, "label": branch_label, "kind": "branch"})
        for leaf_index, (leaf_label, conditional_prob) in enumerate(
            zip(input_data.leaf_labels, input_data.conditional_probabilities[branch_index], strict=True),
        ):
            leaf_y = branch_y + leaf_offsets[leaf_index]
            edges.append({
                "x": [branch_x, leaf_x],
                "y": [branch_y, leaf_y],
                "label_x": (branch_x + leaf_x) / 2,
                "label_y": (branch_y + leaf_y) / 2,
                "weight": f"{leaf_label}|{branch_label}: {conditional_prob:.2f}",
            })
            joint = branch_prob * conditional_prob
            nodes.append({
                "x": leaf_x,
                "y": leaf_y,
                "label": f"{branch_label}∩{leaf_label}: {joint:.3f}",
                "kind": "leaf",
            })
    edge_records = []
    for edge_index, edge in enumerate(edges):
        edge_records.append({"x": edge["x"][0], "y": edge["y"][0], "edge_id": edge_index})
        edge_records.append({"x": edge["x"][1], "y": edge["y"][1], "edge_id": edge_index})
    edge_df = pd.DataFrame.from_records(edge_records)
    line_chart = (
        alt
        .Chart(edge_df)
        .mark_line(color=theme.palette.muted, strokeWidth=1.5)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[-0.4, 3.4]), axis=None),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[-1.9, 1.9]), axis=None),
            detail="edge_id:N",
        )
        .properties(width=520, height=320)
    )
    edge_label_df = pd.DataFrame.from_records([
        {"x": edge["label_x"], "y": edge["label_y"], "label": edge["weight"]} for edge in edges
    ])
    edge_labels = (
        alt
        .Chart(edge_label_df)
        .mark_text(fontSize=11, dy=-8)
        .encode(x="x:Q", y="y:Q", text="label:N")
    )
    node_df = pd.DataFrame.from_records(nodes)
    node_dots = (
        alt
        .Chart(node_df)
        .mark_circle(size=180, color=theme.palette.primary)
        .encode(x="x:Q", y="y:Q")
    )
    node_labels = (
        alt
        .Chart(node_df)
        .mark_text(fontSize=12, fontWeight="bold", align="left", dx=10)
        .encode(x="x:Q", y="y:Q", text="label:N")
    )
    layered = alt.layer(line_chart, edge_labels, node_dots, node_labels).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)
