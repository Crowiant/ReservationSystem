from datetime import datetime
from dateutil import parser
from flask import Blueprint, jsonify
from sqlalchemy import and_
from webapp.auth_check import auth
from webapp.table.models import Table
from webapp.reservation.models import Reservation

blueprint = Blueprint('table', __name__, url_prefix='/table')


@blueprint.route('/')
@blueprint.route('/<int:table_id>')
@auth.login_required
def show_table(table_id=None):
    # Response all tables we have
    if not table_id:
        tables = Table.query.all()
        tables_data = [{'id': table.id, 'floor': table.floor, 'room': table.room} for table in tables]
        return jsonify(result=tables_data)

    # Response only one table and it's reservations
    if table_id <= len(Table.query.all()):
        table_reservations = Reservation.query\
            .join(Reservation.table)\
            .filter(Table.id == table_id,
                    Reservation.reservation_time_from >= datetime.now())\
            .all()
        if table_reservations:
            all_reserv = []
            for reserv in table_reservations:
                reserv_data = {'data_from': reserv.reservation_time_from,
                               'data_to': reserv.reservation_time_to
                               }
                all_reserv.append(reserv_data)
            return jsonify(result=all_reserv)
        return jsonify(result='this table have no reserv')
    return jsonify(result='no table'), 404


@blueprint.route('/<date_from>/<date_to>')
@auth.login_required
def sort_by_datetime(date_from=None, date_to=None):
    if not (date_from and date_to):
        return jsonify(result='No data'), 404

    # Validate datetime are in ISO format
    try:
        data_from_iso = parser.isoparse(date_from)
        data_to_iso = parser.isoparse(date_to)
    except ValueError:
        return jsonify(result='Bad data'), 404

    # Validate that datetimes are not in the past
    if datetime.now() > data_from_iso or datetime.now() > data_to_iso:
        return jsonify(result='No information about past')

    # Check reserv with income data in db
    have_reserv = Reservation.query\
        .join(Reservation.table)\
        .filter(and_(Reservation.reservation_time_from >= data_from_iso,
                     Reservation.reservation_time_from < data_to_iso))

    if have_reserv:
        table_ids = [t.table_id for t in have_reserv]
        raw_tables = Table.query.filter(~Table.id.in_(table_ids)).all()
        if raw_tables:
            spare_tables = [{'id': table.id, 'room': table.room, 'floor': table.floor} for table in raw_tables]
            return jsonify(free_tables_on_data=spare_tables)
        return jsonify(free_tables_on_data='No tables availible')
    else:
        raw_tables = Table.query.all()
        spare_tables = [{'id': table.id, 'room': table.room, 'floor': table.floor} for table in raw_tables]
        return jsonify(free_tables_on_data=spare_tables)
