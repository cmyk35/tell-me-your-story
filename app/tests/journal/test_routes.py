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

def test_new_entry_content(client):
  # Returns h1 text
  response = client.get('/new')
  assert b'New Entry' in response.data

def test_single_entry_content(client):
  # Returns 'title' text of entry with valid entry id
  response = client.get('/entries/1')
  assert b'First day back' in response.data

