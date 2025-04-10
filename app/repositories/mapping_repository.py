from ..extensions import db


from ..models.mapping import Mapping


def wipe_mapping_table():
    """Delete the whole mapping-table"""
    Mapping.query.delete()
    db.session.commit()


def bulk_create_mapping(mappings: list[dict]):
    """takes a list of dictionaries containing:
    port: the port as an integer
    service: the service as a string
    and creates a entry in the mapping table with this values
    """
    mappings_to_be_inserted = []
    for pair in mappings:
        single_mapping = Mapping(port=pair["port"], service=pair["service"])
        mappings_to_be_inserted.append(single_mapping)

    db.session.bulk_save_objects(mappings_to_be_inserted)
    db.session.commit()
    return len(mappings_to_be_inserted)


def get_service_by_port(port_number):
    """get the service using the portnumber as a filter option
    returns 'no default Service found' instead of None in order to display
    it no matter if its in the table
    """
    mapping = Mapping.query.filter(Mapping.port == port_number).first()
    if mapping == None:
        return "No default Service found"
    return mapping.service
