import requests
import pytest

import extract


@pytest.fixture(autouse=True)
def no_waiting(monkeypatch):
    """Skip the real pauses between retries so tests run instantly."""
    monkeypatch.setattr(extract.time, "sleep", lambda seconds: None)


def test_retry_succeeds_after_two_failures(monkeypatch):
    calls = {"count": 0}

    def flaky(lat, lon, start_date, end_date):
        calls["count"] += 1
        if calls["count"] < 3:
            raise requests.exceptions.ConnectionError("network hiccup")
        return {"daily": "ok"}

    monkeypatch.setattr(extract, "fetch_city_weather", flaky)

    result = extract.fetch_with_retry("Delhi", 1, 2, "2026-09-01", "2026-09-30")

    assert result == {"daily": "ok"}
    assert calls["count"] == 3


def test_retry_gives_up_after_max_attempts(monkeypatch):
    calls = {"count": 0}

    def always_fails(lat, lon, start_date, end_date):
        calls["count"] += 1
        raise requests.exceptions.ConnectionError("server down")

    monkeypatch.setattr(extract, "fetch_city_weather", always_fails)

    result = extract.fetch_with_retry("Delhi", 1, 2, "2026-09-01", "2026-09-30")

    assert result is None
    assert calls["count"] == extract.MAX_ATTEMPTS


def test_old_raw_files_are_cleared(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "RAW_DATA_DIR", str(tmp_path))

    old_file = tmp_path / "old_city_2020-01-01_to_2020-01-30.json"
    old_file.write_text("{}")
    other_file = tmp_path / "notes.txt"
    other_file.write_text("keep me")

    extract.clear_old_raw_files()

    assert not old_file.exists()
    assert other_file.exists()