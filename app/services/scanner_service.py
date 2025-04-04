import ipaddress
import os
import socket
from threading import Thread

from ..configs import NUMBER_OF_THREADS, SEARCHSPLOIT_PATH
from ..utils import get_timestamp, log
from ..repositories.mapping_repository import get_service_by_port


payloads:list[bytes] = ['\r\n\r'.encode(), ''.encode()]

found_ports:list[int] = []

def scan_port(host, port):
    global found_ports
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Ipv4
    socket_instance.settimeout(1)
    try:
        socket_instance.connect((host, port))
        socket_instance.close()
        found_ports.append(port)
        log(f'found port: {port} on host: {host}', '+')
    except (ConnectionRefusedError, ConnectionError, TimeoutError):
        socket_instance.close()

def worker(host, part_of_port_list):
    while len(part_of_port_list) > 0:
        scan_port(host, part_of_port_list.pop())
        
def bannergrabbing(host, port):
    global payloads
    for payload in payloads:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.settimeout(1)
        try:
            socket_instance.connect((host,port))
            socket_instance.send(payload)
            response = socket_instance.recv(1024)
            if(len(response) < 2):
                continue
            else:
                socket_instance.close()
                try:
                    
                    return response.decode(), True
                except ValueError:
                    banner = 'The Service responded binary: ' + str(response)
                    return banner, False
                
        except (TimeoutError, ConnectionRefusedError, ConnectionResetError):
            socket_instance.close()
            pass
    return '', False

def format_banner(banner, port):
    """ Used to format the Banner send, can be appended for each port
    """
    if port == 80 or port == 443:
        return banner.split('Host: ')[1].split('\r\n\r')[0]
    if port == 22:
        return banner.split('SSH-2.0-')[1]
    return banner

def scan_for_vulnerabilities(service):
    command = f'{SEARCHSPLOIT_PATH} + {service}'
    output = os.popen(command).read()
    return output
            
        
def port_scan_host(host, port_list):
    """ Will first try a connection to each port in the list
    afterwards, for each found port will try to grab the banner.
    if failed or binary response will display the default service too
    """
    global found_ports
    found_ports = []
    threads: list[Thread] = []
    results: list[dict] = []
    num_threads = NUMBER_OF_THREADS
    # Assign each thread a fraction of the ports to scan
    if(len(port_list) < num_threads):
        num_threads = port_list
    task_size = len(port_list) / num_threads
    log(f'starting scan {get_timestamp()}', '!')
    for i in range(num_threads):
        ports_for_thread = port_list[int(i*task_size):int((i+1)*task_size)]
        new_thread = Thread(target=worker, args=[host, ports_for_thread,])
        new_thread.start()
        threads.append(new_thread)
    for thread in threads:
        thread.join()
        
    log(f'found all ports {get_timestamp()}', '!')
    
    scan_time = get_timestamp()
    for port in found_ports:
        service: str
        # Getting the Service
        banner, readable = bannergrabbing(host, port) # False / Banner 'bin' / 'str'
        if banner != '': # if there is a banner format it
            service = format_banner(banner, port)
            log(f'Found banner: {service}', '+')
        if not readable:
            default_service = get_service_by_port(port)
            service = banner + default_service
        
        # Searching for vulnerabilities
        vulnerabilities = scan_for_vulnerabilities(service)
        results.append({'port':port, 'host':host, 'service': service, 
                        'vulnerabilities': vulnerabilities, 
                        'last_found': scan_time})
    log(f'ended scan {get_timestamp()}', '!')
    return results
    
