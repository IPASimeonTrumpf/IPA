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


def validate(text: str):
    ''' Escapes a list of bad characters in order to secure the 
    application against most injection based attacks
    '''
    output: str = text # make a local instance for changes
    for character in ('"<>|\\&(){}[];:' + "'"):
        if character in output:
            output = output.replace(character, '\\' + character) # escape characters
    return output
