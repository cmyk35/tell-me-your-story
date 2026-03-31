from flask import Flask, render_template, abort
from . import journal 
from app.extensions.database import db, migrate



def create_app():
  app = Flask(__name__, static_folder="assets", static_url_path="/assets")
  app.config.from_object('app.config')

  register_extensions(app)
  register_blueprints(app)

  return app

# Blueprints
def register_blueprints(app: Flask):
  app.register_blueprint(journal.routes.blueprint)

# Extensions
def register_extensions(app: Flask):
  db.init_app(app)
  migrate.init_app(app, db, compare_type=True)




