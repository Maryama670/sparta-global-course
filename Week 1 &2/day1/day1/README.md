# Habit Tracker

This project is a simple habit tracker.

It lets someone create a list of daily habits, tick them off when they are done, and keep a streak going when every habit is completed for the day.

For example, a user might add habits like:

- Drink water
- Read
- Exercise

Each day, they can tick off the habits they complete. At the end of the day, the app checks whether all habits were completed. If they were, the streak goes up by 1. If they were not, the streak resets to 0.

## What The App Can Do

- Add a new habit.
- Show all habits.
- Show whether each habit has been completed today.
- Mark a habit as completed for today.
- Check the user's current streak.
- Update the streak at the end of the day.
- Show encouraging milestone messages.

## Milestone Messages

The app celebrates these streaks:

- 7 days: `One week strong`
- 30 days: `You are on fire`
- 100 days: `Legendary streak`

## How To Start The App

Open a terminal in this project folder:

```bash
cd /Users/rishiram/centellic-FDE/week2/day1
```

If this is your first time running the project, create the Python environment:

```bash
python3 -m venv .venv
```

Turn on the Python environment.

Mac or Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Install the packages the app needs:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Start the app:

```bash
uvicorn habitTracker:app --reload
```

Then open this page in a browser:

```text
http://127.0.0.1:8000/
```

That opens the habit tracker screen.

You can also open the API testing page:

```text
http://127.0.0.1:8000/docs
```

The API testing page gives you buttons and forms for each endpoint.

## How To Deploy To Vercel

This project is ready to deploy to Vercel.

The files that make this work are:

- `app.py`: tells Vercel where the FastAPI app is.
- `requirements.txt`: tells Vercel which packages to install.
- `.vercelignore`: keeps local files like `.venv` and the local database out of the deployment.

To deploy from the terminal:

```bash
npm install -g vercel
vercel login
vercel
```

Follow the questions Vercel asks. When it finishes, it will give you a live website link.

For a production deployment, run:

```bash
vercel --prod
```

You can also deploy by pushing this project to GitHub and importing the repository in Vercel.

Important: this project uses SQLite. On Vercel, the app stores that SQLite file in temporary storage. That means it is fine for a demo, but the data can disappear when Vercel restarts or moves the app. For a real production habit tracker, use a hosted database instead.

## How To Use The App

### 1. Add A Habit

Use:

```text
POST /habits
```

Example habit:

```json
{
  "name": "Read"
}
```

The app will save the habit and give it an ID number.

### 2. See All Habits

Use:

```text
GET /habits
```

This shows every habit and whether it has been completed today.

Example result:

```json
[
  {
    "id": 1,
    "name": "Read",
    "completed_today": false,
    "created_at": "2026-09-14T12:00:00"
  }
]
```

### 3. Mark A Habit As Done

Use:

```text
POST /habits/1/checkins
```

In this example, `1` is the habit ID.

If the habit exists, the app marks it as completed for today. If you press it twice on the same day, it will not create a duplicate.

### 4. Check The Streak

Use:

```text
GET /streak
```

Example result:

```json
{
  "current_streak": 7,
  "last_evaluated_date": "2026-09-14",
  "milestone": {
    "days": 7,
    "message": "One week strong"
  }
}
```

### 5. Evaluate The Day

Use:

```text
POST /streak/evaluate-today
```

This is the end-of-day check.

The app looks at today's habits:

- If every habit is completed, the streak increases by 1.
- If one or more habits are incomplete, the streak resets to 0.
- If this check has already happened today, the app will not add to the streak again.

## Error Messages

The app uses common web status codes:

- `400 Bad Request`: the request is not valid. For example, trying to create a habit with a blank name.
- `404 Not Found`: the thing being requested does not exist. For example, trying to complete a habit ID that is not in the app.

These follow the official HTTP rules from RFC 9110:

- `400` means the request has a client-side mistake.
- `404` means the requested resource was not found.

References:

- https://www.rfc-editor.org/rfc/rfc9110.html#name-400-bad-request
- https://www.rfc-editor.org/rfc/rfc9110.html#name-404-not-found

## How To Run The Tests

The tests check that the app behaves correctly.

Run:

```bash
python -m pytest habitTrackerTest.py
```

Expected result:

```text
13 passed
```

## How To Run Code Checks

These commands check that the code is tidy and typed correctly:

```bash
python -m ruff check habitTracker.py habitTrackerTest.py
python -m mypy habitTracker.py
```

Both should pass.

## Important Notes

- This version is for one user only.
- There is no login system.
- Habits only have a name.
- Habits cannot be deleted in this version.
- The app uses today's date from the server.
- The server timezone is `Europe/London`.
- The streak only changes when `POST /streak/evaluate-today` is used.
