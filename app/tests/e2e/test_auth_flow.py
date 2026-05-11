import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_user_can_register_login_and_logout(page: Page, e2e_base_url):
  email = 'e2e-user@example.com'
  password = 'journalpass'

  page.goto(f'{e2e_base_url}/register')

  expect(page.get_by_role('heading', name='Register')).to_be_visible()

  page.get_by_label('Email').fill(email)
  page.locator('#password').fill(password)
  page.locator('#password_confirmation').fill(password)
  page.get_by_role('button', name='Create Journal Account').click()

  expect(page).to_have_url(f'{e2e_base_url}/login')
  expect(page.get_by_role('heading', name='Login')).to_be_visible()

  page.get_by_label('Email').fill(email)
  page.locator('#password').fill(password)
  page.get_by_role('button', name='Login').click()

  expect(page).to_have_url(f'{e2e_base_url}/')
  expect(page.get_by_role('button', name='Log out')).to_be_visible()
  expect(page.get_by_role('link', name='Log in')).not_to_be_visible()
  expect(page.get_by_role('link', name='Register')).not_to_be_visible()

  page.get_by_role('link', name='Entries', exact=True).click()
  expect(page).to_have_url(f'{e2e_base_url}/entries')
  expect(page.get_by_role('heading', name='All Entries')).to_be_visible()

  page.get_by_role('button', name='Log out').click()

  expect(page).to_have_url(f'{e2e_base_url}/login')
  expect(page.get_by_role('heading', name='Login')).to_be_visible()
  expect(page.get_by_role('link', name='Log in')).to_be_visible()
  expect(page.get_by_role('link', name='Register')).to_be_visible()
  expect(page.get_by_role('button', name='Log out')).not_to_be_visible()
