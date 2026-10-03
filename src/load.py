import os
import sqlite3

from transform import transform_all

DB_PATH = "data/weather.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS daily_weather (
    city          TEXT NOT NULL,
    date          TEXT NOT NULL,
    temp_max_c    REAL,
    temp_min_c    REAL,
    rain_mm       REAL,
    wind_max_kmh  REAL,
    loaded_at     TEXT NOT NULL,
    PRIMARY KEY (city, date)
)
"""

INSERT_ROW = """
INSERT OR REPLACE INTO daily_weather
    (city, date, temp_max_c, temp_min_c, rain_mm, wind_max_kmh, loaded_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""


def load(df):
    """Write the cleaned table into the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    rows = list(df.itertuples(index=False, name=None))

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(CREATE_TABLE)
        conn.executemany(INSERT_ROW, rows)
        conn.commit()

        total = conn.execute("SELECT COUNT(*) FROM daily_weather").fetchone()[0]
    finally:
        conn.close()

    print(f"Wrote {len(rows)} rows. Table now holds {total} rows.")


def main():
    df = transform_all()
    load(df)


if __name__ == "__main__":
    main()