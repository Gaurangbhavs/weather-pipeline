import pandas as pd

from config import CITIES
from quality import check_all_cities_present, run_all_checks
from transform import transform_all


def make_df(cities):
    return pd.DataFrame({"city": cities})


def test_all_expected_cities_present_passes():
    df = make_df(["Delhi", "Mumbai"])
    assert check_all_cities_present(df, ["Delhi", "Mumbai"]) == []


def test_missing_city_is_caught():
    df = make_df(["Delhi"])
    problems = check_all_cities_present(df, ["Delhi", "Mumbai"])
    assert problems == ["Missing city data for: Mumbai"]


def test_unexpected_city_is_caught():
    df = make_df(["Delhi", "Pune"])
    problems = check_all_cities_present(df, ["Delhi"])
    assert problems == ["Unexpected city in data: Pune"]


def test_real_data_has_all_configured_cities():
    df = transform_all()
    assert run_all_checks(df, expected_cities=list(CITIES.keys())) == []


def test_a_whole_missing_city_is_noticed():
    """The gap we found: all other cities look perfect, but one is gone."""
    df = transform_all()
    df = df[df["city"] != "Bengaluru"]
    problems = run_all_checks(df, expected_cities=list(CITIES.keys()))
    assert problems == ["Missing city data for: Bengaluru"]