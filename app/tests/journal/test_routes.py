from datetime import date

from app.extensions.database import db
from app.journal.models import Entry


### Simple routes tests ###

def test_index_success(client):
  # index page loads
  response = client.get('/')
  assert response.status_code == 200


def test_entries_success(client):
  # entries page loads
  response = client.get('/entries')
  assert response.status_code == 200

def test_new_success(client):
  # new entry page loads
  response = client.get('/new')
  assert response.status_code == 200

def test_single_entry_success(client):
  # entry page loads for a valid entry id
  response = client.get('/entries/1')
  assert response.status_code == 200

def test_entry_not_found(client):
  # entry page returns 404 for an unknown entry id
  response = client.get('/entries/999')
  assert response.status_code == 404

### HTML page content tests ###

def test_index_content(client):
  # Returns h1 text
  response = client.get('/')
  assert b'Mini Journal' in response.data

def test_entries_content(client):
  # Returns h1 text
  response = client.get('/entries')
  assert b'All Entries' in response.data

def test_entries_renders_entries(client):
  response = client.get('/entries')
  assert b'First day back' in response.data
  
def test_new_entry_content(client):
  # Returns h1 text
  response = client.get('/new')
  assert b'New Entry' in response.data

def test_single_entry_content(client):
  # Returns 'title' text of entry with valid entry id
  response = client.get('/entries/1')
  assert b'First day back' in response.data


def test_create_entry(client):
  response = client.post(
    '/new',
    data={
      'title': 'Created in test',
      'date': '2026-04-01',
      'content': 'This entry came from a POST request.',
    },
    follow_redirects=False,
  )

  created_entry = Entry.query.filter_by(title='Created in test').first()
  assert created_entry is not None
  assert created_entry.date == date(2026, 4, 1)
  assert response.status_code == 302
  assert response.headers['Location'].endswith(f'/entries/{created_entry.id}')


def test_update_entry(client):
  response = client.post(
    '/entries/1',
    data={
      'title': 'First day back updated',
      'date': '2025-02-02',
      'content': 'Updated content for the first entry.',
    },
    follow_redirects=False,
  )

  updated_entry = db.session.get(Entry, 1)
  assert updated_entry.title == 'First day back updated'
  assert updated_entry.date == date(2025, 2, 2)
  assert updated_entry.content == 'Updated content for the first entry.'
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/entries/1')


def test_delete_entry(client):
  response = client.post('/entries/1/delete', follow_redirects=False)

  deleted_entry = db.session.get(Entry, 1)
  assert deleted_entry is None
  assert response.status_code == 302
  assert response.headers['Location'].endswith('/entries')
