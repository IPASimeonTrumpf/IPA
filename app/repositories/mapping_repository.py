from ..extensions import db

from ..models.mapping import Mapping



def create_mapping(port_number, service):
    new_mapping = Mapping(port=port_number, service=service)
    db.session.add(new_mapping)

def get_mapping_by_id(id):
    mapping = mapping.query.filter(Mapping.id == id).first()
    return mapping

def get_service_by_port(port_number):
    mapping = mapping.query.filter(Mapping.port == port_number).first()
    return mapping.service