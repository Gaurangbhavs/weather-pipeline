import glob
import json
import os
import sys
import time
from datetime import date, timedelta

import requests

from config import CITIES, API_URL, DAILY_FIELDS, RAW_DATA_DIR

MAX_ATTEMPTS = 3
WAIT_SECONDS = 2


def fetch_city_weather(lat, lon, start_date, end_date):
    """Ask the Open-Meteo API for one city's weather and return the reply."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_FIELDS),
        "timezone": "auto",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_with_retry(city, lat, lon, start_date, end_date):
    """Try up to MAX_ATTEMPTS times. Return the data, or None if all fail."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fetch_city_weather(lat, lon, start_date, end_date)
        except requests.exceptions.RequestException as e:
            print(f"  {city}: attempt {attempt}/{MAX_ATTEMPTS} failed: {e}")
            if attempt < MAX_ATTEMPTS:
                time.sleep(WAIT_SECONDS * attempt)
    return None


def clear_old_raw_files():
    """Delete JSON files left over from earlier runs."""
    for path in glob.glob(os.path.join(RAW_DATA_DIR, "*.json")):
        os.remove(path)


def save_raw(city, data, start_date, end_date):
    """Save the raw API reply to a JSON file."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filename = f"{city.lower()}_{start_date}_to_{end_date}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {filepath}")


def main():
    """Fetch every city. Return the list of cities that could not be fetched."""
    # The archive API publishes data with a delay, so stop a week ago
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=29)  # 30 days in total

    start_date = start.isoformat()
    end_date = end.isoformat()

    print(f"Fetching weather from {start_date} to {end_date}")
    clear_old_raw_files()

    failed = []
    for city, coords in CITIES.items():
        data = fetch_with_retry(
            city, coords["lat"], coords["lon"], start_date, end_date
        )
        if data is None:
            failed.append(city)
        else:
            save_raw(city, data, start_date, end_date)

    if failed:
        print(f"Could not fetch: {', '.join(failed)}")
    return failed


if __name__ == "__main__":
    failed_cities = main()
    sys.exit(1 if failed_cities else 0)