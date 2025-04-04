from ..extensions import db

from ..models.host import Host



def create_host(ip_address, network_id):
    new_host = Host(ip=ip_address, network_id=network_id)
    db.session.add(new_host)
    db.session.commit()
    return new_host

def get_host_by_id(id):
    host = Host.query.filter(Host.id == id).first()
    return host

def get_hosts_by_network_id(id):
    hosts = Host.query.filter(Host.host_id == id)
    return hosts
