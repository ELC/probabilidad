import pytest

from core import Settings
from descriptive import ClinicSampleInput, generate_clinic_sample, style_display_table


def test_generate_clinic_sample_builds_cohesive_dataframe() -> None:
    sample = generate_clinic_sample(ClinicSampleInput(settings=Settings(), sample_size=80))

    assert len(sample.clinic_data) == 80
    assert set(sample.clinic_data.columns) == {"value", "area", "delay_reason", "people_ahead"}
    assert list(sample.clinic_display_table.columns) == [
        "Minutos de espera",
        "Área de atención",
        "Motivo de demora",
        "Personas adelante",
    ]
    assert len(sample.waiting_times) == 80
    assert sample.area_frequency_table["absolute_frequency"].sum() == 80
    assert sample.people_ahead_frequency_table["absolute_frequency"].sum() == 80
    assert list(sample.area_display_table.columns) == ["Clase $k$", "$n_k$", "$f_k$"]
    assert list(sample.people_ahead_display_table.columns) == ["$x_k$", "$n_k$", "$f_k$", "$N_k$", "$F_k$"]
    assert list(sample.frequency_display_table.columns) == ["Intervalo", "$x_k$", "$n_k$", "$f_k$", "$N_k$", "$F_k$"]


def test_generate_clinic_sample_excludes_none_from_pareto_table() -> None:
    sample = generate_clinic_sample(ClinicSampleInput(settings=Settings(), sample_size=80))

    assert "Ninguna" in set(sample.clinic_data["delay_reason"])
    assert "Ninguna" not in set(sample.delay_reason_frequency_table["category"])
    assert sample.delay_reason_frequency_table["absolute_frequency"].sum() < len(sample.clinic_data)


def test_generate_clinic_sample_is_reproducible() -> None:
    settings = Settings(random_seed=20260101)
    first = generate_clinic_sample(ClinicSampleInput(settings=settings, sample_size=80))
    second = generate_clinic_sample(ClinicSampleInput(settings=settings, sample_size=80))

    assert first.clinic_data.equals(second.clinic_data)
    assert first.frequency_table.equals(second.frequency_table)


@pytest.mark.parametrize(
    ("table_attr", "numeric_column_count"),
    [
        pytest.param("area_display_table", 2, id="area"),
        pytest.param("delay_reason_display_table", 3, id="delay_reason"),
        pytest.param("people_ahead_display_table", 4, id="people_ahead"),
        pytest.param("frequency_display_table", 5, id="frequency"),
    ],
)
def test_style_display_table_aligns_columns_and_formats_floats(
    table_attr: str,
    numeric_column_count: int,
) -> None:
    sample = generate_clinic_sample(ClinicSampleInput(settings=Settings(), sample_size=80))
    table = getattr(sample, table_attr)
    longest_label = int(table.iloc[:, 0].astype(str).str.len().max())
    expected_min_width = f"min-width: {max(280, longest_label * 10 + 24)}px"

    rendered = style_display_table(table).to_html()

    assert "#T_" in rendered
    assert "th > div" in rendered
    assert ".MathJax" in rendered
    assert "th.col0" in rendered
    assert "text-align: center !important" in rendered
    assert expected_min_width in rendered
    for column_index in range(1, numeric_column_count + 1):
        assert f"th.col{column_index}" in rendered
        assert f"td.col{column_index}" in rendered
    if table_attr == "frequency_display_table":
        assert f"{table['$x_k$'].iloc[0]:.2f}" in rendered
