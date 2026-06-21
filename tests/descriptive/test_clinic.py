from core import Settings
from descriptive import ClinicSampleInput, generate_clinic_sample


def test_generate_clinic_sample_builds_cohesive_dataframe() -> None:
    sample = generate_clinic_sample(ClinicSampleInput(settings=Settings(), sample_size=80))

    assert len(sample.clinic_data) == 80
    assert set(sample.clinic_data.columns) == {"value", "area", "delay_reason", "people_ahead"}
    assert len(sample.waiting_times) == 80
    assert sample.area_frequency_table["absolute_frequency"].sum() == 80
    assert sample.people_ahead_frequency_table["absolute_frequency"].sum() == 80


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
