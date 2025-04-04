from ..extensions import db


from ..models.mapping import Mapping



def wipe_mapping_table():
    Mapping.query.delete()
    db.session.commit()

def bulk_create_mapping(mappings: list[dict]):
    mappings_to_be_inserted = []
    for pair in mappings:
        single_mapping = Mapping(port=pair['port'], service=pair['service'])
        mappings_to_be_inserted.append(single_mapping)
    
    db.session.bulk_save_objects(mappings_to_be_inserted)
    db.session.commit()
    return len(mappings_to_be_inserted)
        

def create_mapping(port_number, service):
    new_mapping = Mapping(port=port_number, service=service)
    db.session.add(new_mapping)

def get_mapping_by_id(id):
    mapping = mapping.query.filter(Mapping.id == id).first()
    return mapping

def get_service_by_port(port_number):
    mapping = mapping.query.filter(Mapping.port == port_number).first()
    return mapping.service