# Mini Journal (Hand-in 1)

This is a small static “mini journal” website I made for **Web Technologies Basics (SE_19)**.

It’s meant to be very basic!

## Pages

* **index.html** - home page
* **entries.html** - a list of 5 example entries (static)
* **new.html** - a simple form for a new entry (doesn’t actually save anything yet)

## Run it locally

You can just open `index.html` in your browser.

If you prefer running it on localhost:

* python3 -m http.server 8000


Then open:

* `http://localhost:8000/index.html`

## Responsive / breakpoints

I used two breakpoints:

* **below 600px:** nav stacks vertically
* **600px and up:** nav becomes horizontal
* **900px and up:** entries switch to a 2-column grid

## Small note

This is only the HTML + CSS part for hand-in 1. The plan is to add backend/database stuff later.
