from typing import Any

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib_venn import venn2, venn2_circles
from pydantic import BaseModel, ConfigDict

from core import Settings
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)

_VENN_REGION_IDS = ("10", "01", "11")


def _format_probability(probability: float) -> str:
    return f"{probability:.3g}"


class VennTwoSetsInput(BaseModel):
    model_config = _ARBITRARY

    probability_a: float
    probability_b: float
    probability_intersection: float
    set_a_label: str = "A"
    set_b_label: str = "B"
    intersection_label: str | None = None
    title: str = "Diagrama de Venn"
    settings: Settings = Settings()


def chart_venn_two_sets(input_data: VennTwoSetsInput) -> Figure:  # noqa: PLR0914
    probability_a = input_data.probability_a
    probability_b = input_data.probability_b
    probability_intersection = input_data.probability_intersection
    for name, value in (
        ("probability_a", probability_a),
        ("probability_b", probability_b),
        ("probability_intersection", probability_intersection),
    ):
        if not 0.0 <= value <= 1.0:
            msg = f"{name} must lie in [0, 1]; got {value}"
            raise ValueError(msg)
    if probability_intersection > min(probability_a, probability_b):
        msg = (
            "probability_intersection must not exceed min(probability_a, probability_b);"
            f" got {probability_intersection} > {min(probability_a, probability_b)}"
        )
        raise ValueError(msg)
    subset_a_only = probability_a - probability_intersection
    subset_b_only = probability_b - probability_intersection
    subsets = (subset_a_only, subset_b_only, probability_intersection)
    theme = input_data.settings.chart_theme
    palette = theme.palette
    figure, axes = plt.subplots(figsize=(theme.width / 100, theme.height / 100))
    figure.patch.set_facecolor(palette.background)
    axes.set_facecolor(palette.background)
    diagram = venn2(
        subsets=subsets,
        set_labels=("", ""),
        ax=axes,
    )
    region_colors = {"10": palette.primary, "01": palette.secondary, "11": palette.accent}
    for region_id, color in region_colors.items():
        patch = diagram.get_patch_by_id(region_id)
        patch.set_color(color)
        patch.set_alpha(0.5)
    venn2_circles(subsets=subsets, ax=axes, linewidth=1.5, color=palette.muted)
    intersection_label = (
        input_data.intersection_label
        if input_data.intersection_label is not None
        else _format_probability(probability_intersection)
    )
    region_label_texts = {
        "10": _format_probability(subset_a_only),
        "01": _format_probability(subset_b_only),
        "11": intersection_label,
    }
    for region_id, text in region_label_texts.items():
        label = diagram.get_label_by_id(region_id)
        label.set_text(text)
        label.set_color(theme.label_color)
        label.set_fontsize(theme.font_size)
    legend_handles = [
        Rectangle((0, 0), 1, 1, facecolor=palette.primary, alpha=0.5, edgecolor=palette.muted),
        Rectangle((0, 0), 1, 1, facecolor=palette.secondary, alpha=0.5, edgecolor=palette.muted),
    ]
    axes.legend(
        legend_handles,
        [input_data.set_a_label, input_data.set_b_label],
        loc="upper right",
        frameon=False,
        labelcolor=theme.title_color,
        fontsize=theme.font_size,
    )
    axes.text(
        0.02,
        0.98,
        f"P(Ω) = {_format_probability(1.0)}",
        transform=axes.transAxes,
        color=theme.title_color,
        fontsize=theme.font_size,
        verticalalignment="top",
        horizontalalignment="left",
    )
    figure.suptitle(input_data.title, color=theme.title_color, fontsize=theme.font_size + 3)
    figure.tight_layout()
    return figure


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
        msg = "partition_labels and partition_weights must have the same length"
        raise ValueError(msg)
    weights = np.asarray(input_data.partition_weights, dtype=float)
    if weights.sum() <= 0:
        msg = "partition_weights must sum to a positive number"
        raise ValueError(msg)
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
            msg = "overlay_fractions must match partition length"
            raise ValueError(msg)
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
    root_x, branch_x, leaf_x = 0.0, 1.1, 2.6
    branch_ys = (1.1, -1.1)
    leaf_offsets = (0.7, -0.7)
    edge_label_y_offset = 0.12
    edges: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = [
        {"x": root_x, "y": 0.0, "label": input_data.root_label, "kind": "root"},
    ]
    for branch_index, (branch_label, branch_prob) in enumerate(
        zip(input_data.branch_labels, input_data.branch_probabilities, strict=True),
    ):
        branch_y = branch_ys[branch_index]
        slope_sign = 1.0 if branch_y >= 0.0 else -1.0
        edges.append({
            "x": [root_x, branch_x],
            "y": [0.0, branch_y],
            "label_x": (root_x + branch_x) / 2,
            "label_y": (0.0 + branch_y) / 2 + slope_sign * edge_label_y_offset,
            "weight": f"{branch_label}: {_format_probability(branch_prob)}",
        })
        nodes.append({"x": branch_x, "y": branch_y, "label": branch_label, "kind": "branch"})
        for leaf_index, (leaf_label, conditional_prob) in enumerate(
            zip(input_data.leaf_labels, input_data.conditional_probabilities[branch_index], strict=True),
        ):
            leaf_y = branch_y + leaf_offsets[leaf_index]
            leaf_slope_sign = 1.0 if leaf_offsets[leaf_index] >= 0.0 else -1.0
            edges.append({
                "x": [branch_x, leaf_x],
                "y": [branch_y, leaf_y],
                "label_x": (branch_x + leaf_x) / 2,
                "label_y": (branch_y + leaf_y) / 2 + leaf_slope_sign * edge_label_y_offset,
                "weight": f"{leaf_label}|{branch_label}: {_format_probability(conditional_prob)}",
            })
            joint = branch_prob * conditional_prob
            nodes.append({
                "x": leaf_x,
                "y": leaf_y,
                "label": f"{branch_label}∩{leaf_label}: {_format_probability(joint)}",
                "kind": "leaf",
            })
    edge_records: list[dict[str, Any]] = []
    for edge_index, edge in enumerate(edges):
        edge_records.extend((
            {"x": edge["x"][0], "y": edge["y"][0], "edge_id": edge_index},
            {"x": edge["x"][1], "y": edge["y"][1], "edge_id": edge_index},
        ))
    edge_df = pd.DataFrame.from_records(edge_records)
    line_chart = (
        alt
        .Chart(edge_df)
        .mark_line(color=theme.palette.muted, strokeWidth=1.5)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[-0.4, 4.4]), axis=None),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[-2.2, 2.2]), axis=None),
            detail="edge_id:N",
        )
        .properties(width=560, height=360)
    )
    edge_label_df = pd.DataFrame.from_records([
        {"x": edge["label_x"], "y": edge["label_y"], "label": edge["weight"]} for edge in edges
    ])
    edge_labels = alt.Chart(edge_label_df).mark_text(fontSize=10).encode(x="x:Q", y="y:Q", text="label:N")
    node_df = pd.DataFrame.from_records(nodes)
    node_dots = alt.Chart(node_df).mark_circle(size=180, color=theme.palette.primary).encode(x="x:Q", y="y:Q")
    node_labels = (
        alt
        .Chart(node_df)
        .mark_text(fontSize=12, fontWeight="bold", align="left", dx=12)
        .encode(x="x:Q", y="y:Q", text="label:N")
    )
    layered = alt.layer(line_chart, edge_labels, node_dots, node_labels).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings, set_size=False)
