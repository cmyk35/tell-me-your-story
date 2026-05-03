from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app
from app.extensions.database import db
from .models import Entry
from .services import create_entry_from_form, update_entry_from_form
from flask_login import login_required, current_user

blueprint = Blueprint('journal', __name__)


def get_entry_or_404(entry_id):
    found = Entry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if found is None:
        abort(404)
    return found


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/entries")
@login_required
def entries_list():
    page_number = request.args.get('page', 1, type=int)
    entries_pagination = Entry.query.filter_by(user_id=current_user.id).paginate(
        page=page_number,
        per_page=current_app.config['ENTRIES_PER_PAGE'],
    )
    return render_template("entries.html", entries_pagination=entries_pagination)

@blueprint.get("/entries/<int:entry_id>")
@login_required
def entry(entry_id):
    found = get_entry_or_404(entry_id)
    return render_template("entry.html", entry=found)


@blueprint.post("/entries/<int:entry_id>")
@login_required
def update_entry(entry_id):
    found = get_entry_or_404(entry_id)

    try:
        title = request.form.get("title", "").strip()
        date_value = request.form.get("date", "").strip()
        content = request.form.get("content", "").strip()

        if not all([title, date_value, content]):
            raise Exception("Please fill out all entry fields.")

        if len(title) > 80:
            raise Exception("Title must be 80 characters or fewer.")

        if len(content) > 5000:
            raise Exception("Content must be 5000 characters or fewer.")

        update_entry_from_form(found, request.form)
        return redirect(url_for("journal.entry", entry_id=found.id))
    except Exception as error_message:
        error = str(error_message) or "An error occurred while processing your entry. Please make sure to enter valid data."

        current_app.logger.info(f"Error updating an entry: {error}")

        return render_template("entry.html", entry=found, error=error)


@blueprint.post("/entries/<int:entry_id>/delete")
@login_required
def delete_entry(entry_id):
    found = get_entry_or_404(entry_id)
    found.delete()
    return redirect(url_for("journal.entries_list"))


@blueprint.get("/new")
@login_required
def new_entry():
    return render_template("new.html")


@blueprint.post("/new")
@login_required
def create_entry():
    try:
        title = request.form.get("title", "").strip()
        date_value = request.form.get("date", "").strip()
        content = request.form.get("content", "").strip()

        if not all([title, date_value, content]):
            raise Exception("Please fill out all entry fields.")

        if len(title) > 80:
            raise Exception("Title must be 80 characters or fewer.")

        if len(content) > 5000:
            raise Exception("Content must be 5000 characters or fewer.")

        entry = create_entry_from_form(request.form, current_user)
        return redirect(url_for("journal.entry", entry_id=entry.id))
    except Exception as error_message:
        error = str(error_message) or "An error occurred while processing your entry. Please make sure to enter valid data."

        current_app.logger.info(f"Error creating an entry: {error}")

        return render_template("new.html", error=error)
