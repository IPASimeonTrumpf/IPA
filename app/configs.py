""" In this file are some variables defined that can be configured
feel free to play around and configure until you like it the most
"""
# General logging
VERBOSE :bool = False

# Datasource, not recommended to change
IANA_PORT_TABLE_URL :str = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"

# Scanner Logic:
# How many threads will be used (Per Host), keep down for network scans
NUMBER_OF_THREADS :int = 40
# path to the searchsploit executable, can be exchanged for any similar tool
SEARCHSPLOIT_PATH :str = '/opt/exploitdb/searchsploit'
# specific to searchsploit, whether or not to include papers, default False
PAPER :bool = False
# Payloads for Bannergrabbing
PAYLOADS :list[bytes] = ['\r\n\r'.encode(), ''.encode(), ("HEAD / HTTP/1.1\r\n" + 
                        "Host: example.com\r\n" + 
                        "Connection: close\r\n\r\n").encode()]