from ..extensions import db

from ..models.network import Network



def create_network(ip_address, subnet_mask):
    new_network = Network(ip=ip_address, subnet=subnet_mask)
    db.session.add(new_network)
    db.session.commit()
    return new_network
    

def get_network_by_id(id):
    network = Network.query.filter(Network.id == id).first()
    return network

def get_all_networks():
    networks = Network.query.all()
    return networks
