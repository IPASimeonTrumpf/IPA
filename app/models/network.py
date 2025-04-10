from ..extensions import db


class Network(db.Model):
    """Model for SQL-Alchemy to create networks table"""

    __tablename__ = "networks"
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    ip = db.Column(db.String, nullable=False)
    subnet = db.Column(db.String)

    hosts = db.relationship(
        "Host", back_populates="network", cascade="all, delete-orphan"
    )
