from flask import Blueprint, render_template, abort
from app.extensions.database import db
from .models import Entry

blueprint = Blueprint('journal', __name__)


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/entries")
def entries_list():
    all_entries = Entry.query.all()
    return render_template("entries.html", entries=all_entries)

@blueprint.route("/entries/<int:entry_id>")
def entry(entry_id):
    found = db.session.get(Entry, entry_id)
    if found is None:
        abort(404)
    return render_template("entry.html", entry=found)


@blueprint.route("/new")
def new_entry():
    return render_template("new.html")
