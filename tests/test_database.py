import os
import sqlite3

import pytest

from load import CREATE_TABLE, DB_PATH, INSERT_ROW

GOOD_ROW = ("Delhi", "2026-09-01", 34.0, 26.0, 0.0, 10.0, "2026-10-03 10:00:00")

PLAIN_INSERT = "INSERT INTO daily_weather VALUES (?, ?, ?, ?, ?, ?, ?)"


@pytest.fixture
def memory_db():
    """A fresh, empty database that lives only in memory."""
    conn = sqlite3.connect(":memory:")
    conn.execute(CREATE_TABLE)
    yield conn
    conn.close()


def test_primary_key_blocks_duplicate_city_date(memory_db):
    memory_db.execute(PLAIN_INSERT, GOOD_ROW)
    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute(PLAIN_INSERT, GOOD_ROW)


def test_city_is_required(memory_db):
    row_without_city = (None,) + GOOD_ROW[1:]
    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute(PLAIN_INSERT, row_without_city)


def test_load_is_idempotent(memory_db):
    memory_db.executemany(INSERT_ROW, [GOOD_ROW])
    memory_db.executemany(INSERT_ROW, [GOOD_ROW])  # load the same row twice
    count = memory_db.execute("SELECT COUNT(*) FROM daily_weather").fetchone()[0]
    assert count == 1


needs_real_db = pytest.mark.skipif(
    not os.path.exists(DB_PATH), reason="run load.py first to create the database"
)


@needs_real_db
def test_real_database_has_150_rows():
    conn = sqlite3.connect(DB_PATH)
    try:
        count = conn.execute("SELECT COUNT(*) FROM daily_weather").fetchone()[0]
    finally:
        conn.close()
    assert count == 150


@needs_real_db
def test_real_database_has_30_days_per_city():
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT city, COUNT(*) FROM daily_weather GROUP BY city"
        ).fetchall()
    finally:
        conn.close()
    assert len(rows) == 5
    assert all(count == 30 for _, count in rows)