# Mini Journal

This is a small “mini journal” project for **Web Technologies Basics (SE_19)**.

It stays basic on purpose, but it now has a Flask backend, a SQLite database and a few simple pages for creating, editing and deleting journal entries.

## Routes / Pages

- `/` – home page  
- `/entries` – list of saved entries from the database  
- `/entries/<id>` – edit page for one entry  
- `/new` – form for creating a new entry

## What it does

- uses Jinja templates to render the entries from the database
- lets you create, update, and delete entries
- keeps the date as a real database date field
- includes a tiny character counter on the entry forms with a bit of JavaScript
- has a few tests so the main routes and model actions stay in place

## Run it locally

1) Install dependencies:
- `pip install flask`

2) Start the server:
- `python run.py`

3) Open in your browser:
- `http://127.0.0.1:5001`

If port `5001` is taken, choose another one:
- `PORT=8000 python run.py`

## Responsive / breakpoints

I kept the same simple responsive layout:

- **below 600px:** navigation is compact
- **600px and up:** navigation has more spacing + padding
- **900px and up:** entries switch to a 2-column grid

## Small note

The app is still intentionally simple. There is no login and no fancy frontend framework, just Flask, templates and a database-backed journal.
