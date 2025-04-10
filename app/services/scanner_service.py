import os
import socket
from sqlalchemy import text, create_engine
from threading import Thread

from ..configs import NUMBER_OF_THREADS, SEARCHSPLOIT_PATH, PAPER, PAYLOADS
from ..utils import get_timestamp, log, validate
from ..repositories.mapping_repository import get_service_by_port


def check_host_available(host:str, found_hosts=None):
    ''' Makes a simple Ping on the Host to check the availability
    returns True if online and False if no response / the host not 
    found
    This variable won't be sanitized since it should already be
    there is a timeout of 2 seconds in the ping
    '''
    output = os.popen(f'ping -c 1 -W 2 {host}').read()
    if '64 bytes from ' in output:
        if found_hosts != None:
            found_hosts.append(host)
        return True
    if output == '':
        return False
    

def scan_port(host, port, found_ports):
    ''' Scan a specific TCP-Port on a Host, if the port is found
    it will be:
    - added to the list of found ports (found_ports)
    - logged
    the socket has a timeout of 1 second, to make sure that the 
    scan duration can be limited / calculated
    '''
    
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Ipv4
    socket_instance.settimeout(1)
    try:
        socket_instance.connect((host, port))
        socket_instance.close()
        found_ports.append(port)
        log(f'found port: {port} on host: {host}', '+')
    except (ConnectionRefusedError, ConnectionError, TimeoutError):
        socket_instance.close()

def worker(host, part_of_port_list, found_ports):
    ''' Simply the target for the Thread in port_scan_host
    in order to scan ports, will take a host and a list of ports
    and scan each port in the list on the host.
    '''
    while len(part_of_port_list) > 0:
        scan_port(host, part_of_port_list.pop(), found_ports)
        
def bannergrabbing(host, port):
    ''' Tries to find out the service by sending payloads.
    The payloads used are the global payloads, perhaps this list
    will be exported into the database in a later release.
    '''
    
    for payload in PAYLOADS:
        # create a tcp Ipv4 socket
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.settimeout(1)
        try:
            log(f'grabbing banner on {host}:{port}','i')
            socket_instance.connect((host,port))
            socket_instance.send(payload)
            
            # try to get the banner as a response
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
    if port == 80 or port == 443 or port == 5000:
        try:
            return banner.split('Server: ')[1].split('\n')[0]
        except:
            return f'No Server header found at port : {port}'
    if port == 22:
        return banner.split('SSH-2.0-')[1].split('\n')[0]
    return banner

def scan_for_vulnerabilities(service):
    ''' utilises Searchsploit in order to try to find vulnerabilities
    by using the service. For this task the formatting of the service
    is required.
    '''
    command = f'{SEARCHSPLOIT_PATH} {service}'
    try:
        output = os.popen(command).read()
    except ValueError:
        output = 'Searchsploit crashed'
    if not PAPER:
        output.split('Papers')[0]
    return output
            
        
def port_scan_host(host, port_list, is_threaded=False):
    ''' It will first try a connection to each port in the list
    afterwards, for each found port will try to grab the banner.
    if the bannergrabbing failed or if there was a binary response 
    it will display the default service according to IANA 
    instead / too.
    
    As a security measure, all Data that comes from external sources
    (the output from searchsploit and the response from a tcp service)
    '''
    found_ports = []
    threads: list[Thread] = []
    results: list[dict] = []
    num_threads = NUMBER_OF_THREADS
    # Assign each thread a fraction of the ports to scan
    if(len(port_list) < num_threads):
        num_threads = len(port_list)
    task_size = len(port_list) / num_threads
    log(f'starting scan {get_timestamp()}')
    
    for i in range(num_threads):
        # take all Ports and splitt it so each Thread
        # will take a fraction of the ports
        ports_for_thread = port_list[int(i*task_size):int((i+1)*task_size)]
        
        # Then start all the threads
        new_thread = Thread(
            target=worker, 
            args=(
                host.ip, 
                ports_for_thread,
                found_ports,    
            )
        )
        
        new_thread.start()
        threads.append(new_thread)
        
    for thread in threads:
        # wait for the threads to finish before going further
        thread.join()
        
    log(f'found all ports at {get_timestamp()}')
    
    scan_time = get_timestamp()
    for port in found_ports:
        service: str
        
        # Getting the Service
        banner, readable = bannergrabbing(host.ip, port)
        if banner != '': # if there is a banner format it
            service = format_banner(banner, port)
        
        # if its not clear what service is running, get the default
        if not readable:
            if is_threaded:
                # workaround because no application context in thread
                
                # create a second engine
                engine = create_engine('sqlite:///instance/database.db')
                
                # with the second engine, read the default service
                with engine.connect() as conn:
                    command = 'SELECT service FROM mapping WHERE port = :port'
                    query = text(command)
                    mapping_answer = conn.execute(query, {'port': int(port)})
                    service = mapping_answer.first()
                    # set the default service
                    if service == None:
                        default_service = "No default Service found"
                    else:
                        default_service = service[0]
                        
                service = banner + default_service
                
            else:
                # if application context is available, use the repo
                default_service = get_service_by_port(int(port))
                service = banner + default_service

        # validate the data, since its from an external source
        service = validate(service)
        
        # log the found service
        log(f'set service: {service} for port: {port}', '+')
        
        # Searching for vulnerabilities
        vulnerabilities = scan_for_vulnerabilities(service)
        
        log(f'Found a vulnerability for service: {service}')
        # validate the data, since its from an external source
        validated_vulnerabilites = validate(vulnerabilities)


        # Collect all the data
        results.append({
            'port':port, 
            'host':host, 
            'service': service, 
            'vulnerabilities': validated_vulnerabilites, 
            'last_found': scan_time
        })
        
    
    # log and return results
    
    log(f'ended the Portscan on {host.ip} {get_timestamp()}')

    return results
    
def ping_scan(list_of_hosts: list[str]):
    ''' This function will simply ping each host in the
    list and return each host that responded as a list[str]
    '''
    active_hosts: list[str] = []
    for host in list_of_hosts:
        # ping host to check
        if check_host_available(host):
            active_hosts.append(host)
    
    return active_hosts


def scan_host(host, option, return_array:list=None):
    ''' This is an overlay over all previous functions, in order to select
    the correct method.
    '''
    # formatted for frontend
    results_as_dicts:list[dict] = []
    
    log(f'Starting "{option}" Scan at {get_timestamp()}', '!')
    
    # if its a ping scan no need to calculate ports
    if option == 'ping':
        # simply ping the host
        if check_host_available(host.ip):
            if return_array != None:
                # if running threaded return it per array
                return_array.append(f'{host.ip} is online')
                
            return f'{host.ip} is online'
        else:
            return f'{host.ip} is not online'
        
    # portscan
    ports: list[int] = []
    
    # Make list of ports
    if option == '1000':
        ports: list[int] = []
        for i in range(1001):
            ports.append(i) # convert range to array

    if option == 'all':
        for i in range(65536):
            ports.append(i) # convert range to array
    
    if ',' in option:
        for port_as_string in option.split(','):
            try:
                # convert all ports to numbers
                ports.append(int(port_as_string))
            except (TypeError, ValueError):
                return 'There were invalid values in the specific ports'
    
    # start the scan
    results = port_scan_host(host,ports,is_threaded=True)

    for result in results:
        # return the value according to the used method
        # (return / parameter)
        if return_array != None:
                return_array.append(result)
    
    return results
            

def scan_hosts(hosts, option):
    ''' This function applies scan_host on each host in the parameter
    In order to achieve good efficiency each host gets a thread. 
    '''

    
    outputs:list = []
    threads:list[Thread] = []
    # pass the function an array to store the results in
    return_array = []
    
    for host in hosts:
        thread = Thread(target=scan_host, args=(host, option,return_array,))
        threads.append(thread)
        thread.start() # start one thread for each host
        
    for thread in threads:
        thread.join()

    return return_array