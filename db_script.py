from webapp import create_app
from webapp.db import db
from webapp.reservation.models import Table

app = create_app()


def make_table(id, floor, room):
    new_table = Table(id=id, floor=floor, room=room)
    db.session.add(new_table)
    db.session.commit()


with app.app_context():
    id = 0
    for floor in range(2):
        for room in range(10):
            id += 1
            make_table(id, floor, room)


