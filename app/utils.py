from datetime import datetime
import time
from .configs import VERBOSE

def log(msg:str, status:str ='i'):
    if(not VERBOSE and status == 'i'):
        # informations only logged if verbose is on
        return
    timestamp = datetime.now().replace(microsecond=0)
    print(f'[{status}] {timestamp} {msg}')

        