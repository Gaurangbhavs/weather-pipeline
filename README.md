# Weather Data Pipeline

[![Daily weather pipeline](https://github.com/Gaurangbhavs/weather-pipeline/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Gaurangbhavs/weather-pipeline/actions/workflows/pipeline.yml)

An automated ETL pipeline that pulls daily weather data for five Indian cities
from the [Open-Meteo](https://open-meteo.com) API, cleans it with pandas, validates it
with automated data quality checks, and loads it into a SQLite database. It runs
every day on GitHub Actions, and the tests run on every push.

## How it works

```
Open-Meteo API --> extract --> transform --> quality checks --> load --> SQLite
                  (requests)    (pandas)      (6 checks)       (SQL)   weather.db
```

If any quality check fails, the pipeline exits with a non-zero code and
**nothing is loaded**, so bad data never reaches the database.

## Tech stack
- Python, pandas, requests
- SQL (SQLite)
- pytest (27 tests)
- GitHub Actions (daily schedule and CI)

## Features
- **Reliable extraction:** retries failed requests up to 3 times, clears stale files
  on each run, and stops if any city cannot be fetched
- **Data cleaning:** consistent column names with units, validated dates, a UTC
  `loaded_at` timestamp on every row
- **Data quality checks:** no missing values, no duplicate (city, date) rows,
  believable temperature ranges, max temperature never below min, valid rain and
  wind values, 30 days for every city, and all configured cities present
- **Idempotent load:** a primary key on (city, date) with `INSERT OR REPLACE`, so
  re-running the pipeline never creates duplicates
- **Tested:** negative tests that feed in deliberately bad data, database constraint
  tests, and retry logic tested with mocked network failures

## Project structure
```
src/
  config.py      cities, API address and settings
  extract.py     fetch raw JSON (with retries)
  transform.py   reshape, clean and combine into one table
  quality.py     data quality checks
  load.py        create the table and load rows into SQLite
  pipeline.py    runs all stages in order; stops if a check fails
  queries.py     example SQL queries
tests/           pytest tests
.github/workflows/pipeline.yml   daily schedule and CI
```

## How to run it

```
python -m venv venv
venv\Scripts\activate          # Windows (on Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python src/pipeline.py         # run the full pipeline
pytest                         # run the tests
python src/queries.py          # run the example SQL queries
```

## Example insights (28 Aug to 26 Sep 2026)
- Chennai had the highest average daily maximum temperature (34.3 C)
- Mumbai had more than 1 mm of rain on 29 of 30 days; Ahmedabad on only 12
- Ahmedabad's rainiest day was 2026-09-14 with 58.1 mm

## Limitations and next steps
- SQLite is a single local file. Each GitHub Actions run rebuilds it from the
  last 30 days of data, so the history is not kept permanently.
- The archive API publishes data with a delay, so the window ends a week before today.
- Possible next steps: load into a hosted database such as PostgreSQL, add
  an orchestration tool such as Airflow, and add more cities and weather fields.