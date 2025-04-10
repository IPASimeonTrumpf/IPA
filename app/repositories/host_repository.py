from ..extensions import db

from ..models.host import Host



def create_host(ip_address, network_id):
    ''' Creates a host with the given address, the host will be inside
    the network with the network_id.
    '''
    new_host = Host(ip=ip_address, network_id=network_id)
    db.session.add(new_host)
    db.session.commit()
    return new_host

def get_host_by_id(id):
    ''' Returns the Host by the id, will return None if no host is found'''
    host = Host.query.filter(Host.id == id).first()
    return host

