from webapp import db
from webapp.auth.models import Guest
from webapp.table.models import Table


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship('Guest')
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table')
    reservation_time_from = db.Column(db.String, index=True)
    reservation_time_to = db.Column(db.String, index=True)
