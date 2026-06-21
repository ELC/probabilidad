import matplotlib.pyplot as plt
import pytest

from core import Settings
from visualization import (
    PartitionDiagramInput,
    ProbabilityTreeInput,
    VennTwoSetsInput,
    chart_partition_diagram,
    chart_probability_tree,
    chart_venn_two_sets,
)


def test_chart_venn_two_sets_renders_set_labels(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=0.5,
            probability_b=0.4,
            probability_intersection=0.2,
            set_a_label="Esperan mucho",
            set_b_label="Llegan tarde",
            settings=fixed_settings,
        )
    )
    assert len(figure.axes) == 1
    axes = figure.axes[0]
    texts = [text.get_text() for text in axes.texts]
    legend = axes.get_legend()
    assert legend is not None
    legend_labels = [text.get_text() for text in legend.get_texts()]
    assert "Esperan mucho" in legend_labels
    assert "Llegan tarde" in legend_labels
    assert "P(Ω) = 1" in texts
    assert "0.2" in texts
    plt.close(figure)


def test_chart_venn_two_sets_accepts_custom_intersection_label(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=3 / 6,
            probability_b=3 / 6,
            probability_intersection=2 / 6,
            set_a_label="A",
            set_b_label="B",
            intersection_label="A ∩ B = {4, 6}",
            settings=fixed_settings,
        )
    )
    texts = [text.get_text() for text in figure.axes[0].texts]
    assert "A ∩ B = {4, 6}" in texts
    plt.close(figure)


def test_chart_venn_two_sets_handles_nested_subset(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=0.21,
            probability_b=0.45,
            probability_intersection=0.21,
            set_a_label="T",
            set_b_label="S",
            settings=fixed_settings,
        )
    )
    assert figure.axes
    plt.close(figure)


def test_chart_venn_two_sets_rejects_inconsistent_intersection(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="probability_intersection must not exceed"):
        chart_venn_two_sets(
            VennTwoSetsInput(
                probability_a=0.3,
                probability_b=0.4,
                probability_intersection=0.35,
                settings=fixed_settings,
            )
        )


def test_chart_venn_two_sets_rejects_out_of_range_probability(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="must lie in"):
        chart_venn_two_sets(
            VennTwoSetsInput(
                probability_a=1.2,
                probability_b=0.4,
                probability_intersection=0.1,
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_renders_strips(fixed_settings: Settings) -> None:
    chart = chart_partition_diagram(
        PartitionDiagramInput(
            partition_labels=("Caja 1", "Caja 2", "Caja 3"),
            partition_weights=(2.0, 3.0, 1.0),
            settings=fixed_settings,
        )
    )
    assert chart.to_dict()


def test_chart_partition_diagram_renders_overlay(fixed_settings: Settings) -> None:
    chart = chart_partition_diagram(
        PartitionDiagramInput(
            partition_labels=("A_1", "A_2"),
            partition_weights=(1.0, 1.0),
            overlay_label="Evento B",
            overlay_fractions=(0.4, 0.6),
            settings=fixed_settings,
        )
    )
    assert chart.to_dict()


def test_chart_partition_diagram_rejects_mismatched_lengths(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="same length"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0,),
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_rejects_zero_weights(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="positive"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(0.0, 0.0),
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_rejects_overlay_length_mismatch(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="overlay"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0, 1.0),
                overlay_label="B",
                overlay_fractions=(0.4,),
                settings=fixed_settings,
            )
        )


def test_chart_probability_tree_emits_joint_probabilities(fixed_settings: Settings) -> None:
    chart = chart_probability_tree(
        ProbabilityTreeInput(
            root_label="Ω",
            branch_labels=("Enfermo", "Sano"),
            branch_probabilities=(0.01, 0.99),
            leaf_labels=("Test +", "Test −"),
            conditional_probabilities=((0.99, 0.01), (0.05, 0.95)),
            settings=fixed_settings,
        )
    )
    flattened = str(chart.to_dict(format="vega"))
    assert "Enfermo" in flattened
    assert "Sano" in flattened
    assert "0.01" in flattened
