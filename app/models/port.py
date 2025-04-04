from ..extensions import db

class Port(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String)
    vulnerabilities = db.Column(db.String)

    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    host = db.relationship('Host', back_populates='ports')