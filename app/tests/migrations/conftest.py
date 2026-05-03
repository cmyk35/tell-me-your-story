import pytest
from datetime import date
from os import environ

import sqlalchemy as sa
from flask_migrate import upgrade
from werkzeug.security import generate_password_hash

from app.app import create_app
from app.extensions.database import db

LEGACY_USER_EMAIL = "test@test.de"
LEGACY_USER_PASSWORD = "legacyjournal"

LEGACY_ENTRIES = [
  {"date": "2025-02-01", "title": "First day back", "content": "Semester started today, already three deadlines on the board."},
  {"date": "2025-02-05", "title": "Library afternoon", "content": "Spent four hours in muted, got maybe one hour of actual work done."},
  {"date": "2025-02-10", "title": "Group project kickoff", "content": "We picked projects today. I'm doing a journal app, surprise surprise."},
  {"date": "2025-02-15", "title": "Coffee shop session (again)", "content": "Tried working from a café. Would recommend, very productive vibes."},
  {"date": "2025-02-20", "title": "Almost done", "content": "Hand-in is next week."},
]


def seed_pre_migration_data():
  db.session.execute(
    sa.text("INSERT INTO user (email, password) VALUES (:email, :password)"),
    {
      "email": LEGACY_USER_EMAIL,
      "password": generate_password_hash(LEGACY_USER_PASSWORD),
    },
  )

  for entry in LEGACY_ENTRIES:
    db.session.execute(
      sa.text(
        "INSERT INTO entry (date, title, content) "
        "VALUES (:date, :title, :content)"
      ),
      {
        "date": date.fromisoformat(entry["date"]).isoformat(),
        "title": entry["title"],
        "content": entry["content"],
      },
    )

  db.session.commit()


@pytest.fixture
def app():
  environ["DATABASE_URL"] = "sqlite://"
  app = create_app()

  with app.app_context():
    upgrade(revision="76ac259eb0c0")
    seed_pre_migration_data()
    upgrade(revision="7c3a35dc02ab")
    yield app
    db.session.rollback()
    db.session.remove()
