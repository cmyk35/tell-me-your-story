from app.journal.models import Entry
from app.users.models import User

EXPECTED_ENTRY_COUNT = 5
LEGACY_EMAIL = "test@test.de"


def test_migration_backfills_legacy_entries(db_session):
  legacy_user = User.query.filter_by(email=LEGACY_EMAIL).first()

  assert legacy_user is not None
  assert Entry.query.count() == EXPECTED_ENTRY_COUNT
  assert Entry.query.filter_by(user_id=None).count() == 0

  entries = Entry.query.order_by(Entry.id).all()
  assert all(entry.user_id == legacy_user.id for entry in entries)


def test_migration_keeps_entry_user_relationship(db_session):
  entry = Entry.query.filter_by(title="First day back").first()

  assert entry is not None
  assert entry.user is not None
  assert entry.user.email == LEGACY_EMAIL
