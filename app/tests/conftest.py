import pytest
from os import environ
from datetime import date
import re
from app.app import create_app
from flask_migrate import upgrade
from app.extensions.database import db
from app.journal.models import Entry
from app.users.models import User
from werkzeug.security import generate_password_hash


SEED_ENTRIES = [
  {"date": "2025-02-01", "title": "First day back", "content": "Semester started today, already three deadlines on the board."},
  {"date": "2025-02-05", "title": "Library afternoon", "content": "Spent four hours in muted, got maybe one hour of actual work done."},
  {"date": "2025-02-10", "title": "Group project kickoff", "content": "We picked projects today. I'm doing a journal app, surprise surprise."},
  {"date": "2025-02-15", "title": "Coffee shop session (again)", "content": "Tried working from a café. Would recommend, very productive vibes."},
  {"date": "2025-02-20", "title": "Almost done", "content": "Hand-in is next week."},
]

CSRF_TOKEN_PATTERN = re.compile(r'name="csrf_token"[^>]*value="([^"]+)"')


def extract_csrf_token(response_text):
  match = CSRF_TOKEN_PATTERN.search(response_text)
  assert match is not None, 'CSRF token not found in response HTML'
  return match.group(1)


def seed_entries():
  user = User.query.filter_by(email='authenticated@example.com').first()
  if user is None:
    user = User(
      email='authenticated@example.com',
      password=generate_password_hash('journalpass'),
    )
    db.session.add(user)
    db.session.commit()

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
        user=user,
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

@pytest.fixture
def authenticated_client(client):
  login_page = client.get('/login')
  csrf_token = extract_csrf_token(login_page.get_data(as_text=True))

  login_response = client.post(
    '/login',
    data={
      'csrf_token': csrf_token,
      'email': 'authenticated@example.com',
      'password': 'journalpass',
    },
    follow_redirects=False,
  )

  assert login_response.status_code == 302
  return client


@pytest.fixture
def csrf_token():
  def _csrf_token(client, path='/login'):
    response = client.get(path)
    return extract_csrf_token(response.get_data(as_text=True))

  return _csrf_token
