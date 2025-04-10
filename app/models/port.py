from ..extensions import db


class Port(db.Model):
    """Model for SQL-Alchemy to create ports table"""

    __tablename__ = "ports"
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    port = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String)
    vulnerabilities = db.Column(db.String)
    last_found = db.Column(db.Date)

    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    host = db.relationship("Host", back_populates="ports")
