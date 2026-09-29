import os
import sqlite3
from collections.abc import Iterator
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict

LOCAL_DB_PATH = "habit_tracker.db"
VERCEL_DB_PATH = "/tmp/habit_tracker.db"
SERVER_TIMEZONE = ZoneInfo("Europe/London")
MILESTONES = {
    7: "One week strong",
    30: "You are on fire",
    100: "Legendary streak",
}


class HabitCreate(BaseModel):
    name: str


class HabitResponse(BaseModel):
    id: int
    name: str
    completed_today: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CheckinResponse(BaseModel):
    id: int
    habit_id: int
    checkin_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MilestoneResponse(BaseModel):
    days: int
    message: str


class StreakResponse(BaseModel):
    current_streak: int
    last_evaluated_date: date | None
    milestone: MilestoneResponse | None


class ResetResponse(BaseModel):
    message: str


def today_date() -> date:
    return datetime.now(tz=SERVER_TIMEZONE).date()


def get_milestone(streak: int) -> MilestoneResponse | None:
    message = MILESTONES.get(streak)
    if message is None:
        return None
    return MilestoneResponse(days=streak, message=message)


def get_db_path() -> str:
    default_path = VERCEL_DB_PATH if os.environ.get("VERCEL") else LOCAL_DB_PATH
    return os.environ.get("HABIT_TRACKER_DB", default_path)


def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    db_path = Path(get_db_path())
    if db_path.parent != Path("."):
        db_path.parent.mkdir(parents=True, exist_ok=True)

    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS habit_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                checkin_date TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id),
                UNIQUE (habit_id, checkin_date)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS streak_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                current_streak INTEGER NOT NULL DEFAULT 0,
                last_evaluated_date TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO streak_state (
                id,
                current_streak,
                last_evaluated_date
            )
            VALUES (1, 0, NULL)
            """
        )
        connection.commit()


def db_session() -> Iterator[sqlite3.Connection]:
    with get_db_connection() as connection:
        yield connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Habit Tracker API", lifespan=lifespan)

initialize_database()


@app.get("/", include_in_schema=False)
def read_frontend() -> FileResponse:
    return FileResponse(Path(__file__).with_name("index.html"))


@app.post("/habits", response_model=HabitResponse, status_code=201)
def create_habit(habit: HabitCreate) -> HabitResponse:
    habit_name = habit.name.strip()
    if not habit_name:
        raise HTTPException(status_code=400, detail="Habit name cannot be blank")

    with get_db_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO habits (name) VALUES (?)",
            (habit_name,),
        )
        connection.commit()
        row = connection.execute(
            """
            SELECT id, name, created_at
            FROM habits
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return HabitResponse(
        id=row["id"],
        name=row["name"],
        completed_today=False,
        created_at=row["created_at"],
    )


@app.get("/habits", response_model=list[HabitResponse])
def list_habits() -> list[HabitResponse]:
    today = today_date().isoformat()

    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                habits.id,
                habits.name,
                habits.created_at,
                habit_checkins.id IS NOT NULL AS completed_today
            FROM habits
            LEFT JOIN habit_checkins
                ON habit_checkins.habit_id = habits.id
                AND habit_checkins.checkin_date = ?
            ORDER BY habits.id
            """,
            (today,),
        ).fetchall()

    return [
        HabitResponse(
            id=row["id"],
            name=row["name"],
            completed_today=bool(row["completed_today"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]


@app.post(
    "/habits/{habit_id}/checkins",
    response_model=CheckinResponse,
    status_code=201,
)
def check_in_habit(habit_id: int) -> CheckinResponse:
    today = today_date().isoformat()

    with get_db_connection() as connection:
        habit = connection.execute(
            "SELECT id FROM habits WHERE id = ?",
            (habit_id,),
        ).fetchone()
        if habit is None:
            raise HTTPException(status_code=404, detail="Habit not found")

        connection.execute(
            """
            INSERT OR IGNORE INTO habit_checkins (habit_id, checkin_date)
            VALUES (?, ?)
            """,
            (habit_id, today),
        )
        connection.commit()

        row = connection.execute(
            """
            SELECT id, habit_id, checkin_date, created_at
            FROM habit_checkins
            WHERE habit_id = ? AND checkin_date = ?
            """,
            (habit_id, today),
        ).fetchone()

    return CheckinResponse(
        id=row["id"],
        habit_id=row["habit_id"],
        checkin_date=row["checkin_date"],
        created_at=row["created_at"],
    )


@app.get("/streak", response_model=StreakResponse)
def get_streak() -> StreakResponse:
    with get_db_connection() as connection:
        row = connection.execute(
            """
            SELECT current_streak, last_evaluated_date
            FROM streak_state
            WHERE id = 1
            """
        ).fetchone()

    if row is None:
        return StreakResponse(
            current_streak=0,
            last_evaluated_date=None,
            milestone=None,
        )

    current_streak = row["current_streak"]
    return StreakResponse(
        current_streak=current_streak,
        last_evaluated_date=row["last_evaluated_date"],
        milestone=get_milestone(current_streak),
    )


@app.post("/streak/evaluate-today", response_model=StreakResponse)
def evaluate_today() -> StreakResponse:
    today_value = today_date()
    today = today_value.isoformat()

    with get_db_connection() as connection:
        streak_row = connection.execute(
            """
            SELECT current_streak, last_evaluated_date
            FROM streak_state
            WHERE id = 1
            """
        ).fetchone()

        if streak_row is None:
            connection.execute(
                """
                INSERT INTO streak_state (
                    id,
                    current_streak,
                    last_evaluated_date
                )
                VALUES (1, 0, NULL)
                """
            )
            current_streak = 0
            last_evaluated_date = None
        else:
            current_streak = streak_row["current_streak"]
            last_evaluated_date = streak_row["last_evaluated_date"]

        if last_evaluated_date == today:
            return StreakResponse(
                current_streak=current_streak,
                last_evaluated_date=today_value,
                milestone=get_milestone(current_streak),
            )

        total_habits = connection.execute(
            "SELECT COUNT(*) FROM habits",
        ).fetchone()[0]
        completed_habits = connection.execute(
            """
            SELECT COUNT(*)
            FROM habit_checkins
            WHERE checkin_date = ?
            """,
            (today,),
        ).fetchone()[0]

        if total_habits > 0 and completed_habits == total_habits:
            current_streak += 1
        else:
            current_streak = 0

        connection.execute(
            """
            UPDATE streak_state
            SET current_streak = ?, last_evaluated_date = ?
            WHERE id = 1
            """,
            (current_streak, today),
        )
        connection.commit()

    return StreakResponse(
        current_streak=current_streak,
        last_evaluated_date=today_value,
        milestone=get_milestone(current_streak),
    )


@app.post("/reset", response_model=ResetResponse)
def reset_app() -> ResetResponse:
    with get_db_connection() as connection:
        connection.execute("DELETE FROM habit_checkins")
        connection.execute("DELETE FROM habits")
        connection.execute(
            """
            UPDATE streak_state
            SET current_streak = 0, last_evaluated_date = NULL
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO streak_state (
                id,
                current_streak,
                last_evaluated_date
            )
            VALUES (1, 0, NULL)
            """
        )
        connection.commit()

    return ResetResponse(message="Habit tracker reset")
