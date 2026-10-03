import sqlite3

import pandas as pd

DB_PATH = "data/weather.db"

QUERIES = {
    "1. Average daily max temperature per city (hottest first)": """
        SELECT city,
               ROUND(AVG(temp_max_c), 1) AS avg_max_temp_c
        FROM daily_weather
        GROUP BY city
        ORDER BY avg_max_temp_c DESC
    """,
    "2. The five rainiest days": """
        SELECT city, date, rain_mm
        FROM daily_weather
        ORDER BY rain_mm DESC
        LIMIT 5
    """,
    "3. Days with more than 1 mm of rain, per city": """
        SELECT city,
               COUNT(*) AS rainy_days
        FROM daily_weather
        WHERE rain_mm > 1
        GROUP BY city
        ORDER BY rainy_days DESC
    """,
    "4. Ahmedabad: 7-day rolling average of max temperature (latest 10 days)": """
        SELECT city,
               date,
               temp_max_c,
               ROUND(AVG(temp_max_c) OVER (
                   PARTITION BY city
                   ORDER BY date
                   ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
               ), 1) AS rolling_7d_avg
        FROM daily_weather
        WHERE city = 'Ahmedabad'
        ORDER BY date DESC
        LIMIT 10
    """,
}


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        for title, sql in QUERIES.items():
            print(title)
            result = pd.read_sql_query(sql, conn)
            print(result.to_string(index=False))
            print()
    finally:
        conn.close()


if __name__ == "__main__":
    main()