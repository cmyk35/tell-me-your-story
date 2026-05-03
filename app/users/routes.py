from flask import Blueprint, render_template, request, redirect, url_for
from app.users.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from urllib.parse import urlsplit


blueprint = Blueprint('users', __name__)


def is_safe_next_url(target):
  parsed_target = urlsplit(target)
  return not parsed_target.scheme and not parsed_target.netloc


@blueprint.get('/register')
def get_register():
  return render_template('users/register.html')


@blueprint.post('/register')
def post_register():
  try:
    if request.form.get('password') != request.form.get('password_confirmation'):
      raise Exception('The password confirmation must match the password.')
    elif len(request.form.get('password')) < 5:
      raise Exception('The password must be at least 5 characters long.')
    elif User.query.filter_by(email=request.form.get('email')).first():
      raise Exception('The email address is already registered.')

    new_user = User(
      email=request.form.get('email'),
      password=generate_password_hash(request.form.get('password'))
    )
    new_user.save()

    return redirect(url_for('users.get_login'))
    
  except Exception as error_message:
    error = error_message or 'An error occurred while creating a user. Please make sure to enter valid data.'
    return render_template('users/register.html', error=error)

@blueprint.get('/login')
def get_login():
  return render_template('users/login.html')

@blueprint.post('/login')
def post_login():
  try:
    user = User.query.filter_by(email=request.form.get('email')).first()

    if not user:
      raise Exception('No user with the given email address was found.')
    elif not check_password_hash(user.password, request.form.get('password')):
      raise Exception('The password does not appear to be correct.')
    
    login_user(user)
    next_url = request.args.get('next')

    if next_url and is_safe_next_url(next_url):
      return redirect(next_url)

    return redirect(url_for('journal.index'))
    
  except Exception as error_message:
    error = error_message or 'An error occurred while logging in. Please verify your email and password.'
    return render_template('users/login.html', error=error)

@blueprint.post('/logout')
def logout():
  logout_user()
  
  return redirect(url_for('users.get_login'))
