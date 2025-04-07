from ..extensions import db

from ..models.port import Port



def create_port(port_number, host_id, service=None, vulnerabilities=None, 
                found_date=None):
    new_port = Port(port=port_number, host_id=host_id, service=service,
                vulnerabilities=vulnerabilities, last_found=found_date)

    db.session.add(new_port)
    db.session.commit()
    return new_port

def get_port_by_id(id):
    port = Port.query.filter(Port.id == id).first()
    return port

