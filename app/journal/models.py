from app.extensions.database import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String(80))
    content = db.Column(db.Text(5000))

