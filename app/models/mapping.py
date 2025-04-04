from ..extensions import db

class Mapping(db.Model):
    __tablename__ = 'mapping'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    port = db.Column(db.Integer)
    service = db.Column(db.String)