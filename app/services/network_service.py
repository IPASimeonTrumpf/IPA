import ipaddress
from threading import Thread

from .scanner_service import scan_hosts

from ..models.network import Network # used for types

from ..repositories.host_repository import create_host
from ..repositories.network_repository import (
    create_network, 
    get_network_by_id, 
    get_all_networks, 
    remove_network_by_id
)

from ..repositories.port__repository import create_port

from ..services.scanner_service import check_host_available

from ..utils import log, get_timestamp


def get_network_data(ip_and_subnet):
    # THIS FUNCTION WAS GENERATED BY CHATGPT
    # Parse the network
    network = ipaddress.ip_network(ip_and_subnet, strict=False)

    # Subnet address
    netmask = str(network.netmask)

    # All usable IP addresses in the network (excluding network and broadcast addresses)
    usable_ips = [str(ip) for ip in network.hosts()]

    return usable_ips, netmask



def add_network(ip_with_cidr:str):
    ''' Adds a network, will be called from the index when adding a network
    '''
    # Try-Except incase invalid data
    try:
        possible_hosts, subnet_mask = get_network_data(ip_with_cidr)
    except:
        return 'Network could not be calculated, please verify your data'
    
    display_ip:str = ip_with_cidr.split('/')[0]
    created_network:Network = create_network(
        ip_address=display_ip, 
        subnet_mask=subnet_mask
    )
    network_id:int = created_network.id
    log(f'Added Network: {display_ip}', '+')
    
    threads:list[Thread] = []
    found_hosts:list[str] = []
    
    for possible_host in possible_hosts:
        # ping each host to check if they are online
        resp:bool = False
        thread = Thread(target=check_host_available, 
                        args=(possible_host,found_hosts,)
        )
        
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        # wait for threads to finish
        thread.join()
    
    if len(found_hosts) == 0:
        remove_network_by_id(network_id)
        msg = 'No hosts have been found in the Network,'
        msg += 'Network won\'t be created'
        return msg
    
    for host in found_hosts:
        # add each found host to the network    
        create_host(ip_address=host, network_id=network_id)
        log(f'Added host: {host} to network: {display_ip}', '+')
    
    return 'network has been created'

def scan_network(id, option):
    ''' The active function called when wanting to scan a network
    Expects the values are already santized
    '''
    network_to_scan:Network = get_network_by_id(id)
    results = []
    results = scan_hosts(network_to_scan.hosts, option)
    
    
    results_as_dicts = []
    if option == 'ping':
        return f'{len(results)} Hosts are online'
    
    for data in results:
        create_port(
            port_number=data['port'],
            host_id=data['host'].id,
            service=data['service'],
            vulnerabilities=data['vulnerabilities'],
            found_date=get_timestamp()
        )
        long_vulnerability =len(data['vulnerabilities']) > 100
        
        results_as_dicts.append({
            'port_number':data['port'],
            'host_id':data['host'].id,
            'service':data['service'],
            'vulnerabilities':data['vulnerabilities'],
            'vuln_long':long_vulnerability,
            'found_date':get_timestamp()
        })
        
    return results_as_dicts


def get_all_networks_formatted():
    ''' Returns all Networks in the form of dicts, instead of hosts returns
    the length, in order to distinguish between a single host and networks of
    mutliple hosts
    '''
    networks:list[Network] = get_all_networks()
    # convert the network objects to dicts for ease of use in jinja2
    network_dicts:list[dict] = []
    for network in networks:
        network_dicts.append({
            'id': network.id, 
            'ip':network.ip, 
            'subnet':network.subnet, 
            'size': len(network.hosts), 
            'hosts':network.hosts
        })
        
    return network_dicts