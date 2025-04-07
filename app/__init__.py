from datetime import datetime
from flask import Flask

from .extensions import db
from .routes.network_routes import network_blueprint
from .routes.host_routes import host_blueprint
from .routes.mapping_routes import mapping_blueprint


def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    
    app.register_blueprint(network_blueprint)
    app.register_blueprint(host_blueprint)
    app.register_blueprint(mapping_blueprint)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    return app
    
