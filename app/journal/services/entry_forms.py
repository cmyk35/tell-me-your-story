from datetime import date

from app.journal.models import Entry


def parse_entry_date(raw_date):
    if not raw_date:
        return None
    return date.fromisoformat(raw_date)


def create_entry_from_form(form_data):
    entry = Entry(
        title=form_data.get("title", "").strip(),
        date=parse_entry_date(form_data.get("date")),
        content=form_data.get("content", "").strip(),
    )
    entry.save()
    return entry


def update_entry_from_form(entry, form_data):
    entry.date = parse_entry_date(form_data.get("date"))
    entry.title = form_data.get("title", "").strip()
    entry.content = form_data.get("content", "").strip()
    entry.save()
    return entry
