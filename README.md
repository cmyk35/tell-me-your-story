# Mini Journal

This is a super small “mini journal” project for **Web Technologies Basics (SE_19)**.

It’s still meant to stay basic on purpose, but now it has a tiny Flask backend with a few routes and one dynamic route.

## Routes / Pages

- `/` – home page  
- `/entries` – list of example entries (server-rendered)  
- `/entries/<id>` – entry detail page (dynamic route)  
- `/new` – a simple form (still doesn’t save anything yet)

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

I kept the same responsive layout:

- **below 600px:** navigation is compact
- **600px and up:** navigation has more spacing + padding
- **900px and up:** entries switch to a 2-column grid

## Small note

Entries are hardcoded in `app.py` for now. No database, no login, no saving.
