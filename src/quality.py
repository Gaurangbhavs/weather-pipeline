# Limits for believable values
TEMP_LOW_C = -50
TEMP_HIGH_C = 60
WIND_HIGH_KMH = 250


def check_no_missing_values(df):
    """No column may contain empty values."""
    problems = []
    for column, count in df.isnull().sum().items():
        if count > 0:
            problems.append(f"{count} missing value(s) in column '{column}'")
    return problems


def check_no_duplicates(df):
    """Each city may appear only once per date."""
    count = df.duplicated(subset=["city", "date"]).sum()
    if count > 0:
        return [f"{count} duplicate (city, date) row(s)"]
    return []


def check_temperature_range(df):
    """Temperatures must be within a believable range."""
    problems = []
    for column in ["temp_max_c", "temp_min_c"]:
        bad = df[(df[column] < TEMP_LOW_C) | (df[column] > TEMP_HIGH_C)]
        if len(bad) > 0:
            problems.append(
                f"{len(bad)} row(s) where '{column}' is outside "
                f"{TEMP_LOW_C} to {TEMP_HIGH_C} C"
            )
    return problems


def check_max_not_below_min(df):
    """The day's highest temperature can't be lower than its lowest."""
    bad = df[df["temp_max_c"] < df["temp_min_c"]]
    if len(bad) > 0:
        return [f"{len(bad)} row(s) where temp_max_c is below temp_min_c"]
    return []


def check_rain_and_wind(df):
    """Rain can't be negative; wind can't be negative or absurdly high."""
    problems = []
    negative_rain = df[df["rain_mm"] < 0]
    if len(negative_rain) > 0:
        problems.append(f"{len(negative_rain)} row(s) with negative rain_mm")
    bad_wind = df[(df["wind_max_kmh"] < 0) | (df["wind_max_kmh"] > WIND_HIGH_KMH)]
    if len(bad_wind) > 0:
        problems.append(
            f"{len(bad_wind)} row(s) where wind_max_kmh is outside 0 to {WIND_HIGH_KMH}"
        )
    return problems


def check_row_counts(df, expected_days):
    """Every city must have exactly the expected number of days."""
    problems = []
    for city, count in df.groupby("city").size().items():
        if count != expected_days:
            problems.append(f"{city} has {count} rows, expected {expected_days}")
    return problems


def run_all_checks(df, expected_days=30):
    """Run every check and return one combined list of problems."""
    problems = []
    problems += check_no_missing_values(df)
    problems += check_no_duplicates(df)
    problems += check_temperature_range(df)
    problems += check_max_not_below_min(df)
    problems += check_rain_and_wind(df)
    problems += check_row_counts(df, expected_days)
    return problems