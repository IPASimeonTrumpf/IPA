from flask import Blueprint, render_template, request, jsonify

from ..utils import validate
from ..services.host_service import get_host_by_id, scan_host

host_blueprint:Blueprint = Blueprint('host', __name__, static_folder='static')

@host_blueprint.route('/hosts/<id>')
def serve_get_host_by_id(id):
    id_as_str = validate(id)
    id_as_int:int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return 'invalid id', 400
    host = get_host_by_id(id_as_int)
    if not host:
        return 'Host not found', 404
    # TODO
    # Give Jinja2 only the Parts of Host needed
    return render_template('host.html', host=host), 200
    
    
@host_blueprint.route('/scan_host', methods=['POST'])
def serve_scan_host():
    input_host_id = request.json['host_id']
    input_option = request.json['option']
    option = validate(input_option)
    try:
        host_id = int(input_host_id)
    except ValueError:
        return 'Invalid id', 400
    host = get_host_by_id(host_id)
    if not host:
        return 'Host not found', 404
    result = scan_host(host=host, option=option)
    return jsonify({'data':result}), 200
    
    
@host_blueprint.route('/results/<id>')
def get_results_of_host(id):
    id_as_str = validate(id)
    id_as_int:int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return 'invalid id', 400
    host = get_host_by_id(id_as_int)
    if not host:
        return 'Host not found', 404
    return render_template('results.html', css='', js='', host=host)

@host_blueprint.route('/export_results/<id>')
def export_results(id):
    id_as_str = validate(id)
    id_as_int:int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return 'invalid id', 400
    host = get_host_by_id(id_as_int)
    if not host:
        return 'Host not found', 404
    
    with open('../static/css/results.css', 'r') as css_file:
        css = css_file.read()
    with open('../static/js/results.js', 'r') as js_file:
        js = js_file.read()
        
    return render_template('results.html', css=css, js=js, host=host)