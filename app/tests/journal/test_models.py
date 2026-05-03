from datetime import date
from app.extensions.database import db
from app.journal.models import Entry
from app.users.models import User


def test_entry_update(db_session):
    user = User.query.filter_by(email='authenticated@example.com').first()
    assert user is not None

    # Create a new entry
    entry = Entry(title='Day 1', content='Today was great!', date=date(2024, 1, 1), user=user)
    db_session.add(entry)
    db_session.commit()

    # Update the entry's properties
    entry.title = 'Day 1 - Updated'
    entry.content = 'Today was even better!'
    db_session.commit()

    # Fetch again and check changes
    updated_entry = db_session.get(Entry, entry.id)
    assert updated_entry is not None
    assert updated_entry.title == 'Day 1 - Updated'
    assert updated_entry.content == 'Today was even better!'
    assert updated_entry.date == date(2024, 1, 1)

def test_entry_delete(client):
    user = User.query.filter_by(email='authenticated@example.com').first()
    assert user is not None

    # deletes entry
    entry = Entry(title='Day 2', content='Today was the best!', date=date(2026, 1, 2), user=user)
    db.session.add(entry)
    db.session.commit()

    entry.delete()

    deleted_entry = Entry.query.filter_by(title='Day 2').first()
    assert deleted_entry is None
