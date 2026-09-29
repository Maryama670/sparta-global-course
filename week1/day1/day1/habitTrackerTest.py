import importlib
import os
import sqlite3
import sys
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "habit_tracker_test.db"
    monkeypatch.setenv("HABIT_TRACKER_DB", str(db_path))

    if "habitTracker" in sys.modules:
        app_module = importlib.reload(sys.modules["habitTracker"])
    else:
        app_module = importlib.import_module("habitTracker")

    return TestClient(app_module.app)


def create_habit(client, name="Drink water"):
    response = client.post("/habits", json={"name": name})
    assert response.status_code in (200, 201), response.text
    return response.json()


def get_habits(client):
    response = client.get("/habits")
    assert response.status_code == 200, response.text
    return response.json()


def get_streak(client):
    response = client.get("/streak")
    assert response.status_code == 200, response.text
    return response.json()


def evaluate_today(client):
    response = client.post("/streak/evaluate-today")
    assert response.status_code == 200, response.text
    return response.json()


def reset_app(client):
    response = client.post("/reset")
    assert response.status_code == 200, response.text
    return response.json()


def db_connect():
    return sqlite3.connect(os.environ["HABIT_TRACKER_DB"])


def today_date():
    return datetime.now().astimezone().date()


def test_add_habit_and_retrieve_it(client):
    created = create_habit(client, "Read")

    habits = get_habits(client)

    assert len(habits) == 1
    assert habits[0]["id"] == created["id"]
    assert habits[0]["name"] == "Read"
    assert habits[0]["completed_today"] is False


def test_reject_blank_habit_name(client):
    response = client.post("/habits", json={"name": "   "})

    assert response.status_code in (400, 422)


def test_check_off_habit_marks_it_completed_today(client):
    habit = create_habit(client, "Exercise")

    response = client.post(f"/habits/{habit['id']}/checkins")

    assert response.status_code in (200, 201), response.text
    habits = get_habits(client)
    assert habits[0]["completed_today"] is True


def test_rechecking_same_habit_today_does_not_duplicate_checkin(client):
    habit = create_habit(client, "Journal")

    first = client.post(f"/habits/{habit['id']}/checkins")
    second = client.post(f"/habits/{habit['id']}/checkins")

    assert first.status_code in (200, 201), first.text
    assert second.status_code in (200, 201), second.text
    with db_connect() as connection:
        checkin_count = connection.execute(
            "SELECT COUNT(*) FROM habit_checkins WHERE habit_id = ?",
            (habit["id"],),
        ).fetchone()[0]
    assert checkin_count == 1


def test_checking_in_missing_habit_returns_error(client):
    response = client.post("/habits/999999/checkins")

    assert response.status_code == 404


def test_evaluate_today_increments_streak_when_all_habits_are_complete(client):
    first = create_habit(client, "Read")
    second = create_habit(client, "Exercise")

    client.post(f"/habits/{first['id']}/checkins")
    client.post(f"/habits/{second['id']}/checkins")
    result = evaluate_today(client)

    assert result["current_streak"] == 1
    assert result["last_evaluated_date"] == today_date().isoformat()


def test_evaluate_today_resets_streak_when_not_all_habits_are_complete(client):
    create_habit(client, "Read")
    yesterday = (today_date() - timedelta(days=1)).isoformat()

    with db_connect() as connection:
        connection.execute("DELETE FROM streak_state")
        connection.execute(
            """
            INSERT INTO streak_state (current_streak, last_evaluated_date)
            VALUES (?, ?)
            """,
            (5, yesterday),
        )
        connection.commit()

    result = evaluate_today(client)

    assert result["current_streak"] == 0
    assert result["last_evaluated_date"] == today_date().isoformat()


def test_evaluating_same_date_twice_does_not_increment_twice(client):
    habit = create_habit(client, "Read")
    client.post(f"/habits/{habit['id']}/checkins")

    first_result = evaluate_today(client)
    second_result = evaluate_today(client)

    assert first_result["current_streak"] == 1
    assert second_result["current_streak"] == 1


@pytest.mark.parametrize(
    ("streak_value", "expected_message"),
    [
        (7, "One week strong"),
        (30, "You are on fire"),
        (100, "Legendary streak"),
    ],
)
def test_milestone_messages_appear_at_fixed_streak_values(
    client, streak_value, expected_message
):
    with db_connect() as connection:
        connection.execute("DELETE FROM streak_state")
        connection.execute(
            """
            INSERT INTO streak_state (current_streak, last_evaluated_date)
            VALUES (?, ?)
            """,
            (streak_value, today_date().isoformat()),
        )
        connection.commit()

    result = get_streak(client)

    assert result["current_streak"] == streak_value
    assert result["milestone"] == {
        "days": streak_value,
        "message": expected_message,
    }


def test_get_streak_returns_current_streak_and_no_milestone_when_not_matched(client):
    with db_connect() as connection:
        connection.execute("DELETE FROM streak_state")
        connection.execute(
            """
            INSERT INTO streak_state (current_streak, last_evaluated_date)
            VALUES (?, ?)
            """,
            (3, today_date().isoformat()),
        )
        connection.commit()

    result = get_streak(client)

    assert result["current_streak"] == 3
    assert result["last_evaluated_date"] == today_date().isoformat()
    assert result["milestone"] is None


def test_reset_clears_habits_checkins_and_streak(client):
    habit = create_habit(client, "Read")
    client.post(f"/habits/{habit['id']}/checkins")
    evaluate_today(client)

    result = reset_app(client)

    assert result["message"] == "Habit tracker reset"
    assert get_habits(client) == []
    assert get_streak(client) == {
        "current_streak": 0,
        "last_evaluated_date": None,
        "milestone": None,
    }
    with db_connect() as connection:
        checkin_count = connection.execute(
            "SELECT COUNT(*) FROM habit_checkins"
        ).fetchone()[0]
    assert checkin_count == 0
