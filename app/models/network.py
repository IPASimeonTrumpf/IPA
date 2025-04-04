from ..extensions import db

class Network(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ip = db.Column(db.String)
    subnet = db.Column(db.String)

    hosts = db.relationship('Host', back_populates='network', 
                            cascade='all, delete-orphan')