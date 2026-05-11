import pytest
from datetime import date

from app.journal.services.entry_forms import (
  create_entry_from_form,
  parse_entry_date,
  validate_entry_fields,
)
from app.users.models import User


def test_parse_entry_date_returns_date_for_valid_iso_string():
  result = parse_entry_date('2026-04-01')

  assert result == date(2026, 4, 1)


def test_parse_entry_date_returns_none_for_empty_string():
  result = parse_entry_date('')

  assert result is None


def test_parse_entry_date_returns_none_for_none():
  result = parse_entry_date(None)

  assert result is None


def test_parse_entry_date_raises_value_error_for_invalid_date():
  with pytest.raises(ValueError):
    parse_entry_date('2026-99-99')


def test_validate_entry_fields_returns_cleaned_values():
  result = validate_entry_fields(
    '  My title  ',
    '2026-04-01',
    '  My content  ',
  )

  assert result == {
    'title': 'My title',
    'date': '2026-04-01',
    'content': 'My content',
  }


def test_validate_entry_fields_rejects_missing_title():
  with pytest.raises(ValueError, match='Please fill out all entry fields.'):
    validate_entry_fields('', '2026-04-01', 'Some content')


def test_validate_entry_fields_rejects_title_over_80_chars():
  with pytest.raises(ValueError, match='Title must be 80 characters or fewer.'):
    validate_entry_fields('A' * 81, '2026-04-01', 'Some content')


def test_validate_entry_fields_accepts_title_with_exactly_80_chars():
  result = validate_entry_fields('A' * 80, '2026-04-01', 'Some content')

  assert result['title'] == 'A' * 80


def test_validate_entry_fields_rejects_content_over_5000_chars():
  with pytest.raises(ValueError, match='Content must be 5000 characters or fewer.'):
    validate_entry_fields('Title', '2026-04-01', 'A' * 5001)


def test_validate_entry_fields_accepts_content_with_exactly_5000_chars():
  result = validate_entry_fields('Title', '2026-04-01', 'A' * 5000)

  assert result['content'] == 'A' * 5000


def test_create_entry_from_form_strips_values_and_assigns_user(monkeypatch):
  saved_entries = []

  def fake_save(self):
    saved_entries.append(self)
    return self

  monkeypatch.setattr('app.journal.models.Entry.save', fake_save)

  form_data = {
    'title': '  My title  ',
    'date': '2026-04-01',
    'content': '  My content  ',
  }
  user = User(id=1, email='unit@example.com', password='not-saved')

  entry = create_entry_from_form(form_data, user)

  assert entry.title == 'My title'
  assert entry.date == date(2026, 4, 1)
  assert entry.content == 'My content'
  assert entry.user == user
  assert saved_entries == [entry]
