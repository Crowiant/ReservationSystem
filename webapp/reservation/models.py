from webapp import db
from webapp.auth.models import Guest


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, index=True)
    room = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f'Table located on {self.floor} floor in room {self.room}'


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship('Guest')
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table')
    reservation_time_from = db.Column(db.DateTime, index=True)
    reservation_time_to = db.Column(db.DateTime, index=True)
