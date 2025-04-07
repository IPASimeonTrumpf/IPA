import os
import socket
from threading import Thread

from ..configs import NUMBER_OF_THREADS, SEARCHSPLOIT_PATH
from ..utils import get_timestamp, log, validate
from ..repositories.mapping_repository import get_service_by_port


payloads:list[bytes] = ['\r\n\r'.encode(), ''.encode()]

found_ports:list[int] = []
results_of_the_scans:list = []

def check_host_available(host):
    ''' Makes a simple Ping on the Host to check the availability
    returns True if online and False if no response / the host not 
    found
    This variable won't be sanitized since it should already be
    '''
    output = os.popen(f'ping -c 1 {host}').read()
    if 'name or service not known' in output:
        return False
    if '64 bytes from ' in output:
        return True
    if output == '':
        return False

def scan_port(host, port):
    ''' Scan a specific TCP-Port on a Host, if the port is found
    it will be:
    - added to the list of found ports (found_ports)
    - logged
    the socket has a timeout of 1 second, to make sure that the 
    scan duration can be limited / calculated
    '''
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
    ''' Simply the target for the Thread in port_scan_host
    in order to scan ports, will take a host and a list of ports
    and scan each port in the list on the host.
    '''
    while len(part_of_port_list) > 0:
        scan_port(host, part_of_port_list.pop())
        
def bannergrabbing(host, port):
    ''' Tries to find out the service by sending payloads.
    The payloads used are the global payloads, perhaps this list
    will be exported into the database in a later release.
    '''
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
    '''Used to format the Banner send, can be appended for each port
    will perhaps be appended to the database too in a later realease
    '''
    if port == 80 or port == 443:
        return banner.split('Host: ')[1].split('\r\n\r')[0]
    if port == 22:
        return banner.split('SSH-2.0-')[1]
    return banner

def scan_for_vulnerabilities(service):
    ''' utilises Searchsploit in order to try to find vulnerabilities
    by using the service. For this task the formatting of the service
    is required.
    '''
    validated_service = validate(service) # validate before executing
    command = f'{SEARCHSPLOIT_PATH} + {validated_service}'
    output = os.popen(command).read()
    return output
            
        
def port_scan_host(host, port_list):
    ''' This is the "main"-function of this application
    It will first try a connection to each port in the list
    afterwards, for each found port will try to grab the banner.
    if the bannergrabbing failed or if there was a binary response 
    it will display the default service according to IANA 
    instead / too.
    '''
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
    
def ping_scan(list_of_hosts: list[str]):
    ''' This function will simply ping each host in the
    list and return each host that responded.
    '''
    active_hosts: list[str] = []
    for host in list_of_hosts:
        if check_host_available(host):
            active_hosts.append(host)
    
    return active_hosts


def scan_host(host, option):
    global results_of_the_scans
    ''' just a simpler way of calling the correct function;
    its a mapping from option to the specific scan.
    '''
    if option == 'ping':
        # simply ping the host
        if check_host_available(host):
            return f'{host} is online'
    
    if option == '1000':
        ports: list[int] = []
        for i in range(1001):
            ports.append(i) # convert range to array
        
        
        results_of_the_scans.append(port_scan_host(host,ports))
    
    if option == 'all':
        ports: list[int] = []
        for i in range(65536):
            ports.append(i) # convert range to array
        
        results_of_the_scans(port_scan_host(host,ports))
    else:
        # specific ports comma separated
        ports_as_strings:list[str] = option.split(',')
        ports: list[int] = []
        for port_as_string in ports_as_strings:
            try:
                ports.append(int(port_as_string))
            except ValueError:
                return 'There were invalid values in the specific ports'
        results_of_the_scans.append(port_scan_host(host, ports))


def scan_hosts(hosts, option):
    ''' Just a overlay for multiple hosts, so that no more logic needs
    to happen in the other business logic
    '''
    global results_of_the_scans
    
    outputs:list = []
    threads:list[Thread] = []
    for host in hosts:
        thread = Thread(target=scan_host, args=(host, option,))
        threads.append(thread)
        thread.start() # start one thread for each host
        
    for thread in threads:
        thread.join() 
    
    # when all threads are finished return all results
    return results_of_the_scans