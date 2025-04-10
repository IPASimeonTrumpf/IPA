from ..extensions import db

class Mapping(db.Model):
    '''Model for SQL-Alchemy to create mapping table'''
    __tablename__ = 'mapping'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    port = db.Column(db.Integer, nullable=False, index=True)
    service = db.Column(db.String)