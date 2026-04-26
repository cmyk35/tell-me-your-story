from werkzeug.security import check_password_hash, generate_password_hash

from app.users.models import User


def test_get_register_renders_registration_form(client):
  response = client.get('/register')

  assert response.status_code == 200
  assert b'Register' in response.data
  assert b'Email' in response.data


def test_get_login_renders_login_form(client):
  response = client.get('/login')

  assert response.status_code == 200
  assert b'Login' in response.data
  assert b'Password' in response.data


def test_logged_out_nav_shows_login_and_register(client):
  response = client.get('/')

  assert response.status_code == 200
  assert b'Log in' in response.data
  assert b'Register' in response.data
  assert b'Log out' not in response.data


def test_authenticated_nav_shows_logout(authenticated_client):
  response = authenticated_client.get('/')

  assert response.status_code == 200
  assert b'Log out' in response.data
  assert b'Log in' not in response.data
  assert b'Register' not in response.data


def test_post_register_password_confirmation_mismatch_shows_error(client):
  response = client.post(
    '/register',
    data={
      'email': 'reader@example.com',
      'password': 'journalpass',
      'password_confirmation': 'differentpass',
    },
    follow_redirects=False,
  )

  assert response.status_code == 200
  assert b'The password confirmation must match the password.' in response.data
  assert User.query.filter_by(email='reader@example.com').first() is None


def test_post_register_duplicate_email_shows_error(client):
  existing_user = User(
    email='already@journal.com',
    password='pbkdf2:sha256:dummyhash',
  )
  existing_user.save()

  response = client.post(
    '/register',
    data={
      'email': 'already@journal.com',
      'password': 'journalpass',
      'password_confirmation': 'journalpass',
    },
    follow_redirects=False,
  )

  assert response.status_code == 200
  assert b'The email address is already registered.' in response.data
  assert User.query.filter_by(email='already@journal.com').count() == 1


def test_post_register_creates_user_with_hashed_password(client):
  response = client.post(
    '/register',
    data={
      'email': 'new@journal.com',
      'password': 'journalpass',
      'password_confirmation': 'journalpass',
    },
    follow_redirects=False,
  )

  created_user = User.query.filter_by(email='new@journal.com').first()

  assert response.status_code == 302
  assert created_user is not None
  assert created_user.password != 'journalpass'
  assert check_password_hash(created_user.password, 'journalpass')


def test_post_register_redirects_to_login_after_success(client):
  response = client.post(
    '/register',
    data={
      'email': 'redirect@journal.com',
      'password': 'journalpass',
      'password_confirmation': 'journalpass',
    },
    follow_redirects=False,
  )

  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login')


def test_post_login_invalid_credentials_renders_login_form(client):
  response = client.post(
    '/login',
    data={
      'email': 'missing@journal.com',
      'password': 'wrongpass',
    },
    follow_redirects=False,
  )

  assert response.status_code == 200
  assert b'Login' in response.data


def test_post_login_redirects_to_next_url(client):
  user = User(
    email='next@example.com',
    password=generate_password_hash('journalpass'),
  )
  user.save()

  response = client.post(
    '/login?next=/new',
    data={
      'email': 'next@example.com',
      'password': 'journalpass',
    },
    follow_redirects=False,
  )

  assert response.status_code == 302
  assert response.headers['Location'].endswith('/new')


def test_get_logout_redirects_to_login_and_clears_session(client):
  user = User(
    email='logout@example.com',
    password=generate_password_hash('journalpass'),
  )
  user.save()

  login_response = client.post(
    '/login',
    data={
      'email': 'logout@example.com',
      'password': 'journalpass',
    },
    follow_redirects=False,
  )

  assert login_response.status_code == 302

  with client.session_transaction() as session:
    assert session.get('_user_id') == str(user.id)

  response = client.get('/logout', follow_redirects=False)

  assert response.status_code == 302
  assert response.headers['Location'].endswith('/login')

  with client.session_transaction() as session:
    assert '_user_id' not in session
