from webapp import db


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Guest {self.name}>'
