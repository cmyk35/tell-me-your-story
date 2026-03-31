import pytest
from os import environ
from datetime import date
from app.app import create_app
from flask_migrate import upgrade
from app.extensions.database import db
from app.journal.models import Entry


SEED_ENTRIES = [
  {"date": "2025-02-01", "title": "First day back", "content": "Semester started today, already three deadlines on the board."},
  {"date": "2025-02-05", "title": "Library afternoon", "content": "Spent four hours in muted, got maybe one hour of actual work done."},
  {"date": "2025-02-10", "title": "Group project kickoff", "content": "We picked projects today. I'm doing a journal app, surprise surprise."},
  {"date": "2025-02-15", "title": "Coffee shop session (again)", "content": "Tried working from a café. Would recommend, very productive vibes."},
  {"date": "2025-02-20", "title": "Almost done", "content": "Hand-in is next week."},
]


def seed_entries():
  for entry in SEED_ENTRIES:
    entry_date = date.fromisoformat(entry["date"])
    exists = Entry.query.filter_by(date=entry_date, title=entry["title"]).first()
    if exists:
      continue

    db.session.add(
      Entry(
        date=entry_date,
        title=entry["title"],
        content=entry["content"],
      )
    )

  db.session.commit()


@pytest.fixture
def app():
  environ['DATABASE_URL'] = 'sqlite://'
  app = create_app()

  with app.app_context():
    upgrade()
    seed_entries()
    yield app


@pytest.fixture
def client(app):
  return app.test_client()


@pytest.fixture
def db_session(app):
  yield db.session
  db.session.rollback()
  db.session.remove()
