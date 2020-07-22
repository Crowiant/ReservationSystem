from flask import Blueprint, jsonify
from webapp.table.models import Table

blueprint = Blueprint('table', __name__, url_prefix='/table')


@blueprint.route('/')
@blueprint.route('/<int:table_id>')
def show_table(table_id=None):
    if not table_id:
        tables = Table.query.all()
        tables_data = [{'id': table.id, 'floor': table.floor, 'room': table.room} for table in tables]
        return jsonify(result=tables_data)
    if table_id < len(Table.query.all()):
        table = Table.query.filter_by(id=table_id).first()
        table_data = {'id': table.id, 'floor': table.floor, 'room': table.room}
        return jsonify(result=table_data)
    return jsonify(result='no table'), 404

