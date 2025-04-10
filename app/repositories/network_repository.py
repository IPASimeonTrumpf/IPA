from ..extensions import db

from ..models.network import Network


def create_network(ip_address, subnet_mask):
    """creates a network with the given values and returns it"""
    new_network = Network(ip=ip_address, subnet=subnet_mask)
    db.session.add(new_network)
    db.session.commit()
    return new_network


def get_network_by_id(id):
    """gets the network by the network id"""
    network = Network.query.filter(Network.id == id).first()
    return network


def get_all_networks():
    """returns all networks as a list[Network]"""
    networks = Network.query.all()
    return networks


def remove_network_by_id(id):
    """deletes the network with the given id"""
    network_to_delete = get_network_by_id(id)
    if network_to_delete != None:
        db.session.delete(network_to_delete)
        db.session.commit()
