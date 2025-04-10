from ..extensions import db

class Host(db.Model):
    ''' Model for SQL-Alchemy to create hosts table'''
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    ip = db.Column(db.String, nullable=False) # ip of the host

    network_id = db.Column(db.Integer, db.ForeignKey("networks.id"), 
                           nullable=False)
    
    network = db.relationship('Network', back_populates='hosts')

    ports = db.relationship('Port', back_populates='host', 
                            cascade='all, delete-orphan')