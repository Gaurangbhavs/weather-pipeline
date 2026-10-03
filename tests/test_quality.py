import pytest

from transform import transform_all
from quality import (
    check_max_not_below_min,
    check_no_duplicates,
    check_no_missing_values,
    check_rain_and_wind,
    check_row_counts,
    check_temperature_range,
    run_all_checks,
)


@pytest.fixture(scope="module")
def df():
    """Load and clean the real raw data once, and share it with every test."""
    return transform_all()


def test_no_missing_values(df):
    assert check_no_missing_values(df) == []


def test_no_duplicate_city_dates(df):
    assert check_no_duplicates(df) == []


def test_temperatures_are_believable(df):
    assert check_temperature_range(df) == []


def test_max_temperature_not_below_min(df):
    assert check_max_not_below_min(df) == []


def test_rain_and_wind_are_valid(df):
    assert check_rain_and_wind(df) == []


def test_every_city_has_30_days(df):
    assert check_row_counts(df, expected_days=30) == []


def test_all_checks_pass_together(df):
    assert run_all_checks(df) == []