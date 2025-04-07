from flask import Blueprint, jsonify

from ..services.mapping_service import update_mapping_table

mapping_blueprint = Blueprint('mapping', __name__, static_folder='static')

@mapping_blueprint.route('/update_data')
def update_data():
    update_mapping_table()
    return 'renewed data'