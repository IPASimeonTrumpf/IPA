from datetime import datetime
import time
from .configs import VERBOSE


def get_timestamp():
    return datetime.now().replace(microsecond=0)

def log(msg:str, status:str ='i'):
    if(not VERBOSE and status == 'i'):
        # informations only logged if verbose is on
        return
    print(f'[{status}] {get_timestamp()} {msg}')

