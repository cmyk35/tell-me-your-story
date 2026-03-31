from flask import Blueprint, render_template, abort

blueprint = Blueprint('journal', __name__)

entries = [
    {"id": 1, "date": "2025-02-01", "title": "First day back",
     "content": "Semester started today, already three deadlines on the board."},
    {"id": 2, "date": "2025-02-05", "title": "Library afternoon",
     "content": "Spent four hours in muted, got maybe one hour of actual work done."},
    {"id": 3, "date": "2025-02-10", "title": "Group project kickoff",
     "content": "We picked projects today. I'm doing a journal app, surprise surprise."},
    {"id": 4, "date": "2025-02-15", "title": "Coffee shop session (again)",
     "content": "Tried working from a café. Would recommend, very productive vibes."},
    {"id": 5, "date": "2025-02-20", "title": "Almost done",
     "content": "Hand-in is next week."},
]


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/entries")
def entries_list():
    return render_template("entries.html", entries=entries)

@blueprint.route("/entries/<int:entry_id>")
def entry(entry_id):
    found = next((e for e in entries if e["id"] == entry_id), None)
    if found is None:
        abort(404)
    return render_template("entry.html", entry=found)


@blueprint.route("/new")
def new_entry():
    return render_template("new.html")
