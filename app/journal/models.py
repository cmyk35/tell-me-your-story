from app.extensions.database import db, CRUDMixin

class Entry(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String(80))
    content = db.Column(db.String(5000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
