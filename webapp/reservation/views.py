from flask import Blueprint, request, jsonify
from webapp.reservation.controllers import create_reservation

blueprint = Blueprint('reserv', __name__, url_prefix='/reserv')


@blueprint.route('/', methods=['POST'])
def reservation():
    try:
        guest_data = request.json['guest']
        guest_reserv = request.json['table']
    except KeyError:
        return 'No guest or table data'
    try:
        guest = {'name': guest_data['name'], 'phone': guest_data['phone'], 'email': guest_data['email']}
        req_table = {'id': guest_reserv['id'], 'data_from': guest_reserv['d_fr'], 'data_to': guest_reserv['d_to']}
    except KeyError:
        return 'Not enough data'

    db_response = create_reservation(guest, req_table)

    return jsonify(response=db_response), 201
