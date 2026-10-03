import json
import os
from datetime import date, timedelta

import requests

from config import CITIES, API_URL, DAILY_FIELDS, RAW_DATA_DIR


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


def save_raw(city, data, start_date, end_date):
    """Save the raw API reply to a JSON file."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filename = f"{city.lower()}_{start_date}_to_{end_date}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {filepath}")


def main():
    # The archive API publishes data with a delay, so stop a week ago
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=29)  # 30 days in total

    start_date = start.isoformat()
    end_date = end.isoformat()

    print(f"Fetching weather from {start_date} to {end_date}")

    for city, coords in CITIES.items():
        try:
            data = fetch_city_weather(
                coords["lat"], coords["lon"], start_date, end_date
            )
            save_raw(city, data, start_date, end_date)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {city}: {e}")


if __name__ == "__main__":
    main()