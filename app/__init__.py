from datetime import datetime
from flask import Flask


# Test in order to create Database

from .extensions import db

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
        
        network = create_network('192.168.1.1','255.255.255.0')
        host = create_host('192.168.1.110', network.id)
        port = create_port(1337, host.id, 'elite', 'none', datetime.now().
                            replace(microsecond=0))
        
    return app
    
