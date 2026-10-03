# Weather Data Pipeline

An ETL pipeline that pulls daily weather data for five Indian cities from the
Open-Meteo API, cleans it with pandas, and loads it into a SQL database with
automated data quality checks.

## Status
- [x] Extract: fetch raw JSON from the API (Python, requests)
- [x] Transform: clean and reshape data (pandas)
- [x] Load: store in a SQL database
- [ ] Data quality checks (pytest)
- [ ] Daily scheduling (GitHub Actions)

## How to run
1. Create and activate a virtual environment
2. `pip install -r requirements.txt`
3. `python src/extract.py`
## Example insights from the data
- Chennai had the highest average daily max temperature (34.3 C) over the 30-day window
- Mumbai had more than 1 mm of rain on 29 of 30 days; Ahmedabad on only 12
- Ahmedabad's rainiest day was 2026-09-14 with 58.1 mm