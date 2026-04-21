from flask import Blueprint, render_template
from app.users.models import User

blueprint = Blueprint('users', __name__)

@blueprint.get('/register')
def get_register():
  return render_template('users/register.html')

@blueprint.post('/register')
def post_register():
  return 'User created'

@blueprint.get('/login')
def get_login():
  return render_template('users/login.html')

@blueprint.post('/login')
def post_login():
  return 'User logged in'

@blueprint.get('/logout')
def logout():
  return 'User logged out'

