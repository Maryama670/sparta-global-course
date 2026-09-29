SPEC

# Habit Tracker API Spec

## Summary
Build a single-user habit tracker as a FastAPI REST API backed by SQLite. Users can add habits, retrieve habits, check off one habit at a time for the current server date, and call an end-of-day streak evaluation endpoint that increments or resets the streak.

## API And Data Model
Use JSON request/response bodies and ISO date strings.

Core tables:
- `habits`: `id`, `name`, `created_at`
- `habit_checkins`: `id`, `habit_id`, `checkin_date`, `created_at`
- `streak_state`: single-row state with `current_streak`, `last_evaluated_date`

Endpoints:
- `POST /habits`
  - Request: `{ "name": "Drink water" }`
  - Creates a habit.
  - Rejects empty names.

- `GET /habits`
  - Returns all habits with today’s completion state.
  - Response item: `{ "id": 1, "name": "Drink water", "completed_today": true }`

- `POST /habits/{habit_id}/checkins`
  - Checks off one habit for the server’s current local date.
  - Idempotent: checking the same habit twice today does not create duplicates.
  - Does not update the streak directly.

- `POST /streak/evaluate-today`
  - Evaluates whether all habits are checked for the current server date.
  - If all habits are checked and today has not already been evaluated, increments streak by `1`.
  - If not all habits are checked, resets streak to `0`.
  - Idempotent: calling it multiple times for the same date does not repeatedly increment.
  - Returns current streak plus milestone, if any.

- `GET /streak`
  - Returns current streak state and milestone, if applicable.
  - Response: `{ "current_streak": 7, "last_evaluated_date": "2026-09-14", "milestone": { "days": 7, "message": "One week strong" } }`

## Streak And Milestone Rules
- The global streak increases only when every habit in the database has been checked off for the evaluated date.
- A date can only be evaluated once.
- If the day is evaluated and not all habits are complete, the streak resets to `0`.
- No habit removal/archive behavior in v1.
- Fixed milestone messages:
  - `7`: `One week strong`
  - `30`: `You are on fire`
  - `100`: `Legendary streak`
- Milestone is returned only when `current_streak` exactly matches a milestone value.

## Implementation Plan
1. Set up a FastAPI app with SQLite connection handling and app startup table creation.
2. Create the `habits`, `habit_checkins`, and `streak_state` tables.
3. Add request and response models for habit creation, habit listing, check-ins, streak state, and milestone data.
4. Implement `POST /habits` with validation that rejects blank habit names.
5. Implement `GET /habits` so it returns all habits plus `completed_today` based on the server’s current date.
6. Implement `POST /habits/{habit_id}/checkins` so it validates the habit exists and creates one check-in for today only if it does not already exist.
7. Implement milestone lookup for streak values `7`, `30`, and `100`.
8. Implement `GET /streak` so it returns the current streak state and matching milestone, if one exists.
9. Implement `POST /streak/evaluate-today` so it checks whether all habits are complete today, increments or resets the streak, stores `last_evaluated_date`, and prevents double-counting the same date.
10. Add automated tests from the test plan.

## Test Plan
Use this section as the source of truth for automated tests.

- Add a habit and verify it appears in `GET /habits`.
- Reject habit creation with a blank name.
- Check off a habit and verify `completed_today` becomes `true`.
- Re-checking the same habit today should not duplicate the check-in.
- Verify check-in requests for a missing habit return an error.
- Verify `POST /streak/evaluate-today` increments streak only when all habits are checked.
- Verify `POST /streak/evaluate-today` resets streak when not all habits are checked.
- Verify evaluating the same date twice does not increment twice.
- Verify milestone messages appear at 7, 30, and 100 only.
- Verify `GET /streak` returns the current streak and matching milestone data.

## Assumptions
- Server local date is the source of truth for “today.”
- SQLite is the database.
- FastAPI is the implementation framework.
- Single-user only: no auth, user IDs, or ownership checks in v1.
- Habits are simple name-only records in v1.
