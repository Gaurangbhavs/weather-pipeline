# Weather Data Pipeline

An ETL pipeline that pulls daily weather data for five Indian cities from the
Open-Meteo API, cleans it with pandas, and loads it into a SQL database with
automated data quality checks.

## Status
- [x] Extract: fetch raw JSON from the API (Python, requests)
- [ ] Transform: clean and reshape data (pandas)
- [ ] Load: store in a SQL database
- [ ] Data quality checks (pytest)
- [ ] Daily scheduling (GitHub Actions)

## How to run
1. Create and activate a virtual environment
2. `pip install -r requirements.txt`
3. `python src/extract.py`