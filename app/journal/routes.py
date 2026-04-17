from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app
from app.extensions.database import db
from .models import Entry
from .services import create_entry_from_form, update_entry_from_form

blueprint = Blueprint('journal', __name__)


def get_entry_or_404(entry_id):
    found = db.session.get(Entry, entry_id)
    if found is None:
        abort(404)
    return found


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/entries")
def entries_list():
    page_number = request.args.get('page', 1, type=int)
    entries_pagination = Entry.query.paginate(page=page_number, per_page=current_app.config['ENTRIES_PER_PAGE'])
    return render_template("entries.html", entries_pagination=entries_pagination)

@blueprint.get("/entries/<int:entry_id>")
def entry(entry_id):
    found = get_entry_or_404(entry_id)
    return render_template("entry.html", entry=found)


@blueprint.post("/entries/<int:entry_id>")
def update_entry(entry_id):
    found = get_entry_or_404(entry_id)
    update_entry_from_form(found, request.form)
    return redirect(url_for("journal.entry", entry_id=found.id))


@blueprint.post("/entries/<int:entry_id>/delete")
def delete_entry(entry_id):
    found = get_entry_or_404(entry_id)
    found.delete()
    return redirect(url_for("journal.entries_list"))


@blueprint.get("/new")
def new_entry():
    return render_template("new.html")


@blueprint.post("/new")
def create_entry():
    entry = create_entry_from_form(request.form)
    return redirect(url_for("journal.entry", entry_id=entry.id))
