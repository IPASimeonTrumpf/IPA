import pytest
import time

from IPA.app import create_app
from IPA.app.extensions import db
from IPA.app.models.host import Host

from IPA.app.services.host_service import (
    scan_host,
    scan_host_by_id,
    get_ports_by_host_id,
)

from IPA.app.services.network_service import add_network
from IPA.app.services.mapping_service import update_mapping_table


# Generated by ChatGPT
@pytest.fixture(scope="function")
def test_db():
    """Fixture für die Flask-Testumgebung"""
    flask_app = create_app()
    # Create the Database only in Memory for tests
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.app_context():
        db.create_all()  # Neue Tabellen für jeden Test
        update_mapping_table()
        yield flask_app  # Übergibt die Datenbank an den Test
        db.session.remove()
        db.drop_all()


# self written

# NOTE
"""I will only conduct positive tests since the validation is inside
the routes / API rather than inside the business logic.
"""


def test_create_host_success(test_db):
    add_network("127.0.0.1/32")
    host: Host = Host.query.all()[0]

    assert host.ip == "127.0.0.1"


def test_ping_scan_host_success(test_db):
    # prepare
    add_network("127.0.0.1/32")
    host: Host = Host.query.all()[0]

    # get data
    response = scan_host(host, "ping")
    assert response == "127.0.0.1 is online"
    assert host.ip == "127.0.0.1"


def test_port_scan_host_success(test_db):
    """tests if scan happens"""
    # prepare
    add_network("127.0.0.1/32")
    host: Host = Host.query.all()[0]

    # get data
    response = scan_host(host, "1000")

    with open("data.json", "w") as j:
        j.write(str(response))

    assert response[0]["port"] == 22
    assert response[0]["host"] == host
    assert "OpenSSH" in response[0]["service"]
    assert "No Results" in response[0]["vulnerabilities"]
    assert 4 == len(response[0]["vulnerabilities"].split("No Results"))


def test_port_scan_timed_host_success(test_db):
    """test if 1000 port scan takes less than 1 minute"""
    # prepare
    add_network("127.0.0.1/32")
    print(Host.query.all())
    host: Host = Host.query.all()[0]

    # get data
    start_time = time.time()
    response = scan_host(host, "1000")
    end_time = time.time()
    assert start_time + 60 > end_time


def test_scan_host_by_id_success(test_db):
    """test if port scan can be done with id"""
    # prepare
    add_network("127.0.0.1/32")
    host: Host = Host.query.all()[0]

    # get data
    response = scan_host_by_id(host.id, "1000")

    assert response == "Scan finished, scanned 3 open ports"


def test_get_ports_by_host_id_success(test_db):
    """test if port scan can be done with id"""
    # prepare
    add_network("127.0.0.1/32")
    host: Host = Host.query.all()[0]
    _ = scan_host_by_id(host.id, "1000")

    # get data
    response = get_ports_by_host_id(host.id)

    assert len(response) == 3
