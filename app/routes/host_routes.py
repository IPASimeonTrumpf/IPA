from flask import Blueprint, render_template, request, jsonify

from ..utils import validate, get_timestamp
from ..services.host_service import get_host_by_id, scan_host

from ..repositories.port__repository import create_port

host_blueprint:Blueprint = Blueprint('host', __name__, static_folder='static')

@host_blueprint.route('/host/<id>')
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
    
    print(option)
    if option != '1000' and option != 'all' and option != 'ping':
        # validate specific ports
        if option.__contains__(','):
            for port in option.split(','):
                try:
                    test = int(port)
                except ValueError:
                    return 'Invalid port', 400
        else:
            return 'Invalid format for specific scan'
    print('valid')
    result = scan_host(host=host, option=option)
    json_serializable_data = []
    if option == 'ping':
        return jsonify({'msg':result})
    for data in result:
        # formatting
        long_vulnerability =len(data['vulnerabilities']) > 100
        print(long_vulnerability)
        create_port(port_number=data['port'],host_id=data['host'].id,service=data['service'],vulnerabilities=data['vulnerabilities'],
                    found_date=get_timestamp())
        json_serializable_data.append({'port_number':data['port'],
                                       'host_id':data['host'].id,
                                       'service':data['service'],
                                       'vulnerabilities':data['vulnerabilities'],
                                       'vuln_long':long_vulnerability,
                                       'found_date':get_timestamp()})
        
    return jsonify({'data':json_serializable_data}), 200
    
    
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
    print(id)
    id_as_str = validate(id)
    print(id_as_str)
    id_as_int:int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return 'invalid id', 400
    host = get_host_by_id(id_as_int)
    if not host:
        return 'Host not found', 404
        
    return render_template('result_for_export.html', host=host)