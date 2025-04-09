from flask import Blueprint, render_template, request, jsonify

from ..utils import validate
from ..services.network_service import add_network, get_all_networks_formatted, get_network_by_id, scan_network

network_blueprint:Blueprint = Blueprint('network', __name__, static_folder='static')

@network_blueprint.route('/')
def index():
    return render_template('index.html')

@network_blueprint.route('/create_network', methods=['POST'])
def serve_create_network():
    json_data = request.json['ip_with_cidr']
    ip_with_cidr = validate(json_data)
    print(json_data)
    if not ip_with_cidr.__contains__('/'):
        return 'No / was supplied', 400
    # validation of IP-Adress
    ip = ip_with_cidr.split('/')[0]
    if not ip.__contains__('.') or len(ip.split('.')) != 4:
        return 'not a valid IP-Adress, format: xxx.xxx.xxx.xxx', 400
    for part in ip.split('.'):
        try:
            part = int(part)
            if part > 255 or part < 0:
                return f'IP contains invalid value: {part}', 400
        except ValueError:
            return 'IP contains non-numeric contents', 400
    
    # Validate CIDR
    cidr_as_string = ip_with_cidr.split('/')[1]
    try:
        cidr = int(cidr_as_string)
    except ValueError:
        return 'Invalid CIDR', 400
    if cidr > 32 or cidr < 24:
        return 'CIDR is not between 23 and 33, therefore invalid', 400
    
    
    
    response = add_network(ip_with_cidr)
    
    if response == 'network has been created':
        return jsonify({'msg': response}), 201
    else:
        return response, 400
    
@network_blueprint.route('/overview')
def overview():
    networks = get_all_networks_formatted()
    print(networks)
    return render_template('overview.html', networks=networks)


@network_blueprint.route('/network/<id>')
def serve_network(id):
    id_as_string = validate(str(id)) # validate User-Input
    try:
        network_id = int(id_as_string)
    except ValueError:
        return 'Invalid id', 400
    network = get_network_by_id(network_id)
    if not network:
        return 'Network not found', 404
    return render_template('network.html', network=network)


@network_blueprint.route('/scan_network', methods=['POST'])
def serve_scan_network():
    input_network_id = request.json['network_id']
    input_option = request.json['option']
    print(input_option)
    input_network_id_as_string = validate(input_network_id)
    option = validate(input_option)
    try:
        network_id = int(input_network_id_as_string)
    except ValueError:
        return 'Id was not a Integer, please submit a valid id', 400
    
    if option != '1000' and option != 'all' and option != 'ping':
        # validate specific ports
        if option.__contains__(','):
            for port in option.split(','):
                try:
                    test = int(port)
                except ValueError:
                    return 'Invalid port', 400
        else:
            return 'Invalid format for specific scan', 400
    
    response = scan_network(id=network_id, option=option)
    print('response')
    print(response)
    if option == 'ping':
        return jsonify({'msg':response})
    for result in response:
        print(result)
        # format
    print(response)
    return jsonify({'msg':response})