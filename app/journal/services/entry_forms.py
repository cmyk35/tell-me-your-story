from datetime import date

from app.journal.models import Entry


def parse_entry_date(raw_date):
    if not raw_date:
        return None
    return date.fromisoformat(raw_date)


def validate_entry_fields(title, date_value, content):
    title = title.strip()
    date_value = date_value.strip()
    content = content.strip()

    if not all([title, date_value, content]):
        raise ValueError("Please fill out all entry fields.")

    if len(title) > 80:
        raise ValueError("Title must be 80 characters or fewer.")

    if len(content) > 5000:
        raise ValueError("Content must be 5000 characters or fewer.")

    return {
        "title": title,
        "date": date_value,
        "content": content,
    }


def create_entry_from_form(form_data, user):
    cleaned_fields = validate_entry_fields(
        form_data.get("title", ""),
        form_data.get("date", ""),
        form_data.get("content", ""),
    )

    entry = Entry(
        title=cleaned_fields["title"],
        date=parse_entry_date(cleaned_fields["date"]),
        content=cleaned_fields["content"],
        user=user,
    )
    entry.save()
    return entry


def update_entry_from_form(entry, form_data):
    cleaned_fields = validate_entry_fields(
        form_data.get("title", ""),
        form_data.get("date", ""),
        form_data.get("content", ""),
    )
    parsed_date = parse_entry_date(cleaned_fields["date"])

    entry.date = parsed_date
    entry.title = cleaned_fields["title"]
    entry.content = cleaned_fields["content"]
    entry.save()
    return entry
