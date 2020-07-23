from datetime import datetime
from dateutil import parser
from webapp import db
from sqlalchemy import and_
from sqlalchemy.orm import load_only
from webapp.reservation.models import Table, Guest, Reservation
from webapp.config import SPACE_OPEN_HOUR, SPACE_CLOSE_HOUR


def create_reservation(guest, req_table):
    all_tables = Table.query.options(load_only('id')).all()
    tables_id = []
    # Validate that we have an id of table in our db
    for table in all_tables:
        tables_id.append(str(table.id))
    if req_table['id'] not in tables_id:
        return False, f"Table with id: {req_table['id']} does not exist"

    if not validate_datetime(req_table['data_from'], req_table['data_to']):
        return False, 'Datetime error'

    # Check guest in db
    guest_status = Guest.query.filter_by(phone_number=guest['phone']).first()

    # Create if guest first time reserv
    if not guest_status:
        guest_status = Guest(name=guest['name'], phone_number=guest['phone'], email=guest['email'])
        db.session.add(guest_status)

    reservations_exist = Reservation.query\
        .join(Reservation.table)\
        .filter(Table.id == req_table['id'],
                and_(Reservation.reservation_time_from >= req_table['data_from'], Reservation.reservation_time_from < req_table['data_to'])
                )\
        .all()

    if reservations_exist:
        # If found reserv in db
        return False, 'Table already reserv for this time'
    new_reservation = Reservation(guest=guest_status, table=Table.query.get(int(req_table['id'])),
                                  reservation_time_from=req_table['data_from'],
                                  reservation_time_to=req_table['data_to']
                                  )

    db.session.add(new_reservation)
    db.session.commit()
    result = 'Created'

    return True, result


def validate_datetime(date_from, date_to):
    # Validate ISO format of string
    try:
        data_from_iso = parser.isoparse(date_from)
        data_to_iso = parser.isoparse(date_to)
    except ValueError:
        return False

    # Check equal of input time
    if date_from == date_to:
        return False

    # Validate absence of values in minutes, seconds, microseconds
    time_from = data_from_iso.time()
    time_to = data_to_iso.time()
    fr_minutes, fr_seconds, fr_microseconds = time_from.minute, time_from.second, time_from.microsecond
    to_minutes, to_seconds, to_microseconds = time_to.minute, time_to.second, time_to.microsecond
    if (fr_minutes or fr_seconds or fr_microseconds) or (to_minutes or to_seconds or to_microseconds):
        return False

    # Check schedule of Space
    if (time_from < SPACE_OPEN_HOUR or time_from > SPACE_CLOSE_HOUR) or (
        time_to > SPACE_CLOSE_HOUR or time_to < SPACE_OPEN_HOUR
    ):
        return False

    # Validate that datetimes are not in the past
    if datetime.now() > data_from_iso or datetime.now() > data_to_iso:
        return False

    return True

