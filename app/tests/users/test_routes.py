from werkzeug.security import check_password_hash

from app.users.models import User


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
