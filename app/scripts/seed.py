from app.app import create_app
from app.journal.models import Entry
from app.extensions.database import db
from datetime import date


if __name__ == '__main__':
  app = create_app()
  app.app_context().push()

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


added_count = 0

for entry in entries:
  entry_date = date.fromisoformat(entry["date"])
  existing_entry = Entry.query.filter_by(date=entry_date, title=entry["title"]).first()
  if existing_entry:
    continue

  new_entry = Entry(
      date=entry_date,
      title=entry["title"],
      content=entry["content"],
  )
  db.session.add(new_entry)
  added_count += 1

db.session.commit()
print(f"Seed complete. Added {added_count} new entries.")
