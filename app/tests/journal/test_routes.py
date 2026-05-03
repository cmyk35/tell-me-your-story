import pytest
from datetime import date

from app.extensions.database import db
from app.journal.models import Entry
from app.users.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def other_user_entry(db_session):
  other_user = User(
    email='other@example.com',
    password=generate_password_hash('journalpass'),
  )
  db_session.add(other_user)
  db_session.commit()

  entry = Entry(
    date=date(2025, 3, 1),
    title='Private entry',
    content='Private content for another user.',
    user=other_user,
  )
  db_session.add(entry)
  db_session.commit()

  return entry


### Simple routes tests ###

def test_index_success(client):
  # index page loads
  response = client.get('/')
  assert response.status_code == 200


def test_entries_success(authenticated_client):
  # entries page loads
  response = authenticated_client.get('/entries')
  assert response.status_code == 200

def test_new_success(authenticated_client):
  # new entry page loads
  response = authenticated_client.get('/new')
  assert response.status_code == 200

def test_single_entry_success(authenticated_client):
  # entry page loads for a valid entry id
  response = authenticated_client.get('/entries/1')
  assert response.status_code == 200

def test_entry_not_found(authenticated_client):
  # entry page returns 404 for an unknown entry id
  response = authenticated_client.get('/entries/999')
  assert response.status_code == 404

### Unauthorized access tests ###

def test_entries_requires_authentication(client):
  response = client.get('/entries')
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fentries')


def test_new_requires_authentication(client):
  response = client.get('/new')
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fnew')


def test_single_entry_requires_authentication(client):
  response = client.get('/entries/1')
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fentries%2F1')


def test_create_entry_requires_authentication(client):
  response = client.post(
    '/new',
    data={
      'title': 'Created without auth',
      'date': '2026-04-01',
      'content': 'This should be blocked.',
    },
    follow_redirects=False,
  )

  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fnew')


def test_update_entry_requires_authentication(client):
  response = client.post(
    '/entries/1',
    data={
      'title': 'Updated without auth',
      'date': '2025-02-02',
      'content': 'This should be blocked.',
    },
    follow_redirects=False,
  )

  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fentries%2F1')


def test_delete_entry_requires_authentication(client):
  response = client.post('/entries/1/delete', follow_redirects=False)
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login?next=%2Fentries%2F1%2Fdelete')


### HTML page content tests ###

def test_index_content(client):
  # Returns h1 text
  response = client.get('/')
  assert b'Mini Journal' in response.data

def test_entries_content(authenticated_client):
  # Returns h1 text
  response = authenticated_client.get('/entries')
  assert b'All Entries' in response.data

def test_entries_renders_entries(authenticated_client):
  response = authenticated_client.get('/entries')
  assert b'First day back' in response.data

def test_entries_only_shows_current_users_entries(authenticated_client, other_user_entry):
  response = authenticated_client.get('/entries')

  assert response.status_code == 200
  assert b'First day back' in response.data
  assert b'Private entry' not in response.data
  
def test_new_entry_content(authenticated_client):
  # Returns h1 text
  response = authenticated_client.get('/new')
  assert b'New Entry' in response.data

def test_single_entry_content(authenticated_client):
  # Returns 'title' text of entry with valid entry id
  response = authenticated_client.get('/entries/1')
  assert b'First day back' in response.data

def test_single_entry_of_other_user_returns_404(authenticated_client, other_user_entry):
  response = authenticated_client.get(f'/entries/{other_user_entry.id}')

  assert response.status_code == 404

def test_update_entry_of_other_user_returns_404(authenticated_client, other_user_entry):
  response = authenticated_client.post(
    f'/entries/{other_user_entry.id}',
    data={
      'title': 'Updated private entry',
      'date': '2025-03-02',
      'content': 'This should not be allowed.',
    },
    follow_redirects=False,
  )

  assert response.status_code == 404

def test_delete_entry_of_other_user_returns_404(authenticated_client, other_user_entry):
  response = authenticated_client.post(f'/entries/{other_user_entry.id}/delete', follow_redirects=False)

  assert response.status_code == 404


def test_create_entry(authenticated_client):
  response = authenticated_client.post(
    '/new',
    data={
      'title': 'Created in test',
      'date': '2026-04-01',
      'content': 'This entry came from a POST request.',
    },
    follow_redirects=False,
  )

  created_entry = Entry.query.filter_by(title='Created in test').first()
  seeded_user = User.query.filter_by(email='authenticated@example.com').first()
  assert created_entry is not None
  assert seeded_user is not None
  assert created_entry.date == date(2026, 4, 1)
  assert created_entry.user_id == seeded_user.id
  assert response.status_code == 302
  assert response.headers['Location'].endswith(f'/entries/{created_entry.id}')


def test_update_entry(authenticated_client):
  response = authenticated_client.post(
    '/entries/1',
    data={
      'title': 'First day back updated',
      'date': '2025-02-02',
      'content': 'Updated content for the first entry.',
    },
    follow_redirects=False,
  )

  updated_entry = db.session.get(Entry, 1)
  seeded_user = User.query.filter_by(email='authenticated@example.com').first()
  assert seeded_user is not None
  assert updated_entry.title == 'First day back updated'
  assert updated_entry.date == date(2025, 2, 2)
  assert updated_entry.content == 'Updated content for the first entry.'
  assert updated_entry.user_id == seeded_user.id
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/entries/1')


def test_delete_entry(authenticated_client):
  response = authenticated_client.post('/entries/1/delete', follow_redirects=False)

  deleted_entry = db.session.get(Entry, 1)
  assert deleted_entry is None
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/entries')


def test_create_entry_missing_title_shows_error_and_logs(authenticated_client, caplog):
  with caplog.at_level('INFO', logger=authenticated_client.application.logger.name):
    response = authenticated_client.post(
      '/new',
      data={
        'title': '',
        'date': '2026-04-01',
        'content': 'This entry should not be created.',
      },
      follow_redirects=False,
    )

  assert response.status_code == 200
  assert b'Please fill out all entry fields.' in response.data
  assert Entry.query.filter_by(content='This entry should not be created.').first() is None
  assert 'Error creating an entry: Please fill out all entry fields.' in caplog.text


def test_create_entry_title_too_long_shows_error(authenticated_client):
  response = authenticated_client.post(
    '/new',
    data={
      'title': 'A' * 81,
      'date': '2026-04-01',
      'content': 'This entry should not be created.',
    },
    follow_redirects=False,
  )

  assert response.status_code == 200
  assert b'Title must be 80 characters or fewer.' in response.data
  assert Entry.query.filter_by(content='This entry should not be created.').first() is None


def test_update_entry_missing_content_shows_error(authenticated_client):
  response = authenticated_client.post(
    '/entries/1',
    data={
      'title': 'First day back still the same',
      'date': '2025-02-02',
      'content': '',
    },
    follow_redirects=False,
  )

  unchanged_entry = db.session.get(Entry, 1)
  assert response.status_code == 200
  assert b'Please fill out all entry fields.' in response.data
  assert unchanged_entry.title == 'First day back'
  assert unchanged_entry.date == date(2025, 2, 1)
  assert unchanged_entry.content == 'Semester started today, already three deadlines on the board.'


def test_update_entry_invalid_date_shows_error(authenticated_client):
  response = authenticated_client.post(
    '/entries/1',
    data={
      'title': 'First day back still the same',
      'date': '2025-13-40',
      'content': 'Updated content that should not save.',
    },
    follow_redirects=False,
  )

  unchanged_entry = db.session.get(Entry, 1)
  assert response.status_code == 200
  assert b'month must be in 1..12' in response.data
  assert unchanged_entry.title == 'First day back'
  assert unchanged_entry.date == date(2025, 2, 1)
  assert unchanged_entry.content == 'Semester started today, already three deadlines on the board.'
