from webapp.db import db


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, index=True)
    room = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f'Table located on {self.floor} floor in room {self.room}'
