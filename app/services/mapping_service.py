import urllib3

import requests

from ..utils import log, validate
from ..configs import IANA_PORT_TABLE_URL

from ..repositories.mapping_repository import bulk_create_mapping, wipe_mapping_table


def update_mapping_table():
    """Downloads a CSV-File from  IANA containing
    a mapping of ports and defaultservices
    """
    mappings: list[dict] = []
    # Disable only InsecureRequestWarning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # fetching new data
    response = requests.get(IANA_PORT_TABLE_URL, verify=False)
    csv: str = response.content.decode()
    if len(csv) < 10000:  # Check for correct size
        log("The CSV table was not downloaded correctly", "!")
        log("The Mappingtable will not be updated", "!")
        return

    wipe_mapping_table()  # reset the table
    header_line = True
    for line in csv.split("\n"):
        if header_line:  # Skip the table header
            header_line = False
            continue

        # make sure the values dont contain injections
        sanitized_line = validate(line)

        values = sanitized_line.split(",")
        if len(values) < 3:  # 3 Values needed
            continue
        if values[1] == "":  # Don't append data if no port available
            continue
        if values[2] != "tcp":  # Scope is TCP-Only
            continue
        if values[0] != "":
            # if there is a default service associated assign it
            mappings.append({"port": values[1], "service": values[0]})
        else:
            # otherwise let the user know there is no known service
            mappings.append(
                {"port": values[1], "service": "There is no default Service"}
            )
    bulk_create_mapping(mappings)
    log("updated Mappingtable to the newest data", "!")
