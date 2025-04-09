""" In this file are some variables defined that can be configured
feel free to play around and configure until you like it the most
"""

IANA_PORT_TABLE_URL = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"
VERBOSE = False
NUMBER_OF_THREADS = 40 # number of threads, the higher the faster, keep down if scanning networks, since each host will have one too
SEARCHSPLOIT_PATH = '/opt/exploitdb/searchsploit' # path to searchsploit or similar function
NO_PAPER = True # Whether or not to include Papers written about exploits
