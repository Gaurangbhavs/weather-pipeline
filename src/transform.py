import glob
import json
import os
from datetime import datetime, timezone

import pandas as pd

from config import RAW_DATA_DIR

# Old column names from the API -> clear names we want
COLUMN_NAMES = {
    "time": "date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "rain_mm",
    "wind_speed_10m_max": "wind_max_kmh",
}


def load_city_file(filepath):
    """Read one raw JSON file and return a table with one row per day."""
    with open(filepath) as f:
        raw = json.load(f)

    df = pd.DataFrame(raw["daily"])

    # The city name is only in the file name, e.g. "ahmedabad_2026-08-28_to_..."
    filename = os.path.basename(filepath)
    city = filename.split("_")[0].title()
    df["city"] = city

    return df


def clean(df):
    """Rename columns, check dates, add a load timestamp, order columns."""
    df = df.rename(columns=COLUMN_NAMES)

    # Convert text to real dates (this raises an error if a date is invalid),
    # then write it back as clean "YYYY-MM-DD" text for the database
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # Record when this data was processed
    df["loaded_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Put the columns in a sensible order
    df = df[["city", "date", "temp_max_c", "temp_min_c",
             "rain_mm", "wind_max_kmh", "loaded_at"]]
    return df


def transform_all():
    """Load, clean and combine every raw file into one table."""
    files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "*.json")))
    print(f"Found {len(files)} files")

    tables = [clean(load_city_file(f)) for f in files]
    return pd.concat(tables, ignore_index=True)


def main():
    df = transform_all()

    print(df.head())
    print("Shape (rows, columns):", df.shape)
    print()
    print(df.dtypes)
    print()
    print("Missing values per column:")
    print(df.isnull().sum())
    print()
    print("Duplicate (city, date) rows:", df.duplicated(subset=["city", "date"]).sum())
    print()
    print("Rows per city:")
    print(df.groupby("city").size())


if __name__ == "__main__":
    main()