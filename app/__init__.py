from datetime import datetime
from flask import Flask


# Test in order to create Database
from .extensions import db

# Updating the Mapping table
from .services.mapping_service import update_mapping_table
from .services.scanner_service import port_scan_host

# Testing DB creation
from .repositories.host_repository import create_host
from .repositories.network_repository import create_network
from .repositories.port__repository import create_port
from .repositories.mapping_repository import create_mapping

def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        update_mapping_table()
        prep:list[int] = []
        for i in range(10000):
            prep.append(i)

        port_scan_host('127.0.0.1', prep)
        
    return app
    
