# Mini Journal

Mini Journal is a small Flask-based journal app for **Web Technologies Basics (SE_19)**.

Live app: https://tell-me-your-story.onrender.com

The app is server-rendered with Jinja templates, backed by SQLite/PostgreSQL-compatible SQLAlchemy models, and includes user accounts so each user only sees and manages their own entries.

## Features

- user registration and login
- create, edit, and delete journal entries
- per-user entry ownership and access control
- server-side rendering for all pages
- a small client-side JavaScript character counter on the entry forms
- responsive layout for mobile and larger screens
- CSRF protection for form submissions
- database migrations for schema changes

## Routes

- `/` - home page
- `/register` - create an account
- `/login` - log in
- `/logout` - log out
- `/entries` - list the current user's entries
- `/entries/<id>` - edit a single entry
- `/new` - create a new entry

## Tech Stack

- Flask
- Jinja2
- Flask-Login
- Flask-WTF / CSRF protection
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- SQLite for local development
- Gunicorn for production

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Set the required environment variables in a `.env` file:
   - `SECRET_KEY`
   - `DATABASE_URL`
4. Run the app:
   - `python run.py`
5. Open:
   - `http://127.0.0.1:5001`

If you want to use a different port:

- `PORT=8000 python run.py`

## Environment Variables

- `SECRET_KEY` - Flask session and CSRF secret
- `DATABASE_URL` - database connection string
- `FLASK_DEBUG` - optional local debug toggle
- `FLASK_APP` - points to `run.py`

## Responsive Layout

The site uses a simple responsive layout:

- below `600px`: compact navigation
- `600px` and up: navigation gets more spacing
- `900px` and up: entry cards switch to a 2-column grid

## Testing

The repository includes tests for:

- user authentication routes
- journal CRUD routes
- ownership and access control
- migration behavior

## Notes

- The app is intentionally simple and template-driven rather than built on a frontend framework.
- The deployed production version is hosted on Render at the link above.
