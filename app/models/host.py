from ..extensions import db

class Host(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ip = db.Column(db.String, nullable=False)

    network_id = db.Column(db.Integer, db.ForeignKey("networks.id"), 
                           nullable=False)
    network = db.relationship('Network', back_populates='hosts')

    ports = db.relationship('Port', back_populates='host', 
                            cascade='all, delete-orphan')