# Cities to pull weather data for
CITIES = {
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
}

# The web address of the weather API (archive = past weather)
API_URL = "https://archive-api.open-meteo.com/v1/archive"

# The daily measurements we want for each city
DAILY_FIELDS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]

# The folder where raw API responses will be saved
RAW_DATA_DIR = "data/raw"