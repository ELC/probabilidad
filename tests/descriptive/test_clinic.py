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


def test_style_display_table_centers_headers_and_formats_floats() -> None:
    sample = generate_clinic_sample(ClinicSampleInput(settings=Settings(), sample_size=80))

    rendered = style_display_table(sample.frequency_display_table).to_html()

    assert "text-align: center !important" in rendered
    assert "min-width: 240px" in rendered
    assert f"{sample.frequency_display_table['$x_k$'].iloc[0]:.2f}" in rendered
