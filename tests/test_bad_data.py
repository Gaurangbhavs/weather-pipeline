import pandas as pd

from quality import (
    check_max_not_below_min,
    check_no_duplicates,
    check_no_missing_values,
    check_rain_and_wind,
    check_row_counts,
    check_temperature_range,
    run_all_checks,
)


def make_good_df():
    """A tiny, perfectly valid table: 1 city, 2 days."""
    return pd.DataFrame({
        "city": ["Delhi", "Delhi"],
        "date": ["2026-09-01", "2026-09-02"],
        "temp_max_c": [34.0, 35.0],
        "temp_min_c": [26.0, 27.0],
        "rain_mm": [0.0, 1.2],
        "wind_max_kmh": [10.0, 12.0],
    })


def test_good_data_passes_every_check():
    assert run_all_checks(make_good_df(), expected_days=2) == []


def test_missing_value_is_caught():
    df = make_good_df()
    df.loc[0, "rain_mm"] = float("nan")
    problems = check_no_missing_values(df)
    assert len(problems) == 1
    assert "rain_mm" in problems[0]


def test_duplicate_row_is_caught():
    df = make_good_df()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    assert len(check_no_duplicates(df)) == 1


def test_impossible_temperature_is_caught():
    df = make_good_df()
    df.loc[0, "temp_max_c"] = 99.0
    assert len(check_temperature_range(df)) == 1


def test_max_below_min_is_caught():
    df = make_good_df()
    df.loc[0, "temp_max_c"] = 20.0  # lower than the 26.0 minimum
    assert len(check_max_not_below_min(df)) == 1


def test_negative_rain_is_caught():
    df = make_good_df()
    df.loc[0, "rain_mm"] = -5.0
    problems = check_rain_and_wind(df)
    assert len(problems) == 1
    assert "negative rain" in problems[0]


def test_missing_day_is_caught():
    df = make_good_df().iloc[:1]  # keep only 1 of the 2 days
    problems = check_row_counts(df, expected_days=2)
    assert problems == ["Delhi has 1 rows, expected 2"]