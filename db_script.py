from webapp import create_app
from webapp.db import db
from webapp.reservation.models import Table

app = create_app()


def make_table(id, floor, room):
    new_table = Table(id=id, floor=floor, room=room)
    db.session.add(new_table)
    db.session.commit()


with app.app_context():
    table_id = 0
    for floor in range(1, 3):
        for room in range(1, 11):
            table_id += 1
            make_table(table_id, floor, room)


