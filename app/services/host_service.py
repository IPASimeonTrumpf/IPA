import ipaddress

from .scanner_service import scan_host, scan_hosts

from ..utils import log
from ..repositories.host_repository import create_host, get_host_by_id
from ..repositories.network_repository import create_network
from ..models.host import Host # in order to assign variables


def add_host(ip_address):
    ''' Creates a Network (using the IP-Adress and subnet 32). Therefore
    this network will only have one host and will be considered a host.
    '''
    network = create_network(ip_address=ip_address, 
                             subnet_mask='255.255.255.255') #/32
    create_host(ip_address=ip_address, network_id=network.id)
    log(f'Host: {ip_address} has been created', '+')
    return 'Host has been created'

def scan_host_by_id(id, option):
    '''will scan the specified host according to the specific option
    '''
    
    ports:int = 0
    target_host:Host = get_host_by_id(id)
    
    response = scan_host(ip=target_host.ip, option=option)
    if option == 'ping':
        return response # simply return the response
    else:
        for port_object in response:
            ports += 1
            log(f'port {port_object.port} has been added to host: {target_host.ip}', 
                '+')
    return f'Scan finished, scanned {ports} open ports'

def get_ports_by_host_id(id):
    ''' Convert port objects to dicts for ease of use in jinja2'''
    port_dicts: list[dict] = []
    host:Host = get_host_by_id(id)
    for port in host.ports:
        port_dicts.append({'port_number':port.port, 'service': port.service, 
                           'vulnerabilities':port.vulnerabilities, 
                           'scan_date':port.last_found})
    return port_dicts