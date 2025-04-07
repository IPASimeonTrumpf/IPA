from datetime import datetime
from flask import Flask

from .extensions import db
from .routes.network_routes import network_blueprint

# used to update the mapping table at each run
from .services.mapping_service import update_mapping_table

def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    
    app.register_blueprint(network_blueprint)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    return app
    
