from webapp import db
from webapp.table.models import Table


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship('Guest')
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table')
    reservation_time_from = db.Column(db.String, index=True)
    reservation_time_to = db.Column(db.String, index=True)


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f'<Guest {self.name}>'